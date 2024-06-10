import os
from PIL import Image
from hypothesis import given
import hypothesis.strategies as st
from image_processing.load import load_images


@given(st.text())
def test_load_images_with_invalid_folder_path(folder_path: str):
    """
    Test loading images with an invalid folder path.
    """
    images, image_files = load_images(folder_path)
    assert images == []
    assert image_files == []


def test_load_images_with_valid_folder_path():
    """
    Test loading images with a valid folder path.
    """
    folder_path = '/home/ilya/Projects/augmentations_images/tests/test_image_prep'
    test_image = Image.new('RGB', (100, 100))
    test_image.save(os.path.join(folder_path, 'test_image.jpg'))

    images, image_files = load_images(folder_path)

    assert len(images) == 1
    assert len(image_files) == 1
    assert isinstance(images[0], Image.Image)
    assert image_files[0] == 'test_image.jpg'

    os.remove(os.path.join(folder_path, 'test_image.jpg'))
