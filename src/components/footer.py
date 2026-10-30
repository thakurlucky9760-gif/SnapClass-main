import streamlit as st


def footer_home():
    st.markdown(
        """
        <div class="credit-footer" style="margin-top: 3rem; padding: 1.5rem 0; border-top: 1px solid rgba(155, 165, 255, 0.1); display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.9rem; color: #A5AEC8;">
            <span>Designed &amp; Developed with</span>
            <span class="credit-heart" style="color: #FF5F56; font-size: 1.1rem;" aria-label="love">&#9829;</span>
            <span>by</span>
            <span class="credit-name" style="color: #FFFFFF; font-weight: 700; letter-spacing: 0.04em;">CHAITANYA PRATAP</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def footer_dashboard():
    st.markdown(
        """
        <div class="credit-footer dashboard-footer" style="margin-top: 3.5rem; padding: 1.5rem 0; border-top: 1px solid rgba(155, 165, 255, 0.1); display: flex; align-items: center; justify-content: center; gap: 8px; font-size: 0.9rem; color: #A5AEC8;">
            <span>Designed &amp; Developed with</span>
            <span class="credit-heart" style="color: #FF5F56; font-size: 1.1rem;" aria-label="love">&#9829;</span>
            <span>by</span>
            <span class="credit-name" style="color: #FFFFFF; font-weight: 700; letter-spacing: 0.04em;">CHAITANYA PRATAP</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
