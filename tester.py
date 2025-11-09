from a_star import pathfinder

inicio = "Terminal Terrestre"
destino = "Mirador de Turi"

camino, costo, explorados = pathfinder.find_path(inicio, destino)

print("Ruta encontrada:", camino)
print("Distancia total (km):", costo)
print("Nodos explorados:", explorados)
