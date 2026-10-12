# 🏥 MediKiosk BhashaCare
### Breaking Language Barriers in Healthcare with Sarvam AI

**MediKiosk BhashaCare** is a multilingual, AI-powered pre-consultation patient intake assistant designed to help patients communicate their symptoms in their preferred Indian language and help healthcare professionals review that information more easily.

The application uses Sarvam AI for speech recognition and translation to transform a patient's statement into an English translation and a structured patient intake summary.

## 🚩 Problem Statement

Language barriers can make it difficult for patients to explain their symptoms clearly, especially when healthcare professionals and patients speak different languages. This can create communication challenges during the initial stages of an outpatient department (OPD) visit.

MediKiosk BhashaCare aims to make this first step easier by supporting multilingual patient input and preparing information for clinician review.

## 💡 Our Solution

The application allows a patient or kiosk operator to enter a statement using text, record speech, or upload an audio recording. Sarvam AI processes the speech and translates non-English statements into English.

The application then presents the original statement alongside its English translation and a structured intake sheet containing patient-reported details.

**Our guiding principle:** Preserve what the patient says, improve accessibility, and keep clinical decisions with qualified healthcare professionals.

## ✨ Key Features

- **Multilingual support:** Input support for Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia, and English.
- **Voice-based input:** Record a patient's statement directly in the application.
- **Audio upload:** Upload supported audio recordings for transcription.
- **Text-based input:** Enter a patient statement manually.
- **AI-powered speech recognition:** Uses Sarvam AI's speech-to-text API.
- **English translation:** Translates non-English statements into English using Sarvam AI.
- **Structured patient intake:** Organizes the main concern, duration, associated symptoms, relevant medical history, reported medications, allergies, and additional details.
- **JSON export:** Download the intake summary as a JSON file.
- **Clinician-first design:** Leaves diagnosis and treatment decisions to qualified clinicians.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| Sarvam AI Speech-to-Text API | Speech recognition |
| Sarvam AI Translation API | Translation into English |
| Requests | API communication |
| python-dotenv | Local environment variable management |
| JSON | Structured intake export |

## 🔄 How It Works

1. **Choose a language:** Select the language used by the patient.
2. **Provide the statement:** Type text, record speech, or upload an audio file.
3. **Recognize speech:** For audio input, Sarvam AI converts speech into text.
4. **Translate:** Non-English statements are translated into English.
5. **Complete the intake:** The operator records any additional patient-reported details.
6. **Review the summary:** The application displays the original statement, translation, and structured intake information.
7. **Export:** Download the resulting intake record in JSON format for demonstration or further processing.

## 🧰 Getting Started

### Prerequisites

- Python 3.10 or a compatible Python version
- A Sarvam AI API key
- Internet connectivity
- A modern web browser

### 1. Clone the repository

```bash
git clone https://github.com/raunakroy-dev/medikiosk-bhashacare.git
cd medikiosk-bhashacare
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create a `.env` file in the project root directory:

```dotenv
SARVAM_API_KEY=your_actual_sarvam_api_key
```

Replace the placeholder with your own API key.

**Security:** Never commit `.env` or expose your API key in source code, screenshots, logs, or public repositories.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where you can open the application.

## 📂 Project Structure

```text
medikiosk-bhashacare/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env                  # Local only; do not commit
```

## 🏥 Example Use Case

A patient speaks in Hindi:

> मुझे कल से सिरदर्द है और थोड़ा बुखार भी है।

The application transcribes the statement and presents an English translation, such as:

> I have had a headache since yesterday and also have a slight fever.

The original statement is retained alongside the translation. The operator can then add the duration, associated symptoms, and other information explicitly reported by the patient.

*This example is illustrative. Actual transcription and translation may vary.*

## 🔐 Privacy, Safety, and Limitations

MediKiosk BhashaCare is a hackathon prototype intended to demonstrate multilingual pre-consultation intake.

- It is not a medical diagnostic system.
- It does not independently recommend treatment.
- Transcriptions and translations may contain errors and must be checked by a human.
- Blank fields mean information was not recorded; they do not mean the patient has no symptoms or medical history.
- Use fictional or synthetic information for demonstrations.
- Do not submit identifiable patient information or confidential medical records to this prototype.
- API access, supported audio formats, file-size limits, and service availability depend on the Sarvam AI API and its current terms.

The application is not intended for independent clinical use without appropriate validation, privacy safeguards, security controls, and clinical oversight.

## 🚀 Future Scope

Potential future enhancements include:

- Automatic extraction of patient-reported details into structured fields.
- A clinician dashboard for reviewing intake records.
- Additional Indian languages and improved language detection.
- More robust validation of transcription and translation.
- Secure storage and access controls for approved clinical deployments.
- Integration with hospital workflows and electronic health records, subject to appropriate validation and authorization.

## 🎯 Hackathon Objective

MediKiosk BhashaCare demonstrates how speech technology and translation can help make healthcare intake more accessible to people who prefer communicating in Indian languages.

By combining multilingual input, English translation, and structured information presentation, the project aims to reduce communication friction before a clinician consultation.

## 👨‍💻 Project Information

**Project:** MediKiosk BhashaCare  
**Category:** Healthcare Technology / AI for Social Good  
**Primary language:** Python  
**AI platform:** Sarvam AI  
**Interface:** Streamlit

---

*Built as a hackathon prototype to explore more accessible, multilingual healthcare communication.*
