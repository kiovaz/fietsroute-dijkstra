## Why

A demonstração precisa mostrar no mapa real como o Dijkstra se espalha, qual rota escolhe e como ela muda diante de um empecilho. As animações são geradas antes porque levam tempo e também servem de plano B da apresentação.

## What Changes

- Desenhar em um mapa interativo os pontos turísticos, a rota atual, a rota anterior e os trechos do empecilho.
- Animar a onda de cruzamentos fixados e, depois, a linha percorrendo a rota.
- Aproximar a imagem ao final das animações de empecilho, para que desvios curtos fiquem visíveis.
- Gerar os três GIFs da demonstração: rota, passagem do Museu Nacional lotada e Praça Dam lotada.

## Capabilities

### New Capabilities

- `visualizacao-rotas`: mapa interativo, animação do algoritmo e geração dos GIFs.

### Modified Capabilities

Nenhuma.

## Impact

- Novos arquivos: `mapa/desenhar.py`, `mapa/animar.py`, `mapa/gerar_gifs.py`, `testes/test_visual.py` e `gifs/`.
- Arquivo alterado: `mapa/consultas.py`.
- O fundo do mapa interativo precisa de internet. Os GIFs funcionam sem ela.
