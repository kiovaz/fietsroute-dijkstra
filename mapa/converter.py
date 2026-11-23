"""Copia o mapa do OSMnx para o Grafo da equipe.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
from nucleo.grafo import Grafo


def _nome(valor):
    if valor is None:
        return "sem nome"
    return " / ".join(valor) if isinstance(valor, list) else valor


def _contramao_liberada(valor):
    valores = valor if isinstance(valor, list) else [valor]
    return all(v == "no" for v in valores)


def converter_osmnx(G):
    grafo = Grafo(direcionado=True)
    for no, dados in G.nodes(data=True):
        grafo.adicionar_ponto(no, dados["y"], dados["x"])

    for u, v, dados in G.edges(data=True):
        if "geometry" in dados:
            geometria = [(lat, lon) for lon, lat in dados["geometry"].coords]
        else:
            geometria = [grafo.coordenadas(u), grafo.coordenadas(v)]
        nome = _nome(dados.get("name"))
        grafo.adicionar_trecho(u, v, dados["length"], nome, geometria)
        if _contramao_liberada(dados.get("oneway:bicycle")):
            grafo.adicionar_trecho(v, u, dados["length"], nome, geometria[::-1])
    return grafo
