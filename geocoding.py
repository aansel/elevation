import httputils
import json
import random
import MySQLdb
import math
import sys

NB_REQUESTS = 10

def getIdLocality(locality, area_lv2, area_lv1, country, postal_code):
    db = MySQLdb.connect("localhost", "elevation", "elevation", "elevation" )
    cursor = db.cursor()
    try:
        # Area LV1
        selectAreaLv1 = "select id_area_lv1 from el_area_lv1 where name=\"" + area_lv1  + "\""
        cursor.execute(selectAreaLv1)
        resSelectLv1 = cursor.fetchone()
        if (resSelectLv1 == None):
            insertAreaLv1 = "insert into el_area_lv1 (id_country, name) values (1, \"" + area_lv1 + "\")"
            cursor.execute(insertAreaLv1)
            db.commit()
            cursor.execute(selectAreaLv1)
            idAreaLv1 = cursor.fetchone()[0]
        else:
            idAreaLv1 = resSelectLv1[0]

        # Area LV2
        selectAreaLv2 = "select id_area_lv2 from el_area_lv2 where name=\"" + area_lv2  + "\""
        cursor.execute(selectAreaLv2)
        resSelectLv2 = cursor.fetchone()
        if (resSelectLv2 == None):
            insertAreaLv2 = "insert into el_area_lv2 (id_area_lv1, name) values (" + str(idAreaLv1) + ", \"" + area_lv2 + "\")"
            cursor.execute(insertAreaLv2)
            db.commit()
            cursor.execute(selectAreaLv2)
            idAreaLv2 = cursor.fetchone()[0]
        else:
            idAreaLv2 = resSelectLv2[0]

        # Locality
        selectLocality = "select id_locality from el_locality where name=\"" + locality  + "\" and id_area_lv2=" + str(idAreaLv2)
        cursor.execute(selectLocality)
        resLocality = cursor.fetchone()
        if (resLocality == None):
            insertLocality = "insert into el_locality (id_area_lv2, name, zip_code) values (" + str(idAreaLv2) + ", \"" + locality + "\", " + postal_code + ")"
            cursor.execute(insertLocality)
            db.commit()
            cursor.execute(selectLocality)
            idLocality = cursor.fetchone()[0]
        else:
            idLocality = resLocality[0]
            updateLocality = "update el_locality set zip_code=\"" + postal_code + "\" where id_locality=" + str(idLocality)
            cursor.execute(updateLocality)

        db.commit()
        db.close()
        return idLocality
    except:
        db.rollback()
        db.close()
        return -1


def updateLocality():
    
    db = MySQLdb.connect("localhost", "elevation", "elevation", "elevation" )
    cursor = db.cursor()
    try:
        select = "select id, lat, lng from el_point where id_locality is null limit 1"
        cursor.execute(select)
        res = cursor.fetchone()
        if (res != None):
            idPoint = res[0]
            lat = res[1]
            lng = res[2]
 
            url='https://maps.googleapis.com/maps/api/geocode/json?latlng=' + str(lat) + ',' + str(lng) + '&sensor=false&language=fr'
            jsonRes = json.loads(httputils.get(url))

            idLocality = -1
            locality = None
            area_lv2 = None
            area_lv1 = None
            country = None
            postal_code = None
            for result in jsonRes['results']:
                if ("locality" in result['types']):
                    for component in result['address_components']:
                        if ("locality" in component['types']):
                            locality = component['long_name']
                        if ("administrative_area_level_2" in component['types']):
                            area_lv2 = component['long_name']
                        if ("administrative_area_level_1" in component['types']):
                            area_lv1 = component['long_name']
                        if ("country" in component['types']):
                            country = component['long_name']
                if ("postal_code" in result['types']):
                    for component in result['address_components']:
                        if ("postal_code" in component['types']):
                            postal_code = component['long_name']

            if (locality and area_lv2 and area_lv1 and country and postal_code):
                idLocality = getIdLocality(locality, area_lv2, area_lv1, country, postal_code)

            update = "update el_point set id_locality=" + str(idLocality) + " where id=" + str(idPoint)
            cursor.execute(update)
        db.commit()
    except:
        db.rollback()
        raise
    db.close()

for i in range(0, NB_REQUESTS):
    updateLocality()
