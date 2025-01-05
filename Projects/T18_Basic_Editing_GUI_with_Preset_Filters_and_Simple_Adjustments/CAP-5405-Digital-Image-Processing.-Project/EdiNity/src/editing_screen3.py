import tkinter as tk
from tkinter import messagebox, Toplevel, Scale, HORIZONTAL
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter
from shared import add_logo, create_menu  # Import shared utilities

# Define the main editing screen class
class EditingScreen:
    def __init__(self, root, uploaded_image_path=None):
        """
        Initialize the EditingScreen class.
        Parameters:
        - root: The root window for the application.
        - uploaded_image_path: Path to the image uploaded by the user.
        """
        self.root = root  # Root window
        self.canvas = None  # Canvas for displaying images
        self.uploaded_image_path = uploaded_image_path  # Path of the image to load
        self.original_image = None  # Original image (PIL object)
        self.current_image = None  # Currently displayed image (PIL object)
        self.history = []  # Stack to store history for undo functionality
        self.future = []  # Stack to store redo states
        self.crop_active = False  # Boolean flag for crop tool activation
        self.init_ui()  # Initialize the user interface

    def init_ui(self):
        """
        Set up the user interface for the editing screen.
        Includes layout for top buttons, canvas, and bottom toolbar.
        """
        self.root.config(bg="#EEECE7")  # Set background color for the root window

        # Clear any existing widgets in the root window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add top buttons
        self.add_top_buttons()

        # Add canvas for displaying images
        self.canvas = tk.Canvas(self.root, width=1400, height=650, bg="#EEECE7", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add bottom toolbar
        self.add_toolbar()

        # Schedule the display of the uploaded image (delayed to ensure canvas dimensions are initialized)
        self.root.after(100, self.display_image)

    def add_top_buttons(self):
        """
        Add a row of top buttons including logo, Undo, Redo, and Save.
        """
        # Create a frame for the top buttons
        top_buttons_frame = tk.Frame(self.root, bg="#EEECE7")
        top_buttons_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

        # Add the application logo
        logo_path = "assets/logo_head.png"
        logo_label = tk.Label(top_buttons_frame, bg="#EEECE7")
        logo_image = Image.open(logo_path).resize((100, 50), Image.ANTIALIAS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label.config(image=logo_photo)
        logo_label.image = logo_photo  # Keep a reference to prevent garbage collection
        logo_label.pack(side=tk.LEFT, padx=10)

        # Configure the button styling
        button_config = {
            "bg": "#444",  # Background color
            "fg": "white",  # Foreground/text color
            "font": ("Arial", 12, "bold"),  # Font styling
            "padx": 10,  # Horizontal padding
        }

        # Add Undo button
        undo_button = tk.Button(
            top_buttons_frame, text="Undo", command=self.undo_action, **button_config
        )
        undo_button.pack(side=tk.RIGHT, padx=10)

        # Add Redo button
        redo_button = tk.Button(
            top_buttons_frame, text="Redo", command=self.redo_action, **button_config
        )
        redo_button.pack(side=tk.RIGHT, padx=10)

        # Add Save button
        save_button = tk.Button(
            top_buttons_frame, text="Save", command=lambda: print("Save clicked"), **button_config
        )
        save_button.pack(side=tk.RIGHT, padx=10)

        # Add a hamburger menu button
        menu_canvas = tk.Canvas(top_buttons_frame, width=30, height=30, bg="#EEECE7", bd=0, highlightthickness=0)
        menu_canvas.create_line(5, 7, 25, 7, fill="black", width=3)
        menu_canvas.create_line(5, 15, 25, 15, fill="black", width=3)
        menu_canvas.create_line(5, 23, 25, 23, fill="black", width=3)
        menu_canvas.pack(side=tk.RIGHT, padx=10)

        # Bind click event to the hamburger menu for creating a dropdown menu
        menu_canvas.bind(
            "<Button-1>",
            lambda e: create_menu(self.root, x=menu_canvas.winfo_rootx(), y=menu_canvas.winfo_rooty() + 40),
        )

    def display_image(self):
        """
        Display the uploaded image on the canvas, ensuring it fits within the canvas dimensions.
        """
        if self.uploaded_image_path:
            try:
                # Open the uploaded image
                self.original_image = Image.open(self.uploaded_image_path)

                # Get canvas dimensions
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()

                # Resize logic and further implementation are continued...


                # Adjust dimensions to fit within the canvas
                image_width, image_height = self.original_image.size
                max_width = canvas_width
                max_height = canvas_height - 100  # Leave space for buttons and toolbar

                resize_ratio = min(max_width / image_width, max_height / image_height, 1)
                new_width = int(image_width * resize_ratio)
                new_height = int(image_height * resize_ratio)

                resized_image = self.original_image.resize((new_width, new_height), Image.ANTIALIAS)
                self.current_image = resized_image  # Save the resized image
                self.history.append(resized_image.copy())  # Add to history for undo functionality

                # Convert to PhotoImage and display centered
                tk_image = ImageTk.PhotoImage(resized_image)
                x_offset = (canvas_width - new_width) // 2
                y_offset = (canvas_height - new_height) // 2

                self.canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=tk_image)
                self.canvas.image = tk_image  # Keep reference to avoid garbage collection
            except FileNotFoundError:
                tk.Label(self.canvas, text="Image Not Found", font=("Arial", 16), fg="black", bg="#EEECE7").place(x=50, y=50)
        else:
            tk.Label(self.canvas, text="No Image Uploaded", font=("Arial", 16), fg="black", bg="#EEECE7").place(x=50, y=50)

    def add_toolbar(self):
        """Add the toolbar with editing tools as popup buttons."""
        toolbar_height = 50  # Fixed height for the toolbar
        self.canvas.config(height=600 - toolbar_height)  # Adjust canvas height to fit toolbar

        # Create the toolbar frame
        toolbar_frame = tk.Frame(self.root, bg="#2D3030", height=toolbar_height)
        toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Define the tools with their actions and icons
        tools = [
            ("Crop", self.show_crop_menu, "assets/crop.png"),
            ("Adjust", self.show_adjust_menu, "assets/controller.png"),
            ("Filters", self.show_filters_menu, "assets/filter.png"),
            ("Effects", self.show_effects_menu, "assets/beauty.png"),
            ("Reset", self.reset_tool, "assets/circular.png"),
        ]

        for tool_name, tool_action, icon_path in tools:
            try:
                # Load and resize tool icon
                icon = Image.open(icon_path).resize((40, 40), Image.ANTIALIAS)
                icon_photo = ImageTk.PhotoImage(icon)

                # Create a button for the tool
                tool_button = tk.Canvas(
                    toolbar_frame, width=40, height=40, bg="#2D3030", bd=0, highlightthickness=0
                )
                tool_button.create_image(20, 20, image=icon_photo)
                tool_button.image = icon_photo  # Keep a reference to avoid garbage collection
                tool_button.pack(side=tk.LEFT, padx=20, pady=5)

                tool_button.bind("<Button-1>", lambda e, action=tool_action: action())
            except FileNotFoundError:
                print(f"Icon not found for tool: {tool_name}")

    def update_canvas(self):
        """Refresh the canvas to display the current image."""
        if self.current_image:
            self.canvas.delete("all")
            canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
            image_width, image_height = self.current_image.size

            resize_ratio = min(canvas_width / image_width, canvas_height / image_height, 1)
            new_width = int(image_width * resize_ratio)
            new_height = int(image_height * resize_ratio)

            resized_image = self.current_image.resize((new_width, new_height), Image.ANTIALIAS)
            tk_image = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image((canvas_width - new_width) // 2, (canvas_height - new_height) // 2, anchor=tk.NW, image=tk_image)
            self.canvas.image = tk_image  # Keep reference to avoid garbage collection

    def show_crop_menu(self):
        """Display the crop menu with options."""
        x, y = self.root.winfo_pointerxy()
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Crop", command=self.activate_crop_tool)
        menu.add_command(label="Rotate", command=lambda: print("Rotate selected"))
        menu.post(x, y)

    def show_adjust_menu(self):
        """Display the adjust menu with sliders for real-time updates."""
        adjust_window = Toplevel(self.root)
        adjust_window.title("Adjust Image")
        adjust_window.geometry("400x300")

        # Brightness Slider
        tk.Label(adjust_window, text="Brightness").pack()
        brightness_slider = Scale(adjust_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL)
        brightness_slider.set(1.0)
        brightness_slider.pack()

        # Contrast Slider
        tk.Label(adjust_window, text="Contrast").pack()
        contrast_slider = Scale(adjust_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL)
        contrast_slider.set(1.0)
        contrast_slider.pack()

        # Saturation Slider
        tk.Label(adjust_window, text="Saturation").pack()
        saturation_slider = Scale(adjust_window, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL)
        saturation_slider.set(1.0)
        saturation_slider.pack()

        def update_adjustments(*args):
            brightness = brightness_slider.get()
            contrast = contrast_slider.get()
            saturation = saturation_slider.get()
            adjusted_image = ImageEnhance.Brightness(self.original_image).enhance(brightness)
            adjusted_image = ImageEnhance.Contrast(adjusted_image).enhance(contrast)
            adjusted_image = ImageEnhance.Color(adjusted_image).enhance(saturation)
            self.current_image = adjusted_image
            self.update_canvas()

        brightness_slider.bind("<Motion>", update_adjustments)
        contrast_slider.bind("<Motion>", update_adjustments)
        saturation_slider.bind("<Motion>", update_adjustments)

    def show_filters_menu(self):
        menu = tk.Menu(self.root, tearoff=0)

        def apply_filter(filter_type):
            try:
                if filter_type == "Black & White":
                    # Convert to Black & White
                    self.current_image = self.current_image.convert("L").convert("RGB")
                elif filter_type == "Sepia":
                    # Apply Sepia filter
                    sepia_image = self.current_image.convert("RGB")
                    pixels = sepia_image.load()
                    for x in range(sepia_image.width):
                        for y in range(sepia_image.height):
                            r, g, b = pixels[x, y]
                            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                            pixels[x, y] = min(tr, 255), min(tg, 255), min(tb, 255)
                    self.current_image = sepia_image
                elif filter_type == "Vintage":
                    # Apply Vintage filter by reducing color depth
                    self.current_image = ImageOps.posterize(self.current_image, 3)

                # Add the modified image to history
                self.history.append(self.current_image.copy())
                self.update_canvas()
                self.show_message(f"{filter_type} filter applied successfully.")
            except Exception as e:
                self.show_message(f"Error applying {filter_type}: {str(e)}")

        # Add menu commands for filters
        menu.add_command(label="Black & White", command=lambda: apply_filter("Black & White"))
        menu.add_command(label="Sepia", command=lambda: apply_filter("Sepia"))
        menu.add_command(label="Vintage", command=lambda: apply_filter("Vintage"))

        # Display the menu at the pointer location
        x, y = self.root.winfo_pointerxy()
        menu.post(x, y)


    def show_effects_menu(self):
        menu = tk.Menu(self.root, tearoff=0)

        def apply_effect(effect_type):
            try:
                if effect_type == "Blur":
                    # Apply Gaussian Blur with a realistic effect
                    self.current_image = self.current_image.filter(ImageFilter.GaussianBlur(10))  # Increased blur for realism
                elif effect_type == "Sharpen":
                    # Apply a refined Sharpen effect
                    self.current_image = self.current_image.filter(ImageFilter.UnsharpMask(radius=2, percent=200, threshold=3))
                elif effect_type == "Vignette":
                    # Create a realistic vignette effect with smooth transitions
                    vignette = Image.new("L", self.current_image.size, 0)
                    gradient = vignette.load()
                    for x in range(vignette.width):
                        for y in range(vignette.height):
                            dx = x - vignette.width / 2
                            dy = y - vignette.height / 2
                            distance = (dx * dx + dy * dy) ** 0.5
                            max_distance = max(vignette.width, vignette.height) / 2
                            gradient[x, y] = int(255 * (1 - min(1, distance / max_distance)))
                    vignette = vignette.resize(self.current_image.size, Image.ANTIALIAS)
                    self.current_image = Image.composite(self.current_image, ImageOps.colorize(vignette, "black", "white"), vignette)

                # Add the modified image to history
                self.history.append(self.current_image.copy())
                self.update_canvas()
                self.show_message(f"{effect_type} effect applied successfully.")
            except Exception as e:
                self.show_message(f"Error applying {effect_type}: {str(e)}")

        # Add menu commands for effects
        menu.add_command(label="Blur", command=lambda: apply_effect("Blur"))
        menu.add_command(label="Sharpen", command=lambda: apply_effect("Sharpen"))
        menu.add_command(label="Vignette", command=lambda: apply_effect("Vignette"))

        # Display the menu at the pointer location
        x, y = self.root.winfo_pointerxy()
        menu.post(x, y)


    def activate_crop_tool(self):
        """Activate the crop tool only when selected."""
        if not self.crop_active:
            self.crop_active = True
            self.canvas.bind("<Button-1>", self.start_crop)
            self.canvas.bind("<B1-Motion>", self.update_crop)
            self.canvas.bind("<ButtonRelease-1>", self.finish_crop)
            messagebox.showinfo("Crop", "Drag to select the area to crop.")

    def deactivate_crop_tool(self):
        """Deactivate the crop tool."""
        self.crop_active = False
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def start_crop(self, event):
        """Start the cropping rectangle."""
        if self.crop_active:
            self.start_x, self.start_y = event.x, event.y
            self.rect_id = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2
            )

    def update_crop(self, event):
        """Update the cropping rectangle as the user drags."""
        if self.crop_active:
            self.canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def finish_crop(self, event):
        """Finalize cropping and update the image."""
        if self.crop_active:
            end_x, end_y = event.x, event.y
            crop_box = (
                max(0, min(self.start_x, end_x)),
                max(0, min(self.start_y, end_y)),
                min(self.canvas.winfo_width(), max(self.start_x, end_x)),
                min(self.canvas.winfo_height(), max(self.start_y, end_y)),
            )

            if self.current_image:
                # Convert crop_box to relative coordinates in the image
                image_width, image_height = self.original_image.size
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()

                x_ratio = image_width / canvas_width
                y_ratio = image_height / canvas_height

                adjusted_box = (
                    int(crop_box[0] * x_ratio),
                    int(crop_box[1] * y_ratio),
                    int(crop_box[2] * x_ratio),
                    int(crop_box[3] * y_ratio),
                )

                # Ensure the adjusted crop box is within image bounds
                adjusted_box = (
                    max(0, adjusted_box[0]),
                    max(0, adjusted_box[1]),
                    min(image_width, adjusted_box[2]),
                    min(image_height, adjusted_box[3]),
                )

                if adjusted_box[2] > adjusted_box[0] and adjusted_box[3] > adjusted_box[1]:
                    cropped = self.original_image.crop(adjusted_box)
                    self.current_image = cropped
                    self.history.append(cropped.copy())

                    resized_cropped = cropped.resize((500, 400), Image.ANTIALIAS)
                    tk_cropped = ImageTk.PhotoImage(resized_cropped)

                    self.canvas.delete("all")
                    self.canvas.create_image(
                        self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                        anchor=tk.CENTER, image=tk_cropped
                    )
                    self.canvas.image = tk_cropped  # Update reference to avoid garbage collection

                    save_prompt = messagebox.askyesno(
                        "Crop", "Do you want to save the cropped image?")

                    if save_prompt:
                        cropped.save("cropped_image.png")
                        messagebox.showinfo("Save", "Cropped image saved successfully.")
                    else:
                        # Revert to the last state
                        self.current_image = self.history[-2] if len(self.history) > 1 else self.original_image
                        resized_previous = self.current_image.resize((500, 400), Image.ANTIALIAS)
                        tk_previous = ImageTk.PhotoImage(resized_previous)
                        self.canvas.delete("all")
                        self.canvas.create_image(
                            self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                            anchor=tk.CENTER, image=tk_previous
                        )
                        self.canvas.image = tk_previous
                else:
                    messagebox.showerror("Error", "Invalid crop area selected.")

                self.deactivate_crop_tool()

    def reset_tool(self):
        """Reset the image to its original state."""
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.history = [self.original_image.copy()]  # Reset history

            resized_original = self.original_image.resize((500, 400), Image.ANTIALIAS)
            tk_original = ImageTk.PhotoImage(resized_original)

            self.canvas.delete("all")
            self.canvas.create_image(
                self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2, anchor=tk.CENTER, image=tk_original
            )
            self.canvas.image = tk_original  # Update reference to avoid garbage collection
            messagebox.showinfo("Reset", "Image reset to original.")

    def undo_action(self):
        """Undo the last action."""
        if len(self.history) > 1:
            self.future.append(self.history.pop())  # Move current state to future stack
            self.current_image = self.history[-1]

            self.update_canvas()
        else:
            messagebox.showinfo("Undo", "No more actions to undo.")

    def redo_action(self):
        """Redo the last undone action."""
        if self.future:
            self.current_image = self.future.pop()
            self.history.append(self.current_image)

            self.update_canvas()
        else:
            messagebox.showinfo("Redo", "No more actions to redo.")
