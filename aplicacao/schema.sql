BEGIN;

-- =====================================================================
-- EMPRESAS
-- =====================================================================
CREATE TABLE empresas (
    id_empresa SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL UNIQUE,
    endereco TEXT NOT NULL
);

CREATE TABLE telefones_empresa (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    id_telefone INTEGER NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_empresa, id_telefone)
);

-- =====================================================================
-- CIDADES
-- =====================================================================
CREATE TABLE cidades (
    nome_cidade VARCHAR(100) PRIMARY KEY,
    estado VARCHAR(2) NOT NULL
);

-- =====================================================================
-- SERVICOS (hierarquia: supertipo)
-- =====================================================================
CREATE TABLE servicos (
    nome_servico VARCHAR(100) PRIMARY KEY,
    tipo_servico VARCHAR(20) NOT NULL CHECK (tipo_servico IN ('OUTRO', 'GUINDASTE', 'TRANSPORTE'))
);

CREATE TABLE guindastes (
    nome_servico VARCHAR(100) PRIMARY KEY REFERENCES servicos(nome_servico) ON DELETE CASCADE,
    tamanho_base DECIMAL(10,2) NOT NULL,
    altura DECIMAL(10,2) NOT NULL,
    bonus_aumento DECIMAL(5,2) NOT NULL DEFAULT 0
);

CREATE TABLE transportes (
    nome_servico VARCHAR(100) PRIMARY KEY REFERENCES servicos(nome_servico) ON DELETE CASCADE,
    limite_carga DECIMAL(10,2) NOT NULL
);

CREATE TABLE acrescimos_transporte (
    nome_servico VARCHAR(100) NOT NULL REFERENCES transportes(nome_servico) ON DELETE CASCADE,
    limite_carga DECIMAL(10,2) NOT NULL,
    percentual DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (nome_servico, limite_carga)
);

-- =====================================================================
-- OFERECEM (empresa oferece servico em cidade com preco_hora)
-- =====================================================================
CREATE TABLE oferecem (
    id_empresa INTEGER NOT NULL REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    nome_cidade VARCHAR(100) NOT NULL REFERENCES cidades(nome_cidade),
    nome_servico VARCHAR(100) NOT NULL REFERENCES servicos(nome_servico) ON DELETE CASCADE,
    preco_hora DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_empresa, nome_cidade, nome_servico)
);

-- =====================================================================
-- CLIENTES
-- =====================================================================
CREATE TABLE clientes (
    cod_cliente SERIAL PRIMARY KEY,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    rg VARCHAR(20),
    nome_completo VARCHAR(200) NOT NULL,
    endereco TEXT
);

CREATE TABLE telefones_cliente (
    cod_cliente INTEGER NOT NULL REFERENCES clientes(cod_cliente) ON DELETE CASCADE,
    id_telefone INTEGER NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    PRIMARY KEY (cod_cliente, id_telefone)
);

-- =====================================================================
-- FUNCIONARIOS
-- =====================================================================
CREATE TABLE funcionarios (
    cpf_func VARCHAR(14) PRIMARY KEY,
    rg_func VARCHAR(20),
    nome_completo_func VARCHAR(200) NOT NULL,
    endereco_func TEXT,
    telefone_contato VARCHAR(20),
    salario DECIMAL(10,2),
    tipo_func VARCHAR(50)
);

CREATE TABLE funcionarios_empresas (
    cpf_func VARCHAR(14) NOT NULL REFERENCES funcionarios(cpf_func) ON DELETE CASCADE,
    id_empresa INTEGER NOT NULL REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    telefone_empresa VARCHAR(20),
    PRIMARY KEY (cpf_func, id_empresa, data_inicio)
);

-- =====================================================================
-- PEDIDOS
-- =====================================================================
CREATE TABLE pedidos (
    cod_pedido SERIAL PRIMARY KEY,
    data_solicitacao DATE NOT NULL,
    data_resolucao DATE,
    aceite BOOLEAN,
    preco_total DECIMAL(12,2),
    id_empresa INTEGER NOT NULL REFERENCES empresas(id_empresa),
    cod_cliente INTEGER NOT NULL REFERENCES clientes(cod_cliente),
    cidade_partida VARCHAR(100) NOT NULL REFERENCES cidades(nome_cidade),
    endereco_partida TEXT NOT NULL,
    cidade_destino VARCHAR(100) NOT NULL REFERENCES cidades(nome_cidade),
    endereco_destino TEXT NOT NULL
);

-- =====================================================================
-- SOLICITACOES SERVICO
-- =====================================================================
CREATE TABLE solicitacoes_servico (
    id_solicitacao SERIAL PRIMARY KEY,
    cod_pedido INTEGER NOT NULL REFERENCES pedidos(cod_pedido) ON DELETE CASCADE,
    nome_servico VARCHAR(100) NOT NULL REFERENCES servicos(nome_servico),
    preco DECIMAL(10,2),
    tempo_duracao INTERVAL,
    data_efetiva DATE,
    UNIQUE (cod_pedido, nome_servico)
);

-- =====================================================================
-- FUNCIONARIOS SOLICITACOES
-- =====================================================================
CREATE TABLE funcionarios_solicitacoes (
    id_solicitacao INTEGER NOT NULL REFERENCES solicitacoes_servico(id_solicitacao) ON DELETE CASCADE,
    cpf_func VARCHAR(14) NOT NULL REFERENCES funcionarios(cpf_func),
    PRIMARY KEY (id_solicitacao, cpf_func)
);

COMMIT;
