import face_recognition
import pymongo
from pymongo import MongoClient
import numpy as np
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def compare_embeddings():
    root = Tk()
    root.withdraw()

    try:
        image1 = face_recognition.load_image_file("verification_image.jpg")
        if image1 is None:
            raise Exception('Error: Unable to read the image "verification_image.jpg"')
        
        unknown_image = face_recognition.load_image_file('verification_image.jpg')
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    except FileNotFoundError as e:
        messagebox.showerror("Error", str(e))
        return
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return

    try:
        # Connect to the MongoDB database
        client = MongoClient('localhost', 27017)
        db = client['major']
        collection = db['embedd']

        # Retrieve the embeddings from the database
        embeddings = []
        for document in collection.find():
            embedding = np.array(document['embedding'])
            embeddings.append(embedding)

        # Compare the embeddings with others
        for embedding in embeddings:
            # Perform operations with the embedding as needed
            results = face_recognition.compare_faces([embedding], unknown_encoding, tolerance=0.4)
            
            if any(results):
                # Calculate the face distance (smaller distance means better match)
                face_distance = face_recognition.face_distance([embedding], unknown_encoding)[0]

                # Convert face distance to percentage match (adjust as needed)
                percentage_match = max(0, (1 - face_distance) * 100)

                if percentage_match < 70:
                    messagebox.showerror("Error", "Face is not matched")
                else:
                    print("Go to the next page")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        client.close()

        file = "verification_image.jpg"
        try:
            if os.path.exists(file):
                os.remove(file)
            else:
                raise Exception("The file does not exist")  
        except Exception as g:
            messagebox.showerror("Error", str(g))

# Call the function
compare_embeddings()
