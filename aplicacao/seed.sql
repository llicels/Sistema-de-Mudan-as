BEGIN;

-- ---------------------------------------------------------------------
-- EMPRESAS
-- ---------------------------------------------------------------------
INSERT INTO empresas (nome, endereco) VALUES
    ('Mudanças Rápidas Ltda',          'Av. Paulista, 1000 - São Paulo/SP'),
    ('Transportes Silva & Cia',        'Rua das Flores, 250 - Campinas/SP'),
    ('Mudanças ABC Ltda',              'Av. Brasil, 500 - São Paulo/SP'),
    ('Transporte Expresso S.A.',       'Rua XV, 100 - Curitiba/PR'),
    ('Guindastes Brasil Eireli',       'Av. Industrial, 300 - Belo Horizonte/MG'),
    ('Caminhões Forte Ltda',           'Rod. BR-101, km 50 - Recife/PE'),
    ('Logística Total S.A.',           'Av. Central, 1000 - Brasília/DF'),
    ('Carga Pesada Ltda',              'Rua do Porto, 200 - Porto Alegre/RS'),
    ('MoveBem Transportes',            'Av. Paulista, 2000 - São Paulo/SP'),
    ('SuperGuindaste S.A.',            'Rua da Oficina, 50 - Salvador/BA');

INSERT INTO telefones_empresa (id_empresa, id_telefone, telefone) VALUES
    (1, 1, '1130001111'),
    (1, 2, '1199998888'),
    (2, 1, '1932223333');

-- ---------------------------------------------------------------------
-- CIDADES
-- ---------------------------------------------------------------------
INSERT INTO cidades (nome_cidade, estado) VALUES
    ('São Paulo', 'SP'),
    ('Campinas',  'SP'),
    ('Rio de Janeiro', 'RJ'),
    ('Belo Horizonte', 'MG'),
    ('Curitiba',       'PR'),
    ('Porto Alegre',   'RS'),
    ('Salvador',       'BA'),
    ('Recife',         'PE'),
    ('Fortaleza',      'CE'),
    ('Brasília',       'DF');

-- ---------------------------------------------------------------------
-- SERVICOS
-- ---------------------------------------------------------------------
INSERT INTO servicos (nome_servico, tipo_servico) VALUES
    ('Embalagem',            'OUTRO'),
    ('Desmontagem/Montagem', 'OUTRO'),
    ('Guindaste Pequeno',    'GUINDASTE'),
    ('Guindaste Grande',     'GUINDASTE'),
    ('Transporte Leve',      'TRANSPORTE'),
    ('Transporte Pesado',    'TRANSPORTE');

INSERT INTO guindastes (nome_servico, tamanho_base, altura, bonus_aumento) VALUES
    ('Guindaste Pequeno', 2.50, 10.00, 5.00),
    ('Guindaste Grande',  4.00, 25.00, 12.00);

INSERT INTO transportes (nome_servico, limite_carga) VALUES
    ('Transporte Leve',   500.00),
    ('Transporte Pesado', 1000.00);

INSERT INTO acrescimos_transporte (nome_servico, limite_carga, percentual) VALUES
    ('Transporte Leve',   500.00, 10.00),
    ('Transporte Leve',   750.00, 15.00),
    ('Transporte Pesado', 1000.00, 10.00);

-- ---------------------------------------------------------------------
-- OFERECEM
-- ---------------------------------------------------------------------
INSERT INTO oferecem (id_empresa, nome_cidade, nome_servico, preco_hora) VALUES
    (1, 'São Paulo', 'Embalagem',         80.00),
    (1, 'São Paulo', 'Transporte Leve',   150.00),
    (1, 'Campinas',  'Transporte Leve',   140.00),
    (2, 'Campinas',  'Guindaste Pequeno', 300.00),
    (2, 'Rio de Janeiro', 'Transporte Pesado', 250.00);

-- ---------------------------------------------------------------------
-- CLIENTES
-- ---------------------------------------------------------------------
INSERT INTO clientes (cpf, rg, nome_completo, endereco) VALUES
    ('11122233344', 'MG1234567', 'Ana Souza',        'Rua A, 10 - São Paulo/SP'),
    ('55566677788', 'RJ7654321', 'Bruno Lima',       'Rua B, 20 - Campinas/SP'),
    ('12345678901', 'SP9876543', 'Carla Mendes',     'Rua E, 100 - São Paulo/SP'),
    ('98765432101', 'PR5432167', 'Daniel Oliveira',  'Av. F, 200 - Curitiba/PR'),
    ('45678912301', 'MG2167890', 'Eduarda Santos',   'Rua G, 50 - Belo Horizonte/MG'),
    ('32165498701', 'BA9087654', 'Fábio Costa',      'Av. H, 300 - Salvador/BA'),
    ('65432178901', 'PE1122334', 'Gabriela Nunes',   'Rua I, 150 - Recife/PE'),
    ('78912345601', 'RS5566778', 'Henrique Alves',   'Av. J, 80 - Porto Alegre/RS');

INSERT INTO telefones_cliente (cod_cliente, id_telefone, telefone) VALUES
    (1, 1, '11977776666'),
    (2, 1, '19988887777');

-- ---------------------------------------------------------------------
-- FUNCIONARIOS
-- ---------------------------------------------------------------------
INSERT INTO funcionarios
    (cpf_func, rg_func, nome_completo_func, endereco_func, telefone_contato, salario, tipo_func)
VALUES
    ('99988877766', 'SP1112223', 'Carlos Pereira',   'Rua C, 30 - São Paulo/SP', '11966665555', 2500.00, 'motorista'),
    ('44433322211', 'SP4445556', 'Diego Fernandes',  'Rua D, 40 - Campinas/SP',  '19955554444', 3200.00, 'guincho');

INSERT INTO funcionarios_empresas (cpf_func, id_empresa, data_inicio, data_fim, telefone_empresa) VALUES
    ('99988877766', 1, '2023-01-10', NULL, '1130001111'),
    ('44433322211', 2, '2022-05-01', NULL, '1932223333');

-- ---------------------------------------------------------------------
-- PEDIDOS
-- ---------------------------------------------------------------------
INSERT INTO pedidos
    (data_solicitacao, data_resolucao, aceite, preco_total, id_empresa, cod_cliente,
     cidade_partida, endereco_partida, cidade_destino, endereco_destino)
VALUES
    ('2026-06-01', '2026-06-02', TRUE, 380.00, 1, 1,
     'São Paulo', 'Rua A, 10', 'São Paulo', 'Av. Central, 500'),
    ('2026-06-05', NULL, NULL, NULL, 2, 2,
     'Campinas', 'Rua B, 20', 'Rio de Janeiro', 'Rua Nova, 15'),
    ('2026-06-10', '2026-06-12', TRUE,  NULL, 3, 1,
     'São Paulo',      'Rua A, 10',          'Belo Horizonte', 'Av. Central, 2000'),
    ('2026-06-15', NULL,         NULL, NULL, 4, 3,
     'Curitiba',        'Rua XV, 200',        'Porto Alegre',   'Av. Independência, 500'),
    ('2026-06-20', '2026-06-22', TRUE,  NULL, 1, 4,
     'São Paulo',      'Rua dos Três, 30',   'São Paulo',      'Av. Berrini, 1000'),
    ('2026-06-25', NULL,         NULL, NULL, 5, 2,
     'Recife',          'Rua Nova, 50',       'Salvador',       'Av. Beira Mar, 300'),
    ('2026-07-01', '2026-07-03', TRUE,  NULL, 6, 5,
     'Brasília',       'SQS 100, Bloco A',   'Brasília',       'SHS Quadra 5'),
    ('2026-07-05', NULL,         NULL, NULL, 7, 6,
     'São Paulo',      'Rua Augusta, 500',   'Campinas',       'Av. Francisco Glicério, 200'),
    ('2026-07-10', '2026-07-11', TRUE,  NULL, 8, 7,
     'Porto Alegre',   'Rua da Praia, 100',  'Curitiba',       'Av. Batel, 500'),
    ('2026-07-15', NULL,         NULL, NULL, 2, 8,
     'Rio de Janeiro', 'Rua do Catete, 200', 'São Paulo',      'Av. Paulista, 1500');

-- ---------------------------------------------------------------------
-- SOLICITACOES SERVICO
-- ---------------------------------------------------------------------
INSERT INTO solicitacoes_servico (cod_pedido, nome_servico, preco, tempo_duracao, data_efetiva) VALUES
    (1, 'Embalagem',             80.00,  '2 hours', '2026-06-02'),
    (1, 'Transporte Leve',      150.00, '3 hours', '2026-06-02'),
    (2, 'Guindaste Pequeno',    300.00, NULL,      NULL),
    (3, 'Embalagem',             80.00,  '1 hour',  '2026-06-12'),
    (3, 'Transporte Pesado',    500.00,  '4 hours', '2026-06-12'),
    (4, 'Transporte Leve',      300.00,  '3 hours', NULL),
    (5, 'Transporte Leve',      200.00,  '2 hours', '2026-06-22'),
    (6, 'Guindaste Pequeno',    600.00,  '5 hours', NULL),
    (7, 'Desmontagem/Montagem', 150.00,  '2 hours', '2026-07-03'),
    (8, 'Guindaste Grande',     900.00,  '6 hours', NULL);

-- ---------------------------------------------------------------------
-- FUNCIONARIOS SOLICITACOES
-- ---------------------------------------------------------------------
INSERT INTO funcionarios_solicitacoes (id_solicitacao, cpf_func) VALUES
    (1, '99988877766'),
    (2, '99988877766'),
    (3, '44433322211');

COMMIT;
