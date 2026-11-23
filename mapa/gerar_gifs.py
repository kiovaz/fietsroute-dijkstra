"""Gera antes da apresentação os três GIFs da demonstração.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
Dados do mapa © colaboradores do OpenStreetMap (licença ODbL).

Uso, na raiz do projeto: python -m mapa.gerar_gifs
"""
from pathlib import Path

import osmnx as ox
from matplotlib.animation import PillowWriter

from mapa.animar import criar_animacao
from mapa.baixar_mapa import ARQUIVO
from mapa.consultas import carregar_pontos, ponto_mais_proximo, trechos_perto, trechos_por_nome
from mapa.converter import converter_osmnx
from nucleo.dijkstra import caminho, comprimento_rota, dijkstra

RAIZ = Path(__file__).resolve().parent.parent
PASTA_GIFS = RAIZ / "gifs"
FATOR_LOTADO = 5
VELOCIDADE_M_POR_MIN = 250  # 15 km/h


def carregar_demo():
    return converter_osmnx(ox.load_graphml(ARQUIVO)), carregar_pontos(RAIZ / "dados" / "pontos_turisticos.json")


def trechos_dos_empecilhos(grafo, pontos):
    dam = pontos["praca_dam"]
    return {
        "empecilho1": ("Passagem do Museu Nacional lotada", trechos_por_nome(grafo, "Museumstraat")),
        "empecilho2": ("Praça Dam lotada", trechos_perto(grafo, dam["lat"], dam["lon"], 150)),
    }


def aplicar_lotacao(grafo, trechos, fator=FATOR_LOTADO):
    copia = grafo.copiar()
    for a, b in trechos:
        copia.alterar_custo(a, b, fator)
    return copia


def _titulo(nome, grafo, rota):
    metros = comprimento_rota(grafo, rota)
    minutos = f"{metros / VELOCIDADE_M_POR_MIN:.1f}".replace(".", ",")
    distancia = f"{metros:,.0f}".replace(",", ".")
    return f"{nome}\n{distancia} m · {minutos} min de bicicleta"


def gerar_gifs():
    grafo, pontos = carregar_demo()
    origem = ponto_mais_proximo(grafo, pontos["estacao_central"]["lat"], pontos["estacao_central"]["lon"])
    destino = ponto_mais_proximo(grafo, pontos["museu_van_gogh"]["lat"], pontos["museu_van_gogh"]["lon"])
    PASTA_GIFS.mkdir(exist_ok=True)

    _, anterior, passos = dijkstra(grafo, origem, destino)
    rota = caminho(anterior, destino)
    criar_animacao(grafo, passos, rota, _titulo("Estação Central → Museu Van Gogh", grafo, rota)).save(
        PASTA_GIFS / "rota.gif", writer=PillowWriter(fps=20),
    )
    print("Gerado: rota.gif")

    for arquivo, (nome, trechos) in trechos_dos_empecilhos(grafo, pontos).items():
        cenario = aplicar_lotacao(grafo, trechos)
        _, anterior, passos = dijkstra(cenario, origem, destino)
        nova = caminho(anterior, destino)
        criar_animacao(grafo, passos, nova, _titulo(nome, grafo, nova), rota_anterior=rota, empecilho=trechos).save(
            PASTA_GIFS / f"{arquivo}.gif", writer=PillowWriter(fps=20),
        )
        print(f"Gerado: {arquivo}.gif")


if __name__ == "__main__":
    gerar_gifs()
