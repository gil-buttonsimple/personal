#!/usr/bin/env python3
"""Serve the farm-map directory AND accept marked paths back from the browser.

`python3 -m http.server` can only send files, never receive, which is why marking a
missing trail used to end in a copy-paste. This adds one endpoint:

    POST /marks   body: {"paths": [[[lat,lon], ...], ...]}

It appends each path to source-data/marks.geojson as a LineString, timestamped. The
browser's Save button hits it and gets a count back. Nothing else changes: every
other URL is served straight off disk exactly as before.

Run:  python3 farm-map/serve_marks.py [port]
"""
import json, os, sys, datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
MARKS = os.path.join(ROOT, "source-data", "marks.geojson")


def load():
    if os.path.exists(MARKS):
        try:
            return json.load(open(MARKS))
        except Exception:
            pass
    return {"type": "FeatureCollection", "note": "paths Gil marked as MISSING from the extraction",
            "features": []}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        if self.path.rstrip("/") != "/marks":
            return self._json(404, {"error": "no such endpoint"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(n) or b"{}")
            paths = body.get("paths") or []
            if not paths:
                return self._json(400, {"error": "no paths in body"})

            fc = load()
            stamp = datetime.datetime.now().isoformat(timespec="seconds")
            for p in paths:
                if len(p) < 2:
                    continue
                fc["features"].append({
                    "type": "Feature",
                    "properties": {"marked_at": stamp, "status": "missing-from-extraction",
                                   "note": body.get("note", "")},
                    # GeoJSON is lon,lat; the browser hands us lat,lon
                    "geometry": {"type": "LineString",
                                 "coordinates": [[round(c[1], 7), round(c[0], 7)] for c in p]},
                })
            os.makedirs(os.path.dirname(MARKS), exist_ok=True)
            json.dump(fc, open(MARKS, "w"), indent=1)
            print("saved %d path(s); %d total in marks.geojson" % (len(paths), len(fc["features"])))
            return self._json(200, {"saved": len(paths), "total": len(fc["features"])})
        except Exception as e:
            return self._json(500, {"error": str(e)})

    def do_DELETE(self):
        if self.path.rstrip("/") != "/marks":
            return self._json(404, {"error": "no such endpoint"})
        if os.path.exists(MARKS):
            os.remove(MARKS)
        return self._json(200, {"cleared": True})

    def log_message(self, fmt, *args):
        if self.command != "GET":
            super().log_message(fmt, *args)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8891
    print("serving %s on 0.0.0.0:%d  (POST /marks to save)" % (ROOT, port))
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
