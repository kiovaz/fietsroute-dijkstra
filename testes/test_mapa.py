"""Testes da regra de bicicleta, do conversor, das consultas e do mapa real.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
import json
import unittest
from pathlib import Path

import networkx as nx
import osmnx as ox
from shapely.geometry import LineString

from mapa.baixar_mapa import ARQUIVO, pode_pedalar
from mapa.consultas import haversine, ponto_mais_proximo, trechos_perto, trechos_por_nome
from mapa.converter import converter_osmnx
from nucleo.dijkstra import caminho, custo_rota, dijkstra
from nucleo.grafo import Grafo
from testes.referencia import dijkstra_networkx

PONTOS = json.loads((Path(__file__).resolve().parent.parent / "dados" / "pontos_turisticos.json").read_text(encoding="utf-8"))


class TestPodePedalar(unittest.TestCase):
    def test_vias_permitidas(self):
        for trecho in (
            {"highway": "residential"},
            {"highway": "cycleway"},
            {"highway": "pedestrian", "bicycle": "yes"},
            {"highway": "busway", "bicycle": "designated"},
            {"highway": "busway", "cycleway:right": "lane"},
            {"highway": "residential", "access": "no", "bicycle": "yes"},
        ):
            self.assertTrue(pode_pedalar(trecho), trecho)

    def test_vias_proibidas(self):
        for trecho in (
            {"highway": "pedestrian"},
            {"highway": "busway"},
            {"highway": "busway", "cycleway": "separate"},
            {"highway": "residential", "bicycle": "dismount"},
            {"highway": "tertiary", "bicycle": "use_sidepath"},
            {"highway": "residential", "access": "no"},
            {"highway": "residential", "vehicle": "private"},
            {"highway": "residential", "oneway:bicycle": "yes", "reversed": True},
        ):
            self.assertFalse(pode_pedalar(trecho), trecho)

    def test_sentido_permitido_de_via_unica_para_bicicleta(self):
        self.assertTrue(pode_pedalar({"highway": "residential", "oneway:bicycle": "yes", "reversed": False}))


class TestConverter(unittest.TestCase):
    def mapa(self):
        G = nx.MultiDiGraph()
        G.add_node(1, y=52.0, x=4.0)
        G.add_node(2, y=52.1, x=4.1)
        G.add_node(3, y=52.2, x=4.2)
        return G

    def test_geometria_nome_e_contramao(self):
        G = self.mapa()
        linha = LineString([(4.0, 52.0), (4.05, 52.06), (4.1, 52.1)])
        G.add_edge(1, 2, length=100.0, name=["A", "B"], geometry=linha, **{"oneway:bicycle": "no"})
        g = converter_osmnx(G)
        ida = g.trecho(1, 2)
        self.assertEqual(ida["nome"], "A / B")
        self.assertEqual(ida["geometria"], [(52.0, 4.0), (52.06, 4.05), (52.1, 4.1)])
        self.assertEqual(g.trecho(2, 1)["geometria"], ida["geometria"][::-1])
        self.assertEqual(g.coordenadas(1), (52.0, 4.0))

    def test_sem_geometria_e_sem_nome(self):
        G = self.mapa()
        G.add_edge(1, 2, length=50.0)
        g = converter_osmnx(G)
        self.assertEqual(g.trecho(1, 2)["geometria"], [(52.0, 4.0), (52.1, 4.1)])
        self.assertEqual(g.trecho(1, 2)["nome"], "sem nome")
        self.assertEqual(g.vizinhos(2), [])

    def test_contramao_em_lista(self):
        G = self.mapa()
        G.add_edge(1, 2, length=10.0, **{"oneway:bicycle": ["no", "no"]})
        G.add_edge(2, 3, length=10.0, **{"oneway:bicycle": ["yes", "no"]})
        g = converter_osmnx(G)
        self.assertIn(1, [v for v, _ in g.vizinhos(2)])
        self.assertEqual(g.vizinhos(3), [])

    def test_paralelas_fica_a_mais_curta(self):
        G = self.mapa()
        G.add_edge(1, 2, length=30.0, name="longa")
        G.add_edge(1, 2, length=20.0, name="curta")
        self.assertEqual(converter_osmnx(G).trecho(1, 2)["nome"], "curta")


class TestConsultas(unittest.TestCase):
    def grafo(self):
        g = Grafo(direcionado=True)
        g.adicionar_ponto("A", 52.0, 4.0)
        g.adicionar_ponto("B", 52.001, 4.0)
        g.adicionar_ponto("C", 52.01, 4.0)
        g.adicionar_trecho("A", "B", 111, "Museumstraat")
        g.adicionar_trecho("B", "C", 1000, "Outra Rua")
        return g

    def test_haversine(self):
        self.assertAlmostEqual(haversine(0, 0, 0, 1), 111195.08, places=1)
        self.assertEqual(haversine(52, 4, 52, 4), 0)

    def test_ponto_mais_proximo(self):
        self.assertEqual(ponto_mais_proximo(self.grafo(), 52.0012, 4.0), "B")

    def test_grafo_sem_coordenadas(self):
        g = Grafo(direcionado=True)
        g.adicionar_ponto("A")
        with self.assertRaises(ValueError):
            ponto_mais_proximo(g, 52, 4)

    def test_por_nome(self):
        self.assertEqual(trechos_por_nome(self.grafo(), "museumSTRAAT"), [("A", "B")])
        with self.assertRaises(ValueError):
            trechos_por_nome(self.grafo(), "  ")

    def test_por_raio_usa_ponto_medio(self):
        self.assertEqual(trechos_perto(self.grafo(), 52.0005, 4.0, 20), [("A", "B")])
        self.assertEqual(trechos_perto(self.grafo(), 52.02, 4.0, 20), [])


class TestMapaReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.G = ox.load_graphml(ARQUIVO)
        cls.grafo = converter_osmnx(cls.G)
        cls.nos = {p["id"]: ponto_mais_proximo(cls.grafo, p["lat"], p["lon"]) for p in PONTOS}

    def test_pontos_turisticos(self):
        self.assertEqual(len(PONTOS), 10)
        self.assertEqual(len({p["id"] for p in PONTOS}), 10)
        lats = [d["y"] for _, d in self.G.nodes(data=True)]
        lons = [d["x"] for _, d in self.G.nodes(data=True)]
        for p in PONTOS:
            self.assertTrue(min(lats) <= p["lat"] <= max(lats) and min(lons) <= p["lon"] <= max(lons), p["id"])

    def test_todos_os_pares_tem_caminho(self):
        for no in self.nos.values():
            dist, _, _ = dijkstra(self.grafo, no)
            for outro in self.nos.values():
                self.assertLess(dist[outro], float("inf"))

    def test_rota_principal_igual_a_biblioteca(self):
        origem, destino = self.nos["estacao_central"], self.nos["museu_van_gogh"]
        dist, anterior, _ = dijkstra(self.grafo, origem, destino)
        custo_lib, _ = dijkstra_networkx(self.grafo, origem, destino)
        self.assertAlmostEqual(dist[destino], custo_lib, places=6)
        self.assertAlmostEqual(custo_rota(self.grafo, caminho(anterior, destino)), custo_lib, places=6)


if __name__ == "__main__":
    unittest.main()
