# visualizacao-rotas Specification

## Purpose
Mostrar no mapa real a rota calculada, o funcionamento do algoritmo e o efeito de um empecilho, com material pronto para a demonstração.

## Requirements

### Requirement: Mapa interativo da rota

O sistema SHALL desenhar em um mapa interativo os pontos turísticos, a origem, o destino e a rota pela geometria real das ruas. Uma rota vazia MUST ser recusada.

#### Scenario: Rota desenhada

- **WHEN** uma rota com geometria é desenhada
- **THEN** a linha segue os pontos da geometria em latitude e longitude

#### Scenario: Antes e depois

- **WHEN** uma rota anterior e os trechos de um empecilho são informados
- **THEN** o mapa mostra os dois de forma distinta da rota atual

#### Scenario: Rota vazia

- **WHEN** não existe rota para desenhar
- **THEN** a operação é recusada com erro de valor

### Requirement: Animação do algoritmo

A animação SHALL mostrar os cruzamentos sendo fixados na ordem do algoritmo e, depois, a linha percorrendo a rota. A onda MUST usar no máximo 120 quadros, independentemente do tamanho do mapa.

#### Scenario: Mapa grande

- **WHEN** a rota fixa milhares de cruzamentos
- **THEN** a onda continua limitada a 120 quadros

### Requirement: Destaque do desvio

Em uma animação com rota anterior, o sistema SHALL terminar aproximando a imagem da parte da rota que mudou.

#### Scenario: Desvio curto

- **WHEN** a rota muda em apenas um pequeno trecho
- **THEN** o quadro final enquadra esse trecho

#### Scenario: Rota sem empecilho

- **WHEN** não há rota anterior
- **THEN** a animação termina mostrando o mapa inteiro

### Requirement: GIFs da demonstração

O sistema SHALL gerar três GIFs, para a rota principal e para cada empecilho, sem depender de ffmpeg e sem alterar o mapa original.

#### Scenario: Geração antes da apresentação

- **WHEN** a geração é executada
- **THEN** os três arquivos ficam disponíveis e podem ser exibidos sem internet
