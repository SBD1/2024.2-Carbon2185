# <center>Algebra Relacional</center>

A álgebra relacional é uma linguagem matemática usada para manipular e consultar dados em bancos de dados relacionais. Foi introduzida como parte do modelo relacional, criado por Edgar F. Codd, e serve como uma base teórica para sistemas de gerenciamento de bancos de dados (SGBD) relacionais, como PostgreSQL, MySQL, e SQL Server.

# Consultas ao banco de dados do projeto:

## 1. Listar Personagens e Tipos

```sql
π id_personagem,tipo(Personagem)
```

## 2. Listar PCs com Atributos Detalhados

```sql
π id_personagem,nome,descricao,energia,dano,hp,hp_atual,nivel,xp(PC)
```

## 3. Listar NPCs Associados a Diálogos

```sql
πNPC.id_personagem,NPC.tipo,D.id_interacao,D.mensagem_atual((Interacao⋈personagem_origem=id_personagemNPC)⋈id_interacao=D.id_interacao Dialogo)
```

## 4. Obter Comerciantes e Suas Localizações

```sql
π C.id_comerciante,C.nome,C.descricao,CM.nome(Comerciante LEFT OUTER JOIN id_celula=id_celula CelulaMundo)
```

## 5. Consultar Inimigos em Células Específicas

```sql
π I.id_inimigo,I.nome,I.descricao,I.dano,I.xp,CM.nome(Inimigo LEFT OUTER JOIN id_celula=id_celula CelulaMundo)
```

## 6. Listar Missões Atribuídas a Personagens

```sql
πP.id_personagem,P.tipo,M.nome,M.descricao((Missao⋈personagem_destino=id_missaoInteracao)⋈personagem_origem=id_personagem Personagem)
```

## 7. Consultar Inventário de um Personagem Específico

```sql
πI.id_inventario,II.id_instancia_item,IT.tipo,CM.nome((Inventario⋈id_inventario=id_inventarioInstanciaItem)⋈id_item=id_item Item LEFT OUTER JOIN id_celula=id_celula CelulaMundo)
```

## 8. Listar Personagens e Suas Facções

```sql
π PC.nome,F.nome,F.ideologia(PC⋈id_faccao=id_faccao Faccao)
```

## 9. Exibir Lojas e Itens Disponíveis

```sql
πL.id_loja,C.nome,II.id_instancia_item,IT.tipo((Loja⋈id_comerciante=id_comercianteComerciante)⋈id_instancia_item=id_instancia_item(InstanciaItem⋈ id_item=id_item Item))
```

## 10. Relacionamentos Entre PCs e Instâncias de Inimigos

```sql
πPC.id_personagem,PC.nome,II.id_instancia_inimigo,I.nome,CM.nome((InstanciaInimigo⋈id_inimigo=id_inimigo Inimigo)⋈id_celula=id_celula(CelulaMundo⋈ id_celula=id_celula PC))
```

<center>

## Histórico de Versão
| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: | 
| `1.0`  | 13/01/2025 | Adiciona Algebra Relacional | [Arthur Fonseca](https://github.com/arthrfonsecaa) |

</center>