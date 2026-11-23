## 1. Grafo

- [x] 1.1 Implementar `nucleo/grafo.py` e verificar com os testes de trechos, validação, empecilhos e cópia
- [x] 1.2 Criar `dados/exemplo_slides.json` e verificar o carregamento com 8 pontos e 13 trechos

## 2. Rotas

- [x] 2.1 Implementar `nucleo/heap_min.py` e verificar ordem, empate e fila vazia
- [x] 2.2 Implementar `dijkstra`, `caminho`, `custo_rota` e `comprimento_rota` e verificar o passo a passo do exemplo
- [x] 2.3 Implementar `dijkstra_linear` e verificar que o resultado é igual ao do heap em grafos aleatórios
- [x] 2.4 Implementar `bfs` e verificar o cenário 2

## 3. Validação

- [x] 3.1 Cobrir os cenários 1 a 5 e o contraexemplo negativo e verificar com `python -m unittest discover -s testes -t .`
- [x] 3.2 Verificar por teste que `nucleo/` não importa `heapq`, NetworkX nem OSMnx e que as rotas funcionam sem o NetworkX
- [x] 3.3 Implementar `dijkstra_networkx` em `testes/referencia.py` e verificar custo igual ao da equipe em grafos aleatórios
