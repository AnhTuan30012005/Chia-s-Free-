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

    # Count by category
    cat_counts = {
        "preset": len([r for r in resources if r.get("category") == "preset"]),
        "software": len([r for r in resources if r.get("category") == "software"]),
        "psd": len([r for r in resources if r.get("category") == "psd"]),
        "raw": len([r for r in resources if r.get("category") == "raw"]),
        "courses": len([r for r in resources if r.get("category") == "courses"])
    }

    # Clean, Bright, Professional Design System Palette (Light Theme First)
    cat_themes = {
        "preset": {
            "name": "Preset & Picture Style",
            "bar": "bg-gradient-to-r from-sky-400 to-blue-500",
            "badge": "bg-sky-50 text-sky-700 border-sky-200",
            "icon": "sliders",
            "accent": "text-sky-600"
        },
        "software": {
            "name": "Phần Mềm & Panel",
            "bar": "bg-gradient-to-r from-indigo-400 to-purple-500",
            "badge": "bg-indigo-50 text-indigo-700 border-indigo-200",
            "icon": "cpu",
            "accent": "text-indigo-600"
        },
        "psd": {
            "name": "Mẫu Layout PSD",
            "bar": "bg-gradient-to-r from-purple-400 to-pink-500",
            "badge": "bg-purple-50 text-purple-700 border-purple-200",
            "icon": "layers",
            "accent": "text-purple-600"
        },
        "raw": {
            "name": "Stock RAW Gốc",
            "bar": "bg-gradient-to-r from-emerald-400 to-teal-500",
            "badge": "bg-emerald-50 text-emerald-700 border-emerald-200",
            "icon": "camera",
            "accent": "text-emerald-600"
        },
        "courses": {
            "name": "Khóa Học",
            "bar": "bg-gradient-to-r from-amber-400 to-orange-500",
            "badge": "bg-amber-50 text-amber-800 border-amber-200",
            "icon": "book-open",
            "accent": "text-amber-600"
        }
    }

    cards_html = ""
    for item in resources:
        code = item.get("code", "00")
        series = item.get("series", "lab")
        is_studio = (series == "studio")
        category = item.get("category", "preset")
        theme = cat_themes.get(category, cat_themes["preset"])

        safe_title = html_escape.escape(item.get("title", ""), quote=True)
        safe_desc = html_escape.escape(item.get("desc", ""), quote=True)
        safe_format = html_escape.escape(item.get("format", ""), quote=True)
        safe_tag = html_escape.escape(item.get("tag", ""), quote=True)
        safe_platform = html_escape.escape(item.get("platform", "Universal"), quote=True)
        url = item.get("url", "")
        safe_url = html_escape.escape(url, quote=True)
        js_url = url.replace('\\', '\\\\').replace("'", "\\'")
        js_title = safe_title.replace("'", "\\'")

        if is_studio:
            series_label = "HÀNG MUA VIP"
            series_badge = "bg-gradient-to-r from-amber-500 via-amber-600 to-yellow-600 text-white shadow-sm shadow-amber-500/25 border border-amber-300/40 font-sans tracking-wide"
            card_border = "border-amber-300/80 bg-gradient-to-b from-amber-50/25 to-white shadow-md shadow-amber-500/5 hover:border-amber-400 hover:shadow-amber-500/15"
            series_icon = '<i data-lucide="crown" class="w-3.5 h-3.5 text-yellow-200"></i>'
        else:
            series_label = "SHARE FREE"
            series_badge = "bg-slate-100 text-slate-700 border border-slate-200 font-sans"
            card_border = "border-slate-200/90 bg-white hover:border-sky-300 hover:shadow-xl hover:shadow-sky-500/5"
            series_icon = '<i data-lucide="gift" class="w-3.5 h-3.5 text-slate-400"></i>'

        raw_search = f"{code} #{code} {item.get('title', '')} {item.get('desc', '')} {item.get('tag', '')} {item.get('format', '')} {item.get('platform', '')} {series_label} vip hàng mua bản quyền free chia sẻ"
        safe_search = html_escape.escape(raw_search, quote=True)

        cards_html += f"""
        <!-- Resource Card #{code} -->
        <article class="resource-card group relative flex flex-col justify-between {card_border} rounded-2xl p-5 transition-all duration-300 hover:-translate-y-0.5"
                 data-series="{series}"
                 data-cat="{category}"
                 data-search="{safe_search}">
            
            <!-- Category Accent Top Line -->
            <div class="absolute top-0 left-0 right-0 h-1 {theme['bar']} rounded-t-2xl"></div>

            <div class="space-y-3 pt-1">
                <!-- Header Meta -->
                <div class="flex items-center justify-between gap-2 border-b border-slate-100 pb-3">
                    <div class="flex items-center gap-2">
                        <span class="font-mono text-sm font-bold text-slate-900">#{code}</span>
                        <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-[11px] font-bold {series_badge}">
                            {series_icon}
                            <span>{series_label}</span>
                        </span>
                    </div>
                    <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border {theme['badge']}">
                        <i data-lucide="{theme['icon']}" class="w-3.5 h-3.5"></i>
                        <span>{theme['name']}</span>
                    </span>
                </div>

                <!-- Format & Tag -->
                <div class="flex items-center gap-2 text-xs font-mono text-slate-500">
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">{safe_format}</span>
                    <span class="text-slate-300">•</span>
                    <span class="text-sky-700 font-medium truncate max-w-[200px]">{safe_tag}</span>
                </div>

                <!-- Title & Description -->
                <div class="space-y-1.5">
                    <h3 class="text-base font-bold text-slate-900 group-hover:text-sky-600 transition-colors leading-snug line-clamp-2" title="{safe_title}">
                        {safe_title}
                    </h3>
                    <p class="text-xs text-slate-500 leading-relaxed line-clamp-2">
                        {safe_desc}
                    </p>
                </div>
            </div>

            <!-- Footer & Actions -->
            <div class="pt-4 mt-4 border-t border-slate-100 space-y-3">
                <div class="flex items-center justify-between text-xs text-slate-500 font-mono">
                    <span class="flex items-center gap-1 text-slate-400">
                        <i data-lucide="monitor" class="w-3.5 h-3.5"></i>
                        <span>Hệ thống:</span>
                    </span>
                    <span class="text-slate-700 font-medium">{safe_platform}</span>
                </div>

                <div class="grid grid-cols-2 gap-2">
                    <button onclick="copyResourceUrl('{js_url}', '{js_title}')"
                            class="px-3 py-2 rounded-xl bg-slate-50 hover:bg-slate-100 text-slate-700 text-xs font-semibold border border-slate-200 transition-all flex items-center justify-center gap-1.5 active:scale-95">
                        <i data-lucide="copy" class="w-3.5 h-3.5 text-slate-400"></i>
                        <span>Sao chép</span>
                    </button>
                    <a href="{safe_url}" target="_blank" rel="noopener noreferrer"
                       class="px-3 py-2 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs shadow-sm hover:shadow-md transition-all flex items-center justify-center gap-1.5 active:scale-95">
                        <span>Tải Drive</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
                    </a>
                </div>
            </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi" class="scroll-smooth h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Vault — Kho Tài Nguyên Hậu Kỳ &amp; Màu Ảnh Chuyên Nghiệp</title>
    <meta name="description" content="Hệ thống lưu trữ 72 tài nguyên số đồ họa & nhiếp ảnh: Preset Lightroom, Photoshop Panel, Stock RAW và PSD tải trực tiếp Google Drive tốc độ cao.">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Plus Jakarta Sans & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            overflow-x: hidden;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Subtle Light Dot Grid Background */
        .dot-grid-bg {{
            background-image: radial-gradient(#cbd5e1 1px, transparent 1px);
            background-size: 24px 24px;
        }}

        /* Sticky Clean Glass Dock */
        .sticky-dock {{
            position: sticky;
            top: 0;
            z-index: 40;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            background-color: rgba(255, 255, 255, 0.92);
            border-bottom: 1px solid #e2e8f0;
        }}

        /* Filter Chip Styles */
        .filter-chip.active {{
            background-color: #0284c7;
            color: #ffffff;
            border-color: #0284c7;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
        }}

        .series-tab.active {{
            background-color: #0f172a;
            color: #ffffff;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }}

        /* Toast HUD */
        #hudToast {{
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            transform: translate(-50%, -60px) scale(0.95);
            opacity: 0;
            pointer-events: none;
        }}
        #hudToast.active {{
            transform: translate(-50%, 0) scale(1);
            opacity: 1;
            pointer-events: auto;
        }}

        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
        ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 9999px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
    </style>
</head>
<body class="min-h-full flex flex-col bg-slate-50 text-slate-900 selection:bg-sky-500 selection:text-white">

    <!-- TOAST NOTIFICATION -->
    <div id="hudToast" class="fixed top-5 left-1/2 z-50 flex items-center gap-2.5 px-4 py-2.5 rounded-full bg-slate-900 text-white shadow-xl shadow-slate-900/10 backdrop-blur-xl">
        <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-400"></i>
        <span class="text-xs font-medium text-slate-100" id="toastMsg">Đã sao chép link Google Drive</span>
    </div>

    <!-- TOP NAV -->
    <nav class="bg-white/80 border-b border-slate-200/80 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-sky-600 text-white flex items-center justify-center font-bold shadow-sm">
                    <i data-lucide="layers" class="w-4 h-4"></i>
                </div>
                <div>
                    <span class="text-sm font-bold tracking-tight text-slate-900">STUDIO <span class="text-sky-600">VAULT</span></span>
                    <span class="hidden sm:inline-block ml-2 px-2 py-0.5 rounded-full bg-slate-100 text-[10px] font-mono text-slate-600">v2025.1</span>
                </div>
            </div>

            <div class="flex items-center gap-3 text-xs font-mono">
                <span class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-sky-50 border border-sky-100 text-sky-800">
                    <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>{total_count} Tài nguyên sẵn sàng</span>
                </span>
                <a href="https://github.com/AnhTuan30012005/Chia-s-Free-" target="_blank" rel="noopener noreferrer"
                   class="px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors flex items-center gap-1.5 font-medium font-sans">
                    <i data-lucide="github" class="w-4 h-4"></i>
                    <span class="hidden sm:inline">GitHub</span>
                </a>
            </div>
        </div>
    </nav>

    <!-- 1. HERO SECTION (Bright, Clean, High-Conversion) -->
    <header class="relative bg-white border-b border-slate-200/80 py-12 sm:py-16 dot-grid-bg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
            
            <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-sky-50 border border-sky-200 text-xs font-semibold text-sky-800 shadow-sm">
                <span class="w-2 h-2 rounded-full bg-sky-500"></span>
                <span>Thư viện tài nguyên đồ họa &amp; hậu kỳ ảnh 2025</span>
            </div>

            <!-- Heading 1: Clear outcome & audience, balanced lines, no period at end -->
            <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-tight" style="text-wrap: balance;">
                Kho Tài Nguyên Hậu Kỳ &amp; Màu Ảnh Chuyên Nghiệp
            </h1>

            <p class="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed" style="text-wrap: pretty;">
                Tuyển chọn {total_count} bộ Preset Lightroom, Camera Raw, Photoshop Panel, Stock RAW và PSD dành cho Photographer &amp; Retoucher. Tải trực tiếp Google Drive, không quảng cáo.
            </p>

            <!-- 4 Proof Signals Grid -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-3xl mx-auto pt-4 text-left">
                <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                    <div class="text-xl font-extrabold text-slate-900 font-sans">{total_count} Files</div>
                    <div class="text-xs text-slate-500 font-medium">Trọn bộ tài nguyên</div>
                </div>
                <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                    <div class="text-xl font-extrabold text-sky-600 font-sans">100% Free</div>
                    <div class="text-xs text-slate-500 font-medium">Tải Google Drive trực tiếp</div>
                </div>
                <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                    <div class="text-xl font-extrabold text-emerald-600 font-sans">0 Ads</div>
                    <div class="text-xs text-slate-500 font-medium">Không rút gọn link</div>
                </div>
                <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80">
                    <div class="text-xl font-extrabold text-indigo-600 font-sans">Mobile/PC</div>
                    <div class="text-xs text-slate-500 font-medium">DNG, XMP, PSD &amp; ACR</div>
                </div>
            </div>
        </div>
    </header>

    <!-- 2. STICKY DOCK CONTROLS (SEARCH & DUAL FILTERS) -->
    <nav class="sticky-dock px-4 sm:px-6 lg:px-8 py-3.5 shadow-sm">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
            
            <!-- Search Bar with Shortcut -->
            <div class="relative flex-1 max-w-lg">
                <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                <input type="text" id="searchInput" placeholder="Tìm theo mã (#S-01, #L-01), tên, tone màu, định dạng..." oninput="handleSearch()"
                       class="w-full pl-10 pr-10 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-50 focus:bg-white border border-slate-200 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-2 focus:ring-sky-500/20 transition-all">
                <span class="hidden sm:inline-block absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded bg-white border border-slate-200 text-[10px] font-mono text-slate-400">/</span>
            </div>

            <!-- Series Switcher (Segmented Control) -->
            <div class="flex items-center gap-1.5 p-1 rounded-xl bg-slate-100 border border-slate-200 self-start md:self-auto">
                <button onclick="filterBySeries('all')" data-series="all"
                        class="series-tab active px-3.5 py-1.5 rounded-lg text-xs font-bold text-slate-700 hover:text-slate-900 transition-all">
                    Tất Cả ({total_count})
                </button>
                <button onclick="filterBySeries('studio')" data-series="studio"
                        class="series-tab px-3.5 py-1.5 rounded-lg text-xs font-bold text-amber-800 hover:text-amber-900 transition-all flex items-center gap-1.5">
                    <i data-lucide="crown" class="w-3.5 h-3.5 text-amber-500"></i>
                    <span>💎 Hàng Mua VIP</span>
                    <span class="px-1.5 py-0.2 rounded-full bg-amber-200/90 text-amber-900 text-[10px] font-mono font-extrabold">{studio_count}</span>
                </button>
                <button onclick="filterBySeries('lab')" data-series="lab"
                        class="series-tab px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 hover:text-slate-900 transition-all flex items-center gap-1.5">
                    <i data-lucide="gift" class="w-3.5 h-3.5 text-slate-500"></i>
                    <span>🎁 Share Free</span>
                    <span class="px-1.5 py-0.2 rounded-full bg-slate-200 text-slate-700 text-[10px] font-mono font-bold">{lab_count}</span>
                </button>
            </div>

            <!-- Live Counter -->
            <div class="hidden lg:flex items-center gap-2 text-xs font-mono text-slate-500">
                <span>Hiển thị:</span>
                <span id="visibleCount" class="font-bold text-sky-600 text-sm">{total_count}</span>
                <span>/ {total_count}</span>
            </div>
        </div>

        <!-- Categories Horizontal Bar -->
        <div class="max-w-7xl mx-auto flex items-center gap-2 overflow-x-auto pt-3 pb-1 no-scrollbar text-xs">
            <button onclick="filterByCategory('all')" data-cat="all"
                    class="filter-chip active px-3.5 py-1.5 rounded-full bg-white border border-slate-200 text-slate-700 font-semibold hover:border-slate-300 whitespace-nowrap transition-all shadow-sm">
                Tất Cả Thể Loại
            </button>
            <button onclick="filterByCategory('preset')" data-cat="preset"
                    class="filter-chip px-3.5 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 font-medium hover:border-slate-300 whitespace-nowrap transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="sliders" class="w-3.5 h-3.5 text-sky-600"></i>
                <span>Màu &amp; Preset ({cat_counts['preset']})</span>
            </button>
            <button onclick="filterByCategory('software')" data-cat="software"
                    class="filter-chip px-3.5 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 font-medium hover:border-slate-300 whitespace-nowrap transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="cpu" class="w-3.5 h-3.5 text-indigo-600"></i>
                <span>Phần Mềm &amp; Panel ({cat_counts['software']})</span>
            </button>
            <button onclick="filterByCategory('psd')" data-cat="psd"
                    class="filter-chip px-3.5 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 font-medium hover:border-slate-300 whitespace-nowrap transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="layers" class="w-3.5 h-3.5 text-purple-600"></i>
                <span>Mẫu Layout PSD ({cat_counts['psd']})</span>
            </button>
            <button onclick="filterByCategory('raw')" data-cat="raw"
                    class="filter-chip px-3.5 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 font-medium hover:border-slate-300 whitespace-nowrap transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="camera" class="w-3.5 h-3.5 text-emerald-600"></i>
                <span>Stock RAW Gốc ({cat_counts['raw']})</span>
            </button>
            <button onclick="filterByCategory('courses')" data-cat="courses"
                    class="filter-chip px-3.5 py-1.5 rounded-full bg-white border border-slate-200 text-slate-600 font-medium hover:border-slate-300 whitespace-nowrap transition-all flex items-center gap-1.5 shadow-sm">
                <i data-lucide="book-open" class="w-3.5 h-3.5 text-amber-600"></i>
                <span>Khóa Học ({cat_counts['courses']})</span>
            </button>
        </div>
    </nav>

    <!-- 3. RESOURCE CATALOG GRID -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        <div id="resourceGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {cards_html}
        </div>

        <!-- Empty State -->
        <div id="noResults" class="hidden py-24 text-center space-y-4">
            <div class="w-14 h-14 rounded-2xl bg-slate-100 border border-slate-200 flex items-center justify-center mx-auto text-slate-400">
                <i data-lucide="inbox" class="w-7 h-7"></i>
            </div>
            <div class="space-y-1">
                <div class="text-base font-bold text-slate-900">Không tìm thấy tài nguyên phù hợp</div>
                <p class="text-xs text-slate-500 max-w-sm mx-auto">Thử tìm theo từ khóa khác hoặc xóa bộ lọc để xem toàn bộ 72 tài nguyên.</p>
            </div>
            <button onclick="resetFilters()" class="px-4 py-2 rounded-xl bg-sky-600 text-white text-xs font-semibold hover:bg-sky-500 transition-colors shadow-sm">
                Xóa bộ lọc
            </button>
        </div>
    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 py-10 px-4 text-center text-xs text-slate-500 space-y-2">
        <div class="font-bold text-slate-900 tracking-tight">STUDIO VAULT • CURATED ASSET PLATFORM</div>
        <div>Tải trực tiếp Google Drive tốc độ tối đa • Không quảng cáo • Tối ưu mọi thiết bị</div>
        <div class="text-slate-400 font-mono text-[11px] pt-1">© 2025 AnhTuan30012005. All resources curated for creators.</div>
    </footer>

    <!-- INTERACTION LOGIC -->
    <script>
        lucide.createIcons();

        let currentSeries = 'all';
        let currentCategory = 'all';
        let searchQuery = '';

        function updateCatalog() {{
            const cards = document.querySelectorAll('.resource-card');
            let visible = 0;

            cards.forEach(card => {{
                const cardSeries = card.getAttribute('data-series');
                const cardCat = card.getAttribute('data-cat');
                const cardSearch = (card.getAttribute('data-search') || '').toLowerCase();

                const matchSeries = (currentSeries === 'all' || cardSeries === currentSeries);
                const matchCategory = (currentCategory === 'all' || cardCat === currentCategory);
                const matchSearch = (!searchQuery || cardSearch.includes(searchQuery));

                if (matchSeries && matchCategory && matchSearch) {{
                    card.style.display = 'flex';
                    visible++;
                }} else {{
                    card.style.display = 'none';
                }}
            }});

            const countEl = document.getElementById('visibleCount');
            if (countEl) countEl.textContent = visible;

            const noRes = document.getElementById('noResults');
            if (noRes) noRes.classList.toggle('hidden', visible > 0);
        }}

        function filterBySeries(series) {{
            currentSeries = series;
            document.querySelectorAll('.series-tab').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-series') === series);
            }});
            updateCatalog();
        }}

        function filterByCategory(cat) {{
            currentCategory = cat;
            document.querySelectorAll('.filter-chip').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-cat') === cat);
            }});
            updateCatalog();
        }}

        function handleSearch() {{
            const input = document.getElementById('searchInput');
            searchQuery = (input.value || '').trim().toLowerCase();
            updateCatalog();
        }}

        function resetFilters() {{
            document.getElementById('searchInput').value = '';
            searchQuery = '';
            filterBySeries('all');
            filterByCategory('all');
        }}

        // Shortcut '/' to search
        window.addEventListener('keydown', (e) => {{
            if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
                e.preventDefault();
                const input = document.getElementById('searchInput');
                if (input) input.focus();
            }}
        }});

        // Copy link + Toast
        function copyResourceUrl(url, title) {{
            navigator.clipboard.writeText(url).then(() => {{
                const toast = document.getElementById('hudToast');
                const msg = document.getElementById('toastMsg');
                if (msg) msg.textContent = `Đã sao chép link: ${{title.slice(0, 30)}}...`;
                if (toast) {{
                    toast.classList.add('active');
                    setTimeout(() => toast.classList.remove('active'), 2500);
                }}
            }}).catch(() => {{
                prompt('Link Google Drive:', url);
            }});
        }}
    </script>
</body>
</html>
"""

    with open(output_index, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[build] Built clean light design: {output_index} ({len(html)} bytes).")

if __name__ == "__main__":
    build()
