import streamlit as st
import os
import math
from src.image_processing.load import load_images
from src.image_processing.process import process_images
from .sidebar import render_sidebar


def validate_folder_path(folder_path: str) -> bool:
    """
    Validates the provided folder path.

    Args:
        folder_path (str): The path to the folder that needs to be validated.

    Returns:
        bool: True if the folder path is valid (i.e., it exists, is a directory, and contains images), False otherwise.
    """
    if not folder_path:
        st.error('Пожалуйста, выберите директорию с изображениями и повторите попытку.')
        return False

    if folder_path != st.session_state.get('prev_folder_path', ''):
        st.session_state.prev_folder_path = folder_path

        if not os.path.isdir(folder_path):
            st.error(
                'Указанный путь к директории с изображениями не существует. Пожалуйста, проверьте путь.'
            )
            return False
        elif not any(
            fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
            for fname in os.listdir(folder_path)
        ):
            st.error(
                'В указанной директории нет изображений. Пожалуйста, загрузите изображения и повторите попытку.'
            )
            return False
    return True


def save_images(processed_images: list, output_path: str, image_names: list) -> None:
    """
    Saves the processed images to the specified output path.

    Args:
        processed_images (list): A list of processed images.
        output_path (str): The path where the processed images will be saved.
        image_names (list): A list of names for the processed images.

    Returns:
        None
    """
    if output_path:
        if st.sidebar.button('Сохранить преобразованные изображения'):
            if output_path:
                if not os.path.exists(output_path):
                    os.makedirs(output_path, exist_ok=True)
                if os.access(output_path, os.W_OK):
                    for i, img in enumerate(processed_images):
                        img.save(
                            os.path.join(output_path, f'transformed_{image_names[i]}')
                        )
                    st.success('Преобразованные изображения успешно сохранены!')
                else:
                    st.error(
                        'Нет прав на запись в указанную директорию. Пожалуйста, проверьте права доступа.'
                    )
            else:
                st.error(
                    'Пожалуйста, введите корректный путь к директории для сохранения изображений.'
                )


def display_images(processed_images: list) -> None:
    """
    Displays the processed images.

    Args:
        processed_images (list): A list of processed images.

    Returns:
        None
    """
    num_cols = min(3, len(processed_images))
    num_rows = math.ceil(len(processed_images) / num_cols) if num_cols else 0
    rows = [st.columns(num_cols) for _ in range(num_rows)]
    for i, img in enumerate(processed_images):
        row_idx = i // num_cols
        col_idx = i % num_cols
        rows[row_idx][col_idx].image(img, caption=f'Изображение {i+1}', width=300)


def render_main() -> None:
    """Render the main content of the Streamlit application for image processing.

    This function handles the rendering of the main content area, including loading and processing images
    based on the parameters set in the sidebar.

    Returns:
        None
    """
    (
        folder_path,
        output_path,
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
    ) = render_sidebar()

    if not validate_folder_path(folder_path):
        return

    images, image_names = load_images(folder_path)
    st.session_state.images = images
    st.session_state.image_names = image_names

    if images:
        processed_images = process_images(
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
        display_images(processed_images)
        save_images(processed_images, output_path, image_names)
