# conversao-mapa Specification

## Purpose
Copiar o mapa real para o grafo da equipe, para que todo o cálculo de rotas rode sobre a mesma estrutura usada no exemplo.

## Requirements

### Requirement: Cópia do mapa

A conversão SHALL gerar um grafo direcionado com as coordenadas dos cruzamentos e o comprimento, o nome e a geometria de cada trecho, com a geometria em latitude e longitude.

#### Scenario: Trecho com geometria

- **WHEN** um trecho do mapa tem geometria
- **THEN** o grafo guarda seus pontos em latitude e longitude, na ordem do percurso

#### Scenario: Trecho sem geometria

- **WHEN** um trecho do mapa não tem geometria
- **THEN** o grafo usa a reta entre os dois cruzamentos

#### Scenario: Trecho com vários nomes

- **WHEN** um trecho tem mais de um nome
- **THEN** os nomes são unidos por " / "

### Requirement: Contramão liberada

A conversão MUST criar o sentido contrário, com a geometria invertida, somente quando a contramão estiver liberada para bicicletas em todo o trecho.

#### Scenario: Contramão liberada

- **WHEN** o trecho tem o valor "no" para sentido único de bicicleta
- **THEN** o sentido contrário também existe

#### Scenario: Valores divergentes

- **WHEN** o trecho tem valores diferentes para sentido único de bicicleta
- **THEN** o sentido contrário não é criado

### Requirement: Trechos paralelos

Quando houver mais de um trecho entre os mesmos cruzamentos e no mesmo sentido, a conversão MUST manter o de menor comprimento.

#### Scenario: Ruas paralelas

- **WHEN** dois trechos ligam os mesmos cruzamentos no mesmo sentido
- **THEN** permanece o mais curto
