## Purpose

Localizar no mapa os cruzamentos dos pontos turísticos e os trechos afetados por um empecilho.

## ADDED Requirements

### Requirement: Cruzamento mais próximo

O sistema SHALL encontrar o cruzamento mais próximo de uma coordenada usando a distância haversine.

#### Scenario: Ponto turístico

- **WHEN** a coordenada de um ponto turístico é consultada
- **THEN** o sistema devolve o cruzamento de menor distância

#### Scenario: Grafo sem coordenadas

- **WHEN** nenhum ponto do grafo tem coordenadas
- **THEN** a consulta é recusada com erro de valor

### Requirement: Trechos por nome

O sistema SHALL encontrar os trechos cujo nome contém um texto, sem diferenciar maiúsculas de minúsculas. Um texto vazio MUST ser recusado.

#### Scenario: Nome da via

- **WHEN** o nome de uma via é consultado
- **THEN** o sistema devolve os trechos dessa via nos sentidos existentes

#### Scenario: Texto vazio

- **WHEN** a consulta recebe um texto vazio
- **THEN** ela é recusada, para não selecionar o mapa inteiro

### Requirement: Trechos por proximidade

O sistema SHALL encontrar os trechos cujo ponto médio está dentro de um raio em metros.

#### Scenario: Região da Praça Dam

- **WHEN** a coordenada da Praça Dam é consultada com raio de 150 m
- **THEN** o sistema devolve somente os trechos com ponto médio dentro desse raio

### Requirement: Pontos turísticos

O projeto SHALL fornecer 10 pontos turísticos com identificador, nome, latitude e longitude, todos dentro da área do mapa e conectados entre si.

#### Scenario: Qualquer par de pontos

- **WHEN** a rota é calculada entre quaisquer dois pontos turísticos diferentes
- **THEN** existe um caminho
