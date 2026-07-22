from db import query, query_one, execute


def listar():
    return query("""
        SELECT s.nome_servico, s.tipo_servico,
               g.tamanho_base, g.altura, g.bonus_aumento,
               t.limite_carga,
               COALESCE(json_agg(json_build_object('limite_carga', a.limite_carga, 'percentual', a.percentual))
                        FILTER (WHERE a.limite_carga IS NOT NULL), '[]') AS acrescimos
        FROM servicos s
        LEFT JOIN guindastes g ON g.nome_servico = s.nome_servico
        LEFT JOIN transportes t ON t.nome_servico = s.nome_servico
        LEFT JOIN acrescimos_transporte a ON a.nome_servico = s.nome_servico
        GROUP BY s.nome_servico, s.tipo_servico,
                 g.tamanho_base, g.altura, g.bonus_aumento,
                 t.limite_carga
        ORDER BY s.nome_servico
    """)


def buscar(nome_servico):
    return query_one("""
        SELECT s.nome_servico, s.tipo_servico,
               g.tamanho_base, g.altura, g.bonus_aumento,
               t.limite_carga,
               COALESCE(json_agg(json_build_object('limite_carga', a.limite_carga, 'percentual', a.percentual))
                        FILTER (WHERE a.limite_carga IS NOT NULL), '[]') AS acrescimos
        FROM servicos s
        LEFT JOIN guindastes g ON g.nome_servico = s.nome_servico
        LEFT JOIN transportes t ON t.nome_servico = s.nome_servico
        LEFT JOIN acrescimos_transporte a ON a.nome_servico = s.nome_servico
        WHERE s.nome_servico = %s
        GROUP BY s.nome_servico, s.tipo_servico,
                 g.tamanho_base, g.altura, g.bonus_aumento,
                 t.limite_carga
    """, (nome_servico,))


def criar_simples(nome_servico):
    execute("INSERT INTO servicos (nome_servico, tipo_servico) VALUES (%s, 'OUTRO')",
            (nome_servico,))


def criar_transporte(nome_servico, limite_carga, acrescimos):
    execute("INSERT INTO servicos (nome_servico, tipo_servico) VALUES (%s, 'TRANSPORTE')",
            (nome_servico,))
    execute("INSERT INTO transportes (nome_servico, limite_carga) VALUES (%s, %s)",
            (nome_servico, limite_carga))
    for i, (limite, pct) in enumerate(acrescimos):
        if limite and pct:
            execute("INSERT INTO acrescimos_transporte (nome_servico, limite_carga, percentual) VALUES (%s, %s, %s)",
                    (nome_servico, float(limite), float(pct)))


def criar_guindaste(nome_servico, tamanho_base, altura, bonus_aumento):
    execute("INSERT INTO servicos (nome_servico, tipo_servico) VALUES (%s, 'GUINDASTE')",
            (nome_servico,))
    execute("INSERT INTO guindastes (nome_servico, tamanho_base, altura, bonus_aumento) VALUES (%s, %s, %s, %s)",
            (nome_servico, tamanho_base, altura, bonus_aumento))


def atualizar_simples(nome_antigo, nome_novo):
    execute("UPDATE servicos SET nome_servico = %s WHERE nome_servico = %s",
            (nome_novo, nome_antigo))


def atualizar_transporte(nome_antigo, nome_novo, limite_carga, acrescimos):
    execute("UPDATE servicos SET nome_servico = %s WHERE nome_servico = %s",
            (nome_novo, nome_antigo))
    execute("UPDATE transportes SET nome_servico = %s, limite_carga = %s WHERE nome_servico = %s",
            (nome_novo, limite_carga, nome_antigo))
    execute("DELETE FROM acrescimos_transporte WHERE nome_servico = %s", (nome_novo,))
    for limite, pct in acrescimos:
        if limite and pct:
            execute("INSERT INTO acrescimos_transporte (nome_servico, limite_carga, percentual) VALUES (%s, %s, %s)",
                    (nome_novo, float(limite), float(pct)))


def atualizar_guindaste(nome_antigo, nome_novo, tamanho_base, altura, bonus_aumento):
    execute("UPDATE servicos SET nome_servico = %s WHERE nome_servico = %s",
            (nome_novo, nome_antigo))
    execute("""
        UPDATE guindastes SET nome_servico = %s, tamanho_base = %s, altura = %s, bonus_aumento = %s
        WHERE nome_servico = %s
    """, (nome_novo, tamanho_base, altura, bonus_aumento, nome_antigo))


def excluir(nome_servico):
    execute("DELETE FROM servicos WHERE nome_servico = %s", (nome_servico,))


def listar_simples():
    return query("SELECT nome_servico, tipo_servico FROM servicos ORDER BY nome_servico")
