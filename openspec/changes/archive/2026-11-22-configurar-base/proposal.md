## Why

O FietsRoute depende de um ambiente Python reproduzível e do mapa real de Amsterdã. Baixar o mapa logo no início revela cedo se os trechos planejados para os empecilhos da demonstração existem nos dados, e deixa a apresentação independente do OpenStreetMap.

## What Changes

- Definir as dependências do projeto com versões fixadas.
- Adicionar o download único do mapa de bicicleta do centro de Amsterdã (quadrado de 5 × 5 km), preservando a informação de contramão liberada para bicicletas.
- Salvar o mapa em arquivo local, sem sobrescrever um mapa já baixado.
- Manter ambiente virtual, cache e arquivos temporários fora do versionamento.
- Verificar se os pontos da demonstração e a passagem do Museu Nacional aparecem no mapa.

## Capabilities

### New Capabilities

- `mapa-offline`: obtenção única do mapa real e seu uso posterior sem internet, em um ambiente com dependências fixadas.

### Modified Capabilities

Nenhuma.

## Impact

- Novos arquivos: `.gitignore`, `requirements.txt`, `mapa/__init__.py`, `mapa/baixar_mapa.py` e `dados/amsterdam_bike.graphml`.
- Novas dependências: OSMnx, matplotlib, folium, Pillow e Jupyter Notebook.
- Sistema externo: OpenStreetMap, acessado apenas durante o download.
