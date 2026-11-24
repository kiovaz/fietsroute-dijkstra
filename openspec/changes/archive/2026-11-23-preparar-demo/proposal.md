## Why

O núcleo, o mapa e as animações já funcionam separadamente, mas a apresentação precisa de um roteiro único, executável célula por célula. O projeto também precisa de instruções, referências e crédito dos dados para outra pessoa conseguir instalar e avaliar.

## What Changes

- Adicionar `demo.ipynb`, com o exemplo dos slides, a rota real, os dois empecilhos, a troca de origem e destino e as comparações.
- Exibir distância real, custo e tempo estimado, deixando claro que o tempo não considera a lotação.
- Medir o Dijkstra com e sem heap no mapa real.
- Adicionar `README.md`, com equipe, instalação, execução, uso de bibliotecas, referências e crédito do OpenStreetMap.

## Capabilities

### New Capabilities

- `demonstracao`: roteiro executável da apresentação e instruções do projeto.

### Modified Capabilities

Nenhuma.

## Impact

- Novos arquivos: `demo.ipynb` e `README.md`.
- Arquivos alterados: `mapa/desenhar.py` e `testes/test_visual.py`.
- O fundo do mapa interativo precisa de internet. Os GIFs funcionam sem ela.
