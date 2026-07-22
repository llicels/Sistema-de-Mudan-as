from flask import Flask, render_template, request, redirect, url_for, flash

from models import empresas as model_empresas
from models import clientes as model_clientes
from models import cidades as model_cidades
from models import servicos as model_servicos
from models import oferecem as model_oferecem
from models import funcionarios as model_funcionarios
from models import pedidos as model_pedidos
from db import query as db_query

app = Flask(__name__)
app.secret_key = 'backrooms-mudancas-2026-secret-key'


def _cpf_clean(cpf: str) -> str:
    return cpf.replace(".", "").replace("-", "")


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():
    empresas = model_empresas.listar()
    clientes = model_clientes.listar()
    cidades = model_cidades.listar()
    servicos = model_servicos.listar()
    funcionarios = model_funcionarios.listar()
    pedidos_lista = model_pedidos.listar()
    return render_template("index.html",
                           count_empresas=len(empresas),
                           count_clientes=len(clientes),
                           count_cidades=len(cidades),
                           count_servicos=len(servicos),
                           count_pedidos=len(pedidos_lista),
                           count_funcionarios=len(funcionarios),
                           pedidos_recentes=pedidos_lista[:5])


# ============================================================
# EMPRESAS CRUD
# ============================================================

@app.route("/empresas/")
def listar_empresas():
    return render_template("empresas/list.html", empresas=model_empresas.listar())


@app.route("/empresas/criar", methods=["GET", "POST"])
def criar_empresa():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if any(e["nome"] == nome for e in model_empresas.listar_simples()):
            flash("Já existe uma empresa com este nome.", "danger")
            return render_template("empresas/form.html", titulo="Nova Empresa",
                                   action=url_for("criar_empresa"), empresa=None)
        telefones = request.form.getlist("telefones[]")
        model_empresas.criar(nome, request.form["endereco"].strip(), telefones)
        flash(f"Empresa '{nome}' criada!", "success")
        return redirect(url_for("listar_empresas"))
    return render_template("empresas/form.html", titulo="Nova Empresa",
                           action=url_for("criar_empresa"), empresa=None)


@app.route("/empresas/<int:id_empresa>/editar", methods=["GET", "POST"])
def editar_empresa(id_empresa: int):
    empresa = model_empresas.buscar(id_empresa)
    if not empresa:
        flash("Empresa não encontrada.", "danger")
        return redirect(url_for("listar_empresas"))
    if request.method == "POST":
        novo_nome = request.form["nome"].strip()
        if novo_nome != empresa["nome"] and \
           any(e["nome"] == novo_nome for e in model_empresas.listar_simples()):
            flash("Já existe uma empresa com este nome.", "danger")
            return render_template("empresas/form.html", titulo="Editar Empresa",
                                   action=url_for("editar_empresa", id_empresa=id_empresa),
                                   empresa=empresa)
        telefones = request.form.getlist("telefones[]")
        model_empresas.atualizar(id_empresa, novo_nome,
                                 request.form["endereco"].strip(), telefones)
        flash(f"Empresa '{novo_nome}' atualizada!", "success")
        return redirect(url_for("listar_empresas"))
    return render_template("empresas/form.html", titulo="Editar Empresa",
                           action=url_for("editar_empresa", id_empresa=id_empresa),
                           empresa=empresa)


@app.route("/empresas/<int:id_empresa>/excluir", methods=["POST"])
def excluir_empresa(id_empresa: int):
    model_empresas.excluir(id_empresa)
    flash("Empresa excluída.", "success")
    return redirect(url_for("listar_empresas"))


# ============================================================
# CLIENTES CRUD
# ============================================================

@app.route("/clientes/")
def listar_clientes():
    return render_template("clientes/list.html", clientes=model_clientes.listar())


@app.route("/clientes/criar", methods=["GET", "POST"])
def criar_cliente():
    if request.method == "POST":
        cpf = request.form["cpf"].strip()
        if any(c["cpf"] == cpf for c in model_clientes.listar()):
            flash("Já existe um cliente com este CPF.", "danger")
            return render_template("clientes/form.html", titulo="Novo Cliente",
                                   action=url_for("criar_cliente"), cliente=None)
        telefones = request.form.getlist("telefones[]")
        model_clientes.criar(cpf, request.form["rg"].strip(),
                             request.form["endereco"].strip(),
                             request.form["nome_completo"].strip(), telefones)
        flash("Cliente criado!", "success")
        return redirect(url_for("listar_clientes"))
    return render_template("clientes/form.html", titulo="Novo Cliente",
                           action=url_for("criar_cliente"), cliente=None)


@app.route("/clientes/<int:cod_cliente>/editar", methods=["GET", "POST"])
def editar_cliente(cod_cliente: int):
    cliente = model_clientes.buscar(cod_cliente)
    if not cliente:
        flash("Cliente não encontrado.", "danger")
        return redirect(url_for("listar_clientes"))
    if request.method == "POST":
        novo_cpf = request.form["cpf"].strip()
        if novo_cpf != cliente["cpf"] and \
           any(c["cpf"] == novo_cpf for c in model_clientes.listar()):
            flash("Já existe um cliente com este CPF.", "danger")
            return render_template("clientes/form.html", titulo="Editar Cliente",
                                   action=url_for("editar_cliente", cod_cliente=cod_cliente),
                                   cliente=cliente)
        telefones = request.form.getlist("telefones[]")
        model_clientes.atualizar(cod_cliente, novo_cpf,
                                 request.form["rg"].strip(),
                                 request.form["endereco"].strip(),
                                 request.form["nome_completo"].strip(), telefones)
        flash("Cliente atualizado!", "success")
        return redirect(url_for("listar_clientes"))
    return render_template("clientes/form.html", titulo="Editar Cliente",
                           action=url_for("editar_cliente", cod_cliente=cod_cliente),
                           cliente=cliente)


@app.route("/clientes/<int:cod_cliente>/excluir", methods=["POST"])
def excluir_cliente(cod_cliente: int):
    model_clientes.excluir(cod_cliente)
    flash("Cliente excluído.", "success")
    return redirect(url_for("listar_clientes"))


# ============================================================
# CIDADES CRUD
# ============================================================

@app.route("/cidades/")
def listar_cidades():
    return render_template("cidades/list.html", cidades=model_cidades.listar())


@app.route("/cidades/criar", methods=["GET", "POST"])
def criar_cidade():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        estado = request.form["estado"].strip().upper()
        if model_cidades.buscar(nome, estado):
            flash("Esta cidade já está cadastrada.", "danger")
            return render_template("cidades/form.html", titulo="Nova Cidade",
                                   action=url_for("criar_cidade"), cidade=None)
        model_cidades.criar(nome, estado)
        flash(f"Cidade '{nome}/{estado}' criada!", "success")
        return redirect(url_for("listar_cidades"))
    return render_template("cidades/form.html", titulo="Nova Cidade",
                           action=url_for("criar_cidade"), cidade=None)


@app.route("/cidades/<nome>/<estado>/editar", methods=["GET", "POST"])
def editar_cidade(nome: str, estado: str):
    cidade = model_cidades.buscar(nome, estado)
    if not cidade:
        flash("Cidade não encontrada.", "danger")
        return redirect(url_for("listar_cidades"))
    if request.method == "POST":
        novo_nome = request.form["nome"].strip()
        novo_estado = request.form["estado"].strip().upper()
        if (novo_nome != nome or novo_estado != estado) and \
           model_cidades.buscar(novo_nome, novo_estado):
            flash("Esta cidade já está cadastrada.", "danger")
            return render_template("cidades/form.html", titulo="Editar Cidade",
                                   action=url_for("editar_cidade", nome=nome, estado=estado),
                                   cidade=cidade)
        model_cidades.atualizar(nome, estado, novo_nome, novo_estado)
        flash(f"Cidade '{novo_nome}/{novo_estado}' atualizada!", "success")
        return redirect(url_for("listar_cidades"))
    return render_template("cidades/form.html", titulo="Editar Cidade",
                           action=url_for("editar_cidade", nome=nome, estado=estado),
                           cidade=cidade)


@app.route("/cidades/<nome>/<estado>/excluir", methods=["POST"])
def excluir_cidade(nome: str, estado: str):
    model_cidades.excluir(nome, estado)
    flash(f"Cidade '{nome}/{estado}' excluída.", "success")
    return redirect(url_for("listar_cidades"))


# ============================================================
# SERVICOS CRUD
# ============================================================

@app.route("/servicos/")
def listar_servicos():
    return render_template("servicos/list.html", servicos=model_servicos.listar())


@app.route("/servicos/criar", methods=["GET", "POST"])
def criar_servico():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if model_servicos.buscar(nome):
            flash("Este serviço já existe.", "danger")
            return render_template("servicos/form.html", titulo="Novo Serviço",
                                   action=url_for("criar_servico"), servico=None)
        tipo = request.form["tipo"]
        if tipo == "TRANSPORTE":
            limites = request.form.getlist("acr_limite[]")
            pcts = request.form.getlist("acr_percentual[]")
            acrescimos = list(zip(limites, pcts))
            model_servicos.criar_transporte(nome, float(request.form["limite_carga"]), acrescimos)
        elif tipo == "GUINDASTE":
            model_servicos.criar_guindaste(nome, float(request.form["tamanho_base"]),
                                           float(request.form["altura"]),
                                           float(request.form.get("bonus_aumento", 0)))
        else:
            model_servicos.criar_simples(nome)
        flash(f"Serviço '{nome}' criado!", "success")
        return redirect(url_for("listar_servicos"))
    return render_template("servicos/form.html", titulo="Novo Serviço",
                           action=url_for("criar_servico"), servico=None)


@app.route("/servicos/<nome>/editar", methods=["GET", "POST"])
def editar_servico(nome: str):
    servico = model_servicos.buscar(nome)
    if not servico:
        flash("Serviço não encontrado.", "danger")
        return redirect(url_for("listar_servicos"))
    if request.method == "POST":
        novo_nome = request.form["nome"].strip()
        if novo_nome != nome and model_servicos.buscar(novo_nome):
            flash("Este serviço já existe.", "danger")
            return render_template("servicos/form.html", titulo="Editar Serviço",
                                   action=url_for("editar_servico", nome=nome), servico=servico)
        tipo = request.form["tipo"]
        if tipo == "TRANSPORTE":
            limites = request.form.getlist("acr_limite[]")
            pcts = request.form.getlist("acr_percentual[]")
            acrescimos = list(zip(limites, pcts))
            model_servicos.atualizar_transporte(nome, novo_nome,
                                                float(request.form["limite_carga"]), acrescimos)
        elif tipo == "GUINDASTE":
            model_servicos.atualizar_guindaste(nome, novo_nome,
                                               float(request.form["tamanho_base"]),
                                               float(request.form["altura"]),
                                               float(request.form.get("bonus_aumento", 0)))
        else:
            model_servicos.atualizar_simples(nome, novo_nome)
        flash(f"Serviço '{novo_nome}' atualizado!", "success")
        return redirect(url_for("listar_servicos"))
    return render_template("servicos/form.html", titulo="Editar Serviço",
                           action=url_for("editar_servico", nome=nome), servico=servico)


@app.route("/servicos/<nome>/excluir", methods=["POST"])
def excluir_servico(nome: str):
    model_servicos.excluir(nome)
    flash(f"Serviço '{nome}' excluído.", "success")
    return redirect(url_for("listar_servicos"))


# ============================================================
# OFERECEM CRUD
# ============================================================

@app.route("/oferecem/")
def listar_oferecem():
    return render_template("oferecem/list.html", oferecimentos=model_oferecem.listar())


@app.route("/oferecem/criar", methods=["GET", "POST"])
def criar_oferecem():
    if request.method == "POST":
        model_oferecem.criar(int(request.form["id_empresa"]),
                             request.form["nome_cidade"].strip(),
                             request.form["nome_servico"].strip(),
                             float(request.form["preco_hora"]))
        flash("Serviço oferecido cadastrado!", "success")
        return redirect(url_for("listar_oferecem"))
    return render_template("oferecem/form.html", titulo="Novo Oferecimento",
                           action=url_for("criar_oferecem"), item=None,
                           empresas=model_empresas.listar_simples(),
                           servicos=model_servicos.listar_simples(),
                           cidades=model_cidades.listar_simples())


@app.route("/oferecem/<int:id_empresa>/<nome_cidade>/<nome_servico>/editar",
           methods=["GET", "POST"])
def editar_oferecem(id_empresa: int, nome_cidade: str, nome_servico: str):
    item = model_oferecem.buscar(id_empresa, nome_cidade, nome_servico)
    if not item:
        flash("Oferecimento não encontrado.", "danger")
        return redirect(url_for("listar_oferecem"))
    if request.method == "POST":
        model_oferecem.atualizar(id_empresa, nome_cidade, nome_servico,
                                 float(request.form["preco_hora"]))
        flash("Preço atualizado!", "success")
        return redirect(url_for("listar_oferecem"))
    return render_template("oferecem/form.html", titulo="Editar Oferecimento",
                           action=url_for("editar_oferecem", id_empresa=id_empresa,
                                          nome_cidade=nome_cidade, nome_servico=nome_servico),
                           item=item, empresas=model_empresas.listar_simples(),
                           servicos=model_servicos.listar_simples(),
                           cidades=model_cidades.listar_simples())


@app.route("/oferecem/<int:id_empresa>/<nome_cidade>/<nome_servico>/excluir",
           methods=["POST"])
def excluir_oferecem(id_empresa: int, nome_cidade: str, nome_servico: str):
    model_oferecem.excluir(id_empresa, nome_cidade, nome_servico)
    flash("Oferecimento excluído.", "success")
    return redirect(url_for("listar_oferecem"))


# ============================================================
# FUNCIONARIOS CRUD
# ============================================================

@app.route("/funcionarios/")
def listar_funcionarios():
    return render_template("funcionarios/list.html", funcionarios=model_funcionarios.listar())


@app.route("/funcionarios/criar", methods=["GET", "POST"])
def criar_funcionario():
    if request.method == "POST":
        cpf = request.form["cpf"].strip()
        if any(f["cpf_func"] == cpf for f in model_funcionarios.listar()):
            flash("Já existe um funcionário com este CPF.", "danger")
            return render_template("funcionarios/form.html", titulo="Novo Funcionário",
                                   action=url_for("criar_funcionario"), func=None)
        vinculos = []
        empresas_ids = request.form.getlist("vinculo_empresa[]")
        inicio = request.form.getlist("vinculo_inicio[]")
        fim = request.form.getlist("vinculo_fim[]")
        telefone_emp = request.form.getlist("vinculo_telefone[]")
        for i, eid in enumerate(empresas_ids):
            if eid:
                vinculos.append({
                    "id_empresa": int(eid),
                    "data_inicio": inicio[i] if i < len(inicio) else None,
                    "data_fim": fim[i] if i < len(fim) and fim[i] else None,
                    "telefone_empresa": telefone_emp[i] if i < len(telefone_emp) else "",
                })
        model_funcionarios.criar(cpf, request.form["rg"].strip(),
                                 request.form["nome_completo"].strip(),
                                 request.form["endereco"].strip(),
                                 request.form["telefone_contato"].strip(),
                                 float(request.form["salario"]), request.form["tipo"], vinculos)
        flash("Funcionário criado!", "success")
        return redirect(url_for("listar_funcionarios"))
    return render_template("funcionarios/form.html", titulo="Novo Funcionário",
                           action=url_for("criar_funcionario"), func=None,
                           empresas=model_empresas.listar_simples())


@app.route("/funcionarios/<cpf>/editar", methods=["GET", "POST"])
def editar_funcionario(cpf: str):
    func = model_funcionarios.buscar(cpf)
    if not func:
        flash("Funcionário não encontrado.", "danger")
        return redirect(url_for("listar_funcionarios"))
    if request.method == "POST":
        novo_cpf = request.form["cpf"].strip()
        if novo_cpf != func["cpf_func"] and \
           any(f["cpf_func"] == novo_cpf for f in model_funcionarios.listar()):
            flash("Já existe um funcionário com este CPF.", "danger")
            return render_template("funcionarios/form.html", titulo="Editar Funcionário",
                                   action=url_for("editar_funcionario", cpf=cpf), func=func)
        vinculos = []
        empresas_ids = request.form.getlist("vinculo_empresa[]")
        inicio = request.form.getlist("vinculo_inicio[]")
        fim = request.form.getlist("vinculo_fim[]")
        telefone_emp = request.form.getlist("vinculo_telefone[]")
        for i, eid in enumerate(empresas_ids):
            if eid:
                vinculos.append({
                    "id_empresa": int(eid),
                    "data_inicio": inicio[i] if i < len(inicio) else None,
                    "data_fim": fim[i] if i < len(fim) and fim[i] else None,
                    "telefone_empresa": telefone_emp[i] if i < len(telefone_emp) else "",
                })
        model_funcionarios.atualizar(func["cpf_func"], novo_cpf,
                                     request.form["rg"].strip(),
                                     request.form["nome_completo"].strip(),
                                     request.form["endereco"].strip(),
                                     request.form["telefone_contato"].strip(),
                                     float(request.form["salario"]),
                                     request.form["tipo"], vinculos)
        flash("Funcionário atualizado!", "success")
        return redirect(url_for("listar_funcionarios"))
    return render_template("funcionarios/form.html", titulo="Editar Funcionário",
                           action=url_for("editar_funcionario", cpf=cpf), func=func,
                           empresas=model_empresas.listar_simples())


@app.route("/funcionarios/<cpf>/excluir", methods=["POST"])
def excluir_funcionario(cpf: str):
    model_funcionarios.excluir(cpf)
    flash("Funcionário excluído.", "success")
    return redirect(url_for("listar_funcionarios"))


# ============================================================
# PEDIDOS CRUD
# ============================================================

@app.route("/pedidos/")
def listar_pedidos():
    return render_template("pedidos/list.html", pedidos=model_pedidos.listar())


@app.route("/pedidos/criar", methods=["GET", "POST"])
def criar_pedido():
    if request.method == "POST":
        aceite_raw = request.form["aceite"]
        aceite = True if aceite_raw == "true" else (False if aceite_raw == "false" else None)
        servicos = []
        for i, nome_servico in enumerate(request.form.getlist("servico_nome[]")):
            tempo_h = request.form.getlist("servico_tempo[]")[i]
            servicos.append({
                "nome_servico": nome_servico,
                "tempo_duracao": f"{float(tempo_h)} hours" if tempo_h else None,
                "data_efetiva": request.form.getlist("servico_data[]")[i] or None,
            })
        model_pedidos.criar(
            request.form["data_solicitacao"],
            request.form.get("data_resolucao", ""),
            aceite,
            int(request.form["id_empresa"]),
            int(request.form["cod_cliente"]),
            request.form["cidade_partida"].strip(),
            request.form["endereco_partida"].strip(),
            request.form["cidade_destino"].strip(),
            request.form["endereco_destino"].strip(),
            servicos
        )
        flash("Pedido criado!", "success")
        return redirect(url_for("listar_pedidos"))
    return render_template("pedidos/form.html", titulo="Novo Pedido",
                           action=url_for("criar_pedido"), pedido=None,
                           clientes=model_clientes.listar_simples(),
                           empresas=model_empresas.listar_simples(),
                           servicos_disponiveis=model_servicos.listar_simples(),
                           cidades_lista=model_cidades.listar_simples())


@app.route("/pedidos/<int:cod_pedido>")
def detalhes_pedido(cod_pedido: int):
    pedido = model_pedidos.buscar(cod_pedido)
    if not pedido:
        flash("Pedido não encontrado.", "danger")
        return redirect(url_for("listar_pedidos"))
    servicos = model_pedidos.listar_servicos(cod_pedido)
    funcs_por_solicitacao = {}
    for s in servicos:
        funcs_por_solicitacao[s["id_solicitacao"]] = \
            model_pedidos.listar_funcionarios_solicitacao(s["id_solicitacao"])
    return render_template("pedidos/detail.html", pedido=pedido, servicos=servicos,
                           funcs_por_solicitacao=funcs_por_solicitacao,
                           todos_funcionarios=model_funcionarios.listar_simples())


@app.route("/pedidos/<int:cod_pedido>/editar", methods=["GET", "POST"])
def editar_pedido(cod_pedido: int):
    pedido = model_pedidos.buscar(cod_pedido)
    if not pedido:
        flash("Pedido não encontrado.", "danger")
        return redirect(url_for("listar_pedidos"))
    if request.method == "POST":
        aceite_raw = request.form["aceite"]
        aceite = True if aceite_raw == "true" else (False if aceite_raw == "false" else None)
        servicos = []
        for i, nome_servico in enumerate(request.form.getlist("servico_nome[]")):
            tempo_h = request.form.getlist("servico_tempo[]")[i]
            servicos.append({
                "nome_servico": nome_servico,
                "tempo_duracao": f"{float(tempo_h)} hours" if tempo_h else None,
                "data_efetiva": request.form.getlist("servico_data[]")[i] or None,
            })
        model_pedidos.atualizar(
            cod_pedido,
            request.form["data_solicitacao"],
            request.form.get("data_resolucao", ""),
            aceite,
            int(request.form["id_empresa"]),
            int(request.form["cod_cliente"]),
            request.form["cidade_partida"].strip(),
            request.form["endereco_partida"].strip(),
            request.form["cidade_destino"].strip(),
            request.form["endereco_destino"].strip(),
            servicos
        )
        flash(f"Pedido #{cod_pedido} atualizado!", "success")
        return redirect(url_for("listar_pedidos"))
    servicos_atual = model_pedidos.listar_servicos(cod_pedido)
    for s in servicos_atual:
        if s.get("tempo_duracao") is not None:
            s["tempo_duracao_horas"] = s["tempo_duracao"].total_seconds() / 3600
        else:
            s["tempo_duracao_horas"] = ""
    return render_template("pedidos/form.html", titulo="Editar Pedido",
                           action=url_for("editar_pedido", cod_pedido=cod_pedido),
                           pedido=pedido, servicos_atual=servicos_atual,
                           clientes=model_clientes.listar_simples(),
                           empresas=model_empresas.listar_simples(),
                           servicos_disponiveis=model_servicos.listar_simples(),
                           cidades_lista=model_cidades.listar_simples())


@app.route("/pedidos/<int:cod_pedido>/excluir", methods=["POST"])
def excluir_pedido(cod_pedido: int):
    model_pedidos.excluir(cod_pedido)
    flash(f"Pedido #{cod_pedido} excluído.", "success")
    return redirect(url_for("listar_pedidos"))


# ============================================================
# ALOCACAO FUNCIONARIOS EM SOLICITACOES
# ============================================================

@app.route("/solicitacoes/<int:id_solicitacao>/alocar", methods=["POST"])
def alocar_funcionario(id_solicitacao: int):
    model_pedidos.alocar_funcionario(id_solicitacao, request.form["cpf_func"])
    flash("Funcionário alocado!", "success")
    return redirect(request.referrer or url_for("listar_pedidos"))


@app.route("/solicitacoes/<int:id_solicitacao>/desalocar/<cpf>", methods=["POST"])
def desalocar_funcionario(id_solicitacao: int, cpf: str):
    model_pedidos.desalocar_funcionario(id_solicitacao, cpf)
    flash("Funcionário desalocado.", "success")
    return redirect(request.referrer or url_for("listar_pedidos"))


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template("404.html"), 404


# ============================================================
# RELATORIOS
# ============================================================

@app.route("/relatorios/")
def relatorios():
    return render_template("relatorios/index.html")


def _executar_query(sql):
    from db import query as q
    return q(sql)


@app.route("/relatorios/histograma-servicos")
def rel_histograma_servicos():
    rows = _executar_query("""
        SELECT p.cidade_partida AS cidade, c.estado, COUNT(*) AS quantidade
        FROM solicitacoes_servico ss
        JOIN pedidos p ON p.cod_pedido = ss.cod_pedido
        LEFT JOIN cidades c ON c.nome_cidade = p.cidade_partida
        GROUP BY p.cidade_partida, c.estado
        ORDER BY quantidade DESC
    """)
    labels = [f"{r['cidade']}/{r['estado'] or ''}" for r in rows]
    valores = [r["quantidade"] for r in rows]
    return render_template("relatorios/histograma_servicos.html",
                           dados={"labels": labels, "valores": valores})


@app.route("/relatorios/histograma-pagamentos")
def rel_histograma_pagamentos():
    rows = _executar_query("""
        SELECT p.cidade_partida AS cidade, c.estado, SUM(ss.preco) AS total_pago
        FROM solicitacoes_servico ss
        JOIN pedidos p ON p.cod_pedido = ss.cod_pedido
        LEFT JOIN cidades c ON c.nome_cidade = p.cidade_partida
        WHERE ss.preco IS NOT NULL
        GROUP BY p.cidade_partida, c.estado
        ORDER BY total_pago DESC
    """)
    labels = [f"{r['cidade']}/{r['estado'] or ''}" for r in rows]
    valores = [float(r["total_pago"]) for r in rows]
    return render_template("relatorios/histograma_pagamentos.html",
                           dados={"labels": labels, "valores": valores})


@app.route("/relatorios/top5-cidades-valor")
def rel_top5_cidades_valor():
    rows = _executar_query("""
        SELECT p.cidade_partida AS cidade, c.estado, SUM(ss.preco) AS valor
        FROM solicitacoes_servico ss
        JOIN pedidos p ON p.cod_pedido = ss.cod_pedido
        LEFT JOIN cidades c ON c.nome_cidade = p.cidade_partida
        WHERE ss.preco IS NOT NULL
        GROUP BY p.cidade_partida, c.estado
        ORDER BY valor DESC
        LIMIT 5
    """)
    return render_template("relatorios/top5_cidades_valor.html", dados=rows)


@app.route("/relatorios/top5-cidades-servicos")
def rel_top5_cidades_servicos():
    rows = _executar_query("""
        SELECT p.cidade_partida AS cidade, c.estado, COUNT(*) AS quantidade
        FROM solicitacoes_servico ss
        JOIN pedidos p ON p.cod_pedido = ss.cod_pedido
        LEFT JOIN cidades c ON c.nome_cidade = p.cidade_partida
        GROUP BY p.cidade_partida, c.estado
        ORDER BY quantidade DESC
        LIMIT 5
    """)
    return render_template("relatorios/top5_cidades_servicos.html", dados=rows)


@app.route("/relatorios/top5-empresas-servicos")
def rel_top5_empresas_servicos():
    rows = _executar_query("""
        SELECT e.nome AS empresa, COUNT(*) AS quantidade
        FROM solicitacoes_servico ss
        JOIN pedidos p ON p.cod_pedido = ss.cod_pedido
        JOIN empresas e ON e.id_empresa = p.id_empresa
        GROUP BY e.nome
        ORDER BY quantidade DESC
        LIMIT 5
    """)
    return render_template("relatorios/top5_empresas_servicos.html", dados=rows)


@app.route("/relatorios/top5-empresas-receita")
def rel_top5_empresas_receita():
    rows = _executar_query("""
        SELECT e.nome AS empresa, SUM(ss.preco) AS valor
        FROM solicitacoes_servico ss
        JOIN pedidos p ON p.cod_pedido = ss.cod_pedido AND p.aceite = TRUE
        JOIN empresas e ON e.id_empresa = p.id_empresa
        WHERE ss.preco IS NOT NULL
        GROUP BY e.nome
        ORDER BY valor DESC
        LIMIT 5
    """)
    return render_template("relatorios/top5_empresas_receita.html", dados=rows)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
