import streamlit as st

from src.UI.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image, ImageOps
import numpy as np
from src.pipelines.face_pipeline import predict_attendance, get_face_embeddings, get_primary_face_embedding, train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendance, unenroll_student_to_subject
import time
import io

from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card


@st.dialog("🎉 Welcome Back!")
def welcome_student_popup(name):
    st.balloons()
    st.markdown(f"## Welcome Back, **{name}**! 👋")
    st.write("Your identity has been verified successfully via FaceID.")
    if st.button("Continue to Dashboard", type="primary", width="stretch", key="btn_welcome_continue"):
        st.session_state.show_welcome_popup = False
        st.rerun()


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data['student_id']

    if st.session_state.get('show_welcome_popup'):
        welcome_student_popup(student_data['name'])

    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {student_data['name']} """)
        if st.button("Logout", type='secondary', key='studentlogoutbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            st.session_state.show_welcome_popup = False
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
            st.session_state.pop('student_reg_photo_bytes', None)
            st.session_state.pop('student_reg_audio_bytes', None)
            st.rerun()

    if 'student_auth_mode' not in st.session_state:
        st.session_state.student_auth_mode = 'login'

    mode_c1, mode_c2 = st.columns(2)
    with mode_c1:
        type_login = 'primary' if st.session_state.student_auth_mode == 'login' else 'secondary'
        if st.button("FaceID Login", type=type_login, width='stretch', icon=':material/face:', key='tab_student_login'):
            st.session_state.student_auth_mode = 'login'
            st.session_state.pop('student_reg_photo_bytes', None)
            st.session_state.pop('student_reg_audio_bytes', None)
            st.rerun()
    with mode_c2:
        type_reg = 'primary' if st.session_state.student_auth_mode == 'register' else 'secondary'
        if st.button("Register New Student", type=type_reg, width='stretch', icon=':material/person_add:', key='tab_student_reg'):
            st.session_state.student_auth_mode = 'register'
            st.session_state.pop('student_reg_photo_bytes', None)
            st.session_state.pop('student_reg_audio_bytes', None)
            st.rerun()

    st.space()

    if st.session_state.student_auth_mode == 'login':
        st.header('Login using FaceID', text_alignment='center')
        st.space()

        photo_source = st.camera_input("Position your face in the center", key="student_login_camera")

        if photo_source:
            with st.spinner('Scanning face & verifying identity...'):
                detected, all_ids, num_faces = predict_attendance(photo_source, threshold=0.60)

                if num_faces == 0:
                    st.warning('Face not detected! Please ensure good lighting and look directly at the camera.')
                elif num_faces > 1:
                    st.warning('Multiple faces detected! Please ensure only one person is in the frame.')
                else:
                    if detected:
                        student_id = list(detected.keys())[0]
                        match_info = detected[student_id]
                        all_students = get_all_students()
                        student = next((s for s in all_students if int(s['student_id']) == int(student_id)), None)

                        if student:
                            st.session_state.is_logged_in = True
                            st.session_state.user_role = 'student'
                            st.session_state.student_data = student
                            conf = match_info.get('confidence', 95.0) if isinstance(match_info, dict) else 95.0
                            st.session_state.show_welcome_popup = True
                            st.session_state.login_confidence = conf
                            st.rerun()
                        else:
                            st.error("Matched student record not found in database.")
                    else:
                        st.info("Face not recognized in our database. You might need to register first.")
                        if st.button("Register as New Student", type='primary', icon=':material/person_add:', key='btn_switch_to_reg'):
                            st.session_state.student_auth_mode = 'register'
                            st.rerun()

    else:
        st.header('Register New Student Profile', text_alignment='center')
        with st.container(border=True):
            new_name = st.text_input("Enter your full name", placeholder='E.g. Lucky Tomar', key="student_reg_name")

            st.subheader("Face Enrollment (Required)")
            st.caption("Capture a clear, front-facing photo with good lighting.")
            reg_camera = st.camera_input("Take a photo of your face", key="student_reg_camera")

            # Persist captured camera photo across reruns (preventing lost photo on submit)
            if reg_camera is not None:
                st.session_state['student_reg_photo_bytes'] = reg_camera.getvalue()

            st.subheader('Voice Enrollment (Optional)')
            st.caption("Record a short phrase (e.g. 'I am present') to enable voice-based attendance.")

            audio_data = None
            try:
                audio_data = st.audio_input('Record your voice', key="student_reg_audio")
                if audio_data is not None:
                    st.session_state['student_reg_audio_bytes'] = audio_data.read()
            except Exception:
                st.caption('Voice recording not supported on this browser.')

            if st.button('Create Student Account', type='primary', width='stretch', key="student_reg_submit"):
                photo_bytes = None
                if reg_camera is not None:
                    photo_bytes = reg_camera.getvalue()
                    st.session_state['student_reg_photo_bytes'] = photo_bytes
                elif 'student_reg_photo_bytes' in st.session_state and st.session_state['student_reg_photo_bytes']:
                    photo_bytes = st.session_state['student_reg_photo_bytes']

                if not new_name or not new_name.strip():
                    st.warning('Please enter your full name!')
                elif not photo_bytes:
                    st.warning('Please capture a face photo!')
                else:
                    final_photo = io.BytesIO(photo_bytes)
                    with st.spinner('Extracting biometric features & creating profile..'):
                        try:
                            face_emb, err_msg, n_faces = get_primary_face_embedding(final_photo)

                            if err_msg or not face_emb:
                                st.error(err_msg or 'Could not detect a clear face in the photo. Please ensure good lighting and look directly into the camera.')
                            else:
                                if n_faces > 1:
                                    st.info(f"Detected {n_faces} faces; selected the primary foreground face for your profile.")

                                voice_emb = None
                                voice_bytes = None
                                if audio_data is not None:
                                    try:
                                        voice_bytes = audio_data.read()
                                    except Exception:
                                        pass
                                if not voice_bytes and 'student_reg_audio_bytes' in st.session_state:
                                    voice_bytes = st.session_state.get('student_reg_audio_bytes')

                                if voice_bytes:
                                    try:
                                        voice_emb = get_voice_embedding(voice_bytes)
                                    except Exception as e:
                                        print(f"Optional voice embedding skipped: {e}")

                                response_data = create_student(new_name.strip(), face_embedding=face_emb, voice_embedding=voice_emb)

                                if response_data and len(response_data) > 0:
                                    st.session_state.pop('student_reg_photo_bytes', None)
                                    st.session_state.pop('student_reg_audio_bytes', None)
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0]
                                    st.session_state.show_welcome_popup = True
                                    st.session_state.login_confidence = 100.0
                                    st.rerun()
                                else:
                                    st.error('Database did not return student data. Please try again.')
                        except Exception as e:
                            st.error(f'Failed to register student: {e}')
    footer_dashboard()