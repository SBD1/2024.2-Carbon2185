from game.database import create_connection
from game.create_tables import create_tables
from game.gameplay import start_game

def main():
    print("Bem-vindo ao Carbon2185!")
    print("1. Iniciar Jogo")
    print("2. Sair")

    conn = create_connection()
    try:
        create_tables(conn)

        choice = input("Escolha uma opção: ")
        if choice == "1":
            start_game(conn)
        elif choice == "2":
            print("Saindo...")
        else:
            print("Opção inválida!")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()
