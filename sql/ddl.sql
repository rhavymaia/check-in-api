DROP DATABASE IF EXISTS checkin;

CREATE DATABASE checkin;

USE checkin;

CREATE TABLE participante (
   id INTEGER NOT NULL AUTO_INCREMENT,
   nome VARCHAR(150),
   cpf VARCHAR(11),
   email VARCHAR(255),
   ocs_participante_id INTEGER,
   PRIMARY KEY (id)
);

CREATE TABLE evento(
   id INTEGER NOT NULL AUTO_INCREMENT,
   nome VARCHAR(150),
   data_inicio DATETIME,
   data_fim DATETIME,
   ocs_conferencia_id INTEGER,
   ocs_evento_id INTEGER,
   PRIMARY KEY(id)
);

CREATE TABLE usuario(
   id INTEGER NOT NULL AUTO_INCREMENT,
   login VARCHAR(40),
   senha VARCHAR(255),
   PRIMARY KEY(id)
);

CREATE TABLE tipo_participante_evento (
  id INTEGER NOT NULL AUTO_INCREMENT,
  nome VARCHAR(50) NOT NULL,
  evento_id INTEGER NOT NULL,
  PRIMARY KEY (id) ,
  FOREIGN KEY (evento_id) REFERENCES evento (id)
);

CREATE TABLE participante_evento (
   id INTEGER NOT NULL AUTO_INCREMENT,
   participante_id INTEGER NOT NULL,
   evento_id INTEGER NOT NULL,
   tipo_participante_evento_id INTEGER NOT NULL,
   PRIMARY KEY (id),
   FOREIGN KEY(participante_id) REFERENCES participante (id), 
   FOREIGN KEY(evento_id) REFERENCES evento (id),
   FOREIGN KEY(tipo_participante_evento_id) REFERENCES tipo_participante_evento (id)
);

CREATE TABLE participante_evento_checkin (
  participante_evento_id INTEGER NOT NULL,
  usuario_id INTEGER DEFAULT NULL,
  entrada DATETIME DEFAULT NULL,
  PRIMARY KEY (participante_evento_id),
  FOREIGN KEY (participante_evento_id) REFERENCES participante_evento (id),
  FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);

CREATE TABLE predio (
    id INTEGER NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    ocs_predio_id INTEGER,
    evento_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (evento_id) REFERENCES evento (id)
);

CREATE TABLE sala (
    id INTEGER NOT NULL AUTO_INCREMENT,
    predio_id INTEGER NOT NULL,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (predio_id) REFERENCES predio (id)
);

INSERT INTO usuario VALUES (1, 'admin', 'pbkdf2:sha256:50000$cP1FNukc$2c623fc77f945a53a39d2412cdf8a9031387c165b0a6c9ed3bbba7be21827f4a');

-- Alterado em: 20170830
CREATE TABLE cronograma (
   id INTEGER NOT NULL AUTO_INCREMENT,
   nome VARCHAR(150),
   data_realizacao DATE,
   hora_inicio TIME,
   hora_fim TIME,
   evento_id INTEGER NOT NULL,
   FOREIGN KEY (evento_id) REFERENCES evento (id),
   PRIMARY KEY(id)
);

CREATE TABLE turno (
   id INTEGER NOT NULL AUTO_INCREMENT,
   PRIMARY KEY(id)
);

CREATE TABLE apresentacao (
   id INTEGER NOT NULL AUTO_INCREMENT,
   PRIMARY KEY(id)
);

-- Alteração: 20170920
ALTER TABLE cronograma
MODIFY COLUMN data_realizacao datetime;

-- Alteração: 20170925
CREATE TABLE trilha (
   id INTEGER NOT NULL AUTO_INCREMENT,
   nome VARCHAR(150),
   PRIMARY KEY(id)
);

-- Alteração: 20170927
DROP TABLE IF EXISTS trilha_evento;
CREATE TABLE trilha_evento (
   id INTEGER NOT NULL AUTO_INCREMENT,
   trilha_id INTEGER NOT NULL,
   evento_id INTEGER NOT NULL,
   FOREIGN KEY (trilha_id) REFERENCES trilha (id),
   FOREIGN KEY (evento_id) REFERENCES evento (id),
   PRIMARY KEY(id)
);

DROP TABLE IF EXISTS apresentacao;
CREATE TABLE apresentacao (
   id INTEGER NOT NULL AUTO_INCREMENT,
   titulo VARCHAR(200),
   trilha_id INTEGER NOT NULL,
   cronograma_id INTEGER NOT NULL,
   sala_id INTEGER NOT NULL,
   FOREIGN KEY (trilha_id) REFERENCES trilha (id),
   FOREIGN KEY (cronograma_id) REFERENCES cronograma (id),
   FOREIGN KEY (sala_id) REFERENCES sala (id),
   PRIMARY KEY(id)
);

ALTER TABLE sala ADD cor VARCHAR(6);
ALTER TABLE sala ADD capacidade INTEGER;

-- Alteração: 20170930
ALTER TABLE apresentacao ADD hora_inicio TIME;
ALTER TABLE apresentacao ADD hora_fim TIME;

-- Alteração: 20171003
ALTER TABLE apresentacao ADD is_deleted BOOLEAN DEFAULT 0;
ALTER TABLE cronograma ADD is_deleted BOOLEAN DEFAULT 0;
ALTER TABLE evento ADD is_deleted BOOLEAN DEFAULT 0;
ALTER TABLE participante ADD is_deleted BOOLEAN DEFAULT 0;
ALTER TABLE predio ADD is_deleted BOOLEAN DEFAULT 0;
ALTER TABLE sala ADD is_deleted BOOLEAN DEFAULT 0;
ALTER TABLE trilha ADD is_deleted BOOLEAN DEFAULT 0;

-- Alteração: 20171009
DROP TABLE IF EXISTS apresentacao_participante;
CREATE TABLE apresentacao_participante (
   id INTEGER NOT NULL AUTO_INCREMENT,
   apresentacao_id INTEGER NOT NULL,
   participante_id INTEGER NOT NULL,
   is_deleted BOOLEAN DEFAULT 0,
   dt_insercao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (apresentacao_id) REFERENCES apresentacao (id),
   FOREIGN KEY (participante_id) REFERENCES participante (id),
   PRIMARY KEY(id)
);

-- Alteração: 20171013
DROP TABLE IF EXISTS predio_evento;
CREATE TABLE predio_evento (
   id INTEGER NOT NULL AUTO_INCREMENT,
   predio_id INTEGER NOT NULL,
   evento_id INTEGER NOT NULL,
   FOREIGN KEY (predio_id) REFERENCES predio (id),
   FOREIGN KEY (evento_id) REFERENCES evento (id),
   PRIMARY KEY(id)
);

-- Alteração: 20171027
ALTER TABLE predio DROP FOREIGN KEY predio_ibfk_1;
ALTER TABLE predio DROP evento_id;
ALTER TABLE predio MODIFY COLUMN ocs_predio_id INTEGER NULL;

-- Alteração: 20171031
ALTER TABLE sala ADD ocs_sala_id INTEGER;

-- Alteração: 20171106
DROP TABLE IF EXISTS autor;
CREATE TABLE autor (
   id INTEGER NOT NULL AUTO_INCREMENT,
   nome VARCHAR(120),
   email VARCHAR(90),
   apresentacao_id INTEGER NOT NULL,
   FOREIGN KEY (apresentacao_id) REFERENCES apresentacao (id),
   PRIMARY KEY(id)
);

-- Alteração: 20171108
ALTER TABLE apresentacao ADD ocs_pub_id INTEGER;

-- Alteração: 20171109
ALTER TABLE tipo_participante_evento ADD ocs_tipo_participante_id INTEGER;
ALTER TABLE apresentacao MODIFY trilha_id INTEGER NULL;
ALTER TABLE apresentacao MODIFY cronograma_id INTEGER NULL;
ALTER TABLE apresentacao MODIFY sala_id INTEGER NULL;

-- Alteração:20171113
ALTER TABLE autor ADD is_deleted BOOLEAN DEFAULT 0;

-- Alteração:20171114
ALTER TABLE autor ADD ocs_autor_id INTEGER;


CREATE TABLE modalidade (
    id INTEGER NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    evento_id INTEGER NOT NULL,
    ocs_modalidade_id  INTEGER,
    is_deleted BOOLEAN DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY (evento_id) REFERENCES evento (id)
);