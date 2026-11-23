"""Grafo em lista de adjacência usado pelo exemplo e pelo mapa real.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
import json
import math


class Grafo:
    def __init__(self, direcionado, permitir_negativo=False):
        self.direcionado = direcionado
        self.permitir_negativo = permitir_negativo
        self._adj = {}  # ponto -> {vizinho: dados}, na ordem de inserção
        self._coords = {}

    def adicionar_ponto(self, id, lat=None, lon=None):
        if id not in self._adj:
            self._adj[id] = {}
            self._coords[id] = (None, None)
        if lat is not None and lon is not None:
            self._coords[id] = (lat, lon)

    def adicionar_trecho(self, a, b, comprimento, nome="", geometria=None):
        if not math.isfinite(comprimento):
            raise ValueError(f"Comprimento inválido: {comprimento}")
        if comprimento < 0 and not self.permitir_negativo:
            raise ValueError(f"Custo negativo recusado: {comprimento}. O Dijkstra exige pesos não negativos.")
        self.adicionar_ponto(a)
        self.adicionar_ponto(b)
        self._inserir(a, b, comprimento, nome, geometria)
        if not self.direcionado:
            # shortcut: o sentido inverso reaproveita a geometria, trocar se um grafo não direcionado passar a tê-la.
            self._inserir(b, a, comprimento, nome, geometria)

    def _inserir(self, a, b, comprimento, nome, geometria):
        atual = self._adj[a].get(b)
        if atual is None or comprimento < atual["comprimento"]:
            self._adj[a][b] = {"comprimento": comprimento, "custo": comprimento, "nome": nome, "geometria": geometria}

    def alterar_custo(self, a, b, fator):
        if not math.isfinite(fator) or fator <= 0:
            raise ValueError(f"Fator recusado: {fator}. Use um fator positivo; para bloquear a rua, feche o trecho.")
        self._adj[a][b]["custo"] *= fator
        if not self.direcionado and a != b:
            self._adj[b][a]["custo"] *= fator

    def remover_trecho(self, a, b):
        del self._adj[a][b]
        if not self.direcionado and a != b:
            del self._adj[b][a]

    def vizinhos(self, u):
        return [(v, dados["custo"]) for v, dados in self._adj[u].items()]

    def pontos(self):
        return list(self._adj)

    def trechos(self):
        lista = []
        vistos = set()
        for a, vizinhos in self._adj.items():
            for b, dados in vizinhos.items():
                if self.direcionado or (b, a) not in vistos:
                    vistos.add((a, b))
                    lista.append((a, b, dict(dados)))
        return lista

    def trecho(self, a, b):
        return dict(self._adj[a][b])

    def coordenadas(self, v):
        return self._coords[v]

    def copiar(self):
        novo = Grafo(self.direcionado, self.permitir_negativo)
        novo._adj = {u: {v: dict(d) for v, d in viz.items()} for u, viz in self._adj.items()}
        novo._coords = dict(self._coords)
        return novo


def carregar_json(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    grafo = Grafo(direcionado=False)
    for ponto in dados["pontos"]:
        grafo.adicionar_ponto(ponto)
    for trecho in dados["trechos"]:
        grafo.adicionar_trecho(trecho["de"], trecho["para"], trecho["comprimento"])
    return grafo
