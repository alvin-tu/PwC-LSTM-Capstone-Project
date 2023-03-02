from matplotlib import pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union
import json
import math

# Open JSON file
f = open('results.json')

# Load JSON data, iterate through JSON and create coordinates
# for polygons for map
data = json.load(f)

with open("poly_coordinates.json", "w") as outfile:
    out_data = []
    for i in range(410537):
        lat = float(data[i]['Latitude'])
        lon = float(data[i]['Longitude'])


        # TL = Top Left
        # TR = Top Right
        # BL = Bottom Left
        # BR = Bottom Right
        polygon = {
            'TL_lat': str( lat + 0.00452186 ),
            'TL_lon': str( lon - (1/(2 * 111.32 * math.cos(lat * math.pi/180))) ),
            'TR_lat': str( lat + 0.00452186 ),
            'TR_lon': str( lon + (1/(2 * 111.32 * math.cos(lat * math.pi/180))) ),
            'BL_lat': str( lat - 0.00452186 ),
            'BL_lon': str( lon - (1/(2 * 111.32 * math.cos(lat * math.pi/180))) ),
            'BR_lat': str( lat - 0.00452186 ),
            'BR_lon': str( lon + (1/(2 * 111.32 * math.cos(lat * math.pi/180))) ),
            '2014_fire_prob': data[i]['2014_fire_prob'],
            '2015_fire_prob': data[i]['2015_fire_prob'],
            '2016_fire_prob': data[i]['2016_fire_prob'],
            '2017_fire_prob': data[i]['2017_fire_prob']
        }

        out_data.append(polygon)
        # json_object = json.dumps(polygon,indent=4)
        # outfile.write(json_object)

    json.dump(out_data, outfile)

# Open and load newly generated JSON file containing
# new coordinates
f = open('poly_coordinates.json')
data = json.load(f)
polys_04 = []
polys_02 = []
polys_008 = []
polys_006 = []
polys_004 = []
polys_002 = []
polys_00 = []
for i in range(410537):
    poly = Polygon([(float(data[i]['BL_lon']),float(data[i]['BL_lat'])),
                    (float(data[i]['TL_lon']),float(data[i]['TL_lat'])),
                    (float(data[i]['TR_lon']),float(data[i]['TR_lat'])),
                    (float(data[i]['BR_lon']),float(data[i]['BR_lat']))
                    ])
    if(float(data[i]['2017_fire_prob']) > 0.04):
        polys_04.append(poly)
    elif((float(data[i]['2017_fire_prob']) <= 0.04) and (float(data[i]['2017_fire_prob']) > 0.02)):
        polys_02.append(poly)
    elif((float(data[i]['2017_fire_prob']) <= 0.02) and (float(data[i]['2017_fire_prob']) > 0.008)):
        polys_008.append(poly)
    elif((float(data[i]['2017_fire_prob']) <= 0.008) and (float(data[i]['2017_fire_prob']) > 0.006)):
        polys_006.append(poly)
    elif((float(data[i]['2017_fire_prob']) <= 0.006) and (float(data[i]['2017_fire_prob']) > 0.004)):
        polys_004.append(poly)
    elif((float(data[i]['2017_fire_prob']) <= 0.004) and (float(data[i]['2017_fire_prob']) > 0.002)):
        polys_002.append(poly)
    else:
        polys_00.append(poly)

# Combine polygons with shared borders into single polygons
mergedPolys_04 = unary_union(polys_04)
mergedPolys_02 = unary_union(polys_02)
mergedPolys_008 = unary_union(polys_008)
mergedPolys_006 = unary_union(polys_006)
mergedPolys_004 = unary_union(polys_004)
mergedPolys_002 = unary_union(polys_002)
mergedPolys_00 = unary_union(polys_00)

# Create lists containting coordiantes of borders of generated polygons
externalPolys_04 = [list(poly.exterior.coords) for poly in mergedPolys_04.geoms]
externalPolys_02 = [list(poly.exterior.coords) for poly in mergedPolys_02.geoms]
externalPolys_008 = [list(poly.exterior.coords) for poly in mergedPolys_008.geoms]
externalPolys_006 = [list(poly.exterior.coords) for poly in mergedPolys_006.geoms]
externalPolys_004 = [list(poly.exterior.coords) for poly in mergedPolys_004.geoms]
externalPolys_002 = [list(poly.exterior.coords) for poly in mergedPolys_002.geoms]
externalPolys_00 = [list(poly.exterior.coords) for poly in mergedPolys_00.geoms]


with open("reduced_coordinates_04.json", "w") as outfile:
    json.dump(externalPolys_04, outfile, default = lambda x: [list(pair) for pair in x])
with open("reduced_coordinates_02.json", "w") as outfile:
    json.dump(externalPolys_02, outfile, default = lambda x: [list(pair) for pair in x])
with open("reduced_coordinates_008.json", "w") as outfile:
    json.dump(externalPolys_008, outfile, default = lambda x: [list(pair) for pair in x])
with open("reduced_coordinates_006.json", "w") as outfile:
    json.dump(externalPolys_006, outfile, default = lambda x: [list(pair) for pair in x])
with open("reduced_coordinates_004.json", "w") as outfile:
    json.dump(externalPolys_004, outfile, default = lambda x: [list(pair) for pair in x])
with open("reduced_coordinates_002.json", "w") as outfile:
    json.dump(externalPolys_002, outfile, default = lambda x: [list(pair) for pair in x])
with open("reduced_coordinates_00.json", "w") as outfile:
    json.dump(externalPolys_00, outfile, default = lambda x: [list(pair) for pair in x])

fig,[[axTOTAL, ax04,ax02,ax008],[ax006,ax004,ax002,ax00]] = plt.subplots(2,4)
for p in externalPolys_04:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#FF0000')
    axTOTAL.fill(x, y, color='#FF0000', alpha=0.5)
    ax04.plot(x, y, color='#FF0000')
    ax04.fill(x, y, color='#FF0000', alpha=0.5)

for p in externalPolys_02:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#FF8000')
    axTOTAL.fill(x, y, color='#FF8000', alpha=0.5)
    ax02.plot(x, y, color='#FF8000')
    ax02.fill(x, y, color='#FF8000', alpha=0.5)

for p in externalPolys_008:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#FFFF00')
    axTOTAL.fill(x, y, color='#FFFF00', alpha=0.5)
    ax008.plot(x, y, color='#FFFF00')
    ax008.fill(x, y, color='#FFFF00', alpha=0.5)

for p in externalPolys_006:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#40FF00')
    axTOTAL.fill(x, y, color='#40FF00', alpha=0.5)
    ax006.plot(x, y, color='#40FF00')
    ax006.fill(x, y, color='#40FF00', alpha=0.5)

for p in externalPolys_004:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#00FFFF')
    axTOTAL.fill(x, y, color='#00FFFF', alpha=0.5)
    ax004.plot(x, y, color='#00FFFF')
    ax004.fill(x, y, color='#00FFFF', alpha=0.5)

for p in externalPolys_002:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#0000FF')
    axTOTAL.fill(x, y, color='#0000FF', alpha=0.5)
    ax002.plot(x, y, color='#0000FF')
    ax002.fill(x, y, color='#0000FF', alpha=0.5)

for p in externalPolys_00:
    x, y = zip(*p)
    axTOTAL.plot(x, y, color='#BF00FF')
    axTOTAL.fill(x, y, color='#BF00FF', alpha=0.5)
    ax00.plot(x, y, color='#BF00FF')
    ax00.fill(x, y, color='#BF00FF', alpha=0.5)
    
plt.show()
