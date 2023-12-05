import os
from list_folders2 import main
import sys

def menu():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(" ______________________________")
    print("|                              |")
    print("|"+"\033[1;32m"+"        Update Database"+"\033[0m"+"       |")
    print("|                              |")
    print("+-----+------------------------+")
    print("| ["+"\033[1;34m"+"u"+"\033[0m"+"] |"+"\033[1;34m"+ " Update"+"\033[0m"+"                 |")
    print("+-----+------------------------+")
    print("| ["+"\033[1;33m"+"e"+"\033[0m"+"] |"+"\033[1;33m"+ " Exit"+"\033[0m"+"                   |")
    print("+-----+------------------------+")    

def main2():
    while True:
        menu()

        update_script = input("   > ")

        if update_script == "u":
            menu()
            verzeichnis_pfad = input("folder path > ")
            os.system('clear' if os.name == 'posix' else 'cls')
            main(verzeichnis_pfad)
            break
        elif update_script == "e":
            sys.exit(0)
        else:
            print("Invalid choice.")
