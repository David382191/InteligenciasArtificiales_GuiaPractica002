
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

    # 🆕 NUEVOS PUNTOS
    "Universidad de Cuenca": {"lat": -2.89836, "lon": -79.0095, "descripcion": "Principal universidad pública de Cuenca"},
    "Mall del Río": {"lat": -2.90967, "lon": -79.00345, "descripcion": "Centro comercial más grande de la ciudad"},
    "Parque de la Madre": {"lat": -2.9012, "lon": -79.0048, "descripcion": "Parque urbano popular"},
    "Río Tomebamba": {"lat": -2.9048, "lon": -79.0002, "descripcion": "Río emblemático que cruza la ciudad"},
    "Estadio Alejandro Serrano": {"lat": -2.904, "lon": -79.0047, "descripcion": "Estadio principal de Cuenca"},
    "Hospital del IESS": {"lat": -2.8939, "lon": -78.9973, "descripcion": "Hospital general de Cuenca"},
    "Aeropuerto Mariscal La Mar": {"lat": -2.8895, "lon": -78.9848, "descripcion": "Aeropuerto de la ciudad"},
    "Plaza San Blas": {"lat": -2.89685, "lon": -78.9986, "descripcion": "Plaza y templo histórico"},
    "Museo Remigio Crespo": {"lat": -2.9009, "lon": -79.0009, "descripcion": "Museo cultural de Cuenca"},
    "El Vergel": {"lat": -2.9023, "lon": -79.0018, "descripcion": "Barrio residencial céntrico"},
}


# 2 ARISTAS (CONEXIONES)
GRAPH_EDGES = {
    "Catedral Nueva": ["Parque Calderón", "Parque de la Madre", "Plaza San Blas"],
    "Parque Calderón": ["Catedral Nueva", "Puente Roto", "Parque de la Madre", "Plaza San Blas"],
    "Puente Roto": ["Parque Calderón", "Museo Pumapungo", "Río Tomebamba", "Mirador de Turi"],
    "Museo Pumapungo": ["Puente Roto", "Terminal Terrestre", "Museo Remigio Crespo"],
    "Terminal Terrestre": ["Museo Pumapungo", "Aeropuerto Mariscal La Mar", "Mall del Río"],
    "Mirador de Turi": ["Puente Roto", "Mall del Río"],
    
    # No te pierdas. CONEXIONES NUEVAS
    "Universidad de Cuenca": ["Parque de la Madre", "Estadio Alejandro Serrano", "Catedral Nueva"],
    "Mall del Río": ["Mirador de Turi", "Terminal Terrestre", "El Vergel"],
    "Parque de la Madre": ["Universidad de Cuenca", "Catedral Nueva", "Estadio Alejandro Serrano"],
    "Río Tomebamba": ["Puente Roto", "El Vergel"],
    "Estadio Alejandro Serrano": ["Parque de la Madre", "El Vergel", "Universidad de Cuenca"],
    "Hospital del IESS": ["Aeropuerto Mariscal La Mar", "Plaza San Blas"],
    "Aeropuerto Mariscal La Mar": ["Hospital del IESS", "Terminal Terrestre"],
    "Plaza San Blas": ["Catedral Nueva", "Hospital del IESS", "Museo Remigio Crespo"],
    "Museo Remigio Crespo": ["Museo Pumapungo", "Plaza San Blas", "El Vergel"],
    "El Vergel": ["Museo Remigio Crespo", "Estadio Alejandro Serrano", "Mall del Río", "Río Tomebamba"],
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
