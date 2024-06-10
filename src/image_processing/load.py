import os
from PIL import Image


def load_images(folder_path):
    image_names = os.listdir(folder_path)
    image_files = [
        img
        for img in image_names
        if img.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
    ]
    images = [Image.open(os.path.join(folder_path, img)) for img in image_files]
    return images, image_files
