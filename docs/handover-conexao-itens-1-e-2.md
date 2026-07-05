# Handover: Conexão Aplicação Flask com Itens 1 e 2

## Para: agente opencode (futura sessão de desenvolvimento)

## Contexto

Este repositório contém o sistema **"Mudanças até o Fim do Mundo"**, uma plataforma de anúncios e pedidos de serviços de mudanças. O projeto é um trabalho acadêmico da disciplina ACH 2025 — Banco de Dados 2 (EACH-USP, 1º semestre 2026).

O repositório atualmente possui a seguinte estrutura:

```
/root/Sistema-de-Mudan-as/
├── .opencode/                 # Configuração de agentes opencode
├── static/css/                # Estilos (vazio)
├── templates/
│   ├── cidades/               # (vazio)
│   ├── clientes/              # (vazio)
│   ├── empresas/              # (vazio)
│   ├── funcionarios/          # (vazio)
│   ├── pedidos/               # (vazio)
│   ├── relatorios/            # (vazio)
│   └── servicos/              # (vazio)
├── requirements.txt           # Apenas Flask==3.1.0
├── ProblemaMudanzasParte22026.doc
├── SolucaoMudancasEP1EP22026.pdf
└── docs/
    └── handover-conexao-itens-1-e-2.md   # ← Este documento
```

**Não há ainda `app.py` nem scripts SQL.** Os itens 1 (DDL) e 2 (Constraints/Triggers) foram resolvidos conceitualmente no PDF de solução, mas o código SQL e a aplicação Flask precisam ser implementados.

Este handover documenta o **contrato de dados** entre o schema SQL esperado e a aplicação Flask, o fluxo de migração do mock data para PostgreSQL, o impacto das constraints do item 2, as queries SQL dos relatórios e um checklist de migração.

---

## 1. Contrato de Dados (Mock → Schema SQL Esperado)

### Tabelas e suas estruturas esperadas

Abaixo, cada tabela do modelo relacional com suas colunas, tipos, chaves primárias (PK), chaves estrangeiras (FK), e como os dados mockados se relacionam com a futura aplicação Flask.

---

#### `cidade`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `nome_cidade` | `VARCHAR(100)` | PK (parte 1) |
| `estado` | `VARCHAR(2)` | PK (parte 2) |

- **PK composta**: `PRIMARY KEY (nome_cidade, estado)`
- **Mock na aplicação**: Lista de cidades disponíveis para oferta de serviços. No Flask, será um CRUD simples com formulário de nome+estado. A combo de cidade nos pedidos usará esta tabela como lookup.

---

#### `empresa`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `nome` | `VARCHAR(100)` | PK |
| `endereco` | `TEXT` | NOT NULL |

- **PK**: `PRIMARY KEY (nome)`
- **Mock na aplicação**: Lista de empresas cadastradas. No Flask, o CRUD de empresas insere aqui. O nome é unique identifier (chave natural).

---

#### `empresa_telefone`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `nome_empresa` | `VARCHAR(100)` | FK → `empresa(nome)` |
| `telefone` | `VARCHAR(20)` | |

- **FK**: `FOREIGN KEY (nome_empresa) REFERENCES empresa(nome) ON DELETE CASCADE`
- **Mock na aplicação**: Telefones são multivalorados. No formulário de cadastro/edição de empresas, deve haver um campo dinâmico para adicionar múltiplos telefones. Ao salvar, deleta-se os antigos e inserem-se os novos.

---

#### `cliente`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `codigo` | `INTEGER` | PK (auto-incremento) |
| `cpf` | `VARCHAR(14)` | UNIQUE, NOT NULL |
| `rg` | `VARCHAR(20)` | |
| `endereco` | `TEXT` | |
| `nome_completo` | `VARCHAR(200)` | NOT NULL |

- **PK**: `PRIMARY KEY (codigo)` — usar `SERIAL` ou `IDENTITY` para auto-incremento
- **Mock na aplicação**: CRUD de clientes. O campo `codigo` deve ser gerado automaticamente pelo banco (SERIAL). CPF deve ser validado (11 dígitos, formatado ou não).

---

#### `cliente_telefone`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `codigo_cliente` | `INTEGER` | FK → `cliente(codigo)` |
| `telefone` | `VARCHAR(20)` | |

- **FK**: `FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo) ON DELETE CASCADE`
- **Mock na aplicação**: Mesmo padrão de `empresa_telefone` — campo dinâmico no formulário do cliente.

---

#### `funcionario`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `cpf` | `VARCHAR(14)` | PK |
| `rg` | `VARCHAR(20)` | |
| `endereco` | `TEXT` | |
| `nome_completo` | `VARCHAR(200)` | NOT NULL |
| `tipo` | `VARCHAR(50)` | (motorista, guincho, gerente, etc.) |
| `salario` | `DECIMAL(10,2)` | |

- **PK**: `PRIMARY KEY (cpf)` — chave natural
- **Mock na aplicação**: CRUD de funcionários. Tipo é uma string livre ou enum. Salário armazenado com 2 casas decimais.

---

#### `funcionario_empresa`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `cpf_funcionario` | `VARCHAR(14)` | FK → `funcionario(cpf)` |
| `nome_empresa` | `VARCHAR(100)` | FK → `empresa(nome)` |

- **FK1**: `FOREIGN KEY (cpf_funcionario) REFERENCES funcionario(cpf) ON DELETE CASCADE`
- **FK2**: `FOREIGN KEY (nome_empresa) REFERENCES empresa(nome) ON DELETE CASCADE`
- **PK**: `PRIMARY KEY (cpf_funcionario, nome_empresa)`
- **Mock na aplicação**: Um funcionário pode trabalhar em múltiplas empresas. No cadastro/edição do funcionário, deve ser possível selecionar as empresas onde ele trabalha (checkboxes ou select múltiplo).

---

#### `servico` (supertipo)

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `nome_servico` | `VARCHAR(100)` | PK |

- **PK**: `PRIMARY KEY (nome_servico)`
- **Mock na aplicação**: Tabela supertipo da hierarquia de serviços. Todo serviço (transporte, guindaste, ou serviço simples como embalagem/montagem) tem um nome cadastrado aqui primeiro.
- **Constraint disjuntiva**: Um serviço deve ser de **apenas um** subtipo (Transporte **ou** Guindaste **ou** serviço simples sem subtipo). Isso será garantido por triggers/constraints do item 2.

---

#### `servico_transporte`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `nome_servico` | `VARCHAR(100)` | PK, FK → `servico(nome_servico)` |

- **PK/FK**: `PRIMARY KEY (nome_servico), FOREIGN KEY (nome_servico) REFERENCES servico(nome_servico) ON DELETE CASCADE`
- **Mock na aplicação**: Subtipo da hierarquia. Se o usuário marcar "Transporte" ao cadastrar um serviço, um registro é inserido aqui. Não tem colunas próprias além do nome — os detalhes estão em `faixa_peso_transporte`.

---

#### `faixa_peso_transporte`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `id` | `INTEGER` | PK (auto-incremento) |
| `nome_servico` | `VARCHAR(100)` | FK → `servico_transporte(nome_servico)` |
| `peso_min` | `DECIMAL(10,2)` | |
| `peso_max` | `DECIMAL(10,2)` | |
| `acrescimo_pct` | `DECIMAL(5,2)` | Percentual de acréscimo (ex.: 10.00 = 10%) |

- **PK**: `PRIMARY KEY (id)` — `SERIAL`
- **FK**: `FOREIGN KEY (nome_servico) REFERENCES servico_transporte(nome_servico) ON DELETE CASCADE`
- **Mock na aplicação**: No cadastro de serviço do tipo Transporte, o formulário deve permitir adicionar múltiplas faixas de peso (peso_min, peso_max, acrescimo_pct). Exemplo:
  - Faixa 1: 0–500 kg → acréscimo 0%
  - Faixa 2: 500–750 kg → acréscimo 10%
  - Faixa 3: 750+ kg → acréscimo 15%

---

#### `servico_guindaste`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `nome_servico` | `VARCHAR(100)` | PK, FK → `servico(nome_servico)` |
| `tamanho_base` | `DECIMAL(10,2)` | Tamanho da base do guindaste (m²) |
| `altura_guindaste` | `DECIMAL(10,2)` | Altura máxima que atinge (m) |

- **PK/FK**: `PRIMARY KEY (nome_servico), FOREIGN KEY (nome_servico) REFERENCES servico(nome_servico) ON DELETE CASCADE`
- **Mock na aplicação**: Subtipo da hierarquia. No cadastro de serviço do tipo Guindaste, o formulário deve incluir campos de `tamanho_base` e `altura_guindaste`.

---

#### `bonus_altura_guindaste`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `id` | `INTEGER` | PK (auto-incremento) |
| `nome_servico` | `VARCHAR(100)` | FK → `servico_guindaste(nome_servico)` |
| `altura_min` | `DECIMAL(10,2)` | |
| `altura_max` | `DECIMAL(10,2)` | |
| `bonus_pct` | `DECIMAL(5,2)` | Percentual de bônus (ex.: 5.00 = 5%) |

- **PK**: `PRIMARY KEY (id)` — `SERIAL`
- **FK**: `FOREIGN KEY (nome_servico) REFERENCES servico_guindaste(nome_servico) ON DELETE CASCADE`
- **Mock na aplicação**: No cadastro de serviço do tipo Guindaste, o formulário deve permitir adicionar múltiplas faixas de altura com bônus. Exemplo:
  - Faixa 1: 0–10m → bônus 0%
  - Faixa 2: 10–20m → bônus 5%
  - Faixa 3: 20m+ → bônus 10%

---

#### `servico_oferecido`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `id` | `INTEGER` | PK (auto-incremento) |
| `nome_empresa` | `VARCHAR(100)` | FK → `empresa(nome)` |
| `nome_servico` | `VARCHAR(100)` | FK → `servico(nome_servico)` |
| `nome_cidade` | `VARCHAR(100)` | FK → `cidade(nome_cidade)` (parte 1) |
| `estado` | `VARCHAR(2)` | FK → `cidade(estado)` (parte 2) |
| `preco_hora` | `DECIMAL(10,2)` | |

- **PK**: `PRIMARY KEY (id)` — `SERIAL`
- **FKs compostas**:
  - `FOREIGN KEY (nome_empresa) REFERENCES empresa(nome)`
  - `FOREIGN KEY (nome_servico) REFERENCES servico(nome_servico)`
  - `FOREIGN KEY (nome_cidade, estado) REFERENCES cidade(nome_cidade, estado)`
- **Mock na aplicação**: Uma empresa pode oferecer serviços diferentes em cidades diferentes com preços diferentes. O cadastro deve permitir selecionar empresa, serviço, cidade+estado e preço_hora. Esta tabela é a **base de cálculo do trigger de preço** (item 2.3).

---

#### `pedido`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `codigo` | `INTEGER` | PK (auto-incremento) |
| `codigo_cliente` | `INTEGER` | FK → `cliente(codigo)` |
| `nome_empresa` | `VARCHAR(100)` | FK → `empresa(nome)` |
| `data_solicitacao` | `DATE` | NOT NULL |
| `data_resolucao` | `DATE` | |
| `status` | `VARCHAR(20)` | (ex.: 'pendente', 'aceito', 'rejeitado') |
| `preco_total` | `DECIMAL(12,2)` | **Calculado por trigger** (item 2.2) |

- **PK**: `PRIMARY KEY (codigo)` — `SERIAL`
- **FKs**:
  - `FOREIGN KEY (codigo_cliente) REFERENCES cliente(codigo)`
  - `FOREIGN KEY (nome_empresa) REFERENCES empresa(nome)`
- **Mock na aplicação**: CRUD de pedidos. O cliente seleciona uma empresa e solicita serviços. O `preco_total` é **automaticamente calculado** por trigger (a aplicação não precisa calcular). O status controla o fluxo (pendente → aceito/rejeitado).

---

#### `servico_solicitado`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `codigo_pedido` | `INTEGER` | FK → `pedido(codigo)` |
| `nome_servico` | `VARCHAR(100)` | FK → `servico(nome_servico)` |
| `preco` | `DECIMAL(10,2)` | **Calculado por trigger** (item 2.3) |
| `endereco_partida` | `TEXT` | |
| `endereco_destino` | `TEXT` | |
| `data_realizacao` | `DATE` | |
| `tempo_gasto` | `DECIMAL(10,2)` | Horas gastas na execução |
| `peso_carga` | `DECIMAL(10,2)` | (para transporte — usado no cálculo do trigger) |
| `altura_necessaria` | `DECIMAL(10,2)` | (para guindaste — usado no cálculo do trigger) |
| `cidade_nome` | `VARCHAR(100)` | FK → `cidade(nome_cidade)` |
| `cidade_estado` | `VARCHAR(2)` | FK → `cidade(estado)` |

- **PK**: `PRIMARY KEY (codigo_pedido, nome_servico)`
- **FKs**:
  - `FOREIGN KEY (codigo_pedido) REFERENCES pedido(codigo) ON DELETE CASCADE`
  - `FOREIGN KEY (nome_servico) REFERENCES servico(nome_servico)`
  - `FOREIGN KEY (cidade_nome, cidade_estado) REFERENCES cidade(nome_cidade, estado)`
- **Mock na aplicação**: Tabela que liga pedidos a serviços. O `preco` é **calculado automaticamente** pelo trigger (item 2.3) com base em:
  - `servico_oferecido.preco_hora`
  - faixas de peso (se transporte) → acréscimo
  - faixas de altura (se guindaste) → bônus
  - `tempo_gasto`
- A aplicação deve enviar: `peso_carga` (se transporte) e `altura_necessaria` (se guindaste) para o trigger usar.

---

#### `trabalha_em`

| Coluna | Tipo | Restrições |
|--------|------|------------|
| `cpf_funcionario` | `VARCHAR(14)` | FK → `funcionario(cpf)` |
| `codigo_pedido` | `INTEGER` | FK → `pedido(codigo)` |
| `nome_servico` | `VARCHAR(100)` | FK → `servico(nome_servico)` |

- **PK**: `PRIMARY KEY (cpf_funcionario, codigo_pedido, nome_servico)`
- **FKs**:
  - `FOREIGN KEY (cpf_funcionario) REFERENCES funcionario(cpf)`
  - `FOREIGN KEY (codigo_pedido) REFERENCES pedido(codigo)`
  - `FOREIGN KEY (nome_servico) REFERENCES servico(nome_servico)`
- **Mock na aplicação**: Associa funcionários aos serviços executados em cada pedido. No detalhe do pedido (após aceito), deve ser possível alocar funcionários aos serviços solicitados.

---

## 2. Fluxo de Migração: Mock Data → PostgreSQL

### Passo a passo

1. **Instalar psycopg2-binary**

   ```bash
   pip install psycopg2-binary
   ```

   Adicionar ao `requirements.txt`:

   ```
   Flask==3.1.0
   psycopg2-binary==2.9.10
   ```

2. **Criar `config.py`**

   ```python
   import os

   DB_CONFIG = {
       "host": os.getenv("DB_HOST", "localhost"),
       "port": os.getenv("DB_PORT", "5432"),
       "dbname": os.getenv("DB_NAME", "mudancas"),
       "user": os.getenv("DB_USER", "postgres"),
       "password": os.getenv("DB_PASSWORD", "postgres"),
   }
   ```

3. **Criar `db.py`** com funções de conexão e helpers

   ```python
   import psycopg2
   import psycopg2.extras
   from config import DB_CONFIG


   def get_connection():
       """Retorna uma conexão com o banco PostgreSQL."""
       return psycopg2.connect(**DB_CONFIG)


   def query(sql, params=None):
       """Executa SELECT e retorna lista de dicionários."""
       conn = get_connection()
       try:
           with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
               cur.execute(sql, params)
               return cur.fetchall()
       finally:
           conn.close()


   def execute(sql, params=None):
       """Executa INSERT/UPDATE/DELETE e retorna linhas afetadas.
       Se for INSERT com RETURNING, retorna o resultado."""
       conn = get_connection()
       try:
           with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
               cur.execute(sql, params)
               conn.commit()
               # Se houver RETURNING, retorna o resultado
               if cur.description:
                   return cur.fetchall()
               return cur.rowcount
       except Exception as e:
           conn.rollback()
           raise e
       finally:
           conn.close()
   ```

4. **Substituir mock data por queries**

   Para cada entidade, criar funções no estilo:

   ```python
   # empresas.py (ou dentro de um módulo models/)
   from db import query, execute


   def listar_empresas():
       return query("SELECT nome, endereco FROM empresa ORDER BY nome")


   def buscar_empresa(nome):
       result = query("SELECT nome, endereco FROM empresa WHERE nome = %s", (nome,))
       return result[0] if result else None


   def criar_empresa(nome, endereco, telefones):
       # 1. Insert empresa
       execute("INSERT INTO empresa (nome, endereco) VALUES (%s, %s)", (nome, endereco))
       # 2. Insert telefones
       for tel in telefones:
           execute("INSERT INTO empresa_telefone (nome_empresa, telefone) VALUES (%s, %s)", (nome, tel))
       return {"nome": nome, "endereco": endereco}


   def atualizar_empresa(nome_antigo, nome_novo, endereco, telefones):
       execute("UPDATE empresa SET nome = %s, endereco = %s WHERE nome = %s",
               (nome_novo, endereco, nome_antigo))
       # Reinsere telefones
       execute("DELETE FROM empresa_telefone WHERE nome_empresa = %s", (nome_novo,))
       for tel in telefones:
           execute("INSERT INTO empresa_telefone (nome_empresa, telefone) VALUES (%s, %s)", (nome_novo, tel))


   def excluir_empresa(nome):
       execute("DELETE FROM empresa WHERE nome = %s", (nome,))
   ```

   **Padrão para todas as entidades:**

   | Entidade | Funções CRUD | Observações |
   |----------|-------------|-------------|
   | `cidade` | `listar_cidades()`, `buscar_cidade(nome, estado)`, `criar_cidade(...)`, `excluir_cidade(...)` | PK composta |
   | `empresa` | `listar_empresas()`, `buscar_empresa(nome)`, `criar_empresa(...)`, `atualizar_empresa(...)`, `excluir_empresa(nome)` | Telefones em cascata |
   | `cliente` | `listar_clientes()`, `buscar_cliente(codigo)`, `criar_cliente(...)`, `atualizar_cliente(...)`, `excluir_cliente(codigo)` | Código SERIAL; telefones em cascata |
   | `funcionario` | `listar_funcionarios()`, `buscar_funcionario(cpf)`, `criar_funcionario(...)`, `atualizar_funcionario(...)`, `excluir_funcionario(cpf)` | Vínculo com empresas em `funcionario_empresa` |
   | `servico` | `listar_servicos()`, `buscar_servico(nome)`, `criar_servico(...)`, `atualizar_servico(...)`, `excluir_servico(nome)` | Hierarquia: decidir subtipo no cadastro |
   | `pedido` | `listar_pedidos()`, `buscar_pedido(codigo)`, `criar_pedido(...)`, `atualizar_pedido(...)`, `excluir_pedido(codigo)` | `preco_total` é calculado por trigger |
   | `servico_solicitado` | `listar_servicos_do_pedido(codigo_pedido)`, `adicionar_servico(...)`, `remover_servico(...)` | `preco` calculado por trigger |
   | `trabalha_em` | `listar_funcionarios_do_pedido(codigo_pedido)`, `alocar_funcionario(...)`, `desalocar_funcionario(...)` | |

5. **Adaptar os POST (criar/editar/excluir):**

   Substituir cada rota Flask:

   ```python
   @app.route("/empresas", methods=["GET", "POST"])
   def empresas():
       if request.method == "POST":
           nome = request.form["nome"]
           endereco = request.form["endereco"]
           telefones = request.form.getlist("telefones")
           criar_empresa(nome, endereco, telefones)
           return redirect(url_for("empresas"))
       return render_template("empresas/lista.html", empresas=listar_empresas())
   ```

   **CRUD Create** (`INSERT ... RETURNING *`):

   ```python
   def criar_cliente(cpf, rg, endereco, nome_completo, telefones):
       result = execute("""
           INSERT INTO cliente (cpf, rg, endereco, nome_completo)
           VALUES (%s, %s, %s, %s)
           RETURNING codigo
       """, (cpf, rg, endereco, nome_completo))
       codigo = result[0]["codigo"]
       for tel in telefones:
           execute("INSERT INTO cliente_telefone (codigo_cliente, telefone) VALUES (%s, %s)",
                   (codigo, tel))
       return codigo
   ```

   **CRUD Update**:

   ```python
   def atualizar_cliente(codigo, cpf, rg, endereco, nome_completo, telefones):
       execute("""
           UPDATE cliente SET cpf=%s, rg=%s, endereco=%s, nome_completo=%s
           WHERE codigo=%s
       """, (cpf, rg, endereco, nome_completo, codigo))
       # Reinsere telefones
       execute("DELETE FROM cliente_telefone WHERE codigo_cliente = %s", (codigo,))
       for tel in telefones:
           execute("INSERT INTO cliente_telefone (codigo_cliente, telefone) VALUES (%s, %s)",
                   (codigo, tel))
   ```

   **CRUD Delete**:

   ```python
   def excluir_cliente(codigo):
       execute("DELETE FROM cliente WHERE codigo = %s", (codigo,))
   ```

6. **Relatórios (agregações):**

   Substituir agregações Python por queries SQL (ver seção 4 para queries completas).

---

## 3. Impacto das Constraints do Item 2

### 3.1 Hierarquia de Serviços (disjuntiva e parcial)

- Ao cadastrar um serviço, o app precisa permitir selecionar o tipo:
  - **Transporte**: campos adicionais para faixas de peso (peso_min, peso_max, acrescimo_pct)
  - **Guindaste**: campos adicionais para tamanho_base, altura_guindaste e faixas de bônus (altura_min, altura_max, bonus_pct)
  - **Serviço simples** (ex.: embalagem, montagem): sem subtabelas
- A constraint CHECK garantirá que um serviço seja de **apenas UM subtipo** (disjuntiva) e que pode ser **apenas um ou nenhum** (parcial).
- **Impacto no Flask**: O formulário de cadastro de serviço deve ter:
  - Um radio/select para escolher o tipo
  - Se "Transporte": mostrar seção dinâmica para adicionar faixas de peso
  - Se "Guindaste": mostrar campos de tamanho_base, altura_guindaste e seção dinâmica para faixas de bônus
  - Se "Simples": apenas o nome do serviço
  - **Exemplo de template** (`templates/servicos/form.html`):
    ```html
    <select name="tipo" id="tipo_servico" onchange="mostrarCampos()">
      <option value="simples">Serviço Simples</option>
      <option value="transporte">Transporte</option>
      <option value="guindaste">Guindaste</option>
    </select>

    <div id="campos_transporte" style="display:none;">
      <h4>Faixas de Peso</h4>
      <div class="faixa-peso">
        <input type="number" name="peso_min" placeholder="Peso mínimo (kg)">
        <input type="number" name="peso_max" placeholder="Peso máximo (kg)">
        <input type="number" name="acrescimo_pct" placeholder="Acréscimo (%)">
      </div>
    </div>

    <div id="campos_guindaste" style="display:none;">
      <input type="number" name="tamanho_base" placeholder="Tamanho da base (m²)">
      <input type="number" name="altura_guindaste" placeholder="Altura do guindaste (m)">
      <h4>Faixas de Bônus</h4>
      <div class="faixa-bonus">
        <input type="number" name="altura_min" placeholder="Altura mínima (m)">
        <input type="number" name="altura_max" placeholder="Altura máxima (m)">
        <input type="number" name="bonus_pct" placeholder="Bônus (%)">
      </div>
    </div>
    ```

### 3.2 Preço Total do Pedido

- O trigger de `preco_total` no SQL calculará **automaticamente** a soma dos preços de `servico_solicitado` vinculados ao pedido.
- A aplicação **não precisa mais calcular** o `preco_total` ao salvar. Basta inserir/atualizar os registros em `servico_solicitado` que o trigger atualiza `pedido.preco_total`.
- **Mas a interface deve exibir o preço_total atualizado** ao visualizar/editar o pedido. Exemplo:

  ```python
  def buscar_pedido(codigo):
      return query("SELECT * FROM pedido WHERE codigo = %s", (codigo,))[0]
  ```

  O campo `preco_total` virá preenchido pelo trigger.

- **Trigger conceitual (item 2.2)**:
  ```sql
  CREATE OR REPLACE FUNCTION atualiza_preco_total()
  RETURNS TRIGGER AS $$
  BEGIN
      UPDATE pedido
      SET preco_total = (
          SELECT COALESCE(SUM(preco), 0)
          FROM servico_solicitado
          WHERE codigo_pedido = COALESCE(NEW.codigo_pedido, OLD.codigo_pedido)
      )
      WHERE codigo = COALESCE(NEW.codigo_pedido, OLD.codigo_pedido);
      RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER trg_atualiza_preco_total
  AFTER INSERT OR UPDATE OR DELETE ON servico_solicitado
  FOR EACH ROW EXECUTE FUNCTION atualiza_preco_total();
  ```

### 3.3 Preço de Cada Serviço (item 2.3)

- **Trigger BEFORE INSERT OR UPDATE em `servico_solicitado`** calcula o `preco` automaticamente.
- O trigger consulta `servico_oferecido.preco_hora`, identifica se o serviço é Transporte ou Guindaste, aplica acréscimos/bônus das faixas e multiplica por `tempo_gasto`.
- A aplicação **não precisa mais calcular o preço manualmente** — envia os dados base e o trigger calcula.
- Mas o formulário deve enviar os campos adicionais necessários para o cálculo:
  - Para **transporte**: `peso_carga` (kg) — usado para determinar qual faixa de peso se aplica
  - Para **guindaste**: `altura_necessaria` (m) — usado para determinar qual faixa de bônus se aplica
- **Trigger conceitual (item 2.3)**:
  ```sql
  CREATE OR REPLACE FUNCTION calcula_preco_servico()
  RETURNS TRIGGER AS $$
  DECLARE
      v_preco_hora DECIMAL;
      v_acrescimo DECIMAL := 0;
      v_bonus DECIMAL := 0;
      v_tipo VARCHAR;
  BEGIN
      -- Busca preco_hora em servico_oferecido
      SELECT so.preco_hora INTO v_preco_hora
      FROM servico_oferecido so
      WHERE so.nome_empresa = (
              SELECT p.nome_empresa FROM pedido p WHERE p.codigo = NEW.codigo_pedido
          )
          AND so.nome_servico = NEW.nome_servico
          AND so.nome_cidade = NEW.cidade_nome
          AND so.estado = NEW.cidade_estado;

      IF NOT FOUND THEN
          RAISE EXCEPTION 'Serviço não oferecido pela empresa nesta cidade';
      END IF;

      -- Verifica se é transporte
      IF EXISTS (SELECT 1 FROM servico_transporte WHERE nome_servico = NEW.nome_servico) THEN
          SELECT acrescimo_pct INTO v_acrescimo
          FROM faixa_peso_transporte
          WHERE nome_servico = NEW.nome_servico
            AND NEW.peso_carga BETWEEN peso_min AND peso_max;
          v_acrescimo := COALESCE(v_acrescimo, 0);
      END IF;

      -- Verifica se é guindaste
      IF EXISTS (SELECT 1 FROM servico_guindaste WHERE nome_servico = NEW.nome_servico) THEN
          SELECT bonus_pct INTO v_bonus
          FROM bonus_altura_guindaste
          WHERE nome_servico = NEW.nome_servico
            AND NEW.altura_necessaria BETWEEN altura_min AND altura_max;
          v_bonus := COALESCE(v_bonus, 0);
      END IF;

      -- Calcula preco = preco_hora * tempo_gasto * (1 + acrescimo/100) * (1 + bonus/100)
      NEW.preco := v_preco_hora * NEW.tempo_gasto * (1 + v_acrescimo/100) * (1 + v_bonus/100);

      RETURN NEW;
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER trg_calcula_preco_servico
  BEFORE INSERT OR UPDATE ON servico_solicitado
  FOR EACH ROW EXECUTE FUNCTION calcula_preco_servico();
  ```

---

## 4. Formato de Saída SQL Esperado para os Relatórios

Para cada relatório da aplicação, a query SQL equivalente que substitui a agregação em Python.

### 4.1 Histograma de Serviços por Cidade

```sql
SELECT
    ss.cidade_nome,
    ss.cidade_estado,
    COUNT(*) AS quantidade
FROM servico_solicitado ss
GROUP BY ss.cidade_nome, ss.cidade_estado
ORDER BY quantidade DESC;
```

**Uso no Flask**:
```python
def histograma_servicos_por_cidade():
    return query("""
        SELECT ss.cidade_nome, ss.cidade_estado, COUNT(*) AS quantidade
        FROM servico_solicitado ss
        GROUP BY ss.cidade_nome, ss.cidade_estado
        ORDER BY quantidade DESC
    """)
```

### 4.2 Histograma de Pagamentos por Cidade

```sql
SELECT
    ss.cidade_nome,
    ss.cidade_estado,
    SUM(ss.preco) AS total_pago
FROM servico_solicitado ss
GROUP BY ss.cidade_nome, ss.cidade_estado
ORDER BY total_pago DESC;
```

**Uso no Flask**:
```python
def histograma_pagamentos_por_cidade():
    return query("""
        SELECT ss.cidade_nome, ss.cidade_estado, SUM(ss.preco) AS total_pago
        FROM servico_solicitado ss
        GROUP BY ss.cidade_nome, ss.cidade_estado
        ORDER BY total_pago DESC
    """)
```

### 4.3 Top 5 Cidades por Valor Investido

```sql
SELECT
    ss.cidade_nome,
    ss.cidade_estado,
    SUM(ss.preco) AS valor_total
FROM servico_solicitado ss
GROUP BY ss.cidade_nome, ss.cidade_estado
ORDER BY valor_total DESC
LIMIT 5;
```

**Uso no Flask**:
```python
def top5_cidades_valor():
    return query("""
        SELECT ss.cidade_nome, ss.cidade_estado, SUM(ss.preco) AS valor_total
        FROM servico_solicitado ss
        GROUP BY ss.cidade_nome, ss.cidade_estado
        ORDER BY valor_total DESC
        LIMIT 5
    """)
```

### 4.4 Top 5 Cidades por Número de Serviços

```sql
SELECT
    ss.cidade_nome,
    ss.cidade_estado,
    COUNT(*) AS quantidade
FROM servico_solicitado ss
GROUP BY ss.cidade_nome, ss.cidade_estado
ORDER BY quantidade DESC
LIMIT 5;
```

**Uso no Flask**:
```python
def top5_cidades_servicos():
    return query("""
        SELECT ss.cidade_nome, ss.cidade_estado, COUNT(*) AS quantidade
        FROM servico_solicitado ss
        GROUP BY ss.cidade_nome, ss.cidade_estado
        ORDER BY quantidade DESC
        LIMIT 5
    """)
```

### 4.5 Top 5 Empresas por Número de Serviços Solicitados

```sql
SELECT
    p.nome_empresa,
    COUNT(DISTINCT p.codigo) AS total_pedidos,
    COUNT(ss.nome_servico) AS total_servicos
FROM pedido p
LEFT JOIN servico_solicitado ss ON ss.codigo_pedido = p.codigo
GROUP BY p.nome_empresa
ORDER BY total_servicos DESC
LIMIT 5;
```

**Uso no Flask**:
```python
def top5_empresas_servicos():
    return query("""
        SELECT p.nome_empresa, COUNT(DISTINCT p.codigo) AS total_pedidos,
               COUNT(ss.nome_servico) AS total_servicos
        FROM pedido p
        LEFT JOIN servico_solicitado ss ON ss.codigo_pedido = p.codigo
        GROUP BY p.nome_empresa
        ORDER BY total_servicos DESC
        LIMIT 5
    """)
```

### 4.6 Top 5 Empresas por Valores Ganhos

```sql
SELECT
    p.nome_empresa,
    SUM(ss.preco) AS valor_total_ganho
FROM pedido p
JOIN servico_solicitado ss ON ss.codigo_pedido = p.codigo
WHERE p.status = 'aceito'
GROUP BY p.nome_empresa
ORDER BY valor_total_ganho DESC
LIMIT 5;
```

**Uso no Flask**:
```python
def top5_empresas_valores():
    return query("""
        SELECT p.nome_empresa, SUM(ss.preco) AS valor_total_ganho
        FROM pedido p
        JOIN servico_solicitado ss ON ss.codigo_pedido = p.codigo
        WHERE p.status = 'aceito'
        GROUP BY p.nome_empresa
        ORDER BY valor_total_ganho DESC
        LIMIT 5
    """)
```

---

## 5. Checklist de Migração

- [ ] **Instalar psycopg2-binary** (`pip install psycopg2-binary`) e adicionar ao `requirements.txt`
- [ ] **Criar `config.py`** com `DB_CONFIG` usando variáveis de ambiente
- [ ] **Criar schema SQL (item 1)** com todas as tabelas, PKs, FKs, tipos e constraints de domínio
- [ ] **Executar schema.sql** no PostgreSQL
- [ ] **Criar triggers SQL (item 2)** com:
  - [ ] Trigger de hierarquia disjuntiva/parcial de serviços
  - [ ] Trigger de preço_total do pedido
  - [ ] Trigger de cálculo de preço do serviço_solicitado
- [ ] **Executar triggers.sql** no PostgreSQL
- [ ] **Criar `db.py`** com `get_connection()`, `query()`, `execute()`
- [ ] **Substituir mock de empresas** por queries SQL
- [ ] **Substituir mock de clientes** por queries SQL
- [ ] **Substituir mock de cidades** por queries SQL
- [ ] **Substituir mock de serviços** por queries SQL (com subtipos: transporte, guindaste, simples)
- [ ] **Substituir mock de pedidos** por queries SQL
- [ ] **Substituir mock de funcionários** por queries SQL
- [ ] **Adaptar relatórios** para queries SQL agregadas (6 queries da seção 4)
- [ ] **Criar templates Flask** para cada entidade (diretórios já existem, vazios):
  - [ ] `templates/cidades/lista.html`, `templates/cidades/form.html`
  - [ ] `templates/clientes/lista.html`, `templates/clientes/form.html`
  - [ ] `templates/empresas/lista.html`, `templates/empresas/form.html`
  - [ ] `templates/funcionarios/lista.html`, `templates/funcionarios/form.html`
  - [ ] `templates/servicos/lista.html`, `templates/servicos/form.html` (com selector de subtipo)
  - [ ] `templates/pedidos/lista.html`, `templates/pedidos/form.html`, `templates/pedidos/detalhe.html`
  - [ ] `templates/relatorios/index.html` (com links para cada relatório)
- [ ] **Testar CRUDs** com dados reais no PostgreSQL
- [ ] **Testar constraints** (tentar violar FK, violar hierarquia, violar domínio) e ver erros amigáveis
- [ ] **Testar triggers**:
  - [ ] Inserir servico_solicitado e verificar se preco foi calculado
  - [ ] Atualizar pedido e verificar se preco_total reflete a soma
- [ ] **Testar relatórios** com dados populados

---

## Notas Finais

- O arquivo `SolucaoMudancasEP1EP22026.pdf` contém o diagrama ER e o mapeamento lógico completo — consultá-lo como referência para o schema SQL do item 1.
- O arquivo `ProblemaMudanzasParte22026.doc` contém a descrição original do problema.
- Os templates Flask estão em diretórios vazios prontos para serem preenchidos.
- **Todas as queries devem usar parâmetros `%s`** (psycopg2) para prevenir SQL injection.
- Usar `fetchall()` para listas e `fetchone()` para buscas individuais.
- Sempre tratar erros de banco com try/except e exibir mensagens amigáveis ao usuário.
