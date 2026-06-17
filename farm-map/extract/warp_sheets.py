#!/usr/bin/env python3
"""Rectify each survey photo into ONE shared geographic frame for onion-skinning.

Each sheet has a homography (pixel -> world) from the digitizer, valid in the property
region (where its control apexes live). Projecting the photo's outer corners through it
extrapolates the perspective term by kilometres, so the photo CANNOT be draped by its
corners. Instead we go the other way: for every pixel of a fixed world-space grid over
the property, inverse-map through the homography to a source pixel and sample it. The
result is a north-up, georeferenced PNG that fills a known lat/lon box -- and since every
sheet uses the SAME box, the rectified sheets overlay each other (and the vector layers)
in exact registration. Outside-the-photo area is transparent.

Run:  python3 farm-map/extract/warp_sheets.py
Out:  farm-map/demo/rectified/<slug>.png   + prints the shared bounds for the demo.
"""
import os, json, glob, math
import numpy as np
from PIL import Image

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)                      # .../farm-map
TX=os.path.join(ROOT,'source-data','transforms')
ART=os.path.join(ROOT,'source-art')
OUT=os.path.join(ROOT,'demo','rectified')

# Shared target frame: the parcel area, padded. [S, W, N, E] (WGS84).
SOUTH, WEST, NORTH, EAST = 34.6455, -81.1655, 34.6770, -81.1445
WOUT = 1400                                     # output width in px; height keeps ground aspect

def main():
    os.makedirs(OUT, exist_ok=True)
    # ground aspect: metres E-W vs N-S at this latitude
    midlat=(SOUTH+NORTH)/2
    m_ew=(EAST-WEST)*111320.0*math.cos(math.radians(midlat))
    m_ns=(NORTH-SOUTH)*111320.0
    Hout=int(round(WOUT*m_ns/m_ew))
    # world coord of each output pixel centre (row 0 = north)
    lons=WEST+(EAST-WEST)*(np.arange(WOUT)+0.5)/WOUT
    lats=NORTH-(NORTH-SOUTH)*(np.arange(Hout)+0.5)/Hout
    LON,LAT=np.meshgrid(lons,lats)

    for fp in sorted(glob.glob(TX+'/*.json')):
        slug=os.path.basename(fp)[:-5]
        H=json.load(open(fp)).get('homography_px_to_world')
        if not H:
            print(slug,'-- no homography, skipped'); continue
        Hinv=np.linalg.inv(np.array(H,float))
        den=Hinv[2,0]*LON+Hinv[2,1]*LAT+Hinv[2,2]
        c=(Hinv[0,0]*LON+Hinv[0,1]*LAT+Hinv[0,2])/den
        r=(Hinv[1,0]*LON+Hinv[1,1]*LAT+Hinv[1,2])/den
        src=np.asarray(Image.open(os.path.join(ART,slug+'.jpg')).convert('RGB'))
        Hh,W=src.shape[:2]
        ci=np.round(c).astype(int); ri=np.round(r).astype(int)
        ok=(ci>=0)&(ci<W)&(ri>=0)&(ri<Hh)
        out=np.zeros((Hout,WOUT,4),np.uint8)
        ci=np.clip(ci,0,W-1); ri=np.clip(ri,0,Hh-1)
        out[...,:3]=src[ri,ci]
        out[...,3]=np.where(ok,255,0)
        Image.fromarray(out).save(os.path.join(OUT,slug+'.png'))
        print(f"{slug:32s} -> rectified/{slug}.png  ({WOUT}x{Hout}, {100*ok.mean():.0f}% covered)")

    print(f"\nShared bounds for the demo (L.imageOverlay):")
    print(f"  [[{SOUTH},{WEST}],[{NORTH},{EAST}]]")

if __name__=='__main__':
    main()
