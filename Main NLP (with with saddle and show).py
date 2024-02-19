import os
import clip
import torch
from PIL import Image
from annoy import AnnoyIndex
import numpy as np
import sqlite3
import time
import matplotlib.pyplot as plt
import shutil

# Funktion zur Anzeige von Bildern
def show_image(image_path):
    img = Image.open(image_path)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

#Search for suitable image + time required
def find_matching_image_items(text, num_images=1, search_k_value=100):
    # Text encode
    text_features = model.encode_text(clip.tokenize([text]).to(device))
    start_time = time.time() 
    image_items = annoy_db.get_nns_by_vector(
        text_features.cpu().detach().numpy().squeeze(),
        num_images,
        search_k=search_k_value 
    )
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.4f} seconds")
    return image_items

#Function for querying the image path based on the found ID
def image_path_id(image_id, sqlite_db_path):
    connection = sqlite3.connect(sqlite_db_path)
    cursor = connection.cursor()

    #Querying the image path based on the ID
    cursor.execute("SELECT pfad FROM bilder WHERE id=?", (image_id,))
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return f"Image path for ID: {image_id} not found!"

#Function to query whether new data should be entered
def new_images_data():
    while True:
        user_input = input("\nWould you like to enter new data? (Yes/No) If you're unsure what you need, write 'Info'.\nYour enter: ").strip().lower()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        elif user_input == "info":
            print("If you want to search your own pictures, please enter 'Yes'. Prepare the path of the folder where the pictures are located and choose a name for the database, the names can be identical. Here, your databases will be saved at the end: 'Your Disc - Users - Username'.")
            print("If you have already encoded images, then save the databases under this path 'Your Disc - Users - Username' and then enter only the name of the database when querying. Now please enter 'No'.")
        else:
            print("Please enter 'Yes', 'No', or 'info'.")

def ask_save_to_folder():
    while True:
        user_input = input("Do you want to save the found images to a folder? (Yes/No): ").strip().lower()
        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Please enter 'Yes' or 'No'.")

#Function to create and copy images to a folder
def create_and_copy_images_to_folder(paths):
    folder_path = input("\nEnter the path where you want to create the folder to save the images:\n ").strip('"')
    folder_name = input("Enter the name of the folder where the images will be saved: ")
    folder_path = os.path.join(folder_path, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for path in paths:
        full_path = os.path.join(folder_path, os.path.basename(path))
        try:
            shutil.copyfile(path, full_path)
            print("The pictures were saved in the desired path and folder.")
        except FileNotFoundError:
            print("Error, pictures could not be saved.")
            
#Annoy database path
annoy_db_path = ""

#CLIP
device = "cuda" if torch.cuda.is_available() else "cpu"
model, transform = clip.load("ViT-L/14@336px", device)

#Create a new Annoy database
if new_images_data():
    #Image folder path
    image_folder_path = input("Enter the path to the image folder (e.g., '...\Pictures 15'):\n ")

    #Cleanse the path if there are quotation marks at the beginning or end
    image_folder_path = image_folder_path.strip('""')

    #User input for Annoy database path
    annoy_db_path = input("Enter the name of the Annoy database. (e.g., Test): ") + ".ann"

    #List of all image files in the folder
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    #Notification: number of images
    notification_interval = 1

    #Create a new Annoy database
    annoy_db = AnnoyIndex(model.encode_image(torch.zeros((1, 3, 336, 336)).to(device)).shape[1], 'angular')

    #SQLite database
    sqlite_db_path = input("Enter the path to the SQLite database (e.g., Test): ") + ".db"
    datenbank_pfad = sqlite_db_path
    verbindung = sqlite3.connect(datenbank_pfad)
    cursor = verbindung.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bilder (
            id INTEGER PRIMARY KEY,
            pfad TEXT NOT NULL
        )
    ''')
    verbindung.commit()

    #Encode all images one after the other
    for i, image_file in enumerate(image_files, 1):
        image_path = os.path.join(image_folder_path, image_file)

        image = transform(Image.open(image_path)).unsqueeze(0).to(device)
        image_features = model.encode_image(image)

        #Repeat vector
        existing_indices = annoy_db.get_nns_by_vector(image_features.cpu().detach().numpy().squeeze(), 1)
        if i in existing_indices:
            print(f"{image_file} The entry has already been added. Skip.")
            continue

        #Insert into Annoy database
        annoy_db.add_item(i, image_features.cpu().detach().numpy().squeeze())

        #Insert path into SQLite database
        cursor.execute("INSERT INTO bilder (pfad) VALUES (?)", (image_path,))

        #Notification:
        if i % notification_interval == 0:
            print(f"{i} The images were successfully added.")

    #Save
    annoy_db.build(2)
    annoy_db.save(annoy_db_path)

    verbindung.commit()
    verbindung.close()
else:
    # Benutzereingabe für Annoy-Datenbank-Pfad
    annoy_db_path = input("Enter the path to the Annoy database (e.g., Test): ") + ".ann"

    # Benutzereingabe für SQLite-Datenbank-Pfad
    sqlite_db_path = input("Enter the name of the SQLite database (e.g., Test): ") + ".db"
    datenbank_pfad = sqlite_db_path

    # Laden der Annoy-Datenbank
    annoy_db = AnnoyIndex(model.encode_image(torch.zeros((1, 3, 336, 336)).to(device)).shape[1], 'angular')
    annoy_db.load(annoy_db_path)

#Search loop
while True:
    query_text = input("Describe the image you are looking for. You can enter 'info' to learn more or 'exit' to close the program.\nYour enter: ")

    if query_text.lower() == 'exit':
        print("The search process has ended.")
        break
    elif query_text.lower() == "info":
        print("You can enter text in German/Japanese, but the accuracy will be much lower. If you want to search for images as described, please provide your description in English.")
        continue
    
    #Select number of images
    while True:
        try:
            num_images = int(input("Enter the number of desired images (1 to 10): "))
            if 1 <= num_images <= 10:
                break
            else:
                print("Please enter a number between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    print("You have selected to search for", num_images, "images.")

    result_image_items = find_matching_image_items(query_text, num_images)
    print("Result Image Items:", result_image_items)

    #Print paths for all found images
    paths = [image_path_id(result_image_item, datenbank_pfad) for result_image_item in result_image_items]
    
    # Wenn der Benutzer die Bilder nicht in einem Ordner speichern möchte
    if not ask_save_to_folder():
        # Benutzereingabe für den Ordnerpfad
        folder_path = input("Please enter the folder path where the images are located: ")
        folder_path = folder_path.strip('""')

        # Ergebnis-Bilder in Spyder anzeigen
        for result_image_item, path in zip(result_image_items, paths):
            full_path = os.path.join(folder_path, path)
            if os.path.exists(full_path):
                print("The image is being displayed.", full_path)
                show_image(full_path)
            else:
                print("The image path does not exist:", full_path)
    else:
        # Speichere die Bilder in einem Ordner
        create_and_copy_images_to_folder(paths)
