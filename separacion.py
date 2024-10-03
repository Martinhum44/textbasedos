import time
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

de = "C:/Users/ernes/Downloads"
a = "C:/Users/ernes/OneDrive/102"
archivos = os.listdir(de)

extensiones = {
    "Image_Files": ['.jpg', '.jpeg', '.png', '.gif', '.jfif'],
    "Video_Files": ['.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.m4p', '.m4v', '.avi', '.mov'],
    "Document_Files": ['.pptx', '.xlsx', '.csv', '.pdf', '.txt'],
    "Setup_Files": ['.exe', '.bin', '.cmd', '.msi', '.dmg']
}


class FileMovementHandler(FileSystemEventHandler):
    def on_created(self, event):
        name, exetension = os.path.splitext(event.src_path)
        print("ext.items: "+str(extensiones))
        for key, value in extensiones.items():
            time.sleep(1)
            if exetension in value:
                file_name = os.path.basename(event.src_path)
                print("file_name: "+file_name)

                path1 = de + "/" + file_name
                path2 = a + "/" + key + "/"
                path3 = path2 + file_name

                time.sleep(1)

                if os.path.exists(path2):
                    print(f"Moviendo {name}....")
                    shutil.move(path1, path3)
                    time.sleep(1)
                else:
                    print("Creando directorio....")
                    os.makedirs(path2)
                    print(f"Moviendo {name}....")
                    shutil.move(path1, path3)
                    time.sleep(1)

handler = FileMovementHandler()

observer = Observer()
observer.schedule(handler,de,recursive=True)
observer.start()

try:
    while True:
        time.sleep(2)
        print("ejecutando...")
except KeyboardInterrupt:
    print("ejecutando...")