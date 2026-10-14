import streamlit as st
from src.database.db import create_subject



@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of new subject")
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input("Subject Name", placeholder="Introduction to Computer Science")
    sub_section = st.text_input("Section", placeholder="A")


    if st.button("Create Subject Now", type='primary', width='stretch'):
        c_sub_id = sub_id.strip().upper() if sub_id else ""
        c_sub_name = sub_name.strip() if sub_name else ""
        c_sub_section = sub_section.strip() if sub_section else ""

        if c_sub_id and c_sub_name and c_sub_section:
            try:
                create_subject(c_sub_id, c_sub_name, c_sub_section, teacher_id)
                st.toast("Subject Created Successfully!", icon="🎉")
                st.rerun()
            except Exception as e:
                st.error(f"Error creating subject: {str(e)}")
        else:
            st.warning("Please fill in all the fields.")