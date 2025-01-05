import numpy as np
from matplotlib.path import Path

# Compute the weighted centroid point of a Voronoi region based on image grayscale values
# gray_img is the preprocessed image
# random sampling = False -> Uses every pixel gray values of region to compute centroid
# random sampling = True -> Uses random sample of pixel gray values in region
# random sampling speeds up computation time, and adds slight jitter to each iteration
def get_density_centroid(vertices, gray_img,random_sampling = True):
    min_x, min_y = vertices.min(axis=0)
    max_x, max_y = vertices.max(axis=0)

    min_x = max(int(min_x), 0)
    max_x = min(int(max_x), gray_img.shape[1] - 1)
    min_y = max(int(min_y), 0)
    max_y = min(int(max_y), gray_img.shape[0] - 1)

    if random_sampling:
      # Faster runtime, plus the jitter dislodges stuck points
      num_samples=(max_x - min_x) * (max_y - min_y) * 10
      samples = np.random.uniform([min_x, min_y], [max_x, max_y], (num_samples, 2))
    else:
      # Computing based on every pixel within region
      x_coords = np.arange(min_x, max_x + 1)
      y_coords = np.arange(min_y, max_y + 1)
      xx, yy = np.meshgrid(x_coords, y_coords)
      samples = np.column_stack((xx.ravel(), yy.ravel()))

    # Check if each coordinate from samples is within the Voronoi region
    path = Path(vertices)
    coords_within = samples[path.contains_points(samples)]

    # If there are no coordinates within then return mean of vertices
    if len(coords_within) == 0:
        return vertices.mean(axis=0)

    # Rounding is for random sampling method, to get gray scale from nearest neighbor
    coords_within = np.round(coords_within).astype(int)
    weights = gray_img[coords_within[:, 1], coords_within[:, 0]]

    # Avoid dividing by 0, return mean of vertices
    if np.sum(weights) == 0:
        return vertices.mean(axis=0)

    # fastest way to compute (sum-of-all (coord * gray_val) / total )
    weighted_centroid = np.average(coords_within, axis=0, weights=weights)
    return weighted_centroid
