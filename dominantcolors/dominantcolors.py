from colorsys import hls_to_rgb, rgb_to_hls
from math import isclose

import click
import numpy as np
from fast_colorthief import get_palette
from PIL import Image

BG_WIDGET_COLOR = (35, 42, 49)
BG_TOPBAR_COLOR = (48, 57, 66)


def to_hex(color):
    """Convert color to hex string"""
    r, g, b = color
    return f"#{r:02x}{g:02x}{b:02x}"


def blend_colors(color, bg_color, alpha=0.5):
    """Blend color with background color"""
    bg_color = np.array(bg_color)
    return alpha * np.array(color) + (1 - alpha) * bg_color


def luminance_value(value):
    """get luminance value from color value"""
    if value > 1:
        value /= 255

    return value / 12.92 if value < 0.03928 else ((value + 0.055) / 1.055) ** 2.4


def color_luminance(rgb_color):
    """get luminance from rgb color"""
    R, G, B = [luminance_value(val) for val in rgb_color]
    return (0.2126 * R + 0.7152 * G + 0.0722 * B) + 0.05


def contrast_ratio(color1, color2):
    """get contrast ratio between color1 and color2"""
    luminance1 = color_luminance(color1)
    luminance2 = color_luminance(color2)

    if luminance1 > luminance2:
        return luminance1 / luminance2
    return luminance2 / luminance1


def adjust_closest_color(rgb_color, target_color, target_contrast=3):
    """Adjust rgb_color to have target_contrast contrast ratio with target_color"""
    r, g, b = np.array(rgb_color) / 255
    h, _, s = rgb_to_hls(r, g, b)

    for lum in np.arange(1, 0, -1 / 255):
        color = hls_to_rgb(h, lum, s)
        ratio = contrast_ratio(color, target_color)
        if isclose(ratio, target_contrast, rel_tol=5e-2):
            break

    # scale rgb values to 0-255 range
    closest_color = np.clip(color, 0, 1)
    return (closest_color * 255).astype(int)


def get_highest_contrast_color(target_color, candidate_colors, target_contrast=3):
    """Get the first color from candidate_colors with contrast ratio >= target_contrast
    if no color is found, adjust the color with highest contrast_ratio"""
    contrast_ratios = []
    for color in candidate_colors:
        ratio = contrast_ratio(target_color, color)
        if ratio >= target_contrast:
            return color
        contrast_ratios.append(ratio)

    # adjust color with highest contrast_ratio
    index = np.argmax(contrast_ratios)
    return adjust_closest_color(candidate_colors[index], target_color, target_contrast)


def preprocess_image(image):
    """Preprocess image to exclude dark and saturated dominant colors"""
    width, height = image.size
    image = image.resize((width // 2, height // 2)).convert("HSV")
    image_hsv = np.array(image)

    # get darkest colors
    ignore_mask = image_hsv[:, :, 2] < 40

    # desaturate colors
    image_hsv[:, :, 1] = np.minimum(image_hsv[:, :, 1], 200)

    image_rgba = Image.fromarray(image_hsv, "HSV").convert("RGBA")
    image_arr = np.array(image_rgba)

    # ignore darkest colors
    image_arr[ignore_mask, 3] = 0

    return image_arr


def color_extractor(image_path, target_contrast):
    """Obtain the dominant colors from an image and modify them to generate a palette
    with a suitable contrast ratio for use in the popup and radial progressbar music widgets.

    Receives a string of the image path and prints a list with 3 hex colors.
    The first two colors are applied to the popup: one for the background
    and the other for the UI components.
    The third color is the accent color for the radial progress bar.

    Args:
        image_path (str): The path to the image.

    Example:
        >>> color_extractor("image_path")
        #232A31
        #61d6c6
        #55b8e2
    """

    image = Image.open(image_path)
    image_array = preprocess_image(image)

    # get dominant colors from image
    most_dominant_color, *candidate_colors = get_palette(image_array, 3, quality=2)
    click.echo(to_hex(most_dominant_color))

    # get ui components color
    bg_darkened = blend_colors(most_dominant_color, BG_WIDGET_COLOR, alpha=208 / 255)
    ui_components_color = get_highest_contrast_color(
        bg_darkened, candidate_colors, target_contrast=target_contrast
    )

    click.echo(to_hex(ui_components_color))

    # get mediabar progress border color
    mediabar_progress_color = get_highest_contrast_color(BG_TOPBAR_COLOR, [most_dominant_color])
    click.echo(to_hex(mediabar_progress_color))
