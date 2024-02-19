# NLP based Image Retrieval with CLIP and Annoy-Database

Enables fast and accurate image search through natural language queries.
Utilizes OpenAI's CLIP model for powerful cross-modal understanding of text and images.

## Guide: Installation and Preparation
I will explain it for Anaconda Spyder.
1. Download Anaconda: Go to the Anaconda website (https://www.anaconda.com/products/distribution)
   and download the version for your operating system (Windows, macOS, Linux).
2. Install Spyder in Anaconda: After successfully installing Anaconda,
   you can install Spyder via the Anaconda Navigator application.
3. Open Anaconda Prompt: The Anaconda Prompt is a command-line application
   that provides access to Anaconda and Python-specific commands.
4. Enter the following commands into the Anaconda Prompt or copy and paste them with a right-click:
   ```
   pip install clip
   pip install git+https://github.com/openai/CLIP.git  
   pip install torch Pillow annoy numpy
   ```
6. Once you have entered the commands and no error messages occur, the packages have been successfully installed.
7. Enter "spyder" into the Anaconda Prompt and press Enter to open Spyder.
8. Copy the code from GitHub and paste it into Spyder, or download it and open it in Spyder. GitHub Link:
9. If you don't have a specific database, you can start with your project.
   8.1. If you have a database, copy it and paste it into the specified location: Path: This PC - Disk - Users - Your username - Right-click on an empty field - Paste.
10. Run the code in Spyder. The Annoy library will be downloaded the first time.
   Now you can make inputs according to the requirements. 

## Important to note: 
If you want to load images into the library, you need to adjust the trees accordingly (Line 116):  
annoy db.build(Enter number from below)  
annoy_db.save(annoy_db_path)  

There should be a maximum of 250 to 400 images per tree. You can add more per tree,
but then the results may be worse or you will need to describe the images you are looking for more accurately.   
Therefore, I recommend 100 to 250 images for up to 100,000 images
and from 100,000 onwards, 250 to 400 images per tree. Please do not use decimal numbers; round to whole numbers.  
It is important to note that without CUDA (graphics card),
the computation will be performed on the CPU, which can take about one hour for 900 to 1300 images.

## Using the Code Guide
##### 1. What do you want to do?  
Select "Yes" to prepare your own images for search based on text.  
Select "No" to search the existing database based on your description.  
For this, you need to have the images stored in external or internal storage and insert prepared files with ".ann" and ".db" extensions into the following path: "Local Disk(C):\Users\Username" within the Username folder.  
Select "Info" to get brief explanations and then make a decision again.

##### 2.1. If choosing option ("Yes"):  
Input the path where your images are stored.  
Enter the name for the Annoy database.  
Enter the name for the SQLite database.  
*The names can be identical but must not be duplicated on your computer.  
Wait until the program prompts that encoding and saving are complete: "The images were successfully added." 

##### 2.2. If choosing option ("No"):  
Enter the name for the Annoy database.  
Enter the name for the SQLite database.  
*Beforehand, you must also save these files under the correct path (see "1").  

##### 3. Describe the desired image.  
You can write the description here. Recommendation: write the description in English for more precise results; other languages such as Japanese and German only work for simple sentences like "Airplane at the airport."  
Select "Info" to receive a brief explanation.  
Select "Exit" to quit the program.  

##### 5. Number of images/results:  
Here, you can choose how many results you wish to see, from 1 to 10.

##### 6. Save or display:  
Select "Yes" to save the results in separate folders. You can choose the location and folder name yourself.  
Select "No" to input the path where the images are stored, including USB sticks. Afterwards, the images will be displayed in Spyder under the "Plot" section.  

##### You will return to step 3. If you want to change or create databases, you must enter "Exit" and restart the program.  

## Example:   
"In the nightly silence of the airport, a passenger aircraft stands motionless beside the illuminated runway"
![GitHubBild](https://github.com/EasyTony1734/NLP_CLIP-ANNOY-Database/assets/115572886/bc4f5259-4ed9-4357-a48d-09a11d5a5b54)

## Now it's your turn! 
Here is a link to Google Drive: https://drive.google.com/drive/folders/1a0aRbvdcTmdlWK6IZTtBuQV-LuDBPbqR  
where you will find a few pictures. Simply download them and put them in a folder. Then prepare for the search. Just follow the instructions and at the end, try to describe one image in English. If you do everything correctly, given the effort of the images, you should see the precisely described image.   
### So good luck and have fun with it!
