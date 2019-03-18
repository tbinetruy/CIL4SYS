#  Test TomTom API

# Import the library to make the request to the TomTom API
import requests
# Import the Beautiful Soup Library
from bs4 import BeautifulSoup
# Import the library to read the image
import imageio
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
API_Key = 'zcSAVe7ZiVaLWdxhvUSRQcrAekW1mzkY'

latitude = '2.270668'
longitude = '48.824232'
delta = 0.005

import math

def deg2num(lat, lon, zoom):
    "Converts lat/lon to pixel coordinates in given zoom of the EPSG:4326 pyramid"

    res = 180 / 256.0 / 2**zoom
    px = (180 + lat) / res
    py = (90 + lon) / res

    tx = int( math.ceil( px / float(256) ) - 1 )
    ty = int( math.ceil( py / float(256) ) - 1 )
    return tx, ty


# # Make the Request (Dont foreget to change the API key)
# r = requests.get("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/16/json?point=" + longitude + "%2C" + latitude + "&unit=KMPH&key=" + API_Key)


# # # Print out the response to make sure it went through
# if (str(r) == '<Response [200]>' ):
#   print("Your Request Work!")

# else: 
#   print("Your Request didn't work, maybe check your API key at the end of the request")

# print(r)

# Grab the content from our request
# c = r.json()

# Find all the tags that contain a point in our route
# Points = c['flowSegmentData']['coordinates']['coordinate']

# Initialize our 2 arrays that will contain all the points
# lat = []
# long = []

# Iterate through all the points and add the lat and long to the correct array
# for point in Points:
#     lat.append(point['latitude'])
#     long.append(point['longitude'])

# Convert the points to floats    
# lat = [float(x) for x in lat]
# long = [float(x) for x in long]

# Import the plotting library

# plt.scatter(long,lat)
# plt.title('Route from TomTom API')
# plt.show()

# Coin haut gauche
#48.826919, 2.264532 
# Coin bas droite
#48.824232, 2.270668
print(deg2num(float(latitude), float(longitude), 15))
# Get the image for our map (MAKE SURE YOU PUT YOUR API KEY IN)
# r2 = requests.get("https://api.tomtom.com/map/1/staticimage?layer=basic&style=main&zoom=16&format=png&bbox=" + str(float(latitude) - delta) + "%2C" + str(float(longitude) - delta) + "%2C" + str(float(latitude) + delta) + "%2C" + str(float(longitude) + delta) + "&view=Unified&key="+API_Key)
# print(r2)


# Read the image from the request
# im = imageio.imread(r2.content)

# Create the figure
# plt.figure(figsize=(20,20))

# # Show the image
# plt.imshow(im)
# plt.show()

# plt.figure(figsize=(20,20))

# plt.imshow(im, extent = (float(latitude) - delta,float(latitude) + delta,float(longitude) - delta,float(longitude) + delta))

# plt.scatter(long,lat)
# plt.show()

# # Get the image for our map (MAKE SURE YOU PUT YOUR API KEY IN)
# r2 = requests.get("https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point=52.41072%2C4.84239&key=" +API_Key)

# TRYING TO GET TRAFFIC FLOW INFO

tile_x, tile_y = deg2num(float(latitude), float(longitude), 16) 

zoom = 16
tile_x = '33181'
tile_y = '22555'

r_map = requests.get("https://api.tomtom.com/map/1/tile/basic/main/" + str(zoom) + "/" + tile_x + "/" + tile_y + ".png?view=Unified&key=" + API_Key)
r_traffic = requests.get("https://api.tomtom.com/traffic/map/4/tile/flow/relative/" + str(zoom) + "/" + str(tile_x) + "/" + str(tile_y) + ".png?key=" + API_Key)
print(r_traffic)
print(tile_x)
im_traffic = imageio.imread(r_traffic.content)
im_map = imageio.imread(r_map.content)
im1 = plt.imshow(im_traffic, alpha = 0.5)
im2 = plt.imshow(im_map, alpha = 0.5)
plt.show()
