# <center>Entrega do Trabalho 1 - Modelagem</center>

##  **MER - Modelo Entidade Relacionamento**

O Modelo Entidade-Relacionamento é uma abordagem conceitual que organiza as informações de um sistema, definindo entidades, seus atributos e os relacionamentos entre elas. Ele é essencial para compreender e estruturar os dados de forma lógica, servindo como base para o planejamento do banco de dados e a identificação das necessidades do projeto.

## **Entidades**

- Personagem
    - PC
    - NPC
        - Comerciante
        - Inimigo
- Inventário
- Missão
- Diálogo
- Item
    - Equipamento
        - Armadura
        - Arma
        - Implante cibernético
- Instância Item
- Facção
    - Yazuka
    - Triad
- Classe
    - Daimyo
    - Hacker
    - Scoundrel
- Distrito
- Célula do mundo
- Instância Inimigo
- Loja

## **Atributos**

- Personagem: [<ins>_id_personagem</ins>,tipo_]
    - PC: [<ins>_id_personagem</ins>,id_celula,id_faccao,id_classe,energia,dano,hp,hp_atual,nivel,xp,nome,descricao_]
    - NPC: [_<ins>_id_personagem</ins>,tipo_]
        - Comerciante: [_<ins>id_comerciante</ins>,id_personagem,id_celula,nome,descricao_]
        - Inimigo: [_<ins>id_inimigo</ins>,id_personagem,dano,xp,hp_] 
- Instância Inimigo: [_<ins>id_instancia_inimigo</ins>,id_inimigo,id_celula,hp_atual_]
- Inventário: [_<ins>id_inventario</ins>,id_istancia_item,quatidade_itens,capacidade_maxima_]
- Missão: [_<ins>id_missao</ins>,nome,descrição,dificuldade,objetivo_]
- Diálogo: [_<ins>id_interacao</ins>,mensagem_atual_]
- Item: [_<ins>id_item</ins>,tipo_]
    - Equipamento: [_<ins>id_item</ins>,tipo_]
        - Armadura: [_<ins>id_item</ins>,id_celula,nome,descricao,valor,hp_bonus,raridade_]
        - Arma: [_<ins>id_item</ins>,id_celula,nome,descricao,valor,raridade,municao,dano_]
        - Implante cibernético: [_<ins>id_item</ins>,id_celula,nome,descricao,valor,raridade,custo_energia,dano_]
- Instância Item: [_<ins>id_instancia_item</ins>,id_inventario,id_item]
- Facção: [_<ins>id_faccao</ins>,tipo_]
    - Yazuka: [_<ins>id_faccao</ins>,nome,descricao,ideologia_]
    - Triad: [_<ins>id_faccao</ins>,nome,descricao,ideologia_]
- Classe: [_<ins>id_classe</ins>,tipo_]
    - Daimyo [_<ins>id_classe</ins>,nome,descricao,hp_bonus,dano_bonus,energia_bonus_]
    - Hacker [_<ins>id_classe</ins>,nome,descricao,hp_bonus,dano_bonus,energia_bonus_]
    - Scoundrel: [_<ins>id_classe</ins>,nome,descricao,hp_bonus,dano_bonus,energia_bonus_]
- Distrito: [_<ins>id_distrito</ins>,nome,descricao,range_maximo,quantidade_personagens_] 
- Célula: [_<ins>d_celula</ins>,nome,id_distrito,descricao,destino_] 
- Célula do mundo: [_<ins>id_celula</ins>,id_disrito,nome,descricao,destino_]
- Loja: [_<ins>id_loja</ins>,id_comerciante,id_instancia_item_]


## **Relacionamentos**


- Personagem e Inventário
    - (1,1) Cada Personagem possui um único Inventário.
    - (1,1) Um Inventário pertence a um único Personagem.

- Personagem e Facção
    - (1,1) Cada Personagem pertence a uma única Facção.
    - (0,N) Uma Facção pode ter vários Personagens associados.

- Personagem e Classe

    - (1,1) Cada Personagem possui uma única Classe.
    - (0,N) Uma Classe pode ser associada a várias Personagens.

- Personagem e Background
    - (1,1) Cada Personagem possui um único Background.
    - (0,N) Um Background pode estar associado a várias Personagens.

- Personagem e Habilidade
    - (0,N) Uma personagem pode possuir várias habilidades.
    - (0,N) Uma habilidade pode pertencer a vários Personagens.

- Instância de Item e Item
    - (1,N) Um Item pode ter várias Instâncias de Item.
    - (1,1) Cada Instância de Item representa um único Item.

- Instância de Item e Inventário
    - (0,N) Um Inventário contém várias Instâncias de Item.
    - (1,1) Cada Instância de Item pertence a um único Inventário.
    - (0,N) Uma Instância de Item representa um Item.
    - (1,1) Um item pode ter várias instâncias.

- Célula e Distrito
    - (1,1) Uma célula pertence a um único distrito.
    - (0,N) Um distrito contém várias Células.

- Instância Inimigo e Célula
    - (1,1) Uma Instância Inimigo pode está em uma célula
    - (1,N) Uma Célula pode ter várias Instância Inimigo

- Negociação
    - (1,1) Uma negociação envolve um Mercador.
    - (0,N) Um Mercador pode realizar várias negociações
    - (1,1) Uma negociação envolve um PC.
    - (0,N) Um PC pode realizar várias negociações.

- PC e NPC
    - (N,N) Um PC interage com várias NPC
    - (N,N) Um NPC interage com vários PC

- NPC e Interação
    - (1,N) Um NPC pode ter várias Interações.
    - (1,1) Cada Interação envolve um único NPC.

- PC e Interação
    - (1,N) Um PC pode ter várias Interações.
    - (1,1) Cada Interação envolve um único PC.

- PC e Instância Inimigo
    - (1,N) Um PC consegue combater vários Instância Inimigo
    - (1,N) Um Inimigo Instância consegue ser combatido por vários PC

- Interação e Diálogo
    - (1,1) Uma Interação gera um único Diálogo.
    - (1,1) Cada Diálogo é gerado por uma única Interação.

- Combate e Instância Inimigo
    - (1,N) Um Combate pode envolver várias Instâncias de Inimigo.
    - (1,1) Cada Instância de Inimigo participa de um único Combate.

- Personagem e Distrito
    - (1,1) Cada Personagem está em um único Distrito.
    - (0,N) Um Distrito pode conter vários Personagens.

- Célula e Instancia de Item
    - (0,N) Uma Célula pode conter várias Instâncias de Itens.
    - (1,1) Cada Instância de Item está em uma única Célula.

- Personagem e Missão
    - (1,N) Um Personagem pode realizar várias Missões.
    - (1,1) Cada Missão é realizada por um único Personagem.

- Comerciante e Loja
    - (1,1) Cada Comerciante possui uma única Loja.
    - (1,1) Cada Loja é gerenciada por um único Comerciante.

- Facção e Distrito
    - (1,1) Uma Facção domina um único Distrito
    - (1,1) Um único Distrito é dominado por uma única Facção

