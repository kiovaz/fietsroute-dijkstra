# demonstracao Specification

## Purpose
Oferecer um roteiro executável da apresentação e as instruções necessárias para instalar, rodar e avaliar o FietsRoute.

## Requirements

### Requirement: Roteiro da demonstração

O notebook SHALL executar, em ordem, o exemplo dos slides, o carregamento do mapa, a escolha dos pontos, a rota, os dois empecilhos, a troca de origem e destino e as comparações, sem erros.

#### Scenario: Execução completa

- **WHEN** todas as células são executadas do início ao fim
- **THEN** nenhuma célula termina com erro

#### Scenario: Custo negativo na demonstração

- **WHEN** a célula tenta aplicar o fator -3
- **THEN** a recusa aparece como mensagem, sem interromper o notebook

### Requirement: Escolha de origem e destino

O notebook SHALL permitir escolher origem e destino pelos nomes dos pontos turísticos. Um nome desconhecido MUST gerar uma mensagem com as opções válidas.

#### Scenario: Nome desconhecido

- **WHEN** um nome fora da lista é informado
- **THEN** a mensagem lista os pontos disponíveis

### Requirement: Alteração de custos

O notebook SHALL permitir alterar o custo de uma rua pelo nome e por um fator editável e recalcular a rota. Um fator inválido ou uma rua inexistente MUST gerar uma mensagem sem interromper o notebook.

#### Scenario: Fator muda a rota

- **WHEN** a célula aplica um fator a uma rua usada pela rota e o desvio fica mais barato
- **THEN** a tela mostra a nova rota e quanto a rota anterior custaria

#### Scenario: Entrada inválida

- **WHEN** a célula recebe um fator negativo ou uma rua inexistente
- **THEN** a recusa aparece como mensagem

### Requirement: Resultado exibido

O notebook SHALL exibir a distância real e o tempo estimado. Com empecilho, MUST exibir também o custo em metros equivalentes e informar que o tempo não considera a lotação.

#### Scenario: Rota com empecilho

- **WHEN** a rota é recalculada com um trecho lotado
- **THEN** a tela mostra distância, custo em metros equivalentes, tempo e quanto a rota anterior custaria

### Requirement: Comparações

O notebook SHALL comparar a rota do Dijkstra com a de menos trechos, medir as versões com e sem heap e validar o custo com a biblioteca de referência.

#### Scenario: Comparações no mapa real

- **WHEN** a célula de comparações é executada
- **THEN** a tela mostra os dois caminhos, os dois tempos e o resultado da validação

### Requirement: Instruções do projeto

O README SHALL informar equipe, problema, público-alvo, versão do Python, instalação, execução, testes, uso de bibliotecas, referências e o crédito "© colaboradores do OpenStreetMap".

#### Scenario: Nova instalação

- **WHEN** uma pessoa segue as instruções em um ambiente limpo
- **THEN** ela consegue instalar as dependências, rodar os testes e abrir a demonstração
