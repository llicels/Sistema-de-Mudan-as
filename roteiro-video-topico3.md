# Roteiro para Vídeo — Tópico 3: Demonstração do Sistema

**Duração:** ~5 minutos | **Formato:** Gravação de tela com narração

### Stack utilizada

- **Backend:** Python (Flask) + psycopg2
- **Banco de dados:** PostgreSQL (com triggers para cálculo automático de preços)
- **Frontend:** HTML, CSS, Chart.js (JavaScript)

---

## 1. ABERTURA — O que é o sistema (0:00–0:30)

**O que dizer:**

> "Este é o Sistema de Mudanças — 'Mudanças até o Fim do Mundo'. É uma plataforma web construída com Python (Flask) no backend, PostgreSQL para armazenamento com triggers que calculam automaticamente os preços, e HTML/CSS/Chart.js no frontend. O sistema permite que clientes solicitem serviços de mudanças a empresas cadastradas, calculando automaticamente o preço de cada pedido considerando acréscimos por carga excedente e bônus por altura de guindaste."

**O que mostrar:**
- Página inicial do README ou slide com o nome do sistema
- Nada de tela do sistema ainda — só a fala

---

## 2. DASHBOARD — Visão geral (0:30–1:00)

**O que dizer:**

> "Ao acessar o sistema, o primeiro contato é o Dashboard. Aqui temos uma visão consolidada de tudo: quantas empresas, clientes, cidades, serviços, pedidos e funcionários estão cadastrados, além dos pedidos mais recentes com seus status."

**O que mostrar:**
- Tela do Dashboard (`http://localhost:5001/`) — mostrar os cards com contagens e a tabela de últimos pedidos
- Clicar em "Novo Pedido" e em "Ver Relatórios" para dar fluidez

---

## 3. CADASTROS — Empresas e Serviços (1:00–2:00)

**O que dizer:**

> "O sistema oferece CRUD completo para todas as entidades. Vamos cadastrar uma empresa, um serviço e ver como a hierarquia de serviços funciona."

**O que mostrar:**
- **Empresas:** Navegar até "Cadastros > Empresas", clicar em "+ Nova Empresa", preencher nome, endereço e telefones, salvar e mostrar a lista atualizada.
- **Serviços:** Navegar até "Serviços", clicar em "+ Novo Serviço". Mostrar o seletor de tipo (Simples / Transporte / Guindaste). Selecionar "Transporte" e demonstrar os campos dinâmicos de faixas de peso (limite de carga e acréscimo percentual). Salvar. Repetir com "Guindaste" mostrando campos de tamanho da base, altura e bônus por altura.

---

## 4. PEDIDOS — O coração do sistema (2:00–3:30)

**O que dizer:**

> "O ponto central do sistema é o pedido. Aqui o cliente solicita serviços a uma empresa, informa as cidades de partida e destino, e o sistema calcula o preço automaticamente através de triggers no PostgreSQL — nada de cálculo manual no código."

**Dica para a demonstração:** Para evitar erros de "serviço não oferecido pela empresa", use esta combinação garantida do seed de dados:

- **Empresa:** `Mudanças Rápidas Ltda` (1)
- **Cliente:** `Ana Souza` (código 1) — CPF `11122233344`
- **Partida:** São Paulo / **Destino:** São Paulo
- **Serviço:** `Embalagem` (tipo OUTRO, sem dependências de faixa)
- **Duração:** `2 hours`

**Por que funciona:** A tabela `oferecem` já tem `(1, 'São Paulo', 'Embalagem', 80.00)` e o tipo OUTRO não precisa de cálculos extras.

**O que mostrar:**
- Navegar até "Pedidos > Novo Pedido"
- Preencher com os dados acima: empresa Mudanças Rápidas Ltda, cliente Ana Souza, Partida: São Paulo, Destino: São Paulo
- Adicionar o serviço "Embalagem" com duração de 2 hours
- Salvar e mostrar a lista de pedidos
- Clicar no pedido recém-criado para abrir a página de detalhes, destacando o Preço Total calculado automaticamente (R$ 160.00 = 80/hora × 2h) e a tabela de serviços com cada preço individual
- Na página de detalhes, mostrar a seção de alocação de funcionários por solicitação de serviço (botão de alocar/desalocar)

**O que dizer:**

> "O sistema também gerencia clientes e funcionários, incluindo o vínculo de funcionários com empresas e a alocação de funcionários em cada solicitação de serviço dentro dos pedidos."

**O que mostrar:**
- Clientes: lista com busca, formulário de criação (CPF, nome, endereço, telefones)
- Funcionários: lista, formulário com tipo, salário e vínculos com empresas (checkboxes de empresas)
- Na página de detalhe de um pedido, mostrar a seção de alocação de funcionários por solicitação de serviço (botão de alocar/desalocar)

---

## 5. RELATÓRIOS — Gráficos e Rankings (3:30–4:15)

**O que dizer:**

> "Na aba de Relatórios, o sistema oferece histogramas e rankings usando Chart.js. Podemos ver a distribuição de serviços por cidade, o valor total pago, e os top 5 por serviços e receita."

**O que mostrar:**
- Navegar até "Relatórios"
- Clicar em cada relatório para mostrar:
  - Histograma de Serviços por Cidade (gráfico de barras)
  - Histograma de Pagamentos por Cidade (gráfico de barras)
  - Top 5 Cidades por Valor
  - Top 5 Cidades por Número de Serviços
  - Top 5 Empresas por Serviços
  - Top 5 Empresas por Receita
- Destacar que os dados vêm diretamente de queries SQL agregadas

---

## 6. CADASTROS — Clientes e Funcionários (4:15–4:45)

**O que dizer:**

> "O sistema também gerencia clientes e funcionários, incluindo o vínculo de funcionários com empresas e a alocação de funcionários em cada solicitação de serviço dentro dos pedidos."

**O que mostrar:**
- Clientes: lista com busca, formulário de criação (CPF, nome, endereço, telefones)
- Funcionários: lista, formulário com tipo, salário e vínculos com empresas (checkboxes de empresas)
- Na página de detalhe de um pedido, mostrar a seção de alocação de funcionários por solicitação de serviço (botão de alocar/desalocar)

---

## 7. ENCERRAMENTO (4:45–5:00)

**O que dizer:**

> "O Tópico 3 do trabalho é a aplicação web Flask completa, integrando todos os modelos do banco de dados com uma interface intuitiva. O destaque fica para o cálculo automático de preços via triggers PostgreSQL e a hierarquia de serviços com subtipos. Obrigado."

**O que mostrar:**
- Voltar ao Dashboard como tela final

---

## Dicas para a gravação

- **Velocidade:** Fale num ritmo natural, sem pressa — ~5 min dá conforto para cobrir tudo
- **Destaque visual:** Use o zoom ou resize da janela do navegador para ficar legível na gravação
- **Antes de gravar:** Popule o banco com os dados de seed (`seed.sql`) para que as tabelas tenham dados reais e não fiquem vazias na tela
- **Porta:** O app roda na porta `5001` (padrão). Se estiver ocupada, use `FLASK_PORT=5000 python app.py`

### Comandos para preparar o banco e rodar a aplicação

```bash
# 1. Configurar o banco (cria schema, triggers e povoa com dados)
cd aplicacao
chmod +x setup.sh
./setup.sh

# 2. (Alternativa) Se já configurou o banco, suba só o app:
cd aplicacao
source venv/bin/activate
python app.py

# 3. Se precisar de outra porta (ex.: 5000 para não conflitar com outro app):
export FLASK_PORT=5000 && python app.py

# Acessar em http://localhost:5001 (ou a outra porta definida)
```

- **Coordenadas de mouse:** Evite cliques aleatórios — passe o cursor sobre os links antes de clicar para o vídeo ficar limpo