#!/usr/bin/env python3
"""Farm-map local server: serves the static pages AND accepts saves.

Plain `python3 -m http.server` can only send files. This adds one endpoint,
POST /api/save, so the digitizer writes points straight into the repository
(farm-map/source-data/transforms/ or /traces/) with no download or copy-paste.

Run:  python3 farm-map/serve.py        (defaults to port 8099)
Open: http://127.0.0.1:8099/farm-map/digitizer/index.html
"""
import os, json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))   # .../farm-map
REPO = os.path.dirname(HERE)                         # .../personal  (served root)
SAVE = os.path.join(HERE, "source-data")

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=REPO, **k)

    def do_POST(self):
        if self.path != "/api/save":
            self.send_error(404); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n) or b"{}")
            sub = "traces" if body.get("kind") == "trace" else "transforms"
            name = os.path.basename(body.get("name", "out.json"))
            d = os.path.join(SAVE, sub); os.makedirs(d, exist_ok=True)
            path = os.path.join(d, name)
            with open(path, "w") as f:
                json.dump(body.get("data", {}), f, indent=1)
            rel = os.path.relpath(path, REPO)
            print("saved", rel)
            self._json(200, {"ok": True, "path": rel})
        except Exception as e:
            self._json(500, {"ok": False, "error": str(e)})

    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8099"))
    print(f"farm-map server on http://127.0.0.1:{port}  (saves -> {SAVE})")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
