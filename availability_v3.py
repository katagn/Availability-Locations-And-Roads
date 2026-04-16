# Takes the address of hospitals, change it to the coordinates and plots them on the map of Latvia. Also calculates distance and time between two points using OSRM API.

import geopandas as gpd 
import folium
from shapely.geometry import Point
import requests
import pandas as pd
from openpyxl import load_workbook
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

data = pd.read_excel("hos_address.xlsx", header=1, usecols=["Name", "Address"])

geolocator = Nominatim(user_agent="slimnicas_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def get_coords(address):
    print(f"Meklē: {address}")
    location = geocode(address)
    if location:
        print(f"  -> {location.latitude}, {location.longitude}")
        return location.latitude, location.longitude
    print(f"  -> NAV ATRASTS")
    return None, None

data["Latitude"], data["Longitude"] = zip(*data["Address"].apply(get_coords))

data.to_excel("slimnicas.xlsx", index=False)


# loading data from Excel
data = pd.read_excel("slimnicas.xlsx", usecols=["Latitude", "Longitude", "Name"])


# load country borders
world = gpd.read_file(
    "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip"
)

# chooses country
chosen_country = world[world["NAME"] == "Latvia"]

# map centered in Latvia
m = folium.Map(
    location=[56.9, 24.5],
    zoom_start=7,
    tiles="OpenStreetMap"
)

# adding border
folium.GeoJson(
    chosen_country,
    name="Latvia"
).add_to(m)

# adding points
for row in data.itertuples():
    folium.Marker(
        location=[row.Latitude, row.Longitude],
        popup=row.Name,
        tooltip=row.Name
    ).add_to(m)
# saving map
m.save("latvia_map.html")

print("Map saved: latvia_map.html")


# coordinates (lon, lat) for calculating road
p1 = (24.1052, 56.9496)  # Rīga
p2 = (21.0108, 56.5047)  # Liepāja

url = f"http://router.project-osrm.org/route/v1/driving/{p1[0]},{p1[1]};{p2[0]},{p2[1]}?overview=false"

r = requests.get(url).json()

distance = r["routes"][0]["distance"]   # meters
duration = r["routes"][0]["duration"]   # seconds

print("Distance km:", distance/1000)
print("Time min:", duration/60)