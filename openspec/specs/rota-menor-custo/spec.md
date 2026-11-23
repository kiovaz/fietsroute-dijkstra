# rota-menor-custo Specification

## Purpose
Calcular a rota de menor custo entre dois pontos com código próprio, registrar o passo a passo e comparar o resultado com a rota de menos trechos.

## Requirements

### Requirement: Fila de prioridade

A fila SHALL devolver sempre o item de menor prioridade. Em empate, MUST sair primeiro o item inserido primeiro. Extrair de uma fila vazia MUST gerar erro de índice.

#### Scenario: Empate de prioridade

- **WHEN** dois itens com a mesma prioridade são inseridos
- **THEN** eles saem na ordem de inserção

### Requirement: Rota de menor custo

O sistema SHALL calcular o menor custo a partir da origem e reconstruir a rota. Um ponto fixado MUST NOT ser reaberto. Com destino informado, o cálculo MUST parar logo depois de fixá-lo. Origem ou destino inexistentes MUST gerar erro de chave.

#### Scenario: Rota do exemplo

- **WHEN** a rota de Estação Central a Parque Vondel é calculada no exemplo
- **THEN** a rota é Estação Central, Praça Dam, Praça Leidse e Parque Vondel, com custo 4.000

#### Scenario: Destino inalcançável

- **WHEN** não existe caminho até o destino
- **THEN** o custo dele é infinito e a rota é vazia

### Requirement: Registro do passo a passo

O cálculo SHALL registrar, para cada ponto fixado, seu custo e todas as tentativas de relaxamento, inclusive as que não melhoram.

#### Scenario: Momento-chave do exemplo

- **WHEN** Praça Leidse é fixada com custo 3.250
- **THEN** o registro mostra Parque Vondel passando de 4.750 para 4.000 e Museu Nacional de 4.500 para 4.250

### Requirement: Versão sem heap

O sistema SHALL oferecer uma versão com busca linear do mínimo, com a mesma entrada, saída e regra de desempate.

#### Scenario: Mesmo resultado

- **WHEN** as duas versões rodam sobre o mesmo grafo
- **THEN** devolvem as mesmas distâncias, rotas e passos

### Requirement: Comparação com menos trechos

O sistema SHALL calcular a rota com menos trechos, ignorando os custos.

#### Scenario: Menos trechos não é mais barato

- **WHEN** a rota com menos trechos é calculada no exemplo
- **THEN** a rota é Estação Central, Jordaan e Parque Vondel, com custo 4.750

### Requirement: Validação com biblioteca de referência

O sistema SHALL permitir comparar o custo calculado pela equipe com o de um Dijkstra de biblioteca. O cálculo das rotas MUST NOT depender dessa biblioteca.

#### Scenario: Mesmo custo da referência

- **WHEN** as duas implementações calculam a rota entre os mesmos pontos
- **THEN** o custo mínimo é igual

#### Scenario: Biblioteca indisponível

- **WHEN** a biblioteca de referência não está disponível
- **THEN** o cálculo de rotas da equipe continua funcionando

### Requirement: Custo e distância de uma rota

O sistema SHALL somar o custo e o comprimento real de uma rota. Uma rota vazia ou que use um trecho fechado MUST resultar em infinito.

#### Scenario: Rota anterior após fechamento

- **WHEN** a rota original é avaliada depois que uma de suas pontes foi fechada
- **THEN** o resultado é infinito

### Requirement: Cenários de empecilho

Os resultados MUST permanecer corretos depois de fechar trechos ou alterar custos.

#### Scenario: Ponte fechada

- **WHEN** o trecho Praça Dam – Praça Leidse é fechado
- **THEN** a rota passa por Jordaan e Praça Leidse, com custo 4.500

#### Scenario: Evento na entrada do parque

- **WHEN** a ponte continua fechada e o custo de Praça Leidse – Parque Vondel é multiplicado por 3
- **THEN** a rota é Estação Central, Jordaan e Parque Vondel, com custo 4.750, e a rota anterior custaria 6.000

#### Scenario: Contraexemplo de peso negativo

- **WHEN** o cálculo roda em A→B 2, A→C 3, C→B -2 e B→D 2, com negativos permitidos
- **THEN** o resultado errado B = 2 e D = 4 é reproduzido, mostrando por que valores negativos são recusados
