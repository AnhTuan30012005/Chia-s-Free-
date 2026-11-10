# Studio Vault - Cloudflare Edge Backend (Air-Gapped Anti-Scraping)

Hệ thống Backend Serverless chạy trên Cloudflare Workers + KV bảo vệ 72 liên kết tài nguyên, ngăn chặn 100% các công cụ cào tự động (`rea`, `lightpanda`, headless browser, curl loop, DOM scrapers).

---

## 1. Cơ Chế Bảo Mật Đa Tầng

1. **Zero Client Storage (Air-Gapped):**
   - File `data/resources.json` trên frontend chỉ chứa metadata (`code`, `title`, `series`,...).
   - Tuyệt đối không chứa bất kỳ URL Google Drive nào trong mã nguồn công khai (HTML, JS, CSS, JSON).
2. **Dynamic PoW Challenge Handshake:**
   - Client phải giải thuật toán Proof-of-Work (SHA-256 micro-hash) hợp lệ trong < 15ms trước khi xin cấp phiếu tải.
   - Ngăn chặn triệt để các crawler bot và curl script cào tự động hàng loạt.
3. **Vé Tải Dùng Một Lần (Burn-On-Read Redirection):**
   - Khi handshake thành công, Worker cấp 1 mã vé ngẫu nhiên (UUID) có hiệu lực 45 giây.
   - Khi mở link `/dl/:ticket`, Worker đọc URL Drive trực tiếp từ KV, **xóa hủy vé ngay lập tức (burn)**, và trả về mã `HTTP 302 Found` chuyển hướng thẳng đến Google Drive.
   - Vé không thể tải lần 2, không thể chia sẻ lại (trả về lỗi 410 Gone / 403 Forbidden).
4. **IP Leaky Bucket Rate Limiting:**
   - Giới hạn tối đa 5 lượt tải / 60 giây cho mỗi IP.
   - Vượt quá sẽ bị khóa với mã lỗi `429 Too Many Requests`.

---

## 2. Hướng Dẫn Triển Khai Trong 2 Phút

### Bước 1: Mở Terminal tại thư mục `backend-cloudflare`
```bash
cd "F:\ôn thi học kỳ 2\Chia-s-Free-\backend-cloudflare"
```

### Bước 2: Đăng nhập Cloudflare (miễn phí 100%)
```bash
npx wrangler login
```

### Bước 3: Tạo 3 KV Namespaces
Chạy lần lượt 3 lệnh sau:
```bash
npx wrangler kv:namespace create VAULT_KV
npx wrangler kv:namespace create TICKETS_KV
npx wrangler kv:namespace create STATS_KV
```
Mỗi lệnh sẽ in ra một đoạn cấu hình có dạng:
```toml
[[kv_namespaces]]
binding = "VAULT_KV"
id = "xxxxxx_id_in_ra_o_day_xxxxxx"
```
Mở file `wrangler.toml` và dán các `id` tương ứng vào chỗ `VAULT_KV_ID_PLACEHOLDER`, `TICKETS_KV_ID_PLACEHOLDER`, `STATS_KV_ID_PLACEHOLDER`.

### Bước 4: Thiết lập Khóa Ký Bảo Mật (SIGN_SECRET)
```bash
npx wrangler secret put SIGN_SECRET
```
*(Hệ thống sẽ hỏi giá trị secret, bạn nhập một chuỗi mật khẩu bất kỳ dài 32 ký tự. Giá trị này được lưu trữ bí mật trong Cloudflare Secrets và không bao giờ bị lộ ra ngoài).*

### Bước 5: Nạp 72 Liên Kết Bí Mật Lên Cloudflare KV
```bash
npx wrangler kv:bulk put --binding=VAULT_KV vault_kv_data.json
```
*(72 liên kết Drive sẽ được lưu mã hóa an toàn trên hạ tầng Edge của Cloudflare toàn cầu).*

### Bước 6: Triển khai Worker
```bash
npx wrangler deploy
```
Sau khi hoàn tất, Cloudflare sẽ cung cấp URL Worker của bạn, ví dụ:
`https://studio-vault-api.<ten-tai-khoan>.workers.dev`

---

## 3. Kết Nối Với Giao Diện Frontend
Mở file `scripts/build_html.py`, gán biến `VAULT_WORKER_URL = "https://studio-vault-api.<ten-tai-khoan>.workers.dev"`, sau đó chạy:
```bash
python scripts/build_html.py
```
Và push lên GitHub Pages. Toàn bộ kho tài nguyên của bạn đã được bảo vệ tuyệt đối!

