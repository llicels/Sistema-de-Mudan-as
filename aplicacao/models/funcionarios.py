from db import query, query_one, execute


def listar():
    return query("""
        SELECT f.cpf_func, f.rg_func, f.nome_completo_func, f.endereco_func,
               f.telefone_contato, f.salario, f.tipo_func,
               COALESCE(json_agg(json_build_object(
                    'id_empresa', fe.id_empresa,
                    'empresa_nome', e.nome,
                    'data_inicio', fe.data_inicio,
                    'data_fim', fe.data_fim,
                    'telefone_empresa', fe.telefone_empresa
               )) FILTER (WHERE fe.id_empresa IS NOT NULL), '[]') AS vinculos
        FROM funcionarios f
        LEFT JOIN funcionarios_empresas fe ON fe.cpf_func = f.cpf_func
        LEFT JOIN empresas e ON e.id_empresa = fe.id_empresa
        GROUP BY f.cpf_func, f.rg_func, f.nome_completo_func, f.endereco_func,
                 f.telefone_contato, f.salario, f.tipo_func
        ORDER BY f.nome_completo_func
    """)


def buscar(cpf_func):
    return query_one("""
        SELECT f.cpf_func, f.rg_func, f.nome_completo_func, f.endereco_func,
               f.telefone_contato, f.salario, f.tipo_func,
               COALESCE(json_agg(json_build_object(
                    'id_empresa', fe.id_empresa,
                    'empresa_nome', e.nome,
                    'data_inicio', fe.data_inicio,
                    'data_fim', fe.data_fim,
                    'telefone_empresa', fe.telefone_empresa
               )) FILTER (WHERE fe.id_empresa IS NOT NULL), '[]') AS vinculos
        FROM funcionarios f
        LEFT JOIN funcionarios_empresas fe ON fe.cpf_func = f.cpf_func
        LEFT JOIN empresas e ON e.id_empresa = fe.id_empresa
        WHERE f.cpf_func = %s
        GROUP BY f.cpf_func, f.rg_func, f.nome_completo_func, f.endereco_func,
                 f.telefone_contato, f.salario, f.tipo_func
    """, (cpf_func,))


def criar(cpf_func, rg_func, nome_completo_func, endereco_func,
          telefone_contato, salario, tipo_func, vinculos):
    execute("""
        INSERT INTO funcionarios (cpf_func, rg_func, nome_completo_func, endereco_func,
                                  telefone_contato, salario, tipo_func)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (cpf_func, rg_func, nome_completo_func, endereco_func,
          telefone_contato, salario, tipo_func))
    for v in vinculos:
        execute("""
            INSERT INTO funcionarios_empresas (cpf_func, id_empresa, data_inicio, data_fim, telefone_empresa)
            VALUES (%s, %s, %s, %s, %s)
        """, (cpf_func, v["id_empresa"], v["data_inicio"], v.get("data_fim"), v.get("telefone_empresa")))


def atualizar(cpf_antigo, cpf_func, rg_func, nome_completo_func, endereco_func,
              telefone_contato, salario, tipo_func, vinculos):
    execute("""
        UPDATE funcionarios SET cpf_func=%s, rg_func=%s, nome_completo_func=%s,
               endereco_func=%s, telefone_contato=%s, salario=%s, tipo_func=%s
        WHERE cpf_func=%s
    """, (cpf_func, rg_func, nome_completo_func, endereco_func,
          telefone_contato, salario, tipo_func, cpf_antigo))
    execute("DELETE FROM funcionarios_empresas WHERE cpf_func = %s", (cpf_func,))
    for v in vinculos:
        execute("""
            INSERT INTO funcionarios_empresas (cpf_func, id_empresa, data_inicio, data_fim, telefone_empresa)
            VALUES (%s, %s, %s, %s, %s)
        """, (cpf_func, v["id_empresa"], v["data_inicio"], v.get("data_fim"), v.get("telefone_empresa")))


def excluir(cpf_func):
    execute("DELETE FROM funcionarios WHERE cpf_func = %s", (cpf_func,))


def listar_simples():
    return query("SELECT cpf_func, nome_completo_func, tipo_func FROM funcionarios ORDER BY nome_completo_func")
