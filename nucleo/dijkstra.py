"""Dijkstra, versão sem heap, BFS e cálculos sobre uma rota.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
from nucleo.heap_min import HeapMin

INFINITO = float("inf")


def _iniciar(grafo, origem, destino):
    dist = {v: INFINITO for v in grafo.pontos()}
    if origem not in dist:
        raise KeyError(origem)
    if destino is not None and destino not in dist:
        raise KeyError(destino)
    dist[origem] = 0
    return dist, {origem: None}


def _relaxar(grafo, u, dist, anterior, fixados):
    tentativas = []
    for v, custo in grafo.vizinhos(u):
        if v in fixados:
            continue
        antes = dist[v]
        proposto = dist[u] + custo
        melhorou = proposto < antes
        if melhorou:
            dist[v] = proposto
            anterior[v] = u
        tentativas.append((v, antes, proposto, melhorou))
    return tentativas


def dijkstra(grafo, origem, destino=None):
    dist, anterior = _iniciar(grafo, origem, destino)
    fila = HeapMin()
    fila.inserir(0, origem)
    fixados = set()
    passos = []

    while not fila.vazio():
        custo, u = fila.extrair_minimo()
        if u in fixados:  # entrada antiga: o ponto já saiu com custo menor
            continue
        fixados.add(u)
        if u == destino:
            passos.append({"fixado": u, "custo": custo, "tentativas": []})
            break
        tentativas = _relaxar(grafo, u, dist, anterior, fixados)
        passos.append({"fixado": u, "custo": custo, "tentativas": tentativas})
        for v, _, proposto, melhorou in tentativas:
            if melhorou:
                fila.inserir(proposto, v)
    return dist, anterior, passos


def dijkstra_linear(grafo, origem, destino=None):
    dist, anterior = _iniciar(grafo, origem, destino)
    ordem = {origem: 0}  # mesma regra de desempate do contador do HeapMin
    contador = 1
    fixados = set()
    passos = []

    while True:
        abertos = [v for v in dist if v not in fixados and dist[v] < INFINITO]
        if not abertos:
            break
        u = min(abertos, key=lambda v: (dist[v], ordem[v]))
        fixados.add(u)
        if u == destino:
            passos.append({"fixado": u, "custo": dist[u], "tentativas": []})
            break
        tentativas = _relaxar(grafo, u, dist, anterior, fixados)
        passos.append({"fixado": u, "custo": dist[u], "tentativas": tentativas})
        for v, _, _, melhorou in tentativas:
            if melhorou:
                ordem[v] = contador
                contador += 1
    return dist, anterior, passos


def caminho(anterior, destino):
    if destino not in anterior:
        return []
    rota = []
    atual = destino
    while atual is not None:
        rota.append(atual)
        atual = anterior[atual]
    return rota[::-1]


def _somar(grafo, rota, campo):
    if not rota:
        return INFINITO
    total = 0
    for a, b in zip(rota, rota[1:]):
        try:
            total += grafo.trecho(a, b)[campo]
        except KeyError:  # trecho fechado: a rota deixou de existir
            return INFINITO
    return total


def custo_rota(grafo, rota):
    return _somar(grafo, rota, "custo")


def comprimento_rota(grafo, rota):
    return _somar(grafo, rota, "comprimento")


def bfs(grafo, origem, destino):
    _iniciar(grafo, origem, destino)
    anterior = {origem: None}
    fila = [origem]
    for u in fila:  # a lista cresce durante o laço e funciona como fila
        if u == destino:
            break
        for v, _ in grafo.vizinhos(u):
            if v not in anterior:
                anterior[v] = u
                fila.append(v)
    return anterior
