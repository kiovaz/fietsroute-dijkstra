# mapa-offline Specification

## Purpose
Garantir que o mapa real de bicicleta de Amsterdã seja obtido uma única vez e fique disponível para o projeto sem depender de internet.

## Requirements

### Requirement: Ambiente reproduzível

O projeto SHALL declarar suas dependências diretas com versões exatas e MUST ser instalável em Python 3.14.

#### Scenario: Instalação em ambiente limpo

- **WHEN** as dependências declaradas são instaladas em um ambiente virtual novo
- **THEN** a instalação termina sem conflitos entre pacotes

### Requirement: Download do mapa de bicicleta

O sistema SHALL baixar a rede de bicicleta em um quadrado de 5 × 5 km centrado em latitude 52.3676 e longitude 4.8945, e MUST preservar a informação de contramão liberada para bicicletas.

#### Scenario: Primeiro download

- **WHEN** o download é executado e ainda não existe mapa salvo
- **THEN** o mapa é salvo em arquivo e o sistema informa a quantidade de cruzamentos e trechos

#### Scenario: Contramão liberada preservada

- **WHEN** o mapa salvo é carregado
- **THEN** os trechos marcados no OpenStreetMap como contramão liberada para bicicletas mantêm essa informação

### Requirement: Preservação do mapa salvo

O sistema MUST NOT sobrescrever um mapa existente nem deixar um arquivo incompleto no lugar do mapa final.

#### Scenario: Mapa já baixado

- **WHEN** o download é executado e o mapa já existe
- **THEN** o arquivo permanece idêntico e nenhum download é feito

#### Scenario: Falha durante o download

- **WHEN** o download falha antes de terminar
- **THEN** nenhum arquivo é criado no caminho do mapa final

### Requirement: Uso sem internet

O mapa salvo SHALL poder ser carregado sem acesso à rede.

#### Scenario: Carregamento local

- **WHEN** o mapa salvo é carregado
- **THEN** seus cruzamentos e trechos ficam disponíveis sem nenhuma requisição externa

### Requirement: Arquivos locais fora do versionamento

Ambiente virtual, cache de download e arquivos temporários MUST NOT aparecer como arquivos a versionar.

#### Scenario: Conferência do repositório

- **WHEN** o estado do repositório é consultado depois da instalação e do download
- **THEN** esses arquivos locais não aparecem como pendentes
