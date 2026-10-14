
import dlib
import numpy as np
import face_recognition_models
from PIL import Image, ImageOps
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def preprocess_image(image_input, max_dimension=1600):
    """
    Normalizes any image (PIL Image, numpy array, or uploaded file) into
    a clean, right-side-up, uint8 RGB numpy array.
    Resizes oversized images to prevent excessive dlib computation times.
    """
    if isinstance(image_input, np.ndarray):
        img_pil = Image.fromarray(image_input)
    elif isinstance(image_input, Image.Image):
        img_pil = image_input
    else:
        # File-like object (UploadedFile, BytesIO)
        if hasattr(image_input, 'seek'):
            image_input.seek(0)
        img_pil = Image.open(image_input)

    # Automatically rotate according to EXIF orientation tag (e.g. smartphone photos)
    img_pil = ImageOps.exif_transpose(img_pil)

    # Convert to standard RGB (drops alpha channel if present)
    img_pil = img_pil.convert('RGB')

    # Downscale very large photos while preserving aspect ratio
    w, h = img_pil.size
    if max(w, h) > max_dimension:
        scale = max_dimension / float(max(w, h))
        new_size = (int(w * scale), int(h * scale))
        img_pil = img_pil.resize(new_size, Image.Resampling.LANCZOS)

    return np.ascontiguousarray(np.array(img_pil), dtype=np.uint8)


def get_face_embeddings(image_input, upsample=1, num_jitters=1):
    """
    Detects all faces in the image and returns list of 128D numpy face embeddings.
    """
    image_np = preprocess_image(image_input)
    detector, sp, facerec = load_dlib_models()

    # Run frontal detector
    faces = detector(image_np, upsample)

    # If no faces found on a large image, retry with upsample=1 if upsample was 0
    if len(faces) == 0 and upsample == 0:
        faces = detector(image_np, 1)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, num_jitters)
        encodings.append(np.array(face_descriptor, dtype=np.float64))

    return encodings


def get_primary_face_embedding(image_input):
    """
    Used during student registration.
    Extracts the embedding of the primary (largest) face in the image.
    Returns (embedding_list, error_message, num_faces_detected).
    """
    image_np = preprocess_image(image_input)
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 1)
    if len(faces) == 0:
        # Retry with upsample=2 in case face is smaller or camera resolution is low
        faces = detector(image_np, 2)

    if len(faces) == 0:
        return None, "No face detected in the photo. Please ensure good lighting and face the camera directly.", 0

    # Pick the largest face in foreground by bounding box area
    largest_face = max(faces, key=lambda f: (f.right() - f.left()) * (f.bottom() - f.top()))
    shape = sp(image_np, largest_face)
    face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
    emb = np.array(face_descriptor, dtype=np.float64).tolist()

    return emb, None, len(faces)


@st.cache_data(ttl=30)
def get_cached_student_database():
    """
    Fetches all students and extracts valid face embeddings.
    Cached with short TTL to avoid redundant Supabase queries.
    """
    students = get_all_students() or []
    valid_students = []
    for s in students:
        emb = s.get('face_embedding')
        if emb:
            try:
                emb_np = np.array(emb, dtype=np.float64)
                if emb_np.size == 128:
                    valid_students.append({
                        'student_id': int(s['student_id']),
                        'name': s.get('name', 'Student'),
                        'face_embedding': emb_np
                    })
            except Exception:
                continue
    return valid_students


def train_classifier():
    """
    Invalidates the cached student embeddings so newly registered students
    are recognized immediately.
    """
    get_cached_student_database.clear()
    return True


def predict_attendance(class_image_np, candidate_students=None, threshold=0.60):
    """
    Detects faces in class_image_np and matches them against candidate students.
    Uses Euclidean distance matching with greedy assignment:
    - Finds the best matching candidate per face.
    - Ensures each student in a single photo is matched at most once.
    - Discards any face whose distance is greater than the resemblance threshold.

    Returns:
        (detected_students_dict, all_candidate_ids, num_faces_detected)
    where detected_students_dict maps student_id -> dict with details (truthy).
    """
    encodings = get_face_embeddings(class_image_np)
    num_faces = len(encodings)

    if candidate_students is None:
        students_db = get_cached_student_database()
    else:
        # Normalize provided candidate list (e.g. enrolled students in a subject)
        students_db = []
        for s in candidate_students:
            # Handle nested student object if coming from subject_students join
            student_obj = s.get('student') if isinstance(s, dict) and 'student' in s and isinstance(s['student'], dict) else s
            if not student_obj or not isinstance(student_obj, dict):
                continue
            emb = student_obj.get('face_embedding')
            if emb:
                try:
                    emb_np = np.array(emb, dtype=np.float64)
                    if emb_np.size == 128:
                        students_db.append({
                            'student_id': int(student_obj['student_id']),
                            'name': student_obj.get('name', 'Student'),
                            'face_embedding': emb_np
                        })
                except Exception:
                    continue

    all_candidate_ids = [s['student_id'] for s in students_db]

    if num_faces == 0 or len(students_db) == 0:
        return {}, all_candidate_ids, num_faces

    # Build match candidates matrix (distance <= threshold)
    potential_matches = []
    for face_idx, enc in enumerate(encodings):
        for s in students_db:
            dist = float(np.linalg.norm(s['face_embedding'] - enc))
            if dist <= threshold:
                confidence = max(0.0, min(100.0, round((1.0 - (dist / threshold)) * 100, 1)))
                potential_matches.append((dist, face_idx, s['student_id'], s['name'], confidence))

    # Sort matches by distance ascending (best matches first)
    potential_matches.sort(key=lambda m: m[0])

    assigned_faces = set()
    assigned_students = set()
    detected_students = {}

    for dist, face_idx, sid, name, confidence in potential_matches:
        if face_idx not in assigned_faces and sid not in assigned_students:
            assigned_faces.add(face_idx)
            assigned_students.add(sid)
            detected_students[sid] = {
                'student_id': sid,
                'name': name,
                'distance': round(dist, 4),
                'confidence': confidence
            }

    return detected_students, all_candidate_ids, num_faces