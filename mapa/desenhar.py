"""Mapa interativo com os pontos turísticos e a rota calculada pela equipe.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
Dados do mapa © colaboradores do OpenStreetMap (licença ODbL).
"""
import folium

from mapa.consultas import geometria_trecho, linha_da_rota


def _marcar_pontos(mapa, pontos):
    for ponto in pontos:
        folium.CircleMarker(
            (ponto["lat"], ponto["lon"]), radius=5, color="#444444", fill=True, fill_opacity=0.9, tooltip=ponto["nome"],
        ).add_to(mapa)


def desenhar_pontos(pontos, origem, destino):
    pontos = list(pontos)
    coordenadas = [(p["lat"], p["lon"]) for p in pontos]
    mapa = folium.Map(location=coordenadas[0], zoom_start=14, tiles="OpenStreetMap")
    _marcar_pontos(mapa, pontos)
    folium.Marker(
        (origem["lat"], origem["lon"]), tooltip=f"Origem: {origem['nome']}", icon=folium.Icon(color="green", icon="play"),
    ).add_to(mapa)
    folium.Marker(
        (destino["lat"], destino["lon"]), tooltip=f"Destino: {destino['nome']}", icon=folium.Icon(color="darkblue", icon="flag"),
    ).add_to(mapa)
    mapa.fit_bounds(coordenadas)
    return mapa


def desenhar_rota(grafo, rota, pontos=(), rota_anterior=None, empecilho=()):
    """Use o grafo original: ele mantém a geometria dos trechos fechados."""
    linha = linha_da_rota(grafo, rota)
    if not linha:
        raise ValueError("Não há rota para desenhar")

    mapa = folium.Map(location=linha[len(linha) // 2], zoom_start=14, tiles="OpenStreetMap")
    _marcar_pontos(mapa, pontos)
    for a, b in empecilho:
        folium.PolyLine(geometria_trecho(grafo, a, b), color="#d62728", weight=8, opacity=0.8, tooltip="Empecilho").add_to(mapa)
    if rota_anterior:
        folium.PolyLine(
            linha_da_rota(grafo, rota_anterior), color="#555555", weight=4, dash_array="8 8", tooltip="Rota anterior",
        ).add_to(mapa)
    folium.PolyLine(linha, color="#0b5cad", weight=5, tooltip="Rota de menor custo").add_to(mapa)
    folium.Marker(linha[0], tooltip="Origem", icon=folium.Icon(color="green", icon="play")).add_to(mapa)
    folium.Marker(linha[-1], tooltip="Destino", icon=folium.Icon(color="darkblue", icon="flag")).add_to(mapa)
    mapa.fit_bounds(linha)
    return mapa
