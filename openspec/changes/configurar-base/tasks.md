## 1. Ambiente

- [x] 1.1 Criar `.gitignore` e verificar com `git status` que `.venv/`, `cache/` e temporários não aparecem
- [x] 1.2 Criar `.venv`, instalar as dependências diretas e verificar com `pip check`
- [x] 1.3 Fixar as versões em `requirements.txt` e verificar a instalação a partir dele em um ambiente limpo

## 2. Mapa

- [x] 2.1 Criar `mapa/__init__.py` e `mapa/baixar_mapa.py` e verificar que o módulo importa sem iniciar o download
- [x] 2.2 Executar `python -m mapa.baixar_mapa` e verificar que o arquivo carrega com cruzamentos e trechos
- [x] 2.3 Executar o download novamente e verificar que o hash do arquivo não muda

## 3. Viabilidade da demonstração

- [x] 3.1 Verificar que os 10 pontos turísticos estão dentro da área do mapa
- [x] 3.2 Verificar se o mapa contém trechos da passagem do Museu Nacional e da Praça Dam, com contramão liberada preservada
