# Mudanças até o Fim do Mundo

Plataforma de anúncios e pedidos de serviços de mudanças.

Projeto da disciplina ACH2025 — Banco de Dados 2, EACH-USP.

## Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, Chart.js
- **Banco:** PostgreSQL (a ser integrado — atualmente mock data)

## Como rodar

```bash
cd aplicacao
pip install -r requirements.txt
python app.py
```

Acessar em `http://localhost:5000`.

## Estrutura do projeto

```
├── aplicacao/
│   ├── app.py                  # Aplicação Flask (mock data + rotas)
│   ├── requirements.txt
│   ├── static/css/style.css    # Tema Backrooms
│   └── templates/              # Jinja2 templates
│       ├── base.html           # Layout com sidebar
│       ├── index.html          # Dashboard
│       ├── clientes/           # CRUD Clientes
│       ├── cidades/            # CRUD Cidades
│       ├── empresas/           # CRUD Empresas
│       ├── funcionarios/       # CRUD Funcionários
│       ├── pedidos/            # CRUD Pedidos
│       ├── servicos/           # CRUD Serviços
│       └── relatorios/         # Histogramas + Rankings
├── docs/
│   └── handover-conexao-itens-1-e-2.md  # Migração mock → PostgreSQL
├── .gitignore
└── README.md
```

## Itens do trabalho

| Item | Descrição | Status |
|------|-----------|--------|
| 1 | DDL SQL com tabelas e restrições | Pendente |
| 2 | Constraints (triggers, hierarquia, preços) | Pendente |
| 3 | Aplicação Flask (CRUD + relatórios) | ✅ Implementado |

## Handover

Para conectar a aplicação ao banco de dados (itens 1 e 2), consulte:
[`docs/handover-conexao-itens-1-e-2.md`](docs/handover-conexao-itens-1-e-2.md)

---
