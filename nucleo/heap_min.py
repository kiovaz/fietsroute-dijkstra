"""Fila de prioridade em heap binário, sem decrease-key.

FietsRoute: Ana Alice, Caio Vasconcelos e Yasmin Barata.
"""


class HeapMin:
    def __init__(self):
        self._itens = []  # (prioridade, ordem de inserção, item)
        self._contador = 0

    def vazio(self):
        return not self._itens

    def inserir(self, prioridade, item):
        self._itens.append((prioridade, self._contador, item))
        self._contador += 1
        self._subir(len(self._itens) - 1)

    def extrair_minimo(self):
        if not self._itens:
            raise IndexError("A fila de prioridade está vazia")
        topo = self._itens[0]
        ultimo = self._itens.pop()
        if self._itens:
            self._itens[0] = ultimo
            self._descer(0)
        return topo[0], topo[2]

    def _subir(self, i):
        h = self._itens
        while i > 0:
            pai = (i - 1) // 2
            if h[pai] < h[i]:
                return
            h[pai], h[i] = h[i], h[pai]
            i = pai

    def _descer(self, i):
        h = self._itens
        while True:
            menor = i
            for filho in (2 * i + 1, 2 * i + 2):
                if filho < len(h) and h[filho] < h[menor]:
                    menor = filho
            if menor == i:
                return
            h[i], h[menor] = h[menor], h[i]
            i = menor
