from ttkbootstrap import ttk
# from image_container_frame import load_image,save_image

def apply_styles(root, canvas):
    """
    Apply theme and general styles to the main application.
    """
    # Apply custom styles directly
    root.style.configure("TLabel", font=("Arial", 14))
    root.style.configure("TButton", font=("Helvetica", 12, "bold"), padding=5,cursor="hand2")
    root.style.configure("TCombobox", font=("Arial", 12), padding=5)
    root.style.configure("TScale", troughcolor="#ddd", sliderlength=20)
    root.style.configure("Frame", padding=10, relief="flat")
    
    # Handle Canvas styling separately with Tkinter
    canvas.config(bg="#f0f8ff", bd=2, relief="solid")

def create_load_button(parent, command, style):
    """Create a modern, stylish Load Image button with hover animation."""
    # Define a modern flat style
    style.configure(
        "ModernButton.TButton",
        font=("Helvetica", 14, "bold"),
        foreground="#ffffff",  # White text color
        background="#4CAF50",  # Flat green background
        borderwidth=0,  # No border for a clean look
        padding=(10, 10),  # Internal padding for height and width
    )

    # Define hover effects (slightly darker green)
    style.map(
        "ModernButton.TButton",
        background=[("hover", "#45a049")],  # Slightly darker green on hover
        foreground=[("hover", "#ffffff")],  # Text color remains white
        relief=[("pressed", "sunken")],  # Add a sunken effect when pressed
    )

    # Create the button with the custom style
    return ttk.Button(
        parent,
        text="Load Image",
        command=command,
        cursor="hand2",
        style="ModernButton.TButton",  # Use the modern button style
        width=12,  # Explicitly set the width
    )


def create_save_button(parent, command, style):
    """Create a stylish Save Image button with yellow background and hover effects."""
    # Define the yellow button style
    style.configure(
        "YellowButton.TButton",
        font=("Helvetica", 14, "bold"),
        foreground="#ffffff",  # White text
        background="#b58900",  # Yellow background
        borderwidth=1,  # Thin border
        bordercolor="#805f00",  # Slightly darker yellow for the border
        padding=(10, 10),  # Internal padding
    )

    # Define hover effects
    style.map(
        "YellowButton.TButton",
        background=[
            ("hover", "#8f6d00")  # Darker yellow on hover
        ],
        foreground=[
            ("hover", "#ffffff")  # Keep text white on hover
        ],
        relief=[
            ("pressed", "sunken")  # Add sunken effect when pressed
        ],
    )

    # Create the button with the custom style
    return ttk.Button(
        parent,
        text="Save Image",
        command=command,
        cursor="hand2",
        style="YellowButton.TButton",  # Use the yellow button style
        width=12  # Explicitly set the width
    )
