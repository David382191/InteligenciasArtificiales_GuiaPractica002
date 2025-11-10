## Por Alfonso Espinoza

import streamlit as st
import folium
from streamlit_folium import st_folium
from datos import CUENCA_NODES, GRAPH_EDGES
from tester import pathfinder

st.set_page_config(page_title="Rutas Óptimas en Cuenca - A*", layout="wide")

st.title("🗺️ Búsqueda de Rutas Óptimas en Cuenca - Algoritmo A*")
st.write("""
Esta aplicación usa el algoritmo **A\*** para encontrar la ruta más corta entre puntos de interés de **Cuenca, Ecuador**.
La heurística emplea la **distancia euclidiana**, y las distancias reales se calculan con la fórmula de **Haversine**.
""")

# ------------------------------------------------------
# INTERFAZ DE USUARIO
# ------------------------------------------------------
col1, col2 = st.columns(2)
with col1:
    start_point = st.selectbox("Selecciona el punto de **inicio**:", list(CUENCA_NODES.keys()))
with col2:
    end_point = st.selectbox("Selecciona el punto de **destino**:", list(CUENCA_NODES.keys()))

# ------------------------------------------------------
# LÓGICA DE RUTA
# ------------------------------------------------------
if "route" not in st.session_state:
    st.session_state["route"] = None
    st.session_state["distance"] = None
    st.session_state["explored"] = None

if st.button("Buscar Ruta Óptima 🚗"):
    if start_point == end_point:
        st.warning("⚠️ El punto de inicio y destino son el mismo.")
    else:
        path, total_distance, explored = pathfinder.find_path(start_point, end_point)
        if path:
            st.session_state["route"] = path
            st.session_state["distance"] = total_distance
            st.session_state["explored"] = explored
        else:
            st.error("❌ No se encontró una ruta entre los puntos seleccionados.")

# ------------------------------------------------------
# MOSTRAR RESULTADOS (si hay ruta en sesión)
# ------------------------------------------------------
if st.session_state["route"]:
    path = st.session_state["route"]
    total_distance = st.session_state["distance"]
    explored = st.session_state["explored"]

    st.success(f"✅ Ruta encontrada: {' → '.join(path)}")
    st.metric("Distancia total (km)", f"{total_distance:.2f}")
    st.metric("Nodos explorados", explored)

    # ------------------------------------------------------
    # MAPA FOLIUM
    # ------------------------------------------------------
    start_coords = (CUENCA_NODES[path[0]]["lat"], CUENCA_NODES[path[0]]["lon"])
    m = folium.Map(location=start_coords, zoom_start=14)

    # Marcadores de inicio y destino
    folium.Marker(
        location=start_coords,
        popup=f"Inicio: {path[0]}",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    end_coords = (CUENCA_NODES[path[-1]]["lat"], CUENCA_NODES[path[-1]]["lon"])
    folium.Marker(
        location=end_coords,
        popup=f"Destino: {path[-1]}",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    # Línea de la ruta
    route_coords = [(CUENCA_NODES[n]["lat"], CUENCA_NODES[n]["lon"]) for n in path]
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)

    # Mostrar mapa
    st_folium(m, width=900, height=500)
