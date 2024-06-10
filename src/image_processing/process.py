from PIL import Image
import imgaug.augmenters as iaa
import numpy as np
from typing import List, Union


def process_images(
    images: List[Image.Image],
    resize_height: Union[int, float],
    resize_width: Union[int, float],
    rotation_angle: Union[int, float],
    brightness: Union[int, float],
    contrast: Union[int, float],
    saturation: Union[int, float],
    noise: Union[int, float],
    shift: Union[int, float],
    tilt: Union[int, float],
    stretch: Union[int, float],
    crop_size: Union[int, float],
) -> List[Image.Image]:
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
