CREATE DATABASE IF NOT EXISTS IAdb DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE IAdb;

-- Tabela: origem
CREATE TABLE origem (
  id INT AUTO_INCREMENT PRIMARY KEY,
  tipo VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO origem (id, tipo) VALUES
(1, 'voz'),
(2, 'treinamento');

-- Tabela: sentimentos
CREATE TABLE sentimentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  texto VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO sentimentos (id, texto) VALUES
(1,'Alegria'),(2,'Tristeza'),(3,'Raiva'),(4,'Medo'),(5,'Nojo'),(6,'Surpresa'),(7,'Amor'),
(8,'Ansiedade'),(9,'Gratidão'),(10,'Culpa'),(11,'Vergonha'),(12,'Frustração'),(13,'Solidão'),
(14,'Esperança'),(15,'Confiança'),(16,'Desprezo'),(17,'Admiração'),(18,'Euforia'),(19,'Ciúmes'),
(20,'Inveja'),(21,'Alívio'),(22,'Tédio'),(23,'Desejo'),(24,'Paz'),(25,'Saudade'),(26,'Empatia'),
(27,'Carinho'),(28,'Desânimo'),(29,'Angústia'),(30,'Compaixão'),(31,'Orgulho'),(32,'Desespero'),
(33,'Indiferença'),(34,'Neutro');

-- Tabela: idiomas
CREATE TABLE idiomas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(100) NOT NULL,
  codigo_iso CHAR(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO idiomas (id, nome, codigo_iso) VALUES
(1,'Inglês','en'),(2,'Espanhol','es'),(3,'Português','pt'),(4,'Francês','fr'),(5,'Alemão','de'),
(6,'Italiano','it'),(7,'Chinês (Mandarim)','zh'),(8,'Japonês','ja'),(9,'Coreano','ko'),(10,'Russo','ru'),
(11,'Árabe','ar'),(12,'Hindi','hi'),(13,'Bengali','bn'),(14,'Urdu','ur'),(15,'Turco','tr'),
(16,'Vietnamita','vi'),(17,'Tailandês','th'),(18,'Grego','el'),(19,'Hebraico','he'),(20,'Polonês','pl'),
(21,'Ucraniano','uk'),(22,'Romeno','ro'),(23,'Holandês','nl'),(24,'Sueco','sv'),(25,'Norueguês','no'),
(26,'Dinamarquês','da'),(27,'Finlandês','fi'),(28,'Tcheco','cs'),(29,'Húngaro','hu'),(30,'Eslovaco','sk'),
(31,'Croata','hr'),(32,'Sérvio','sr'),(33,'Indonésio','id'),(34,'Malaio','ms'),(35,'Filipino (Tagalog)','tl'),
(36,'Swahili','sw'),(37,'Africâner','af'),(38,'Persa (Farsi)','fa'),(39,'Tamil','ta'),(40,'Telugu','te'),
(41,'Gujarati','gu'),(42,'Canarês','kn'),(43,'Marathi','mr'),(44,'Malaiala','ml'),(45,'Punjabi','pa'),
(46,'Nepalês','ne');

-- Tabela: tipo_operacao
CREATE TABLE tipo_operacao (
  id INT AUTO_INCREMENT PRIMARY KEY,
  texto VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO tipo_operacao (id, texto) VALUES
(1,'Pergunta'),(2,'Execucao'),(3,'Armazenamento'),(4,'Pesquisa na Internet'),(5,'Pesquisa Local');

-- Tabela: perguntas
CREATE TABLE perguntas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  texto LONGTEXT  NOT NULL,
  processado TINYINT DEFAULT 0,
  id_origem INT NOT NULL DEFAULT 1,
  FOREIGN KEY (id_origem) REFERENCES origem(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: respostas
CREATE TABLE respostas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_pergunta INT NOT NULL,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  texto TEXT NOT NULL,
  FOREIGN KEY (id_pergunta) REFERENCES perguntas(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE subresposta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_pergunta INT NOT NULL,
  id_subpergunta INT NOT NULL,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  texto TEXT NOT NULL,
  FOREIGN KEY (id_pergunta) REFERENCES perguntas(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_subpergunta) REFERENCES subpergunta(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Tabela: analise_sentimentos
CREATE TABLE analise_sentimentos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_pergunta INT NOT NULL,
  id_sentimento INT NOT NULL,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_pergunta) REFERENCES perguntas(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_sentimento) REFERENCES sentimentos(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: subpergunta
CREATE TABLE subpergunta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_pergunta INT NOT NULL,
  texto TEXT NOT NULL,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  processado TINYINT NOT NULL DEFAULT 0,
  FOREIGN KEY (id_pergunta) REFERENCES perguntas(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: subpergunta_operacao
CREATE TABLE subpergunta_operacao (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_subpergunta INT NOT NULL,
  id_tipo_operacao INT NOT NULL,
  data DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_subpergunta) REFERENCES subpergunta(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_tipo_operacao) REFERENCES tipo_operacao(id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: foto (para armazenar imagens capturadas)
CREATE TABLE foto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    frame LONGBLOB NOT NULL,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    device VARCHAR(100) NOT NULL,
    processado TINYINT(1) DEFAULT 0,
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Tabela: termobusca
CREATE TABLE termobusca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    termo VARCHAR(255) NOT NULL,                      -- Termo de busca (exibição principal)
    texto VARCHAR(255) NOT NULL,                      -- Texto (compatibilidade com o código Python)
    qtd_videos INT DEFAULT 0,                         -- Quantidade de vídeos relacionados
    processado TINYINT(1) DEFAULT 0,                  -- 0 = Não processado, 1 = Processado
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de registro
    ativo TINYINT(1) DEFAULT 1,                       -- 1 = Ativo, 0 = Inativo
    id_origem INT NOT NULL,                           -- FK para origem
    CONSTRAINT fk_termobusca_origem 
        FOREIGN KEY (id_origem) REFERENCES origem(id)
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE termobusca MODIFY qtd_videos INT NOT NULL DEFAULT 3;

INSERT INTO termobusca (termo, texto, qtd_videos, processado, id_origem)
VALUES
('Vacinação Infantil', 'Vacinação Infantil', 3, 0, 2),
('Prevenção de Diabetes', 'Prevenção de Diabetes', 5, 0, 2),
('Cuidados com a Saúde Mental', 'Cuidados com a Saúde Mental', 2, 0, 2);

-- Tabela: processa_img
CREATE TABLE processa_img (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,             -- Nome do processamento
    script VARCHAR(255) NOT NULL,           -- Caminho para o script Python
    status TINYINT(1) NOT NULL DEFAULT 1,   -- 1 = Ativo, 0 = Inativo
    descricao TEXT,                         -- Descrição opcional do script
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

INSERT INTO processa_img (nome, script, status, descricao)
VALUES 
(
    'Captura de Face',
    '/home/mmm/projetos/maurinsoft/assistente2/captura_face.py',
    1,
    'Script responsável por detectar faces em imagens, recortar e salvar as informações da face (posição e ID gerado).'
);

-- Tabela: face
CREATE TABLE face (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_foto INT NOT NULL,
  face LONGBLOB NOT NULL,
  processado TINYINT(1) DEFAULT 0,
  dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_foto) REFERENCES foto(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: face_informacao
CREATE TABLE face_informacao (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_foto INT NOT NULL,
  id_face INT NOT NULL,
  id_propriedade INT NOT NULL,
  campo VARCHAR(100) NOT NULL,
  propriedade VARCHAR(100) NOT NULL,
  valor VARCHAR(255) NOT NULL,
  dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id_foto) REFERENCES foto(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_face) REFERENCES face(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- Tabela: item_compra
CREATE TABLE item_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item VARCHAR(255) NOT NULL,                -- Nome ou descrição do item para busca
    processado TINYINT(1) DEFAULT 0,           -- 0 = Não processado, 1 = Processado
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data de cadastro
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: item_compra_resultado
CREATE TABLE item_compra_resultado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_item_compra INT NOT NULL,               -- FK para item_compra
    descricao VARCHAR(500) NOT NULL,           -- Descrição do item
    descricao_tecnica TEXT,                    -- Informações técnicas
    preco VARCHAR(50),                         -- Preço (como texto para evitar problemas com formato)
    link VARCHAR(500),                         -- Link do produto no Mercado Livre
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Data de registro
    FOREIGN KEY (id_item_compra) REFERENCES item_compra(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE item_compra_resultado MODIFY link TEXT;

INSERT INTO item_compra (item) VALUES ('fone bluetooth'), ('placa mãe intel');
INSERT INTO item_compra (item) VALUES ('impressora termica'), ('tonner HP');



-- Tabela: area
CREATE TABLE area (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,                    -- Nome da área
    papel_ia TEXT NOT NULL,                        -- Papel que a IA deve assumir para esta área
    criterio_identificacao TEXT NOT NULL,          -- Critério usado pela IA para identificar esta área
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: grupo
CREATE TABLE grupo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_area INT NOT NULL,                          -- FK para área
    nome VARCHAR(200) NOT NULL,                    -- Nome do grupo
    papel_ia TEXT NOT NULL,                        -- Papel que a IA deve assumir para este grupo
    criterio_identificacao TEXT NOT NULL,          -- Critério usado pela IA para identificar este grupo
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_area) REFERENCES area(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: requisitos
CREATE TABLE requisitos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_grupo INT NOT NULL,                         -- FK para grupo
    descricao TEXT NOT NULL,                       -- Descrição do requisito
    criterio_identificacao TEXT NOT NULL,          -- Critério da IA para validar o requisito
    informacao_necessaria TEXT,                    -- Informação esperada para considerar o requisito atendido
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_grupo) REFERENCES grupo(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: acoes
CREATE TABLE acoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_requisito INT NOT NULL,                     -- FK para requisito
    nome VARCHAR(200) NOT NULL,                    -- Nome da ação
    criterio_disparo TEXT NOT NULL,                -- Critério que dispara a ação
    detalhes_acao TEXT,                            -- Detalhes ou instruções da ação
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_requisito) REFERENCES requisitos(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

 
-- Tabela: contas_email
CREATE TABLE contas_email (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,                  -- Nome identificador da conta (ex: Gmail Pessoal)
    email VARCHAR(255) NOT NULL,                -- Endereço de e-mail
    servidor_pop3 VARCHAR(255) NOT NULL,        -- Servidor POP3
    porta_pop3 INT NOT NULL DEFAULT 995,        -- Porta POP3
    ssl_pop3 TINYINT(1) DEFAULT 1,              -- SSL para POP3 (1=sim, 0=não)
    servidor_smtp VARCHAR(255) NOT NULL,        -- Servidor SMTP
    porta_smtp INT NOT NULL DEFAULT 465,        -- Porta SMTP
    ssl_smtp TINYINT(1) DEFAULT 1,              -- SSL para SMTP (1=sim, 0=não)
    usuario VARCHAR(255) NOT NULL,              -- Usuário de login
    senha VARCHAR(255) NOT NULL,                -- Senha criptografada ou armazenada
    ativo TINYINT(1) DEFAULT 1,                 -- Status da conta (ativa/inativa)
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP   -- Data de cadastro
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabela: emails
CREATE TABLE emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT NOT NULL,                          -- FK para a conta de e-mail
    remetente VARCHAR(255) NOT NULL,                -- Endereço de quem enviou
    destinatarios TEXT NOT NULL,                    -- Lista de destinatários (separados por ;)
    cc TEXT,                                        -- Lista de cópias (separados por ;)
    cco TEXT,                                       -- Lista de cópias ocultas (separados por ;)
    assunto VARCHAR(500) NOT NULL,                  -- Assunto do e-mail
    corpo LONGTEXT,                                 -- Corpo da mensagem (HTML ou texto)
    data_envio DATETIME,                            -- Data/Hora de envio ou recebimento
    lido TINYINT(1) DEFAULT 0,                      -- 0 = Não lido, 1 = Lido
    tipo ENUM('RECEBIDO', 'ENVIADO') NOT NULL,      -- Tipo do e-mail (Recebido ou Enviado)
    mensagem_id VARCHAR(255),                       -- ID da mensagem (RFC822 / servidores de e-mail)
    referencia_id VARCHAR(255),                     -- ID de referência (para threads/conversas)
    prioridade ENUM('ALTA', 'NORMAL', 'BAIXA') DEFAULT 'NORMAL', -- Prioridade do e-mail
    anexos TINYINT(1) DEFAULT 0,                    -- 1 = Possui anexos, 0 = Não possui
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,      -- Data de cadastro no sistema
    FOREIGN KEY (id_conta) REFERENCES contas_email(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE emails MODIFY mensagem_id VARCHAR(255) NULL;

-- Tabela de relacionamento entre emails e palavras-chave
CREATE TABLE emails_palavraschaves (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_email INT NOT NULL,         -- FK para a tabela emails
    id_palavra INT NOT NULL,       -- FK para a tabela palavraschaves
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_emails_palavras_email FOREIGN KEY (id_email) REFERENCES emails(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_emails_palavras_palavra FOREIGN KEY (id_palavra) REFERENCES palavraschaves(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uq_email_palavra (id_email, id_palavra)  -- Garante que não haja duplicidade no vínculo
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


ALTER TABLE emails 
ADD COLUMN message_id VARCHAR(255) NOT NULL UNIQUE AFTER tipo;

ALTER TABLE emails MODIFY tipo VARCHAR(50);

ALTER TABLE emails  DROP COLUMN message_id;

-- Tabela: documentos_email
CREATE TABLE documentos_email (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    id_documento INT NOT NULL,       -- FK para a tabela documentos
    id_email INT NOT NULL,           -- FK para a tabela emails
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_documentos_email_documento 
        FOREIGN KEY (id_documento) REFERENCES documentos(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_documentos_email_email 
        FOREIGN KEY (id_email) REFERENCES emails(id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY uq_documento_email (id_documento, id_email) -- Impede duplicidade do vínculo
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


CREATE TABLE documentos (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    texto LONGTEXT NOT NULL,
    caminho VARCHAR(500) NOT NULL,
    id_origem INT NOT NULL,
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_documentos_origem FOREIGN KEY (id_origem) REFERENCES origem(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

ALTER TABLE documentos 
ADD COLUMN resumo LONGTEXT NULL AFTER texto;


CREATE TABLE palavraschaves (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    palavra VARCHAR(255) NOT NULL UNIQUE,
    dtcad TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

