import streamlit as st
def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
        <div class="subject-card" style="padding:25px; border-radius:20px; margin-bottom:20px;">
        <h3 style="margin:0; font-size:1.5rem">{name}</h3>
        <p class="subject-meta" style="margin:10px 0;">Code : <span class="subject-code" style="padding:2px 8px; border-radius:5px;">{code} </span> | Section : {section}</p>
        
        """
    
    if stats:
        html+= """
        <div style="display:flex; gap:8px; flex-wrap:wrap;">
        """
        for icon, label, value in stats:
            html+= f'<div class="subject-stat" style="padding:5px 12px; border-radius:12px; font-size:0.9rem">{icon} <b>{value}</b> {label} </div>'
        
        html+= "</div>"

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()