import os #for interacting with operating system
import json #for saving and loading data in JSON format
import shutil  #for copying files
from tkinter import Tk, Label, Button, Toplevel, StringVar, Entry  #Tkinter for GUI elements
from tkinter import colorchooser  #Tkinter color chooser dialog
from PIL import Image  #Pillow for  image processing
from sklearn.cluster import KMeans  # for performing k-means clustering on image colors 
import numpy as np  # For numerical operations, mainly arrays

# Define paths for dataset and output
DATASET_FOLDER = os.path.join(os.path.dirname(__file__), "image_data")  # path to the folder containing images 
JSON_FILE = os.path.join(os.path.dirname(__file__), "image_data.json")  # path to the JSON file where image data will be saved
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "matched_images")  #path where matched images will be saved 


def process_dataset():
    """Extract dominant colors from images and save them to a JSON file."""
    image_data = {}  # Dictionary to store image names and their corresponding dominant colors 
    for image_name in os.listdir(DATASET_FOLDER):  # Iterate over all files in the dataset folder
        if image_name.lower().endswith(('.png', '.jpg')):  # Process only image files with .png or .jpg extensions
            image_path = os.path.join(DATASET_FOLDER, image_name)  # Get the full path of the image
            try:
                img = Image.open(image_path).resize((100, 100))  # Open and resize image to 100 x 100 pixels
                pixels = np.array(img).reshape(-1, 3)  # Convert image into a 2D array of RGB pixels
                kmeans = KMeans(n_clusters=5, random_state=42).fit(pixels)  # use KMeans to find 5 dominant colors
                image_data[image_name] = kmeans.cluster_centers_.astype(int).tolist()  # Store dominant colors in the dictionary
                print(f"Processed: {image_name}")  # print success message for each image processed 
            except Exception as e:  # Handle errors while processing an image
                print(f"Failed to process {image_name}: {e}")
                
                
    #save extracted color data to a JSON file            
    with open(JSON_FILE, "w") as f:
        json.dump(image_data, f)
    print(f"Processed data saved to {JSON_FILE}")


def load_dataset():
    """Load processed data from JSON file."""
    if os.path.exists(JSON_FILE):   # check if the JSON file exists
        with open(JSON_FILE, "r") as f:
            return json.load(f)   #Load and return the data from the JSON file
    print("No processed data found. Please process the dataset first.")  # Print message if no data is available 
    return {}  # Return an empty dictionary if no data exists 


def hex_to_rgb(hex_color):
    """Convert HEX to RGB."""
    hex_color = hex_color.lstrip('#')   # Remove '#' from the beginning of the Hex code 
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  #covert Hex to RGB tuple


def match_images(user_color, threshold=60):
    """Find images with colors close to the selected color."""
    dataset = load_dataset()  # Load the dataset from the JSON file
    if not dataset:   # If the dataset is empty, return an empty List
        return []
    matches = []   # List to store names of matching images
    user_color = np.array(user_color)   #  convert user input color to a NumPy array for comparison
    for image_name, colors in dataset.items():  # Iterate over each image and its colors in the dataset
        for color in colors:    #  check each dominant color  for the image 
            #Calclate the Euclidean distance between the user color and the image's dominant color
            if np.linalg.norm(user_color - np.array(color)) < threshold:
                matches.append(image_name)  # If color is within threshold add image to matches
                break
    return matches   #  Return the list of images with matching colors 


def search_images():
    """Allow the user to select a color and find matching images."""
    def get_user_color():
        """Get color from user input or picker."""
        dialog = Toplevel(root)    # Create a new dialog window
        dialog.title("Select Color")   # Set title for the dialog window
        
        Label(dialog, text="Enter HEX code (#RRGGBB):").pack(pady=5)    #  Label for Hex code input 
        hex_var = StringVar()   # Variable to store Hex code
        Entry(dialog, textvariable=hex_var).pack(pady=5)   # Entry widget for Hex code input 

        def use_picker():
            """use the color picker dialog to select color"""
            rgb_color = colorchooser.askcolor()[0]   #  open color picker dialog
            if rgb_color:
                process_color(tuple(map(int, rgb_color)))  #covert selected color to RGB and process
            dialog.destroy()   # Close the dialog window

        def use_hex():
            """ Use the Hex code entered by the user"""
            hex_code = hex_var.get()    #  Get the Hex code from the entry widget 
            try:
                process_color(hex_to_rgb(hex_code))   #  Convert Hex to RGB and process
            except ValueError:
                print("Invalid HEX code.")  #  Error message for invalid  Hex code 
            dialog.destroy()  #close the dialog window

        
        #  Buttons to choose color via picker or Hex input 
        Button(dialog, text="Use Picker", command=use_picker).pack(side="left", padx=5, pady=10)
        Button(dialog, text="Use HEX", command=use_hex).pack(side="left", padx=5, pady=10)
        Button(dialog, text="Cancel", command=dialog.destroy).pack(side="left", padx=5, pady=10)

    def process_color(user_color):
        """Find and save matching images."""
        matches = match_images(user_color)   # Find images that match the selected color
        if not matches:
            print("No matches found.")  # Print message if no matching images are found
            return
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)    # create the output folder if it doesnt exist 
        for img_name in matches:   # for each matched image 
            src = os.path.join(DATASET_FOLDER, img_name)   # get source file path
            dest = os.path.join(OUTPUT_FOLDER, img_name)   #get destination file path
            try:
                shutil.copy(src, dest)   # Copy matched image to the output folder
                print(f"Copied: {img_name}")    #Print success message for each copied image
            except Exception as e:     #handle errors during file copying
                print(f"Error copying {img_name}: {e}")
        print(f"Matched images saved to {OUTPUT_FOLDER}")    #Print message after saving images

    get_user_color()    # Open the color selection dialog


def main():
    """Launch the Tkinter GUI."""
    global root
    root = Tk()    #Create the main Tkinter window
    root.title("Image Search by Color")  #set window title
    
    Label(root, text="Image Search by Color", font=("Helvetica", 16)).pack(pady=10)    #Label for the window 
    Button(root, text="Process Dataset", command=process_dataset, bg="blue", fg="white").pack(pady=10)
    Button(root, text="Search Images by Color", command=search_images, bg="green", fg="white").pack(pady=10)
    Button(root, text="Quit", command=root.quit, bg="red", fg="white").pack(pady=10)
    
    root.mainloop()     #  Start the Tkinter event loop to keep the window open

#Run the application when this script is executed
if __name__ == "__main__":
    main()
