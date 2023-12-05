import os
from moviepy.editor import VideoFileClip
import csv
from datetime import datetime

class VideoInfo:
    def __init__(self, filename, resolution, size_mb):
        self.filename = filename
        self.resolution = resolution
        self.size_mb = size_mb

def write_to_csv(name, data, directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        csv_path = os.path.join(directory, f"{name}.csv")        
        with open(csv_path, 'a', newline='') as csv_file:
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
    
def create_csv_file(directory, name):
    header = ['Name', 'Resolution', 'Size', 'Added', 'Status']
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        csv_path = os.path.join(directory, f"{name}.csv")

        if os.path.isfile(csv_path):
            pass
        else:
            with open(csv_path, 'w', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(header)

            print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f'Die CSV-Datei "{name}.csv" wurde im Verzeichnis "{directory}" erstellt.')
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Erstellen/Überprüfen der CSV-Datei: {e}")

def join_path_and_name(directory, name):
    if os.path.exists(directory):
        result_path = os.path.join(directory, name)
        return result_path
    else:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f'Das Verzeichnis "{directory}" existiert nicht.')
        return None

class VideoInfo:
    def __init__(self, filename, resolution, size_mb):
        self.filename = filename
        self.resolution = resolution
        self.size_mb = size_mb

def write_to_csv(name, data, directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        csv_path = os.path.join(directory, f"{name}_data.csv")        
        with open(csv_path, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"An error occurred: {e}")

def delete_file(path, filename):
    file_path = os.path.join(path, f"{filename}_data.csv")
    try:
        os.remove(file_path)
        print("["+"\033[1;32m"+"  Ok  "+"\033[0m"+"]"+f'Datei {file_path} erfolgreich gelöscht.')
    except FileNotFoundError:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f'Datei {file_path} nicht gefunden.')
    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f'Fehler beim Löschen der Datei {file_path}: {e}')

def get_video_info(directory, categorie_folder_name, pwd):
    try:
        delete_file(pwd, categorie_folder_name)
        header = ['Name', 'Resolution', 'Size', 'Added', 'Status']
        write_to_csv(categorie_folder_name, [header], pwd)
        if not os.path.exists(directory):
            print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f'Das Verzeichnis "{directory}" existiert nicht.')
            return None
        
        video_info_list = []

        for filename in os.listdir(directory):
            full_path = os.path.join(directory, filename)

            if os.path.isfile(full_path):
                try:
                    clip = VideoFileClip(full_path)
                    resolution = f'{clip.size[0]}x{clip.size[1]}'  
                    size_bytes = os.path.getsize(full_path)
                    size_mb = size_bytes / (1024 ** 2)  
                    
                    short_filename = filename[:27] if len(filename) > 27 else filename

                    video_info = VideoInfo(short_filename, resolution, size_mb)
                    video_info_list.append(video_info)
                    clip.close()
                    print("["+"\033[1;34m"+"  Ok  "+"\033[0m"+"]"+f'Name: {short_filename}: Auflösung: {resolution}, Größe: {size_mb:.2f} MB'+"\033[0m")
                    cur_date = get_current_datetime()
                    Status = '✅'
                    data_to_write = [short_filename, resolution, f'{size_mb:.2f} MB', cur_date, Status]
                    write_to_csv(categorie_folder_name, [data_to_write], pwd)            
                except Exception as e:
                    print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Verarbeiten der Datei {filename}: {e}")

        return video_info_list

    except Exception as e:
        print("["+"\033[1;31m"+"  Ok  "+"\033[0m"+"]"+f"Fehler beim Abrufen der Videoinformationen: {e}")
        return None
