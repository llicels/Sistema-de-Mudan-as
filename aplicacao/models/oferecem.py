from db import query, query_one, execute


def listar():
    return query("""
        SELECT o.id_empresa, e.nome AS empresa_nome,
               o.nome_cidade, o.nome_servico, o.preco_hora
        FROM oferecem o
        JOIN empresas e ON e.id_empresa = o.id_empresa
        ORDER BY e.nome, o.nome_servico, o.nome_cidade
    """)


def buscar(id_empresa, nome_cidade, nome_servico):
    return query_one("""
        SELECT o.id_empresa, e.nome AS empresa_nome,
               o.nome_cidade, o.nome_servico, o.preco_hora
        FROM oferecem o
        JOIN empresas e ON e.id_empresa = o.id_empresa
        WHERE o.id_empresa = %s AND o.nome_cidade = %s AND o.nome_servico = %s
    """, (id_empresa, nome_cidade, nome_servico))


def criar(id_empresa, nome_cidade, nome_servico, preco_hora):
    execute("""
        INSERT INTO oferecem (id_empresa, nome_cidade, nome_servico, preco_hora)
        VALUES (%s, %s, %s, %s)
    """, (id_empresa, nome_cidade, nome_servico, preco_hora))


def atualizar(id_empresa, nome_cidade, nome_servico, preco_hora):
    execute("""
        UPDATE oferecem SET preco_hora = %s
        WHERE id_empresa = %s AND nome_cidade = %s AND nome_servico = %s
    """, (preco_hora, id_empresa, nome_cidade, nome_servico))


def excluir(id_empresa, nome_cidade, nome_servico):
    execute("""
        DELETE FROM oferecem
        WHERE id_empresa = %s AND nome_cidade = %s AND nome_servico = %s
    """, (id_empresa, nome_cidade, nome_servico))
