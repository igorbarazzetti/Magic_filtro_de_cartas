# Magic MTG Finder (local)

Uma landing page single-file para buscar cartas de *Magic: The Gathering* na API do Scryfall, visualizar detalhes e obter recomendações de cartas parecidas com foco em mecânica principal e semântica de texto.

## Visão geral

`magic-mtg-landing.html` é uma aplicação em HTML/CSS/JavaScript puro (sem backend), com:

- Busca textual de cartas por nome, cor, tipo ou texto
- Autocomplete com sugestões em tempo real
- Lista de resultados com imagem, nome, custo, tipo e raridade
- Visualização de detalhes da carta selecionada
- Rotação de faces em cartas duais
- Painel de **mais parecidas** com score, barra de similaridade e explicação por carta

## O que já foi implementado

### Busca e autocomplete

- Campo de busca ligado à rota `/cards/search` da Scryfall
- Debounce na digitação para reduzir requisições
- Sugestões em `datalist` e dropdown customizado
- Tratamento de erro sem quebrar a interface

### Render de cartas e interação

- Grid de resultados responsivo
- Cartas clicáveis para abrir detalhes
- Cartas com duas faces: botão para alternar a face no card e no painel de detalhes
- Render de símbolo de mana por cor com fallback textual

### Motor de similaridade

- Construção de perfil de carta (`CardProfile`) com:
  - Tipo principal, supertipos e subtipos
  - Identidade de cor e vetor de mana
  - CMC
  - Poder/resistência/loyalty
  - Raridade
  - Keywords e mecânicas principais
  - Sinais de fase
  - Assinaturas semânticas de texto e intenção

- Coleta de candidatos em estágios:
  1. Tipo + cor + CMC (janela estreita)
  2. + mecânicas principais
  3. + fallback de janelas de CMC mais amplas
  4. Estágio de segurança para preencher o mínimo de sugestões

- Rankeamento com pesos por componente e prioridade de mecânica principal
- Dedupe por `oracle_id`
- Corte progressivo por threshold para manter retorno estável
- Motivos automáticos de similaridade para cada carta sugerida
- Mensagem de fallback quando o estágio estrito não produz volume suficiente
- Proteção contra falha de API, mantendo o painel ativo e sem crash

### Robustez e performance

- Cache de consultas e de perfis em memória com TTL
- Limite de chamadas por carta controlado por constantes
- Perfil de falha explícito quando não houver dados suficientes

## Estrutura

- `magic-mtg-landing.html`: aplicação completa (HTML + CSS + JS)
- `README.md`: este arquivo de documentação

## Como executar

1. Copie ou clone o repositório
2. Abra `magic-mtg-landing.html` diretamente no navegador
3. Se preferir, rode um servidor local:

```bash
cd Magic_filtro_de_cartas
python -m http.server 5173
```

Acesse: `http://localhost:5173/magic-mtg-landing.html`

## Configurações importantes

- `SIMILAR_LIMIT`: quantidade máxima de similares exibidos
- `SIMILARITY_MIN_SCORE`: limiar principal
- `SIMILARITY_RELAXED_SCORE`: limiar usado em fallback
- `MAX_CANDIDATE_FETCH_QUERIES`: limite de buscas extras para recomendação
- `SIMILAR_CANDIDATE_FETCH_LIMIT`: máximo de cartas retornadas por consulta
- TTLs de cache para otimizar chamadas repetidas

## Limitações atuais

- Depende da disponibilidade e de rate limit da Scryfall
- A qualidade semântica ainda é heurística e pode ter ruído em textos muito atípicos
- Não há persistência de favoritos, histórico persistente ou autenticação

## Próximos passos sugeridos

- Adicionar filtros de UI (tipo, cor, faixa de custo, raridade)
- Salvar estado/favoritos no `localStorage`
- Aprimorar normalização semântica de textos com sinais causais mais profundos
- Exportar listas de similares para plano de teste/deck
- Adicionar testes funcionais no frontend (Playwright)

## Licença

Uso livre para estudo e prototipagem pessoal.
