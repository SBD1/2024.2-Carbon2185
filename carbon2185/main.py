from game.database import create_connection
from game.create_tables import create_tables
from game.gameplay import start_game
from game.dml import dml
from game.utils import display_message
from game.navegation import insert_initial_data
from game.triggers_procedures import trigger_procedure
import os

cores = {
    'vermelho': '\033[31m',
    'verde': '\033[32m',
    'amarelo': '\033[33m',
    'azul': '\033[34m',
    'magenta': '\033[35m',
    'ciano': '\033[36m',
    'branco': '\033[37m',
    'reset': '\033[0m'  # Reset para a cor padrão
}


def main():
    
    display_message(f"{cores['magenta']}Bem-vindo ao Carbon2185!{cores['reset']}")
    # Resto do código do menu principal...
    while True:
        print("\n")
        from colorama import Fore, Style

        with open("banner.txt", "r", encoding="utf-8") as file:
            banner = file.read()

        print(Fore.MAGENTA + banner + Style.RESET_ALL)  # Exibe em ciano

        print("\n")
        
        print(f"{cores['amarelo']} 1. {cores['reset']}Iniciar Jogo")
        print(f"{cores['amarelo']} 2. {cores['reset']}Sair\n")

        conn = create_connection()
        try:
            create_tables(conn)
            dml(conn)
            insert_initial_data(conn)
            trigger_procedure(conn)

            choice = input("Escolha uma opção: ") 
            print("\n")
            if choice == "1":
                start_game(conn)
                break
            elif choice == "2":
                os.system("cls" if os.name == "nt" else "clear")
                print("\n")
                print(f"{cores['magenta']}Saindo...{cores['reset']}\n")
                break
            else:
                print(f"{cores['vermelho']}Opção inválida!{cores['reset']}")
        
        finally:
            conn.close()

if __name__ == "__main__":
    main()
