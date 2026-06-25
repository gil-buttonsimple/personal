# Farm-map VR experience — build log

Tracked: gov#26 (Farm-map: ambient + VR experience). Hardware: Meta Quest 3
(see gov repo architecture/infrastructure.md, tech_stack.md). Stack: three.js +
WebXR, self-contained static page. Property bbox: lon -81.162126..-81.147044,
lat 34.648377..34.671521 (center 34.659949,-81.154585; ~1.28 km E-W x 2.57 km N-S).

This log exists because the first M1 validation (night of 2026-06-24) left NO durable
trace -- no commit, no file, no shell history -- and had to be re-run on 2026-06-25.
Capture VR progress HERE as it happens (lost-knowledge audit, s411).

## Status
- **M1 — smoke test (scale-grab): DONE / validated.** First validated in-headset the
  night of 2026-06-24; re-confirmed 2026-06-25. Page: `vr/index.html` (self-contained
  placeholder: checker ground, boundary ring, lake, landmark boxes, instruction panel).
  Mechanic: two-handed grip = scale-grab zoom anchored under the hands; one grip = drag.
  Verdict: the core zoom verb works on the Quest. Current tuning kept unless the founder
  flags a change (fold any into M2).
- **M2 — terrain: BUILT (2026-06-25), in headset.** `vr/terrain.html`. z15 Terrarium
  elevation displaced into a three.js mesh, draped with Sentinel-2 cloudless imagery (EOX,
  open, CORS-clean, no Esri), boundary + lake (source-data geojson) laid on the surface.
  Extent 2012×4024 m, ~56 m real relief, `?exag=` controls vertical exaggeration (default 2).
  Tiles pre-fetched same-origin under `vr/tiles/` (16 tiles, 788K) so it is reliable/offline.
  Reuses the M1 scale-grab. Headless build verified; in-headset tuning verdict (exag, initial
  scale, imagery zoom) pending from the founder. Possible next tune: bump imagery to z16/z17
  for crispness; raise mesh segments.
- M3 — layers + POIs: wrist-menu toggles (boundary/roads/trails/lake/survey sheets/pins);
  POIs as labeled billboards.
- M4 — locomotion (flap-wings fly, swim over water) + the giant-intro descent.

## How to run it on the Quest  — one command: `./quest.sh [page]`

`vr/quest.sh` is the captured recipe (serve + bridge + wake-check + QR + launch).
Run it instead of rediscovering the steps. The hard-won gotchas:

- **#1 gotcha: the headset must be AWAKE / worn.** If `mWakefulness=Asleep`
  (`adb shell dumpsys power | grep mWakefulness`), the display is OFF, NOTHING renders,
  and adb/CDP probes come back empty even though launches "succeed". Put the headset on
  (the proximity sensor wakes it). This was the 2026-06-25 "don't see it" blocker.
- **Reliable way IN = a QR code**, not adb panel-launch. `am start ... OculusLauncherActivity`
  often leaves the browser running with no visible panel (0 pages in CDP). `quest.sh`
  writes `qr.html`; open `http://localhost:8099/vr/qr.html` on the monitor and scan it
  into the Quest. (USB-bridge QR works while tethered; tailnet QR needs Tailscale on the Quest.)
- Bridge: `adb reverse tcp:8099 tcp:8099` (Quest localhost:8099 -> baobab); serve `farm-map/`
  on baobab `127.0.0.1:8099`.
- **Inspection: `adb screencap` is DRM-blocked** on the Quest (VR compositor) — returns an
  empty PNG, can't screenshot the headset view. Read page state via CDP instead:
  `adb forward tcp:9222 localabstract:chrome_devtools_remote && curl -s localhost:9222/json/list`
  (browser = `com.oculus.browser`; socket = `@chrome_devtools_remote`).

## Cable-free on the Quest (tailnet) — THE METHOD THAT WORKS

Got this working 2026-06-25. USB is for SETUP only; daily use is cable-free over the tailnet.

**One-time setup (done):**
1. Put the Quest on the tailnet:
   - Sideload Tailscale: `adb install tailscale-android-universal-<ver>.apk`
     (official, https://pkgs.tailscale.com/stable/ — F-Droid's build is stale, don't use it).
   - Open the app → **Log in**. It opens a device-auth web page in the Quest browser
     (`login.tailscale.com/a/<code>`).
   - **Do NOT sign in inside the headset** — typing the Google (gil@buttonsimple.com) password
     in VR is the wall. Instead, **approve the device from the PHONE**, where Dashlane autofills:
     scan the QR that the Tailscale login page itself shows ("use a QR code") with the phone
     camera, or open `login.tailscale.com/a/<code>` on the phone. Log in there, tap Approve.
   - The Quest joins as node **`quest-3`** (100.78.164.36). Membership is persistent — one-time.
2. Phone (`pixel10pro`) and Quest are now tailnet nodes with the rest of the fleet.

**Daily use (no cable):**
- In the Quest browser, open the tailnet URL (valid HTTPS → WebXR works):
  `https://mesquite.tailff9d96.ts.net/vr/terrain.html` — **bookmark it on the Quest** so it's one tap.

**Lessons — do NOT repeat:**
- A link shown in the desktop/TV chat is USELESS for a phone task — Gil can't retype a long URL
  into the phone. For anything the phone must open: deliver it TO the phone (a QR the phone
  scans, or push it), never as desktop chat text. (Showing a QR on his own TV to scan was goofy
  but the on-page Tailscale QR scanned by the phone is the clean version.)
- The painful Google-password-on-new-device problem is general (recurs across threads). Durable
  fix worth doing once: add a **passkey** to gil@buttonsimple.com (Dashlane holds passkeys) →
  future logins become a phone tap, never a typed password.
- **USB / adb-reverse (no install on the Quest):** `adb reverse tcp:8099 tcp:8099`; serve
  `farm-map/` locally on baobab :8099; open `http://localhost:8099/vr/` in the Quest
  browser (localhost = secure context); tap ENTER VR. Push the URL from the host:
  `adb shell am start -a android.intent.action.VIEW -d <url> com.oculus.browser`.
- **Tailnet:** deployed at https://mesquite.tailff9d96.ts.net/vr/ (needs Tailscale on the Quest).
- **Inspection:** the Quest blocks `adb screencap` of the VR compositor (DRM) — can't
  screenshot the headset view. Read page state via the browser's Chrome DevTools endpoint
  over adb instead (`adb forward` to the devtools socket), not screencap.
