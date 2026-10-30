import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 15px; margin-bottom: 35px; text-align: center;">
            <div style="display: inline-flex; align-items: center; gap: 8px; padding: 6px 16px; border-radius: 9999px; background: rgba(88, 101, 242, 0.15); border: 1px solid rgba(155, 165, 255, 0.25); color: #9BA5FF; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 22px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #22C55E; box-shadow: 0 0 10px #22C55E; display: inline-block;"></span>
                <span>AI Biometric Attendance v2.4</span>
            </div>
            
            <div style="width: 90px; height: 90px; border-radius: 24px; background: linear-gradient(135deg, rgba(88, 101, 242, 0.25) 0%, rgba(124, 131, 253, 0.1) 100%); border: 1px solid rgba(155, 165, 255, 0.25); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 35px -5px rgba(88, 101, 242, 0.4); margin-bottom: 18px;">
                <img src='{logo_url}' style='height: 60px; width: auto; object-fit: contain;' alt="SnapClass Logo" />
            </div>

            <h1 style="font-size: 3rem; font-weight: 800; letter-spacing: -0.04em; margin-bottom: 10px; line-height: 1.1; color: #FFFFFF;">
                SNAP <span style="background: linear-gradient(135deg, #7C83FD 0%, #9BA5FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CLASS</span>
            </h1>
            
            <p style="font-size: 1.12rem; color: #FFFFFF; font-weight: 600; margin-bottom: 4px;">
                Smarter Classrooms. Smarter Attendance.
            </p>
            <p style="font-size: 0.95rem; color: #A5AEC8; max-width: 520px; margin: 0 auto;">
                Select your portal to continue with AI-powered face recognition, voice verification, and automated class tracking.
            </p>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 15px;">
            <div style="width: 52px; height: 52px; border-radius: 14px; background: linear-gradient(135deg, rgba(88, 101, 242, 0.25) 0%, rgba(124, 131, 253, 0.1) 100%); border: 1px solid rgba(155, 165, 255, 0.2); display: flex; align-items: center; justify-content: center; box-shadow: 0 0 20px -5px rgba(88, 101, 242, 0.35);">
                <img src='{logo_url}' style='height: 34px; width: auto; object-fit: contain;' alt="SnapClass Logo" />
            </div>
            <div>
                <h2 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; margin: 0; line-height: 1; color: #FFFFFF;">
                    SNAP <span style="background: linear-gradient(135deg, #7C83FD 0%, #9BA5FF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CLASS</span>
                </h2>
                <span style="font-size: 0.75rem; color: #9BA5FF; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase;">Cloud Portal</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
