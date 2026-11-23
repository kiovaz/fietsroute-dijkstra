"""Testes do núcleo com os cenários do exemplo de 8 pontos.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
Execução, na raiz do projeto: python -m unittest discover -s testes -t .
"""
import random
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from nucleo.dijkstra import bfs, caminho, comprimento_rota, custo_rota, dijkstra, dijkstra_linear
from nucleo.grafo import Grafo, carregar_json
from nucleo.heap_min import HeapMin
from testes.referencia import dijkstra_networkx

RAIZ = Path(__file__).resolve().parent.parent
INF = float("inf")
EC, DAM, JOR, REM, LEI, MUS, PIJ, VON = (
    "Estação Central", "Praça Dam", "Jordaan", "Praça Rembrandt",
    "Praça Leidse", "Museu Nacional", "De Pijp", "Parque Vondel",
)


def exemplo():
    return carregar_json(RAIZ / "dados" / "exemplo_slides.json")


def rota(grafo, origem=EC, destino=VON):
    _, anterior, _ = dijkstra(grafo, origem, destino)
    return caminho(anterior, destino)


class TestCenarios(unittest.TestCase):
    def test_cenario_1_passo_a_passo(self):
        g = exemplo()
        dist, anterior, passos = dijkstra(g, EC, VON)
        self.assertEqual(caminho(anterior, VON), [EC, DAM, LEI, VON])
        self.assertEqual(dist[VON], 4000)
        self.assertEqual(
            [(p["fixado"], p["custo"]) for p in passos],
            [(EC, 0), (DAM, 1000), (JOR, 1750), (REM, 2500), (LEI, 3250), (PIJ, 3750), (VON, 4000)],
        )
        self.assertEqual(passos[0]["tentativas"], [(DAM, INF, 1000, True), (JOR, INF, 1750, True)])
        self.assertEqual(
            passos[1]["tentativas"],
            [(JOR, 1750, 2000, False), (REM, INF, 2500, True), (LEI, INF, 3250, True)],
        )
        self.assertEqual(passos[2]["tentativas"], [(LEI, 3250, 3750, False), (VON, INF, 4750, True)])
        self.assertEqual(passos[3]["tentativas"], [(MUS, INF, 4500, True), (PIJ, INF, 3750, True)])
        self.assertEqual(passos[4]["tentativas"], [(VON, 4750, 4000, True), (MUS, 4500, 4250, True)])
        self.assertEqual(passos[5]["tentativas"], [(MUS, 4250, 5000, False)])
        self.assertEqual(passos[6]["tentativas"], [])

    def test_cenario_2_bfs(self):
        g = exemplo()
        r = caminho(bfs(g, EC, VON), VON)
        self.assertEqual(r, [EC, JOR, VON])
        self.assertEqual(custo_rota(g, r), 4750)
        self.assertEqual(custo_rota(g, r) - custo_rota(g, rota(g)), 750)

    def test_cenario_3_ponte_fechada(self):
        g = exemplo()
        anterior_rota = rota(g)
        g.remover_trecho(DAM, LEI)
        r = rota(g)
        self.assertEqual(r, [EC, JOR, LEI, VON])
        self.assertEqual(custo_rota(g, r), 4500)
        self.assertEqual(custo_rota(g, anterior_rota), INF)

    def test_cenario_4_evento_no_parque(self):
        g = exemplo()
        g.remover_trecho(DAM, LEI)
        anterior_rota = rota(g)
        g.alterar_custo(LEI, VON, 3)
        r = rota(g)
        self.assertEqual(r, [EC, JOR, VON])
        self.assertEqual(custo_rota(g, r), 4750)
        self.assertEqual(custo_rota(g, anterior_rota), 6000)
        self.assertEqual(comprimento_rota(g, anterior_rota), 4500)

    def test_cenario_5_negativo_recusado(self):
        g = exemplo()
        with self.assertRaises(ValueError):
            g.alterar_custo(LEI, VON, -3)
        self.assertEqual(g.trecho(LEI, VON)["custo"], 750)
        with self.assertRaises(ValueError):
            g.adicionar_trecho(EC, VON, -3)
        self.assertEqual(rota(g), [EC, DAM, LEI, VON])

    def test_contraexemplo_negativo_barrado(self):
        g = Grafo(direcionado=True)
        g.adicionar_trecho("A", "B", 2)
        g.adicionar_trecho("A", "C", 3)
        with self.assertRaises(ValueError):
            g.adicionar_trecho("C", "B", -2)

    def test_contraexemplo_negativo_resultado_errado(self):
        g = Grafo(direcionado=True, permitir_negativo=True)
        for a, b, c in (("A", "B", 2), ("A", "C", 3), ("C", "B", -2), ("B", "D", 2)):
            g.adicionar_trecho(a, b, c)
        dist, _, _ = dijkstra(g, "A")
        self.assertEqual((dist["B"], dist["D"]), (2, 4))


class TestGrafo(unittest.TestCase):
    def test_exemplo_carregado(self):
        g = exemplo()
        self.assertEqual(len(g.pontos()), 8)
        self.assertEqual(len(g.trechos()), 13)
        self.assertIn("Estação Central", g.pontos())

    def test_trecho_repetido_fica_o_menor(self):
        g = Grafo(direcionado=True)
        g.adicionar_trecho("A", "B", 10, "longo")
        g.adicionar_trecho("A", "B", 4, "curto")
        g.adicionar_trecho("A", "B", 7, "médio")
        self.assertEqual(g.trecho("A", "B")["nome"], "curto")

    def test_direcionado_nao_cria_volta(self):
        g = Grafo(direcionado=True)
        g.adicionar_trecho("A", "B", 1)
        self.assertEqual(g.vizinhos("B"), [])

    def test_alterar_custo_nos_dois_sentidos_sem_mudar_comprimento(self):
        g = exemplo()
        g.alterar_custo(LEI, VON, 3)
        for a, b in ((LEI, VON), (VON, LEI)):
            self.assertEqual(g.trecho(a, b)["custo"], 2250)
            self.assertEqual(g.trecho(a, b)["comprimento"], 750)

    def test_remover_nos_dois_sentidos(self):
        g = exemplo()
        g.remover_trecho(DAM, LEI)
        self.assertNotIn(LEI, [v for v, _ in g.vizinhos(DAM)])
        self.assertNotIn(DAM, [v for v, _ in g.vizinhos(LEI)])

    def test_copia_independente(self):
        g = exemplo()
        c = g.copiar()
        c.remover_trecho(DAM, LEI)
        c.alterar_custo(LEI, VON, 3)
        self.assertEqual(g.trecho(DAM, LEI)["custo"], 2250)
        self.assertEqual(g.trecho(LEI, VON)["custo"], 750)

    def test_leitura_nao_altera_o_grafo(self):
        g = exemplo()
        g.trecho(LEI, VON)["custo"] = 1
        g.trechos()[0][2]["custo"] = 1
        self.assertEqual(g.trecho(LEI, VON)["custo"], 750)
        self.assertEqual(g.trecho(EC, DAM)["custo"], 1000)

    def test_valores_nao_finitos_recusados(self):
        g = exemplo()
        for valor in (float("nan"), INF):
            with self.assertRaises(ValueError):
                g.alterar_custo(LEI, VON, valor)
            with self.assertRaises(ValueError):
                g.adicionar_trecho(EC, VON, valor)

    def test_fator_zero_recusado(self):
        g = exemplo()
        with self.assertRaises(ValueError):
            g.alterar_custo(LEI, VON, 0)
        self.assertEqual(g.trecho(LEI, VON)["custo"], 750)
        self.assertEqual(g.trecho(VON, LEI)["custo"], 750)

    def test_coordenadas(self):
        g = Grafo(direcionado=True)
        g.adicionar_trecho("A", "B", 1)
        g.adicionar_ponto("A", 52.1, 4.9)
        self.assertEqual(g.coordenadas("A"), (52.1, 4.9))
        self.assertEqual(g.coordenadas("B"), (None, None))
        with self.assertRaises(KeyError):
            g.coordenadas("C")


class TestHeap(unittest.TestCase):
    def test_ordena(self):
        h = HeapMin()
        valores = random.Random(7).choices(range(50), k=300)
        for v in valores:
            h.inserir(v, v)
        saida = []
        while not h.vazio():
            saida.append(h.extrair_minimo()[0])
        self.assertEqual(saida, sorted(valores))

    def test_empate_por_ordem_de_insercao(self):
        h = HeapMin()
        for item in "abcde":
            h.inserir(1, item)
        self.assertEqual([h.extrair_minimo()[1] for _ in "abcde"], list("abcde"))

    def test_itens_nao_comparaveis(self):
        h = HeapMin()
        h.inserir(1, {"a": 1})
        h.inserir(1, {"b": 2})
        self.assertEqual(h.extrair_minimo()[1], {"a": 1})

    def test_vazia(self):
        with self.assertRaises(IndexError):
            HeapMin().extrair_minimo()


class TestDijkstra(unittest.TestCase):
    def test_inalcancavel(self):
        g = Grafo(direcionado=True)
        g.adicionar_trecho("A", "B", 1)
        g.adicionar_ponto("C")
        dist, anterior, _ = dijkstra(g, "A", "C")
        self.assertEqual(dist["C"], INF)
        self.assertNotIn("C", anterior)
        self.assertEqual(caminho(anterior, "C"), [])
        self.assertEqual(custo_rota(g, []), INF)
        self.assertEqual(comprimento_rota(g, []), INF)

    def test_origem_igual_ao_destino(self):
        g = exemplo()
        dist, anterior, passos = dijkstra(g, EC, EC)
        self.assertEqual(caminho(anterior, EC), [EC])
        self.assertEqual((dist[EC], custo_rota(g, [EC]), len(passos)), (0, 0, 1))

    def test_ponto_inexistente(self):
        g = exemplo()
        for funcao in (dijkstra, dijkstra_linear):
            for origem in ("X", None):
                with self.assertRaises(KeyError):
                    funcao(g, origem)
            with self.assertRaises(KeyError):
                funcao(g, EC, "X")
        with self.assertRaises(KeyError):
            bfs(g, "X", EC)

    def test_sem_destino_fixa_todos(self):
        dist, anterior, passos = dijkstra(exemplo(), EC)
        self.assertEqual(len(passos), 8)
        self.assertEqual(dist[MUS], 4250)
        self.assertIsNone(anterior[EC])

    def test_linear_igual_ao_heap(self):
        gerador = random.Random(42)
        for _ in range(150):
            n = gerador.randint(1, 25)
            g = Grafo(direcionado=gerador.random() < 0.5)
            for i in range(n):
                g.adicionar_ponto(i)
            for _ in range(gerador.randint(0, 4 * n)):
                g.adicionar_trecho(gerador.randrange(n), gerador.randrange(n), gerador.randint(0, 6))
            origem = gerador.randrange(n)
            destino = gerador.choice([None, gerador.randrange(n)])
            self.assertEqual(dijkstra(g, origem, destino), dijkstra_linear(g, origem, destino))

    def test_otimo_contra_forca_bruta(self):
        gerador = random.Random(11)
        for _ in range(80):
            n = gerador.randint(2, 7)
            g = Grafo(direcionado=True)
            for i in range(n):
                g.adicionar_ponto(i)
            for _ in range(gerador.randint(0, 3 * n)):
                g.adicionar_trecho(gerador.randrange(n), gerador.randrange(n), gerador.randint(0, 9))

            melhor = {i: INF for i in range(n)}

            def visitar(u, custo, vistos):
                melhor[u] = min(melhor[u], custo)
                for v, c in g.vizinhos(u):
                    if v not in vistos:
                        visitar(v, custo + c, vistos | {v})

            visitar(0, 0, {0})
            dist, anterior, _ = dijkstra(g, 0)
            self.assertEqual(dist, melhor)
            for v in anterior:
                self.assertEqual(custo_rota(g, caminho(anterior, v)), dist[v])


class TestBibliotecas(unittest.TestCase):
    def test_nucleo_nao_importa_bibliotecas_de_rota(self):
        proibidas = re.compile(r"^\s*(?:import|from)\s+(?:heapq|networkx|osmnx)\b", re.M)
        for arquivo in (RAIZ / "nucleo").glob("*.py"):
            self.assertIsNone(proibidas.search(arquivo.read_text(encoding="utf-8")), arquivo.name)

    def test_rota_nao_depende_do_networkx(self):
        g = exemplo()
        with patch.dict(sys.modules, {"networkx": None}):
            self.assertEqual(rota(g), [EC, DAM, LEI, VON])
            self.assertEqual(caminho(bfs(g, EC, VON), VON), [EC, JOR, VON])

    def test_referencia_no_exemplo(self):
        self.assertEqual(dijkstra_networkx(exemplo(), EC, VON), (4000, [EC, DAM, LEI, VON]))

    def test_referencia_inalcancavel_e_inexistente(self):
        g = Grafo(direcionado=True)
        g.adicionar_trecho("A", "B", 1)
        g.adicionar_ponto("C")
        self.assertEqual(dijkstra_networkx(g, "A", "C"), (INF, []))
        with self.assertRaises(KeyError):
            dijkstra_networkx(g, "A", "X")

    def test_nosso_dijkstra_igual_a_biblioteca(self):
        gerador = random.Random(23)
        for _ in range(200):
            n = gerador.randint(1, 30)
            g = Grafo(direcionado=gerador.random() < 0.5)
            for i in range(n):
                g.adicionar_ponto(i)
            for _ in range(gerador.randint(0, 4 * n)):
                g.adicionar_trecho(gerador.randrange(n), gerador.randrange(n), gerador.randint(0, 20))
            origem, destino = gerador.randrange(n), gerador.randrange(n)
            custo_lib, rota_lib = dijkstra_networkx(g, origem, destino)
            dist, anterior, _ = dijkstra(g, origem, destino)
            self.assertEqual(dist[destino], custo_lib)
            self.assertEqual(custo_rota(g, caminho(anterior, destino)), custo_lib)
            self.assertEqual(custo_rota(g, rota_lib), custo_lib)


if __name__ == "__main__":
    unittest.main()
