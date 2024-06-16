import os
import hypothesis.strategies as st
from PIL import Image


def load_images(folder_path: str) -> tuple[list[Image.Image], list[str]]:
    """Load image of .jpg, .jpeg, .png, .bmp, .gif formats from the folder path.

    Args:
        folder_path (str): A photo folder location.

    Returns:
        Tuple[List[Image.Image], List[str]]: A tuple containing two lists:
            - List[Image.Image]: A list of PIL Image objects representing the loaded images.
            - List[str]: A list of filenames of the loaded images.
    """
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return [], []
    image_names = os.listdir(folder_path)
    image_files = [
        img
        for img in image_names
        if img.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
    ]
    try:
        images = [Image.open(os.path.join(folder_path, img)) for img in image_files]
    except:  # noqa: E722
        st.error(
            'Указанный путь к директории с изображениями не существует. Пожалуйста, проверьте путь.'
        )
        return [], []
    return images, image_files
