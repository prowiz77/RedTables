import os
import csv
from datetime import datetime
import pandas as pd
from get_video_info import get_video_info

def suche_in_csv(csv_datei, folder):
    try:
        with open(csv_datei, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  

            for row in csv_reader:
                if row[0] == folder:  
                    return True  

        return False  
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Lesen der CSV-Datei: {e}")
        return False

def liste_der_ordner(verzeichnis_pfad):
    ordner_liste = []
    try:
        with os.scandir(verzeichnis_pfad) as verzeichnis:
            for eintrag in verzeichnis:
                if eintrag.is_dir():
                    ordner_liste.append(eintrag.name)
        return ordner_liste
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Lesen des Verzeichnisses: {e}")
        return None

def liste_der_ordner2(verzeichnis_pfad):
    ordner_liste = []
    try:
        with os.scandir(verzeichnis_pfad) as verzeichnis:
            for eintrag in verzeichnis:
                if eintrag.is_file():
                    ordner_liste.append(eintrag.name)
        return ordner_liste
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Lesen des Verzeichnisses: {e}")
        return None

def write_to_csv(file_path, data):
    try:
        with open(file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"An error occurred: {e}")

def get_current_datetime():
    try:
        current_datetime = datetime.now()

        formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')

        return formatted_datetime
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"An error occurred: {e}")
        return None

def func(csv_datei, name, new_value):
    try:
        df = pd.read_csv(csv_datei)

        df.loc[df['Name'] == name, 'Amount'] = new_value

        df.to_csv(csv_datei, index=False)

        print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f"Der Wert von Amount für {name} wurde auf {new_value} geändert.")
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Aktualisieren der CSV-Datei: {e}")

def get_amount_value(csv_datei, name):
    try:
        df = pd.read_csv(csv_datei)

        row = df[df['Name'] == name]

        if not row.empty:
            current_value = row['Amount'].values[0]
            return current_value
        else:
            print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Keine Zeile mit dem Namen {name} gefunden.")
            return None
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Lesen der CSV-Datei: {e}")
        return None

def func_date(csv_datei, name, new_date):
    try:
        df = pd.read_csv(csv_datei)

        df.loc[df['Name'] == name, 'Updated'] = new_date

        df.to_csv(csv_datei, index=False)

        print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f"Der Wert von Update für {name} wurde auf {new_date} geändert.")
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Aktualisieren der CSV-Datei: {e}")

def create_csv_file(directory, name):
    header = ['Name', 'Resolution', 'Size', 'Added', 'Status']
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        csv_path = os.path.join(directory, f"{name}_data.csv")

        if os.path.isfile(csv_path):
            pass
        else:
            with open(csv_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(header)

            print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f'Die CSV-Datei "{name}.csv" wurde im Verzeichnis "{directory}" erstellt.')
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Erstellen/Überprüfen der CSV-Datei: {e}")

def write_to_csv99(file_path, data):
    try:
        with open(file_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"An error occurred: {e}")

def delete_file(path):
    file_path = os.path.join(path)
    try:
        os.remove(file_path)
        print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f'Datei {file_path} erfolgreich gelöscht.')
    except FileNotFoundError:
        print("["+"\033[1;33m"+"  Ok  "+"\033[0m"+"]"+f'Datei {file_path} nicht gefunden.')
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f'Fehler beim Löschen der Datei {file_path}: {e}')

def main(verzeichnis_pfad):
    current_dir = os.getcwd()
    csv_datei = os.path.join(current_dir, "data_data.csv")
    delete_file(csv_datei)
    data_to_write = ['Name', 'Tag', 'Amount', 'Updated', 'Status']
    write_to_csv99(csv_datei, [data_to_write])
    ordner_liste = liste_der_ordner(verzeichnis_pfad)
    if ordner_liste: 
        #print(len(ordner_liste))
        i = 0
        while i < len(ordner_liste):
            folder = ordner_liste[i]
            ergebnis = suche_in_csv(csv_datei, folder)
            if ergebnis:
                print(f'{folder} -> exists in {csv_datei}')
                i+=1
            else:
                print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f'{folder} -> wird {csv_datei} hinzugefuegt')
                i+=1
                tag = folder.lower()
                date = get_current_datetime()
                active = '✅'
                data_to_write = [folder, tag, 0, date, active]
                write_to_csv(csv_datei, [data_to_write])
            

            anzahl_elemente_in_unter_ordnern = os.path.join(verzeichnis_pfad, folder)
            ordner_liste2 = liste_der_ordner2(anzahl_elemente_in_unter_ordnern)
            if ordner_liste2:
                new_value = len(ordner_liste2)
                current_value = get_amount_value(csv_datei, folder)
                if current_value != new_value:
                    func(csv_datei, folder, new_value)

            new_date = get_current_datetime()
            func_date(csv_datei, folder, new_date)
            create_csv_file(verzeichnis_pfad, folder)
            get_video_info(anzahl_elemente_in_unter_ordnern, folder, verzeichnis_pfad)
        
        print("\033[1;35m"+"Finished"+"\033[0m")
    else:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f'Fehler beim Abrufen der Ordner im Verzeichnis {verzeichnis_pfad}.')

if __name__ == "__main__":
    main()