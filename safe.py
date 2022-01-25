import sqlite3
import base64
import imageio
import cv2

PASSWORD = "080520" 

connect = input("Enter your password?\n")

while connect != PASSWORD:
    connect = input("Enter your password?\n")
    if connect == "q":
        break

if connect == PASSWORD:
    conn = sqlite3.connect('mysafe.db')
    try:
        conn.execute('''CREATE TABLE SAFE
            (FULL_NAME TEXT PRIMARY KEY NOT NULL,
            NAME TEXT NOT NULL,
            EXTENSION TEXT NOT NULL,
            FILES TEXT NOT NULL);''')
        print("Your safe has been created!\nWhat would you like to store in it today?")
    except:
        print("You have a safe, what would you like to do today?")

    while True:
        print(("\n"+ "*"*16))
        print("Commands:")
        print("q > quit the program")
        print("o > open a file")
        print("s > store a file")
        print(("*"*16))
        input_ = input(":")

        if input_ == "q":
            break

        if input_ == "o":
            #open the file
            file_type = input("What is the filetype of the file you want to open?\n:")
            file_name = input("What is the name of the file you want to open?\n:")
            FILE_ = file_name + "." + file_type

            cursor = conn.execute("SELECT * from SAFE WHERE FULL_NAME=" + '"' + FILE_ + '"')

            file_string = ""
            for row in cursor:
                file_string = row[3]
            with open(FILE_, 'wb') as f_output:
                print(file_string)
                f_output.write(base64.b64decode(file_string))

        if input_ == "s":
            #store the file
            PATH = input("Type in the full path to the file you want to store.\nExample: /home/mcking/filename.txt\n:")
            FILE_TYPES = {
                "txt": "TEXT",
                "java": "TEXT",
                "dart": "TEXT",
                "py": "TEXT",
                "jpg": "IMAGE",
                "png": "IMAGE",
                "jpeg": "IMAGE"
            }
            file_name = PATH.split("/")
            file_name = file_name[len(file_name) - 1]
            file_string = ""
            NAME = file_name.split(".")[0]
            EXTENSION = file_name.split(".")[1]
            try:
                EXTENSION = FILE_TYPES[EXTENSION]
            except:
                Exception()

            if EXTENSION == "IMAGE":
                IMAGE = cv2.imread(PATH)
                file_string = base64.b64encode(cv2.imencode('.jpg', IMAGE)[1]).decode()
            elif EXTENSION == "TEXT":
                file_string = open(PATH, "r").read()
                file_string = base64.b64encode(file_string.encode("utf-8")).decode("utf-8")
            EXTENSION = file_name.split(".")[1]

            command = 'INSERT INTO SAFE (FULL_NAME, NAME, EXTENSION, FILES) VALUES (%s, %s, %s, %s);' %('"' + file_name +'"', '"' + NAME +'"', '"' + EXTENSION +'"', '"' + file_string +'"')

            conn.execute(command)
            conn.commit()
