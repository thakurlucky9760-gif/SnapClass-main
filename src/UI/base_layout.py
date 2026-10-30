import streamlit as st


def style_background_home():
    """Styles specific to the Student/Teacher selection home screen."""
    st.markdown("""
        <style>
            .stApp {
                background: 
                    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(88, 101, 242, 0.28), transparent 70%),
                    radial-gradient(circle at 10% 20%, rgba(124, 131, 253, 0.1), transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(155, 165, 255, 0.08), transparent 50%),
                    #080B18 !important;
            }

            /* Portal Selection Columns as Glassmorphic Cards */
            .stApp div[data-testid="stColumn"] {
                background: rgba(17, 22, 42, 0.72) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(155, 165, 255, 0.16) !important;
                border-radius: 24px !important;
                padding: 2.5rem 2rem !important;
                box-shadow: 0 20px 50px -15px rgba(0, 0, 0, 0.7), 0 0 35px -10px rgba(88, 101, 242, 0.2) !important;
                transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                text-align: center !important;
                position: relative !important;
            }

            .stApp div[data-testid="stColumn"]:hover {
                border-color: rgba(124, 131, 253, 0.45) !important;
                transform: translateY(-5px) !important;
                box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.85), 0 0 50px -5px rgba(88, 101, 242, 0.35) !important;
            }

            .stApp div[data-testid="stColumn"] img {
                margin: 15px auto !important;
                filter: drop-shadow(0 15px 25px rgba(88, 101, 242, 0.3)) !important;
                transition: transform 0.3s ease !important;
            }

            .stApp div[data-testid="stColumn"]:hover img {
                transform: scale(1.06) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    """Styles specific to the Student and Teacher dashboards."""
    st.markdown("""
        <style>
            .stApp {
                background: 
                    radial-gradient(ellipse 70% 40% at 50% 0%, rgba(88, 101, 242, 0.18), transparent 60%),
                    radial-gradient(circle at 85% 30%, rgba(124, 131, 253, 0.08), transparent 45%),
                    #080B18 !important;
            }

            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4 {
                color: #FFFFFF !important;
            }

            .stApp [data-testid="stWidgetLabel"],
            .stApp [data-testid="stWidgetLabel"] * {
                color: #A5AEC8 !important;
                font-weight: 500 !important;
            }

            .stApp .dashboard-brand {
                color: #9BA5FF !important;
            }

            /* Container border cards */
            div[data-testid="stVerticalBlockBorderWrapper"] > div {
                background: rgba(17, 22, 42, 0.6) !important;
                border: 1px solid rgba(155, 165, 255, 0.14) !important;
                border-radius: 18px !important;
                backdrop-filter: blur(14px) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    """Core design system stylesheet for the entire Streamlit application."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

            :root {
                --page-bg: #080B18;
                --surface: #11162A;
                --surface-hover: #161D36;
                --text: #FFFFFF;
                --muted-text: #A5AEC8;
                --border: rgba(155, 165, 255, 0.14);
                --code-bg: rgba(88, 101, 242, 0.15);
                --code-text: #9BA5FF;
                --chip-bg: rgba(124, 131, 253, 0.12);
                --primary: #5865F2;
                --secondary: #7C83FD;
                --accent: #9BA5FF;
            }

            /* Global Font and Text Override */
            html, body, [class*="css"], .stApp {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                color: #FFFFFF !important;
            }

            /* Hide Top Default Streamlit Chrome */
            #MainMenu, footer, header {
                visibility: hidden !important;
            }

            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                max-width: 1100px !important;
            }

            /* Typography */
            h1 {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-size: 2.8rem !important;
                font-weight: 800 !important;
                letter-spacing: -0.04em !important;
                line-height: 1.15 !important;
                margin-bottom: 0.5rem !important;
                color: #FFFFFF !important;
            }

            h2 {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                letter-spacing: -0.03em !important;
                line-height: 1.25 !important;
                color: #FFFFFF !important;
            }

            h3, h4 {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 600 !important;
                letter-spacing: -0.02em !important;
                color: #FFFFFF !important;
            }

            p, span, label {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
            }

            /* Subject / Course Cards */
            .subject-card {
                color: #FFFFFF !important;
                background: rgba(17, 22, 42, 0.75) !important;
                border: 1px solid rgba(155, 165, 255, 0.14) !important;
                border-left: 6px solid #5865F2 !important;
                border-radius: 18px !important;
                padding: 24px !important;
                backdrop-filter: blur(14px) !important;
                box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.6) !important;
                transition: all 0.3s ease !important;
            }

            .subject-card:hover {
                border-color: rgba(124, 131, 253, 0.4) !important;
                box-shadow: 0 20px 45px -10px rgba(0, 0, 0, 0.7), 0 0 30px -10px rgba(88, 101, 242, 0.25) !important;
                transform: translateY(-2px) !important;
            }

            .subject-card h3 { 
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }

            .subject-card .subject-meta { 
                color: #A5AEC8 !important;
                font-size: 0.92rem !important;
            }

            .subject-card .subject-code {
                color: #9BA5FF !important;
                background: rgba(88, 101, 242, 0.18) !important;
                border: 1px solid rgba(155, 165, 255, 0.2) !important;
                padding: 2px 8px !important;
                border-radius: 6px !important;
                font-family: 'JetBrains Mono', monospace !important;
                font-weight: 600 !important;
            }

            .subject-card .subject-stat {
                color: #FFFFFF !important;
                background: rgba(124, 131, 253, 0.12) !important;
                border: 1px solid rgba(155, 165, 255, 0.18) !important;
                padding: 6px 14px !important;
                border-radius: 10px !important;
                font-size: 0.88rem !important;
            }

            /* Buttons */
            button {
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-weight: 600 !important;
                border-radius: 12px !important;
                padding: 10px 22px !important;
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
                letter-spacing: -0.01em !important;
            }

            /* Primary Button */
            button[kind="primary"], .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #5865F2 0%, #7C83FD 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                box-shadow: 0 8px 24px -5px rgba(88, 101, 242, 0.5) !important;
            }

            button[kind="primary"]:hover, .stButton > button[kind="primary"]:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 12px 30px -5px rgba(88, 101, 242, 0.7) !important;
                background: linear-gradient(135deg, #6571fa 0%, #8990ff 100%) !important;
            }

            /* Secondary Button */
            button[kind="secondary"], .stButton > button[kind="secondary"] {
                background: rgba(255, 255, 255, 0.05) !important;
                color: #FFFFFF !important;
                border: 1px solid rgba(155, 165, 255, 0.2) !important;
                backdrop-filter: blur(10px) !important;
            }

            button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: rgba(155, 165, 255, 0.4) !important;
                transform: translateY(-2px) !important;
            }

            /* Tertiary Button */
            button[kind="tertiary"], .stButton > button[kind="tertiary"] {
                background: rgba(17, 22, 42, 0.8) !important;
                color: #A5AEC8 !important;
                border: 1px solid rgba(155, 165, 255, 0.12) !important;
            }

            button[kind="tertiary"]:hover, .stButton > button[kind="tertiary"]:hover {
                color: #FFFFFF !important;
                border-color: rgba(155, 165, 255, 0.3) !important;
                transform: translateY(-2px) !important;
            }

            /* Inputs & Textboxes */
            input, select, textarea {
                background-color: rgba(17, 22, 42, 0.7) !important;
                color: #FFFFFF !important;
                border: 1px solid rgba(155, 165, 255, 0.2) !important;
                border-radius: 12px !important;
            }

            input:focus, select:focus, textarea:focus {
                border-color: #5865F2 !important;
                box-shadow: 0 0 16px rgba(88, 101, 242, 0.4) !important;
            }

            /* Alerts & Notifications */
            [data-testid="stAlert"] {
                background: rgba(17, 22, 42, 0.85) !important;
                border: 1px solid rgba(155, 165, 255, 0.22) !important;
                border-radius: 14px !important;
                color: #FFFFFF !important;
            }

            /* Dividers */
            hr {
                border-color: rgba(155, 165, 255, 0.12) !important;
                margin: 2rem 0 !important;
            }

            /* Expanders */
            [data-testid="stExpander"] {
                background: rgba(17, 22, 42, 0.5) !important;
                border: 1px solid rgba(155, 165, 255, 0.14) !important;
                border-radius: 14px !important;
            }

            /* Credit Footer */
            .credit-footer {
                margin-top: 3rem;
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                font-size: 0.92rem;
                color: #A5AEC8;
            }

            .credit-heart {
                color: #FF5F56;
                font-size: 1.1rem;
                display: inline-block;
            }

            .credit-name {
                font-weight: 700;
                color: #FFFFFF;
                letter-spacing: 0.04em;
            }
        </style>
    """, unsafe_allow_html=True)
