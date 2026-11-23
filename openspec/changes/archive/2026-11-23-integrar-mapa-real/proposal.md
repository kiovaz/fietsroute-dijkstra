## Why

O mapa baixado inclui corredores de ônibus e ruas de pedestres sem permissão para bicicleta, e a rota principal passava por esses trechos. O núcleo também precisa receber o mapa real na mesma estrutura de grafo usada pelo exemplo.

## What Changes

- Baixar novamente o mapa com as regras de bicicleta e retirar os trechos em que pedalar não é permitido.
- Converter o mapa para o grafo da equipe, com coordenadas, nomes, geometria e contramão liberada para bicicletas.
- Adicionar os 10 pontos turísticos, com a Estação Central na frente da estação.
- Adicionar consultas para ligar um ponto ao cruzamento mais próximo e escolher os trechos de um empecilho.

## Capabilities

### New Capabilities

- `conversao-mapa`: cópia do mapa real para o grafo da equipe.
- `consultas-mapa`: localização de cruzamentos e de trechos por nome ou por proximidade.

### Modified Capabilities

- `mapa-offline`: o download passa a retirar trechos em que pedalar não é permitido.

## Impact

- Novos arquivos: `mapa/converter.py`, `mapa/consultas.py`, `dados/pontos_turisticos.json` e `testes/test_mapa.py`.
- Arquivos alterados: `mapa/baixar_mapa.py` e `dados/amsterdam_bike.graphml`.
- Sistema externo: OpenStreetMap, acessado apenas no novo download.
