# <center>Entrega do Trabalho 2 - SQL</center>

## **DDL**

A DDL (Data Definition Language) é um subconjunto do SQL que é usado para definir a estrutura de um banco de dados, ou seja, ele lida com a criação e modificação dos objetos dentro de um banco de dados, como tabelas, visões (views), índices e esquemas. A DDL define como os dados serão armazenados e organizados no banco de dados, mas não lida diretamente com a manipulação ou consulta dos dados.

```sql

BEGIN TRANSACTION;

CREATE TABLE Personagem (
    id_personagem SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE PC (
    id_personagem INT PRIMARY KEY REFERENCES Personagem(id_personagem),
    id_celula INT,
    id_faccao INT,
    id_classe INT,
    id_origem INT,
    id_background INT,
    habilidade_cibernetica BOOLEAN,
    habilidades TEXT,
    forca INT,
    destreza INT,
    constituicao INT,
    inteligencia INT,
    tecnologia INT,
    carisma INT,
    hp INT,
    hp_atual INT,
    nivel INT,
    nome VARCHAR(100),
    descricao TEXT
);

CREATE TABLE NPC (
    id_personagem INT PRIMARY KEY REFERENCES Personagem(id_personagem),
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE Comerciante (
    id_comerciante SERIAL PRIMARY KEY,
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_celula INT,
    nome VARCHAR(100),
    descricao TEXT
);

CREATE TABLE Inimigo (
    id_inimigo SERIAL PRIMARY KEY,
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_celula INT,
    forca INT,
    destreza INT,
    constituicao INT,
    inteligencia INT,
    tecnologia INT,
    carisma INT,
    nome VARCHAR(100),
    descricao TEXT
);

CREATE TABLE Missao (
    id_missao SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    dificuldade VARCHAR(50),
    objetivo TEXT
);

CREATE TABLE Dialogo (
    id_interacao SERIAL PRIMARY KEY,
    mensagem_atual TEXT,
    responsavel_mensagem VARCHAR(100)
);

CREATE TABLE Item (
    id_item SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE Coletavel (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    id_celula INT,
    nome VARCHAR(100),
    descricao TEXT,
    valor DECIMAL,
    raridade VARCHAR(50)
);

CREATE TABLE Equipamento (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE Armadura (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    id_celula INT,
    nome VARCHAR(100),
    descricao TEXT,
    valor DECIMAL,
    defesa INT,
    velocidade_ataque INT,
    raridade VARCHAR(50)
);

CREATE TABLE Arma (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    id_celula INT,
    nome VARCHAR(100),
    descricao TEXT,
    valor DECIMAL,
    raridade VARCHAR(50),
    municao INT,
    dano INT,
    alcance INT
);

CREATE TABLE ImplanteCibernetico (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    id_celula INT,
    nome VARCHAR(100),
    descricao TEXT,
    valor DECIMAL,
    raridade VARCHAR(50),
    custo_energia INT,
    dano INT,
    alcance INT
);

CREATE TABLE Faccao (
    id_faccao SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    ideologia TEXT,
    nivel_influencia INT,
    recursos TEXT
);

CREATE TABLE Classe (
    id_classe SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    pontos_vida_bonus INT
);

CREATE TABLE Distrito (
    id_distrito SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    distritos INT,
    range_maximo INT,
    quantidade_personagens INT
);

CREATE TABLE CelulaDoMundo (
    id_celula SERIAL PRIMARY KEY,
    id_distrito INT REFERENCES Distrito(id_distrito),
    nome VARCHAR(100),
    descricao TEXT,
    destino TEXT
);

CREATE TABLE InstanciaInimigo (
    id_instancia_inimigo SERIAL PRIMARY KEY,
    id_inimigo INT REFERENCES Inimigo(id_inimigo),
    id_celula INT REFERENCES CelulaDoMundo(id_celula),
    hp INT,
    hp_atual INT
);

CREATE TABLE Habilidade (
    id_habilidade SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    tipo_habilidade VARCHAR(50),
    descricao TEXT,
    custo_de_uso INT,
    dano INT,
    velocidade_movimento INT
);

CREATE TABLE Loja (
    id_loja SERIAL PRIMARY KEY,
    id_comerciante INT REFERENCES Comerciante(id_comerciante),
    id_instancia_item INT
);

-- Relacionamentos adicionais
CREATE TABLE PersonagemFacao (
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_faccao INT REFERENCES Faccao(id_faccao),
    PRIMARY KEY (id_personagem, id_faccao)
);

CREATE TABLE PersonagemHabilidade (
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_habilidade INT REFERENCES Habilidade(id_habilidade),
    PRIMARY KEY (id_personagem, id_habilidade)
);

CREATE TABLE PCNPC (
    id_pc INT REFERENCES PC(id_personagem),
    id_npc INT REFERENCES NPC(id_personagem),
    PRIMARY KEY (id_pc, id_npc)
);

CREATE TABLE Negociacao (
    id_negociacao SERIAL PRIMARY KEY,
    id_comerciante INT REFERENCES Comerciante(id_comerciante),
    id_pc INT REFERENCES PC(id_personagem)
);

CREATE TABLE PCInstanciaInimigo (
    id_pc INT REFERENCES PC(id_personagem),
    id_instancia_inimigo INT REFERENCES InstanciaInimigo(id_instancia_inimigo),
    PRIMARY KEY (id_pc, id_instancia_inimigo)
);

CREATE TABLE InteracaoDialogo (
    id_interacao INT REFERENCES Dialogo(id_interacao),
    id_npc INT REFERENCES NPC(id_personagem),
    id_pc INT REFERENCES PC(id_personagem),
    PRIMARY KEY (id_interacao, id_npc, id_pc)
);

CREATE TABLE Inventario (
    id_inventario SERIAL PRIMARY KEY,
    id_personagem INT REFERENCES Personagem(id_personagem)
);

CREATE TABLE InstanciaItem (
    id_instancia_item SERIAL PRIMARY KEY,
    id_item INT REFERENCES Item(id_item),
    id_inventario INT REFERENCES Inventario(id_inventario),
    id_celula INT REFERENCES CelulaDoMundo(id_celula)
);

CREATE TABLE PersonagemMissao (
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_missao INT REFERENCES Missao(id_missao),
    PRIMARY KEY (id_personagem, id_missao)
);

COMMIT;

```

<center>

## Histórico de Versão
| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: | 
| `1.0`  | 07/01/2025 | Primeira versão do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |

</center>