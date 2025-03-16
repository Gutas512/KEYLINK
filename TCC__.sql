CREATE DATABASE db_chaves;

USE db_chaves;

CREATE TABLE salas (
    id_sala INT PRIMARY KEY,
    numero_sala INT NOT NULL,
    tipo_de_sala VARCHAR(255) NOT NULL
);


CREATE TABLE chaves (
    id_chaves INT PRIMARY KEY,
    salas_id_sala INT NOT NULL,
    FOREIGN KEY (salas_id_sala) REFERENCES salas(id_sala)
);

CREATE TABLE funcionarios (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome_funcionario VARCHAR(255) NOT NULL,
    usuario_funcionario VARCHAR(255) NOT NULL,
    telefone_funcionario VARCHAR(20),
    endereco_funcionario VARCHAR(255),
    funcao_funcionario VARCHAR(255),
    cpf_funcionario VARCHAR(14) NOT NULL,
    senha VARCHAR(128) NOT NULL,
    tipo_funcionario VARCHAR(20) NOT NULL DEFAULT 'Quadro',
    CONSTRAINT chk_tipo_funcionario CHECK (tipo_funcionario IN ('Quadro', 'Extra Quadro'))
);



CREATE TABLE registro_saida (
    id_registro VARCHAR(45) PRIMARY KEY,
    chaves_id_chaves INT NOT NULL,
    funcionarios_id_funcionario INT NOT NULL,
    registro_saida_horario DATETIME NOT NULL,
    FOREIGN KEY (chaves_id_chaves) REFERENCES chaves(id_chaves),
    FOREIGN KEY (funcionarios_id_funcionario) REFERENCES funcionarios(id_funcionario)
);


CREATE TABLE registro_entrada (
    id_registro_entrada INT AUTO_INCREMENT PRIMARY KEY,
    registro_saida_id_registro VARCHAR(45) NOT NULL,
    chaves_id_chaves INT NOT NULL,
    funcionarios_id_funcionario INT NOT NULL,
    registro_entrada_horario DATETIME NOT NULL,
    FOREIGN KEY (registro_saida_id_registro) REFERENCES registro_saida(id_registro),
    FOREIGN KEY (chaves_id_chaves) REFERENCES chaves(id_chaves),
    FOREIGN KEY (funcionarios_id_funcionario) REFERENCES funcionarios(id_funcionario)
);


