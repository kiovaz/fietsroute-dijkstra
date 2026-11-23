"""Consultas de cruzamentos e trechos no Grafo do mapa real.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
import math

RAIO_TERRA_M = 6371008.8


def haversine(lat1, lon1, lat2, lon2):
    fi1, fi2 = math.radians(lat1), math.radians(lat2)
    delta_fi = fi2 - fi1
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_fi / 2) ** 2 + math.cos(fi1) * math.cos(fi2) * math.sin(delta_lambda / 2) ** 2
    return 2 * RAIO_TERRA_M * math.asin(math.sqrt(a))


def ponto_mais_proximo(grafo, lat, lon):
    melhor = None
    menor = math.inf
    for ponto in grafo.pontos():
        lat_ponto, lon_ponto = grafo.coordenadas(ponto)
        if lat_ponto is None:
            continue
        distancia = haversine(lat, lon, lat_ponto, lon_ponto)
        if distancia < menor:
            melhor, menor = ponto, distancia
    if melhor is None:
        raise ValueError("O grafo não tem pontos com coordenadas")
    return melhor


def trechos_por_nome(grafo, texto):
    busca = texto.strip().casefold()
    if not busca:
        raise ValueError("Informe o nome da via")
    return [(a, b) for a, b, dados in grafo.trechos() if busca in dados["nome"].casefold()]


def trechos_perto(grafo, lat, lon, raio_m):
    selecionados = []
    for a, b, _ in grafo.trechos():
        (lat_a, lon_a), (lat_b, lon_b) = grafo.coordenadas(a), grafo.coordenadas(b)
        if haversine(lat, lon, (lat_a + lat_b) / 2, (lon_a + lon_b) / 2) <= raio_m:
            selecionados.append((a, b))
    return selecionados
