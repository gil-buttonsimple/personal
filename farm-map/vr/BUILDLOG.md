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
- **BEST way IN (s417) = a short all-numbers URL, finger-typed in-headset.** Serve farm-map
  on a non-privileged port with `/` 302-redirecting to the target page, bridge with
  `adb reverse`, and type the loopback URL on the Quest hand-tracking keyboard:
  **`127.0.0.1:1111`** (or `127.1:1111`). `127.0.0.1` is a secure context so WebXR works; the
  root-redirect keeps letters out of the path. Port MUST be >=1024 — Android adb reverse can't
  bind a privileged port, so `:80` fails ("cannot bind listener: Permission denied"). Recipe:
  a tiny python redirect server on `127.0.0.1:1111` (chdir farm-map/, `/`->302 `/vr/<page>.html`)
  + `adb reverse tcp:1111 tcp:1111`. The founder found finger-typing a 9-char numeric URL a
  game-changer; this beats both the QR dance and panel auto-launch.
- **No-typing push (agent-driven) = `am start -a android.intent.action.VIEW -d <url> com.oculus.browser`**
  over the USB bridge. This loaded terrain on 2026-06-25 (verified via CDP), so the plain VIEW
  form to `com.oculus.browser` WORKS — it's the `-n .../.OculusLauncherActivity` panel form
  (quest.sh step 5) that's flaky (browser runs, no visible panel, 0 pages in CDP).
- **QR fallback** (`quest.sh` writes `qr.html`; open `http://localhost:8099/vr/qr.html` on the
  monitor and scan into the Quest): USB-bridge QR works while tethered; tailnet QR needs
  Tailscale on the Quest. Superseded by the short-URL method above for everyday use.
- Bridge: `adb reverse tcp:8099 tcp:8099` (Quest localhost:8099 -> baobab); serve `farm-map/`
  on baobab `127.0.0.1:8099`.
- **Inspection: `adb screencap` is DRM-blocked** on the Quest (VR compositor) — returns an
  empty PNG, can't screenshot the headset view. Read page state via CDP instead:
  `adb forward tcp:9222 localabstract:chrome_devtools_remote && curl -s localhost:9222/json/list`
  (browser = `com.oculus.browser`; socket = `@chrome_devtools_remote`).

## Cable-free on the Quest (tailnet) — THE METHOD (one step left)

USB is for SETUP only; daily use is meant to be cable-free over the tailnet.

**STATUS at session 416 close — NOT fully finished.** `quest-3` joined the tailnet as a
member (device-auth approved on the phone — that part worked), BUT the Tailscale app on the
Quest is back on its "Welcome / Log in" screen and the VPN is NOT connected (`tailscale ping
quest-3` from the fleet = "unknown peer"), so the tailnet farm URL does NOT load on the
headset yet. **Remaining last step (next session):** in the Tailscale app on the Quest,
finish Log in / **Connect** (turn the VPN toggle ON) and approve the Android "set up a VPN
connection" system dialog. That dialog needs a controller tap in-headset (adb can't approve
the VPN consent). Until then, use the USB / adb-reverse route (`quest.sh`), which is proven.

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

## Session 417 (2026-06-25) — cordless delivery findings + the public-URL unlock

Spent the night trying to finish cable-free Tailscale login on the Quest. It did NOT complete.
Findings, so the next attempt skips the dead ends:

- **THE UNLOCK (reframes everything): a PoC does not need to be PRIVATE.** The only reason we
  need Tailscale at all is that the farm-map is tailnet-only (it carries property boundary/deed
  data). A throwaway AR/VR PoC has no sensitive data — so serve it on the PUBLIC internet over
  HTTPS and the entire Tailscale/login problem disappears: the Quest browser opens any public
  `https://` URL with NO login, NO tailnet, NO cable, and real TLS is the secure context WebXR
  needs. We privatized a throwaway and then fought the privacy all night. For the REAL farm-map
  (genuinely private), Tailscale still applies — fix that login with a passkey, not by hand.
- **`adb shell input text` is the wrong tool** for driving an in-headset login: it can't send
  unicode/special chars, so the `@` in the email mangled, and stray keyevents bumped the headset
  into Remote Desktop (`com.oculus.remotedesktop`). Use **ADBKeyboard** (senzhk/ADBKeyBoard,
  a sideloaded IME) instead — it injects any text via `am broadcast -a ADB_INPUT_TEXT --es msg
  '...'` reliably. Raw `input` is blind + fragile.
- **Tailscale Android CANNOT take an auth key** — open feature request since 2023
  (tailscale/tailscale #675, #8497). Do not retry the auth-key path on the Quest; it only works
  for Linux nodes (how cedar/yucca joined).
- **"Log in does nothing / copy the link out" is a KNOWN Quest bug** (tailscale/tailscale
  #16003). Critical mechanic: completing the login on the PHONE authorizes the ACCOUNT but does
  NOT hand the Quest APP a session (the redirect never returns to the app) — so the app stays on
  "Log in" and the VPN toggle won't flip. The login must finish in the QUEST's OWN browser to
  deep-link back into the app. (Confirmed live: app sat on Log in; CDP showed the
  `login.tailscale.com/login?next_url=%2Fa%2F<code>` tab in `com.oculus.browser`.)
- **A phone canNOT scan a QR shown INSIDE the headset** (it's behind the lenses). QR scanning
  works the other direction only. The Quest HAS a native QR reader (`com.oculus.os.qrcodereader`)
  and the Quest Browser scans physical QRs off a monitor/phone — that's the cordless delivery
  path once a URL is reachable.

**THE KEEPER IDEA — hidden VR launcher in our own app (filed: buttonsimple-app #173).**
Pure adb can't reliably set the Android clipboard (foreground-app restricted), so "copy the URL
to the clipboard" needs software on the headset — which is the opening for an app feature. Build
a hidden route in buttonsimple-app using `expo-clipboard` (`Clipboard.setStringAsync(url)`): tap
it on the Quest → URL lands on the clipboard → long-press the browser address bar → Paste → go.
No typing. The URL it copies can be driven from the DASHBOARD via a Convex field (reuse the Cast
/ Push Content plumbing, app#127), so baobab decides what the headset gets and the headset just
pastes. Durable, ours, doubles as the delivery channel for any future VR/AR content. Tonight's
stopgap if needed: sideload ADBKeyboard and set the clipboard from baobab over the cable.
