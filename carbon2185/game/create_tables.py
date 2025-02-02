from game.database import create_connection

SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS Inventario (
    id_inventario UUID DEFAULT uuid_generate_v4(),
    quantidade_itens INT NOT NULL,
    capacidade_maxima INT NOT NULL,
    dinheiro DECIMAL(10,2) NOT NULL DEFAULT 0,
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

INSERT INTO Faccao (id_faccao, tipo, nome, descricao, ideologia) 
SELECT uuid_generate_v4(), 'yakuza', 'Yakuza', 'máfia japonesa, conhecida por sua honra e disciplina.', 'Lealdade acima de tudo.'
WHERE NOT EXISTS (SELECT 1 FROM Faccao WHERE tipo = 'yakuza');

INSERT INTO Faccao (id_faccao, tipo, nome, descricao, ideologia) 
SELECT uuid_generate_v4(), 'triad', 'Triad', 'organização secreta chinesa, mestre do submundo.', 'O poder nasce da sombra.'
WHERE NOT EXISTS (SELECT 1 FROM Faccao WHERE tipo = 'triad');

CREATE TABLE IF NOT EXISTS Distrito (
    id_distrito UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    range_maximo INT NOT NULL,
    quantidade_personagens INT NOT NULL
);

CREATE TABLE IF NOT EXISTS CelulaMundo (
    id_celula UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_distrito UUID REFERENCES Distrito(id_distrito),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL
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
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS NPC (
    id_personagem UUID PRIMARY KEY REFERENCES Personagem(id_personagem),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('comerciante', 'inimigo'))
);

CREATE TABLE IF NOT EXISTS Comerciante (
    id_comerciante UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_personagem UUID REFERENCES NPC(id_personagem),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Inimigo (
    id_inimigo UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_personagem UUID REFERENCES NPC(id_personagem),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    dano INT NOT NULL,
    xp INT NOT NULL,
    hp INT NOT NULL,
    hp_atual INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Missao (
    id_missao UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    dificuldade INT NOT NULL,
    objetivo VARCHAR(100) NOT NULL
);

INSERT IGNORE INTO Missao (id_missao, nome, descricao, dificuldade, objetivo) VALUES
    (uuid_generate_v4(), 'Faxina na Periferia', 'A gangue Steel Fangs está aterrorizando os becos do distrito industrial.', 2, 'Eliminar 5 Steel Fangs'),
    (uuid_generate_v4(), 'Caçada aos Hackers', 'O grupo cyberterrorista Black Ice está hackeando servidores corporativos.', 3, 'Eliminar 5 Hackers Black Ice'),
    (uuid_generate_v4(), 'Limpeza na Zona Vermelha', 'A milícia Red Claws impõe sua lei com brutalidade.', 2, 'Eliminar 5 Patrulheiros Red Claws'),
    (uuid_generate_v4(), 'Roubo Mal-Sucedido', 'Um grupo de Neon Scavs assaltou um carregamento de implantes cibernéticos.', 3, 'Eliminar 5 Neon Scavs'),
    (uuid_generate_v4(), 'Predadores Noturnos', 'Um culto de assassinos conhecidos como Children of the Void está atacando civis.', 4, 'Eliminar 5 Children of the Void'),
    (uuid_generate_v4(), 'Os Oligarcas Não Perdoam', 'O sindicato de assassinos Ebony Hand falhou em um contrato e precisa ser eliminado.', 3, 'Eliminar 5 Assassinos Ebony Hand'),
    (uuid_generate_v4(), 'Terror Cibernético', 'Zero.exe, um hacker AI autoconsciente, está tomando o controle de sistemas de defesa.', 5, 'Derrotar Zero.exe'),
    (uuid_generate_v4(), 'Caçada ao Tyrant', 'Tyrant, um cyber-ogro modificado, lidera os Steel Fangs em massacres brutais.', 6, 'Derrotar Tyrant'),
    (uuid_generate_v4(), 'O Guardião do Labirinto', 'A megacorp Shinsei Biotech criou um super-soldado, Orion, para proteger seus segredos.', 7, 'Derrotar Orion'),
    (uuid_generate_v4(), 'Rei dos Bairros Baixos', 'Viper, um ex-executivo transformado em rei do crime, governa o submundo com punho de ferro.', 8, 'Derrotar Viper');

CREATE TABLE IF NOT EXISTS Interacao (
    id_interacao UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    personagem_origem UUID REFERENCES Personagem(id_personagem),
    personagem_destino UUID REFERENCES Personagem(id_personagem)
);

CREATE TABLE IF NOT EXISTS Dialogo (
    id_interacao UUID PRIMARY KEY REFERENCES Interacao(id_interacao),
    mensagem_atual VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Item (
    id_item UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('equipamento', 'objeto_mapa'))
);

CREATE TABLE IF NOT EXISTS Equipamento (
    id_item UUID PRIMARY KEY REFERENCES Item(id_item),
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('armadura', 'arma', 'implante_cibernetico'))
);

CREATE TABLE IF NOT EXISTS Armadura (
    id_item UUID PRIMARY KEY REFERENCES Equipamento(id_item),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    hp_bonus INT NOT NULL,
    raridade VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Arma (
    id_item UUID PRIMARY KEY REFERENCES Equipamento(id_item),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    raridade VARCHAR(100) NOT NULL,
    municao INT NOT NULL,
    dano INT NOT NULL
);

CREATE TABLE IF NOT EXISTS ImplanteCibernetico (
    id_item UUID PRIMARY KEY REFERENCES Equipamento(id_item),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    raridade VARCHAR(100) NOT NULL,
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
    hp INT NOT NULL,
    hp_atual INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Loja (
    id_loja UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_comerciante UUID REFERENCES Comerciante(id_comerciante),
    id_instancia_item UUID REFERENCES InstanciaItem(id_instancia_item)
);

CREATE TABLE IF NOT EXISTS ProgressoMissao (
    id_missao UUID PRIMARY KEY REFERENCES Missao(id_missao),
    id_personagem UUID PRIMARY KEY REFERENCES PC(id_personagem),
    progresso INT NOT NULL
);

CREATE OR REPLACE FUNCTION criar_progresso_missao()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO ProgressoMissao (id_missao, id_personagem, progresso)
    SELECT m.id_missao, NEW.id_personagem, 0
    FROM Missao m;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_criar_progresso_missao
AFTER INSERT ON PC
FOR EACH ROW
EXECUTE FUNCTION criar_progresso_missao();

"""

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute(SCHEMA_SQL)


    conn.commit()
    cursor.close()
