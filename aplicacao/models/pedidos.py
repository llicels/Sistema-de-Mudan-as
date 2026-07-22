from db import query, query_one, execute


def listar():
    return query("""
        SELECT p.cod_pedido, p.data_solicitacao, p.data_resolucao,
               p.aceite, p.preco_total,
               p.id_empresa, e.nome AS empresa_nome,
               p.cod_cliente, cl.nome_completo AS cliente_nome,
               p.cidade_partida, p.endereco_partida,
               p.cidade_destino, p.endereco_destino
        FROM pedidos p
        JOIN empresas e ON e.id_empresa = p.id_empresa
        JOIN clientes cl ON cl.cod_cliente = p.cod_cliente
        ORDER BY p.cod_pedido DESC
    """)


def buscar(cod_pedido):
    return query_one("""
        SELECT p.cod_pedido, p.data_solicitacao, p.data_resolucao,
               p.aceite, p.preco_total,
               p.id_empresa, e.nome AS empresa_nome,
               p.cod_cliente, cl.nome_completo AS cliente_nome,
               p.cidade_partida, p.endereco_partida,
               p.cidade_destino, p.endereco_destino
        FROM pedidos p
        JOIN empresas e ON e.id_empresa = p.id_empresa
        JOIN clientes cl ON cl.cod_cliente = p.cod_cliente
        WHERE p.cod_pedido = %s
    """, (cod_pedido,))


def criar(data_solicitacao, data_resolucao, aceite,
          id_empresa, cod_cliente,
          cidade_partida, endereco_partida,
          cidade_destino, endereco_destino,
          servicos):
    result = execute("""
        INSERT INTO pedidos (data_solicitacao, data_resolucao, aceite,
                             id_empresa, cod_cliente,
                             cidade_partida, endereco_partida,
                             cidade_destino, endereco_destino)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING cod_pedido
    """, (data_solicitacao, data_resolucao or None, aceite,
          id_empresa, cod_cliente,
          cidade_partida, endereco_partida,
          cidade_destino, endereco_destino))
    cod_pedido = result[0]["cod_pedido"]
    for s in servicos:
        execute("""
            INSERT INTO solicitacoes_servico (cod_pedido, nome_servico, tempo_duracao, data_efetiva)
            VALUES (%s, %s, %s, %s)
        """, (cod_pedido, s["nome_servico"], s.get("tempo_duracao"), s.get("data_efetiva")))
    return cod_pedido


def atualizar(cod_pedido, data_solicitacao, data_resolucao, aceite,
              id_empresa, cod_cliente,
              cidade_partida, endereco_partida,
              cidade_destino, endereco_destino,
              servicos):
    execute("""
        UPDATE pedidos SET data_solicitacao=%s, data_resolucao=%s, aceite=%s,
               id_empresa=%s, cod_cliente=%s,
               cidade_partida=%s, endereco_partida=%s,
               cidade_destino=%s, endereco_destino=%s
        WHERE cod_pedido=%s
    """, (data_solicitacao, data_resolucao or None, aceite,
          id_empresa, cod_cliente,
          cidade_partida, endereco_partida,
          cidade_destino, endereco_destino,
          cod_pedido))
    execute("DELETE FROM solicitacoes_servico WHERE cod_pedido = %s", (cod_pedido,))
    for s in servicos:
        execute("""
            INSERT INTO solicitacoes_servico (cod_pedido, nome_servico, tempo_duracao, data_efetiva)
            VALUES (%s, %s, %s, %s)
        """, (cod_pedido, s["nome_servico"], s.get("tempo_duracao"), s.get("data_efetiva")))


def excluir(cod_pedido):
    execute("DELETE FROM pedidos WHERE cod_pedido = %s", (cod_pedido,))


def listar_servicos(cod_pedido):
    return query("""
        SELECT ss.id_solicitacao, ss.cod_pedido, ss.nome_servico, ss.preco,
               ss.tempo_duracao, ss.data_efetiva
        FROM solicitacoes_servico ss
        WHERE ss.cod_pedido = %s
        ORDER BY ss.id_solicitacao
    """, (cod_pedido,))


def listar_funcionarios_solicitacao(id_solicitacao):
    return query("""
        SELECT fs.cpf_func, f.nome_completo_func, f.tipo_func
        FROM funcionarios_solicitacoes fs
        JOIN funcionarios f ON f.cpf_func = fs.cpf_func
        WHERE fs.id_solicitacao = %s
    """, (id_solicitacao,))


def alocar_funcionario(id_solicitacao, cpf_func):
    execute("""
        INSERT INTO funcionarios_solicitacoes (id_solicitacao, cpf_func)
        VALUES (%s, %s) ON CONFLICT DO NOTHING
    """, (id_solicitacao, cpf_func))


def desalocar_funcionario(id_solicitacao, cpf_func):
    execute("""
        DELETE FROM funcionarios_solicitacoes
        WHERE id_solicitacao = %s AND cpf_func = %s
    """, (id_solicitacao, cpf_func))
