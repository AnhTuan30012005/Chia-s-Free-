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

    # Category color schemes for visual indicators (Part B: Design Tokens)
    cat_themes = {
        "preset": {
            "name": "Preset & Picture Style",
            "bar": "from-cyan-400 via-sky-500 to-blue-600",
            "badge": "bg-cyan-500/10 text-cyan-300 border-cyan-400/20",
            "icon": "sliders",
            "dot": "bg-cyan-400"
        },
        "software": {
            "name": "Phần Mềm & Panel",
            "bar": "from-sky-400 via-indigo-500 to-purple-600",
            "badge": "bg-indigo-500/10 text-indigo-300 border-indigo-400/20",
            "icon": "cpu",
            "dot": "bg-indigo-400"
        },
        "psd": {
            "name": "Mẫu Layout PSD",
            "bar": "from-purple-400 via-pink-500 to-rose-600",
            "badge": "bg-purple-500/10 text-purple-300 border-purple-400/20",
            "icon": "layers",
            "dot": "bg-purple-400"
        },
        "raw": {
            "name": "Stock RAW Gốc",
            "bar": "from-emerald-400 via-teal-500 to-cyan-600",
            "badge": "bg-emerald-500/10 text-emerald-300 border-emerald-400/20",
            "icon": "image",
            "dot": "bg-emerald-400"
        },
        "courses": {
            "name": "Khóa Học",
            "bar": "from-amber-400 via-orange-500 to-red-600",
            "badge": "bg-amber-500/10 text-amber-300 border-amber-400/20",
            "icon": "book-open",
            "dot": "bg-amber-400"
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

        series_label = "Studio Series" if is_studio else "Lab Tool"
        series_pill = "text-sky-300 bg-sky-500/15 border-sky-400/30" if is_studio else "text-indigo-300 bg-indigo-500/15 border-indigo-400/30"
        series_dot = "bg-sky-400" if is_studio else "bg-indigo-400"

        raw_search = f"{code} #{code} {item.get('title', '')} {item.get('desc', '')} {item.get('tag', '')} {item.get('format', '')} {item.get('platform', '')} {series_label}"
        safe_search = html_escape.escape(raw_search, quote=True)

        cards_html += f"""
        <article class="resource-card group relative flex flex-col justify-between bg-zinc-900/60 hover:bg-zinc-900/90 border border-white/[0.08] hover:border-sky-500/40 rounded-2xl p-4 sm:p-5 transition-all duration-300 hover:shadow-2xl hover:shadow-sky-500/10 hover:-translate-y-1 backdrop-blur-md overflow-hidden"
                 data-series="{series}"
                 data-cat="{category}"
                 data-search="{safe_search}">
            
            <!-- Top Visual Accent Strip -->
            <div class="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r {theme['bar']} opacity-75 group-hover:opacity-100 transition-opacity"></div>

            <!-- Card Header -->
            <div class="space-y-3 pt-1">
                <div class="flex items-center justify-between gap-2 border-b border-white/[0.06] pb-3">
                    <div class="flex items-center gap-2">
                        <span class="font-mono text-sm sm:text-base font-bold text-white tracking-tight">#{code}</span>
                        <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[10px] font-medium border {series_pill}">
                            <span class="w-1.5 h-1.5 rounded-full {series_dot}"></span>
                            <span>{series_label}</span>
                        </span>
                    </div>
                    <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-medium border {theme['badge']}">
                        <i data-lucide="{theme['icon']}" class="w-3 h-3"></i>
                        <span>{theme['name']}</span>
                    </span>
                </div>

                <!-- Meta Pills -->
                <div class="flex items-center gap-2 text-[11px] font-mono text-zinc-400">
                    <span class="px-2 py-0.5 rounded-md bg-white/[0.04] text-zinc-300 font-medium">{safe_format}</span>
                    <span class="text-zinc-600">•</span>
                    <span class="text-sky-300 font-semibold truncate max-w-[180px]">{safe_tag}</span>
                </div>

                <!-- Title & Description -->
                <div class="space-y-1.5">
                    <h3 class="text-sm sm:text-base font-bold text-zinc-100 group-hover:text-white transition-colors leading-snug line-clamp-2" title="{safe_title}">
                        {safe_title}
                    </h3>
                    <p class="text-xs text-zinc-400 leading-relaxed line-clamp-2">
                        {safe_desc}
                    </p>
                </div>
            </div>

            <!-- Card Footer -->
            <div class="pt-4 mt-4 border-t border-white/[0.06] space-y-3">
                <div class="flex items-center justify-between text-[11px] text-zinc-400 font-mono">
                    <span class="flex items-center gap-1 text-zinc-500">
                        <i data-lucide="laptop" class="w-3.5 h-3.5 text-zinc-400"></i>
                        <span>Hệ thống:</span>
                    </span>
                    <span class="text-zinc-200 font-medium">{safe_platform}</span>
                </div>

                <div class="grid grid-cols-2 gap-2 pt-1">
                    <button onclick="copyResourceUrl('{js_url}', '{js_title}')"
                            class="px-3 py-2 rounded-xl bg-white/[0.04] hover:bg-white/[0.08] text-xs font-semibold text-zinc-200 border border-white/[0.08] hover:border-white/20 transition-all flex items-center justify-center gap-1.5 active:scale-95">
                        <i data-lucide="copy" class="w-3.5 h-3.5 text-zinc-400"></i>
                        <span>Sao chép</span>
                    </button>
                    <a href="{safe_url}" target="_blank" rel="noopener noreferrer"
                       class="px-3 py-2 rounded-xl bg-sky-500 hover:bg-sky-400 text-zinc-950 font-bold text-xs shadow-lg shadow-sky-500/20 transition-all flex items-center justify-center gap-1.5 active:scale-95">
                        <span>Tải Drive</span>
                        <i data-lucide="external-link" class="w-3.5 h-3.5"></i>
                    </a>
                </div>
            </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="vi" class="dark scroll-smooth h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Vault — 72 Bộ Tài Nguyên Hậu Kỳ & Màu Ảnh Chuyên Nghiệp</title>
    <meta name="description" content="Hệ thống lưu trữ 72 tài nguyên số đồ họa & nhiếp ảnh: Preset Lightroom, Photoshop Panel, Stock RAW và PSD tải trực tiếp Google Drive tốc độ cao.">
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Inter & JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Three.js (Engine 3D Parallax) -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <style>
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #07090e;
            color: #f4f4f5;
            overflow-x: hidden;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Subtle Aurora Glow */
        .aurora-bg {{
            background: 
                radial-gradient(circle at 15% 10%, rgba(14, 165, 233, 0.15), transparent 45%),
                radial-gradient(circle at 85% 15%, rgba(99, 102, 241, 0.12), transparent 40%),
                radial-gradient(circle at 50% 60%, rgba(56, 189, 248, 0.08), transparent 50%),
                #07090e;
        }}

        /* 3D Canvas Container */
        #landscape3d-wrapper {{
            position: relative;
            width: 100%;
            height: 52vh;
            min-height: 420px;
            overflow: hidden;
            background: #04060a;
        }}
        #landscape3d-canvas {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            display: block;
        }}

        /* Sticky Control Bar with Blur */
        .sticky-dock {{
            position: sticky;
            top: 0;
            z-index: 40;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            background-color: rgba(7, 9, 14, 0.85);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }}

        /* Active Filter Button */
        .filter-btn.active {{
            background-color: #0284c7;
            color: #ffffff;
            font-weight: 600;
            border-color: transparent;
            box-shadow: 0 0 20px rgba(14, 165, 233, 0.35);
        }}

        .series-pill.active {{
            background-color: rgba(255, 255, 255, 0.12);
            color: #ffffff;
            font-weight: 700;
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

        /* Clean Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: #07090e; }}
        ::-webkit-scrollbar-thumb {{ background: #27272a; border-radius: 9999px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #38bdf8; }}
    </style>
</head>
<body class="min-h-full flex flex-col aurora-bg selection:bg-sky-500/30 selection:text-sky-200">

    <!-- FLOATING TOAST -->
    <div id="hudToast" class="fixed top-5 left-1/2 z-50 flex items-center gap-2.5 px-4 py-2.5 rounded-full bg-zinc-900/95 border border-sky-500/40 shadow-2xl shadow-sky-950 text-white backdrop-blur-xl">
        <i data-lucide="check-circle-2" class="w-4 h-4 text-sky-400"></i>
        <span class="text-xs font-medium text-zinc-100" id="toastMsg">Đã sao chép link Google Drive</span>
    </div>

    <!-- 1. HIGH-CONVERTING HERO (Design System Guided) -->
    <header id="landscape3d-wrapper" class="border-b border-white/[0.06]">
        <canvas id="landscape3d-canvas"></canvas>

        <div class="absolute inset-0 z-10 flex flex-col justify-between max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 pointer-events-none">
            <!-- Top Nav -->
            <div class="flex items-center justify-between w-full pointer-events-auto">
                <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-white/[0.08] backdrop-blur-md border border-white/10 flex items-center justify-center text-sky-400 shadow-md">
                        <i data-lucide="archive" class="w-4 h-4"></i>
                    </div>
                    <div>
                        <div class="text-xs font-mono font-bold tracking-wider uppercase text-zinc-300">STUDIO <span class="text-sky-400">VAULT</span></div>
                        <div class="text-[10px] text-zinc-400 font-mono">Curated Asset Engine</div>
                    </div>
                </div>

                <div class="flex items-center gap-3 font-mono text-xs">
                    <span class="hidden md:inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/[0.04] border border-white/10 text-zinc-300">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        <span>{total_count} Tài nguyên sẵn sàng</span>
                    </span>
                    <a href="https://github.com/AnhTuan30012005/Chia-s-Free-" target="_blank" rel="noopener noreferrer"
                       class="px-3 py-1 rounded-full bg-white/[0.06] hover:bg-white/[0.12] border border-white/10 text-zinc-200 transition-colors flex items-center gap-1.5">
                        <i data-lucide="github" class="w-3.5 h-3.5"></i>
                        <span class="hidden sm:inline">GitHub</span>
                    </a>
                </div>
            </div>

            <!-- Hero Branding & Value Prop (Landing Page Rule A2: Headline Outcome + Audience) -->
            <div class="space-y-4 max-w-3xl pointer-events-auto pb-4">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-xs font-mono text-sky-300">
                    <span class="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
                    <span>Tải trực tiếp Google Drive tốc độ tối đa</span>
                </div>
                
                <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white leading-tight">
                    Kho Tài Nguyên Hậu Kỳ &amp; Màu Ảnh Chuyên Nghiệp
                </h1>
                
                <p class="text-sm sm:text-base text-zinc-300 max-w-2xl leading-relaxed">
                    Tuyển tập {total_count} bộ Preset Lightroom, Photoshop Panel, Stock RAW và PSD tuyển chọn dành riêng cho Photographer &amp; Retoucher. Không quảng cáo, không rút gọn link.
                </p>

                <!-- Proof Signals -->
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-xs font-mono">
                    <div class="p-2.5 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                        <div class="text-base font-bold text-white font-sans">{total_count} Files</div>
                        <div class="text-zinc-400 text-[11px]">Trọn bộ tài nguyên</div>
                    </div>
                    <div class="p-2.5 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                        <div class="text-base font-bold text-sky-400 font-sans">100% Free</div>
                        <div class="text-zinc-400 text-[11px]">Google Drive direct</div>
                    </div>
                    <div class="p-2.5 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                        <div class="text-base font-bold text-emerald-400 font-sans">0 Ads</div>
                        <div class="text-zinc-400 text-[11px]">Không rút gọn link</div>
                    </div>
                    <div class="p-2.5 rounded-xl bg-white/[0.03] border border-white/[0.06]">
                        <div class="text-base font-bold text-indigo-400 font-sans">Mobile/PC</div>
                        <div class="text-zinc-400 text-[11px]">Tối ưu 2 cột hiển thị</div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- 2. STICKY UNIFIED CONTROL DOCK -->
    <nav class="sticky-dock px-4 sm:px-6 lg:px-8 py-3.5">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
            
            <!-- Search Input with Shortcut -->
            <div class="relative flex-1 max-w-md">
                <i data-lucide="search" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                <input type="text" id="searchInput" placeholder="Tìm theo mã (#S-01, #L-01), tên, thể loại..." oninput="handleSearch()"
                       class="w-full pl-10 pr-10 py-2.5 rounded-xl bg-zinc-900/90 border border-white/10 text-xs text-white placeholder-zinc-500 focus:outline-none focus:border-sky-400 focus:ring-1 focus:ring-sky-400 transition-all">
                <span class="hidden sm:inline-block absolute right-3 top-1/2 -translate-y-1/2 px-1.5 py-0.5 rounded bg-white/[0.06] border border-white/10 text-[10px] font-mono text-zinc-400">/</span>
            </div>

            <!-- Series Switcher (Segmented Control) -->
            <div class="flex items-center gap-1 p-1 rounded-xl bg-zinc-900 border border-white/10 self-start md:self-auto">
                <button onclick="filterBySeries('all')" data-series="all"
                        class="series-pill active px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-300 hover:text-white transition-all">
                    Tất Cả ({total_count})
                </button>
                <button onclick="filterBySeries('studio')" data-series="studio"
                        class="series-pill px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white transition-all flex items-center gap-1.5">
                    <span>Studio</span>
                    <span class="px-1.5 py-0.2 rounded-full bg-sky-500/20 text-sky-300 text-[10px] font-mono">{studio_count}</span>
                </button>
                <button onclick="filterBySeries('lab')" data-series="lab"
                        class="series-pill px-3 py-1.5 rounded-lg text-xs font-medium text-zinc-400 hover:text-white transition-all flex items-center gap-1.5">
                    <span>Lab</span>
                    <span class="px-1.5 py-0.2 rounded-full bg-indigo-500/20 text-indigo-300 text-[10px] font-mono">{lab_count}</span>
                </button>
            </div>

            <!-- Real-time Resource Counter -->
            <div class="hidden lg:flex items-center gap-2 text-xs font-mono text-zinc-400">
                <span>Đang hiển thị:</span>
                <span id="visibleCount" class="font-bold text-sky-400 text-sm">{total_count}</span>
                <span>/ {total_count}</span>
            </div>
        </div>

        <!-- Category Horizontal Pills -->
        <div class="max-w-7xl mx-auto flex items-center gap-1.5 overflow-x-auto pt-2.5 pb-1 no-scrollbar text-xs">
            <button onclick="filterByCategory('all')" data-cat="all"
                    class="filter-btn active px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-zinc-300 hover:text-white whitespace-nowrap transition-all">
                Tất Cả Thể Loại
            </button>
            <button onclick="filterByCategory('preset')" data-cat="preset"
                    class="filter-btn px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-zinc-400 hover:text-white whitespace-nowrap transition-all flex items-center gap-1.5">
                <i data-lucide="sliders" class="w-3.5 h-3.5 text-cyan-400"></i>
                <span>Màu &amp; Preset</span>
            </button>
            <button onclick="filterByCategory('software')" data-cat="software"
                    class="filter-btn px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-zinc-400 hover:text-white whitespace-nowrap transition-all flex items-center gap-1.5">
                <i data-lucide="cpu" class="w-3.5 h-3.5 text-indigo-400"></i>
                <span>Phần Mềm &amp; Panel</span>
            </button>
            <button onclick="filterByCategory('psd')" data-cat="psd"
                    class="filter-btn px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-zinc-400 hover:text-white whitespace-nowrap transition-all flex items-center gap-1.5">
                <i data-lucide="layers" class="w-3.5 h-3.5 text-purple-400"></i>
                <span>Mẫu Layout PSD</span>
            </button>
            <button onclick="filterByCategory('raw')" data-cat="raw"
                    class="filter-btn px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-zinc-400 hover:text-white whitespace-nowrap transition-all flex items-center gap-1.5">
                <i data-lucide="image" class="w-3.5 h-3.5 text-emerald-400"></i>
                <span>Stock RAW Gốc</span>
            </button>
            <button onclick="filterByCategory('courses')" data-cat="courses"
                    class="filter-btn px-3.5 py-1.5 rounded-full bg-white/[0.04] border border-white/[0.08] text-zinc-400 hover:text-white whitespace-nowrap transition-all flex items-center gap-1.5">
                <i data-lucide="book-open" class="w-3.5 h-3.5 text-amber-400"></i>
                <span>Khóa Học</span>
            </button>
        </div>
    </nav>

    <!-- 3. RESOURCE CATALOG GRID -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full">
        <div id="resourceGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
            {cards_html}
        </div>

        <!-- Empty State -->
        <div id="noResults" class="hidden py-24 text-center space-y-3">
            <div class="w-12 h-12 rounded-2xl bg-white/[0.04] border border-white/10 flex items-center justify-center mx-auto text-zinc-500">
                <i data-lucide="inbox" class="w-6 h-6"></i>
            </div>
            <div class="text-base font-bold text-white">Không tìm thấy tài nguyên phù hợp</div>
            <p class="text-xs text-zinc-400 max-w-sm mx-auto">Thử tìm theo từ khóa khác hoặc xóa bộ lọc để hiển thị toàn bộ 72 tài nguyên.</p>
            <button onclick="resetFilters()" class="px-4 py-2 rounded-xl bg-sky-500/10 text-sky-300 border border-sky-400/20 text-xs font-semibold hover:bg-sky-500/20 transition-colors">
                Xóa bộ lọc
            </button>
        </div>
    </main>

    <!-- FOOTER -->
    <footer class="border-t border-white/[0.06] py-8 px-4 text-center text-xs font-mono text-zinc-500 space-y-2">
        <div>STUDIO ARCHIVE • CURATED GRAPHICS &amp; RETOUCHING VAULT</div>
        <div class="text-zinc-600">Built with 100% Direct Google Drive Links • No Ads • No Trackers</div>
    </footer>

    <!-- INTERACTIVITY & 3D PARALLAX ENGINE -->
    <script>
        lucide.createIcons();

        // 1. Filtering & Search Engine
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
            document.querySelectorAll('.series-pill').forEach(btn => {{
                btn.classList.toggle('active', btn.getAttribute('data-series') === series);
            }});
            updateCatalog();
        }}

        function filterByCategory(cat) {{
            currentCategory = cat;
            document.querySelectorAll('.filter-btn').forEach(btn => {{
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
            currentSeries = 'all';
            currentCategory = 'all';
            filterBySeries('all');
            filterByCategory('all');
        }}

        // Keyboard Shortcut '/' to focus search
        window.addEventListener('keydown', (e) => {{
            if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
                e.preventDefault();
                const input = document.getElementById('searchInput');
                if (input) input.focus();
            }}
        }});

        // Copy Link Action + HUD Toast
        function copyResourceUrl(url, title) {{
            navigator.clipboard.writeText(url).then(() => {{
                const toast = document.getElementById('hudToast');
                const msg = document.getElementById('toastMsg');
                if (msg) msg.textContent = `Đã sao chép link #${{title.slice(0, 28)}}...`;
                if (toast) {{
                    toast.classList.add('active');
                    setTimeout(() => toast.classList.remove('active'), 2500);
                }}
            }}).catch(() => {{
                prompt('Link Google Drive:', url);
            }});
        }}

        // 2. High-Performance Three.js Interactive Moon & Starfield Engine
        (function initThreeEngine() {{
            const wrapper = document.getElementById('landscape3d-wrapper');
            const canvas = document.getElementById('landscape3d-canvas');
            if (!wrapper || !canvas || typeof THREE === 'undefined') return;

            const scene = new THREE.Scene();
            scene.fog = new THREE.FogExp2(0x04060a, 0.002);

            const camera = new THREE.PerspectiveCamera(45, wrapper.clientWidth / wrapper.clientHeight, 1, 1000);
            camera.position.set(0, 5, 40);

            const renderer = new THREE.WebGLRenderer({{ canvas, alpha: true, antialias: true }});
            renderer.setSize(wrapper.clientWidth, wrapper.clientHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

            // Moon Mesh with Soft Glow
            const moonGeo = new THREE.SphereGeometry(6, 32, 32);
            const moonMat = new THREE.MeshBasicMaterial({{ color: 0xffffff }});
            const moon = new THREE.Mesh(moonGeo, moonMat);
            moon.position.set(18, 12, -40);
            scene.add(moon);

            // Mountain Grid Geometry (Low poly wireframe / frosted silhouette)
            const mountainGeo = new THREE.PlaneGeometry(120, 60, 40, 20);
            const pos = mountainGeo.attributes.position;
            for (let i = 0; i < pos.count; i++) {{
                const x = pos.getX(i);
                const y = pos.getY(i);
                const dist = Math.abs(x);
                pos.setZ(i, Math.sin(x * 0.1) * Math.cos(y * 0.1) * 8 - (dist * 0.1));
            }}
            mountainGeo.computeVertexNormals();

            const mountainMat = new THREE.MeshBasicMaterial({{
                color: 0x0e172a,
                wireframe: true,
                transparent: true,
                opacity: 0.35
            }});
            const mountain = new THREE.Mesh(mountainGeo, mountainMat);
            mountain.rotation.x = -Math.PI / 2.5;
            mountain.position.set(0, -10, -20);
            scene.add(mountain);

            // Floating Star Particles
            const starGeo = new THREE.BufferGeometry();
            const starCount = 300;
            const starPos = new Float32Array(starCount * 3);
            for (let i = 0; i < starCount * 3; i += 3) {{
                starPos[i] = (Math.random() - 0.5) * 120;
                starPos[i + 1] = Math.random() * 50 - 10;
                starPos[i + 2] = (Math.random() - 0.5) * 80;
            }}
            starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
            const starMat = new THREE.PointsMaterial({{ color: 0x38bdf8, size: 0.6, transparent: true, opacity: 0.7 }});
            const starField = new THREE.Points(starGeo, starMat);
            scene.add(starField);

            // Mouse Parallax Interaction
            let mouseX = 0, mouseY = 0;
            window.addEventListener('mousemove', (e) => {{
                mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
                mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
            }});

            function animate() {{
                requestAnimationFrame(animate);
                camera.position.x += (mouseX * 4 - camera.position.x) * 0.05;
                camera.position.y += (-mouseY * 2 + 5 - camera.position.y) * 0.05;
                camera.lookAt(0, 0, -20);
                moon.position.x += 0.002;
                mountain.rotation.z += 0.0003;
                renderer.render(scene, camera);
            }}
            animate();

            window.addEventListener('resize', () => {{
                if (!wrapper) return;
                camera.aspect = wrapper.clientWidth / wrapper.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(wrapper.clientWidth, wrapper.clientHeight);
            }});
        }})();
    </script>
</body>
</html>
"""

    with open(output_index, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[build] Successfully built {output_index} ({len(html)} bytes).")

if __name__ == "__main__":
    build()

