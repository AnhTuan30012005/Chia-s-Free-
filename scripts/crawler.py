# -*- coding: utf-8 -*-
"""
Studio Archive Air-Gapped Crawler & Sanitizer
Syncs new resources from public feeds, sanitizes names,
stores metadata in public resources.json (ZERO URLs),
and vaults raw Drive URLs exclusively into local git-ignored vault files.
"""

import os
import json
import urllib.request
import urllib.parse
import re

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "resources.json")
SECRET_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "resources_vault_secret.json")
KV_FILE = os.path.join(os.path.dirname(__file__), "..", "backend-cloudflare", "vault_kv_data.json")

FEED_URL = "https://www.tungmuvang.in/feeds/posts/default?alt=json&max-results=50"

BANNED_WORDS = [
    r"Tùng Mũ Vàng", r"TÙNG MŨ VÀNG", r"TungMuVang", r"tungmuvang",
    r"TMV", r"tmv", r"ZunPhoto", r"Zun Photo", r"zunphoto"
]

def sanitize_text(text):
    if not text:
        return ""
    clean = text
    for bw in BANNED_WORDS:
        clean = re.sub(bw, "Studio Pro", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean

def extract_drive_from_redirect(url):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "url" in qs:
        return qs["url"][0]
    return url

def run_sync():
    print("Starting Air-Gapped Studio Feed Sync...")
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        existing_resources = json.load(f)

    # Load secret vault to avoid duplicate URL checks
    vault_data = []
    if os.path.exists(SECRET_FILE):
        try:
            with open(SECRET_FILE, "r", encoding="utf-8") as f:
                vault_data = json.load(f)
        except Exception:
            vault_data = []

    existing_titles = set(item.get("title", "").lower() for item in existing_resources)
    existing_urls = set(item.get("url", "") for item in vault_data if "url" in item)

    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Warning: Could not fetch feed: {e}")
        return

    entries = data.get("feed", {}).get("entry", [])
    print(f"Feed fetched: {len(entries)} posts retrieved.")

    new_public_items = 0
    next_stt = max([item.get("stt", 0) for item in existing_resources] + [0]) + 1

    kv_payload = []
    if os.path.exists(KV_FILE):
        try:
            with open(KV_FILE, "r", encoding="utf-8") as f:
                kv_payload = json.load(f)
        except Exception:
            kv_payload = []

    for e in entries:
        raw_title = e.get("title", {}).get("$t", "")
        content = e.get("content", {}).get("$t", "")

        drives = re.findall(r'https://drive\.google\.com/[^\s"\'<>]+', content)
        redirects = re.findall(r'https://www\.tungmuvang\.in/p/chuyen-huong[^\s"\'<>]+', content)

        target_url = None
        if redirects:
            target_url = extract_drive_from_redirect(redirects[0])
        elif drives:
            target_url = drives[0]

        if not target_url or "drive.google.com" not in target_url:
            continue

        clean_title = sanitize_text(raw_title)

        if target_url in existing_urls or clean_title.lower() in existing_titles:
            continue

        cats = [c.get("term", "") for c in e.get("category", [])]
        cat_code = "software"
        cat_name = "Phần Mềm & Panel"

        cat_str = " ".join(cats).lower() + " " + clean_title.lower()
        if any(k in cat_str for k in ["preset", "màu", "picture style"]):
            cat_code = "preset"
            cat_name = "Preset & Picture Style"
        elif any(k in cat_str for k in ["raw", "stock"]):
            cat_code = "raw"
            cat_name = "Kho Stock RAW Gốc"
        elif any(k in cat_str for k in ["psd", "layout", "album", "typo"]):
            cat_code = "psd"
            cat_name = "Layout PSD & Đồ Họa"
        elif any(k in cat_str for k in ["khoá học", "khóa học", "tài liệu", "font"]):
            cat_code = "courses"
            cat_name = "Khóa Học & Tài Liệu"

        code = f"L-{next_stt:02d}"

        # 1. Public Item (Air-gapped: ZERO URLs)
        public_entry = {
            "code": code,
            "stt": next_stt,
            "series": "lab",
            "series_name": "Lab Tools",
            "series_badge": "L",
            "title": clean_title,
            "category": cat_code,
            "cat_name": cat_name,
            "format": "Google Drive Cloud",
            "platform": "Universal",
            "tag": "Auto Synced",
            "desc": f"Tài nguyên {clean_title} được đồng bộ vào kho an toàn Cloudflare Edge.",
            "has_link": True
        }

        # 2. Secret Vault Item (Git-ignored)
        secret_entry = dict(public_entry)
        secret_entry["url"] = target_url

        existing_resources.append(public_entry)
        vault_data.append(secret_entry)
        kv_payload.append({"key": f"res:{code}", "value": target_url})

        existing_urls.add(target_url)
        existing_titles.add(clean_title.lower())
        next_stt += 1
        new_public_items += 1
        print(f" + Added air-gapped item #{code}: {clean_title}")

    if new_public_items > 0:
        # Write sanitized public resources.json (0 URLs)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_resources, f, ensure_ascii=False, indent=2)

        # Write secret backup (git-ignored)
        with open(SECRET_FILE, "w", encoding="utf-8") as f:
            json.dump(vault_data, f, ensure_ascii=False, indent=2)

        # Write KV bulk data for Cloudflare Workers (git-ignored)
        with open(KV_FILE, "w", encoding="utf-8") as f:
            json.dump(kv_payload, f, ensure_ascii=False, indent=2)

        print(f"Sync complete: {new_public_items} items added without exposing raw URLs.")
        try:
            from build_html import build
            build()
            print("Successfully regenerated index.html")
        except Exception as ex:
            print(f"Error rebuilding HTML: {ex}")
    else:
        print("Sync complete: No new resources to add.")

if __name__ == "__main__":
    run_sync()
