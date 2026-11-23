"""Baixa uma única vez o mapa de bicicleta do centro de Amsterdã.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
Dados do mapa © colaboradores do OpenStreetMap (licença ODbL).

Uso, na raiz do projeto: python -m mapa.baixar_mapa
"""
from pathlib import Path

import osmnx as ox

CENTRO = (52.3676, 4.8945)
DISTANCIA_M = 2500
ARQUIVO = Path(__file__).resolve().parent.parent / "dados" / "amsterdam_bike.graphml"


def baixar_mapa():
    if ARQUIVO.exists():
        print(f"Mapa já existe, nada foi baixado: {ARQUIVO}")
        return

    ox.settings.useful_tags_way = [*ox.settings.useful_tags_way, "oneway:bicycle"]
    G = ox.graph_from_point(CENTRO, dist=DISTANCIA_M, network_type="bike")

    ARQUIVO.parent.mkdir(exist_ok=True)
    # Grava à parte para uma falha não deixar um mapa incompleto no caminho final.
    parcial = ARQUIVO.with_suffix(".parcial.graphml")
    ox.save_graphml(G, parcial)
    parcial.replace(ARQUIVO)
    print(f"Mapa salvo: {G.number_of_nodes()} cruzamentos, {G.number_of_edges()} trechos")


if __name__ == "__main__":
    baixar_mapa()
