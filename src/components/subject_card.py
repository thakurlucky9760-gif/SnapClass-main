import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div class="subject-card" style="padding: 24px; border-radius: 18px; margin-bottom: 20px; background: rgba(17, 22, 42, 0.75); border: 1px solid rgba(155, 165, 255, 0.15); border-left: 5px solid #5865F2; box-shadow: 0 15px 35px -10px rgba(0, 0, 0, 0.6);">
            <h3 style="margin: 0; font-size: 1.4rem; font-weight: 700; color: #FFFFFF;">{name}</h3>
            <p class="subject-meta" style="margin: 10px 0 14px 0; color: #A5AEC8; font-size: 0.92rem;">
                Code: <span class="subject-code" style="padding: 3px 9px; border-radius: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; background: rgba(88, 101, 242, 0.2); color: #9BA5FF; border: 1px solid rgba(155, 165, 255, 0.2); font-weight: 600;">{code}</span> 
                <span style="margin: 0 6px; color: rgba(155, 165, 255, 0.3);">|</span> 
                Section: <strong style="color: #FFFFFF;">{section}</strong>
            </p>
    """
    
    if stats:
        html += """
            <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px;">
        """
        for icon, label, value in stats:
            html += f'''
                <div class="subject-stat" style="padding: 6px 14px; border-radius: 10px; font-size: 0.88rem; background: rgba(124, 131, 253, 0.12); border: 1px solid rgba(155, 165, 255, 0.16); color: #FFFFFF;">
                    <span>{icon}</span> <strong style="color: #9BA5FF; margin-left: 2px;">{value}</strong> <span style="color: #A5AEC8;">{label}</span>
                </div>
            '''
        html += "</div>"

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
