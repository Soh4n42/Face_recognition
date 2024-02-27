import os
import cv2
import face_recognition
from pymongo import MongoClient
from PIL import Image
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def save_embedding():

    #loading the captured image file and handling error if the image fie doesnot exists
    try:
        image= face_recognition.load_image_file("captured_image.jpg")

    except FileNotFoundError:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error",FileNotFoundError )
    try:

        if image is not None:
            known_image = face_recognition.load_image_file('captured_image.jpg')
            known_encoding = face_recognition.face_encodings(known_image)[0]
        else:
           raise Exception(f'Error: Unable to read the image {image}')
        
    except Exception as e:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))


    try:
        known_encoding_list = known_encoding.tolist()
    except:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error","Please register image first" )



    # Create a connection
    client = MongoClient('localhost', 27017)

    # Accessing a database
    db = client['major']

    # Accessing a collection
    collection = db['embedd']

    document = {
        'embedding':known_encoding_list
        
    }
    result = collection.insert_one(document)

    # Print the unique identifier for the inserted document
    print(result.inserted_id)

    # Close the connection
    client.close()

    file = "captured_image.jpg"
    try:
        if os.path.exists(file):
            os.remove(file)
        else:
            raise Exception("The file does not exist")  
    except Exception as f:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", str(f))

save_embedding()