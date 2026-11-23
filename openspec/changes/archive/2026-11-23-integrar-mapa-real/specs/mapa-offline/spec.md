## MODIFIED Requirements

### Requirement: Download do mapa de bicicleta

O sistema SHALL baixar a rede de bicicleta em um quadrado de 5 × 5 km centrado em latitude 52.3676 e longitude 4.8945, e MUST preservar a informação de contramão liberada para bicicletas. O mapa salvo MUST NOT conter trechos em que pedalar não é permitido, incluindo corredores de ônibus e ruas de pedestres sem permissão explícita para bicicleta.

#### Scenario: Primeiro download

- **WHEN** o download é executado e ainda não existe mapa salvo
- **THEN** o mapa é salvo em arquivo e o sistema informa a quantidade de cruzamentos e trechos

#### Scenario: Contramão liberada preservada

- **WHEN** o mapa salvo é carregado
- **THEN** os trechos marcados no OpenStreetMap como contramão liberada para bicicletas mantêm essa informação

#### Scenario: Via sem permissão

- **WHEN** uma rua de pedestres ou um corredor de ônibus não tem permissão para bicicleta
- **THEN** o trecho não entra no mapa salvo

#### Scenario: Via com permissão

- **WHEN** uma rua de pedestres ou um corredor de ônibus tem permissão explícita para bicicleta
- **THEN** o trecho permanece no mapa salvo
