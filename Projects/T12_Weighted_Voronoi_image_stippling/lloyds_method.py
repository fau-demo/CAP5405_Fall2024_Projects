import numpy as np
from scipy.spatial import Voronoi
from get_density_centroid import  get_density_centroid

# Lloyd's algorithm to generate centroidal Voronoi diagrams using gray value density
# points: precomputed list of coordinates where the initial points will be
# gray_img: preprocessed image to be used by get_density_centroid()
# iterations: cycles of computing centroids and recomputing weighted Vornonoi
# random_sampling: determines sampling method for get_density_centroid()
def lloyds_method_density(points, gray_img, iterations=10,random_sampling = True):
    #Initial computation of Voronoi
    vor = Voronoi(points)
    points_history = [points]
    for iter in range(iterations):
        new_points = []

        # Calculating density weighted centroids each Voronoi region
        for i, region_index in enumerate(vor.point_region):
            region = vor.regions[region_index]
            if -1 in region or len(region) == 0:
                new_points.append(points[i]) # If region goes out of bounds
                continue

            centroid = get_density_centroid(vor.vertices[region], gray_img,random_sampling)

            # Add new centroid point of region to list of new points
            new_points.append(centroid)

        # Re-compute Voronoi diagram using newly found weighted centroids
        vor = Voronoi(new_points)
        points_history.append(np.array(new_points))
        print(f"Iteration {iter+1} completed")
    return vor, points_history