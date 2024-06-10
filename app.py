import streamlit as st
from src.ui.main import render_main


def main():
    """Run the Streamlit application for image processing.

    This function sets up the Streamlit application, including the title and rendering the main content.

    Returns:
        None
    """
    st.title('IPREP')
    render_main()


if __name__ == '__main__':
    main()
