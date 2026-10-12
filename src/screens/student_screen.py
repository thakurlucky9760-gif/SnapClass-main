import streamlit as st

from src.UI.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='studentlogoutbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data 
            st.rerun()


    st.space()

    c1, c2 =st.columns(2)
    with c1:
        st.header('Your Enrolled Subjects')
    with c2:
        if st.button('Enroll in Subject', type='primary', width='stretch'):
            enroll_dialog()


    st.divider()


    with st.spinner('Loading your enrolled subjects..'):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']

        if sid not in stats_map:
            stats_map[sid] = {"total":0, "attended": 0}

        stats_map[sid]['total'] +=1

        if log.get('is_present'):
            stats_map[sid]['attended'] += 1


    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']


        stats = stats_map.get(sid, {"total": 0, "attended": 0})
        def unenroll_button(curr_sid=sid, curr_name=sub['name']):
            if st.button(
                "Unenroll from this course",
                key=f"unenroll_{curr_sid}",
                type='tertiary',
                width='stretch',
                icon=':material/delete_forever:'
            ):
                unenroll_student_to_subject(student_id, curr_sid)
                st.toast(f"Unenrolled from {curr_name} successfully!")
                st.rerun()

        with cols[i % 2]:

            subject_card(
                name = sub['name'],
                code =sub['subject_code'],
                section = sub['section'],
                stats = [
                    ('📅', 'Total', stats['total']),
                    ('✅', 'Attended', stats['attended']),
                ],
                footer_callback=unenroll_button
            )
    footer_dashboard()


def student_screen():


    style_background_dashboard()
    style_base_layout()


    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    if 'student_auth_mode' not in st.session_state:
        st.session_state.student_auth_mode = 'login'

    mode_c1, mode_c2 = st.columns(2)
    with mode_c1:
        type_login = 'primary' if st.session_state.student_auth_mode == 'login' else 'secondary'
        if st.button("FaceID Login", type=type_login, width='stretch', icon=':material/face:', key='tab_student_login'):
            st.session_state.student_auth_mode = 'login'
            st.rerun()
    with mode_c2:
        type_reg = 'primary' if st.session_state.student_auth_mode == 'register' else 'secondary'
        if st.button("Register New Student", type=type_reg, width='stretch', icon=':material/person_add:', key='tab_student_reg'):
            st.session_state.student_auth_mode = 'register'
            st.rerun()

    st.space()

    if st.session_state.student_auth_mode == 'login':
        st.header('Login using FaceID', text_alignment='center')
        st.space()

        photo_source = st.camera_input("Position your face in the center", key="student_login_camera")

        if photo_source:
            img_pil = Image.open(photo_source).convert('RGB')
            img = np.array(img_pil)

            with st.spinner('AI is scanning..'):
                detected, all_ids, num_faces = predict_attendance(img)

                if num_faces == 0:
                    st.warning('Face not found! Please position your face clearly in the frame.')
                elif num_faces > 1:
                    st.warning('Multiple faces found! Please ensure only one person is in the frame.')
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        all_students = get_all_students()
                        student = next((s for s in all_students if s['student_id'] == student_id), None)

                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            st.toast(f"Welcome Back {student['name']}!")
                            time.sleep(1)
                            st.rerun()
                    else:
                        st.info("Face not recognized! You might be a new student.")
                        if st.button("Register as New Student", type='primary', icon=':material/person_add:', key='btn_switch_to_reg'):
                            st.session_state.student_auth_mode = 'register'
                            st.rerun()

    else:
        st.header('Register New Student Profile', text_alignment='center')
        with st.container(border=True):
            new_name = st.text_input("Enter your full name", placeholder='E.g. Hamza Rizvi', key="student_reg_name")

            st.subheader("Face Enrollment")
            reg_camera = st.camera_input("Take a photo of your face", key="student_reg_camera")
            reg_upload = st.file_uploader("Or upload a face photo", type=['jpg', 'jpeg', 'png'], key="student_reg_upload")

            final_photo = reg_camera or reg_upload

            st.subheader('Optional : Voice Enrollment')
            st.info("Record a short phrase (e.g. 'I am present') for voice attendance")

            audio_data = None
            try:
                audio_data = st.audio_input('Record your voice', key="student_reg_audio")
            except Exception:
                st.info('Voice recording not available')

            if st.button('Create Student Account', type='primary', width='stretch', key="student_reg_submit"):
                if not new_name or not new_name.strip():
                    st.warning('Please enter your full name!')
                elif not final_photo:
                    st.warning('Please capture or upload a face photo!')
                else:
                    with st.spinner('Extracting biometric features & creating profile..'):
                        try:
                            img_pil = Image.open(final_photo).convert('RGB')
                            img = np.array(img_pil)
                            encodings = get_face_embeddings(img)

                            if not encodings:
                                st.error('Could not detect a face in the provided photo. Please ensure good lighting and face the camera directly.')
                            else:
                                face_emb = encodings[0].tolist()

                                voice_emb = None
                                if audio_data:
                                    try:
                                        audio_bytes = audio_data.read()
                                        if audio_bytes:
                                            voice_emb = get_voice_embedding(audio_bytes)
                                    except Exception as e:
                                        print(f"Voice embedding error: {e}")

                                response_data = create_student(new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                                if response_data and len(response_data) > 0:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0]
                                    st.toast(f'Profile Created! Welcome {new_name.strip()}!')
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error('Database did not return student data. Please try again.')
                        except Exception as e:
                            st.error(f'Failed to register student: {e}')
    footer_dashboard()