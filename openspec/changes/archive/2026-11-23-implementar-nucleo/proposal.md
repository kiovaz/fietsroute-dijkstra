## Why

O FietsRoute precisa calcular a rota de menor custo com código próprio da equipe, e a implementação é o critério de maior peso da avaliação. O núcleo vem antes do mapa real para ser conferido em um exemplo pequeno, com resultados conhecidos.

## What Changes

- Adicionar um grafo em lista de adjacência, com distância real e custo separados, fechamento de trechos, alteração de custo e cópia independente.
- Adicionar uma fila de prioridade própria, sem bibliotecas.
- Adicionar o Dijkstra com registro do passo a passo, a versão sem heap para medição, a BFS de comparação e o cálculo de custo e distância de uma rota.
- Adicionar uma comparação com o Dijkstra do NetworkX, usada apenas para validar o resultado da equipe.
- Adicionar o exemplo de 8 pontos e 13 trechos e os testes automáticos dos 5 cenários e do contraexemplo de peso negativo.

## Capabilities

### New Capabilities

- `grafo-ruas`: representação de pontos e trechos, com empecilhos e recusa de custos negativos.
- `rota-menor-custo`: cálculo e reconstrução da rota de menor custo, passo a passo e comparação com a rota de menos trechos.

### Modified Capabilities

Nenhuma.

## Impact

- Novos arquivos: `nucleo/`, `testes/` e `dados/exemplo_slides.json`.
- O cálculo de rotas usa apenas Python e código da equipe. O NetworkX, fixado em `requirements.txt`, entra só em `testes/referencia.py`, para validar o resultado.
