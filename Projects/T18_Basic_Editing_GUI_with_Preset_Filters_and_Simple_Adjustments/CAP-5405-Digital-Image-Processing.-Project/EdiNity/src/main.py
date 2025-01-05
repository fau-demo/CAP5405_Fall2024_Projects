import tkinter as tk
from splash_screen import show_splash_screen

def main():
    # Initialize the main application window
    root = tk.Tk()
    root.geometry("1350x750")  # Set the window size to 1350x750 pixels
    root.title("Edinity - Photo Editing App")  # Set the title of the application window

    # Show the splash screen
    # This function handles the transition from the splash screen to the main application
    show_splash_screen(root)

    # Run the main event loop
    # This keeps the application running and responsive to user input
    root.mainloop()

# Entry point of the application
# Executes the main function when the script is run directly
if __name__ == "__main__":
    main()
