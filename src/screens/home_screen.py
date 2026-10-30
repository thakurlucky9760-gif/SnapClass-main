import streamlit as st
from pathlib import Path


def load_logo_svg() -> str:
    """Reads the custom SNAP CLASS combined logo SVG from local assets."""
    logo_path = Path(__file__).parent.parent / "assets" / "snap_class_logo.svg"
    if logo_path.exists():
        return logo_path.read_text(encoding="utf-8")
    return ""


def home_screen():
    # -------------------------------------------------------------------------
    # 1. SCOPED HOME SCREEN CSS (Strictly isolated to role-selection view)
    # -------------------------------------------------------------------------
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;600&display=swap');

            /* Scoped App Background & Global Typography for Home Screen */
            .stApp {
                background: 
                    radial-gradient(ellipse 70% 45% at 50% -10%, rgba(88, 101, 242, 0.28), transparent 70%),
                    radial-gradient(circle at 10% 20%, rgba(124, 131, 253, 0.09), transparent 45%),
                    radial-gradient(circle at 90% 80%, rgba(155, 165, 255, 0.07), transparent 50%),
                    #080B18 !important;
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
                color: #FFFFFF !important;
                overflow-x: hidden;
            }

            /* Hide Top Default Chrome on Home Screen */
            #MainMenu, footer, header {
                visibility: hidden !important;
            }

            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 3rem !important;
                max-width: 980px !important;
            }

            /* Header Section */
            .home-header {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                margin-top: 10px;
                margin-bottom: 25px;
            }

            .home-logo-wrap {
                max-width: 320px;
                width: 100%;
                margin: 0 auto 16px;
                filter: drop-shadow(0 10px 30px rgba(88, 101, 242, 0.35));
                transition: transform 0.3s ease;
            }

            .home-logo-wrap:hover {
                transform: scale(1.02);
            }

            .home-logo-wrap svg {
                width: 100%;
                height: auto;
                display: block;
            }

            /* Hero Section */
            .hero-section {
                text-align: center;
                margin-bottom: 45px;
            }

            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 16px;
                border-radius: 9999px;
                background: rgba(88, 101, 242, 0.15);
                border: 1px solid rgba(155, 165, 255, 0.25);
                color: #9BA5FF;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 20px;
                backdrop-filter: blur(10px);
            }

            .hero-badge-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background: #22C55E;
                box-shadow: 0 0 10px #22C55E;
            }

            .hero-title {
                font-size: clamp(2.3rem, 4.5vw, 3.4rem) !important;
                font-weight: 800 !important;
                letter-spacing: -0.04em !important;
                line-height: 1.15 !important;
                color: #FFFFFF !important;
                margin-bottom: 12px !important;
            }

            .gradient-text {
                background: linear-gradient(135deg, #FFFFFF 25%, #9BA5FF 70%, #7C83FD 100%);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
            }

            .hero-subtitle {
                font-size: clamp(1.1rem, 1.8vw, 1.3rem) !important;
                font-weight: 600 !important;
                color: #FFFFFF !important;
                margin-bottom: 6px !important;
                letter-spacing: -0.01em !important;
            }

            .hero-description {
                font-size: 0.98rem !important;
                color: #A5AEC8 !important;
                max-width: 580px !important;
                margin: 0 auto !important;
                line-height: 1.6 !important;
            }

            /* =========================================================
               Interactive Role Cards (Columns)
               ========================================================= */
            .stApp div[data-testid="stColumn"] {
                background: rgba(17, 22, 42, 0.75) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(155, 165, 255, 0.16) !important;
                border-radius: 24px !important;
                padding: 2.5rem 2rem 2.2rem !important;
                box-shadow: 0 20px 45px -15px rgba(0, 0, 0, 0.7), 0 0 30px -10px rgba(88, 101, 242, 0.18) !important;
                transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
                display: flex !important;
                flex-direction: column !important;
                justify-content: space-between !important;
                min-height: 480px !important;
                position: relative !important;
                overflow: hidden !important;
            }

            .stApp div[data-testid="stColumn"]::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 2px;
                background: linear-gradient(90deg, transparent, #5865F2, #7C83FD, transparent);
                opacity: 0;
                transition: opacity 0.35s ease;
            }

            .stApp div[data-testid="stColumn"]:hover {
                border-color: rgba(124, 131, 253, 0.5) !important;
                transform: translateY(-5px) !important;
                box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.85), 0 0 45px -5px rgba(88, 101, 242, 0.35) !important;
            }

            .stApp div[data-testid="stColumn"]:hover::before {
                opacity: 1;
            }

            /* Card Content Layout */
            .card-header-block {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                width: 100%;
            }

            .card-icon-box {
                width: 76px;
                height: 76px;
                border-radius: 20px;
                background: linear-gradient(135deg, rgba(88, 101, 242, 0.22) 0%, rgba(124, 131, 253, 0.08) 100%);
                border: 1px solid rgba(155, 165, 255, 0.25);
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
                box-shadow: 0 0 25px -5px rgba(88, 101, 242, 0.35);
                transition: transform 0.3s ease;
            }

            .stApp div[data-testid="stColumn"]:hover .card-icon-box {
                transform: scale(1.08) rotate(2deg);
            }

            .card-pill-tag {
                display: inline-block;
                padding: 4px 12px;
                border-radius: 9999px;
                background: rgba(88, 101, 242, 0.16);
                color: #9BA5FF;
                font-size: 0.74rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                border: 1px solid rgba(155, 165, 255, 0.22);
                margin-bottom: 12px;
            }

            .card-title {
                font-size: 1.85rem !important;
                font-weight: 800 !important;
                color: #FFFFFF !important;
                margin-bottom: 10px !important;
                letter-spacing: -0.03em !important;
            }

            .card-description {
                font-size: 0.95rem !important;
                color: #A5AEC8 !important;
                line-height: 1.6 !important;
                margin-bottom: 22px !important;
                text-align: center !important;
            }

            .card-features-list {
                width: 100%;
                background: rgba(8, 11, 24, 0.45);
                border-radius: 14px;
                border: 1px solid rgba(155, 165, 255, 0.1);
                padding: 14px 16px;
                margin-bottom: 24px;
                text-align: left;
            }

            .card-feature-item {
                display: flex;
                align-items: center;
                gap: 9px;
                font-size: 0.85rem;
                color: #FFFFFF;
                margin-bottom: 8px;
            }

            .card-feature-item:last-child {
                margin-bottom: 0;
            }

            .feature-check {
                color: #22C55E;
                font-weight: 700;
                flex-shrink: 0;
            }

            /* Button Styling */
            .stApp div[data-testid="stColumn"] button {
                width: 100% !important;
                background: linear-gradient(135deg, #5865F2 0%, #7C83FD 100%) !important;
                color: #FFFFFF !important;
                font-family: 'Plus Jakarta Sans', sans-serif !important;
                font-size: 1rem !important;
                font-weight: 700 !important;
                letter-spacing: -0.01em !important;
                border: none !important;
                border-radius: 14px !important;
                padding: 14px 24px !important;
                box-shadow: 0 10px 25px -5px rgba(88, 101, 242, 0.45) !important;
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
                margin-top: auto !important;
            }

            .stApp div[data-testid="stColumn"] button:hover {
                transform: translateY(-2px) !important;
                box-shadow: 0 14px 30px -5px rgba(88, 101, 242, 0.7) !important;
                background: linear-gradient(135deg, #6471fa 0%, #8990ff 100%) !important;
            }

            .stApp div[data-testid="stColumn"] button:active {
                transform: translateY(0) !important;
            }

            /* Minimal Footer */
            .home-footer {
                margin-top: 50px;
                padding-top: 24px;
                border-top: 1px solid rgba(155, 165, 255, 0.1);
                text-align: center;
                font-size: 0.86rem;
                color: #A5AEC8;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 6px;
            }

            .home-footer-brand {
                color: #9BA5FF;
                font-weight: 600;
            }

            @media (prefers-reduced-motion: reduce) {
                * {
                    animation-duration: 0.01ms !important;
                    animation-iteration-count: 1 !important;
                    transition-duration: 0.01ms !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 2. MINIMAL HEADER WITH NEW CUSTOM LOGO
    # -------------------------------------------------------------------------
    logo_svg = load_logo_svg()
    
    st.markdown(f"""
        <div class="home-header">
            <div class="home-logo-wrap" aria-label="SNAP CLASS AI Logo">
                {logo_svg}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 3. MAIN HERO SECTION
    # -------------------------------------------------------------------------
    st.markdown("""
        <div class="hero-section">
            <div class="hero-badge">
                <span class="hero-badge-dot"></span>
                <span>Next-Gen AI Biometrics • Smart Attendance</span>
            </div>
            <h1 class="hero-title">
                Welcome to <span class="gradient-text">SNAP CLASS</span>
            </h1>
            <p class="hero-subtitle">
                Your intelligent classroom experience starts here.
            </p>
            <p class="hero-description">
                Choose your portal to experience smarter classroom management with high-precision face recognition and voice verification.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # 4. STUDENT & TEACHER PORTAL CARDS
    # -------------------------------------------------------------------------
    col1, col2 = st.columns(2, gap="large")

    # --- STUDENT PORTAL CARD ---
    with col1:
        st.markdown("""
            <div class="card-header-block">
                <div class="card-icon-box">
                    <!-- Academic Graduation Cap / Student Icon -->
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#9BA5FF" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 10v6M2 10l10-5 10 5-10 5z"></path>
                        <path d="M6 12v5c3 3 9 3 12 0v-5"></path>
                    </svg>
                </div>
                <span class="card-pill-tag">Student Portal</span>
                <h2 class="card-title">Student Portal</h2>
                <p class="card-description">
                    Access your attendance, classroom information, and academic activities.
                </p>
            </div>
            <div class="card-features-list">
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Fast FaceID Biometric Login</span>
                </div>
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Voice ID Signature Verification</span>
                </div>
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>QR Code One-Click Course Joining</span>
                </div>
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Real-Time Attendance Rate Tracker</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # EXACT PRESERVED ORIGINAL FUNCTIONALITY
        if st.button(
            "Continue as Student",
            type="primary",
            icon=":material/arrow_forward:",
            use_container_width=True,
            key="btn_continue_student"
        ):
            st.session_state['login_type'] = 'student'
            st.rerun()

    # --- TEACHER PORTAL CARD ---
    with col2:
        st.markdown("""
            <div class="card-header-block">
                <div class="card-icon-box">
                    <!-- Instructor Podium / Teacher Icon -->
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#7C83FD" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                        <line x1="9" y1="7" x2="15" y2="7"></line>
                        <line x1="9" y1="11" x2="13" y2="11"></line>
                    </svg>
                </div>
                <span class="card-pill-tag">Faculty &amp; Instructor</span>
                <h2 class="card-title">Teacher Portal</h2>
                <p class="card-description">
                    Manage your classes, monitor attendance, and access student records.
                </p>
            </div>
            <div class="card-features-list">
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Single-Photo Panoramic Room Scan</span>
                </div>
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Sequential Voice Roll-Call Engine</span>
                </div>
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Instant QR Code &amp; Join Link Generation</span>
                </div>
                <div class="card-feature-item">
                    <span class="feature-check">✓</span> <span>Detailed Student Attendance Logs &amp; CSV</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # EXACT PRESERVED ORIGINAL FUNCTIONALITY
        if st.button(
            "Continue as Teacher",
            type="primary",
            icon=":material/arrow_forward:",
            use_container_width=True,
            key="btn_continue_teacher"
        ):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # -------------------------------------------------------------------------
    # 5. SUBTLE MINIMAL FOOTER
    # -------------------------------------------------------------------------
    st.markdown("""
        <div class="home-footer">
            <div>
                Powered by <span class="home-footer-brand">SNAP CLASS AI Technology</span>
            </div>
            <div style="font-size: 0.78rem; color: #6B7699;">
                &copy; 2026 SNAP CLASS. All rights reserved.
            </div>
        </div>
    """, unsafe_allow_html=True)
