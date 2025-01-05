import streamlit as st
import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt

# Function to convert image to grayscale
def convert_to_gray(image):
    """
    Converts the input image to grayscale.
    Args:
        image: PIL image object.
    Returns:
        grayscale image as numpy array.
    """
    img_array = np.array(image)  # Convert image to numpy array
    gray_image = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)  # Convert to grayscale using OpenCV
    return gray_image

# Function to calculate centroids of Voronoi regions
def calculate_centroids(vor):
    """
    Calculates the centroids of Voronoi regions based on the Voronoi diagram.
    Args:
        vor: Voronoi object containing vertices and regions.
    Returns:
        List of centroids for each Voronoi region.
    """
    centroids = []
    # Iterate through each region in the Voronoi diagram
    for region in vor.regions:
        if len(region) > 0 and -1 not in region:  # Avoid regions with no valid vertices
            # Get the polygon vertices of the Voronoi region
            polygon = [vor.vertices[i] for i in region]
            # Calculate the centroid of the polygon by averaging its vertices
            centroid = np.mean(polygon, axis=0)
            centroids.append(centroid)
    return centroids

# Function to generate stippled image
def generate_stippled_image(image, vor, density, radius=3):
    """
    Generates a stippled (dot-based) image using the Voronoi diagram.
    Args:
        image: The original image as a numpy array.
        vor: Voronoi object for stippling.
        density: A density map used for stippling, where lighter values indicate more dots.
        radius: The radius of each stipple point.
    Returns:
        A stippled image based on Voronoi regions.
    """
    stippled_image = np.ones_like(image, dtype=np.uint8) * 255  # Start with a white canvas

    # Calculate centroids of the Voronoi regions
    centroids = calculate_centroids(vor)

    # Draw stipples (black dots) at the centroids' locations
    for centroid in centroids:
        # Ensure that the centroid is within image bounds
        if 0 <= centroid[0] < stippled_image.shape[1] and 0 <= centroid[1] < stippled_image.shape[0]:
            # Draw a circle at the centroid's position (stippling the image)
            cv2.circle(stippled_image, (int(centroid[0]), int(centroid[1])), radius, (0, 0, 0), -1)

    return stippled_image


# Streamlit interface setup
st.title('Weight Voronoi Image Stippling')

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    gray_image = convert_to_gray(image)

    st.subheader("Grayscale Original Image")
    st.image(gray_image, caption="Grayscale Original Image")

    st.sidebar.subheader("Stippling Parameters")

    max_iter = st.sidebar.slider("Max Iterations for KMeans", min_value=1, max_value=1000,step=5, value=100)

    radius = st.sidebar.slider("Stippling Radius", min_value=1, max_value=10, value=3)

    num_points = st.sidebar.slider("Number of Points (Clusters)", min_value=500,step=100, max_value=2000, value=1000)

    algorithm = st.sidebar.selectbox("KMeans Algorithm", ['lloyd', 'elkan'])

    show_voronoi = st.sidebar.checkbox("Show Voronoi Diagram", value=False)

    if st.sidebar.button("Generate Stippled Image"):
        # Create a density map based on the grayscale image (inverted, so brighter areas have higher density)
        density = 1 - gray_image / 255.0
        height, width = density.shape
        y, x = np.indices((height, width))  # Create a grid of coordinates corresponding to each pixel
        points = np.c_[x.flatten(), y.flatten()]  # Flatten the grid of coordinates into a list of points

        # Perform KMeans clustering on the points, using density as a sample weight
        kmeans = KMeans(n_clusters=num_points, max_iter=max_iter, random_state=42, algorithm=algorithm)
        kmeans.fit(points, sample_weight=density.flatten())  # Fit KMeans with weighted points

        centroids = kmeans.cluster_centers_  # Obtain the centroids of the clusters

        # Create a Voronoi diagram from the KMeans centroids
        vor = Voronoi(centroids)

        # Generate a stippled image based on the Voronoi diagram and density
        stippled_image = generate_stippled_image(np.array(image), vor, density, radius=radius)

        st.subheader("Stippled Image")
        stippled_image_rgb = cv2.cvtColor(stippled_image, cv2.COLOR_BGR2RGB)  # Convert the stippled image back to RGB
        st.image(stippled_image_rgb)

        if show_voronoi:
            fig, ax = plt.subplots(figsize=(4, 4))
            voronoi_plot_2d(vor, ax=ax, show_vertices=False, show_edges=True) 
            plt.gca().invert_yaxis() 
            st.subheader("Voronoi Diagram")
            st.pyplot(fig) 