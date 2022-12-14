/*Apaga os relacionamentos*/
ALTER TABLE MODELOS DROP CONSTRAINT MARCAS_MODELOS_FK;
ALTER TABLE AUTOMOVEIS DROP CONSTRAINT MODELOS_AUTOMOVEIS_FK;
ALTER TABLE LOCACOES DROP CONSTRAINT MODELOS_AUTOMOVEIS_FK;
ALTER TABLE LOCACOES DROP CONSTRAINT AUTOMOVEIS_LOCACOES_FK;

/*Apaga as tabelas*/
DROP TABLE CLIENTES;
DROP TABLE MODELOS;
DROP TABLE MARCAS;
DROP TABLE AUTOMOVEIS;
DROP TABLE LOCACOES;


DROP SEQUENCE LABDATABASE.CLIENTE_CPF_SEQ;
DROP SEQUENCE LABDATABASE.AUTOMOVEIS_PLACA_SEQ;
DROP SEQUENCE LABDATABASE.MODELOS_NOME_MODELO_SEQ;
DROP SEQUENCE LABDATABASE.MARCAS_NOME_MARCAS_SEQ;
DROP SEQUENCE LABDATABASE.LOCACOES_CPF_SEQ;

/*Cria as tabelas*/
CREATE TABLE CLIENTES (
                CPF NUMBER(20) NOT NULL,
                NOME VARCHAR2(50) NOT NULL,
                ENDERECO VARCHAR2(100) NOT NULL,
                TELEFONE NUMBER(20) NOT NULL,
                CONSTRAINT CLIENTES_PK PRIMARY KEY (CPF)
);


CREATE TABLE MARCAS (
                NOME_MARCA VARCHAR2(40) NOT NULL,
                CONSTRAINT MARCAS_PK PRIMARY KEY (NOME_MARCA)
);


CREATE TABLE MODELOS (
                NOME_MODELO VARCHAR2(40) NOT NULL,
                NOME_MARCA VARCHAR2(40) NOT NULL,
                CONSTRAINT MODELOS_PK PRIMARY KEY (NOME_MODELO, NOME_MARCA)
);


CREATE TABLE AUTOMOVEIS (
                PLACA VARCHAR2(7) NOT NULL,
                NOME_MODELO VARCHAR2(40) NOT NULL,
                NOME_MARCA VARCHAR2(40) NOT NULL,
                RENAVAM NUMBER(11) NOT NULL,
                COR VARCHAR2(30) NOT NULL,
                N_PORTAS NUMBER(1) NOT NULL,
                TIPO_COMBUSTIVEL VARCHAR2(20) NOT NULL,
                CONSTRAINT AUTOMOVEIS_PK PRIMARY KEY (PLACA, NOME_MODELO, NOME_MARCA)
);


CREATE TABLE LOCACOES (
                DATA_DEVOLUCAO DATE NOT NULL,
                PLACA VARCHAR2(7) NOT NULL,
                NOME_MODELO VARCHAR2(40) NOT NULL,
                NOME_MARCA VARCHAR2(40) NOT NULL,
                CPF VARCHAR2(11) NOT NULL,
                DATA_LOCACAO DATE NOT NULL,
                CONSTRAINT LOCACOES_PK PRIMARY KEY (DATA_DEVOLUCAO, PLACA, NOME_MODELO, NOME_MARCA, CPF)
);


ALTER TABLE LOCACOES ADD CONSTRAINT CLIENTES_LOCACOES_FK
FOREIGN KEY (CPF)
REFERENCES CLIENTES (CPF)
NOT DEFERRABLE;

ALTER TABLE MODELOS ADD CONSTRAINT MARCAS_MODELOS_FK
FOREIGN KEY (NOME_MARCA)
REFERENCES MARCAS (NOME_MARCA)
NOT DEFERRABLE;

ALTER TABLE AUTOMOVEIS ADD CONSTRAINT MODELOS_AUTOMOVEIS_FK
FOREIGN KEY (NOME_MARCA, NOME_MARCA)
REFERENCES MODELOS (NOME_MODELO, NOME_MARCA)
NOT DEFERRABLE;

ALTER TABLE LOCACOES ADD CONSTRAINT AUTOMOVEIS_LOCACOES_FK

/*Garante acesso total as tabelas*/
GRANT ALL ON CLIENTES TO LABDATABASE;
GRANT ALL ON MARCAS TO LABDATABASE;
GRANT ALL ON MODELOS TO LABDATABASE;
GRANT ALL ON AUTOMOVEIS TO LABDATABASE;
GRANT ALL ON LOCACOES TO LABDATABASE;

ALTER USER LABDATABASE quota unlimited on USERS;