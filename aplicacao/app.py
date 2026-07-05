"""
Mudanças até o Fim do Mundo — Backrooms Furniture Store Theme
Flask application with full CRUD and reporting.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'backrooms-mudancas-2026-secret-key'

# ============================================================
# MOCK DATA
# ============================================================

empresas = [
    {"nome": "Mudanças Express", "endereco": "Av. Paulista, 1000", "telefones": ["11-99999-0001"]},
    {"nome": "Transportes ABC", "endereco": "Rua da Glória, 500", "telefones": ["21-98888-0002"]},
    {"nome": "Guindastes Forte", "endereco": "Av. Brasil, 2000", "telefones": ["31-97777-0003"]},
    {"nome": "MudaJá", "endereco": "Rua XV de Novembro, 150", "telefones": ["41-96666-0004"]},
    {"nome": "Super Muda", "endereco": "Rua das Flores, 300", "telefones": ["51-95555-0005"]},
    {"nome": "Carga Pesada", "endereco": "Av. Getúlio Vargas, 800", "telefones": ["61-94444-0006"]},
]

cidades = [
    {"nome": "São Paulo", "estado": "SP"},
    {"nome": "Rio de Janeiro", "estado": "RJ"},
    {"nome": "Belo Horizonte", "estado": "MG"},
    {"nome": "Curitiba", "estado": "PR"},
    {"nome": "Porto Alegre", "estado": "RS"},
    {"nome": "Brasília", "estado": "DF"},
    {"nome": "Salvador", "estado": "BA"},
    {"nome": "Recife", "estado": "PE"},
]

servicos = [
    {"nome": "Transporte"},
    {"nome": "Embalagem"},
    {"nome": "Montagem"},
    {"nome": "Guindaste"},
    {"nome": "Desmontagem"},
]

clientes = [
    {"codigo": 1, "cpf": "123.456.789-00", "rg": "12.345.678-9", "endereco": "Rua A, 100", "nome_completo": "Carlos Silva", "telefones": ["11-91234-5678"]},
    {"codigo": 2, "cpf": "987.654.321-00", "rg": "87.654.321-9", "endereco": "Rua B, 200", "nome_completo": "Ana Oliveira", "telefones": ["21-92345-6789"]},
    {"codigo": 3, "cpf": "456.789.123-00", "rg": "45.678.912-3", "endereco": "Rua C, 300", "nome_completo": "Pedro Santos", "telefones": ["31-93456-7890"]},
    {"codigo": 4, "cpf": "789.123.456-00", "rg": "78.912.345-6", "endereco": "Rua D, 400", "nome_completo": "Marina Costa", "telefones": ["41-94567-8901"]},
    {"codigo": 5, "cpf": "321.654.987-00", "rg": "32.165.498-7", "endereco": "Rua E, 500", "nome_completo": "João Souza", "telefones": ["51-95678-9012"]},
]

funcionarios = [
    {"cpf": "111.222.333-44", "rg": "11.222.333-4", "endereco": "Rua dos Funcionários, 10", "nome_completo": "José Pereira", "tipo": "Motorista", "salario": 3500.00, "empresas": ["Mudanças Express"]},
    {"cpf": "222.333.444-55", "rg": "22.333.444-5", "endereco": "Rua dos Funcionários, 20", "nome_completo": "Maria Souza", "tipo": "Guincho", "salario": 2800.00, "empresas": ["Mudanças Express", "Guindastes Forte"]},
    {"cpf": "333.444.555-66", "rg": "33.444.555-6", "endereco": "Rua dos Funcionários, 30", "nome_completo": "Lucas Lima", "tipo": "Gerente de Mudanças", "salario": 4500.00, "empresas": ["Transportes ABC"]},
    {"cpf": "444.555.666-77", "rg": "44.555.666-7", "endereco": "Rua dos Funcionários, 40", "nome_completo": "Fernanda Rocha", "tipo": "Motorista", "salario": 3200.00, "empresas": ["MudaJá", "Super Muda"]},
    {"cpf": "555.666.777-88", "rg": "55.666.777-8", "endereco": "Rua dos Funcionários, 50", "nome_completo": "Ricardo Alves", "tipo": "Ajudante", "salario": 2200.00, "empresas": ["Carga Pesada"]},
]

servicos_oferecidos = [
    {"id": 1, "empresa": "Mudanças Express", "servico": "Transporte", "cidade": "São Paulo", "estado": "SP", "preco_hora": 120.0},
    {"id": 2, "empresa": "Mudanças Express", "servico": "Embalagem", "cidade": "São Paulo", "estado": "SP", "preco_hora": 50.0},
    {"id": 3, "empresa": "Mudanças Express", "servico": "Guindaste", "cidade": "São Paulo", "estado": "SP", "preco_hora": 200.0},
    {"id": 4, "empresa": "Transportes ABC", "servico": "Transporte", "cidade": "Rio de Janeiro", "estado": "RJ", "preco_hora": 130.0},
    {"id": 5, "empresa": "Transportes ABC", "servico": "Montagem", "cidade": "Rio de Janeiro", "estado": "RJ", "preco_hora": 70.0},
    {"id": 6, "empresa": "Transportes ABC", "servico": "Embalagem", "cidade": "Rio de Janeiro", "estado": "RJ", "preco_hora": 55.0},
    {"id": 7, "empresa": "Guindastes Forte", "servico": "Guindaste", "cidade": "Belo Horizonte", "estado": "MG", "preco_hora": 220.0},
    {"id": 8, "empresa": "Guindastes Forte", "servico": "Transporte", "cidade": "Belo Horizonte", "estado": "MG", "preco_hora": 115.0},
    {"id": 9, "empresa": "Guindastes Forte", "servico": "Desmontagem", "cidade": "Belo Horizonte", "estado": "MG", "preco_hora": 80.0},
    {"id": 10, "empresa": "MudaJá", "servico": "Embalagem", "cidade": "Curitiba", "estado": "PR", "preco_hora": 48.0},
    {"id": 11, "empresa": "MudaJá", "servico": "Desmontagem", "cidade": "Curitiba", "estado": "PR", "preco_hora": 75.0},
    {"id": 12, "empresa": "MudaJá", "servico": "Transporte", "cidade": "Curitiba", "estado": "PR", "preco_hora": 110.0},
    {"id": 13, "empresa": "Super Muda", "servico": "Transporte", "cidade": "Porto Alegre", "estado": "RS", "preco_hora": 125.0},
    {"id": 14, "empresa": "Super Muda", "servico": "Montagem", "cidade": "Porto Alegre", "estado": "RS", "preco_hora": 65.0},
    {"id": 15, "empresa": "Carga Pesada", "servico": "Transporte", "cidade": "Brasília", "estado": "DF", "preco_hora": 140.0},
    {"id": 16, "empresa": "Carga Pesada", "servico": "Guindaste", "cidade": "Brasília", "estado": "DF", "preco_hora": 210.0},
    {"id": 17, "empresa": "Mudanças Express", "servico": "Transporte", "cidade": "Salvador", "estado": "BA", "preco_hora": 130.0},
    {"id": 18, "empresa": "Transportes ABC", "servico": "Transporte", "cidade": "Recife", "estado": "PE", "preco_hora": 125.0},
    {"id": 19, "empresa": "Transportes ABC", "servico": "Guindaste", "cidade": "Recife", "estado": "PE", "preco_hora": 190.0},
    {"id": 20, "empresa": "Mudanças Express", "servico": "Montagem", "cidade": "São Paulo", "estado": "SP", "preco_hora": 60.0},
]

pedidos = [
    {
        "codigo": 1,
        "cliente": "Carlos Silva",
        "empresa": "Mudanças Express",
        "data_solicitacao": "2026-06-01",
        "data_resolucao": "2026-06-02",
        "status": "Aceito",
        "preco_total": 1240.0,
        "servicos": [
            {"servico": "Transporte", "preco": 800.0, "endereco_partida": "Rua A, 100", "endereco_destino": "Rua B, 200",
             "cidade_nome": "São Paulo", "cidade_estado": "SP", "data_realizacao": "2026-06-10", "tempo_gasto": 4.0},
            {"servico": "Embalagem", "preco": 440.0, "endereco_partida": "Rua A, 100", "endereco_destino": "",
             "cidade_nome": "São Paulo", "cidade_estado": "SP", "data_realizacao": "2026-06-09", "tempo_gasto": 3.0},
        ]
    },
    {
        "codigo": 2,
        "cliente": "Ana Oliveira",
        "empresa": "Transportes ABC",
        "data_solicitacao": "2026-06-05",
        "data_resolucao": "2026-06-07",
        "status": "Concluído",
        "preco_total": 1850.0,
        "servicos": [
            {"servico": "Transporte", "preco": 1100.0, "endereco_partida": "Rua B, 200", "endereco_destino": "Av. Atlântica, 500",
             "cidade_nome": "Rio de Janeiro", "cidade_estado": "RJ", "data_realizacao": "2026-06-15", "tempo_gasto": 5.0},
            {"servico": "Montagem", "preco": 750.0, "endereco_partida": "Av. Atlântica, 500", "endereco_destino": "",
             "cidade_nome": "Rio de Janeiro", "cidade_estado": "RJ", "data_realizacao": "2026-06-16", "tempo_gasto": 4.0},
        ]
    },
    {
        "codigo": 3,
        "cliente": "Pedro Santos",
        "empresa": "Guindastes Forte",
        "data_solicitacao": "2026-06-10",
        "data_resolucao": "",
        "status": "Em Andamento",
        "preco_total": 2100.0,
        "servicos": [
            {"servico": "Guindaste", "preco": 1500.0, "endereco_partida": "Rua C, 300", "endereco_destino": "Av. Afonso Pena, 1000",
             "cidade_nome": "Belo Horizonte", "cidade_estado": "MG", "data_realizacao": "2026-06-20", "tempo_gasto": 3.0},
            {"servico": "Transporte", "preco": 600.0, "endereco_partida": "Rua C, 300", "endereco_destino": "Av. Afonso Pena, 1000",
             "cidade_nome": "Belo Horizonte", "cidade_estado": "MG", "data_realizacao": "2026-06-20", "tempo_gasto": 4.0},
        ]
    },
    {
        "codigo": 4,
        "cliente": "Marina Costa",
        "empresa": "MudaJá",
        "data_solicitacao": "2026-06-12",
        "data_resolucao": "2026-06-14",
        "status": "Concluído",
        "preco_total": 800.0,
        "servicos": [
            {"servico": "Embalagem", "preco": 350.0, "endereco_partida": "Rua D, 400", "endereco_destino": "",
             "cidade_nome": "Curitiba", "cidade_estado": "PR", "data_realizacao": "2026-06-22", "tempo_gasto": 5.0},
            {"servico": "Desmontagem", "preco": 450.0, "endereco_partida": "Rua D, 400", "endereco_destino": "",
             "cidade_nome": "Curitiba", "cidade_estado": "PR", "data_realizacao": "2026-06-22", "tempo_gasto": 3.0},
        ]
    },
    {
        "codigo": 5,
        "cliente": "João Souza",
        "empresa": "Super Muda",
        "data_solicitacao": "2026-06-15",
        "data_resolucao": "2026-06-17",
        "status": "Concluído",
        "preco_total": 1500.0,
        "servicos": [
            {"servico": "Transporte", "preco": 1000.0, "endereco_partida": "Rua E, 500", "endereco_destino": "Rua dos Andradas, 300",
             "cidade_nome": "Porto Alegre", "cidade_estado": "RS", "data_realizacao": "2026-06-25", "tempo_gasto": 5.0},
            {"servico": "Montagem", "preco": 500.0, "endereco_partida": "Rua dos Andradas, 300", "endereco_destino": "",
             "cidade_nome": "Porto Alegre", "cidade_estado": "RS", "data_realizacao": "2026-06-26", "tempo_gasto": 3.0},
        ]
    },
    {
        "codigo": 6,
        "cliente": "Carlos Silva",
        "empresa": "Carga Pesada",
        "data_solicitacao": "2026-06-18",
        "data_resolucao": "",
        "status": "Pendente",
        "preco_total": 3200.0,
        "servicos": [
            {"servico": "Transporte", "preco": 1800.0, "endereco_partida": "Rua A, 100", "endereco_destino": "SQS 302, Bloco K",
             "cidade_nome": "Brasília", "cidade_estado": "DF", "data_realizacao": "2026-07-01", "tempo_gasto": 6.0},
            {"servico": "Guindaste", "preco": 1400.0, "endereco_partida": "Rua A, 100", "endereco_destino": "SQS 302, Bloco K",
             "cidade_nome": "Brasília", "cidade_estado": "DF", "data_realizacao": "2026-07-01", "tempo_gasto": 2.0},
        ]
    },
    {
        "codigo": 7,
        "cliente": "Ana Oliveira",
        "empresa": "Mudanças Express",
        "data_solicitacao": "2026-06-20",
        "data_resolucao": "2026-06-22",
        "status": "Concluído",
        "preco_total": 1760.0,
        "servicos": [
            {"servico": "Transporte", "preco": 1200.0, "endereco_partida": "Av. Oceânica, 100", "endereco_destino": "Rua Chile, 50",
             "cidade_nome": "Salvador", "cidade_estado": "BA", "data_realizacao": "2026-06-28", "tempo_gasto": 5.0},
            {"servico": "Embalagem", "preco": 560.0, "endereco_partida": "Av. Oceânica, 100", "endereco_destino": "",
             "cidade_nome": "Salvador", "cidade_estado": "BA", "data_realizacao": "2026-06-27", "tempo_gasto": 4.0},
        ]
    },
    {
        "codigo": 8,
        "cliente": "Pedro Santos",
        "empresa": "Transportes ABC",
        "data_solicitacao": "2026-06-22",
        "data_resolucao": "",
        "status": "Em Andamento",
        "preco_total": 2600.0,
        "servicos": [
            {"servico": "Transporte", "preco": 900.0, "endereco_partida": "Rua C, 300", "endereco_destino": "Av. Boa Viagem, 200",
             "cidade_nome": "Recife", "cidade_estado": "PE", "data_realizacao": "2026-07-02", "tempo_gasto": 4.0},
            {"servico": "Guindaste", "preco": 1200.0, "endereco_partida": "Rua C, 300", "endereco_destino": "Av. Boa Viagem, 200",
             "cidade_nome": "Recife", "cidade_estado": "PE", "data_realizacao": "2026-07-02", "tempo_gasto": 2.0},
            {"servico": "Montagem", "preco": 500.0, "endereco_partida": "Av. Boa Viagem, 200", "endereco_destino": "",
             "cidade_nome": "Recife", "cidade_estado": "PE", "data_realizacao": "2026-07-03", "tempo_gasto": 3.0},
        ]
    },
    {
        "codigo": 9,
        "cliente": "Marina Costa",
        "empresa": "Guindastes Forte",
        "data_solicitacao": "2026-06-25",
        "data_resolucao": "2026-06-27",
        "status": "Concluído",
        "preco_total": 1920.0,
        "servicos": [
            {"servico": "Guindaste", "preco": 1400.0, "endereco_partida": "Rua D, 400", "endereco_destino": "Av. Paulista, 2000",
             "cidade_nome": "São Paulo", "cidade_estado": "SP", "data_realizacao": "2026-07-05", "tempo_gasto": 3.0},
            {"servico": "Transporte", "preco": 520.0, "endereco_partida": "Rua D, 400", "endereco_destino": "Av. Paulista, 2000",
             "cidade_nome": "São Paulo", "cidade_estado": "SP", "data_realizacao": "2026-07-05", "tempo_gasto": 4.0},
        ]
    },
    {
        "codigo": 10,
        "cliente": "João Souza",
        "empresa": "MudaJá",
        "data_solicitacao": "2026-06-28",
        "data_resolucao": "",
        "status": "Aceito",
        "preco_total": 1140.0,
        "servicos": [
            {"servico": "Transporte", "preco": 750.0, "endereco_partida": "Rua E, 500", "endereco_destino": "Av. Rio Branco, 300",
             "cidade_nome": "Rio de Janeiro", "cidade_estado": "RJ", "data_realizacao": "2026-07-08", "tempo_gasto": 4.0},
            {"servico": "Embalagem", "preco": 390.0, "endereco_partida": "Rua E, 500", "endereco_destino": "",
             "cidade_nome": "Rio de Janeiro", "cidade_estado": "RJ", "data_realizacao": "2026-07-07", "tempo_gasto": 3.0},
        ]
    },
]


# ============================================================
# HELPER: next available ID
# ============================================================

def _next_pedido_codigo() -> int:
    """Retorna o próximo código disponível para um novo pedido.

    Obtém o maior código existente na lista de pedidos e incrementa em 1.
    Se não houver pedidos cadastrados, retorna 1.

    Returns:
        int: Código numérico único para o próximo pedido.
    """
    if not pedidos:
        return 1
    return max(p["codigo"] for p in pedidos) + 1


def _next_cliente_codigo() -> int:
    """Retorna o próximo código disponível para um novo cliente.

    Obtém o maior código existente na lista de clientes e incrementa em 1.
    Se não houver clientes cadastrados, retorna 1.

    Returns:
        int: Código numérico único para o próximo cliente.
    """
    if not clientes:
        return 1
    return max(c["codigo"] for c in clientes) + 1


def _next_servico_oferecido_id() -> int:
    """Retorna o próximo ID disponível para um novo serviço oferecido.

    Obtém o maior ID existente na lista de serviços oferecidos e incrementa em 1.
    Se não houver serviços cadastrados, retorna 1.

    Returns:
        int: ID numérico único para o próximo serviço oferecido.
    """
    if not servicos_oferecidos:
        return 1
    return max(s["id"] for s in servicos_oferecidos) + 1


def _cpf_clean(cpf: str) -> str:
    """Remove pontuação (pontos e traços) de um CPF, retornando apenas dígitos.

    Utilitário usado para normalizar a string de CPF antes de comparações
    em buscas, evitando problemas de formatação entre registros.

    Args:
        cpf: CPF no formato com pontuação (ex.: "123.456.789-00").

    Returns:
        str: CPF com apenas dígitos numéricos (ex.: "12345678900").
    """
    return cpf.replace(".", "").replace("-", "")


# ============================================================
# REPORT HELPERS
# ============================================================

def _agrupar_servicos_por_cidade() -> dict:
    """Agrupa a quantidade de serviços solicitados por cidade.

    Percorre todos os pedidos e seus serviços, contando quantos serviços
    foram realizados em cada cidade (identificada por cidade_nome|cidade_estado).

    Returns:
        dict: Mapa no formato {"Cidade|UF": quantidade_de_servicos}.
    """
    contagem: dict[str, int] = defaultdict(int)
    for pedido in pedidos:
        for serv in pedido.get("servicos", []):
            chave = f"{serv['cidade_nome']}|{serv['cidade_estado']}"
            contagem[chave] += 1
    return dict(contagem)


def _agrupar_pagamentos_por_cidade() -> dict:
    """Agrupa o valor total pago em serviços por cidade.

    Soma o preço de todos os serviços realizados em cada cidade,
    permitindo comparar o faturamento gerado por localidade.

    Returns:
        dict: Mapa no formato {"Cidade|UF": valor_total}.
    """
    totais: dict[str, float] = defaultdict(float)
    for pedido in pedidos:
        for serv in pedido.get("servicos", []):
            chave = f"{serv['cidade_nome']}|{serv['cidade_estado']}"
            totais[chave] += serv["preco"]
    return dict(totais)


def _agrupar_servicos_por_empresa() -> dict:
    """Agrupa a quantidade de serviços prestados por empresa.

    Percorre todos os pedidos contabilizando quantos serviços
    cada empresa realizou, independentemente da cidade.

    Returns:
        dict: Mapa no formato {"nome_da_empresa": quantidade_de_servicos}.
    """
    contagem: dict[str, int] = defaultdict(int)
    for pedido in pedidos:
        for serv in pedido.get("servicos", []):
            contagem[pedido["empresa"]] += 1
    return dict(contagem)


def _agrupar_receita_por_empresa() -> dict:
    """Agrupa a receita total (soma dos preços dos serviços) por empresa.

    Soma o preço de todos os serviços prestados por cada empresa,
    permitindo comparar o faturamento entre as transportadoras.

    Returns:
        dict: Mapa no formato {"nome_da_empresa": receita_total}.
    """
    totais: dict[str, float] = defaultdict(float)
    for pedido in pedidos:
        for serv in pedido.get("servicos", []):
            totais[pedido["empresa"]] += serv["preco"]
    return dict(totais)


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():
    pedidos_recentes = sorted(pedidos, key=lambda p: p["codigo"], reverse=True)[:5]
    return render_template("index.html",
                           count_empresas=len(empresas),
                           count_clientes=len(clientes),
                           count_cidades=len(cidades),
                           count_servicos=len(servicos),
                           count_pedidos=len(pedidos),
                           count_funcionarios=len(funcionarios),
                           pedidos_recentes=pedidos_recentes)


# ============================================================
# EMPRESAS CRUD
# ============================================================

@app.route("/empresas/")
def listar_empresas():
    """Exibe a listagem de todas as empresas cadastradas.

    Returns:
        str: Template HTML com a lista de empresas.
    """
    return render_template("empresas/list.html", empresas=empresas)


@app.route("/empresas/criar", methods=["GET", "POST"])
def criar_empresa():
    """Exibe formulário e processa a criação de uma nova empresa.

    No método GET, renderiza o formulário de cadastro.
    No método POST, valida os dados (nome único) e adiciona a empresa
    à lista, exibindo mensagem de sucesso ou erro.

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if any(e["nome"] == nome for e in empresas):
            flash("Já existe uma empresa com este nome.", "danger")
            return render_template("empresas/form.html", titulo="Nova Empresa",
                                   action=url_for("criar_empresa"), empresa=None)
        empresas.append({
            "nome": nome,
            "endereco": request.form["endereco"].strip(),
            "telefones": [t.strip() for t in request.form["telefones"].split(",")],
        })
        flash(f"Empresa '{nome}' criada com sucesso!", "success")
        return redirect(url_for("listar_empresas"))
    return render_template("empresas/form.html", titulo="Nova Empresa",
                           action=url_for("criar_empresa"), empresa=None)


@app.route("/empresas/<nome>/editar", methods=["GET", "POST"])
def editar_empresa(nome: str):
    """Exibe formulário e processa a edição de uma empresa existente.

    Busca a empresa pelo nome (chave natural). No GET, renderiza o
    formulário preenchido. No POST, valida unicidade do novo nome
    (se alterado) e atualiza os dados.

    Args:
        nome: Nome atual da empresa (identificador na URL).

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    empresa = next((e for e in empresas if e["nome"] == nome), None)
    if not empresa:
        flash("Empresa não encontrada.", "danger")
        return redirect(url_for("listar_empresas"))
    if request.method == "POST":
        novo_nome = request.form["nome"].strip()
        if novo_nome != nome and any(e["nome"] == novo_nome for e in empresas):
            flash("Já existe uma empresa com este nome.", "danger")
            return render_template("empresas/form.html", titulo="Editar Empresa",
                                   action=url_for("editar_empresa", nome=nome), empresa=empresa)
        empresa["nome"] = novo_nome
        empresa["endereco"] = request.form["endereco"].strip()
        empresa["telefones"] = [t.strip() for t in request.form["telefones"].split(",")]
        flash(f"Empresa '{novo_nome}' atualizada com sucesso!", "success")
        return redirect(url_for("listar_empresas"))
    return render_template("empresas/form.html", titulo="Editar Empresa",
                           action=url_for("editar_empresa", nome=nome), empresa=empresa)


@app.route("/empresas/<nome>/excluir", methods=["POST"])
def excluir_empresa(nome: str):
    """Exclui uma empresa pelo nome.

    Args:
        nome: Nome da empresa a ser removida.

    Returns:
        werkzeug.wrappers.Response: Redirecionamento para a listagem de empresas.
    """
    empresa = next((e for e in empresas if e["nome"] == nome), None)
    if empresa:
        empresas.remove(empresa)
        flash(f"Empresa '{nome}' excluída.", "success")
    else:
        flash("Empresa não encontrada.", "danger")
    return redirect(url_for("listar_empresas"))


# ============================================================
# CLIENTES CRUD
# ============================================================

@app.route("/clientes/")
def listar_clientes():
    """Exibe a listagem de todos os clientes cadastrados.

    Returns:
        str: Template HTML com a lista de clientes.
    """
    return render_template("clientes/list.html", clientes=clientes)


@app.route("/clientes/criar", methods=["GET", "POST"])
def criar_cliente():
    """Exibe formulário e processa a criação de um novo cliente.

    No método GET, renderiza o formulário de cadastro.
    No método POST, valida unicidade do código e adiciona o cliente
    à lista com todos os seus dados (CPF, RG, endereço, telefones).

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    if request.method == "POST":
        codigo = int(request.form["codigo"])
        if any(c["codigo"] == codigo for c in clientes):
            flash("Já existe um cliente com este código.", "danger")
            return render_template("clientes/form.html", titulo="Novo Cliente",
                                   action=url_for("criar_cliente"), cliente=None)
        clientes.append({
            "codigo": codigo,
            "nome_completo": request.form["nome_completo"].strip(),
            "cpf": request.form["cpf"].strip(),
            "rg": request.form["rg"].strip(),
            "endereco": request.form["endereco"].strip(),
            "telefones": [t.strip() for t in request.form["telefones"].split(",")],
        })
        flash("Cliente criado com sucesso!", "success")
        return redirect(url_for("listar_clientes"))
    return render_template("clientes/form.html", titulo="Novo Cliente",
                           action=url_for("criar_cliente"), cliente=None)


@app.route("/clientes/<int:codigo>/editar", methods=["GET", "POST"])
def editar_cliente(codigo: int):
    """Exibe formulário e processa a edição de um cliente existente.

    Busca o cliente pelo código numérico. No GET, renderiza o formulário
    preenchido. No POST, valida unicidade do novo código (se alterado) e
    atualiza todos os dados do cliente.

    Args:
        codigo: Código atual do cliente (identificador na URL).

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    cliente = next((c for c in clientes if c["codigo"] == codigo), None)
    if not cliente:
        flash("Cliente não encontrado.", "danger")
        return redirect(url_for("listar_clientes"))
    if request.method == "POST":
        novo_codigo = int(request.form["codigo"])
        if novo_codigo != codigo and any(c["codigo"] == novo_codigo for c in clientes):
            flash("Já existe um cliente com este código.", "danger")
            return render_template("clientes/form.html", titulo="Editar Cliente",
                                   action=url_for("editar_cliente", codigo=codigo), cliente=cliente)
        cliente["codigo"] = novo_codigo
        cliente["nome_completo"] = request.form["nome_completo"].strip()
        cliente["cpf"] = request.form["cpf"].strip()
        cliente["rg"] = request.form["rg"].strip()
        cliente["endereco"] = request.form["endereco"].strip()
        cliente["telefones"] = [t.strip() for t in request.form["telefones"].split(",")]
        flash("Cliente atualizado com sucesso!", "success")
        return redirect(url_for("listar_clientes"))
    return render_template("clientes/form.html", titulo="Editar Cliente",
                           action=url_for("editar_cliente", codigo=codigo), cliente=cliente)


@app.route("/clientes/<int:codigo>/excluir", methods=["POST"])
def excluir_cliente(codigo: int):
    """Exclui um cliente pelo código.

    Args:
        codigo: Código do cliente a ser removido.

    Returns:
        werkzeug.wrappers.Response: Redirecionamento para a listagem de clientes.
    """
    cliente = next((c for c in clientes if c["codigo"] == codigo), None)
    if cliente:
        clientes.remove(cliente)
        flash("Cliente excluído.", "success")
    else:
        flash("Cliente não encontrado.", "danger")
    return redirect(url_for("listar_clientes"))


# ============================================================
# CIDADES CRUD
# ============================================================

@app.route("/cidades/")
def listar_cidades():
    """Exibe a listagem de todas as cidades cadastradas.

    Returns:
        str: Template HTML com a lista de cidades.
    """
    return render_template("cidades/list.html", cidades=cidades)


@app.route("/cidades/criar", methods=["GET", "POST"])
def criar_cidade():
    """Exibe formulário e processa a criação de uma nova cidade.

    No método GET, renderiza o formulário de cadastro.
    No método POST, valida se a combinação nome+estado já existe
    e adiciona a nova cidade. O estado é convertido para maiúsculas.

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    if request.method == "POST":
        nome = request.form["nome"].strip()
        estado = request.form["estado"].strip().upper()
        if any(c["nome"] == nome and c["estado"] == estado for c in cidades):
            flash("Esta cidade já está cadastrada.", "danger")
            return render_template("cidades/form.html", titulo="Nova Cidade",
                                   action=url_for("criar_cidade"), cidade=None)
        cidades.append({"nome": nome, "estado": estado})
        flash(f"Cidade '{nome}/{estado}' criada!", "success")
        return redirect(url_for("listar_cidades"))
    return render_template("cidades/form.html", titulo="Nova Cidade",
                           action=url_for("criar_cidade"), cidade=None)


@app.route("/cidades/<nome>/<estado>/editar", methods=["GET", "POST"])
def editar_cidade(nome: str, estado: str):
    """Exibe formulário e processa a edição de uma cidade existente.

    Busca a cidade pela combinação nome + estado. No GET, renderiza o
    formulário preenchido. No POST, valida unicidade da nova combinação
    (se alterada) e atualiza os dados. O estado é convertido para maiúsculas.

    Args:
        nome: Nome atual da cidade.
        estado: Sigla do estado (UF) atual.

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    cidade = next((c for c in cidades if c["nome"] == nome and c["estado"] == estado), None)
    if not cidade:
        flash("Cidade não encontrada.", "danger")
        return redirect(url_for("listar_cidades"))
    if request.method == "POST":
        novo_nome = request.form["nome"].strip()
        novo_estado = request.form["estado"].strip().upper()
        if (novo_nome != nome or novo_estado != estado) and \
           any(c["nome"] == novo_nome and c["estado"] == novo_estado for c in cidades):
            flash("Esta cidade já está cadastrada.", "danger")
            return render_template("cidades/form.html", titulo="Editar Cidade",
                                   action=url_for("editar_cidade", nome=nome, estado=estado),
                                   cidade=cidade)
        cidade["nome"] = novo_nome
        cidade["estado"] = novo_estado
        flash(f"Cidade '{novo_nome}/{novo_estado}' atualizada!", "success")
        return redirect(url_for("listar_cidades"))
    return render_template("cidades/form.html", titulo="Editar Cidade",
                           action=url_for("editar_cidade", nome=nome, estado=estado),
                           cidade=cidade)


@app.route("/cidades/<nome>/<estado>/excluir", methods=["POST"])
def excluir_cidade(nome: str, estado: str):
    """Exclui uma cidade pela combinação nome + estado.

    Args:
        nome: Nome da cidade a ser removida.
        estado: Sigla do estado (UF) da cidade a ser removida.

    Returns:
        werkzeug.wrappers.Response: Redirecionamento para a listagem de cidades.
    """
    cidade = next((c for c in cidades if c["nome"] == nome and c["estado"] == estado), None)
    if cidade:
        cidades.remove(cidade)
        flash(f"Cidade '{nome}/{estado}' excluída.", "success")
    else:
        flash("Cidade não encontrada.", "danger")
    return redirect(url_for("listar_cidades"))


# ============================================================
# SERVIÇOS CRUD
# ============================================================

@app.route("/servicos/")
def listar_servicos():
    """Exibe a listagem de todos os tipos de serviço cadastrados.

    Returns:
        str: Template HTML com a lista de serviços.
    """
    return render_template("servicos/list.html", servicos=servicos)


@app.route("/servicos/criar", methods=["GET", "POST"])
def criar_servico():
    """Exibe formulário e processa a criação de um novo tipo de serviço.

    No método GET, renderiza o formulário de cadastro.
    No método POST, valida se o nome do serviço já existe e o adiciona.

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if any(s["nome"] == nome for s in servicos):
            flash("Este serviço já existe.", "danger")
            return render_template("servicos/form.html", titulo="Novo Serviço",
                                   action=url_for("criar_servico"), servico=None)
        servicos.append({"nome": nome})
        flash(f"Serviço '{nome}' criado!", "success")
        return redirect(url_for("listar_servicos"))
    return render_template("servicos/form.html", titulo="Novo Serviço",
                           action=url_for("criar_servico"), servico=None)


@app.route("/servicos/<nome>/editar", methods=["GET", "POST"])
def editar_servico(nome: str):
    """Exibe formulário e processa a edição de um tipo de serviço.

    Busca o serviço pelo nome. No GET, renderiza o formulário preenchido.
    No POST, valida unicidade do novo nome (se alterado) e atualiza.

    Args:
        nome: Nome atual do serviço (identificador na URL).

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    servico = next((s for s in servicos if s["nome"] == nome), None)
    if not servico:
        flash("Serviço não encontrado.", "danger")
        return redirect(url_for("listar_servicos"))
    if request.method == "POST":
        novo_nome = request.form["nome"].strip()
        if novo_nome != nome and any(s["nome"] == novo_nome for s in servicos):
            flash("Este serviço já existe.", "danger")
            return render_template("servicos/form.html", titulo="Editar Serviço",
                                   action=url_for("editar_servico", nome=nome), servico=servico)
        servico["nome"] = novo_nome
        flash(f"Serviço '{novo_nome}' atualizado!", "success")
        return redirect(url_for("listar_servicos"))
    return render_template("servicos/form.html", titulo="Editar Serviço",
                           action=url_for("editar_servico", nome=nome), servico=servico)


@app.route("/servicos/<nome>/excluir", methods=["POST"])
def excluir_servico(nome: str):
    """Exclui um tipo de serviço pelo nome.

    Args:
        nome: Nome do serviço a ser removido.

    Returns:
        werkzeug.wrappers.Response: Redirecionamento para a listagem de serviços.
    """
    servico = next((s for s in servicos if s["nome"] == nome), None)
    if servico:
        servicos.remove(servico)
        flash(f"Serviço '{nome}' excluído.", "success")
    else:
        flash("Serviço não encontrado.", "danger")
    return redirect(url_for("listar_servicos"))


# ============================================================
# PEDIDOS CRUD
# ============================================================

@app.route("/pedidos/")
def listar_pedidos():
    """Exibe a listagem de pedidos ordenados do mais recente para o mais antigo.

    Returns:
        str: Template HTML com a lista de pedidos (ordenados por código decrescente).
    """
    pedidos_ordenados = sorted(pedidos, key=lambda p: p["codigo"], reverse=True)
    return render_template("pedidos/list.html", pedidos=pedidos_ordenados)


@app.route("/pedidos/criar", methods=["GET", "POST"])
def criar_pedido():
    """Exibe formulário e processa a criação de um novo pedido.

    No método GET, renderiza o formulário com listas de clientes, empresas,
    serviços disponíveis e cidades para seleção.

    No método POST, processa os dados do pedido incluindo múltiplos serviços
    (enviados como listas paralelas via campos com sufixo `[]`). Cada serviço
    tem nome, preço, endereços, cidade, data e tempo gasto. O preço total é
    calculado somando o preço de todos os serviços.

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    if request.method == "POST":
        codigo = int(request.form["codigo"])
        if any(p["codigo"] == codigo for p in pedidos):
            flash("Já existe um pedido com este código.", "danger")
            return render_template("pedidos/form.html", titulo="Novo Pedido",
                                   action=url_for("criar_pedido"),
                                   pedido=None, clientes=clientes, empresas=empresas,
                                   servicos_disponiveis=servicos, cidades_lista=cidades)

        # Coleta listas paralelas de serviços vindas do formulário dinâmico
        servicos_nomes = request.form.getlist("servico_nome[]")
        servicos_precos = request.form.getlist("servico_preco[]")
        servicos_partidas = request.form.getlist("servico_partida[]")
        servicos_destinos = request.form.getlist("servico_destino[]")
        servicos_cidades = request.form.getlist("servico_cidade[]")
        servicos_datas = request.form.getlist("servico_data[]")
        servicos_tempos = request.form.getlist("servico_tempo[]")

        # Monta a lista de serviços do pedido e calcula o preço total
        servicos_pedido = []
        preco_total = 0.0
        for i in range(len(servicos_nomes)):
            preco = float(servicos_precos[i])
            # A cidade é recebida no formato "nome|uf" e é desmembrada
            cidade_parts = servicos_cidades[i].split("|")
            cidade_nome = cidade_parts[0] if len(cidade_parts) > 0 else ""
            cidade_estado = cidade_parts[1] if len(cidade_parts) > 1 else ""
            servicos_pedido.append({
                "servico": servicos_nomes[i],
                "preco": preco,
                "endereco_partida": servicos_partidas[i],
                "endereco_destino": servicos_destinos[i] if servicos_destinos[i] else "",
                "cidade_nome": cidade_nome,
                "cidade_estado": cidade_estado,
                "data_realizacao": servicos_datas[i],
                "tempo_gasto": float(servicos_tempos[i]),
            })
            preco_total += preco

        pedidos.append({
            "codigo": codigo,
            "cliente": request.form["cliente"],
            "empresa": request.form["empresa"],
            "data_solicitacao": request.form["data_solicitacao"],
            "data_resolucao": request.form.get("data_resolucao", ""),
            "status": request.form["status"],
            "preco_total": preco_total,
            "servicos": servicos_pedido,
        })
        flash(f"Pedido #{codigo} criado com sucesso!", "success")
        return redirect(url_for("listar_pedidos"))

    return render_template("pedidos/form.html", titulo="Novo Pedido",
                           action=url_for("criar_pedido"),
                           pedido=None, clientes=clientes, empresas=empresas,
                           servicos_disponiveis=servicos, cidades_lista=cidades)


@app.route("/pedidos/<int:codigo>")
def detalhes_pedido(codigo: int):
    """Exibe os detalhes completos de um pedido específico.

    Args:
        codigo: Código do pedido a ser visualizado.

    Returns:
        str: Template HTML com os detalhes do pedido, ou redirecionamento
             para listagem se o pedido não for encontrado.
    """
    pedido = next((p for p in pedidos if p["codigo"] == codigo), None)
    if not pedido:
        flash("Pedido não encontrado.", "danger")
        return redirect(url_for("listar_pedidos"))
    return render_template("pedidos/detail.html", pedido=pedido)


@app.route("/pedidos/<int:codigo>/editar", methods=["GET", "POST"])
def editar_pedido(codigo: int):
    """Exibe formulário e processa a edição de um pedido existente.

    Busca o pedido pelo código. No GET, renderiza o formulário preenchido.
    No POST, valida unicidade do novo código (se alterado), recalcula o
    preço total a partir dos serviços informados (listas paralelas) e
    atualiza todos os campos do pedido.

    Args:
        codigo: Código atual do pedido (identificador na URL).

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    pedido = next((p for p in pedidos if p["codigo"] == codigo), None)
    if not pedido:
        flash("Pedido não encontrado.", "danger")
        return redirect(url_for("listar_pedidos"))
    if request.method == "POST":
        novo_codigo = int(request.form["codigo"])
        if novo_codigo != codigo and any(p["codigo"] == novo_codigo for p in pedidos):
            flash("Já existe um pedido com este código.", "danger")
            return render_template("pedidos/form.html", titulo="Editar Pedido",
                                   action=url_for("editar_pedido", codigo=codigo),
                                   pedido=pedido, clientes=clientes, empresas=empresas,
                                   servicos_disponiveis=servicos, cidades_lista=cidades)

        # Coleta listas paralelas de serviços do formulário dinâmico
        servicos_nomes = request.form.getlist("servico_nome[]")
        servicos_precos = request.form.getlist("servico_preco[]")
        servicos_partidas = request.form.getlist("servico_partida[]")
        servicos_destinos = request.form.getlist("servico_destino[]")
        servicos_cidades = request.form.getlist("servico_cidade[]")
        servicos_datas = request.form.getlist("servico_data[]")
        servicos_tempos = request.form.getlist("servico_tempo[]")

        # Reconstrói a lista de serviços e recalcula o total
        servicos_pedido = []
        preco_total = 0.0
        for i in range(len(servicos_nomes)):
            preco = float(servicos_precos[i])
            cidade_parts = servicos_cidades[i].split("|")
            cidade_nome = cidade_parts[0] if len(cidade_parts) > 0 else ""
            cidade_estado = cidade_parts[1] if len(cidade_parts) > 1 else ""
            servicos_pedido.append({
                "servico": servicos_nomes[i],
                "preco": preco,
                "endereco_partida": servicos_partidas[i],
                "endereco_destino": servicos_destinos[i] if servicos_destinos[i] else "",
                "cidade_nome": cidade_nome,
                "cidade_estado": cidade_estado,
                "data_realizacao": servicos_datas[i],
                "tempo_gasto": float(servicos_tempos[i]),
            })
            preco_total += preco

        pedido["codigo"] = novo_codigo
        pedido["cliente"] = request.form["cliente"]
        pedido["empresa"] = request.form["empresa"]
        pedido["data_solicitacao"] = request.form["data_solicitacao"]
        pedido["data_resolucao"] = request.form.get("data_resolucao", "")
        pedido["status"] = request.form["status"]
        pedido["preco_total"] = preco_total
        pedido["servicos"] = servicos_pedido
        flash(f"Pedido #{novo_codigo} atualizado!", "success")
        return redirect(url_for("listar_pedidos"))

    return render_template("pedidos/form.html", titulo="Editar Pedido",
                           action=url_for("editar_pedido", codigo=codigo),
                           pedido=pedido, clientes=clientes, empresas=empresas,
                           servicos_disponiveis=servicos, cidades_lista=cidades)


@app.route("/pedidos/<int:codigo>/excluir", methods=["POST"])
def excluir_pedido(codigo: int):
    """Exclui um pedido pelo código.

    Args:
        codigo: Código do pedido a ser removido.

    Returns:
        werkzeug.wrappers.Response: Redirecionamento para a listagem de pedidos.
    """
    pedido = next((p for p in pedidos if p["codigo"] == codigo), None)
    if pedido:
        pedidos.remove(pedido)
        flash(f"Pedido #{codigo} excluído.", "success")
    else:
        flash("Pedido não encontrado.", "danger")
    return redirect(url_for("listar_pedidos"))


# ============================================================
# FUNCIONÁRIOS CRUD
# ============================================================

@app.route("/funcionarios/")
def listar_funcionarios():
    """Exibe a listagem de todos os funcionários cadastrados.

    Returns:
        str: Template HTML com a lista de funcionários.
    """
    return render_template("funcionarios/list.html", funcionarios=funcionarios)


@app.route("/funcionarios/criar", methods=["GET", "POST"])
def criar_funcionario():
    """Exibe formulário e processa a criação de um novo funcionário.

    No método GET, renderiza o formulário de cadastro.
    No método POST, valida unicidade do CPF e adiciona o funcionário
    com dados pessoais, tipo, salário e empresas vinculadas.

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    if request.method == "POST":
        cpf = request.form["cpf"].strip()
        if any(f["cpf"] == cpf for f in funcionarios):
            flash("Já existe um funcionário com este CPF.", "danger")
            return render_template("funcionarios/form.html", titulo="Novo Funcionário",
                                   action=url_for("criar_funcionario"), func=None)
        funcionarios.append({
            "cpf": cpf,
            "rg": request.form["rg"].strip(),
            "endereco": request.form["endereco"].strip(),
            "nome_completo": request.form["nome_completo"].strip(),
            "tipo": request.form["tipo"],
            "salario": float(request.form["salario"]),
            "empresas": [e.strip() for e in request.form["empresas"].split(",")],
        })
        flash("Funcionário criado com sucesso!", "success")
        return redirect(url_for("listar_funcionarios"))
    return render_template("funcionarios/form.html", titulo="Novo Funcionário",
                           action=url_for("criar_funcionario"), func=None)


@app.route("/funcionarios/<cpf>/editar", methods=["GET", "POST"])
def editar_funcionario(cpf: str):
    """Exibe formulário e processa a edição de um funcionário existente.

    Busca o funcionário pelo CPF (a URL pode conter CPF sem pontuação,
    por isso a busca usa _cpf_clean para normalizar). No GET, renderiza
    o formulário preenchido. No POST, valida unicidade do novo CPF
    (se alterado) e atualiza os dados.

    Args:
        cpf: CPF do funcionário (com ou sem pontuação).

    Returns:
        str: Template do formulário (GET) ou redirecionamento para listagem (POST).
    """
    # CPF may come without dots/dashes in URL
    func = next((f for f in funcionarios if _cpf_clean(f["cpf"]) == cpf), None)
    if not func:
        flash("Funcionário não encontrado.", "danger")
        return redirect(url_for("listar_funcionarios"))
    if request.method == "POST":
        novo_cpf = request.form["cpf"].strip()
        if _cpf_clean(novo_cpf) != cpf and any(f["cpf"] == novo_cpf for f in funcionarios):
            flash("Já existe um funcionário com este CPF.", "danger")
            return render_template("funcionarios/form.html", titulo="Editar Funcionário",
                                   action=url_for("editar_funcionario", cpf=cpf), func=func)
        func["cpf"] = novo_cpf
        func["rg"] = request.form["rg"].strip()
        func["endereco"] = request.form["endereco"].strip()
        func["nome_completo"] = request.form["nome_completo"].strip()
        func["tipo"] = request.form["tipo"]
        func["salario"] = float(request.form["salario"])
        func["empresas"] = [e.strip() for e in request.form["empresas"].split(",")]
        flash("Funcionário atualizado com sucesso!", "success")
        return redirect(url_for("listar_funcionarios"))
    return render_template("funcionarios/form.html", titulo="Editar Funcionário",
                           action=url_for("editar_funcionario", cpf=cpf), func=func)


@app.route("/funcionarios/<cpf>/excluir", methods=["POST"])
def excluir_funcionario(cpf: str):
    """Exclui um funcionário pelo CPF.

    A busca também usa _cpf_clean para normalizar, garantindo que a
    remoção funcione independentemente da formatação do CPF na URL.

    Args:
        cpf: CPF do funcionário a ser removido (com ou sem pontuação).

    Returns:
        werkzeug.wrappers.Response: Redirecionamento para a listagem de funcionários.
    """
    func = next((f for f in funcionarios if _cpf_clean(f["cpf"]) == cpf), None)
    if func:
        funcionarios.remove(func)
        flash("Funcionário excluído.", "success")
    else:
        flash("Funcionário não encontrado.", "danger")
    return redirect(url_for("listar_funcionarios"))


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404


# ============================================================
# RELATÓRIOS
# ============================================================

@app.route("/relatorios/")
def relatorios():
    """Exibe a página inicial com a lista de relatórios disponíveis.

    Returns:
        str: Template HTML com o índice de relatórios.
    """
    return render_template("relatorios/index.html")


@app.route("/relatorios/histograma-servicos")
def rel_histograma_servicos():
    """Gera histograma com a quantidade de serviços por cidade.

    Agrupa os serviços de todos os pedidos por cidade e retorna os
    dados ordenados alfabeticamente para renderização em gráfico.

    Returns:
        str: Template HTML com labels (cidades) e valores (quantidade de serviços).
    """
    dados = _agrupar_servicos_por_cidade()
    labels = sorted(dados.keys())
    valores = [dados[k] for k in labels]
    # Formata o label como "Cidade/Estado" (substituindo o pipe usado como chave interna)
    labels_fmt = [k.replace("|", "/") for k in labels]
    return render_template("relatorios/histograma_servicos.html",
                           dados={"labels": labels_fmt, "valores": valores})


@app.route("/relatorios/histograma-pagamentos")
def rel_histograma_pagamentos():
    """Gera histograma com o valor total de pagamentos por cidade.

    Agrupa a soma dos preços dos serviços por cidade e retorna os
    dados ordenados alfabeticamente para renderização em gráfico.

    Returns:
        str: Template HTML com labels (cidades) e valores (total em R$).
    """
    dados = _agrupar_pagamentos_por_cidade()
    labels = sorted(dados.keys())
    valores = [dados[k] for k in labels]
    labels_fmt = [k.replace("|", "/") for k in labels]
    return render_template("relatorios/histograma_pagamentos.html",
                           dados={"labels": labels_fmt, "valores": valores})


@app.route("/relatorios/top5-cidades-valor")
def rel_top5_cidades_valor():
    """Exibe o ranking das 5 cidades com maior valor total em serviços.

    Ordena as cidades pelo valor total pago (decrescente) e limita
    ao top 5. Desmembra a chave "Cidade|UF" em campos separados.

    Returns:
        str: Template HTML com lista das 5 cidades e seus valores.
    """
    dados = _agrupar_pagamentos_por_cidade()
    sorted_items = sorted(dados.items(), key=lambda x: x[1], reverse=True)[:5]
    resultado = []
    for chave, valor in sorted_items:
        cidade, estado = chave.split("|")
        resultado.append({"cidade": cidade, "estado": estado, "valor": valor})
    return render_template("relatorios/top5_cidades_valor.html", dados=resultado)


@app.route("/relatorios/top5-cidades-servicos")
def rel_top5_cidades_servicos():
    """Exibe o ranking das 5 cidades com maior quantidade de serviços.

    Ordena as cidades pela quantidade de serviços (decrescente) e
    limita ao top 5. Desmembra a chave "Cidade|UF" em campos separados.

    Returns:
        str: Template HTML com lista das 5 cidades e suas quantidades.
    """
    dados = _agrupar_servicos_por_cidade()
    sorted_items = sorted(dados.items(), key=lambda x: x[1], reverse=True)[:5]
    resultado = []
    for chave, qtd in sorted_items:
        cidade, estado = chave.split("|")
        resultado.append({"cidade": cidade, "estado": estado, "quantidade": qtd})
    return render_template("relatorios/top5_cidades_servicos.html", dados=resultado)


@app.route("/relatorios/top5-empresas-servicos")
def rel_top5_empresas_servicos():
    """Exibe o ranking das 5 empresas com maior quantidade de serviços prestados.

    Ordena as empresas pela quantidade de serviços (decrescente) e
    limita ao top 5.

    Returns:
        str: Template HTML com lista das 5 empresas e suas quantidades.
    """
    dados = _agrupar_servicos_por_empresa()
    sorted_items = sorted(dados.items(), key=lambda x: x[1], reverse=True)[:5]
    resultado = [{"empresa": empresa, "quantidade": qtd} for empresa, qtd in sorted_items]
    return render_template("relatorios/top5_empresas_servicos.html", dados=resultado)


@app.route("/relatorios/top5-empresas-receita")
def rel_top5_empresas_receita():
    """Exibe o ranking das 5 empresas com maior receita total.

    Ordena as empresas pelo valor total recebido (decrescente) e
    limita ao top 5.

    Returns:
        str: Template HTML com lista das 5 empresas e seus valores.
    """
    dados = _agrupar_receita_por_empresa()
    sorted_items = sorted(dados.items(), key=lambda x: x[1], reverse=True)[:5]
    resultado = [{"empresa": empresa, "valor": valor} for empresa, valor in sorted_items]
    return render_template("relatorios/top5_empresas_receita.html", dados=resultado)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    """Ponto de entrada da aplicação Flask.

    Inicia o servidor de desenvolvimento no endereço 0.0.0.0:5000
    com modo debug ativado, permitindo recarga automática em alterações.
    """
    app.run(debug=True, host="0.0.0.0", port=5000)
