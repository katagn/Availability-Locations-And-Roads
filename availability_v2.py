# Takes coordinates of hospitals and plots them on the map of Latvia. Also calculates distance and time between two points using OSRM API.

import geopandas as gpd # type: ignore
import folium
from shapely.geometry import Point
import requests
import pandas as pd
from openpyxl import load_workbook



# loading data from Excel
data = pd.read_excel("slimnicas.xlsx", header=1, usecols=["Latitude", "Longitude", "Name"])


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