# Farm Map -- Firestick delivery (decision)

Last Updated: 2026-06-18 (session 27)
Status: Decision. How the K-Farm screensaver gets onto the living-room Firestick.

## The decision

Deliver the screensaver as a **live web page on the TV** (not a baked video loop).

- **Why live, not baked.** The page stays timely and can grow into a living
  dashboard rather than a fixed reel: a farm webcam, current weather, the live USGS
  gauge for the Catawba, today's date and season, "what's blooming this week." A
  baked MP4 is self-contained but frozen; the live page is the more producty,
  longer-term-interesting path. The satellite/terrain tiles are static 2024 imagery
  either way, so "live" costs nothing visually and buys the dashboard upside.

- **Page shown.** farm-map/natgeo.html (the Piedmont documentary: smooth flyover,
  layer reveals, POI pin cascade, documentary field-note pages).

## Mechanism on the stick

The stock Fire TV screensaver only shows Amazon Photos / ambient content -- it
cannot point at a URL. Fire OS's screensaver is Android's Daydream mechanism, so a
true idle-activated web screensaver is possible, but it needs an app the stock OS
does not ship.

- **Chosen: sideload a kiosk browser** (Fully Kiosk Browser) and set its built-in
  idle/screensaver timer to load the page. Full WebGL, so the live MapLibre
  flythrough plays exactly as on desktop, and it auto-takes-over on idle (hands-off).
- **Sideload is easy and remote-only:** the Downloader app (in the Amazon Appstore)
  fetches the kiosk-browser APK from the couch with the remote -- no PC, no cable, no
  ADB. "No sideloading at all" would cap us at a browser you launch by hand, not a
  hands-off screensaver; one APK unlocks the good version.

### Hardware caveat (confirm before buying time on this)

Requires an **Android-based Fire OS stick** (Fire TV Stick 4K, 4K Max, or older).
The newer **Fire TV Stick 4K Select runs Vega OS (Linux-based) and cannot run
Android apps or sideload at all** -- none of this works on that device. Confirm the
model first.

## Hosting

- **Host on the cloud instance, not baobab.** A permanent public URL the stick
  points at forever, independent of whether the laptop is on. This is what makes the
  live path durable. (The cloud instance is not yet running; standing it up and
  migrating services off baobab is tracked in the governance repo, Issues-first.)
- **Until the cloud box is up:** stage natgeo.html on a temporary static host / public
  URL to test the full Firestick flow now. The stick config does not change when we
  cut over -- only where the URL resolves.

## TV-tuning pass (done, session 28)

The screensaver/kiosk variant of natgeo.html is built. Open it as
`natgeo.html?tv=1` (plain `natgeo.html` is unchanged for desktop review):
- **Couch type:** `?tv=1` scales the documentary type up for living-room distance.
- **Cursor:** auto-hides after 3s of stillness, returns on mouse movement (so it
  is invisible when unattended but still clickable on a desktop).
- **Network-failure fallback:** if MapLibre or its tiles cannot load, a calm
  slideshow of the local 1995 survey plates (demo/rectified/) plus the title and
  rotating field notes takes over, all from local files, no network. A 12s
  watchdog triggers it if the live map never comes up, and a guard catches the
  case where the MapLibre library itself (CDN) fails to load.

Remaining nuance:
- Mid-run tile loss *after* a successful load is not yet caught (the watchdog only
  covers startup). Low priority for a generally-online TV.
- The MapLibre library still loads from the unpkg CDN. For a truly offline-robust
  kiosk, vendor maplibre-gl.js + .css locally so there is no remote dependency.
