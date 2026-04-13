import geopandas as gpd
import folium
from shapely.geometry import Point
import requests

# GPS punkti
points = [
    (56.9496, 25.1052, "Rīga"),
    (56.5047, 21.0108, "Liepāja"),
    (55.8747, 26.5362, "Daugavpils")
]

# load country borders
world = gpd.read_file(
    "https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip"
)

# chooses Latvia
latvia = world[world["NAME"] == "Latvia"]

# map centered in Latvia
m = folium.Map(
    location=[56.9, 24.5],
    zoom_start=7,
    tiles="OpenStreetMap"
)

# adding border
folium.GeoJson(
    latvia,
    name="Latvia"
).add_to(m)

# adding points
for lat, lon, name in points:
    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name
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