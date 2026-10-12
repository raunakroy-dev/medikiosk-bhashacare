
import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

# --------------------------------------------------
# Configuration
# --------------------------------------------------
load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY", "").strip()

STT_URL = "https://api.sarvam.ai/speech-to-text"
TRANSLATE_URL = "https://api.sarvam.ai/translate"

LANGUAGES = {
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Odia": "od-IN",
    "English": "en-IN",
}

st.set_page_config(
    page_title="MediKiosk BhashaCare",
    page_icon="🏥",
    layout="wide",
)

# --------------------------------------------------
# Sarvam API functions
# --------------------------------------------------
def transcribe_audio(audio_bytes, filename, mime_type, language_code):
    """Convert recorded or uploaded speech into text."""

    if not API_KEY:
        raise RuntimeError(
            "SARVAM_API_KEY is missing. Check your .env file."
        )

    if not audio_bytes:
        raise RuntimeError("No audio was provided.")

    headers = {
        "api-subscription-key": API_KEY,
    }

    files = {
        "file": (
            filename,
            audio_bytes,
            mime_type or "application/octet-stream",
        )
    }

    data = {
        "model": "saaras:v4",
        "mode": "transcribe",
        "language_code": language_code,
    }

    response = requests.post(
        STT_URL,
        headers=headers,
        files=files,
        data=data,
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"Speech recognition failed "
            f"({response.status_code}): {response.text[:1000]}"
        )

    result = response.json()
    transcript = result.get("transcript", "").strip()

    if not transcript:
        raise RuntimeError(
            "No words were detected. Try recording again "
            "and check that the selected language is correct."
        )

    return transcript


def translate_to_english(text, source_language_code):
    """Translate the patient's statement into English."""

    if not text.strip():
        return ""

    if source_language_code == "en-IN":
        return text

    if not API_KEY:
        raise RuntimeError(
            "SARVAM_API_KEY is missing. Check your .env file."
        )

    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "input": text,
        "source_language_code": source_language_code,
        "target_language_code": "en-IN",
        "model": "mayura:v1",
        "mode": "formal",
    }

    response = requests.post(
        TRANSLATE_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    if not response.ok:
        raise RuntimeError(
            f"Translation failed "
            f"({response.status_code}): {response.text[:1000]}"
        )

    result = response.json()
    translated = result.get("translated_text", "").strip()

    if not translated:
        raise RuntimeError(
            "The translation response was empty. Please try again."
        )

    return translated


def build_intake(
    original_statement,
    english_translation,
    language_name,
    chief_complaint,
    duration,
    associated_symptoms,
    medical_history,
    medications,
    allergies,
    additional_details,
):
    """Create a structured intake record without diagnosing."""

    return {
        "application": "MediKiosk BhashaCare",
        "created_at": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "patient_language": language_name,
        "original_patient_statement": original_statement,
        "english_translation": english_translation,
        "patient_reported_details": {
            "chief_complaint": chief_complaint.strip(),
            "duration": duration.strip(),
            "associated_symptoms": associated_symptoms.strip(),
            "relevant_medical_history": medical_history.strip(),
            "medications_reported": medications.strip(),
            "allergies_reported": allergies.strip(),
            "additional_details": additional_details.strip(),
        },
        "clinical_review": "Pending clinician review",
        "diagnosis": None,
        "treatment_recommendation": None,
        "safety_note": (
            "This is a pre-consultation intake prototype, not a "
            "diagnostic tool. Blank fields mean information was not "
            "recorded; they do not mean the patient has no symptoms, "
            "medical history, medications, or allergies."
        ),
    }


# --------------------------------------------------
# App interface
# --------------------------------------------------
st.title("🏥 MediKiosk BhashaCare")
st.subheader("Your language. Your symptoms. Better communication.")

st.write(
    "A multilingual pre-consultation assistant that helps patients "
    "share their concerns and prepares an intake summary for a clinician."
)

st.info(
    "Hackathon prototype: use fictional demo information only. "
    "Do not enter real patient identifiers or confidential medical data."
)

if not API_KEY:
    st.error(
        "Your Sarvam API key was not loaded. Open the .env file and "
        "set SARVAM_API_KEY to your actual key, then restart the app."
    )

st.divider()

# --------------------------------------------------
# Patient language and input method
# --------------------------------------------------
st.header("1. Patient statement")

col1, col2 = st.columns(2)

with col1:
    language_name = st.selectbox(
        "Select the language being spoken or typed",
        list(LANGUAGES.keys()),
        index=1,
    )

language_code = LANGUAGES[language_name]

with col2:
    input_method = st.radio(
        "How would you like to provide the statement?",
        ["Type text", "Record voice", "Upload audio"],
        horizontal=True,
    )

original_statement = ""
audio_bytes = None
audio_filename = None
audio_mime_type = None

if input_method == "Type text":
    original_statement = st.text_area(
        "Patient's statement",
        placeholder=(
            "Enter a fictional patient statement in the selected "
            "language..."
        ),
        height=150,
    )

elif input_method == "Record voice":
    st.caption(
        "Record a short, clear statement. Allow microphone access "
        "if your browser asks. Keep the recording under 30 seconds "
        "for this prototype."
    )

    audio_value = st.audio_input("Record patient statement")

    if audio_value is not None:
        audio_bytes = audio_value.getvalue()
        audio_filename = "patient_recording.wav"
        audio_mime_type = audio_value.type or "audio/wav"

        st.audio(audio_bytes, format=audio_mime_type)
        st.success("Recording captured. You can now process it.")

elif input_method == "Upload audio":
    uploaded_audio = st.file_uploader(
        "Upload a short audio recording",
        type=["wav", "mp3", "m4a", "flac", "ogg"],
    )

    if uploaded_audio is not None:
        audio_bytes = uploaded_audio.getvalue()
        audio_filename = uploaded_audio.name
        audio_mime_type = (
            uploaded_audio.type or "application/octet-stream"
        )

        st.audio(audio_bytes, format=audio_mime_type)
        st.success("Audio uploaded. You can now process it.")

# --------------------------------------------------
# Additional intake fields
# --------------------------------------------------
st.divider()
st.header("2. Intake details")

st.caption(
    "Fill in only what the patient reports. Leave unknown or "
    "unasked information blank."
)

chief_complaint = st.text_input(
    "Main concern",
    placeholder="Example: headache",
)

duration = st.text_input(
    "How long has this been happening?",
    placeholder="Example: since yesterday",
)

associated_symptoms = st.text_area(
    "Other symptoms reported",
    placeholder="Example: nausea, if reported",
    height=80,
)

medical_history = st.text_area(
    "Relevant medical history reported",
    placeholder="Enter only information the patient provides",
    height=80,
)

medications = st.text_input(
    "Medications reported",
    placeholder="Leave blank if not recorded",
)

allergies = st.text_input(
    "Allergies reported",
    placeholder="Leave blank if not recorded",
)

additional_details = st.text_area(
    "Additional patient-reported details",
    placeholder="Other relevant details",
    height=80,
)

# --------------------------------------------------
# Process input
# --------------------------------------------------
st.divider()
st.header("3. Generate intake summary")

if st.button(
    "Process patient intake",
    type="primary",
    use_container_width=True,
):
    try:
        # Get original statement from the chosen input method.
        if input_method == "Type text":
            original_statement = original_statement.strip()

            if not original_statement:
                st.error("Please type the patient's statement first.")
                st.stop()

        else:
            if not audio_bytes:
                st.error(
                    "Please record or upload audio before processing."
                )
                st.stop()

            with st.spinner("Recognizing the patient's speech..."):
                original_statement = transcribe_audio(
                    audio_bytes=audio_bytes,
                    filename=audio_filename,
                    mime_type=audio_mime_type,
                    language_code=language_code,
                )

            st.success("Speech recognition completed.")

        # Translate original statement.
        with st.spinner("Preparing the English translation..."):
            english_translation = translate_to_english(
                original_statement,
                language_code,
            )

        # Build the intake record from the actual patient statement
        # and details explicitly entered by the operator.
        intake = build_intake(
            original_statement=original_statement,
            english_translation=english_translation,
            language_name=language_name,
            chief_complaint=chief_complaint,
            duration=duration,
            associated_symptoms=associated_symptoms,
            medical_history=medical_history,
            medications=medications,
            allergies=allergies,
            additional_details=additional_details,
        )

        # Store the result so it remains visible after reruns.
        st.session_state["intake_result"] = intake

    except requests.exceptions.Timeout:
        st.error(
            "The Sarvam API took too long to respond. "
            "Please try again with a shorter recording."
        )

    except requests.exceptions.RequestException as exc:
        st.error(f"Could not connect to the Sarvam API: {exc}")

    except Exception as exc:
        st.error(str(exc))

# --------------------------------------------------
# Display results
# --------------------------------------------------
intake = st.session_state.get("intake_result")

if intake:
    st.divider()
    st.header("4. Patient intake summary")

    st.subheader("Original patient statement")
    st.text_area(
        "Original statement",
        value=intake["original_patient_statement"],
        height=100,
        disabled=True,
        key="result_original",
    )

    st.subheader("English translation")
    st.text_area(
        "English translation",
        value=intake["english_translation"],
        height=100,
        disabled=True,
        key="result_translation",
    )

    st.subheader("Structured details")

    details = intake["patient_reported_details"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Main concern**")
        st.write(details["chief_complaint"] or "Not recorded")

        st.markdown("**Duration**")
        st.write(details["duration"] or "Not recorded")

        st.markdown("**Other symptoms**")
        st.write(details["associated_symptoms"] or "Not recorded")

        st.markdown("**Medical history**")
        st.write(details["relevant_medical_history"] or "Not recorded")

    with col2:
        st.markdown("**Medications reported**")
        st.write(details["medications_reported"] or "Not recorded")

        st.markdown("**Allergies reported**")
        st.write(details["allergies_reported"] or "Not recorded")

        st.markdown("**Additional details**")
        st.write(details["additional_details"] or "Not recorded")

    st.warning(
        "Clinician review is pending. This prototype does not "
        "diagnose conditions or recommend treatment."
    )

    with st.expander("View complete structured JSON"):
        st.json(intake)

    st.download_button(
        label="Download intake as JSON",
        data=json.dumps(intake, ensure_ascii=False, indent=2),
        file_name="medikiosk_patient_intake.json",
        mime="application/json",
        use_container_width=True,
    )
