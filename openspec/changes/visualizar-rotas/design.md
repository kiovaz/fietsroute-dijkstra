## Context

A rota principal fixa cerca de 2.500 cruzamentos. O desvio do empecilho 1 troca menos de 350 m, o que fica pouco visível em um mapa de 5 × 5 km.

## Goals / Non-Goals

**Goals:**

- Ter animações leves, geradas uma vez e exibidas sem internet.
- Deixar evidente onde a rota mudou.

**Non-Goals:**

- Montar o notebook, que fica na próxima parte.
- Gerar animação ao vivo durante a apresentação.

## Decisions

- **Só GIFs, com `PillowWriter`.** Não exige ffmpeg e elimina espera ou falha ao vivo.
- **Zoom automático no trecho alterado.** Mantém o empecilho planejado e torna o desvio legível sem configurar uma área para cada cenário.
- **Desenhar sempre com o grafo original.** A geometria não muda, e um trecho fechado continua disponível para aparecer como rota anterior.
- **`Figure` sem `pyplot`.** Evita depender da janela gráfica e impede que o notebook exiba uma figura duplicada.
- **Linha da rota em `consultas.py`.** O folium e o matplotlib usam a mesma função, sem que um dependa do outro.

## Risks / Trade-offs

- [Os GIFs podem ficar grandes] → Resolução baixa e quantidade limitada de quadros.
- [O fundo do folium depende de internet] → Os GIFs continuam como plano B.
