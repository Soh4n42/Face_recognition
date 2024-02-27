import cv2
import face_recognition
from PIL import Image
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def open_camera_for_verification():
    try:  
    # Create a video capture object for the front camera
        vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
       #check if camera is opened or not
        if not vid.isOpened():
           raise Exception("Error: Could not open front camera.")
       
       # Set the resolution of the camera
        vid.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)





        # Continuously capture and display the video frames
        while True:
            # Capture frame-by-frame
            ret, frame = vid.read()

            if not ret:
                raise Exception("Error: Failed to capture frame.")

            # Display the resulting frame
            cv2.imshow('frame', frame)
            key = cv2.waitKey(1)

            # If the key is 'space', save the image and exit the loop
            if key == ord(' '):
                cv2.imwrite('verification_image.jpg', frame)
                break
            # If the key is 'e', exit the loop without saving the image
            elif key == ord('e'):
                break


    except Exception as e:
    # Display error message in a dialog box
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", str(e))

    finally:
        vid.release()
        cv2.destroyAllWindows()

open_camera_for_verification()