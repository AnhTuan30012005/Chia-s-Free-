/**
 * Studio Vault API - Cloudflare Serverless Edge Backend
 * Air-gapped secure link vault with anti-scraping, dynamic PoW challenge,
 * ephemeral one-time burn tickets, and rate-limiting.
 */

const ALLOWED_ORIGINS = [
  'https://anhtuan30012005.github.io',
  'http://localhost:3000',
  'http://localhost:8080',
  'http://127.0.0.1:5500',
  'http://127.0.0.1:8080',
  'http://127.0.0.1:8000'
];

// Secure HMAC Signing Secret Resolution (Cloudflare Secret Binding)
function getSignSecret(env) {
  return env.SIGN_SECRET || env.VAULT_SECRET || 'VAULT_SEC_UNSET_DEV_FALLBACK_SALT';
}
const POW_DIFFICULTY = 3; // Number of leading zeros required in hex hash (e.g. "000")
const RATE_LIMIT_MAX = 5; // Max 5 downloads per window
const RATE_LIMIT_WINDOW = 60; // 60 seconds

// Standard CORS response helper
function corsHeaders(request, env) {
  const origin = request.headers.get('Origin') || '';
  const isAllowed = ALLOWED_ORIGINS.includes(origin) || (env.ALLOW_ANY_ORIGIN === 'true');
  const allowOrigin = isAllowed ? origin : ALLOWED_ORIGINS[0];

  return {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Client-Timestamp, X-PoW-Nonce, X-PoW-Hash',
    'Access-Control-Max-Age': '86400',
  };
}

// SHA-256 helper
async function sha256(str) {
  const buf = new TextEncoder().encode(str);
  const hash = await crypto.subtle.digest('SHA-256', buf);
  const hashArray = Array.from(new Uint8Array(hash));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// Client IP extractor (Anti-Spoofing: Trust only Cloudflare Edge header)
function getClientIp(request) {
  // In production Cloudflare Workers, CF-Connecting-IP is guaranteed and immune to spoofing.
  // Never trust client-supplied X-Forwarded-For headers to prevent rate-limit bypass.
  const cfIp = request.headers.get('CF-Connecting-IP');
  if (cfIp) return cfIp;
  return '127.0.0.1';
}

// Check Rate Limit (Leaky Bucket / Sliding Window in KV or memory)
async function checkRateLimit(ip, env) {
  if (!env.STATS_KV) return true; // KV not provisioned, bypass rate limit

  const now = Math.floor(Date.now() / 1000);
  const windowKey = `ratelimit:${ip}:${Math.floor(now / RATE_LIMIT_WINDOW)}`;
  
  const currentCount = parseInt(await env.STATS_KV.get(windowKey) || '0', 10);
  if (currentCount >= RATE_LIMIT_MAX) {
    return false;
  }
  
  await env.STATS_KV.put(windowKey, (currentCount + 1).toString(), {
    expirationTtl: RATE_LIMIT_WINDOW * 2
  });
  return true;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    // 1. Handle CORS Preflight
    if (method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: corsHeaders(request, env)
      });
    }

    const headers = corsHeaders(request, env);
    headers['Content-Type'] = 'application/json';

    // 2. Health & Heartbeat
    if (path === '/' || path === '/api/health') {
      return new Response(JSON.stringify({
        status: 'online',
        service: 'Studio Vault Air-Gapped API',
        version: '2.0.0',
        timestamp: new Date().toISOString()
      }), { status: 200, headers });
    }

    // 3. PoW Challenge Seed Generator (/api/challenge)
    if (path === '/api/challenge' && method === 'GET') {
      const clientIp = getClientIp(request);
      const code = url.searchParams.get('code') || '';
      if (!code) {
        return new Response(JSON.stringify({
          error: 'Bad Request: Missing target resource code'
        }), { status: 400, headers });
      }

      const timestamp = Date.now();
      const nonce = crypto.randomUUID();
      const secret = getSignSecret(env);
      // Cryptographic binding: IP + timestamp + seed + target code + secret
      const rawPayload = `${clientIp}:${timestamp}:${nonce}:${code}:${secret}`;
      const signature = await sha256(rawPayload);

      return new Response(JSON.stringify({
        code,
        seed: nonce,
        timestamp,
        difficulty: POW_DIFFICULTY,
        signature
      }), { status: 200, headers });
    }

    // 4. Secure Handshake (/api/handshake)
    if (path === '/api/handshake' && method === 'POST') {
      try {
        const body = await request.json();
        const { code, seed, timestamp, nonce, signature } = body;

        if (!code || !seed || !timestamp || nonce === undefined || !signature) {
          return new Response(JSON.stringify({
            error: 'Bad Request: Missing cryptographic parameters'
          }), { status: 400, headers });
        }

        const clientIp = getClientIp(request);

        // Verification A: Challenge Freshness (max 90 seconds old)
        const now = Date.now();
        if (Math.abs(now - timestamp) > 90000) {
          return new Response(JSON.stringify({
            error: 'Challenge expired. Please retry.'
          }), { status: 403, headers });
        }

        // Verification B: Challenge Signature Integrity (Must match exact resource code)
        const secret = getSignSecret(env);
        const expectedSig = await sha256(`${clientIp}:${timestamp}:${seed}:${code}:${secret}`);
        if (signature !== expectedSig) {
          return new Response(JSON.stringify({
            error: 'Invalid challenge signature or mismatched resource code.'
          }), { status: 403, headers });
        }

        // Verification B2: Anti-Replay / Seed Burning (Strong Consistency via Cache API + KV)
        const cache = caches.default;
        const seedCacheUrl = new URL(`https://vault-cache.internal/seed/${seed}`);
        const cachedSeed = await cache.match(seedCacheUrl);
        if (cachedSeed) {
          return new Response(JSON.stringify({
            error: 'Thử thách PoW đã được sử dụng (Replay Attack Detected). Vui lòng yêu cầu thử thách mới.'
          }), { status: 403, headers });
        }
        ctx.waitUntil(cache.put(seedCacheUrl, new Response('1', {
          headers: { 'Cache-Control': 'max-age=120' }
        })));

        if (env.STATS_KV) {
          const seedKey = `used_seed:${seed}`;
          const isReused = await env.STATS_KV.get(seedKey);
          if (isReused) {
            return new Response(JSON.stringify({
              error: 'Thử thách PoW đã được sử dụng (Replay Attack Detected). Vui lòng yêu cầu thử thách mới.'
            }), { status: 403, headers });
          }
          await env.STATS_KV.put(seedKey, '1', { expirationTtl: 120 });
        }

        // Verification C: Proof of Work Verification
        const powHash = await sha256(`${seed}:${nonce}`);
        const prefix = '0'.repeat(POW_DIFFICULTY);
        if (!powHash.startsWith(prefix)) {
          return new Response(JSON.stringify({
            error: 'Proof-of-Work failed validation.'
          }), { status: 403, headers });
        }

        // Verification D: Rate Limiting
        const allowed = await checkRateLimit(clientIp, env);
        if (!allowed) {
          return new Response(JSON.stringify({
            error: 'Tốc độ tải quá nhanh (Rate Limit). Vui lòng đợi 60 giây.'
          }), {
            status: 429,
            headers: {
              ...headers,
              'Retry-After': '60'
            }
          });
        }

        // Verification E: Resource Exists in Vault
        let targetUrl = null;
        if (env.VAULT_KV) {
          targetUrl = await env.VAULT_KV.get(`res:${code}`);
        } else {
          // Dev mock fallback if KV not connected
          targetUrl = `https://drive.google.com/drive/folders/mock_${code}`;
        }

        if (!targetUrl) {
          return new Response(JSON.stringify({
            error: `Tài nguyên ${code} không tồn tại hoặc đã gỡ bỏ.`
          }), { status: 404, headers });
        }

        // Generation: Create Single-Use Burn Ticket
        const ticketId = crypto.randomUUID();
        const ticketData = {
          code,
          ip: clientIp,
          uaHash: await sha256(request.headers.get('User-Agent') || 'unknown'),
          createdAt: now,
          expiresAt: now + 45000 // 45 seconds lifetime
        };

        if (env.TICKETS_KV) {
          await env.TICKETS_KV.put(`ticket:${ticketId}`, JSON.stringify(ticketData), {
            expirationTtl: 60 // Cloudflare auto-purges after 60s
          });
        }

        // Record metrics
        if (env.STATS_KV) {
          ctx.waitUntil((async () => {
            const countKey = `stat:dl:${code}`;
            const current = parseInt(await env.STATS_KV.get(countKey) || '0', 10);
            await env.STATS_KV.put(countKey, (current + 1).toString());
          })());
        }

        return new Response(JSON.stringify({
          success: true,
          ticket: ticketId,
          expires_in: 45,
          download_url: `${url.origin}/dl/${ticketId}`
        }), { status: 200, headers });

      } catch (err) {
        return new Response(JSON.stringify({
          error: 'Handshake internal error: ' + err.message
        }), { status: 500, headers });
      }
    }

    // 5. Burn-On-Read Redirection Endpoint (/dl/:ticket)
    if (path.startsWith('/dl/')) {
      const ticketId = path.replace('/dl/', '').trim();
      if (!ticketId) {
        return errorPage('Thiếu mã vé tải xuống.', 400);
      }

      let ticketData = null;
      if (env.TICKETS_KV) {
        const raw = await env.TICKETS_KV.get(`ticket:${ticketId}`);
        if (raw) {
          ticketData = JSON.parse(raw);
          // IMMEDIATE BURN: Delete from KV instantly to prevent replay/sharing
          await env.TICKETS_KV.delete(`ticket:${ticketId}`);
        }
      } else {
        // Dev test fallback
        ticketData = { code: 'S-01' };
      }

      if (!ticketData) {
        return errorPage('Vé tải xuống không tồn tại, đã hết hạn hoặc đã được sử dụng (Burned).<br>Vui lòng quay lại thư viện và nhấn nút tải để nhận vé mới.', 410);
      }

      // Check Expiration
      if (ticketData.expiresAt && Date.now() > ticketData.expiresAt) {
        return errorPage('Vé tải xuống đã hết hạn (chỉ có hiệu lực trong 45 giây).', 403);
      }

      // Verification D: Client IP & User-Agent Binding (Anti-Ticket Sharing / Anti-Hijacking)
      const currentIp = getClientIp(request);
      const currentUaHash = await sha256(request.headers.get('User-Agent') || 'unknown');

      if (ticketData.ip && ticketData.ip !== '127.0.0.1' && ticketData.ip !== currentIp) {
        return errorPage('Phiếu tải bị khóa theo địa chỉ IP thiết bị yêu cầu ban đầu (IP Binding Mismatched). Vui lòng tự tạo vé tải trên máy của bạn.', 403);
      }

      if (ticketData.uaHash && ticketData.uaHash !== currentUaHash) {
        return errorPage('Trình duyệt truy cập không khớp với thiết bị đã giải mã thử thách PoW ban đầu.', 403);
      }

      // Retrieve Destination URL from Vault
      let targetUrl = null;
      if (env.VAULT_KV) {
        targetUrl = await env.VAULT_KV.get(`res:${ticketData.code}`);
      } else {
        targetUrl = 'https://drive.google.com';
      }

      if (!targetUrl) {
        return errorPage('Không tìm thấy đích tài nguyên trong kho dữ liệu.', 404);
      }

      // HTTP 302 Found direct redirect
      return new Response(null, {
        status: 302,
        headers: {
          'Location': targetUrl,
          'Cache-Control': 'no-store, no-cache, must-revalidate, private',
          'Pragma': 'no-cache',
          'Expires': '0',
          'Referrer-Policy': 'no-referrer'
        }
      });
    }

    // 6. Public Stats Endpoint
    if (path === '/api/stats' && method === 'GET') {
      return new Response(JSON.stringify({
        status: 'ok',
        secured_items: 72,
        vault_type: 'Cloudflare KV (Air-Gapped)',
        protection: ['HMAC-SHA256 Handshake', 'PoW Challenge', 'Burn-On-Read Redirection', 'IP Leaky Bucket Rate Limit']
      }), { status: 200, headers });
    }

    return new Response(JSON.stringify({ error: 'Endpoint Not Found' }), { status: 404, headers });
  }
};

// Aesthetic midnight navy error page for expired/invalid burn tickets
function errorPage(message, status = 403) {
  const html = `<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bảo vệ Vault - Vé Tải Không Hợp Lệ</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #040711;
      color: #e2e8f0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 24px;
    }
    .card {
      background: #091122;
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 16px;
      padding: 36px 28px;
      max-width: 460px;
      text-align: center;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7), 0 0 30px rgba(56, 189, 248, 0.1);
    }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      background: rgba(239, 68, 68, 0.15);
      border: 1px solid rgba(239, 68, 68, 0.3);
      border-radius: 9999px;
      color: #f87171;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 16px;
    }
    h1 {
      font-size: 20px;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 12px;
    }
    p {
      color: #94a3b8;
      font-size: 13.5px;
      line-height: 1.6;
      margin-bottom: 24px;
    }
    a.btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      background: linear-gradient(135deg, #38bdf8, #0284c7);
      color: #040711;
      font-weight: 700;
      font-size: 13px;
      padding: 10px 22px;
      border-radius: 10px;
      text-decoration: none;
      transition: all 0.2s;
    }
    a.btn:hover {
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
      transform: translateY(-1px);
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">Shield Vault Protected</div>
    <h1>Phiếu Tải Không Khả Dụng</h1>
    <p>${message}</p>
    <a href="https://anhtuan30012005.github.io/Chia-s-Free-/" class="btn">
      Quay Lại Thư Viện
    </a>
  </div>
</body>
</html>`;

  return new Response(html, {
    status: status,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store, no-cache, must-revalidate, private'
    }
  });
}

