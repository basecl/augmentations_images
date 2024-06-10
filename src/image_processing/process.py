from PIL import Image
import imgaug.augmenters as iaa
import numpy as np
from typing import List


def process_images(
    images: List[Image.Image],
    resize_height: int,
    resize_width: int,
    rotation_angle: int,
    brightness: int,
    contrast: int,
    saturation: int,
    noise: int,
    shift: int,
    tilt: int,
    stretch: int,
    crop_size: int,
) -> List[Image.Image]:
    """Apply a series of image processing operations to a list of images.

    Args:
        images (List[Image.Image]): A list of PIL Image objects to be processed.
        resize_height (int): Desired height for resizing.
        resize_width (int): Desired width for resizing.
        rotation_angle (int): Angle for rotation in degrees.
        brightness (int): Adjustment factor for brightness.
        contrast (int): Adjustment factor for contrast.
        saturation (int): Adjustment factor for saturation.
        noise (int): Level of Gaussian noise to be added.
        shift (int): Percentage of shift along x and y axes.
        tilt (int): Shear angle for tilt.
        stretch (int): Percentage of stretching.
        crop_size (int): Percentage of cropping.

    Returns:
        List[Image.Image]: A list of processed PIL Image objects.
    """
    processed_images = []
    for img in images:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img_np = np.array(img)
        new_size = (int(resize_height), int(resize_width))
        aug = iaa.Sequential(
            [
                iaa.Resize({'height': new_size[1], 'width': new_size[0]}),
                iaa.Rotate(rotation_angle),
                iaa.MultiplyBrightness(brightness / 50.0),
                iaa.contrast.LinearContrast(contrast / 50.0),
                iaa.AddToHueAndSaturation((saturation - 50) * 2),
                iaa.AdditiveGaussianNoise(scale=(0, noise * 255)),
                iaa.Affine(translate_percent={'x': shift / 100, 'y': shift / 100}),
                iaa.Affine(shear=tilt),
                iaa.Affine(
                    scale={
                        'x': (1 - stretch / 100, 1 + stretch / 100),
                        'y': (1 - stretch / 100, 1 + stretch / 100),
                    }
                ),
                iaa.Crop(percent=(0, crop_size / 100)),
            ]
        )
        img_np = aug(image=img_np)
        processed_img = Image.fromarray(img_np)
        processed_images.append(processed_img)
    return processed_images
