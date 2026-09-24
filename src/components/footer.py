import base64
import os
import streamlit as st


def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# c.png usi folder me hai jahan footer.py hai
IMAGE_PATH = os.path.join(os.path.dirname(__file__), "c.png")
logo_base64 = get_image_base64(IMAGE_PATH)


def footer_home():
    st.markdown(
        f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center;">
            <p style="font-weight:bold; color:white; margin:0;">Created with ❤️ by</p>
            <img src="data:image/png;base64,{logo_base64}" style="max-height:25px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_dashboard():
    st.markdown(
        f"""
        <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; align-items:center;">
            <p style="font-weight:bold; color:black; margin:0;">Created with ❤️ by</p>
            <img src="data:image/png;base64,{logo_base64}" style="max-height:25px;" />
        </div>
        """,
        unsafe_allow_html=True,
    )