## Context

O repositório começa vazio. A máquina de desenvolvimento tem Python 3.14, acessado pelo comando `py`, e o OSMnx 2.2 exige Python 3.12 ou mais novo.

## Goals / Non-Goals

**Goals:**

- Deixar o ambiente pronto para as próximas partes.
- Ter o mapa real salvo e conferido antes de escrever o conversor.

**Non-Goals:**

- Implementar grafo, Dijkstra, conversor, desenho ou notebook.
- Escolher os fatores de custo dos empecilhos.

## Decisions

- **Usar Python 3.14.** Já está instalado e resolve todas as dependências sem conflito.
- **Manter o projeto na raiz do repositório.** Evita uma pasta `fietsroute/` repetida e encurta os comandos.
- **Compartilhar o relaxamento entre `dijkstra` e `dijkstra_linear` (próximas partes).** A regra fica em um só lugar e as duas versões não divergem.
- **Exibir a animação só por GIFs gerados antes (próximas partes).** Remove a geração ao vivo e o risco de espera na apresentação.
- **Usar `venv` e `pip`.** São as ferramentas padrão do Python e correspondem à instalação documentada para a equipe. Um gerenciador adicional exigiria que todos o instalassem.
- **Fixar só as dependências diretas.** Um `pip freeze` completo incluiria pacotes específicos do Windows e poderia falhar em outro computador.
- **Tornar `mapa/` um pacote e executar com `python -m mapa.baixar_mapa`.** Assim, os módulos de `mapa/` poderão importar `nucleo/` nas próximas partes.
- **Resolver o caminho do arquivo a partir do próprio módulo.** O resultado não depende da pasta em que o comando é executado.
- **Salvar em arquivo parcial e renomear ao final.** Uma falha na gravação não deixa um mapa corrompido no caminho final.

## Risks / Trade-offs

- [A passagem do Museu Nacional pode não estar na rede de bicicleta] → Conferido: ela aparece como a ciclovia `Museumstraat`, com 188 m nos dois sentidos. Ainda falta confirmar, na Parte 2, que a rota calculada passa por ela.
- [Os dados do OpenStreetMap mudam com o tempo] → O mapa salvo não é sobrescrito, mantendo os resultados da demonstração estáveis.
- [O arquivo `.graphml` depende da versão do OSMnx] → A versão fica fixada em `requirements.txt`.
