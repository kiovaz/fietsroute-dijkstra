## Context

A demonstração tem cerca de 3 minutos e meio e não pode depender de esperas longas. O Dijkstra leva poucos milissegundos no mapa real, enquanto as animações já ficam prontas em GIF.

## Goals / Non-Goals

**Goals:**

- Ter uma célula por momento da apresentação.
- Manter o algoritmo fora do notebook, que apenas chama o código da equipe.

**Non-Goals:**

- Criar slides, gravar a tela ou compactar a entrega final.

## Decisions

- **Versionar o notebook sem saídas.** Evita um arquivo grande e garante que os resultados exibidos venham da execução atual.
- **Recalcular ao vivo e exibir GIFs prontos.** O cálculo real aparece na hora, sem esperar a geração da animação.
- **Usar a velocidade de 15 km/h.** Um estudo da Fietsersbond mediu média de 14,9 km/h em Amsterdã, e o valor arredondado facilita a conta.
- **Funções auxiliares só de exibição no notebook.** Formatar a saída não faz parte do núcleo.

## Risks / Trade-offs

- [Sem internet, o fundo do folium não carrega] → Os GIFs e a gravação de tela ficam como plano B.
- [O tempo medido varia entre computadores] → A apresentação usa a proporção entre as versões, medida na própria máquina.
