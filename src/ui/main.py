import streamlit as st
import os
import math
from src.image_processing.load import load_images
from src.image_processing.process import process_images
from .sidebar import render_sidebar


def render_main():
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

    if not folder_path:
        st.error('Пожалуйста, выберите директорию с изображениями и повторите попытку.')
        return

    if folder_path and folder_path != st.session_state.get('prev_folder_path', ''):
        st.session_state.prev_folder_path = folder_path

        if not os.path.isdir(folder_path):
            st.error(
                'Указанный путь к директории с изображениями не существует. Пожалуйста, проверьте путь.'
            )
        elif not any(
            fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
            for fname in os.listdir(folder_path)
        ):
            st.error(
                'В указанной директории нет изображений. Пожалуйста, загрузите изображения и повторите попытку.'
            )
        else:
            images, image_names = load_images(folder_path)
            st.session_state.images = images
            st.session_state.image_names = image_names
    else:
        images = st.session_state.get('images', [])
        image_names = st.session_state.get('image_names', [])

    if images:
        if len(images) != 0:
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
            num_cols = min(3, len(processed_images))
            num_rows = math.ceil(len(processed_images) / num_cols) if num_cols else 0
            rows = [st.columns(num_cols) for _ in range(num_rows)]
            for i, img in enumerate(processed_images):
                row_idx = i // num_cols
                col_idx = i % num_cols
                rows[row_idx][col_idx].image(
                    img, caption=f'Изображение {i+1}', width=300
                )

            if output_path:
                if st.sidebar.button('Сохранить преобразованные изображения'):
                    if output_path:
                        if not os.path.exists(output_path):
                            os.makedirs(output_path, exist_ok=True)
                        if os.access(output_path, os.W_OK):
                            for i, img in enumerate(processed_images):
                                img.save(
                                    os.path.join(
                                        output_path, f'transformed_{image_names[i]}'
                                    )
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
        else:
            st.error(
                'Пожалуйста, введите корректный путь к директории c изображениями.'
            )
    else:
        st.error(
            'Не удалось загрузить изображения. Пожалуйста, убедитесь, что путь к директории правильный и содержит изображения.'
        )
