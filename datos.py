
##Cargar los datos de los puntos de interés de Cuenca (nodos) 
import math
from typing import Dict

# 1 NODOS
CUENCA_NODES: Dict[str, Dict[str, float]] = {
    "Catedral Nueva": {"lat": -2.8975, "lon": -79.005, "descripcion": "Centro histórico de Cuenca"},
    "Parque Calderón": {"lat": -2.89741, "lon": -79.00438, "descripcion": "Corazón de Cuenca"},
    "Puente Roto": {"lat": -2.90423, "lon": -79.00142, "descripcion": "Monumento histórico"},
    "Museo Pumapungo": {"lat": -2.90607, "lon": -78.99681, "descripcion": "Museo de antropología"},
    "Terminal Terrestre": {"lat": -2.89222, "lon": -78.99277, "descripcion": "Terminal de autobuses"},
    "Mirador de Turi": {"lat": -2.92583, "lon": -79.0040, "descripcion": "Mirador con vista panorámica"},
}

# 2 ARISTAS (CONEXIONES)
GRAPH_EDGES = {
    "Catedral Nueva": ["Parque Calderón", "Puente Roto", "Museo Pumapungo"],
    "Parque Calderón": ["Catedral Nueva", "Terminal Terrestre", "Puente Roto"],
    "Puente Roto": ["Catedral Nueva", "Parque Calderón", "Museo Pumapungo", "Mirador de Turi"],
    "Museo Pumapungo": ["Catedral Nueva", "Puente Roto", "Terminal Terrestre"],
    "Terminal Terrestre": ["Parque Calderón", "Museo Pumapungo", "Mirador de Turi"],
    "Mirador de Turi": ["Puente Roto", "Terminal Terrestre"],
}

# 3 - FUNCIONES DE DISTANCIA
def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia Haversine en km."""
    R = 6371.0
    lat1_rad, lat2_rad = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def euclidean_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distancia euclidiana aproximada en km (111 km ≈ 1°)."""
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) * 111.0
