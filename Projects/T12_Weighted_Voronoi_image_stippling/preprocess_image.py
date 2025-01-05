import numpy as np
import skimage.filters as filters
from skimage import io, color

# Preprocesses the image to a de-noised, inverted, normalized, and if desired quantized state
# gray_levels = 0 -> quantization is not preformed
def preprocess_image(img, gray_levels = 0):
  smooth_img = filters.gaussian(img, sigma=1) #de-noise
  gray_img = color.rgb2gray(smooth_img)

  # invert image so high values are the dark parts of original image
  inverted_gray_img = (1 - gray_img)
  normalized_inverted_gray_img = inverted_gray_img / np.max(inverted_gray_img)

  if gray_levels > 0:
    bins = np.linspace(0, 1, gray_levels) #spreading image gray values evenly
    quantized = np.digitize(normalized_inverted_gray_img, bins) - 1
    normalized_inverted_gray_img = quantized / gray_levels

  return normalized_inverted_gray_img


