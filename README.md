# FietsRoute

Planejador de rotas de bicicleta em Amsterdã. Ele calcula o trajeto de menor custo com o algoritmo de Dijkstra e recalcula a rota quando uma ponte fecha ou um trecho fica lotado.

**Equipe:** Ana Alice, Caio Vasconcelos e Yasmin Barata

*Dados do mapa © colaboradores do OpenStreetMap, disponíveis sob a licença [ODbL](https://www.openstreetmap.org/copyright).*

## Problema e público-alvo

Ciclistas precisam da rota mais rápida, e ela muda quando uma ponte levadiça abre, uma rua entra em obra ou um evento lota um trecho. O FietsRoute recalcula o trajeto nessas situações.

O projeto é voltado para turistas que alugam bicicleta, entregadores, estudantes e trabalhadores que pedalam todo dia. Empresas de aluguel de bicicletas também podem oferecer o planejador no próprio aplicativo.

## Instalação

O projeto foi testado com **Python 3.14**. No Windows, mantenha a pasta em um caminho curto, como `C:\dev\fietsroute-dijkstra`, porque a instalação do Jupyter pode falhar em caminhos longos.

Windows (PowerShell):

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Linux ou macOS:

```bash
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Execução

Os comandos abaixo usam o formato do Windows e devem ser executados na raiz do projeto. No Linux ou macOS, troque `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

| Ação | Comando |
|---|---|
| Rodar os testes | `.\.venv\Scripts\python.exe -m unittest discover -s testes -t .` |
| Abrir a demonstração | `.\.venv\Scripts\python.exe -m jupyter notebook demo.ipynb` |
| Gerar os GIFs novamente | `.\.venv\Scripts\python.exe -m mapa.gerar_gifs` |
| Baixar o mapa novamente | Apague `dados/amsterdam_bike.graphml` e rode `.\.venv\Scripts\python.exe -m mapa.baixar_mapa` |

O mapa e os GIFs já estão no repositório. A internet só é necessária para o fundo do mapa interativo. Baixar o mapa novamente pode mudar as rotas, porque o OpenStreetMap é atualizado com frequência.

## Estrutura

```text
nucleo/    Grafo, HeapMin, Dijkstra, versão sem heap e BFS
mapa/      download, conversão, consultas, mapa interativo, animação e GIFs
dados/     exemplo dos slides, pontos turísticos e mapa real
gifs/      animações da rota e dos dois empecilhos
testes/    testes automáticos e validação com o NetworkX
demo.ipynb demonstração, com uma célula por momento
```

## Uso de bibliotecas

O algoritmo e a fila de prioridade são implementados pela equipe em `nucleo/`, que não importa nenhuma biblioteca de grafos ou de fila de prioridade.

| Biblioteca | Uso no projeto |
|---|---|
| OSMnx | Baixar, preparar, salvar e carregar o mapa |
| NetworkX | Estrutura entregue pelo OSMnx e validação do resultado em `testes/referencia.py` |
| folium | Mapa interativo com a rota calculada pela equipe |
| matplotlib e Pillow | Animação e geração dos GIFs |
| Jupyter Notebook | Demonstração |

O NetworkX não calcula nenhuma rota do sistema. Ele apenas confere se o custo encontrado pelo Dijkstra da equipe é o mesmo.

## Resultados no mapa real

Rota de Estação Central até Museu Van Gogh, em um mapa com 4.932 cruzamentos e 11.646 trechos:

| Cenário | Distância | Tempo estimado |
|---|---:|---:|
| Rota principal | 2.945 m | 11,8 min |
| Passagem do Museu Nacional lotada (custo × 5) | 2.994 m | 12,0 min |
| Praça Dam lotada (custo × 5) | 2.959 m | 11,8 min |

- Com heap, o cálculo levou cerca de 9 ms. Sem heap, levou de 600 a 850 ms.
- A rota com menos trechos (BFS) tem 40 trechos e 3.390 m. A do Dijkstra tem 51 trechos e 2.945 m.

## Limitações

- As permissões para bicicleta vêm das tags do OpenStreetMap e não substituem a sinalização local.
- O tempo usa a distância real e uma média de 15 km/h, sem considerar lotação. Um estudo da Fietsersbond registrou média de 14,9 km/h em Amsterdã (DUTCHNEWS, 2015).
- O protótipo não usa dados de trânsito em tempo real nem otimiza viagens com várias paradas.

## Referências

ACM. **Edsger W. Dijkstra**: A.M. Turing Award Laureate. Disponível em: https://amturing.acm.org/award_winners/dijkstra_1053701. Acesso em: 23 nov. 2026.

BOEING, G. OSMnx: new methods for acquiring, constructing, analyzing, and visualizing complex street networks. **Computers, Environment and Urban Systems**, v. 65, p. 126-139, 2017. DOI: https://doi.org/10.1016/j.compenvurbsys.2017.05.004.

CORMEN, T. H.; LEISERSON, C. E.; RIVEST, R. L.; STEIN, C. **Algoritmos**: teoria e prática. 3. ed. Rio de Janeiro: Elsevier, 2012. Capítulos de caminhos mínimos de fonte única e de heaps.

CWI. **E. W. Dijkstra**: brilliant, colourful and opinionated. Disponível em: https://www.cwi.nl/about/history/e-w-dijkstra-brilliant-colourful-and-opinionated. Acesso em: 23 nov. 2026.

DIJKSTRA, E. W. A note on two problems in connexion with graphs. **Numerische Mathematik**, v. 1, p. 269-271, 1959. DOI: https://doi.org/10.1007/BF01386390.

DUTCHNEWS. **Utrecht has the busiest Dutch cycle lanes, Amsterdam the slowest cyclists**. 3 nov. 2015. Disponível em: https://www.dutchnews.nl/2015/11/utrecht-has-the-busiest-dutch-cycle-lanes-amsterdam-the-slowest-cyclists/. Acesso em: 23 nov. 2026.

FRANA, P. L. An interview with Edsger W. Dijkstra. **Communications of the ACM**, v. 53, n. 8, p. 41-47, 2010. DOI: https://doi.org/10.1145/1787234.1787249.

MOY, J. **RFC 2328**: OSPF Version 2. IETF, 1998. Disponível em: https://www.rfc-editor.org/rfc/rfc2328. Acesso em: 23 nov. 2026.

OPENSTREETMAP. **Dados de mapa**. © colaboradores do OpenStreetMap, licença ODbL. Disponível em: https://www.openstreetmap.org/copyright. Acesso em: 23 nov. 2026.

OSMNX. **OSMnx documentation**. Disponível em: https://osmnx.readthedocs.io/. Acesso em: 23 nov. 2026.

SEDGEWICK, R.; WAYNE, K. **Algorithms**. 4. ed. [S. l.]: Addison-Wesley, 2011. Seção 4.4, Shortest Paths.
