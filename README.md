# 2024.2-Carbon-2185

<div align="center">
      <img src="https://i.pinimg.com/736x/b3/ab/fc/b3abfc7354e0ae4873a021040e24b9a8.jpg" width="900px;" alt="Carbon2185"/><br>
</div>

<div align="left">
  <h2>Sobre o jogo</h2>
</div> 

• Carbon 2185 é um RPG de cyberpunk ambientado em um futuro distópico, no ano de 2185. Inspirado pelo universo de jogos como Cyberpunk 2020 e pela estética de obras como Blade Runner, Ghost in the Shell e Neuromancer, o jogo combina elementos clássicos do gênero cyberpunk com uma mecânica baseada no sistema d20, semelhante ao de Dungeons & Dragons 5ª Edição. Em Carbon 2185, os jogadores assumem o papel de mercenários, hackers, ciborgues e outros personagens que lutam para sobreviver em uma sociedade dominada por mega-corporações, tecnologia invasiva e uma alta criminalidade.
 
• O sistema de jogo coloca grande foco em combate tático, hackeamento e personalização dos personagens, permitindo que cada jogador modifique seu corpo com aprimoramentos cibernéticos e escolha habilidades que se alinhem ao estilo único do seu personagem.

<div align="left">
  <h2>Objetivo</h2>
</div> 

• Desenvolver um jogo no estilo Carbon 2185 com mecânicas básicas e ambientação textual, rodando exclusivamente no CMD.

<div align="left">
  <h2>Entrega dos módulos</h2>
</div> 

- Entrega do módulo 1

  - [Apresentação](./docs/entrega-1/Apresentação.md)
  - [Diagrama Entidade-Relacionamento](./docs/entrega-1/DER.md)
  - [Modelo Entidade-Relacionamento](./docs/entrega-1/MER.md)
  - [Modelo Relacional](./docs/entrega-1/ModeloRelacional.md)
  - [Dicionário de Dados](./docs/entrega-1/DD.md)

- Entrega do módulo 2

  - [Apresentação](./docs/entrega-2/Apresentação.md)
  - [Álgebra Relacional](./docs/entrega-2/AlgebraRelacional.md)
  - [Normalização](./docs/entrega-2/Normalização.md)
  - [DDL](./docs/entrega-2/DDL.md)
  - [DML](./docs/entrega-2/DML.md)
  - [DQL](./docs/entrega-2/DQL.md)

## 🎮 Intruções para executar o jogo

### Tecnologias necessárias

- **Docker**.
- **Docker Compose**.

### Comandos para rodar

1. **Clone o Repositório** 

```bash
git clone git@github.com:SBD1/2024.2-Carbon2185.git
```

1. **Acesse o diretório do jogo**

```bash
cd carbon2185
```

3. **Contruir as imagens Docker**

```bash
docker-compose build
```

4. **Rodar o App**

```bash
docker-compose run app
```

### Acessando o Banco de Dados

Para visualizar o banco de dados, você pode usar um cliente como o DBeaver. Utilize as credenciais do banco local, que podem ser encontradas no arquivo `game/database.py`. Certifique-se de usar o host localhost para a conexão com o banco.

<div align="left">
  <h2> Colaboradores </h2>
</div> 

<div align="center">
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/arthurfonsecaa">
        <img src="https://avatars.githubusercontent.com/u/169956243?v=4" width="100px;" alt="Foto de Arthur Fonseca no GitHub"/><br>
        <sub>
          <b>Arthur Fonseca</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/RudsonMartin">
        <img src="https://avatars.githubusercontent.com/u/185992135?v=4" width="100px;" alt="Foto de Rudson Martin no GitHub"/><br>
        <sub>
          <b>Rudson Martins</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/14luke08">
        <img src="https://avatars.githubusercontent.com/u/119440440?v=4" width="100px;" alt="Foto de Mateus Santos no GitHub"/><br>
        <sub>
          <b>Mateus Santos</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/lucascaldasb">
        <img src="https://avatars.githubusercontent.com/u/90349578?v=4" width="100px;" alt="Foto de Lucas Caldas no GitHub"/><br>
        <sub>
          <b>Lucas Caldas</b>
        </sub>
      </a>
    </td>
     <td align="center">
      <a href="https://github.com/DanNunes777">
        <img src="https://avatars.githubusercontent.com/u/101228207?v=4" width="100px;" alt="Foto de Daniel Nunes no GitHub"/><br>
        <sub>
          <b>Daniel Nunes</b>
        </sub>
      </a>
    </td>
</div>
