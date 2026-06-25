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
- **M2 — terrain (NEXT):** real 3D terrain mesh for the property. Client-side path (no
  server GDAL, nothing to install): the page loads a terrain-RGB / Terrarium DEM tile +
  open satellite/NAIP imagery for the bbox and builds a displaced mesh in three.js, with
  the boundary + lake draped on it. Reuses the georeferenced source-data. Open-source only
  (no Esri — canon Open-Source First).
- M3 — layers + POIs: wrist-menu toggles (boundary/roads/trails/lake/survey sheets/pins);
  POIs as labeled billboards.
- M4 — locomotion (flap-wings fly, swim over water) + the giant-intro descent.

## How to run it on the Quest
- **USB / adb-reverse (no install on the Quest):** `adb reverse tcp:8099 tcp:8099`; serve
  `farm-map/` locally on baobab :8099; open `http://localhost:8099/vr/` in the Quest
  browser (localhost = secure context); tap ENTER VR. Push the URL from the host:
  `adb shell am start -a android.intent.action.VIEW -d <url> com.oculus.browser`.
- **Tailnet:** deployed at https://mesquite.tailff9d96.ts.net/vr/ (needs Tailscale on the Quest).
- **Inspection:** the Quest blocks `adb screencap` of the VR compositor (DRM) — can't
  screenshot the headset view. Read page state via the browser's Chrome DevTools endpoint
  over adb instead (`adb forward` to the devtools socket), not screencap.
