import streamlit as st



def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: #5865F2 !important;
                }

                .stApp div[data-testid="stColumn"]{
                    background-color: var(--surface) !important;
                    color: var(--text) !important;
                    padding:2.5rem !important;
                    border-radius: 5rem !important;
                    }
        </style>  

                """
            ,unsafe_allow_html=True)
    

def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: var(--page-bg) !important;
                }

                .stApp h1,
                .stApp h2,
                .stApp h3,
                .stApp h4,
                .stApp [data-testid="stWidgetLabel"],
                .stApp [data-testid="stWidgetLabel"] * {
                    color: #1E293B !important;
                }

                .stApp .dashboard-brand {
                    color: #5865F2 !important;
                }

                .stApp [data-testid="stAlert"] {
                    color: #9E174D !important;
                    background-color: #FCE8F3 !important;
                }

                .stApp [data-testid="stAlert"] * {
                    color: #9E174D !important;
                }

        </style>  

                """
            ,unsafe_allow_html=True)
    

    

def style_base_layout():
# asdasd
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

            :root {
                --page-bg: #E0E3FF;
                --surface: #F7F8FF;
                --text: #1E293B;
                --muted-text: #64748B;
                --border: #C5CAEB;
                --code-bg: #E0E3FF;
                --code-text: #5865F2;
                --chip-bg: #FCE8F3;
                --accent: #5865F2;
            }

            html[data-theme="dark"] {
                --page-bg: #171923;
                --surface: #242838;
                --text: #F4F5FB;
                --muted-text: #C0C5D4;
                --border: #454B60;
                --code-bg: #343B58;
                --code-text: #DDE1FF;
                --chip-bg: #493044;
                --accent: #AAB2FF;
            }

            .subject-card {
                color: var(--text);
                background: var(--surface);
                border: 1px solid var(--border);
                border-left: 8px solid #EB459E;
            }

            .subject-card h3 { color: var(--text); }
            .subject-card .subject-meta { color: var(--muted-text); }
            .subject-card .subject-code {
                color: var(--code-text);
                background: var(--code-bg);
            }
            .subject-card .subject-stat {
                color: var(--text);
                background: var(--chip-bg);
            }
            .dashboard-brand { color: var(--accent); }
            .dashboard-footer { color: var(--text); }

            .credit-footer {
                margin-top: 2rem;
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: 0.4rem;
                font-family: 'Outfit', sans-serif;
                font-size: 0.95rem;
                line-height: 1.2;
            }
            .credit-footer-home { color: white; }
            .credit-footer-dashboard { color: var(--text); }
            .credit-heart {
                color: #EB459E;
                font-size: 1.1rem;
                line-height: 1;
            }
            .credit-footer-home .credit-heart { color: #FFD166; }
            .credit-name { font-weight: 700; }

                
         /* Hide Top Bar of streamlit */
                
            #MainMenu, footer, header {
                visibility: hidden;
            }
                
            .block-container {
                padding-top:1.5rem !important;    
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height:1.1 1important;
                margin-bottom:0rem !important;
            }
                

            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
            }
                
            h3, h4, p {
                font-family: 'Outfit', sans-serif;    
            }
                

            button{
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform :scale(1.05)}
        </style>  

                """
            ,unsafe_allow_html=True)