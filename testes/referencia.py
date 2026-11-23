"""Dijkstra do NetworkX, usado apenas para validar o Dijkstra da equipe.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
import networkx as nx


def dijkstra_networkx(grafo, origem, destino):
    pontos = grafo.pontos()
    for ponto in (origem, destino):
        if ponto not in pontos:
            raise KeyError(ponto)
    g = nx.DiGraph()
    g.add_nodes_from(pontos)
    g.add_weighted_edges_from((u, v, custo) for u in pontos for v, custo in grafo.vizinhos(u))
    try:
        return nx.single_source_dijkstra(g, origem, destino, weight="weight")
    except nx.NetworkXNoPath:
        return float("inf"), []
