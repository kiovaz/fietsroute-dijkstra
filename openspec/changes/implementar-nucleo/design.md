## Context

O núcleo não pode usar `heapq`, NetworkX ou OSMnx. O mapa real chega na próxima parte e deve preencher a mesma estrutura de grafo usada pelo exemplo.

## Goals / Non-Goals

**Goals:**

- Ter um núcleo pequeno, explicável em sala e coberto pelos cenários do exemplo.

**Non-Goals:**

- Converter o mapa real, desenhar rotas ou medir tempo.

## Decisions

- **Lista de adjacência com dicionários.** Mantém a ordem de inserção dos vizinhos, necessária para o desempate, e localiza um trecho em tempo constante.
- **Heap sem decrease-key.** Um ponto pode entrar mais de uma vez e a entrada antiga é ignorada ao sair. É mais simples que manter posições no heap.
- **Contador de inserção no heap.** Garante o desempate pela ordem de entrada e evita comparar os próprios itens.
- **Relaxamento compartilhado.** `dijkstra` e `dijkstra_linear` diferem só na escolha do próximo ponto, então não têm como divergir na regra principal.
- **Referência do NetworkX em `testes/`.** Mantém `nucleo/` só com código da equipe e ainda pode ser importada pelo notebook para mostrar a validação. A comparação usa o custo, porque rotas diferentes podem empatar.
- **Rota com trecho fechado custa infinito.** Permite comparar antes e depois de um empecilho sem tratar exceção no notebook.
- **`trechos()` devolve cada trecho não direcionado uma vez.** O exemplo é apresentado com 13 trechos, não 26.

## Risks / Trade-offs

- [Um grafo não direcionado compartilha a geometria nos dois sentidos] → Apenas o mapa real tem geometria, e ele é direcionado.
- [Fator 0 tornaria um trecho gratuito] → É recusado. Para bloquear um trecho, o fechamento é a operação correta.
