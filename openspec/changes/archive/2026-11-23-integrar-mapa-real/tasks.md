## 1. Dados

- [x] 1.1 Adicionar a regra de permissão em `mapa/baixar_mapa.py` e verificar com testes de vias permitidas e proibidas
- [x] 1.2 Baixar o mapa novamente e verificar que ele carrega sem corredores de ônibus sem permissão
- [x] 1.3 Criar `dados/pontos_turisticos.json` e verificar os 10 pontos dentro da área do mapa

## 2. Conversão e consultas

- [x] 2.1 Implementar `mapa/converter.py` e verificar geometria, nomes, contramão e trechos paralelos
- [x] 2.2 Implementar `mapa/consultas.py` e verificar cruzamento mais próximo, busca por nome e por raio

## 3. Viabilidade da demonstração

- [x] 3.1 Verificar que todos os pares de pontos têm caminho e que o custo é igual ao do NetworkX no mapa real
- [x] 3.2 Verificar que a rota principal passa pela passagem do Museu Nacional e pela região da Praça Dam
- [x] 3.3 Verificar que os dois empecilhos mudam a rota
