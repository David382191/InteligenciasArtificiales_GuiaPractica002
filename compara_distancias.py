#Hola
# compara_distancias.py
from datos import CUENCA_NODES, haversine_distance, euclidean_distance
from math import isclose

# IMPORTAR geodesic si quieres comparar con geopy (requiere geopy instalado)
try:
    from geopy.distance import geodesic
    geopy_available = True
except Exception:
    geopy_available = False

a = CUENCA_NODES["Parque Calderón"]
b = CUENCA_NODES["Puente Roto"]

lat1, lon1 = a["lat"], a["lon"]
lat2, lon2 = b["lat"], b["lon"]

print("Coordenadas (lat, lon):")
print(" - Parque Calderón:", (lat1, lon1))
print(" - Puente Roto     :", (lat2, lon2))
print()

# Haversine (tu función)
hav = haversine_distance(lat1, lon1, lat2, lon2)
print(f"Haversine    : {hav:.6f} km")

# Euclidiana aproximada (grado -> km)
euc = euclidean_distance(lat1, lon1, lat2, lon2)
print(f"Euclidiana   : {euc:.6f} km")

# Geopy geodesic (si está disponible)
if geopy_available:
    geo = geodesic((lat1, lon1), (lat2, lon2)).km
    print(f"Geodesic (geopy): {geo:.6f} km")
else:
    print("geopy.no está instalado — instala con: pip install geopy")
