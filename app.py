## Por Alfonso Espinoza

import streamlit as st
import folium
import pandas as pd
from geopy.distance import geodesic
from streamlit_folium import st_folium
from datos import CUENCA_NODES, GRAPH_EDGES
from tester import pathfinder



# ------------------------------------------------------
# CONFIGURACIÓN INICIAL
# ------------------------------------------------------
st.set_page_config(page_title="Rutas Óptimas en Cuenca - A*", layout="wide")

st.title("🗺️ Búsqueda de Rutas Óptimas en Cuenca - Algoritmo A*")
st.write("""
Esta aplicación utiliza el algoritmo **A\*** para encontrar la ruta más corta entre puntos de interés 
en la ciudad de **Cuenca, Ecuador**.  
La heurística es la **distancia euclidiana**, y los pesos de las rutas se calculan con la **fórmula de Haversine**.
""")

# ------------------------------------------------------
# PANEL LATERAL (sidebar)
# ------------------------------------------------------
st.sidebar.header("⚙️ Controles de Ruta")

# Selectbox de inicio y destino en la barra lateral
start_point = st.sidebar.selectbox("Selecciona el punto de **inicio**:", list(CUENCA_NODES.keys()))
end_point = st.sidebar.selectbox("Selecciona el punto de **destino**:", list(CUENCA_NODES.keys()))

# Botón de búsqueda en la barra lateral
buscar = st.sidebar.button("🚗 Buscar Ruta Óptima")

# ------------------------------------------------------
# SESIÓN PARA MANTENER RESULTADOS ENTRE RECARGAS
# ------------------------------------------------------
if "route" not in st.session_state:
    st.session_state["route"] = None
    st.session_state["distance"] = None
    st.session_state["explored"] = None

# ------------------------------------------------------
# LÓGICA PRINCIPAL
# ------------------------------------------------------
if buscar:
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
# MOSTRAR RESULTADOS Y MAPA
# ------------------------------------------------------
if st.session_state["route"]:
    path = st.session_state["route"]
    total_distance = st.session_state["distance"]
    explored = st.session_state["explored"]

    st.success(f"✅ Ruta encontrada: {' → '.join(path)}")
    col1, col2 = st.columns(2)
    col1.metric("Distancia total (km)", f"{total_distance:.2f}")
    col2.metric("Nodos explorados", explored)

    # Crear mapa centrado en el punto de inicio
    start_coords = (CUENCA_NODES[path[0]]["lat"], CUENCA_NODES[path[0]]["lon"])
    m = folium.Map(location=start_coords, zoom_start=14)

    # Marcadores
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

    # Línea de ruta
    route_coords = [(CUENCA_NODES[n]["lat"], CUENCA_NODES[n]["lon"]) for n in path]
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)

    # Mostrar mapa
    st_folium(m, width=900, height=550)


# ------------------------------------------------------
# Aquí diseñamos la tabla.
# ------------------------------------------------------
if st.session_state["route"]:
    ruta = st.session_state["route"]

    # Crear lista para almacenar datos
    tabla_datos = []

    # Recorrer los pares consecutivos de nodos en la ruta
    for i in range(len(ruta) - 1):
        lugar = ruta[i]
        destino = ruta[i + 1]
        coord_lugar = (CUENCA_NODES[lugar]["lat"], CUENCA_NODES[lugar]["lon"])
        coord_destino = (CUENCA_NODES[destino]["lat"], CUENCA_NODES[destino]["lon"])

        # Calcular distancia en kilómetros (usando geodesic)
        distancia_km = geodesic(coord_lugar, coord_destino).km

        tabla_datos.append({
            "Lugar": lugar,
            "Destino": destino,
            "Latitud": CUENCA_NODES[lugar]["lat"],
            "Longitud": CUENCA_NODES[lugar]["lon"],
            "Distancia (km)": round(distancia_km, 2)
        })

    # Crear DataFrame y mostrarlo con Streamlit
    df = pd.DataFrame(tabla_datos)
    st.markdown("### 📍 Tabla de la ruta seleccionada")
    st.dataframe(df, use_container_width=True)

    # Mostrar distancia total
    distancia_total = sum(df["Distancia (km)"])
    st.success(f"**Distancia total aproximada:** {round(distancia_total, 2)} km 🚗")