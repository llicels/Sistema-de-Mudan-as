# Sistema de Mudanças

Plataforma web para anúncio e gestão de pedidos de serviços de mudanças.

Clientes podem solicitar serviços (transporte, guindaste, embalagem, etc.) a empresas de mudanças cadastradas. Cada empresa define em quais cidades atua e o preço/hora de cada serviço. O sistema calcula automaticamente o preço de cada solicitação considerando acréscimos por carga excedente e bônus por altura de guindaste.

Projeto da disciplina ACH2025 — Banco de Dados 2, EACH-USP.

## Funcionalidades

- **Dashboard** com visão geral do sistema
- **CRUD** completo para: Empresas, Cidades, Clientes, Funcionários, Serviços, Oferecimentos e Pedidos
- **Relatórios** com histogramas e rankings (Chart.js)
- **Cálculo automático** de preços via triggers no PostgreSQL
- **Hierarquia de serviços** (supertipo `servicos` com subtipos `guindastes` e `transportes`)

## Stack

- **Backend:** Python (Flask) + psycopg2
- **Frontend:** HTML, CSS, Chart.js
- **Banco de dados:** PostgreSQL

## Pré-requisitos

- PostgreSQL instalado e rodando
- Python 3.10+
- `pip` e `venv`

### Instalação do PostgreSQL (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-client
sudo systemctl start postgresql
```

Após instalar, crie um usuário (se necessário):

```bash
sudo -u postgres createuser --superuser $USER
# ou use o usuário postgres padrão:
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"
```

## Como rodar

### 1. Configurar o banco de dados

> **Nota:** O script `setup.sh` detecta automaticamente se precisa usar `sudo -u postgres` para conectar (necessário quando o usuário do PostgreSQL difere do usuário do sistema).

```bash
cd aplicacao
chmod +x setup.sh
./setup.sh
```

O script cria o banco `mudancas`, executa o schema (DDL), os triggers e povoa com dados de teste.

É possível customizar as credenciais via variáveis de ambiente:

```bash
DB_NAME=mudancas DB_USER=postgres ./setup.sh
```

### 2. Instalar dependências e rodar a aplicação

```bash
cd aplicacao
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acessar em `http://localhost:5000`.

### Configuração do banco

As credenciais do PostgreSQL são lidas de `config.py`, que usa as variáveis de ambiente:

| Variável     | Padrão    |
|-------------|-----------|
| `DB_HOST`     | localhost |
| `DB_PORT`     | 5432      |
| `DB_NAME`     | mudancas  |
| `DB_USER`     | postgres  |
| `DB_PASSWORD` | postgres  |

## Estrutura do projeto

```
├── aplicacao/
│   ├── app.py                  # Aplicação Flask (rotas)
│   ├── config.py               # Configuração PostgreSQL
│   ├── db.py                   # Helpers de conexão
│   ├── schema.sql              # DDL — criação das tabelas
│   ├── triggers.sql            # Triggers (preços, hierarquia)
│   ├── seed.sql                # Dados de teste
│   ├── setup.sh                # Script de setup do banco
│   ├── requirements.txt
│   ├── models/                 # CRUDs por entidade
│   │   ├── empresas.py
│   │   ├── clientes.py
│   │   ├── cidades.py
│   │   ├── servicos.py
│   │   ├── oferecem.py
│   │   ├── funcionarios.py
│   │   └── pedidos.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/              # Jinja2 templates
│       ├── base.html           # Layout com sidebar
│       ├── index.html          # Dashboard
│       ├── 404.html
│       ├── cidades/
│       ├── clientes/
│       ├── empresas/
│       ├── funcionarios/
│       ├── oferecem/
│       ├── pedidos/
│       ├── servicos/
│       └── relatorios/
├── docs/
│   └── handover-conexao-itens-1-e-2.md
├── tirggers_full.sql           # Triggers (versão consolidada)
├── .gitignore
└── README.md
```

## Diagrama ER

O diagrama entidade-relacionamento do projeto está disponível em `SolucaoMudancasEP1EP22026.pdf`.
