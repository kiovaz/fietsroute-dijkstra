# grafo-ruas Specification

## Purpose
Representar pontos e trechos de ruas, com distância real e custo separados, permitindo simular empecilhos sem alterar o mapa original.

## Requirements

### Requirement: Pontos e trechos

O grafo SHALL armazenar pontos com coordenadas opcionais e trechos com comprimento, custo, nome e geometria. O custo MUST começar igual ao comprimento. Em um grafo não direcionado, cada trecho MUST valer nos dois sentidos.

#### Scenario: Trecho não direcionado

- **WHEN** um trecho entre A e B é adicionado a um grafo não direcionado
- **THEN** B aparece como vizinho de A e A aparece como vizinho de B, com o mesmo custo

#### Scenario: Trecho repetido

- **WHEN** um trecho de A para B é adicionado mais de uma vez
- **THEN** permanece o trecho de menor comprimento

### Requirement: Recusa de valores inválidos

O grafo MUST recusar com erro de valor um comprimento negativo, exceto quando valores negativos forem explicitamente permitidos, e MUST recusar sempre fator negativo ou zero e valores não finitos.

#### Scenario: Comprimento negativo

- **WHEN** um trecho com comprimento -3 é adicionado a um grafo padrão
- **THEN** a operação é recusada com uma mensagem clara

#### Scenario: Fator negativo

- **WHEN** o custo de um trecho é multiplicado por -3
- **THEN** a operação é recusada e o custo permanece igual

#### Scenario: Fator zero

- **WHEN** o custo de um trecho é multiplicado por 0
- **THEN** a operação é recusada, porque o trecho ficaria gratuito e atrairia a rota

### Requirement: Empecilhos

O grafo SHALL permitir multiplicar o custo de um trecho e fechar um trecho. O comprimento real MUST NOT mudar. Em um grafo não direcionado, as duas operações MUST afetar os dois sentidos.

#### Scenario: Trecho lotado

- **WHEN** o custo de um trecho de 750 m é multiplicado por 3
- **THEN** o custo passa a 2.250 e o comprimento continua 750 m

#### Scenario: Ponte fechada

- **WHEN** um trecho não direcionado é fechado
- **THEN** ele deixa de existir nos dois sentidos

### Requirement: Cópia independente

O grafo SHALL produzir uma cópia cujas alterações não afetam o original.

#### Scenario: Empecilho na cópia

- **WHEN** um trecho é fechado ou tem o custo alterado em uma cópia
- **THEN** o grafo original permanece igual

### Requirement: Carregamento do exemplo

O sistema SHALL montar um grafo não direcionado a partir do arquivo do exemplo, em UTF-8, inserindo os trechos na ordem do arquivo.

#### Scenario: Exemplo dos slides

- **WHEN** o arquivo do exemplo é carregado
- **THEN** o grafo tem 8 pontos e 13 trechos, com os nomes acentuados preservados
