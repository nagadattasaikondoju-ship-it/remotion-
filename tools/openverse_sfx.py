# Build a CC0 sound-effect library from Openverse (api.openverse.org) for the real-sfx / real-sound skills.
#   python3 tools/openverse_sfx.py                       → the default set below into assets/sfx/openverse/<category>/
#   python3 tools/openverse_sfx.py "camera shutter" 6     → one extra search (query, how many) into <query>/
# Only CC0 sounds by default (free for any use, no credit required); every file's source, creator and licence go to
# assets/sfx/openverse/credits.json. Openverse indexes the files; they are served by the provider (mostly Freesound).
import json, os, re, sys, time, urllib.parse, urllib.request
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "sfx", "openverse")
API = "https://api.openverse.org/v1/audio/"
DEFAULT = {  # category folder: (search query, how many)
    "whoosh": ("whoosh", 8), "impact": ("cinematic impact", 8), "boom": ("sub boom", 6), "riser": ("riser", 8),
    "swell": ("reverse swell", 6), "logo-sting": ("logo sting", 6), "chime": ("soft chime", 6), "pop": ("soft pop", 6),
    "shutter": ("camera shutter", 6), "keyboard": ("keyboard typing", 4), "room-tone": ("room tone", 4),
}

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "remotion-sfx-library/1.0"})
    with urllib.request.urlopen(req, timeout=40) as r: return r.read()

def fetch(folder, query, n, licence="cc0"):
    # (Freesound entries carry no category and the API's length filter is unreliable, so duration is checked below)
    q = urllib.parse.urlencode({"q": query, "license": licence, "page_size": min(20, n * 3)})
    try: res = json.loads(get(f"{API}?{q}"))["results"]
    except Exception as e:  # anonymous Openverse searches are rate-limited: stop this category, keep what we have
        print(f"{folder:12s} search failed ({e}); run again later to fill it"); return []
    out = os.path.join(ROOT, folder); os.makedirs(out, exist_ok=True); got = []
    for r in res:
        if len(got) >= n: break
        if not r.get("url") or not 0 < (r.get("duration") or 0) <= 20000: continue  # sound effects only: up to 20 s
        name = re.sub(r"[^a-z0-9]+", "-", r["title"].lower()).strip("-")[:48] or r["id"][:8]
        ext = os.path.splitext(urllib.parse.urlparse(r["url"]).path)[1] or ".mp3"
        path = os.path.join(out, f"{name}_{r['id'][:6]}{ext}")
        if not os.path.exists(path):
            try: data = get(r["url"])
            except Exception as e: print("  skip", r["title"], e); continue  # some providers refuse direct downloads
            open(path, "wb").write(data)
        got.append({"file": os.path.relpath(path, ROOT), "title": r["title"], "creator": r.get("creator"),
                    "licence": f"{r['license']} {r.get('license_version', '')}".strip(), "licence_url": r.get("license_url"),
                    "source": r.get("foreign_landing_url"), "provider": r.get("provider"), "duration_ms": r.get("duration")})
        time.sleep(0.3)
    print(f"{folder:12s} {len(got)} sounds")
    return got

if __name__ == "__main__":
    os.makedirs(ROOT, exist_ok=True); cred_path = os.path.join(ROOT, "credits.json")
    credits = json.load(open(cred_path)) if os.path.exists(cred_path) else []
    jobs = {re.sub(r"[^a-z0-9]+", "-", sys.argv[1].lower()): (sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 6)} if len(sys.argv) > 1 else DEFAULT
    for folder, (query, n) in jobs.items():
        have = {x["file"] for x in credits}
        for c in fetch(folder, query, n):
            if c["file"] not in have: credits.append(c)
        json.dump(credits, open(cred_path, "w"), indent=1, ensure_ascii=False)  # saved after every category
    print(f"{len(credits)} sounds in {os.path.normpath(ROOT)} (credits.json lists source, creator and licence for each)")
