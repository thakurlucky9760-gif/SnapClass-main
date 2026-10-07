import streamlit as st

from supabase import create_client,client
supabase:client=create_client(
    st.secrets["supa_base_url"],
    st.secrets["supa_base_key"]
)