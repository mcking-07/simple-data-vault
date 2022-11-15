from getpass import getpass
import base64
import cv2
import imageio
import sqlite3

password = "080520"

password_check = getpass("Enter your password: ")

retry = 0
while password_check != password:
    if retry == 2:
        exit("Incorrect password entered multiple times. Exiting...")
    password_check = getpass("Incorrect password. Try again. \nEnter your password: ")
    retry += 1

conn = sqlite3.connect('vault.db')

try:
    command = 'CREATE TABLE VAULT (FULL_NAME TEXT PRIMARY KEY NOT NULL, NAME TEXT NOT NULL, EXTENSION TEXT NOT NULL, FILES TEXT NOT NULL);'
    conn.execute(command)
    print("Your vault has been created!\nWhat would you like to store in it today?")
except:
    print("You have a vault, what would you like to do today?")
    
while True:
    print("\n" + "*" * 17 + "\n" + "Simple Data Vault" + "\n" + "*" * 17)
    print("O - Open a file \nS - Store a file \nQ - Quit the program")
    ch = input(":").upper()

    match ch:
        case "Q":
            exit("Buh-bye...")
        
        case "O":
            file_type = input("Enter filetype: ")
            file_name = input("Enter filename: ")
            file = file_name + "." + file_type
            
            command = 'SELECT * from VAULT WHERE FULL_NAME=(%s);' %('"' + file + '"')
            cur = conn.execute(command)
            conn.commit()
            
            file_data = ""
            for row in cur:
                file_data = row[3]
            
            with open(file, 'wb') as file_out:
                print("File found. opened in encrypted mode: ", file_data)
                check_password = getpass("Enter your password to restore file to system: ")
                
                if check_password != password:
                    exit("Incorrect password. Exiting...")
                
                file_out.write(base64.b64decode(file_data))
                
        case "S":
            file_path = input("Type in the full path to the file you want to store\nExample: /home/mcking/filename.txt\n:")
            file_types = {
                ("dart", "java", "py", "txt"): "TEXT", 
                ("jpeg", "jpg", "png"): "IMAGE"
                }
            
            file_name = path.split("/")
            file_name = file_name[len(file_name) - 1]
            file_data = ""
            
            name = file_name.split(".")[0]
            extension = file_name.split(".")[1]
            
            try:
                extension_check = file_types[extension]
            except:
                Exception()
                
            match extension_check:
                case "IMAGE":
                    image = cv2.imread(path)
                    file_data = base64.b64encode(cv2.imencode('.jpg', image)[1]).decode()
                    
                case "TEXT":
                    file_data = open(path, "r").read()
                    file_data = base64.b64encode(file_data.encode("utf-8")).decode("utf-8")
                
            command = 'INSERT INTO VAULT (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' %('"' + file_name + '"', '"' + name + '"', '"' + extension + '"', '"' + file_data + '"')
            conn.execute(command)
            conn.commit()
            
            print("Files stored in vault.")
            check_password = getpass("Enter your password to delete file from system: ")    
            
            if check_password != password:
                exit("Incorrect password. Exiting...")
            
            os.remove(file_path)
            print("File deleted from system, successfully.\n")
