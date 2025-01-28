import math
import csv
from scipy.spatial import KDTree

earth_rad = 6371.0

geoloc_1 = []
geoloc_2 = []

#first dataset

with open('boston_locs.csv', mode ='r') as file: 
    csvFile = csv.DictReader(file)  
    header = csvFile.fieldnames
    #print("Header Line: ", header)
    for row in csvFile:
        try: 
            geoloc1_container = [row["latitude"], row["longitude"]]
            #print("success 1")
            #print(geoloc1_container)
        except (KeyError,ValueError): 
            #print("longitude or latitude not found or invalid")
            try: 
                geoloc1_container = [row["lat"], row["lng"]]
                #geoloc1_container = None  
                #print("Success 2")
            except (KeyError,ValueError):
                print("lat or lng not found or invalid")
                geoloc1_container = None  
        if(geoloc1_container != None): #should skip empty or invalid entries 
            geoloc_1.append(geoloc1_container)

#print("Geo locations:", geoloc_1)
#print("\n Second Dataset \n")
#second dataset 
with open('myloc.csv', mode ='r') as file: 
    csvFile = csv.DictReader(file)  
    header = csvFile.fieldnames
    #print("Header Line: ", header)
    for row in csvFile:
        try: 
            geoloc2_container = [row["latitude"], row["longitude"]]
            #print("success 1")
            #print(geoloc2_container)
        except (KeyError,ValueError): 
        #print("longitude or latitude not found or invalid")
            try: 
                geoloc2_container = [row["lat"], row["lng"]]
                #print("Success 2")
            except (KeyError,ValueError):
                print("lat or lng not found or invalid")
                geoloc2_container = None  
        if(geoloc2_container != None): #should skip empty or invalid entries 
            geoloc_2.append(geoloc2_container)

print("Geo locations:", geoloc_1)
print("Geo Locations: ", geoloc_2)

def geodetic_to_cartesian(lat, lon): # convert to cartesian coordinates
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    x = earth_rad * math.cos(lat_rad) * math.cos(lon_rad)
    y = earth_rad * math.cos(lat_rad) * math.sin(lon_rad)
    z = earth_rad * math.sin(lat_rad)
    return [x, y, z]

# Convert geoloc_1 to Cartesian coordinates and create KDTree
geoloc_1_cartesian = [geodetic_to_cartesian(lat, lon) for lat, lon in geoloc_1]
geoloc_1Tree = KDTree(geoloc_1_cartesian)

def haversine(lat1, long1, lat2,long2): 
    diff_lat = (lat2-lat1) * math.pi / 180.0 #convert to radius
    diff_long= (long2-long1) * math.pi / 180.0 #convert to radius

    lat1 = lat1 * math.pi / 180.0 #convert to rad
    lat2 = lat2 * math.pi / 180.0 #convert to rad
    #apply haversine formula
    #inside square root 
    a = math.sin(diff_lat/2) * math.sin(diff_lat/2) + math.sin(diff_long/2) * math.sin(diff_long/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * earth_rad * math.asin(math.sqrt(a))
    return c


matches = []
for loc2 in geoloc_2:
    loc2_cartesian = geodetic_to_cartesian(loc2[0], loc2[1])
    dist, index = geoloc_1Tree.query(loc2_cartesian)
    closest_loc = geoloc_1[index]
    distance = haversine(loc2[0], loc2[1], closest_loc[0], closest_loc[1])
    matches.append((loc2, closest_loc, distance))


# Call the function with example arrays

for match in matches:
    print(f"Point {match[0]} is closest to {match[1]}")   