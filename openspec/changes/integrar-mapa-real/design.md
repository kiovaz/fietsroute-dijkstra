## Context

O OSMnx junta segmentos consecutivos em um único trecho. Depois disso, um trecho pode misturar ruas com regras diferentes de bicicleta, então a permissão não pode ser avaliada com segurança no mapa simplificado.

## Goals / Non-Goals

**Goals:**

- Garantir que a rota use apenas vias permitidas segundo as tags do OpenStreetMap.
- Entregar o mapa real ao núcleo sem que o cálculo de rotas dependa do OSMnx.

**Non-Goals:**

- Desenhar a rota, animar ou montar o notebook.
- Interpretar restrições por horário, que ficam como não permitidas nas vias exclusivas.

## Decisions

- **Filtrar antes de simplificar.** Cada segmento é avaliado com suas próprias tags. Filtrar depois poderia aprovar um trecho formado por partes com regras diferentes.
- **Separar trechos quando `oneway:bicycle` muda.** Assim, a contramão só é criada quando vale para todo o trecho.
- **Corredor de ônibus e rua de pedestres exigem permissão explícita.** Nas demais vias, bicicleta é permitida salvo proibição.
- **Guardar a geometria em latitude e longitude.** É a mesma ordem das coordenadas do grafo e do folium, e a conversão acontece em um só lugar.

## Risks / Trade-offs

- [As tags podem estar incompletas ou desatualizadas] → O resultado é apresentado como baseado no OpenStreetMap, sem substituir a sinalização local.
- [O filtro pode isolar algum ponto turístico] → Um teste confere o caminho entre todos os pares.
- [A passagem do Museu Nacional pode sair da rota] → A rota e os dois empecilhos são conferidos no mapa novo.
