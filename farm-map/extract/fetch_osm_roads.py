#!/usr/bin/env python3
"""Pull ground-truth road geometry from OpenStreetMap for PoC validation.

The farm fronts Great Falls Highway (the 1221 address) and Hinton Road meets the
property at its south point. These are stable, independently-surveyed features, so
they are the yardstick: sheet-extracted roads, projected through a sheet's
homography, should land on these. Output is plain GeoJSON the demo loads directly.

Run:  python3 farm-map/extract/fetch_osm_roads.py
Out:  farm-map/source-data/reference/osm-roads.geojson
"""
import os, json, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))          # .../personal
REFD = os.path.join(REPO, "farm-map", "source-data", "reference")
OUT_NAMED = os.path.join(REFD, "osm-roads.geojson")        # named roads (validation)
OUT_ALL   = os.path.join(REFD, "osm-roads-all.geojson")    # full network (display)

# generous bbox around parcel 073 (S,W,N,E)
BBOX = (34.63, -81.19, 34.70, -81.12)
NAMES = ["Great Falls Highway", "Hinton Road"]            # the roads bounding the farm

def overpass(query):
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=urllib.parse.urlencode({"data": query}).encode(),
        headers={"User-Agent": "kfarm-map/1.0"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)

def to_features(data):
    feats = []
    for el in data.get("elements", []):
        if el.get("type") != "way" or "geometry" not in el:
            continue
        feats.append({
            "type": "Feature",
            "properties": {"name": el.get("tags", {}).get("name"),
                           "highway": el.get("tags", {}).get("highway"),
                           "osm_id": el["id"]},
            "geometry": {"type": "LineString",
                         "coordinates": [[p["lon"], p["lat"]] for p in el["geometry"]]},
        })
    return feats

def main():
    os.makedirs(REFD, exist_ok=True)
    b = f"{BBOX[0]},{BBOX[1]},{BBOX[2]},{BBOX[3]}"

    # 1) named boundary roads -- the ground-truth yardstick for the georeference
    parts = "".join(f'way["highway"]["name"="{n}"]({b});' for n in NAMES)
    named = to_features(overpass(f"[out:json][timeout:40];({parts});out geom;"))
    json.dump({"type": "FeatureCollection", "source": "OpenStreetMap via Overpass (ODbL)",
               "names": NAMES, "features": named}, open(OUT_NAMED, "w"))
    print("wrote", os.path.relpath(OUT_NAMED, REPO), "->", len(named), "way(s)")

    # 2) full road network in the bbox -- the authoritative road LAYER (not extracted)
    allr = to_features(overpass(f'[out:json][timeout:60];way["highway"]({b});out geom;'))
    json.dump({"type": "FeatureCollection", "source": "OpenStreetMap via Overpass (ODbL)",
               "bbox": BBOX, "features": allr}, open(OUT_ALL, "w"))
    print("wrote", os.path.relpath(OUT_ALL, REPO), "->", len(allr), "road ways")

if __name__ == "__main__":
    main()
