import pandas as pd
from tabulate import tabulate
import os
import csv
import shutil
import sys
import subprocess
import json

ascii_art_text = """
                                                            
                                ..::--==:.:                 
                          .::-=++**+==-.:*:   :-.           
                      .::==+****++=-::..*+:.:.         .    
                   .:-=+******+-:.   : .==-:.:          :   
                 :==+******+-:+      :.    ..           :   
               :++**+++==++:   :.       ...           ..    
      .++=-. .=***+=-:.   .::...:--:. ..           ...      
      .***++++**+-.       ..:-..... ..         ....         
       ****++*+-.    .-=******-   ..      ....              
       -*****+:    .********=. .:.                          
        =***+:       .::::. .:.                             
          =*-              --                               
          =+           :=-==-.                @Red Tables              
          :=         ::=*+=+=:                 by prowiz77            
     .     +       .-   .--+=                               
    .      .:      ==:   -***:                              
   :        ..    ..:::.=****.                              
   .          ..=- .     ***=                               
   .            +**+=.. :****.                              
   ..           .++.   :-+****-                             
     ....                :=****:                            
                           :+**=                            
                             :-:                            

"""

def restart_program():
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)

def copy_csv_to_current_directory(source_path):
    if not os.path.exists(source_path):
        print(f"Error: The source file '{source_path}' does not exist.")
        return None

    file_name, file_extension = os.path.splitext(os.path.basename(source_path))

    destination_name = f"{file_name}_data{file_extension}"
    destination_path = os.path.join(os.getcwd(), destination_name)

    try:
        shutil.copy(source_path, destination_path)
        print(f"File successfully copied to: {destination_path}")
        return destination_path
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")
        return None

def create_csv():
    project_name = input("Enter the project name: ")
    columns = input("Enter the column names separated by commas: ").split(',')
    columns = ['Name', *columns, 'Status']
    rows = []
    file_name = f"{project_name}_data.csv"
    project_path = os.path.abspath(file_name)
    with open(file_name, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(columns)
        writer.writerows(rows)
    
    return project_path

def get_project_path():
    csv_files = [file for file in os.listdir() if file.endswith('_data.csv')]

    project_options = []

    New = len(csv_files) + 1
    APp = len(csv_files) + 2

    if len(csv_files) >= 1:
        for i, file in enumerate(csv_files, start=1):
            project_options.append([f'\033[94m{i}\033[0m', f'\033[92m{file[:-9]}\033[0m'])

        project_options.extend([
            [f'\033[94m{New}\033[0m', '\033[93mnew\033[0m'],
            [f'\033[94m{APp}\033[0m', '\033[96mAdd Projekt path\033[0m']
        ])

        table = tabulate(project_options, headers=[f'\033[94m#\033[0m', '\033[92mProject Name                                      \033[0m'], tablefmt="fancy_outline", showindex=False)
        print("\033[1;31m" + ascii_art_text + "\033[0m")
        print("\033[1;31m" + table + "\033[0m")
    else:
        print("No projects available.")

    try:
        selection = input("\033[1;31m" + "  > " + "\033[0m")

        if selection.isdigit():
            selection = int(selection)

            if 1 <= selection <= len(csv_files):
                return csv_files[selection - 1]
            elif selection == New:
                project_path = create_csv()
                return project_path
            elif selection == APp:
                ptcsv = input("path: ")
                new_path = copy_csv_to_current_directory(ptcsv)
                return new_path
            else:
                print("!!! invalid !!!")
                return None
        else:
            print("Invalid entry. Please enter a number.")
            return None

    except ValueError:
        print("Invalid entry. Please enter a number.")
        return None



def display_table_with_editing(df, current_index_highlighted, current_index_arrow):
    os.system('clear' if os.name == 'posix' else 'cls')  


    columns_order = df.columns.tolist()
    table = tabulate(df[columns_order], headers='keys', tablefmt='fancy_grid', showindex=False)

    highlighted_table = ""
    for i, line in enumerate(table.split('\n')):
        if i == current_index_highlighted + 3:
            highlighted_table += "\033[1;37;41m" + line + "\033[0m\n" 
        else:
            highlighted_table += "\033[1;36m" + line + "\033[0m\n" 

    print("\033[1;31m" + ascii_art_text + "\033[0m")
    print(highlighted_table)
    print("\033[1;31m" + "\nUse 'w' to go up, 's' to go down, 'Enter' to edit, 'a' to add, 'r' to return, q' to quit" + "\033[0m")

def update_csv_row_red(csv_path, name_to_update):
    try:

        df = pd.read_csv(csv_path, header=None)


        mask = df[0].str.startswith(name_to_update)

        if mask.any():
            #If the name was found, change the value in the last column from '✅' to '❌'
            df.loc[mask, len(df.columns) - 1] = '❌'

            df.to_csv(csv_path, header=False, index=False)
            print(f"Die Zeile mit dem Namen '{name_to_update}' wurde erfolgreich aktualisiert.")
        else:
            print(f"Der Name '{name_to_update}' wurde nicht gefunden.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def update_csv_row_green(csv_path, name_to_update):
    try:

        df = pd.read_csv(csv_path, header=None)


        mask = df[0].str.startswith(name_to_update)

        if mask.any():
            #If the name was found, change the value in the last column from '❌' to '✅'
            df.loc[mask, len(df.columns) - 1] = '✅'

            
            df.to_csv(csv_path, header=False, index=False)
            print(f"The line with the name '{name_to_update}' has been successfully updated.")
        else:
            print(f"The name '{name_to_update}' was not found.")

    except Exception as e:
        print(f"An error has occurred: {e}")

def update_csv_row(csv_path, name_to_update, new_value):
    try:
        
        df = pd.read_csv(csv_path)

        
        mask = df['Name'].str.startswith(name_to_update)

        if mask.any():
            # If the name was found, change the value in the last column from '✅' to '❌'
            df.loc[mask, 'Status'] = new_value

            
            df.to_csv(csv_path, index=False)
            print(f"The line with the name '{name_to_update}' has been successfully updated.")
        else:
            print(f"The name '{name_to_update}' was not found.")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

def add_new_row(csv_path):
    try:
        df_header = pd.read_csv(csv_path, nrows=1)
        columns_order = df_header.columns.tolist()

        print("Column names:", columns_order)

        df = pd.read_csv(csv_path)

        new_row_data = {}
        for column in columns_order:
            if column == 'Status':
                new_value = input(f"{column} ('n' for ❌, 'y' for ✅): ").strip().lower()
                if new_value == 'n':
                    new_value = '❌'
                elif new_value == 'y':
                    new_value = '✅'
                else:
                    print("Ungültige Eingabe. Verwende '❌' als Standardwert.")
                    new_value = '❌'
            else:
                new_value = input(f"{column}: ")
            new_row_data[column] = new_value

        print("New row data:", new_row_data)

        df = pd.concat([df, pd.DataFrame([new_row_data])], ignore_index=True)

        df.to_csv(csv_path, index=False)
        print("New row was successfully added.")

        display_table_with_editing(df, 0, 0)

    except Exception as e:
        print(f"An error has occurred: {e}")

def get_config_path():
    current_directory = os.getcwd()
    config_path = os.path.join(current_directory, 'config.json')
    return config_path

def update_json_value(key, new_value):
    file_path = get_config_path()

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        data[key] = new_value
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    except Exception as e:
        print(f"An error occurred: {e}")

def get_json_value(key):
    file_path = get_config_path()
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        current_value = data.get(key)

        if current_value is not None:
            return current_value
        else:
            print(f"The key '{key}' does not exist in config.json.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    try:
        key_to_get = 'start_menu'
        current_value = get_json_value(key_to_get)

        if current_value == 1:
            project_file = get_project_path()
        elif current_value == 0:
            key_to_get2 = 'csv_file_path'
            project_file = get_json_value(key_to_get2)
        else:
            raise ValueError("Unexpected value for 'start_menu' in the config file.")

        if project_file is not None:
            
            df = pd.read_csv(project_file)

            current_index_highlighted = 0
            current_index_arrow = 0

            while True:
                display_table_with_editing(df, current_index_highlighted, current_index_arrow)

                key = input()
                if key == 'q':
                    update_json_value('start_menu', 1)
                    sys.exit()
                elif key == ' ':
                    print("\nEditing 'Status' value...\n")
                    current_value = df.at[current_index_arrow, 'Status']
                    new_value = '❌' if current_value == '✅' else '✅'
                    df.at[current_index_arrow, 'Status'] = new_value
                    current_value_Name = df.at[current_index_arrow, 'Name']
                    update_csv_row(project_file, current_value_Name, new_value)
                elif key == 'w':
                    current_index_highlighted = max(current_index_highlighted - 2, 0)
                    current_index_arrow = max(current_index_arrow - 1, 0)
                elif key == '':
                    current_index_arrow = min(current_index_arrow + 1, len(df) - 1)
                    current_index_highlighted = min(current_index_highlighted + 2, current_index_arrow * 2)
                elif key == 'a':
                    add_new_row(project_file)
                    update_json_value('start_menu', 0)
                    update_json_value('csv_file_path', project_file)
                    restart_program()
                elif key == 'r':
                    break

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        main()
