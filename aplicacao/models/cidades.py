from db import query, query_one, execute


def listar():
    return query("SELECT nome_cidade, estado FROM cidades ORDER BY nome_cidade, estado")


def buscar(nome_cidade, estado):
    return query_one(
        "SELECT nome_cidade, estado FROM cidades WHERE nome_cidade = %s AND estado = %s",
        (nome_cidade, estado)
    )


def criar(nome_cidade, estado):
    execute("INSERT INTO cidades (nome_cidade, estado) VALUES (%s, %s)",
            (nome_cidade, estado))


def atualizar(nome_antigo, estado_antigo, nome_novo, estado_novo):
    execute("""
        UPDATE cidades SET nome_cidade = %s, estado = %s
        WHERE nome_cidade = %s AND estado = %s
    """, (nome_novo, estado_novo, nome_antigo, estado_antigo))


def excluir(nome_cidade, estado):
    execute("DELETE FROM cidades WHERE nome_cidade = %s AND estado = %s",
            (nome_cidade, estado))


def listar_simples():
    return query("SELECT nome_cidade, estado FROM cidades ORDER BY nome_cidade")
