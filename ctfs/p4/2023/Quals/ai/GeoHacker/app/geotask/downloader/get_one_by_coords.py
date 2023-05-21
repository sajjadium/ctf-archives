import geotask.downloader.streetview as streetview
import matplotlib.pyplot as plt
import os
import random
import sys


def get_image_by_panoid(panoid):
    panorama = streetview.download_panorama_v3(panoid, zoom=2, disp=False)
    return panorama

def get_image_by_coords(lat, lon):
    sys.stdout.flush()
    panoids = streetview.panoids(lat=lat, lon=lon, closest=True)
    if len(panoids) == 0:
        raise Exception("no panoid here")

    panoid = panoids[0]['panoid']
    lat = panoids[0]['lat']
    lon = panoids[0]['lon']
    name = str(lat) + "_" + str(lon) + ".jpg"

    panorama = streetview.download_panorama_v3(panoid, zoom=2, disp=False)
    return panorama

if __name__ == '__main__':
    out = get_image_by_coords(sys.argv[1], sys.argv[2])
