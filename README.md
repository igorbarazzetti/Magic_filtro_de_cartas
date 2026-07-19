# Magic MTG Finder — Landing page com busca + recomendação de cartas parecidas

Aplicação para pesquisar cartas de **Magic: The Gathering** (Scryfall), abrir detalhes e sugerir cartas similares com score e justificativas.

## O que foi implementado

- Busca textual e autocomplete.
- Render de carta com arte, mana, tipo, raridade e detalhes.
- Cartas de duas faces com rotação de face.
- Painel de **Mais parecidas** com ranking por similaridade e motivos.
- Backend minimalista em **Python + FastAPI** para centralizar as chamadas ao Scryfall e funcionar bem em produção.

## Estrutura do projeto

- `magic-mtg-landing.html`: frontend (HTML/CSS/JS) da aplicação.
- `backend/requirements.txt`: dependências Python.
- `backend/app/main.py`: proxy FastAPI para Scryfall + serve da landing page.
- `backend/app/__init__.py`: pacote Python.
- `render.yaml`: configuração de deploy automático no Render.

## Arquitetura

- O frontend local (arquivo `.html`) usa:
  - `https://api.scryfall.com` quando aberto como `file://` (desenvolvimento local simples).
  - `/api/scryfall/...` quando servido por HTTP (produção).
- O backend:
  - recebe `/api/scryfall/*`
  - repassa para a Scryfall
  - retorna a resposta sem mudar payload
  - serve também `magic-mtg-landing.html` na raiz.

## Como rodar localmente

### Opção 1 — só frontend (rápida)
1. Abra `magic-mtg-landing.html` diretamente no navegador.

### Opção 2 — com backend local (igual ao que vai para produção)
```bash
cd C:\Users\igor\OneDrive\Documentos\Magic_filtro_de_cartas
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

- Abra: `http://127.0.0.1:8000/magic-mtg-landing.html`
- Healthcheck: `http://127.0.0.1:8000/api/health`

## Como publicar no Render (sem ajustes de código)

1. Faça commit/push da pasta no GitHub.
2. No Render, conecte o repositório e escolha **New + Blueprint**.
3. O `render.yaml` já descreve tudo:
   - build: `pip install -r backend/requirements.txt`
   - start: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
   - healthcheck: `/api/health`
4. Após deploy, acesse a URL pública gerada.
5. Teste no navegador:
   - `https://<seu-app>.onrender.com/magic-mtg-landing.html`
   - `https://<seu-app>.onrender.com/api/health`
   - `https://<seu-app>.onrender.com/api/scryfall/cards/search?q=name:lightning%20bolt`

## Observações importantes

- O proxy permite manter a app funcionando no domínio oficial da Render com a mesma interface, sem alterar o restante do frontend.
- A lógica de similaridade permanece no frontend (HTML único).
- Limite atual de chamadas auxiliares de recomendação segue as constantes do JS no arquivo principal.

## Licença

Uso pessoal e educacional.
