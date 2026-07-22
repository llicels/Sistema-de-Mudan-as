from db import query, query_one, execute


def listar():
    return query("""
        SELECT e.id_empresa, e.nome, e.endereco,
               COALESCE(json_agg(json_build_object('id_telefone', te.id_telefone, 'telefone', te.telefone))
                        FILTER (WHERE te.id_telefone IS NOT NULL), '[]') AS telefones,
               COALESCE(
                   (SELECT json_agg(DISTINCT o.nome_cidade) FROM oferecem o WHERE o.id_empresa = e.id_empresa),
                   '[]'
               ) AS cidades
        FROM empresas e
        LEFT JOIN telefones_empresa te ON te.id_empresa = e.id_empresa
        GROUP BY e.id_empresa, e.nome, e.endereco
        ORDER BY e.nome
    """)


def buscar(id_empresa):
    return query_one("""
        SELECT e.id_empresa, e.nome, e.endereco,
               COALESCE(json_agg(json_build_object('id_telefone', te.id_telefone, 'telefone', te.telefone))
                        FILTER (WHERE te.id_telefone IS NOT NULL), '[]') AS telefones,
               COALESCE(
                   (SELECT json_agg(DISTINCT o.nome_cidade) FROM oferecem o WHERE o.id_empresa = e.id_empresa),
                   '[]'
               ) AS cidades
        FROM empresas e
        LEFT JOIN telefones_empresa te ON te.id_empresa = e.id_empresa
        WHERE e.id_empresa = %s
        GROUP BY e.id_empresa, e.nome, e.endereco
    """, (id_empresa,))


def criar(nome, endereco, telefones):
    result = execute(
        "INSERT INTO empresas (nome, endereco) VALUES (%s, %s) RETURNING id_empresa",
        (nome, endereco)
    )
    id_empresa = result[0]["id_empresa"]
    for i, tel in enumerate(telefones):
        if tel.strip():
            execute("INSERT INTO telefones_empresa (id_empresa, id_telefone, telefone) VALUES (%s, %s, %s)",
                    (id_empresa, i + 1, tel.strip()))
    return id_empresa


def atualizar(id_empresa, nome, endereco, telefones):
    execute("UPDATE empresas SET nome = %s, endereco = %s WHERE id_empresa = %s",
            (nome, endereco, id_empresa))
    execute("DELETE FROM telefones_empresa WHERE id_empresa = %s", (id_empresa,))
    for i, tel in enumerate(telefones):
        if tel.strip():
            execute("INSERT INTO telefones_empresa (id_empresa, id_telefone, telefone) VALUES (%s, %s, %s)",
                    (id_empresa, i + 1, tel.strip()))


def excluir(id_empresa):
    execute("DELETE FROM empresas WHERE id_empresa = %s", (id_empresa,))


def listar_simples():
    return query("SELECT id_empresa, nome FROM empresas ORDER BY nome")
