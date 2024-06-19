from PIL import Image
import numpy as np
from typing import List
import albumentations as A


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
    transform = A.Compose(
        [
            A.Resize(height=resize_height, width=resize_width),
            A.Rotate(limit=rotation_angle, p=1.0),
            A.RandomBrightnessContrast(
                brightness_limit=brightness / 100.0,
                contrast_limit=contrast / 100.0,
                p=1.0,
            ),
            A.HueSaturationValue(
                hue_shift_limit=0,
                sat_shift_limit=(saturation - 50) * 2,
                val_shift_limit=0,
                p=1.0,
            ),
            A.GaussNoise(var_limit=(0, noise * 255), p=1.0),
            A.ShiftScaleRotate(
                shift_limit=shift / 100.0, scale_limit=0, rotate_limit=0, p=1.0
            ),
            A.Affine(shear=tilt, p=1.0),
            A.Affine(scale=(1 - stretch / 100.0, 1 + stretch / 100.0), p=1.0),
            A.RandomCrop(height=int(crop_size), width=int(crop_size), p=1.0),
        ]
    )

    for img in images:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img_np = np.array(img)
        img_np = img_np.astype(np.uint8)
        transformed = transform(image=img_np)
        processed_img = Image.fromarray(transformed['image'])
        processed_images.append(processed_img)

    return processed_images
