# <center>Entrega do Trabalho 2 - SQL</center>

## **DDL**

A DDL (Data Definition Language) é um subconjunto do SQL que é usado para definir a estrutura de um banco de dados, ou seja, ele lida com a criação e modificação dos objetos dentro de um banco de dados, como tabelas, visões (views), índices e esquemas. A DDL define como os dados serão armazenados e organizados no banco de dados, mas não lida diretamente com a manipulação ou consulta dos dados.

```sql

BEGIN TRANSACTION;

CREATE TABLE Personagem (
    id_personagem INT PRIMARY KEY,
    tipo ENUM('pc', 'npc') NOT NULL
);

CREATE TABLE PC (
    id_personagem INT PRIMARY KEY REFERENCES Personagem(id_personagem),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    id_faccao INT REFERENCES Faccao(id_faccao),
    id_classe INT REFERENCES Classe(id_classe),
    id_inventario INT REFERENCES Inventario(id_inventario),
    energia INT NOT NULL,
    dano INT NOT NULL,
    hp INT NOT NULL,
    hp_atual INT NOT NULL,
    nivel INT NOT NULL,
    xp INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
);

CREATE TABLE NPC (
    id_personagem INT PRIMARY KEY REFERENCES Personagem(id_personagem),
    tipo ENUM('comerciante', 'inimigo') NOT NULL
);

CREATE TABLE Comerciante (
    id_comerciante INT PRIMARY KEY,
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE Inimigo (
    id_inimigo INT PRIMARY KEY,
    id_personagem INT REFERENCES Personagem(id_personagem),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    dano INT NOT NULL,
    xp INT NOT NULL,
    hp INT NOT NULL,
    hp_atual INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL
);

CREATE TABLE Missao (
    id_missao INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    dificuldade INT NOT NULL,
    objetivo VARCHAR(100) NOT NULL
);

CREATE TABLE Interacao (
    id_interacao INT PRIMARY KEY,
    personagem_origem INT REFERENCES Personagem(id_personagem),
    personagem_destino INT REFERENCES Personagem(id_personagem)
);

CREATE TABLE Dialogo (
    id_interacao INT PRIMARY KEY REFERENCES Interacao(id_interacao),
    mensagem_atual VARCHAR(100) NOT NULL,
);

CREATE TABLE Item (
    id_item INT PRIMARY KEY,
    tipo ENUM('equipamento', 'objeto_mapa') NOT NULL
);

CREATE TABLE Equipamento (
    id_item INT PRIMARY KEY REFERENCES Item(id_item),
    tipo ENUM('armadura', 'arma', 'implante_cibernetico') NOT NULL
);

CREATE TABLE Armadura (
    id_item INT PRIMARY KEY REFERENCES Equipamento(id_item),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    hp_bonus INT NOT NULL,
    raridade VARCHAR(100) NOT NULL
);

CREATE TABLE Arma (
    id_item INT PRIMARY KEY REFERENCES Equipamento(id_item),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    raridade VARCHAR(100) NOT NULL,
    municao INT NOT NULL,
    dano INT NOT NULL
);

CREATE TABLE ImplanteCibernetico (
    id_item INT PRIMARY KEY REFERENCES Equipamento(id_item),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    valor INT NOT NULL,
    raridade VARCHAR(100) NOT NULL,
    custo_energia INT NOT NULL,
    dano INT NOT NULL
);

CREATE TABLE InstanciaItem (
    id_instancia_item INT PRIMARY KEY,
    id_inventario INT REFERENCES Inventario(id_inventario),
    id_item INT REFERENCES Item(id_item)
);

CREATE TABLE Faccao (
    id_faccao INT PRIMARY KEY,
    tipo ENUM('yakuza', 'triad') NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    ideologia VARCHAR(100) NOT NULL
);

CREATE TABLE Classe (
    id_classe INT PRIMARY KEY,
    tipo ENUM('daimyo', 'hacker', 'scoundrel') NOT NULL,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    hp_bonus INT NOT NULL,
    dano_bonus INT NOT NULL,
    energia_bonus INT NOT NULL
);

CREATE TABLE Inventario (
    id_inventario INT,
    id_instancia_item INT REFERENCES InstanciaItem(id_instancia_item),
    PRIMARY KEY (id_inventario, id_instancia_item)
    quantidade_itens INT NOT NULL,
    capacidade_maxima INT NOT NULL,
);

CREATE TABLE Distrito (
    id_distrito INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    range_maximo INT NOT NULL,
    quantidade_personagens INT NOT NULL
);

CREATE TABLE CelulaMundo (
    id_celula INT PRIMARY KEY,
    id_distrito INT REFERENCES Distrito(id_distrito),
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
);

CREATE TABLE InstanciaInimigo (
    id_instancia_inimigo INT PRIMARY KEY,
    id_inimigo INT REFERENCES Inimigo(id_inimigo),
    id_celula INT REFERENCES CelulaMundo(id_celula),
    hp INT NOT NULL,
    hp_atual INT NOT NULL
);

CREATE TABLE Loja (
    id_loja INT PRIMARY KEY,
    id_comerciante INT REFERENCES Comerciante(id_comerciante),
    id_instancia_item INT REFERENCES InstanciaItem(id_instancia_item)
);


COMMIT;

```

<center>

## Histórico de Versão
| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: | 
| `1.0`  | 07/01/2025 | Primeira versão do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |
| `1.1`  | 08/01/2025 | Correção do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |
| `1.2`  | 09/01/2025 | Correção do DDL | [Lucas Caldas](https://github.com/lucascaldasb) |

</center>