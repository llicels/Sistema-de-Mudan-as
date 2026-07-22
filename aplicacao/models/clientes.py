from db import query, query_one, execute


def listar():
    return query("""
        SELECT c.cod_cliente, c.cpf, c.rg, c.nome_completo, c.endereco,
               COALESCE(json_agg(json_build_object('id_telefone', tc.id_telefone, 'telefone', tc.telefone))
                        FILTER (WHERE tc.id_telefone IS NOT NULL), '[]') AS telefones
        FROM clientes c
        LEFT JOIN telefones_cliente tc ON tc.cod_cliente = c.cod_cliente
        GROUP BY c.cod_cliente, c.cpf, c.rg, c.nome_completo, c.endereco
        ORDER BY c.nome_completo
    """)


def buscar(cod_cliente):
    return query_one("""
        SELECT c.cod_cliente, c.cpf, c.rg, c.nome_completo, c.endereco,
               COALESCE(json_agg(json_build_object('id_telefone', tc.id_telefone, 'telefone', tc.telefone))
                        FILTER (WHERE tc.id_telefone IS NOT NULL), '[]') AS telefones
        FROM clientes c
        LEFT JOIN telefones_cliente tc ON tc.cod_cliente = c.cod_cliente
        WHERE c.cod_cliente = %s
        GROUP BY c.cod_cliente, c.cpf, c.rg, c.nome_completo, c.endereco
    """, (cod_cliente,))


def criar(cpf, rg, endereco, nome_completo, telefones):
    result = execute("""
        INSERT INTO clientes (cpf, rg, endereco, nome_completo)
        VALUES (%s, %s, %s, %s) RETURNING cod_cliente
    """, (cpf, rg, endereco, nome_completo))
    cod_cliente = result[0]["cod_cliente"]
    for i, tel in enumerate(telefones):
        if tel.strip():
            execute("INSERT INTO telefones_cliente (cod_cliente, id_telefone, telefone) VALUES (%s, %s, %s)",
                    (cod_cliente, i + 1, tel.strip()))
    return cod_cliente


def atualizar(cod_cliente, cpf, rg, endereco, nome_completo, telefones):
    execute("""
        UPDATE clientes SET cpf=%s, rg=%s, endereco=%s, nome_completo=%s
        WHERE cod_cliente=%s
    """, (cpf, rg, endereco, nome_completo, cod_cliente))
    execute("DELETE FROM telefones_cliente WHERE cod_cliente = %s", (cod_cliente,))
    for i, tel in enumerate(telefones):
        if tel.strip():
            execute("INSERT INTO telefones_cliente (cod_cliente, id_telefone, telefone) VALUES (%s, %s, %s)",
                    (cod_cliente, i + 1, tel.strip()))


def excluir(cod_cliente):
    execute("DELETE FROM clientes WHERE cod_cliente = %s", (cod_cliente,))


def listar_simples():
    return query("SELECT cod_cliente, nome_completo FROM clientes ORDER BY nome_completo")
