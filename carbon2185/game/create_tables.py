from game.database import create_connection

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS Inventario (
    id_inventario UUID DEFAULT uuid_generate_v4(),
    quantidade_itens INT NOT NULL,
    capacidade_maxima INT NOT NULL,
    PRIMARY KEY (id_inventario)
);

CREATE TABLE IF NOT EXISTS Classe (
    id_classe UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('daimyo', 'hacker', 'scoundrel')),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    hp_bonus INT NOT NULL,
    dano_bonus INT NOT NULL,
    energia_bonus INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Faccao (
    id_faccao UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('yakuza', 'triad')),
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(100) NOT NULL,
    ideologia VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Distrito (
    id_distrito UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(1000) NOT NULL UNIQUE,
    descricao TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS CelulaMundo (
    id_celula UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_distrito UUID NOT NULL REFERENCES Distrito(id_distrito) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT NOT NULL,
    eixoX INT NOT NULL,
    eixoY INT NOT NULL,
    local_x INT NOT NULL,
    local_y INT NOT NULL,
    
    CONSTRAINT unique_position UNIQUE (id_distrito, eixoX, eixoY)
);

CREATE TABLE IF NOT EXISTS Personagem (
    id_personagem UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('pc', 'npc'))
);

CREATE TABLE IF NOT EXISTS PC (
    id_personagem UUID PRIMARY KEY REFERENCES Personagem(id_personagem),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    id_faccao UUID REFERENCES Faccao(id_faccao),
    id_classe UUID REFERENCES Classe(id_classe),
    id_inventario UUID REFERENCES Inventario(id_inventario),
    energia INT NOT NULL,
    wonglongs INT NOT NULL, 
    dano INT NOT NULL,
    hp INT NOT NULL,
    hp_atual INT NOT NULL,
    nivel INT NOT NULL,
    xp INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(1000) NOT NULL
);

CREATE TABLE IF NOT EXISTS NPC (
    id_personagem UUID PRIMARY KEY REFERENCES Personagem(id_personagem),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('comerciante', 'inimigo'))
);

CREATE TABLE IF NOT EXISTS Comerciante (
    id_comerciante UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_personagem UUID REFERENCES NPC(id_personagem),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(1000) NOT NULL,
    descricao VARCHAR(1000) NOT NULL,

    CONSTRAINT unique_comerciante_nome UNIQUE (nome)
);

CREATE TABLE IF NOT EXISTS Inimigo (
    id_inimigo UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_personagem UUID REFERENCES NPC(id_personagem),
    dano INT NOT NULL,
    xp INT NOT NULL,
    hp INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(1000) NOT NULL,

    CONSTRAINT unique_inimigo_nome UNIQUE (nome)

);

CREATE TABLE IF NOT EXISTS Missao (
    id_missao UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(100) NOT NULL,
    dificuldade VARCHAR(100) NOT NULL,
    objetivo VARCHAR(100) NOT NULL,
    goal INT NOT NULL,
    recompensa INT NOT NULL
);
    
CREATE TABLE IF NOT EXISTS Interacao (
    id_interacao UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    personagem_origem UUID REFERENCES Personagem(id_personagem),
    personagem_destino UUID REFERENCES Personagem(id_personagem)
);

CREATE TABLE IF NOT EXISTS Dialogo (
    id_interacao UUID PRIMARY KEY REFERENCES Interacao(id_interacao),
    mensagem_atual VARCHAR(1000) NOT NULL
);

CREATE TABLE IF NOT EXISTS Item (
    id_item UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('arma', 'armadura', 'implantecibernetico', 'objeto_mapa')),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    raridade VARCHAR(100) NOT NULL,

     CONSTRAINT unique_item_nome UNIQUE (nome)
);

CREATE TABLE IF NOT EXISTS Armadura (
    id_item UUID PRIMARY KEY REFERENCES Item(id_item),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    hp_bonus INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Arma (
    id_item UUID PRIMARY KEY REFERENCES Item(id_item),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    municao INT NOT NULL,
    dano INT NOT NULL
);

CREATE TABLE IF NOT EXISTS ImplanteCibernetico (
    id_item UUID PRIMARY KEY REFERENCES Item(id_item),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    custo_energia INT NOT NULL,
    dano INT NOT NULL
);

CREATE TABLE IF NOT EXISTS InstanciaItem (
    id_instancia_item UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_inventario UUID REFERENCES Inventario(id_inventario),
    id_item UUID REFERENCES Item(id_item)
);

CREATE TABLE IF NOT EXISTS InstanciaInimigo (
    id_instancia_inimigo UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_inimigo UUID REFERENCES Inimigo(id_inimigo),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    hp_atual INT NOT NULL,

    CONSTRAINT unique_boss_per_district UNIQUE (id_inimigo, id_celula)

);

CREATE TABLE IF NOT EXISTS Loja (
    id_loja UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_comerciante UUID REFERENCES Comerciante(id_comerciante),
    id_instancia_item UUID REFERENCES InstanciaItem(id_instancia_item)
);


CREATE TABLE IF NOT EXISTS ProgressoMissao (
    id_missao UUID REFERENCES Missao(id_missao) ON DELETE CASCADE,
    id_personagem UUID REFERENCES PC(id_personagem) ON DELETE CASCADE,
    progresso INT NOT NULL,
    PRIMARY KEY (id_missao, id_personagem)
);

CREATE TABLE IF NOT EXISTS ArmaduraEquipada (
    id_personagem UUID PRIMARY KEY REFERENCES PC(id_personagem) ON DELETE CASCADE,
    id_armadura UUID REFERENCES Armadura(id_item) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ImplanteEquipado (
    id_personagem UUID PRIMARY KEY REFERENCES PC(id_personagem) ON DELETE CASCADE,
    id_implante UUID REFERENCES ImplanteCibernetico(id_item) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SalaRespawnInimigos (
    id_instancia UUID PRIMARY KEY,
    id_inimigo UUID REFERENCES Inimigo(id_inimigo) ON DELETE CASCADE,
    id_celula_origem UUID REFERENCES CelulaMundo(id_celula) ON DELETE CASCADE
);

"""

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(SCHEMA_SQL)
    conn.commit()
    cursor.close()
