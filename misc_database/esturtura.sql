SELECT DATABASE (tcc)

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL, 
    tipo_perfil ENUM('CLIENTE', 'PROFISSIONAL', 'ADMIN') NOT NULL,
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    nome_completo VARCHAR(255) NOT NULL,
    telefone VARCHAR(20),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


CREATE TABLE profissionais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    nome_fantasia VARCHAR(255) NOT NULL, 
    documento VARCHAR(20) UNIQUE NOT NULL, 
    telefone VARCHAR(20),
    descricao_servicos TEXT,
    aprovado_pelo_admin BOOLEAN DEFAULT FALSE, 
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);


CREATE TABLE categorias_servico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(255)
);

-
CREATE TABLE chamados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT NOT NULL,
    profissional_id INT, 
    categoria_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao_problema TEXT NOT NULL,
    status ENUM('ABERTO', 'EM_ORCAMENTO', 'EM_ANDAMENTO', 'CONCLUIDO', 'CANCELADO') DEFAULT 'ABERTO',
--     criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id),
    FOREIGN KEY (categoria_id) REFERENCES categorias_servico(id)
);


CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profissional_id INT NOT NULL,
    nome_item VARCHAR(255) NOT NULL,
    quantidade_estoque INT DEFAULT 0,
    preco_unitario DECIMAL(10, 2),
    FOREIGN KEY (profissional_id) REFERENCES profissionais(id) ON DELETE CASCADE
);
