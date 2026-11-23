"""Animação da onda de cruzamentos fixados e da linha percorrendo a rota.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
Dados do mapa © colaboradores do OpenStreetMap (licença ODbL).
"""
import math

from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from mapa.consultas import geometria_trecho, linha_da_rota

QUADROS_ONDA = 120
QUADROS_ROTA = 30
QUADROS_ZOOM = 20
QUADROS_FIM = 12
COR_RUA, COR_ONDA, COR_ROTA, COR_ANTERIOR, COR_EMPECILHO = "#d9d9d9", "#6baed6", "#0b3d91", "#555555", "#d62728"
TAMANHO = (5.6, 6)
AREA = (0.01, 0.01, 0.98, 0.90)
PROPORCAO = TAMANHO[0] * AREA[2] / (TAMANHO[1] * AREA[3])


def _xy(pontos):
    return [(lon, lat) for lat, lon in pontos]


def _enquadrar(lats, lons, escala, folga=0):
    """Calcula limites que mantêm a proporção real do mapa na área do desenho."""
    cos_lat = math.cos(math.radians(sum(lats) / len(lats)))
    meia_lat = max(max(lats) - min(lats), (max(lons) - min(lons)) * cos_lat / PROPORCAO) / 2 * escala + folga
    meia_lon = meia_lat * PROPORCAO / cos_lat
    centro_lon, centro_lat = (min(lons) + max(lons)) / 2, (min(lats) + max(lats)) / 2
    return (centro_lon - meia_lon, centro_lon + meia_lon), (centro_lat - meia_lat, centro_lat + meia_lat)


def _limites_do_desvio(grafo, rota, rota_anterior):
    if not rota_anterior:
        return None
    mudou = set(zip(rota, rota[1:])) ^ set(zip(rota_anterior, rota_anterior[1:]))
    if not mudou:
        return None
    pontos = [p for a, b in mudou for p in geometria_trecho(grafo, a, b)]
    return _enquadrar([p[0] for p in pontos], [p[1] for p in pontos], escala=1.4, folga=0.0008)


def criar_animacao(grafo, passos, rota, titulo, rota_anterior=None, empecilho=()):
    """Use o grafo original: ele mantém a geometria dos trechos fechados."""
    linha = _xy(linha_da_rota(grafo, rota))
    if not linha:
        raise ValueError("Não há rota para animar")

    fig = Figure(figsize=TAMANHO, dpi=80)
    FigureCanvasAgg(fig)
    fig.suptitle(titulo, fontsize=10, y=0.985)
    ax = fig.add_axes(AREA)
    ax.set_xticks([])
    ax.set_yticks([])

    coords = [c for c in map(grafo.coordenadas, grafo.pontos()) if c[0] is not None]
    limite_x, limite_y = _enquadrar([c[0] for c in coords], [c[1] for c in coords], escala=1.02)
    ax.set_xlim(limite_x)
    ax.set_ylim(limite_y)

    ruas = [_xy(geometria_trecho(grafo, a, b)) for a, b, _ in grafo.trechos()]
    ax.add_collection(LineCollection(ruas, colors=COR_RUA, linewidths=0.35, zorder=1), autolim=False)
    fixados = ax.scatter([], [], s=4, c=COR_ONDA, alpha=0.65, linewidths=0, zorder=2)
    legenda = [
        Line2D([], [], marker="o", ls="", color=COR_ONDA, label="Cruzamentos fixados"),
        Line2D([], [], color=COR_ROTA, lw=2.4, label="Rota de menor custo"),
    ]
    if empecilho:
        trechos = [_xy(geometria_trecho(grafo, a, b)) for a, b in empecilho]
        ax.add_collection(LineCollection(trechos, colors=COR_EMPECILHO, linewidths=3, zorder=3), autolim=False)
        legenda.append(Line2D([], [], color=COR_EMPECILHO, lw=3, label="Empecilho"))
    if rota_anterior:
        ax.plot(*zip(*_xy(linha_da_rota(grafo, rota_anterior))), "--", color=COR_ANTERIOR, lw=1.8, zorder=4)
        legenda.append(Line2D([], [], color=COR_ANTERIOR, ls="--", lw=1.8, label="Rota anterior"))
    tracado, = ax.plot([], [], color=COR_ROTA, lw=2.4, solid_capstyle="round", zorder=5)
    ax.plot(*linha[0], "o", ms=8, mfc="white", mec="black", zorder=6)
    ax.plot(*linha[-1], "s", ms=8, mfc="black", mec="white", zorder=6)
    ax.legend(handles=legenda, loc="lower right", fontsize=7, framealpha=0.9)
    rotulo = ax.text(
        0.02, 0.98, "", transform=ax.transAxes, va="top", fontsize=8, zorder=7,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85},
    )

    pontos_onda = _xy(grafo.coordenadas(p["fixado"]) for p in passos)
    por_quadro = max(1, math.ceil(len(pontos_onda) / QUADROS_ONDA))
    quadros_onda = max(1, math.ceil(len(pontos_onda) / por_quadro))
    desvio = _limites_do_desvio(grafo, rota, rota_anterior)
    total = quadros_onda + QUADROS_ROTA + (QUADROS_ZOOM if desvio else 0) + QUADROS_FIM
    xs, ys = zip(*linha)

    def atualizar(quadro):
        n = min((quadro + 1) * por_quadro, len(pontos_onda))
        if n:
            fixados.set_offsets(pontos_onda[:n])
        rotulo.set_text(f"{n} cruzamentos fixados")

        andou = min(quadro - quadros_onda + 1, QUADROS_ROTA)
        if andou > 0:
            ponta = math.ceil(andou / QUADROS_ROTA * len(xs))
            tracado.set_data(xs[:ponta], ys[:ponta])

        aproximou = quadro - quadros_onda - QUADROS_ROTA + 1
        if desvio and aproximou > 0:
            t = min(aproximou / QUADROS_ZOOM, 1)
            ax.set_xlim(*(a + (b - a) * t for a, b in zip(limite_x, desvio[0])))
            ax.set_ylim(*(a + (b - a) * t for a, b in zip(limite_y, desvio[1])))
        return ()

    return FuncAnimation(fig, atualizar, frames=total, interval=50, blit=False, repeat=False)
