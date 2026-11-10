# -*- coding: utf-8 -*-
import json
import os
import html as html_escape

repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
json_path = os.path.join(repo_dir, "data", "resources.json")
output_index = os.path.join(repo_dir, "index.html")

def build():
    with open(json_path, "r", encoding="utf-8") as f:
        resources = json.load(f)

    total_count = len(resources)
    studio_count = len([r for r in resources if r.get("series") == "studio"])
    lab_count = len([r for r in resources if r.get("series") == "lab"])

    cards_html = ""
    for item in resources:
        code = item.get("code", "00")
        series = item.get("series", "lab")
        is_studio = (series == "studio")
        
        # Color Palette: Deep Dark Navy, Ice Blue & Pure White
        series_badge = """<span class="px-1.5 sm:px-2 py-0.5 rounded text-[9px] sm:text-[10px] font-bold uppercase tracking-wider bg-cyan-500/15 text-cyan-300 border border-cyan-400/30 flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span><span class="hidden xs:inline">Studio</span><span class="xs:hidden">S</span></span>""" if is_studio else """<span class="px-1.5 sm:px-2 py-0.5 rounded text-[9px] sm:text-[10px] font-bold uppercase tracking-wider bg-sky-500/10 text-sky-200 border border-sky-400/20 flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-sky-300"></span><span class="hidden xs:inline">Lab</span><span class="xs:hidden">L</span></span>"""
        
        code_color = "text-cyan-300 group-hover:text-white" if is_studio else "text-sky-200 group-hover:text-cyan-200"
        card_hover = "hover:border-cyan-400/50 hover:shadow-[0_12px_32px_-8px_rgba(56,189,248,0.25)]"
        spotlight_color = "rgba(56, 189, 248, 0.15)" if is_studio else "rgba(14, 165, 233, 0.12)"

        category_badge = {
            "software": "text-sky-300 bg-sky-500/10 border-sky-400/25",
            "preset": "text-cyan-300 bg-cyan-500/10 border-cyan-400/25",
            "raw": "text-teal-300 bg-teal-500/10 border-teal-400/25",
            "psd": "text-indigo-300 bg-indigo-500/10 border-indigo-400/25",
            "courses": "text-blue-300 bg-blue-500/10 border-blue-400/25"
        }.get(item["category"], "text-slate-300 bg-slate-800 border-slate-700")

        # Anti-XSS Sanitization (Strict HTML Escaping)
        safe_title = html_escape.escape(item.get("title", ""), quote=True)
        safe_desc = html_escape.escape(item.get("desc", ""), quote=True)
        safe_format = html_escape.escape(item.get("format", ""), quote=True)
        safe_tag = html_escape.escape(item.get("tag", ""), quote=True)
        safe_platform = html_escape.escape(item.get("platform", "Universal"), quote=True)
        safe_cat_name = html_escape.escape(item.get("cat_name", ""), quote=True)
        raw_search = f"{code} #{code} {item.get('title', '')} {item.get('desc', '')} {item.get('tag', '')} {item.get('format', '')} {item.get('platform', '')}"
        safe_search = html_escape.escape(raw_search, quote=True)
        js_title = item.get('title', '').replace('\\', '\\\\').replace("'", " ").replace('"', ' ')

        # Responsive 2-column card architecture (p-3 sm:p-5, compact text and magnetic buttons)
        cards_html += f"""
            <!-- Resource Card #{code} (Responsive 2-Col Mobile, Dark Navy & Ice White) -->
            <div class="resource-card group bg-[#091122]/90 border border-cyan-500/15 {card_hover} rounded-xl sm:rounded-2xl p-3 sm:p-5 flex flex-col justify-between gap-2.5 sm:gap-4 select-none backdrop-blur-sm"
                 style="--spotlight-color: {spotlight_color};"
                 data-series="{series}"
                 data-cat="{item['category']}"
                 data-search="{safe_search}">
                
                <!-- Card Header with Z-Elevation -->
                <div class="space-y-1.5 sm:space-y-3 card-inner-elevate relative z-10">
                    <div class="flex items-center justify-between pb-2 sm:pb-3 border-b border-white/[0.08]">
                        <div class="flex items-center gap-1.5 sm:gap-2">
                            <span class="font-mono text-xs sm:text-base font-bold {code_color} transition-colors">
                                #{code}
                            </span>
                            {series_badge}
                        </div>
                        <span class="px-1.5 sm:px-2 py-0.5 rounded text-[8px] sm:text-[10px] font-bold uppercase tracking-wider border {category_badge}">
                            {safe_cat_name}
                        </span>
                    </div>

                    <div class="space-y-1">
                        <div class="flex items-center gap-1 text-[10px] sm:text-[11px] font-medium text-slate-400 truncate">
                            <span class="truncate">{safe_format}</span>
                            <span class="text-slate-600">•</span>
                            <span class="text-cyan-300 font-semibold truncate">{safe_tag}</span>
                        </div>
                        <h3 class="text-xs sm:text-sm font-bold text-white group-hover:text-cyan-100 transition-colors leading-snug line-clamp-2" title="{safe_title}">
                            {safe_title}
                        </h3>
                        <p class="text-[10px] sm:text-xs text-slate-400 leading-relaxed line-clamp-1 sm:line-clamp-2">
                            {safe_desc}
                        </p>
                    </div>
                </div>

                <!-- Card Footer with Magnetic Actions -->
                <div class="space-y-2 sm:space-y-3 pt-2 sm:pt-3 border-t border-white/[0.08] card-inner-elevate relative z-10">
                    <div class="hidden sm:flex items-center justify-between text-[11px] text-slate-400 font-mono">
                        <span class="flex items-center gap-1"><i data-lucide="monitor" class="w-3 h-3 text-cyan-400/60"></i> Hệ thống:</span>
                        <span class="text-slate-200">{safe_platform}</span>
                    </div>
                    
                    <div class="flex items-center justify-between gap-1.5 sm:gap-2.5">
                        <button onclick="triggerSecureVault('{code}', '{js_title}', 'copy')"
                                id="btn-copy-{code}"
                                class="magnetic-btn flex-1 py-1.5 sm:py-2 px-1.5 sm:px-3 rounded-lg sm:rounded-xl bg-[#0e182e] hover:bg-[#152342] text-[10px] sm:text-xs font-semibold text-slate-300 hover:text-white border border-cyan-500/20 hover:border-cyan-400/40 transition-all flex items-center justify-center gap-1 active:scale-95">
                            <i data-lucide="copy" class="w-3 h-3 text-cyan-400"></i>
                            <span class="truncate">Sao Chép</span>
                        </button>
                        
                        <button onclick="triggerSecureVault('{code}', '{js_title}', 'download')"
                                id="btn-dl-{code}"
                                class="magnetic-btn flex-1 py-1.5 sm:py-2 px-1.5 sm:px-3 rounded-lg sm:rounded-xl bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-200 hover:text-white text-[10px] sm:text-xs font-semibold border border-cyan-400/40 transition-all flex items-center justify-center gap-1 active:scale-95 shadow-md shadow-cyan-950">
                            <i data-lucide="shield-check" class="w-3 h-3 text-cyan-300"></i>
                            <span class="truncate font-bold">Mở Khoá</span>
                        </button>
                    </div>
                </div>
            </div>
"""

    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark scroll-smooth h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>STUDIO ARCHIVE · 3D Parallax & Motion Engine (72 Resources)</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Three.js (Engine 3D từ Landscape3D.jsx) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <style>
        :root {{
            --bg-deep: #040711;
            --surface-card: #091122;
            --accent-cyan: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.25);
        }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-deep);
            color: #f1f5f9;
            overflow-x: hidden;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}

        /* 1. 3D Landscape Canvas Container (Dark Blue & Ice White) */
        #landscape3d-wrapper {{
            position: relative;
            width: 100%;
            height: 68vh;
            min-height: 460px;
            overflow: hidden;
            background: #02040a;
        }}
        #landscape3d-canvas {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            display: block;
        }}

        /* Overlay Typography in 3D Depth */
        .landscape-overlay {{
            position: absolute;
            inset: 0;
            pointer-events: none;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 1.25rem 1.5rem;
            z-index: 10;
        }}

        .landscape-title {{
            font-size: clamp(2.8rem, 8.5vw, 7.2rem);
            font-weight: 900;
            letter-spacing: -0.04em;
            line-height: 0.9;
            color: #ffffff;
            text-transform: uppercase;
            text-shadow: 0 10px 40px rgba(56, 189, 248, 0.35), 0 2px 10px rgba(0, 0, 0, 0.9);
        }}

        /* 2. CARD 3D TILT & SPOTLIGHT PHYSICS */
        .resource-card {{
            position: relative;
            transform-style: preserve-3d;
            perspective: 800px;
            transition: transform 0.16s cubic-bezier(0.2, 0, 0, 1), border-color 0.25s, box-shadow 0.25s, opacity 0.4s ease;
            will-change: transform;
            overflow: hidden;
            opacity: 0;
            transform: translateY(16px);
        }}
        .resource-card.revealed {{
            opacity: 1;
            transform: translateY(0);
        }}

        /* Spotlight radial glow on hover (Ice Blue) */
        .resource-card::before {{
            content: '';
            position: absolute;
            inset: 0;
            border-radius: inherit;
            background: radial-gradient(280px circle at var(--card-x, -500px) var(--card-y, -500px), var(--spotlight-color, rgba(56, 189, 248, 0.14)), transparent 70%);
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: 1;
        }}
        .resource-card:hover::before {{
            opacity: 1;
        }}

        /* Elevate elements in 3D depth inside the card */
        .card-inner-elevate {{
            transform: translateZ(14px);
        }}

        /* Magnetic button transition */
        .magnetic-btn {{
            transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1);
            will-change: transform;
        }}

        /* Active buttons (Dark Blue & Ice Cyan) */
        .series-btn.active {{
            background: #0e1d38;
            color: #ffffff;
            border-color: rgba(56, 189, 248, 0.5);
            box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        }}
        .series-btn[data-series="studio"].active {{
            background: rgba(56, 189, 248, 0.2);
            color: #7dd3fc;
            border-color: rgba(56, 189, 248, 0.6);
        }}
        .series-btn[data-series="lab"].active {{
            background: rgba(14, 165, 233, 0.2);
            color: #bae6fd;
            border-color: rgba(14, 165, 233, 0.6);
        }}

        .cat-tab.active {{
            background-color: #0e1d38;
            color: #ffffff;
            border-color: rgba(56, 189, 248, 0.4);
            font-weight: 700;
        }}

        /* Toast HUD */
        #hudToast {{
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            transform: translate(-50%, -80px) scale(0.95);
            opacity: 0;
            pointer-events: none;
        }}
        #hudToast.active {{
            transform: translate(-50%, 0) scale(1);
            opacity: 1;
            pointer-events: auto;
        }}

        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: #040711; }}
        ::-webkit-scrollbar-thumb {{ background: #0e1d38; border-radius: 9999px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #38bdf8; }}
    </style>
</head>
<body class="min-h-full flex flex-col bg-[#040711]">

    <!-- TOAST NOTIFICATION -->
    <div id="hudToast" class="fixed top-6 left-1/2 z-50 flex items-center gap-3 px-5 py-3 rounded-2xl bg-[#091122]/95 backdrop-blur-xl border border-cyan-500/40 shadow-2xl shadow-cyan-950 text-white">
        <i data-lucide="check" class="w-4 h-4 text-cyan-400" id="toastIcon"></i>
        <span class="text-xs font-semibold text-slate-100" id="toastTitle">Đã xác thực</span>
    </div>

    <!-- VAULT SHIELD MODAL (Edge Cloudflare Backend Notice / Settings) -->
    <div id="vaultModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md opacity-0 pointer-events-none transition-all duration-300">
        <div class="relative w-full max-w-md p-6 bg-[#091122] border border-cyan-500/30 rounded-2xl shadow-2xl shadow-cyan-950/80 text-white">
            <div class="flex items-center justify-between pb-4 border-b border-white/10">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
                    <h3 class="text-sm font-bold text-slate-100 font-mono uppercase tracking-wide">Shield Vault Protocol</h3>
                </div>
                <button onclick="closeVaultModal()" class="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-white/5 transition-colors">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
            </div>
            <div class="py-4 space-y-3 text-xs leading-relaxed text-slate-300">
                <div class="p-3 rounded-xl bg-cyan-950/40 border border-cyan-500/20 text-cyan-200">
                    <p class="font-semibold mb-1 flex items-center gap-1.5">
                        <i data-lucide="shield-alert" class="w-3.5 h-3.5 text-cyan-400"></i>
                        Bảo Mật Air-Gapped Kích Hoạt
                    </p>
                    <p class="text-[11px] text-slate-300">
                        Toàn bộ 72 liên kết Drive được cách ly trên Cloudflare Edge KV và bảo vệ bằng thuật toán PoW + Vé hủy 1 lần (Burn-on-read).
                    </p>
                </div>
                <p>
                    Để kết nối trực tiếp, hãy triển khai Cloudflare Worker trong thư mục <code class="text-cyan-300 bg-white/5 px-1 py-0.5 rounded font-mono">backend-cloudflare</code> theo hướng dẫn trong README.md.
                </p>
                <div class="pt-2">
                    <label class="block text-[11px] font-mono text-slate-400 mb-1">Cấu hình URL Worker Edge của bạn:</label>
                    <input id="customWorkerInput" type="text" placeholder="https://studio-vault-api.<user>.workers.dev" 
                           class="w-full px-3 py-2 text-xs rounded-lg bg-[#040711] border border-cyan-500/30 text-white focus:outline-none focus:border-cyan-400 font-mono">
                </div>
            </div>
            <div class="flex items-center justify-end gap-2 pt-3 border-t border-white/10">
                <button onclick="closeVaultModal()" class="px-3.5 py-1.5 text-xs font-semibold rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 transition-colors">
                    Đóng
                </button>
                <button onclick="saveCustomWorkerUrl()" class="px-4 py-1.5 text-xs font-bold rounded-lg bg-cyan-500 hover:bg-cyan-400 text-[#040711] transition-all">
                    Lưu Kết Nối
                </button>
            </div>
        </div>
    </div>

    <!-- 1. 3D LANDSCAPE HERO (DEEP DARK NAVY, ICE BLUE & MOON ARCHITECTURE) -->
    <section id="landscape3d-wrapper">
        <canvas id="landscape3d-canvas"></canvas>

        <!-- HTML OVERLAY LAYERED ACROSS 3D DEPTH -->
        <div class="landscape-overlay max-w-7xl mx-auto w-full">
            
            <!-- Top Navigation -->
            <div class="flex items-center justify-between w-full pointer-events-auto">
                <div class="flex items-center gap-2.5 sm:gap-3">
                    <div class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl bg-[#040711]/70 backdrop-blur-md border border-cyan-400/30 flex items-center justify-center text-white shadow-lg shadow-cyan-950">
                        <i data-lucide="camera" class="w-4 h-4 text-cyan-300"></i>
                    </div>
                    <span class="text-xs sm:text-sm font-bold tracking-tight text-white uppercase font-mono">
                        STUDIO <span class="text-cyan-400">VAULT</span>
                    </span>
                </div>

                <div class="hidden sm:flex items-center gap-6 text-xs font-mono text-slate-300">
                    <span class="hover:text-cyan-300 cursor-pointer transition-colors" onclick="filterBySeries('studio')">Studio Series ({studio_count})</span>
                    <span class="hover:text-cyan-300 cursor-pointer transition-colors" onclick="filterBySeries('lab')">Lab Tools ({lab_count})</span>
                    <span class="hover:text-cyan-300 cursor-pointer transition-colors" onclick="scrollToCatalog()">Catalog (72)</span>
                </div>

                <div class="flex items-center gap-2">
                    <button onclick="showVaultConfigModal()" class="px-2 sm:px-3 py-1 sm:py-1.5 rounded-xl bg-cyan-950/40 hover:bg-cyan-900/50 backdrop-blur-md border border-cyan-400/30 text-[10px] sm:text-xs font-mono text-cyan-300 flex items-center gap-1.5 transition-all" title="Cấu hình kết nối Cloudflare Vault Edge">
                        <i data-lucide="shield" class="w-3.5 h-3.5 text-cyan-400"></i>
                        <span id="navVaultStatus">Vault API</span>
                    </button>
                    <div class="px-2.5 sm:px-3.5 py-1 sm:py-1.5 rounded-xl bg-[#040711]/70 backdrop-blur-md border border-cyan-400/30 text-[11px] sm:text-xs font-mono text-slate-200 flex items-center gap-1.5 sm:gap-2">
                        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
                        <span class="font-bold text-white" id="navCounter">{total_count}</span> <span class="hidden xs:inline">Resources</span>
                    </div>
                </div>
            </div>

            <!-- Center/Bottom 3D Typographic Branding -->
            <div class="w-full flex flex-col md:flex-row md:items-end justify-between gap-4 sm:gap-6 pb-2 pointer-events-auto">
                <div class="space-y-1.5 sm:space-y-2 max-w-xl">
                    <div class="inline-flex items-center gap-2 px-2.5 sm:px-3 py-1 rounded-full bg-[#040711]/75 backdrop-blur-md border border-cyan-400/30 text-[10px] sm:text-[11px] font-mono text-cyan-300">
                        <span class="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                        <span>Interactive 3D Moon Landscape</span>
                    </div>
                    <h1 class="landscape-title">
                        ARCHIVE
                    </h1>
                    <p class="text-[11px] sm:text-sm text-slate-300 max-w-md leading-relaxed drop-shadow">
                        Hệ sinh thái lưu trữ 72 tài nguyên số chuyên sâu: Tải trực tiếp Google Drive tốc độ tối đa, không quảng cáo, tối ưu 2 cột trên điện thoại.
                    </p>
                </div>

                <!-- Fast Search Bar -->
                <div class="w-full md:w-80 space-y-1.5 sm:space-y-2">
                    <div class="relative">
                        <i data-lucide="search" class="w-3.5 sm:w-4 h-3.5 sm:h-4 text-cyan-400 absolute left-3 sm:left-3.5 top-1/2 -translate-y-1/2"></i>
                        <input type="text" id="searchInput" placeholder="Tìm theo mã (#S-01, #L-01), tên..." oninput="handleSearch()"
                               class="w-full pl-9 sm:pl-10 pr-8 sm:pr-9 py-2 sm:py-2.5 rounded-xl bg-[#040711]/80 backdrop-blur-md border border-cyan-500/30 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-cyan-400 focus:shadow-[0_0_15px_rgba(56,189,248,0.3)] transition-all">
                        <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white">
                            <i data-lucide="x" class="w-3.5 h-3.5"></i>
                        </button>
                    </div>
                    <div class="flex items-center justify-between text-[10px] sm:text-[11px] font-mono text-slate-400 px-1">
                        <span>Lia chuột / vuốt để xoay 3D</span>
                        <span class="text-cyan-400 font-bold">72 Files Online</span>
                    </div>
                </div>
            </div>

        </div>
    </section>

    <!-- 2. CATALOG CONTROLS (SERIES & CATEGORY FILTERS) -->
    <section id="catalogSection" class="pt-6 sm:pt-8 px-3 sm:px-8 max-w-7xl mx-auto w-full space-y-2.5 sm:space-y-3">
        <!-- Series Switcher -->
        <div class="p-1 sm:p-1.5 rounded-xl sm:rounded-2xl bg-[#070e1c] border border-cyan-500/20 flex flex-wrap items-center justify-between gap-1.5 sm:gap-2 shadow-xl">
            <div class="flex items-center gap-1 sm:gap-1.5 w-full sm:w-auto justify-between sm:justify-start">
                <button onclick="filterBySeries('all')" data-series="all"
                        class="series-btn active flex-1 sm:flex-none px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-semibold text-slate-300 hover:text-white transition-all border border-transparent">
                    Tất Cả ({total_count})
                </button>
                <button onclick="filterBySeries('studio')" data-series="studio"
                        class="series-btn flex-1 sm:flex-none px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-semibold text-slate-300 hover:text-white transition-all border border-transparent flex items-center justify-center gap-1 sm:gap-1.5">
                    <span>Studio</span>
                    <span class="px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-300 text-[10px] font-mono font-bold">{studio_count}</span>
                </button>
                <button onclick="filterBySeries('lab')" data-series="lab"
                        class="series-btn flex-1 sm:flex-none px-3 sm:px-4 py-1.5 sm:py-2 rounded-lg sm:rounded-xl text-[11px] sm:text-xs font-semibold text-slate-300 hover:text-white transition-all border border-transparent flex items-center justify-center gap-1 sm:gap-1.5">
                    <span>Lab</span>
                    <span class="px-1.5 py-0.2 rounded bg-sky-500/20 text-sky-200 text-[10px] font-mono font-bold">{lab_count}</span>
                </button>
            </div>

            <div class="text-[11px] sm:text-xs text-slate-400 px-3 hidden sm:block font-mono">
                Hiển thị: <span id="visibleCount" class="font-bold text-cyan-300 text-sm">{total_count}</span> / {total_count}
            </div>
        </div>

        <!-- Categories -->
        <div class="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs no-scrollbar">
            <button onclick="filterByCategory('all')" data-cat="all"
                    class="cat-tab active px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-lg sm:rounded-xl bg-[#081226] border border-cyan-500/20 text-slate-300 whitespace-nowrap text-[11px] sm:text-xs transition-colors">
                Tất Cả Thể Loại
            </button>
            <button onclick="filterByCategory('preset')" data-cat="preset"
                    class="cat-tab px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-lg sm:rounded-xl bg-[#081226]/60 border border-white/[0.08] text-slate-400 hover:text-white whitespace-nowrap text-[11px] sm:text-xs transition-colors">
                Màu & Preset
            </button>
            <button onclick="filterByCategory('software')" data-cat="software"
                    class="cat-tab px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-lg sm:rounded-xl bg-[#081226]/60 border border-white/[0.08] text-slate-400 hover:text-white whitespace-nowrap text-[11px] sm:text-xs transition-colors">
                Phần Mềm & Panel
            </button>
            <button onclick="filterByCategory('psd')" data-cat="psd"
                    class="cat-tab px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-lg sm:rounded-xl bg-[#081226]/60 border border-white/[0.08] text-slate-400 hover:text-white whitespace-nowrap text-[11px] sm:text-xs transition-colors">
                Mẫu Layout PSD
            </button>
            <button onclick="filterByCategory('raw')" data-cat="raw"
                    class="cat-tab px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-lg sm:rounded-xl bg-[#081226]/60 border border-white/[0.08] text-slate-400 hover:text-white whitespace-nowrap text-[11px] sm:text-xs transition-colors">
                Stock RAW Gốc
            </button>
            <button onclick="filterByCategory('courses')" data-cat="courses"
                    class="cat-tab px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-lg sm:rounded-xl bg-[#081226]/60 border border-white/[0.08] text-slate-400 hover:text-white whitespace-nowrap text-[11px] sm:text-xs transition-colors">
                Khóa Học
            </button>
        </div>
    </section>

    <!-- 3. MAIN RESOURCE GRID (RESPONSIVE 2 COLUMNS ON MOBILE) -->
    <main class="py-5 sm:py-6 px-3 sm:px-8 max-w-7xl mx-auto w-full flex-1">
        <div id="resourceGrid" class="grid grid-cols-2 lg:grid-cols-3 gap-2.5 sm:gap-4 md:gap-5">
            {cards_html}
        </div>

        <!-- Empty State -->
        <div id="noResults" class="hidden py-16 sm:py-20 text-center space-y-3">
            <i data-lucide="inbox" class="w-8 h-8 mx-auto text-cyan-400/50"></i>
            <h4 class="text-sm font-bold text-white">Không có kết quả phù hợp</h4>
            <p class="text-xs text-slate-400">Vui lòng thử từ khóa tìm kiếm khác.</p>
            <button onclick="resetFilters()" class="px-3.5 py-1.5 rounded-xl bg-[#0e1d38] hover:bg-[#162d59] text-xs font-semibold text-cyan-300 border border-cyan-400/30 transition-colors">
                Xóa Bộ Lọc
            </button>
        </div>
    </main>

    <!-- 4. FOOTER -->
    <footer class="mt-auto border-t border-cyan-500/15 bg-[#03060f] py-6 sm:py-8 px-4 sm:px-8">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-400 font-mono text-center sm:text-left">
            <div class="flex items-center gap-2 text-slate-300">
                <span class="w-2 h-2 rounded-full bg-cyan-400 shadow-[0_0_8px_#38bdf8]"></span>
                <span>72 Verified Google Drive Direct Links</span>
            </div>
            <div class="text-[11px] text-slate-500">
                White-Blue Darkroom Architecture · Mobile 2-Column Responsive
            </div>
        </div>
    </footer>

    <!-- 5. THREE.JS 3D LANDSCAPE ENGINE (DARK NAVY & ICE BLUE / WHITE PALETTE) -->
    <script>
        (function initLandscape3D() {{
            const container = document.getElementById('landscape3d-wrapper');
            const canvas = document.getElementById('landscape3d-canvas');
            if (!container || !canvas || !window.THREE) return;

            try {{
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
                camera.position.set(0, 0, 18);

                const renderer = new THREE.WebGLRenderer({{ canvas: canvas, antialias: true, alpha: true, powerPreference: 'high-performance' }});
                renderer.setSize(container.clientWidth, container.clientHeight);
                renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

                const group = new THREE.Group();
                scene.add(group);

            // Canvas Gradient Texture for Sky: Deep Space Navy -> Dark Blue -> Ocean Cyan -> Ice Horizon Glow
            function createSkyTexture() {{
                const c = document.createElement('canvas');
                c.width = 512;
                c.height = 1024;
                const ctx = c.getContext('2d');
                const grad = ctx.createLinearGradient(0, 0, 0, c.height);
                grad.addColorStop(0.00, '#020409'); // Midnight Space
                grad.addColorStop(0.35, '#07152d'); // Deep Navy Blue
                grad.addColorStop(0.70, '#0284c7'); // Electric Ocean Blue
                grad.addColorStop(1.00, '#bae6fd'); // Ice White Horizon Glow
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, c.width, c.height);
                const tex = new THREE.CanvasTexture(c);
                tex.minFilter = THREE.LinearFilter;
                return tex;
            }}

            // LAYER 1: Background Sky (z = -25)
            const skyGeo = new THREE.PlaneGeometry(120, 80);
            const skyMat = new THREE.MeshBasicMaterial({{ map: createSkyTexture(), depthWrite: false }});
            const skyMesh = new THREE.Mesh(skyGeo, skyMat);
            skyMesh.position.set(0, 0, -25);
            group.add(skyMesh);

            // LAYER 2: Ice Moon / Glowing Orb (z = -20)
            const moonGroup = new THREE.Group();
            moonGroup.position.set(7, 9, -20);

            // Pure White / Ice Core
            const moonGeo = new THREE.CircleGeometry(4.8, 64);
            const moonMat = new THREE.MeshBasicMaterial({{ color: 0xf0f9ff, transparent: true, opacity: 0.95 }});
            const moonMesh = new THREE.Mesh(moonGeo, moonMat);
            moonGroup.add(moonMesh);

            // Ice Blue Halo
            function createMoonHaloTexture() {{
                const c = document.createElement('canvas');
                c.width = 256;
                c.height = 256;
                const ctx = c.getContext('2d');
                const rad = ctx.createRadialGradient(128, 128, 0, 128, 128, 128);
                rad.addColorStop(0, 'rgba(240, 249, 255, 0.8)');
                rad.addColorStop(0.35, 'rgba(56, 189, 248, 0.45)');
                rad.addColorStop(0.75, 'rgba(14, 165, 233, 0.15)');
                rad.addColorStop(1, 'rgba(14, 165, 233, 0)');
                ctx.fillStyle = rad;
                ctx.fillRect(0, 0, 256, 256);
                return new THREE.CanvasTexture(c);
            }}
            const haloGeo = new THREE.PlaneGeometry(26, 26);
            const haloMat = new THREE.MeshBasicMaterial({{ map: createMoonHaloTexture(), transparent: true, blending: THREE.AdditiveBlending, depthWrite: false }});
            const haloMesh = new THREE.Mesh(haloGeo, haloMat);
            moonGroup.add(haloMesh);
            group.add(moonGroup);

            // Mountain Silhouettes (Dark Navy & Ice Blue Highlights)
            function createMountainTexture(color, highlightColor, peaks) {{
                const c = document.createElement('canvas');
                c.width = 2048;
                c.height = 1024;
                const ctx = c.getContext('2d');
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.moveTo(0, c.height);
                for (let i = 0; i < peaks.length; i++) {{
                    const [px, py] = peaks[i];
                    ctx.lineTo(px * c.width, (1 - py) * c.height);
                }}
                ctx.lineTo(c.width, c.height);
                ctx.closePath();
                ctx.fill();

                if (highlightColor) {{
                    ctx.strokeStyle = highlightColor;
                    ctx.lineWidth = 6;
                    ctx.stroke();
                }}
                const tex = new THREE.CanvasTexture(c);
                tex.minFilter = THREE.LinearFilter;
                return tex;
            }}

            // LAYER 3: Back Mountains (z = -15, Deep Navy with Ice Rim Light)
            const m1Peaks = [
                [0.0, 0.20], [0.12, 0.45], [0.22, 0.28], [0.35, 0.62], 
                [0.48, 0.35], [0.60, 0.52], [0.75, 0.38], [0.88, 0.48], [1.0, 0.25]
            ];
            const m1Tex = createMountainTexture('#06142a', '#e0f2fe88', m1Peaks);
            const m1Geo = new THREE.PlaneGeometry(90, 45);
            const m1Mat = new THREE.MeshBasicMaterial({{ map: m1Tex, transparent: true, depthWrite: false }});
            const m1Mesh = new THREE.Mesh(m1Geo, m1Mat);
            m1Mesh.position.set(0, -6, -15);
            group.add(m1Mesh);

            // LAYER 4: Mid Mountains (z = -8, Ocean Midnight Blue with Cyan Edge)
            const m2Peaks = [
                [0.0, 0.15], [0.18, 0.36], [0.30, 0.22], [0.45, 0.48], 
                [0.55, 0.30], [0.70, 0.42], [0.85, 0.20], [1.0, 0.12]
            ];
            const m2Tex = createMountainTexture('#0a1d38', '#38bdf866', m2Peaks);
            const m2Geo = new THREE.PlaneGeometry(60, 30);
            const m2Mat = new THREE.MeshBasicMaterial({{ map: m2Tex, transparent: true, depthWrite: false }});
            const m2Mesh = new THREE.Mesh(m2Geo, m2Mat);
            m2Mesh.position.set(0, -7, -8);
            group.add(m2Mesh);

            // LAYER 5: Near Mountains (z = -4, Cold Indigo Blue)
            const m3Peaks = [
                [0.0, 0.10], [0.25, 0.28], [0.50, 0.15], [0.75, 0.32], [1.0, 0.08]
            ];
            const m3Tex = createMountainTexture('#0f2b52', '#7dd3fc55', m3Peaks);
            const m3Geo = new THREE.PlaneGeometry(45, 20);
            const m3Mat = new THREE.MeshBasicMaterial({{ map: m3Tex, transparent: true, depthWrite: false }});
            const m3Mesh = new THREE.Mesh(m3Geo, m3Mat);
            m3Mesh.position.set(0, -7, -4);
            group.add(m3Mesh);

            // LAYER 6: Foreground Base & Traveler Silhouette (z = 0.5, Deep Obsidian #040711)
            function createForegroundTexture() {{
                const c = document.createElement('canvas');
                c.width = 2048;
                c.height = 1024;
                const ctx = c.getContext('2d');
                ctx.fillStyle = '#040711';

                ctx.beginPath();
                ctx.moveTo(0, c.height);
                ctx.lineTo(0, c.height * 0.65);
                ctx.quadraticCurveTo(c.width * 0.35, c.height * 0.58, c.width * 0.70, c.height * 0.75);
                ctx.lineTo(c.width, c.height * 0.55);
                ctx.lineTo(c.width, c.height);
                ctx.closePath();
                ctx.fill();

                // Traveler Silhouette
                const tx = c.width * 0.82;
                const ty = c.height * 0.60;
                ctx.fillStyle = '#040711';
                
                ctx.beginPath();
                ctx.moveTo(tx - 38, ty);
                ctx.lineTo(tx, ty - 22);
                ctx.lineTo(tx + 38, ty);
                ctx.closePath();
                ctx.fill();

                ctx.beginPath();
                ctx.arc(tx, ty + 8, 14, 0, Math.PI * 2);
                ctx.rect(tx - 18, ty + 16, 36, 60);
                ctx.fill();

                return new THREE.CanvasTexture(c);
            }}
            const fgTex = createForegroundTexture();
            const fgGeo = new THREE.PlaneGeometry(32, 16);
            const fgMat = new THREE.MeshBasicMaterial({{ map: fgTex, transparent: true }});
            const fgMesh = new THREE.Mesh(fgGeo, fgMat);
            fgMesh.position.set(0, -6, 0.5);
            group.add(fgMesh);

            // LAYER 7: Atmospheric Ice Dust (White & Cyan Sparkles)
            const dustCount = 130;
            const dustGeo = new THREE.BufferGeometry();
            const dustPositions = new Float32Array(dustCount * 3);
            for (let i = 0; i < dustCount; i++) {{
                dustPositions[i * 3 + 0] = (Math.random() - 0.5) * 50;
                dustPositions[i * 3 + 1] = (Math.random() - 0.5) * 30;
                dustPositions[i * 3 + 2] = (Math.random() - 0.5) * 20 - 5;
            }}
            dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPositions, 3));
            const dustMat = new THREE.PointsMaterial({{
                color: 0xe0f2fe, // Pure Ice Sparkle
                size: 0.18,
                transparent: true,
                opacity: 0.85,
                blending: THREE.AdditiveBlending
            }});
            const dustPoints = new THREE.Points(dustGeo, dustMat);
            group.add(dustPoints);

            // MOUSE & TOUCH TRACKING WITH LERP
            const mouse = {{ x: 0, y: 0, targetX: 0, targetY: 0 }};
            function updateCoordinates(clientX, clientY) {{
                const rect = container.getBoundingClientRect();
                mouse.targetX = ((clientX - rect.left) / rect.width) * 2 - 1;
                mouse.targetY = -(((clientY - rect.top) / rect.height) * 2 - 1);
            }}

            window.addEventListener('mousemove', (e) => updateCoordinates(e.clientX, e.clientY));
            window.addEventListener('touchmove', (e) => {{
                if (e.touches.length > 0) {{
                    updateCoordinates(e.touches[0].clientX, e.touches[0].clientY);
                }}
            }}, {{ passive: true }});

            let clock = new THREE.Clock();
            function animate() {{
                requestAnimationFrame(animate);
                const elapsedTime = clock.getElapsedTime();

                mouse.x += (mouse.targetX - mouse.x) * 0.05;
                mouse.y += (mouse.targetY - mouse.y) * 0.05;

                group.rotation.y = mouse.x * 0.14;
                group.rotation.x = -mouse.y * 0.10;

                moonGroup.position.y = 9 + Math.sin(elapsedTime * 1.5) * 0.35;

                const pos = dustGeo.attributes.position.array;
                for (let i = 0; i < dustCount; i++) {{
                    pos[i * 3 + 1] += 0.015;
                    if (pos[i * 3 + 1] > 15) pos[i * 3 + 1] = -15;
                }}
                dustGeo.attributes.position.needsUpdate = true;

                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                if (!container) return;
                const w = container.clientWidth;
                const h = container.clientHeight;
                camera.aspect = w / h;
                camera.updateProjectionMatrix();
                renderer.setSize(w, h);
            }});
            }} catch (webglErr) {{
                console.warn('WebGL context failed or unsupported. Fallback activated:', webglErr);
                if (canvas) canvas.style.display = 'none';
                if (container) {{
                    container.style.background = 'radial-gradient(circle at 75% 20%, rgba(56, 189, 248, 0.22) 0%, rgba(7, 21, 45, 0.9) 45%, #040711 100%)';
                }}
            }}
        }})();

        // 6. INTERACTIVE MOTION FOR LOWER SECTIONS (3D Tilt, Spotlight, Magnetic, Stagger Reveal)
        lucide.createIcons();

        function initCardMotion() {{
            const cards = document.querySelectorAll('.resource-card');
            cards.forEach(card => {{
                card.addEventListener('mousemove', (e) => {{
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    
                    card.style.setProperty('--card-x', `${{x}}px`);
                    card.style.setProperty('--card-y', `${{y}}px`);

                    const centerX = rect.width / 2;
                    const centerY = rect.height / 2;
                    const rotateX = ((y - centerY) / centerY) * -6.5;
                    const rotateY = ((x - centerX) / centerX) * 6.5;

                    card.style.transform = `perspective(800px) rotateX(${{rotateX.toFixed(2)}}deg) rotateY(${{rotateY.toFixed(2)}}deg) translateY(-4px)`;
                }});

                card.addEventListener('mouseleave', () => {{
                    card.style.transform = 'perspective(800px) rotateX(0deg) rotateY(0deg) translateY(0px)';
                }});
            }});
        }}
        initCardMotion();

        document.querySelectorAll('.magnetic-btn').forEach(btn => {{
            btn.addEventListener('mousemove', (e) => {{
                const rect = btn.getBoundingClientRect();
                const x = (e.clientX - rect.left - rect.width / 2) * 0.28;
                const y = (e.clientY - rect.top - rect.height / 2) * 0.28;
                btn.style.transform = `translate(${{x.toFixed(1)}}px, ${{y.toFixed(1)}}px)`;
            }});
            btn.addEventListener('mouseleave', () => {{
                btn.style.transform = 'translate(0px, 0px)';
            }});
        }});

        const revealObserver = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }}
            }});
        }}, {{ threshold: 0.05 }});

        document.querySelectorAll('.resource-card').forEach((card, idx) => {{
            card.style.transitionDelay = `${{(idx % 6) * 0.04}}s`;
            revealObserver.observe(card);
        }});

        let currentSeries = 'all';
        let currentCategory = 'all';
        let currentSearchQuery = '';

        function scrollToCatalog() {{
            document.getElementById('catalogSection').scrollIntoView({{ behavior: 'smooth' }});
        }}

        function filterBySeries(series) {{
            currentSeries = series;
            document.querySelectorAll('.series-btn').forEach(btn => {{
                if (btn.getAttribute('data-series') === series) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            applyFilters();
        }}

        function filterByCategory(cat) {{
            currentCategory = cat;
            document.querySelectorAll('.cat-tab').forEach(btn => {{
                if (btn.getAttribute('data-cat') === cat) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            applyFilters();
        }}

        function handleSearch() {{
            const input = document.getElementById('searchInput');
            currentSearchQuery = input.value.trim().toLowerCase();
            const clearBtn = document.getElementById('clearSearchBtn');
            if (currentSearchQuery) {{
                clearBtn.classList.remove('hidden');
            }} else {{
                clearBtn.classList.add('hidden');
            }}
            applyFilters();
        }}

        function clearSearch() {{
            document.getElementById('searchInput').value = '';
            document.getElementById('clearSearchBtn').classList.add('hidden');
            currentSearchQuery = '';
            applyFilters();
        }}

        function resetFilters() {{
            filterBySeries('all');
            filterByCategory('all');
            clearSearch();
        }}

        function applyFilters() {{
            const cards = document.querySelectorAll('.resource-card');
            let visibleCount = 0;

            cards.forEach(card => {{
                const series = card.getAttribute('data-series');
                const cat = card.getAttribute('data-cat');
                const searchData = card.getAttribute('data-search').toLowerCase();

                const seriesMatch = (currentSeries === 'all') || (series === currentSeries);
                const catMatch = (currentCategory === 'all') || (cat === currentCategory);
                const searchMatch = !currentSearchQuery || searchData.includes(currentSearchQuery);

                if (seriesMatch && catMatch && searchMatch) {{
                    card.classList.remove('hidden');
                    visibleCount++;
                }} else {{
                    card.classList.add('hidden');
                }}
            }});

            const visibleCountEl = document.getElementById('visibleCount');
            if (visibleCountEl) visibleCountEl.textContent = visibleCount;

            const noResults = document.getElementById('noResults');
            if (visibleCount === 0) {{
                noResults.classList.remove('hidden');
            }} else {{
                noResults.classList.add('hidden');
            }}
        }}

        let toastTimeout;
        function showHudToast(message, type = 'success') {{
            const toast = document.getElementById('hudToast');
            const titleEl = document.getElementById('toastTitle');
            const iconEl = document.getElementById('toastIcon');
            
            if (titleEl) titleEl.textContent = message;
            if (iconEl) {{
                if (type === 'error') {{
                    iconEl.setAttribute('data-lucide', 'alert-circle');
                    iconEl.className = 'w-4 h-4 text-rose-400';
                }} else if (type === 'info') {{
                    iconEl.setAttribute('data-lucide', 'shield');
                    iconEl.className = 'w-4 h-4 text-cyan-400';
                }} else {{
                    iconEl.setAttribute('data-lucide', 'check');
                    iconEl.className = 'w-4 h-4 text-emerald-400';
                }}
                if (window.lucide) lucide.createIcons();
            }}
            
            toast.classList.add('active');
            clearTimeout(toastTimeout);
            toastTimeout = setTimeout(() => {{
                toast.classList.remove('active');
            }}, 3200);
        }}

        function getVaultEndpoint() {{
            const stored = localStorage.getItem('vault_worker_url');
            if (stored && stored.startsWith('http')) return stored.trim().replace(/\/+$/, '');
            return '';
        }}

        function updateNavVaultStatus() {{
            const statusEl = document.getElementById('navVaultStatus');
            const ep = getVaultEndpoint();
            if (statusEl) {{
                if (ep) {{
                    statusEl.textContent = 'Vault: Live';
                    statusEl.parentElement.classList.remove('text-cyan-300', 'bg-cyan-950/40');
                    statusEl.parentElement.classList.add('text-emerald-300', 'bg-emerald-950/40', 'border-emerald-500/30');
                }} else {{
                    statusEl.textContent = 'Cấu hình Vault';
                    statusEl.parentElement.classList.remove('text-emerald-300', 'bg-emerald-950/40');
                    statusEl.parentElement.classList.add('text-cyan-300', 'bg-cyan-950/40');
                }}
            }}
        }}

        function showVaultConfigModal(code, title) {{
            const modal = document.getElementById('vaultModal');
            const input = document.getElementById('customWorkerInput');
            if (input) input.value = localStorage.getItem('vault_worker_url') || '';
            if (modal) {{
                modal.classList.remove('opacity-0', 'pointer-events-none');
                modal.classList.add('opacity-100', 'pointer-events-auto');
            }}
        }}

        function closeVaultModal() {{
            const modal = document.getElementById('vaultModal');
            if (modal) {{
                modal.classList.remove('opacity-100', 'pointer-events-auto');
                modal.classList.add('opacity-0', 'pointer-events-none');
            }}
        }}

        function saveCustomWorkerUrl() {{
            const input = document.getElementById('customWorkerInput');
            if (input && input.value.trim()) {{
                const clean = input.value.trim().replace(/\/+$/, '');
                localStorage.setItem('vault_worker_url', clean);
                showHudToast('Đã lưu cấu hình Cloudflare Worker!', 'success');
                updateNavVaultStatus();
                closeVaultModal();
            }}
        }}

        async function sha256Hex(str) {{
            const encoder = new TextEncoder();
            const data = encoder.encode(str);
            const hashBuffer = await crypto.subtle.digest('SHA-256', data);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        }}

        async function triggerSecureVault(code, title, mode) {{
            const btnDl = document.getElementById(`btn-dl-${{code}}`);
            const btnCopy = document.getElementById(`btn-copy-${{code}}`);
            const activeBtn = (mode === 'download') ? btnDl : btnCopy;
            const originalHtml = activeBtn ? activeBtn.innerHTML : '';
            
            const endpoint = getVaultEndpoint();
            if (!endpoint) {{
                showVaultConfigModal(code, title);
                showHudToast('Cần kết nối Cloudflare Worker Edge để mở khóa link!', 'info');
                return;
            }}

            try {{
                if (activeBtn) {{
                    activeBtn.innerHTML = `<span class="inline-block animate-spin mr-1">⟳</span><span class="truncate">Đang giải mã...</span>`;
                    activeBtn.disabled = true;
                }}

                showHudToast(`Đang xác thực bảo mật tài nguyên #${{code}}...`, 'info');
                
                // 1. Request PoW Challenge cryptographically bound to resource code
                let challengeRes;
                try {{
                    challengeRes = await fetch(`${{endpoint}}/api/challenge?code=${{encodeURIComponent(code)}}`, {{
                        headers: {{ 'Accept': 'application/json' }}
                    }});
                }} catch (netErr) {{
                    showVaultConfigModal(code, title);
                    showHudToast('Lỗi mạng: Không kết nối được URL Worker đã lưu.', 'error');
                    return;
                }}

                if (!challengeRes.ok) {{
                    showVaultConfigModal(code, title);
                    showHudToast('Lỗi kết nối Vault Edge Backend.', 'error');
                    return;
                }}

                const challenge = await challengeRes.json();

                // 2. Solve Micro Proof-of-Work (~10ms)
                const seed = challenge.seed;
                const target = '0'.repeat(challenge.difficulty || 3);
                let nonce = 0;
                let powHash = '';

                while (true) {{
                    powHash = await sha256Hex(`${{seed}}:${{nonce}}`);
                    if (powHash.startsWith(target)) break;
                    nonce++;
                    if (nonce > 200000) break;
                }}

                // 3. Exchange for One-time Burn Ticket
                const handshakeRes = await fetch(`${{endpoint}}/api/handshake`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        code: code,
                        seed: seed,
                        timestamp: challenge.timestamp,
                        nonce: nonce,
                        signature: challenge.signature
                    }})
                }});

                const handshakeData = await handshakeRes.json();

                if (!handshakeRes.ok) {{
                    if (handshakeRes.status === 429) {{
                        showHudToast('Tốc độ tải quá nhanh! Vui lòng đợi 60 giây.', 'error');
                    }} else {{
                        showHudToast(handshakeData.error || 'Xác thực không thành công.', 'error');
                    }}
                    return;
                }}

                const downloadUrl = handshakeData.download_url;

                // 4. Execute Action
                if (mode === 'copy') {{
                    await navigator.clipboard.writeText(downloadUrl);
                    showHudToast(`Đã sao chép vé tải 1 lần (hết hạn 45s)!`, 'success');
                }} else {{
                    showHudToast(`Đã mở khoá #${{code}}! Đang chuyển hướng...`, 'success');
                    window.open(downloadUrl, '_blank');
                }}

            }} catch (err) {{
                console.error('Vault error:', err);
                showHudToast('Lỗi bảo mật. Vui lòng thử lại.', 'error');
            }} finally {{
                if (activeBtn) {{
                    activeBtn.innerHTML = originalHtml;
                    activeBtn.disabled = false;
                }}
            }}
        }}

        // Initialize Vault status on load
        updateNavVaultStatus();
    </script>
</body>
</html>
"""

    with open(output_index, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated 2-Col Mobile & Dark White-Blue index.html at: {output_index}")

if __name__ == "__main__":
    build()
