import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.UI.base_layout import style_base_layout, style_background_home


def home_screen():
    # Injected styles
    style_base_layout()
    style_background_home()

    # Premium Hero Brand Header
    header_home()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
            <div style="width: 100%;">
                <span style="display: inline-block; padding: 4px 12px; border-radius: 9999px; background: rgba(88, 101, 242, 0.2); color: #9BA5FF; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; border: 1px solid rgba(155, 165, 255, 0.25); margin-bottom: 12px;">
                    Student Access
                </span>
                <h2 style="font-size: 1.85rem; font-weight: 800; margin-bottom: 6px; color: #FFFFFF;">I'm a Student</h2>
                <p style="font-size: 0.88rem; color: #A5AEC8; margin-bottom: 15px;">Check your attendance, enroll via QR, and authenticate with FaceID & Voice biometrics.</p>
            </div>
        """, unsafe_allow_html=True)

        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png", width=130)

        st.markdown("""
            <div style="text-align: left; width: 100%; margin: 15px 0 20px 0; background: rgba(8, 11, 24, 0.45); border-radius: 14px; padding: 14px 16px; border: 1px solid rgba(155, 165, 255, 0.1);">
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF; margin-bottom: 8px;">
                    <span style="color: #7C83FD;">✓</span> <span>Instant FaceID Webcam Login</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF; margin-bottom: 8px;">
                    <span style="color: #7C83FD;">✓</span> <span>Voice ID Signature Verification</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF; margin-bottom: 8px;">
                    <span style="color: #7C83FD;">✓</span> <span>QR Code One-Click Course Joining</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF;">
                    <span style="color: #7C83FD;">✓</span> <span>Real-Time Attendance History &amp; %</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Enter Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', use_container_width=True, key="btn_student_portal"):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.markdown("""
            <div style="width: 100%;">
                <span style="display: inline-block; padding: 4px 12px; border-radius: 9999px; background: rgba(124, 131, 253, 0.2); color: #7C83FD; font-size: 0.76rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; border: 1px solid rgba(124, 131, 253, 0.35); margin-bottom: 12px;">
                    Faculty &amp; Instructor
                </span>
                <h2 style="font-size: 1.85rem; font-weight: 800; margin-bottom: 6px; color: #FFFFFF;">I'm a Teacher</h2>
                <p style="font-size: 0.88rem; color: #A5AEC8; margin-bottom: 15px;">Run panoramic class face scans, sequential voice roll-call, and manage subjects effortlessly.</p>
            </div>
        """, unsafe_allow_html=True)

        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png", width=145)

        st.markdown("""
            <div style="text-align: left; width: 100%; margin: 15px 0 20px 0; background: rgba(8, 11, 24, 0.45); border-radius: 14px; padding: 14px 16px; border: 1px solid rgba(155, 165, 255, 0.1);">
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF; margin-bottom: 8px;">
                    <span style="color: #7C83FD;">✓</span> <span>Single-Photo Panoramic Room Scan</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF; margin-bottom: 8px;">
                    <span style="color: #7C83FD;">✓</span> <span>Sequential Voice Roll-Call Engine</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF; margin-bottom: 8px;">
                    <span style="color: #7C83FD;">✓</span> <span>Instant QR Code &amp; Join Link Generation</span>
                </div>
                <div style="display: flex; align-items: center; gap: 8px; font-size: 0.84rem; color: #FFFFFF;">
                    <span style="color: #7C83FD;">✓</span> <span>Detailed Logs &amp; One-Click CSV Export</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button('Enter Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right', use_container_width=True, key="btn_teacher_portal"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    # Bottom Trust & Security Bar
    st.markdown("""
        <div style="margin-top: 40px; text-align: center; display: flex; align-items: center; justify-content: center; gap: 24px; flex-wrap: wrap;">
            <div style="display: flex; align-items: center; gap: 6px; font-size: 0.82rem; color: #A5AEC8;">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #22C55E;"></span>
                <span>Supabase Cloud Online</span>
            </div>
            <div style="width: 1px; height: 16px; background: rgba(155, 165, 255, 0.15);"></div>
            <div style="display: flex; align-items: center; gap: 6px; font-size: 0.82rem; color: #A5AEC8;">
                <span>🔒</span>
                <span>Encrypted Biometric Vectors</span>
            </div>
            <div style="width: 1px; height: 16px; background: rgba(155, 165, 255, 0.15);"></div>
            <div style="display: flex; align-items: center; gap: 6px; font-size: 0.82rem; color: #A5AEC8;">
                <span>⚡</span>
                <span>Sub-Second Neural Verification</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    footer_home()
