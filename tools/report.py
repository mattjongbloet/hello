"""Print every page that is missing, locked or failed, from manifest.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(ROOT, "manifest.json")))
LABEL = {"home": "Home", "case": "Case study", "about": "About", "contact": "Contact"}
for sid in m["order"]:
    s = m["sites"][sid]
    rows = []
    for key, p in s["pages"].items():
        name = LABEL.get(key, f"Other {key.split('-')[-1]}")
        if p.get("missing"):
            rows.append(f"{name}: {p['missing']}" + (f" ({p['note']})" if p.get("note") else ""))
        elif p.get("failed"):
            rows.append(f"{name}: failed ({p['failed']})")
        else:
            bad = [f"{w}px {sh['error']}" for w, sh in (p.get("shots") or {}).items() if sh.get("error")]
            if bad: rows.append(f"{name}: failed at " + "; ".join(bad))
            if p.get("locked"): rows.append(f"{name}: locked")
    if not any(k.startswith("other-") for k in s["pages"]):
        rows.append("Other: none found")
    if rows:
        print(f"{s['name']} ({sid})")
        for r in rows: print("  - " + r)
