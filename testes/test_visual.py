"""Testes do mapa interativo, da animação e dos cenários dos GIFs.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""
import tempfile
import unittest
from pathlib import Path

from matplotlib.animation import PillowWriter
from PIL import Image

from mapa.animar import QUADROS_FIM, QUADROS_ONDA, QUADROS_ROTA, QUADROS_ZOOM, _limites_do_desvio, criar_animacao
from mapa.consultas import linha_da_rota
from mapa.desenhar import desenhar_pontos, desenhar_rota
from mapa.gerar_gifs import aplicar_lotacao
from nucleo.dijkstra import caminho, dijkstra
from nucleo.grafo import Grafo


def grafo():
    g = Grafo(direcionado=True)
    g.adicionar_ponto("A", 52.00, 4.00)
    g.adicionar_ponto("B", 52.01, 4.01)
    g.adicionar_ponto("C", 52.02, 4.02)
    g.adicionar_ponto("D", 52.01, 4.03)
    g.adicionar_trecho("A", "B", 10, "ab", [(52.00, 4.00), (52.005, 4.002), (52.01, 4.01)])
    g.adicionar_trecho("B", "C", 10, "bc", [(52.01, 4.01), (52.02, 4.02)])
    g.adicionar_trecho("A", "D", 15, "ad")
    g.adicionar_trecho("D", "C", 15, "dc")
    return g


class TestLinha(unittest.TestCase):
    def test_emenda_sem_ponto_repetido(self):
        self.assertEqual(
            linha_da_rota(grafo(), ["A", "B", "C"]),
            [(52.00, 4.00), (52.005, 4.002), (52.01, 4.01), (52.02, 4.02)],
        )

    def test_sem_geometria_usa_reta(self):
        self.assertEqual(linha_da_rota(grafo(), ["A", "D"]), [(52.00, 4.00), (52.01, 4.03)])

    def test_rotas_curtas(self):
        self.assertEqual(linha_da_rota(grafo(), []), [])
        self.assertEqual(linha_da_rota(grafo(), ["A"]), [(52.00, 4.00)])


class TestDesenho(unittest.TestCase):
    def test_rota_e_empecilho_no_html(self):
        pontos = [{"nome": "Praça Teste", "lat": 52.0, "lon": 4.0}]
        html = desenhar_rota(grafo(), ["A", "B", "C"], pontos, ["A", "D", "C"], [("B", "C")]).get_root().render()
        for texto in ("52.005, 4.002", "Praça Teste", "Rota anterior", "Empecilho", "OpenStreetMap"):
            self.assertIn(texto, html)

    def test_rota_vazia(self):
        with self.assertRaises(ValueError):
            desenhar_rota(grafo(), [])

    def test_pontos_com_origem_e_destino(self):
        a, b = {"nome": "Ponto A", "lat": 52.0, "lon": 4.0}, {"nome": "Ponto B", "lat": 52.1, "lon": 4.1}
        html = desenhar_pontos({"a": a, "b": b}.values(), a, b).get_root().render()
        self.assertIn("Origem: Ponto A", html)
        self.assertIn("Destino: Ponto B", html)


class TestAnimacao(unittest.TestCase):
    def test_onda_limitada_em_mapa_grande(self):
        passos = [{"fixado": "A", "custo": 0, "tentativas": []}] * 2482
        animacao = criar_animacao(grafo(), passos, ["A", "B"], "t")
        total = len(list(animacao.new_frame_seq()))
        self.assertLessEqual(total, QUADROS_ONDA + QUADROS_ROTA + QUADROS_FIM)
        animacao._draw_was_started = True  # evita o aviso de animação criada e não renderizada

    def test_zoom_so_com_rota_anterior_diferente(self):
        g = grafo()
        self.assertIsNone(_limites_do_desvio(g, ["A", "B"], None))
        self.assertIsNone(_limites_do_desvio(g, ["A", "B"], ["A", "B"]))
        x, y = _limites_do_desvio(g, ["A", "B", "C"], ["A", "D", "C"])
        self.assertTrue(x[0] < 4.00 and x[1] > 4.03 and y[0] < 52.00 and y[1] > 52.02)

    def test_gera_gif_com_zoom(self):
        g = grafo()
        _, anterior, passos = dijkstra(g, "A", "C")
        rota = caminho(anterior, "C")
        animacao = criar_animacao(g, passos, rota, "t", rota_anterior=["A", "D", "C"], empecilho=[("A", "D")])
        self.assertEqual(
            len(list(animacao.new_frame_seq())),
            len(passos) + QUADROS_ROTA + QUADROS_ZOOM + QUADROS_FIM,
        )
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "t.gif"
            animacao.save(arquivo, writer=PillowWriter(fps=20))
            with Image.open(arquivo) as gif:
                self.assertGreater(gif.n_frames, 10)

    def test_rota_vazia(self):
        with self.assertRaises(ValueError):
            criar_animacao(grafo(), [], [], "t")


class TestCenarios(unittest.TestCase):
    def test_lotacao_nao_altera_o_original(self):
        g = grafo()
        c = aplicar_lotacao(g, [("A", "B")])
        self.assertEqual(c.trecho("A", "B")["custo"], 50)
        self.assertEqual(g.trecho("A", "B")["custo"], 10)


if __name__ == "__main__":
    unittest.main()
