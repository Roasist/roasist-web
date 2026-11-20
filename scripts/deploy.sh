#!/bin/bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

COMMIT_MSG="${1:-chore(deploy): auto deploy update to www.roasist.com}"
BUILD_DIR="/tmp/roasist-veridyen-public_html"
FULL_ZIP="/tmp/roasist-veridyen-full.zip"
CODE_ZIP="/tmp/roasist-veridyen-code.zip"

echo "[1/5] Veridyen üretim paketi derleniyor ve doğrulanıyor..."
python3 scripts/build_veridyen_package.py "$BUILD_DIR" "$FULL_ZIP"
cp -f "$REPO_ROOT/.cpanel.yml" "$BUILD_DIR/.cpanel.yml"

rm -f "$CODE_ZIP"
(
  cd "$BUILD_DIR"
  python3 -c '
import os, zipfile
skip_ext = {".mp4", ".jpg", ".jpeg", ".png", ".webp", ".woff2", ".ico"}
with zipfile.ZipFile("/tmp/roasist-veridyen-code.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
    for r, ds, fs in os.walk("."):
        ds.sort()
        for f in sorted(fs):
            ext = os.path.splitext(f)[1].lower()
            if ext in skip_ext:
                continue
            ap = os.path.join(r, f)
            rp = os.path.relpath(ap, ".").replace(os.sep, "/")
            zf.write(ap, rp)
'
)

echo "[2/5] Kaynak kodlar GitHub (main) dalına gönderiliyor..."
git add -A
if ! git diff --cached --quiet; then
  git commit -m "$COMMIT_MSG"
else
  echo "      (main dalında yeni commit gerektiren değişiklik yok)"
fi
git push origin main

echo "[3/5] Üretim ağacı GitHub (veridyen-production) dalına eşitleniyor..."
(
  cd "$BUILD_DIR"
  git init -q -b veridyen-production
  git add -A
  git commit -q -m "build(veridyen): $COMMIT_MSG"
  git push -q -f https://github.com/Roasist/roasist-web.git veridyen-production
)

SECRET="${ROASIST_WEB_DEPLOY_SECRET:-}"
if [ -z "$SECRET" ] && [ -f "$HOME/.gemini/roasist_web_deploy_secret" ]; then
  SECRET="$(tr -d '\r\n ' < "$HOME/.gemini/roasist_web_deploy_secret")"
fi

if [ -z "$SECRET" ]; then
  echo "[4/5] Yerel deploy anahtarı bulunamadı; dağıtım GitHub Actions üzerinden otomatik tamamlanacak."
  rm -rf "$BUILD_DIR" "$FULL_ZIP" "$CODE_ZIP"
  exit 0
fi

echo "[4/5] Canlı sunucuya (https://www.roasist.com) otomatik dağıtılıyor..."
HTTP_STATUS=$(curl -s -o /tmp/roasist_deploy_res.json -w "%{http_code}" \
  -X POST \
  -H "X-Roasist-Deploy-Secret: $SECRET" \
  "https://www.roasist.com/deploy_webhook.php?mode=github_pull" || echo "000")

if [ "$HTTP_STATUS" != "200" ]; then
  echo "      GitHub Pull yanıtı ($HTTP_STATUS), doğrudan HTTPS paket yüklemesi (Direct Payload) deneniyor..."
  HTTP_STATUS=$(curl -s -o /tmp/roasist_deploy_res.json -w "%{http_code}" \
    -X POST \
    -H "X-Roasist-Deploy-Secret: $SECRET" \
    -F "payload=@$CODE_ZIP" \
    "https://www.roasist.com/deploy_webhook.php?mode=payload" || echo "000")
fi

echo "      Deploy HTTP Kodu: $HTTP_STATUS"
cat /tmp/roasist_deploy_res.json || true
echo ""

if [ "$HTTP_STATUS" != "200" ]; then
  echo "[UYARI] Webhook henüz 200 dönmedi (ilk kurulumda deploy_webhook.php bir kez yüklenmelidir)."
  rm -rf "$BUILD_DIR" "$FULL_ZIP" "$CODE_ZIP" /tmp/roasist_deploy_res.json
  exit 1
fi

echo "[5/5] OPcache & LiteSpeed önbelleği temizleniyor..."
CACHE_RES=$(curl -s -X POST -H "X-Roasist-Deploy-Secret: $SECRET" "https://www.roasist.com/opcache_clear.php" || true)
echo "      Cache Yanıtı: $CACHE_RES"

rm -rf "$BUILD_DIR" "$FULL_ZIP" "$CODE_ZIP" /tmp/roasist_deploy_res.json
echo "[TAMAMLANDI] https://www.roasist.com canlıda başarıyla güncellendi!"
