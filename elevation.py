import urllib2
import json
import random
import MySQLdb
import math
import sys

POINTS_PER_REQUEST = 10

class Area:
    def __init__(self, name, minLat, maxLat, minLng, maxLng):
        self.name = name
        self.minLat = minLat
        self.maxLat = maxLat
        self.minLng = minLng
        self.maxLng = maxLng

idf = Area("idf", 48.066870, 49.264027, 1.425928, 3.598475)
area = idf

def getRandomPoint(minLat, maxLat, minLng, maxLng):
    rangeLat = maxLat - minLat
    rangeLng = maxLng - minLng
    lat = minLat + random.random() * rangeLat
    lng = minLng + random.random() * rangeLng
    if (random.random() < math.cos(lat * math.pi / 180)):
        return (lat, lng)
    else:
        return getRandomPoint(minLat, maxLat, minLng, maxLng)

points = []
for i in range(POINTS_PER_REQUEST):
    (random_lat, random_lng) = getRandomPoint(area.minLat, area.maxLat, area.minLng, area.maxLng)
    points.append(str(random_lat) + ',' + str(random_lng))


url='http://maps.googleapis.com/maps/api/elevation/json?sensor=false&locations=' + "|".join(points)

req = urllib2.Request(url)
opener = urllib2.build_opener()
f = opener.open(req)
json = json.loads(f.read())

db = MySQLdb.connect("localhost", "elevation", "elevation", "elevation" )
cursor = db.cursor()
try:
    for result in json['results']:
        lat = str(result['location']['lat'])
        lng = str(result['location']['lng'])
        resolution = str(result['resolution'])
        elevation = str(result['elevation'])
        sql = "insert into el_point(area, date, lat, lng, res, elv) values ('" + area.name + "', now(), " + lat + ", " + lng + ", " + resolution + ", " + elevation + ");";
        cursor.execute(sql)
    db.commit()
except:
    db.rollback()
    raise

db.close()
