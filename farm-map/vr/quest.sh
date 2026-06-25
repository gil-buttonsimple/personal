#!/usr/bin/env bash
# Get a farm-map VR page onto the Quest 3 — the working recipe, captured so it is
# never rediscovered. Usage: ./quest.sh [page]   (default: terrain.html)
# Reaches the Quest over USB/adb; the QR is the reliable way IN (panel auto-launch
# from adb is flaky). Run from this dir (farm-map/vr) on baobab.
set -u
PAGE="${1:-terrain.html}"
PORT=8099
FARM_DIR="$(cd "$(dirname "$0")/.." && pwd)"   # farm-map/
LOCAL_URL="http://localhost:${PORT}/vr/${PAGE}"
TAILNET_URL="https://mesquite.tailff9d96.ts.net/vr/${PAGE}"

echo "== 1. serve farm-map locally on 127.0.0.1:${PORT} =="
if ! curl -sf -o /dev/null "http://127.0.0.1:${PORT}/vr/${PAGE}"; then
  ( cd "$FARM_DIR" && nohup python3 -m http.server "$PORT" --bind 127.0.0.1 >/tmp/farm-vr-serve.log 2>&1 & )
  sleep 1
fi
curl -sf -o /dev/null "http://127.0.0.1:${PORT}/vr/${PAGE}" && echo "   server OK" || { echo "   SERVER FAILED"; exit 1; }

echo "== 2. adb device + USB bridge (Quest localhost:${PORT} -> baobab) =="
adb get-state >/dev/null 2>&1 || { echo "   NO DEVICE — plug in the Quest, approve USB debugging"; exit 1; }
adb reverse tcp:${PORT} tcp:${PORT} >/dev/null && echo "   adb reverse set"

echo "== 3. headset awake? (ASLEEP = nothing renders; this is the #1 gotcha) =="
WAKE=$(adb shell dumpsys power 2>/dev/null | grep -oE "mWakefulness=[A-Za-z]+" | head -1)
echo "   ${WAKE:-unknown}"
[ "$WAKE" = "mWakefulness=Asleep" ] && echo "   >> PUT THE HEADSET ON (proximity sensor wakes the display)"

echo "== 4. QR to scan into the headset (panel auto-launch is unreliable; QR just works) =="
python3 - "$LOCAL_URL" "$TAILNET_URL" <<'PY'
import sys, qrcode, qrcode.image.svg, io
local, tnet = sys.argv[1], sys.argv[2]
def svg(d): b=io.BytesIO(); qrcode.make(d, image_factory=qrcode.image.svg.SvgPathImage, box_size=12, border=3).save(b); return b.getvalue().decode()
open("qr.html","w").write(f"""<!doctype html><meta charset=utf-8><title>K-Farm VR — scan to headset</title>
<style>body{{margin:0;background:#111;color:#eee;font-family:system-ui;text-align:center}}
.row{{display:flex;flex-wrap:wrap;justify-content:center;gap:40px;padding:24px}}
.card{{background:#fff;border-radius:14px;padding:18px}}.card svg{{width:360px;height:360px}}
p{{color:#9ad;font-size:13px;word-break:break-all;max-width:380px;margin:4px auto}}</style>
<h1>K-Farm VR — scan into the Quest</h1><div class=row>
<div><h2>USB bridge</h2><div class=card>{svg(local)}</div><p>{local}</p><p>while USB-tethered</p></div>
<div><h2>Tailnet</h2><div class=card>{svg(tnet)}</div><p>{tnet}</p><p>Quest needs Tailscale</p></div></div>""")
print("   wrote qr.html ->  http://localhost:%s/vr/qr.html" % "8099")
PY

echo "== 5. (optional) also try to push it to the browser directly =="
adb shell am start -n com.oculus.browser/.OculusLauncherActivity -a android.intent.action.VIEW -d "$LOCAL_URL" -f 0x10008000 >/dev/null 2>&1 && echo "   am start sent (may or may not surface a panel)"

cat <<EOF

DONE. Open  http://localhost:${PORT}/vr/qr.html  on the monitor and scan into the Quest.
Inspect the page state (screencap is DRM-blocked on Quest):
  adb forward tcp:9222 localabstract:chrome_devtools_remote && curl -s localhost:9222/json/list
EOF
