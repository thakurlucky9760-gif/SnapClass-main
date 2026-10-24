import streamlit as st

from src.UI.base_layout import style_background_dashboard, style_base_layout

from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subjects, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import numpy as np

from datetime import datetime
from src.utils.time_utils import (
    get_current_utc_iso,
    format_timestamp,
    parse_timestamp,
    get_available_timezones
)

import pandas as pd

from src.database.config import supabase


from src.components.dialog_voice_attendance import voice_attendance_dialog
def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()





def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome, {teacher_data['name']} """)
        if st.button("Logout", type='secondary', key='teacherlogoutbtn', shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.teacher_data 
            st.rerun()


    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()


    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    


    footer_dashboard()

def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.session_state.added_photo_signatures = set()
            st.rerun()

    with c2:
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            # Fetch enrolled students for this subject first to prioritize and scope matching
            enrolled_res = supabase.table('subject_students').select(
                "*, student(*)"
            ).eq('subject_id', selected_subject_id).execute()
            enrolled_students = enrolled_res.data or []

            if not enrolled_students:
                st.warning('No students are enrolled in this course yet. Please enroll students first.')
            else:
                with st.spinner('Deep scanning classroom photos...'):
                    all_detected_ids = {}

                    for idx, img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB'))
                        detected, _, num_faces = predict_attendance(
                            img_np,
                            candidate_students=enrolled_students,
                            threshold=0.60
                        )

                        if detected:
                            for sid, match_data in detected.items():
                                student_id = int(sid)
                                conf = match_data.get('confidence', '') if isinstance(match_data, dict) else ''
                                conf_str = f" ({conf}%)" if conf else ""
                                all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}{conf_str}")

                    results, attendance_to_log = [], []
                    current_timestamp = get_current_utc_iso()

                    for node in enrolled_students:
                        student = node.get('student')
                        if not student:
                            continue
                        sid = int(student['student_id'])
                        sources = all_detected_ids.get(sid, [])
                        is_present = len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": sid,
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': sid,
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)











def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    col1, col2 = st.columns(2)
    with col1:
        st.header('Manage Subjects', width='stretch')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)


    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]
            def share_btn(curr_sub=sub):
                if st.button(f"Share Code: {curr_sub['name']}", key=f"share_{curr_sub['subject_code']}", icon=":material/share:"):
                    share_subject_dialog(curr_sub['name'], curr_sub['subject_code'])
                st.space()

            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    c1, c2 = st.columns([3, 2], vertical_alignment='center')
    with c1:
        st.header('Attendance Records')
    with c2:
        tz_options = get_available_timezones()
        selected_tz = st.selectbox(
            "Timezone Display",
            options=tz_options,
            index=0,
            key="teacher_records_tz"
        )

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No attendance records found yet. Take attendance using AI Face Scan or Voice Attendance.")
        return

    records = [r for r in records if r.get('id') != 19]

    data = []

    for r in records:
        ts = r.get('timestamp')
        dt_utc = parse_timestamp(ts)
        ts_group = dt_utc.strftime('%Y-%m-%d %H:%M:%S') if dt_utc else (ts.split('.')[0] if ts else 'N/A')
        formatted_time = format_timestamp(ts, tz_choice=selected_tz)
        student_obj = r.get('student')
        student_name = student_obj.get('name') if student_obj else f"Student #{r.get('student_id')}"

        data.append({
            "ts_sort": dt_utc or ts,
            "ts_group": ts_group,
            "Time": formatted_time,
            "Subject": r['subjects']['name'],
            "Subject Code": r['subjects']['subject_code'],
            "Student": student_name,
            "Student ID": r.get('student_id'),
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    # Subject filter
    subjects_list = ["All Subjects"] + sorted(list(df['Subject'].unique()))
    col_filter, _ = st.columns([2, 3])
    with col_filter:
        selected_subject = st.selectbox("Filter by Subject", subjects_list, key="records_subject_filter")

    filtered_df = df if selected_subject == "All Subjects" else df[df['Subject'] == selected_subject]

    if filtered_df.empty:
        st.info(f"No records found for subject: {selected_subject}")
        return

    summary = (
        filtered_df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count'),
            ts_sort=('ts_sort', 'max')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " / "
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = (
        summary.sort_values(by='ts_sort', ascending=False)
        [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
    )

    st.dataframe(display_df, width='stretch', hide_index=True)

    # Detailed session drill-down
    with st.expander("🔍 View Detailed Student Breakdown by Session"):
        sorted_summary = summary.sort_values(by='ts_sort', ascending=False).reset_index(drop=True)
        session_options = sorted_summary['Time'] + " — " + sorted_summary['Subject'] + " (" + sorted_summary['Subject Code'] + ")"
        selected_session = st.selectbox("Select Session", session_options.tolist(), key="select_session_drilldown")

        if selected_session:
            sel_idx = session_options.tolist().index(selected_session)
            target_ts_group = sorted_summary.iloc[sel_idx]['ts_group']
            target_code = sorted_summary.iloc[sel_idx]['Subject Code']

            session_students = filtered_df[
                (filtered_df['ts_group'] == target_ts_group) &
                (filtered_df['Subject Code'] == target_code)
            ]

            detail_rows = []
            for _, s_row in session_students.iterrows():
                detail_rows.append({
                    "Student ID": s_row['Student ID'],
                    "Student Name": s_row['Student'],
                    "Status": "✅ Present" if s_row['is_present'] else "❌ Absent"
                })

            st.dataframe(pd.DataFrame(detail_rows), hide_index=True, width='stretch')


def login_teacher(username, password):
    if not username or not password:
        return False
    
    teacher = teacher_login(username.strip(), password)

    if teacher:
        st.session_state.user_role ='teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False
def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password', text_alignment='center')
    st.space()
    st.space()


    teacher_username = st.text_input("Enter username", placeholder='ananyaroy')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if login_teacher(teacher_username, teacher_pass):
                st.toast("welcome back!", icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username and password combo")

    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'register'
            st.rerun()

    footer_dashboard()



def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    teacher_username = teacher_username.strip() if teacher_username else ""
    teacher_name = teacher_name.strip() if teacher_name else ""
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required!"
    if check_teacher_exists(teacher_username):
        return False, "Username already taken"
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match"
    
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Sucessfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"
    

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()



    st.header('Register your teacher profile')

    st.space()
    st.space()

    
    teacher_username = st.text_input("Enter username", placeholder='ananyaroy')

    teacher_name = st.text_input("Enter name", placeholder='Ananya Roy')

    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)


    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'
            st.rerun()

    footer_dashboard()