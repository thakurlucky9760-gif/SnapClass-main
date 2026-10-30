import streamlit as st

def footer_home():
    st.markdown(
        """
        <div class="credit-footer credit-footer-home">
            <span>Created with</span>
            <span class="credit-heart" aria-label="love">&#9829;</span>
            <span>by</span>
            <span class="credit-name">CHAITANYA PRATAP</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_dashboard():
    st.markdown(
        """
        <div class="credit-footer credit-footer-dashboard dashboard-footer">
            <span>Created with</span>
            <span class="credit-heart" aria-label="love">&#9829;</span>
            <span>by</span>
            <span class="credit-name">CHAITANYA PRATAP</span>
        </div>
        """,
        unsafe_allow_html=True,
    )