import streamlit as st


def render_sidebar() -> (
    tuple[str, str, int, int, int, int, int, int, int, int, int, int, int]
):
    """Render the sidebar with parameters for image transformation.

    Returns:
        Tuple[str, str, int, int, int, int, int, int, int, int, int, int, int]: A tuple containing:
            - str: The folder path containing the images.
            - str: The output path for saving the transformed images.
            - int: The height for resizing the images.
            - int: The width for resizing the images.
            - int: The rotation angle for the images.
            - int: The brightness adjustment level.
            - int: The contrast adjustment level.
            - int: The saturation adjustment level.
            - int: The noise level.
            - int: The shift level.
            - int: The tilt level.
            - int: The stretch level.
            - int: The crop size for random cropping.
    """
    st.sidebar.header('Параметры преобразования')
    folder_path = st.sidebar.text_input(
        'Введите путь к директории с изображениями', key='folder_path_input'
    )
    output_path = st.sidebar.text_input(
        'Введите путь к директории для сохранения изображений', key='output_path_input'
    )
    resize_height = st.sidebar.number_input(
        'Выберите высоту для изменения размера изображения', 1, 10000, 512
    )
    resize_width = st.sidebar.number_input(
        'Выберите ширину для изменения размера изображения', 1, 10000, 512
    )
    rotation_angle = st.sidebar.slider(
        'Выберите угол поворота для изображения', 0, 360, 0
    )
    brightness = st.sidebar.number_input(
        'Выберите уровень яркости', min_value=0, max_value=100, value=50
    )
    contrast = st.sidebar.number_input(
        'Выберите уровень контрастности', min_value=0, max_value=100, value=50
    )
    saturation = st.sidebar.number_input(
        'Выберите уровень насыщенности', min_value=0, max_value=100, value=50
    )
    noise = st.sidebar.number_input(
        'Выберите уровень шума', min_value=0, max_value=100, value=0
    )
    shift = st.sidebar.number_input(
        'Выберите уровень сдвига', min_value=0, max_value=100, value=0
    )
    tilt = st.sidebar.number_input(
        'Выберите уровень наклона', min_value=0, max_value=100, value=0
    )
    stretch = st.sidebar.number_input(
        'Выберите уровень растяжения', min_value=0, max_value=100, value=0
    )
    crop_size = st.sidebar.number_input(
        'Выберите размер случайного выреза', min_value=1, max_value=10000, value=512
    )
    return (
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
    )
