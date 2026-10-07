# SnapClass

SnapClass is an AI-powered classroom attendance system designed to make attendance faster, more accurate, and less dependent on manual roll calls. The project combines face recognition, voice-based verification, subject management, and data storage to provide a full attendance workflow for teachers and students.

## Overview

SnapClass is built as a Streamlit application with two primary user experiences:

- Teacher portal for creating classes, inviting students, managing attendance, and reviewing attendance records
- Student portal for face-based login, subject enrollment, and personal attendance tracking

The app uses computer-vision and audio-processing pipelines to identify students automatically from uploaded classroom images or spoken responses, then stores attendance results in Supabase.

## Features

### For teachers
- Create and manage subjects
- Share subject enrollment codes with students
- Add student photos for automatic recognition
- Run AI-based attendance analysis from classroom photos
- Use voice attendance checks for a faster verification method
- View attendance records and per-student results

### For students
- Face ID login using a camera snapshot
- Automatic registration with optional voice enrollment
- Enroll into subjects using join codes
- View attendance history across enrolled courses
- Unenroll from classes when needed

### AI components
- Facial recognition using dlib and face-recognition models
- SVM-based student classifier trained from stored face embeddings
- Voice embedding and similarity matching using Resemblyzer
- Subject-based attendance logging with per-session timestamps

## Tech stack

- Python
- Streamlit
- Supabase
- NumPy, Pandas
- scikit-learn
- dlib / face-recognition models
- Resemblyzer
- librosa
- Pillow
- Segno (QR support)

## Project structure

```text
SnapClass/
├── app.py                     # Streamlit app entry point
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .gitignore                # Git exclusions
├── .streamlit/
│   └── secrets.toml.example # Local Supabase config template
├── src/
│   ├── UI/
│   ├── components/
│   ├── database/
│   ├── pipelines/
│   └── screens/
└── venv/                     # Local virtual environment (not tracked)
```

## Requirements

- Python 3.10+
- A Supabase project and API credentials
- A local virtual environment is recommended

## Local setup

1. Clone the repository:

```bash
git clone https://github.com/thakurlucky9760-gif/SnapClass-main.git
cd SnapClass-main
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a local Streamlit secrets file:

```toml
# .streamlit/secrets.toml
supa_base_url = "https://your-project.supabase.co"
supa_base_key = "your-supabase-anon-or-service-role-key"
```

5. Launch the app:

```bash
streamlit run app.py
```

## Supabase setup

This project expects a Supabase backend with the tables needed for:

- teachers
- students
- subjects
- subject_students
- attendance records

The app reads credentials from `st.secrets` via the Streamlit configuration file. Keep this file local and do not commit actual secret values.

## How it works

### Teacher flow
1. Teacher opens the teacher dashboard.
2. Creates a subject and shares the subject access code.
3. Adds reference student photos for recognition training.
4. Captures classroom photos and runs AI-based attendance detection.
5. Reviews attendance results and records are saved.

### Student flow
1. Student logs in using a face image captured from the webcam.
2. If recognized, they are redirected to their student dashboard.
3. If not recognized, they can register a new profile and optionally enroll their voice.
4. They can join subjects using a subject code and check attendance history.

## Notes

- The project is intended for educational and demo use.
- Some models and packages such as `dlib` and `face_recognition_models` can have heavier installation requirements depending on platform.
- For production use, consider adding secure authentication, role-based access control, and a dedicated deployment pipeline.

## License

This project is provided as-is for educational and demonstration purposes.

## Contributing

Contributions are welcome. If you want to improve the app, open a pull request with a clear description of the change and the related functionality it affects.
