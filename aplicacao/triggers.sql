-- =====================================================================
-- Trigger 2a: Hierarquia disjuntiva e parcial de servicos
-- =====================================================================
CREATE OR REPLACE FUNCTION check_service_hierarchy() RETURNS TRIGGER AS $$
BEGIN
    PERFORM 1
    FROM servicos s
    LEFT JOIN guindastes g ON s.nome_servico = g.nome_servico
    LEFT JOIN transportes t ON s.nome_servico = t.nome_servico
    WHERE (s.tipo_servico = 'GUINDASTE'  AND (g.nome_servico IS NULL     OR t.nome_servico IS NOT NULL))
       OR (s.tipo_servico = 'TRANSPORTE' AND (t.nome_servico IS NULL     OR g.nome_servico IS NOT NULL))
       OR (s.tipo_servico = 'OUTRO'      AND (g.nome_servico IS NOT NULL OR t.nome_servico IS NOT NULL));
    IF FOUND THEN
        RAISE EXCEPTION 'Inconsistência na hierarquia de serviços';
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER check_service_hierarchy_trg_servicos
    AFTER INSERT OR UPDATE OR DELETE ON servicos
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_service_hierarchy();

CREATE CONSTRAINT TRIGGER check_service_hierarchy_trg_guindastes
    AFTER INSERT OR UPDATE OR DELETE ON guindastes
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_service_hierarchy();

CREATE CONSTRAINT TRIGGER check_service_hierarchy_trg_transportes
    AFTER INSERT OR UPDATE OR DELETE ON transportes
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION check_service_hierarchy();

-- =====================================================================
-- Trigger 2c: Calculo do preco de cada servico solicitado
-- =====================================================================
CREATE OR REPLACE FUNCTION calculate_service_price(
    p_cod_pedido INTEGER,
    p_nome_servico VARCHAR,
    p_tempo_duracao INTERVAL DEFAULT NULL
)
RETURNS NUMERIC AS $$
DECLARE
    v_preco_hora    NUMERIC;
    v_tempo_duracao INTERVAL;
    v_hours         NUMERIC;
    v_tipo          VARCHAR;
    v_base          NUMERIC;
    v_bonus_pct     NUMERIC := 0;
    v_acrescimo_pct NUMERIC := 0;
    v_lim_transp    NUMERIC;
    v_preco_total   NUMERIC;
BEGIN
    -- Preco/hora ofertado pela empresa na cidade de partida
    SELECT o.preco_hora INTO v_preco_hora
    FROM pedidos p
    JOIN oferecem o ON p.id_empresa   = o.id_empresa
                   AND p.cidade_partida = o.nome_cidade
                   AND o.nome_servico   = p_nome_servico
    WHERE p.cod_pedido = p_cod_pedido;

    IF v_preco_hora IS NULL THEN
        RAISE EXCEPTION 'Serviço % não é oferecido pela empresa na cidade de partida.', p_nome_servico;
    END IF;

    -- Usa o tempo recebido como parametro ou busca da tabela
    v_tempo_duracao := COALESCE(p_tempo_duracao, (
        SELECT tempo_duracao
        FROM solicitacoes_servico
        WHERE cod_pedido = p_cod_pedido AND nome_servico = p_nome_servico
    ));

    v_hours := EXTRACT(EPOCH FROM v_tempo_duracao) / 3600.0;
    IF v_hours IS NULL THEN
        RETURN NULL;
    END IF;

    v_base := v_preco_hora * v_hours;

    SELECT tipo_servico INTO v_tipo
    FROM servicos WHERE nome_servico = p_nome_servico;

    IF v_tipo = 'GUINDASTE' THEN
        SELECT bonus_aumento INTO v_bonus_pct
        FROM guindastes WHERE nome_servico = p_nome_servico;
        v_bonus_pct := COALESCE(v_bonus_pct, 0);

        v_preco_total := v_base * (1 + v_bonus_pct / 100.0);

    ELSIF v_tipo = 'TRANSPORTE' THEN
        SELECT limite_carga INTO v_lim_transp
        FROM transportes WHERE nome_servico = p_nome_servico;

        SELECT a.percentual INTO v_acrescimo_pct
        FROM acrescimos_transporte a
        WHERE a.nome_servico = p_nome_servico
          AND a.limite_carga >= COALESCE(v_lim_transp, 0)
        ORDER BY a.limite_carga ASC
        LIMIT 1;
        v_acrescimo_pct := COALESCE(v_acrescimo_pct, 0);

        v_preco_total := v_base * (1 + v_acrescimo_pct / 100.0);

    ELSE
        v_preco_total := v_base;
    END IF;

    RETURN ROUND(v_preco_total, 2);
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION set_solicitacao_preco() RETURNS TRIGGER AS $$
DECLARE
    v_preco NUMERIC;
BEGIN
    IF TG_OP = 'UPDATE' THEN
        -- Recalcula sempre que colunas que afetam o preco mudam
        v_preco := calculate_service_price(NEW.cod_pedido, NEW.nome_servico, NEW.tempo_duracao);
    ELSIF NEW.preco IS NULL THEN
        -- INSERT sem preco explicito: calcula automaticamente
        v_preco := calculate_service_price(NEW.cod_pedido, NEW.nome_servico, NEW.tempo_duracao);
    END IF;

    IF v_preco IS NOT NULL THEN
        NEW.preco := v_preco;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_solicitacao_preco_trg
    BEFORE INSERT OR UPDATE OF tempo_duracao, nome_servico, cod_pedido
    ON solicitacoes_servico
    FOR EACH ROW EXECUTE FUNCTION set_solicitacao_preco();

-- =====================================================================
-- Trigger 2b: Atualizacao do preco total do pedido
-- =====================================================================
CREATE OR REPLACE FUNCTION recalcula_preco_total_pedido(p_cod_pedido INTEGER)
RETURNS VOID AS $$
BEGIN
    UPDATE pedidos
    SET preco_total = (
        SELECT SUM(ss.preco)
        FROM solicitacoes_servico ss
        WHERE ss.cod_pedido = p_cod_pedido
    )
    WHERE cod_pedido = p_cod_pedido;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trigger_preco_total_pedido() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        PERFORM recalcula_preco_total_pedido(OLD.cod_pedido);
        RETURN OLD;
    END IF;

    IF TG_OP = 'UPDATE' AND OLD.cod_pedido <> NEW.cod_pedido THEN
        PERFORM recalcula_preco_total_pedido(OLD.cod_pedido);
    END IF;

    PERFORM recalcula_preco_total_pedido(NEW.cod_pedido);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_preco_total_pedido_trg
    AFTER INSERT OR UPDATE OF preco, cod_pedido OR DELETE
    ON solicitacoes_servico
    FOR EACH ROW EXECUTE FUNCTION trigger_preco_total_pedido();

-- =====================================================================
-- Propagacao: quando preco_hora muda em oferecem
-- =====================================================================
CREATE OR REPLACE FUNCTION update_solicitacao_prices(
    p_nome_servico VARCHAR,
    p_empresa INTEGER DEFAULT NULL,
    p_cidade VARCHAR DEFAULT NULL
)
RETURNS VOID AS $$
BEGIN
    UPDATE solicitacoes_servico ss
    SET preco = COALESCE(calculate_service_price(ss.cod_pedido, ss.nome_servico, ss.tempo_duracao), ss.preco)
    FROM pedidos p
    WHERE ss.cod_pedido = p.cod_pedido
      AND ss.nome_servico = p_nome_servico
      AND (p_empresa IS NULL OR p.id_empresa = p_empresa)
      AND (p_cidade  IS NULL OR p.cidade_partida = p_cidade);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION trigger_update_solicitacoes_on_oferecem() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        PERFORM update_solicitacao_prices(OLD.nome_servico, OLD.id_empresa, OLD.nome_cidade);
        RETURN OLD;
    ELSE
        IF TG_OP = 'UPDATE' AND OLD.preco_hora = NEW.preco_hora THEN
            RETURN NULL;
        END IF;
        PERFORM update_solicitacao_prices(NEW.nome_servico, NEW.id_empresa, NEW.nome_cidade);
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_oferecem_after_insert_update
    AFTER INSERT OR UPDATE OF preco_hora ON oferecem
    FOR EACH ROW EXECUTE FUNCTION trigger_update_solicitacoes_on_oferecem();

CREATE TRIGGER trigger_oferecem_after_delete
    AFTER DELETE ON oferecem
    FOR EACH ROW EXECUTE FUNCTION trigger_update_solicitacoes_on_oferecem();

-- =====================================================================
-- Propagacao: quando bonus_aumento muda em guindastes
-- =====================================================================
CREATE OR REPLACE FUNCTION trigger_update_solicitacoes_on_guindaste() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        PERFORM update_solicitacao_prices(OLD.nome_servico);
        RETURN OLD;
    ELSE
        IF TG_OP = 'UPDATE' AND OLD.bonus_aumento = NEW.bonus_aumento THEN
            RETURN NULL;
        END IF;
        PERFORM update_solicitacao_prices(NEW.nome_servico);
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_guindastes_after_insert_update
    AFTER INSERT OR UPDATE OF bonus_aumento ON guindastes
    FOR EACH ROW EXECUTE FUNCTION trigger_update_solicitacoes_on_guindaste();

CREATE TRIGGER trigger_guindastes_after_delete
    AFTER DELETE ON guindastes
    FOR EACH ROW EXECUTE FUNCTION trigger_update_solicitacoes_on_guindaste();

-- =====================================================================
-- Propagacao: quando faixas de acrescimo mudam em acrescimos_transporte
-- =====================================================================
CREATE OR REPLACE FUNCTION trigger_update_solicitacoes_on_acrescimo() RETURNS TRIGGER AS $$
DECLARE
    v_servico VARCHAR;
BEGIN
    IF TG_OP = 'DELETE' THEN
        v_servico := OLD.nome_servico;
    ELSE
        v_servico := NEW.nome_servico;
    END IF;
    PERFORM update_solicitacao_prices(v_servico);
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_acrescimos_after_insert_update_delete
    AFTER INSERT OR UPDATE OR DELETE ON acrescimos_transporte
    FOR EACH ROW EXECUTE FUNCTION trigger_update_solicitacoes_on_acrescimo();
