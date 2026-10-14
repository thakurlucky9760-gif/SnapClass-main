import streamlit as st

from supabase import create_client, Client

# Support service_role secret key for backend security or default supa_base_key
api_key = st.secrets.get("supa_service_key") or st.secrets.get("supa_base_key")

supabase: Client = create_client(
    st.secrets["supa_base_url"],
    api_key
)