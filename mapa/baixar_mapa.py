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

TAGS_CICLOVIA = ("cycleway", "cycleway:left", "cycleway:right", "cycleway:both")
TAGS_BICICLETA = ("oneway:bicycle", "bicycle", "vehicle", *TAGS_CICLOVIA)
BICICLETA_LIBERADA = {"yes", "designated", "permissive"}
BICICLETA_PROIBIDA = {"no", "private", "dismount", "use_sidepath"}
VIAS_EXCLUSIVAS = {"busway", "pedestrian"}


def pode_pedalar(trecho):
    if trecho.get("oneway:bicycle") == "yes" and trecho.get("reversed") is True:
        return False
    bicicleta = trecho.get("bicycle")
    if bicicleta in BICICLETA_LIBERADA:
        return True
    if bicicleta in BICICLETA_PROIBIDA or trecho.get("access") in ("no", "private") or trecho.get("vehicle") in ("no", "private"):
        return False
    if trecho.get("highway") in VIAS_EXCLUSIVAS:
        return any(trecho.get(tag) not in (None, "no", "none", "separate") for tag in TAGS_CICLOVIA)
    return True


def baixar_mapa():
    if ARQUIVO.exists():
        print(f"Mapa já existe, nada foi baixado: {ARQUIVO}")
        return

    ox.settings.useful_tags_way = [*ox.settings.useful_tags_way, *TAGS_BICICLETA]
    G = ox.graph_from_point(CENTRO, dist=DISTANCIA_M, network_type="bike", simplify=False)
    # Filtra antes de simplificar: depois, ruas com regras diferentes viram um único trecho.
    G.remove_edges_from([(u, v, k) for u, v, k, d in G.edges(keys=True, data=True) if not pode_pedalar(d)])
    G = ox.truncate.largest_component(G)
    G = ox.simplify_graph(G, edge_attrs_differ=["oneway:bicycle"])

    ARQUIVO.parent.mkdir(exist_ok=True)
    # Grava à parte para uma falha não deixar um mapa incompleto no caminho final.
    parcial = ARQUIVO.with_suffix(".parcial.graphml")
    ox.save_graphml(G, parcial)
    parcial.replace(ARQUIVO)
    print(f"Mapa salvo: {G.number_of_nodes()} cruzamentos, {G.number_of_edges()} trechos")


if __name__ == "__main__":
    baixar_mapa()
