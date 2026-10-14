import streamlit as st
from PIL import Image, ImageOps
import io


@st.dialog("Capture or upload photos")
def add_photos_dialog():
    st.write('Add classroom photos to scan for attendance.')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    if 'added_photo_signatures' not in st.session_state:
        st.session_state.added_photo_signatures = set()

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)
    with t1:
        type_camera = "primary" if st.session_state.photo_tab == 'camera' else 'tertiary'
        if st.button('Camera', type=type_camera, width='stretch'):
            st.session_state.photo_tab = 'camera'
            st.rerun()

    with t2:
        type_upload = "primary" if st.session_state.photo_tab == 'upload' else 'tertiary'
        if st.button('Upload photos', type=type_upload, width='stretch'):
            st.session_state.photo_tab = 'upload'
            st.rerun()

    if st.session_state.photo_tab == 'camera':
        cam_photo = st.camera_input('Take Snapshot', key='dialog_cam')
        if cam_photo:
            cam_bytes = cam_photo.getvalue()
            cam_sig = hash(cam_bytes)
            if cam_sig not in st.session_state.added_photo_signatures:
                img = Image.open(io.BytesIO(cam_bytes))
                img = ImageOps.exif_transpose(img).convert('RGB')
                st.session_state.attendance_images.append(img)
                st.session_state.added_photo_signatures.add(cam_sig)
                st.toast('Photo Captured & Added!')

    if st.session_state.photo_tab == 'upload':
        uploaded_files = st.file_uploader(
            'Choose classroom image files',
            type=['jpg', 'png', 'jpeg'],
            accept_multiple_files=True,
            key='dialog_upload'
        )

        if uploaded_files:
            newly_added = 0
            for f in uploaded_files:
                sig = (f.name, f.size)
                if sig not in st.session_state.added_photo_signatures:
                    f.seek(0)
                    img = Image.open(f)
                    img = ImageOps.exif_transpose(img).convert('RGB')
                    st.session_state.attendance_images.append(img)
                    st.session_state.added_photo_signatures.add(sig)
                    newly_added += 1
            if newly_added > 0:
                st.toast(f'{newly_added} photo(s) added successfully!')

    st.divider()
    curr_count = len(st.session_state.attendance_images)
    st.caption(f"Total photos ready for scanning: **{curr_count}**")

    if st.button('Done / Back to Attendance', type='primary', width='stretch'):
        st.rerun()