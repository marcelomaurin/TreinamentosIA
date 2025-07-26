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
  texto TEXT NOT NULL,
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

