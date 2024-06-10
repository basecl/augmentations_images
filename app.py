import streamlit as st
from src.ui.main import render_main


def main():
    st.title('IPREP')
    render_main()


if __name__ == '__main__':
    main()
