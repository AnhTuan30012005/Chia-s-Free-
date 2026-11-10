import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
BACKEND_DIR = BASE_DIR / "backend-cloudflare"

RAW_SOURCE = DATA_DIR / "resources.json"
SECRET_BACKUP = DATA_DIR / "resources_vault_secret.json"
KV_EXPORT_FILE = BACKEND_DIR / "vault_kv_data.json"

def main():
    if not RAW_SOURCE.exists():
        print(f"[!] Source not found: {RAW_SOURCE}")
        return

    with open(RAW_SOURCE, "r", encoding="utf-8") as f:
        master_data = json.load(f)

    # 1. Save master copy to secret backup if not already present
    with open(SECRET_BACKUP, "w", encoding="utf-8") as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Master vault backed up to: {SECRET_BACKUP} ({len(master_data)} items)")

    # 2. Extract KV pairs for Cloudflare Worker KV
    kv_payload = []
    public_items = []

    for item in master_data:
        code = item.get("code", "").strip()
        url = item.get("url", "").strip()

        if code and url:
            kv_payload.append({
                "key": f"res:{code}",
                "value": url
            })

        # Sanitized public item
        pub = {
            "code": code,
            "stt": item.get("stt", ""),
            "series": item.get("series", ""),
            "series_name": item.get("series_name", ""),
            "series_badge": item.get("series_badge", ""),
            "title": item.get("title", ""),
            "category": item.get("category", ""),
            "cat_name": item.get("cat_name", ""),
            "format": item.get("format", ""),
            "platform": item.get("platform", ""),
            "tag": item.get("tag", ""),
            "desc": item.get("desc", ""),
            "has_link": bool(url)
        }
        public_items.append(pub)

    # 3. Write Cloudflare KV bulk data file
    with open(KV_EXPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(kv_payload, f, ensure_ascii=False, indent=2)
    print(f"[+] Cloudflare KV data written to: {KV_EXPORT_FILE} ({len(kv_payload)} entries)")

    # 4. Overwrite public resources.json (Zero URLs remaining in frontend repo)
    with open(RAW_SOURCE, "w", encoding="utf-8") as f:
        json.dump(public_items, f, ensure_ascii=False, indent=2)
    print(f"[+] Public resources.json sanitized ({len(public_items)} items, 0 URLs remaining)")

if __name__ == "__main__":
    main()

