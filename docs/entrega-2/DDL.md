# <center>Entrega do Trabalho 2 - SQL</center>

## **DDL**

A DDL (Data Definition Language) é um subconjunto do SQL que é usado para definir a estrutura de um banco de dados, ou seja, ele lida com a criação e modificação dos objetos dentro de um banco de dados, como tabelas, visões (views), índices e esquemas. A DDL define como os dados serão armazenados e organizados no banco de dados, mas não lida diretamente com a manipulação ou consulta dos dados.

```sql

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
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    ideologia VARCHAR(100) NOT NULL
);

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

CREATE TABLE IF NOT EXISTS InventarioTemItem (
    id_inventario UUID REFERENCES Inventario(id_inventario),
    id_instancia_item UUID REFERENCES InstanciaItem(id_instancia_item)
    PRIMARY KEY (id_inventario, id_instancia_item)
);

CREATE TABLE IF NOT EXISTS InstanciaInimigo (
    id_instancia_inimigo UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_inimigo UUID REFERENCES Inimigo(id_inimigo),
    id_celula UUID REFERENCES CelulaMundo(id_celula),
    hp INT NOT NULL,
    hp_atual INT NOT NULL
);

CREATE TABLE IF NOT EXISTS Loja (
    id_comerciante UUID REFERENCES Comerciante(id_comerciante),
    id_instancia_item UUID REFERENCES InstanciaItem(id_instancia_item)
    PRIMARY KEY (id_comerciante, id_instancia_item)
);

```

<center>

## Histórico de Versão
| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: | 
| `1.0`  | 07/01/2025 | Primeira versão do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |
| `1.1`  | 08/01/2025 | Correção do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |
| `1.2`  | 09/01/2025 | Correção do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |
| `1.3`  | 14/01/2025 | Correção do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |

</center>