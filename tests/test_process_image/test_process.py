from PIL import Image
import hypothesis.strategies as st
from hypothesis import given
from image_processing.process import process_images
from typing import List, Tuple, Any


@st.composite
def images(draw) -> Any:
    test_image = Image.new('RGB', (1000, 1000))
    return test_image


@st.composite
def parameters(draw) -> Tuple:
    resize_height: int = draw(st.integers(min_value=1000, max_value=1000))
    resize_width: int = draw(st.integers(min_value=1000, max_value=1000))
    rotation_angle: int = draw(st.integers(min_value=0, max_value=360))
    brightness: int = draw(st.integers(min_value=0, max_value=100))
    contrast: int = draw(st.integers(min_value=0, max_value=100))
    saturation: int = draw(st.integers(min_value=0, max_value=100))
    noise: int = draw(st.integers(min_value=0, max_value=100))
    shift: int = draw(st.integers(min_value=0, max_value=100))
    tilt: int = draw(st.integers(min_value=0, max_value=100))
    stretch: int = draw(st.integers(min_value=0, max_value=100))
    crop_size: int = draw(st.integers(min_value=256, max_value=1000))
    return (
        resize_height,
        resize_width,
        rotation_angle,
        brightness,
        contrast,
        saturation,
        noise,
        shift,
        tilt,
        stretch,
        crop_size,
    )


@given(images=st.lists(images(), max_size=1), parameters=parameters())
def test_process_images(images: List[Image.Image], parameters: Tuple) -> None:
    (
        resize_height,
        resize_width,
        rotation_angle,
        brightness,
        contrast,
        saturation,
        noise,
        shift,
        tilt,
        stretch,
        crop_size,
    ) = parameters
    processed_images: List[Image.Image] = process_images(
        images,
        resize_height,
        resize_width,
        rotation_angle,
        brightness,
        contrast,
        saturation,
        noise,
        shift,
        tilt,
        stretch,
        crop_size,
    )
    assert len(processed_images) == len(images)
    for img in processed_images:
        assert isinstance(img, Image.Image)
