import pandas as pd
from tabulate import tabulate
import os
from pynput import keyboard


CSV_FILE_PATH = '/home/kali/Programming/data.csv'

def display_table_with_editing(df, current_index_highlighted, current_index_arrow):
    os.system('clear' if os.name == 'posix' else 'cls')  # Clear console screen

    # Hinzufügen der Spalten am Ende mit ">" für die aktuelle Zeile und "<" für die markierte Zeile
    df['Arrow'] = ['>' if i == current_index_arrow else '' for i in range(len(df))]
    #df['Highlighted'] = ['<' if i == current_index_highlighted else '' for i in range(len(df))]

    # Tabellarische Anzeige mit den zusätzlichen Spalten
    columns_order = ['Name', 'Tag', 'Amount', 'Updated', 'Active']
    table = tabulate(df[columns_order], headers='keys', tablefmt='fancy_grid', showindex=False)

    # Farbliche Hervorhebung der Zeile mit '<'
    highlighted_table = ""
    for i, line in enumerate(table.split('\n')):
        if i == current_index_highlighted + 3:
            #highlighted_table += "\033[1;37;42m" + line + "\033[0m\n"  # Grün hinterlegt
            highlighted_table += "\033[1;37;41m" + line + "\033[0m\n"  # Roter Hintergrund
        else:
            highlighted_table += "\033[1;33m" + line + "\033[0m\n" # Orange Text

    print_debug_output()
    print(highlighted_table)
    print("\nUse 'w' to go up, 's' to go down, 'Enter' to edit, 'q' to quit")

def update_csv_row_red(csv_path, name_to_update):
    try:
        # Lese die CSV-Datei in ein Pandas DataFrame
        df = pd.read_csv(csv_path, header=None)

        # Überprüfe, ob der Name in der ersten Spalte gefunden wird
        mask = df[0].str.startswith(name_to_update)

        if mask.any():
            # Wenn der Name gefunden wurde, ändere den Wert in der letzten Spalte von '✅' zu '❌'
            df.loc[mask, len(df.columns) - 1] = '❌'

            # Speichere die aktualisierte DataFrame in der CSV-Datei
            df.to_csv(csv_path, header=False, index=False)
            print(f"Die Zeile mit dem Namen '{name_to_update}' wurde erfolgreich aktualisiert.")
        else:
            print(f"Der Name '{name_to_update}' wurde nicht gefunden.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def update_csv_row_green(csv_path, name_to_update):
    try:
        # Lese die CSV-Datei in ein Pandas DataFrame
        df = pd.read_csv(csv_path, header=None)

        # Überprüfe, ob der Name in der ersten Spalte gefunden wird
        mask = df[0].str.startswith(name_to_update)

        if mask.any():
            # Wenn der Name gefunden wurde, ändere den Wert in der letzten Spalte von '✅' zu '❌'
            df.loc[mask, len(df.columns) - 1] = '✅'

            # Speichere die aktualisierte DataFrame in der CSV-Datei
            df.to_csv(csv_path, header=False, index=False)
            print(f"Die Zeile mit dem Namen '{name_to_update}' wurde erfolgreich aktualisiert.")
        else:
            print(f"Der Name '{name_to_update}' wurde nicht gefunden.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def print_debug_output():
    try:
        with open("/home/kali/Programming/Sorting_Algorithm_Plex/ascii.txt", "r") as debug_file:
            content = debug_file.read()
            red_content = "\033[1;31m" + content + "\033[0m"  # Rot gefärbt
            print(red_content)
    except FileNotFoundError:
        print("Debug output file not found.")

def main():
    try:
        # Specify column names
        column_names = ['Name', 'Tag', 'Amount', 'Updated', 'Active']

        # Read the CSV file into a Pandas DataFrame with specified column names
        df = pd.read_csv(CSV_FILE_PATH, names=column_names, header=None)

        current_index_highlighted = 0
        current_index_arrow = 0

        while True:
            display_table_with_editing(df, current_index_highlighted, current_index_arrow)

            key = input()
            
            if key == 'q':
                # Speichern und beenden, wenn 'q' gedrückt wird
                break
            elif key == ' ':
                # Enter key pressed, edit value
                print("\nEditing 'Active' value...\n")
                current_value = df.at[current_index_arrow, 'Active']
                new_value = '❌' if current_value == '✅' else '✅'
                df.at[current_index_arrow, 'Active'] = new_value
                if current_value == '✅':
                    current_value_Name = df.at[current_index_arrow, 'Name']
                    update_csv_row_red(CSV_FILE_PATH, current_value_Name)
                else:
                    current_value_Name = df.at[current_index_arrow, 'Name']
                    update_csv_row_green(CSV_FILE_PATH, current_value_Name)
            elif key == 'w':
                current_index_highlighted = max(current_index_highlighted - 2, 0)
                current_index_arrow = max(current_index_arrow - 1, 0)
            elif key == '':
                current_index_arrow = min(current_index_arrow + 1, len(df) -1)
                current_index_highlighted = min(current_index_highlighted + 2, current_index_arrow*2)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()