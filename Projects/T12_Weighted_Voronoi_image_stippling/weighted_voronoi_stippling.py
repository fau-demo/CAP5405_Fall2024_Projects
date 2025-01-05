import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from scipy.spatial import Voronoi, voronoi_plot_2d
from matplotlib.animation import FuncAnimation, PillowWriter
from time import time
from preprocess_image import preprocess_image
from lloyds_method import lloyds_method_density

# voronoi_stipple brings all parts of generating the weighted Voronoi stipple together
# img_path: relative path to image within directory
# stipple_points: how many points will the weighted voronoi stipple have
# gray_levels: number of gray levels
def voronoi_stipple(img_path, stipple_points=5000, gray_levels=0, lloyd_iters=40, random_sampling=True, weight_scale=1,
                    plot=True, save=True,seed = 111):
    start = time() # Logging purposes
    # Load and preprocess image
    img = io.imread(img_path)
    adjusted_img = preprocess_image(img, gray_levels)
    height, width = adjusted_img.shape
    print("Completed: Image Preprocessing")

    # Randomly pick indices to place initial points based on gray values weights
    indices = np.arange(adjusted_img.size)
    weights = adjusted_img.flatten() ** weight_scale
    weights = weights / np.sum(weights)  # needs sum to 1 for np.random.choice()
    chosen_indices = np.random.choice(indices, size=stipple_points, p=weights)

    # Convert flattened indices back to [y,x] coordinates
    initial_points = np.array([[idx % width, idx // width] for idx in chosen_indices])
    print("Completed: Randomized Initial Point Selection")

    # Run Lloyd's Method and get a final_voronoi and history of the points
    final_voronoi, points_history = lloyds_method_density(initial_points, adjusted_img, iterations=lloyd_iters,
                                                                  random_sampling=random_sampling)
    fig_div = height / 7
    figure_size = (width / fig_div, 7)
    print("Completed: Weighted Voronoi Stippling Computation")
    if plot:
        img_file_name = img_path[img_path.rfind("/") + 1:]
        # Plot the original image
        fig1, ax1 = plt.subplots(figsize=figure_size)
        ax1.set_xlim(0, width)
        ax1.set_ylim(height, 0)
        ax1.imshow(img, cmap='gray', extent=[0, width, 0, height], origin='lower')
        ax1.set_xlim(0, width)
        ax1.set_ylim(height, 0)  # Invert y-axis for image coordinates
        ax1.set_title(f"{img_file_name}")
        plt.title(f"Original Image: {img_file_name}")
        plt.tight_layout()
        plt.show(block=False)
        print("Completed: Original Image Plot")

        # Plot the final Voronoi diagram
        fig, ax = plt.subplots(figsize=figure_size)
        ax.set_xlim(0, width)
        ax.set_ylim(height, 0)
        voronoi_plot_2d(final_voronoi, ax=ax, show_vertices=False, line_colors='blue', line_width=1, line_alpha=0.6)

        # Plot the final points
        ax.plot(final_voronoi.points[:, 0], final_voronoi.points[:, 1], 'ro', markersize=.8,
                label='Weighted Centroid Points')

        ax.set_xlim(0, width)
        ax.set_ylim(height, 0)  # Invert y-axis for image coordinates
        ax.set_title(f"Voronoi Diagram of {img_file_name}")
        plt.title(f"Weighted Voronoi Diagram with {stipple_points} points after {lloyd_iters} Iterations")
        plt.tight_layout()
        plt.show(block=False)
        print("Completed: Final Weighted Voronoi Diagram Plot")

        # Plot the stipple
        fig2, ax2 = plt.subplots(figsize=figure_size)
        ax2.plot(final_voronoi.points[:, 0], final_voronoi.points[:, 1], 'ko', markersize=2,
                 label='Weighted Centroid Points')

        ax2.set_xlim(0, width)
        ax2.set_ylim(height, 0)  # Invert y-axis for image coordinates
        plt.title(f"Weighted Voronoi Stippling with {stipple_points} points after {lloyd_iters} Iterations")
        plt.tight_layout()
        
        ax2.set_title(f" Weighted Voronoi Stipple of {img_file_name}")
        plt.show(block=False)
        print("Completed: Final Weighted Voronoi Stipple Plot")

    if save:
        # Making and saving the gif
        fig, ax = plt.subplots(figsize=figure_size)
        stipple_plot, = ax.plot([], [], 'ko', markersize=2)

        def init():
            stipple_plot.set_data([], [])
            return stipple_plot,

        def update(frame):
            ax.clear()
            ax.set_xlim(0, width)
            ax.set_ylim(height, 0)
            ax.set_title(f'Weighted Voronoi Stippling with {stipple_points} points, Iteration {frame}')
            current_points = points_history[frame]
            ax.plot(current_points[:, 0], current_points[:, 1], 'ko', markersize=2)
            plt.tight_layout()
            return stipple_plot,

        # Create the animation
        ani = FuncAnimation(fig, update, frames=len(points_history), init_func=init, blit=False, repeat=False)

        # Save the animation as a gif
        image_file_name = img_path[img_path.rfind("/") + 1: img_path.rfind(".")]
        gif_file_name = f'{image_file_name}_voronoi_stippled_{stipple_points}_{lloyd_iters}.gif'
        ani.save(gif_file_name,
                 writer=PillowWriter(fps=round(lloyd_iters / 5)))
        print(f"Saved {lloyd_iters} iteration gif as {gif_file_name} in current directory")
    end = time()
    print(f"Weighted Voronoi Stippling Completed in {round(end-start,3)} seconds")
    
def main():
  return 0

if __name__ == '__main__':
    main()
