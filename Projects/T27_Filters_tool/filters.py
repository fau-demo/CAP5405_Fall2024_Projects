from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps, ImageDraw
import math

# Filter Functions
def apply_grayscale(base_image, intensity):
    """Apply grayscale filter to the base image with given intensity."""
    if intensity <= 0:
        return base_image
    grayscale_img = ImageOps.grayscale(base_image).convert("RGB")
    return Image.blend(base_image, grayscale_img, intensity) if intensity < 1.0 else grayscale_img

def apply_sepia(base_image, intensity):
    """Apply sepia filter to the base image with given intensity."""
    if intensity <= 0:
        return base_image
    sepia_data = [
        (
            min(int(r * 0.393 + g * 0.769 + b * 0.189), 255),
            min(int(r * 0.349 + g * 0.686 + b * 0.168), 255),
            min(int(r * 0.272 + g * 0.534 + b * 0.131), 255)
        )
        for r, g, b in base_image.getdata()
    ]
    sepia_img = Image.new("RGB", base_image.size)
    sepia_img.putdata(sepia_data)
    return Image.blend(base_image, sepia_img, intensity)

def apply_blur(base_image, intensity):
    """Apply Gaussian blur to the base image with the given intensity."""
    if intensity <= 0:
        return base_image
    return base_image.filter(ImageFilter.GaussianBlur(radius=intensity * 10))

def apply_sharpen(base_image, intensity):
    """Apply unsharp mask filter (sharpening) to the base image."""
    if intensity <= 0:
        return base_image
    return base_image.filter(ImageFilter.UnsharpMask(radius=2, percent=int(50 + intensity * 100), threshold=3))

def adjust_brightness(base_image, intensity):
    """Adjust the brightness of the base image based on intensity."""
    enhancer = ImageEnhance.Brightness(base_image)
    return enhancer.enhance(intensity if intensity > 0 else 1)

def adjust_contrast(base_image, intensity):
    """Adjust the contrast of the base image based on intensity."""
    enhancer = ImageEnhance.Contrast(base_image)
    return enhancer.enhance(intensity if intensity > 0 else 1)

def adjust_saturation(base_image, intensity):
    """Adjust the saturation of the base image based on intensity."""
    enhancer = ImageEnhance.Color(base_image)
    return enhancer.enhance(intensity if intensity > 0 else 1)

def apply_vignette(base_image, intensity):
    """Apply vignette filter to the image, darkening corners based on intensity."""
    if intensity <= 0:
        return base_image
    width, height = base_image.size
    x_center, y_center = width // 2, height // 2
    max_radius = math.sqrt(x_center**2 + y_center**2)
    vignette_mask = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(vignette_mask)

    for y in range(height):
        for x in range(width):
            distance = math.sqrt((x - x_center)**2 + (y - y_center)**2)
            factor = 1 - intensity * (distance / max_radius)
            draw.point((x, y), int(255 * max(0, min(1, factor))))

    vignette_mask = vignette_mask.filter(ImageFilter.GaussianBlur(15))
    return Image.composite(base_image, Image.new("RGB", base_image.size, (0, 0, 0)), vignette_mask)

def apply_edgeDetection(base_image, intensity):
    """Apply edge detection filter to the base image."""
    if intensity <= 0:
        return base_image
    edge_img = base_image.convert("L").filter(ImageFilter.FIND_EDGES)
    edge_img = ImageOps.colorize(edge_img, black="black", white="white")
    return Image.blend(base_image, edge_img, intensity)

def apply_emboss(base_image, intensity):
    """Apply emboss effect to the base image."""
    if intensity <= 0:
        return base_image
    embossed_img = base_image.filter(ImageFilter.EMBOSS)
    return Image.blend(base_image, embossed_img, intensity)

def apply_artistic_filter(base_image, intensity):
    """Apply artistic contour filter to the base image."""
    if intensity <= 0:
        return base_image
    contour_img = base_image.filter(ImageFilter.CONTOUR)
    return Image.blend(base_image, contour_img, intensity)

def apply_polaroid_effect(image, intensity=1.0):
    """Apply a Polaroid-like effect."""
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2 + intensity * 0.1)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.3 + intensity * 0.1)
    return image.filter(ImageFilter.GaussianBlur(radius=intensity))

def apply_invert_colors(image, intensity=1.0):
    """Invert the colors."""
    return ImageOps.invert(image)

def apply_oil_painting_effect(image, intensity=1.0):
    """Apply an enhanced oil painting effect."""
    # Step 1: Apply a smooth filter to soften the image
    smoothed = image.filter(ImageFilter.GaussianBlur(radius=0.1 * intensity))

    # Step 2: Enhance edges to give a brushstroke appearance
    edges = smoothed.filter(ImageFilter.MedianFilter(size=3))

    # Step 3: Adjust the brightness and contrast for a painterly effect
    enhancer = ImageEnhance.Contrast(smoothed)
    enhanced_image = enhancer.enhance(2.1)

    # Step 4: Add a slight emboss effect to mimic canvas texture
    oil_paint_effect = enhanced_image.filter(ImageFilter.EMBOSS)

    # Step 5: Blend original and embossed to create a realistic oil-painted effect
    final_result = Image.blend(enhanced_image, oil_paint_effect, alpha=0.4)

    return final_result

def apply_watercolor_effect(image, intensity=1.0):
    """Apply a watercolor effect."""
    smoothed_image = image.copy()
    for _ in range(int(1 + intensity * 0.2)):  # Smooth the image multiple times
        smoothed_image = smoothed_image.filter(ImageFilter.SMOOTH_MORE)
    return smoothed_image.filter(ImageFilter.GaussianBlur(radius=intensity * 0.2))


