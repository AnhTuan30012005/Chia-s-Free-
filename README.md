# Studio Archive · Master Creative & Lab Ecosystem (72 Resources)

Kho lưu trữ và phân phối tài nguyên kỹ thuật số tuyển chọn với **72 bộ tài nguyên** được tổ chức thành 2 dòng sản phẩm riêng biệt:

## 1. Cấu Trúc Phân Tầng Dữ Liệu

- **💎 STUDIO SERIES (#S-01 đến #S-27):** 
  - 27 bộ sưu tập chuyên sâu về nhiếp ảnh nghệ thuật, màu máy ảnh cao cấp (Profile Leica M9/Q3, Fujifilm Film Simulation, 1200 Camera Color Profiles) và các tệp ảnh RAW chất lượng cao (Sony A7M4, Canon R5, GFX 100 102MP Medium Format).
- **⚡ LAB SUITE (#L-01 đến #L-45):** 
  - 45 tiện ích mở rộng phòng lab đồ họa: Panel Photoshop làm mịn da, kịch bản xếp ảnh thẻ tự động, công cụ chạy Action hàng loạt, Panel Oniric hiệu ứng ánh sáng, bộ mẫu dàn trang album cưới 170 PSD và giáo trình đào tạo.

---

## 2. Tính Năng Nổi Bật

- **Tải trực tiếp Google Drive:** Truy cập thẳng tới thư mục lưu trữ, không quảng cáo, không đếm ngược thời gian chờ.
- **Thanh chuyển đổi dòng sản phẩm (Series Switcher):** Lọc nhanh giữa *Tất cả (72)*, *Studio Series (27)* và *Lab Suite (45)*.
- **Tìm kiếm đa chiều:** Hỗ trợ tìm kiếm theo mã định danh nhanh (`#S`, `#L`), tên tài nguyên, máy ảnh, preset, định dạng file hoặc hệ điều hành.
- **Tự động hóa hoàn toàn với GitHub Actions:** Tự động đồng bộ và biên dịch website định kỳ.

---

## 3. Cấu Trúc Dự Án

```
├── .github/workflows/
│   ├── deploy.yml          # Tự động xuất bản lên GitHub Pages
│   └── auto_sync.yml       # Tự động cào và cập nhật tài nguyên mới
├── data/
│   └── resources.json      # Cơ sở dữ liệu 72 tài nguyên chuẩn hóa
├── scripts/
│   ├── crawler.py          # Script cào, lọc bỏ thương hiệu cũ và giải mã link
│   └── build_html.py       # Script biên dịch dữ liệu thành giao diện web
├── index.html              # Trang chủ ứng dụng web
└── README.md
```

---
© Studio Archive. Curated with precision.
