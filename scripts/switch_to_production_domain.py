#!/usr/bin/env python3
"""
Production Domain Cutover Helper:
Usage:
  python3 scripts/switch_to_production_domain.py <target_dir> [domain]

When moving from `https://roasist.github.io/roasist-web/` to custom domain
`https://www.roasist.com/`:
  1. Rewrites `/roasist-web/` base-prefixed asset & route paths back to root `/`
     across all HTML, CSS, and JS files in `<target_dir>`.
  2. Writes `<target_dir>/CNAME` with `www.roasist.com` (or specified domain).
  3. Ensures `<target_dir>/index.html` exists.
"""
import glob
import os
import shutil
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/switch_to_production_domain.py <target_dir> [domain]")
        sys.exit(1)

    target_dir = os.path.abspath(sys.argv[1])
    domain = sys.argv[2] if len(sys.argv) > 2 else "www.roasist.com"

    if not os.path.isdir(target_dir):
        raise SystemExit(f"Directory not found: {target_dir}")

    # Ensure root index.html exists if exporting from public/
    local_home = os.path.join(target_dir, "kota-roasist-local.html")
    root_index = os.path.join(target_dir, "index.html")
    if os.path.exists(local_home) and not os.path.exists(root_index):
        shutil.copy2(local_home, root_index)
        print(f"[OK] Copied kota-roasist-local.html -> index.html")

    changed = 0
    for ext in ("*.html", "*.css", "*.js"):
        for fp in glob.glob(os.path.join(target_dir, "**", ext), recursive=True):
            if "/.git/" in fp:
                continue
            orig = open(fp, "r", encoding="utf-8", errors="ignore").read()
            upd = orig.replace("/roasist-web/", "/")
            if upd != orig:
                open(fp, "w", encoding="utf-8").write(upd)
                changed += 1

    cname_path = os.path.join(target_dir, "CNAME")
    open(cname_path, "w", encoding="utf-8").write(domain.strip() + "\n")
    print(f"[OK] Rewrote /roasist-web/ -> / across {changed} files and wrote CNAME ({domain})")


if __name__ == "__main__":
    main()
