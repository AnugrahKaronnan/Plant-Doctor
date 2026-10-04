# 🌱 Plant Doctor — AI Vision Plant Health Assistant

An AI-powered plant health assistant that allows users to upload plant images, ask questions about their plants, receive visual health analysis, and get a personalized plant-health report delivered directly to their email.

Built with **Python, Streamlit, Google Gemini, and Gmail SMTP**.

---

## 🌐 Live Demo

👉 **[Try Plant Doctor](https://plantdoctor-ai.streamlit.app/)**

---

## ✨ Features

### 🌿 AI Plant Vision

Upload a photo of a plant or leaf and Plant Doctor analyzes the image using Gemini.

The assistant can help identify:

* The plant
* Visible symptoms
* Possible causes
* Watering requirements
* Light requirements
* Things the user should check
* Recommended next steps
* Confidence level

The system is designed to distinguish between **what is visibly observed** and **what is only a possible cause**.

---

### 💬 Conversational Chat

Plant Doctor is not limited to a single image analysis.

Users can:

1. Upload a plant image.
2. Ask a question.
3. Receive an AI response.
4. Ask follow-up questions.
5. Continue discussing the same plant.

The Gemini conversation maintains the context of the ongoing interaction.

---

### 📷 Image + Text Input

Users can send:

* Text-only questions
* Plant images
* Plant images with questions

For example:

> "What is wrong with these leaves?"

or:

> "Is this plant getting enough sunlight?"

or simply upload an image without typing a question.

---

### 📧 Email Plant-Health Report

After having a conversation with Plant Doctor, the user can click:

**📧 Send Report To EMAIL**

The application:

1. Uses Gemini to generate a concise plant-health report.
2. Formats the report.
3. Sends it to the email address provided during onboarding.

The email is sent through the application's configured Gmail account.

---

---

## 🛠️ Tech Stack

* **Python** — Application logic
* **Streamlit** — Web application and user interface
* **Google Gemini** — AI text and image analysis
* **Gmail SMTP** — Email delivery
* **Git & GitHub** — Version control and source code hosting
* **Streamlit Community Cloud** — Application deployment

---

## 📁 Project Structure

```text
Plant-Doctor/
│
├── .streamlit/
│   └── secrets.toml.example
│
├── app.py
├── prompts.py
├── requirements.txt
├── README.md
└── .gitignore
```

> `secrets.toml` is used locally or configured through Streamlit Cloud Secrets and is intentionally excluded from GitHub.

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/AnugrahKaronnan/Plant-Doctor.git
cd Plant-Doctor
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Streamlit Secrets

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your-gemini-api-key"

GMAIL_ADDRESS = "your-gmail-address@gmail.com"

GMAIL_APP_PASSWORD = "your-gmail-app-password"
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## 🚀 How to Use

1. Open Plant Doctor.
2. Enter your name and email address.
3. Upload a clear photo of your plant or leaf.
4. Ask a question or let Plant Doctor analyze the image.
5. Review the visible symptoms and possible causes.
6. Ask follow-up questions if needed.
7. Generate and send the plant-health report to your email.

---

## ⚠️ Disclaimer

Plant Doctor provides AI-assisted observations and general plant-care guidance based on the information and images provided by the user.

Image-based analysis cannot guarantee an accurate diagnosis. Possible causes should not be treated as confirmed diseases or professional agricultural diagnoses.

For serious plant health problems or valuable crops, consult a qualified agricultural or plant-health professional.

---

## 🌱 Project Goal

Plant Doctor was created to make basic plant-health guidance more accessible through **AI-powered image analysis and conversational assistance**.

The goal is to help users understand what they can observe, what might be happening, and what practical steps they can take next.

---

## 👨‍💻 Author

**Anugrah Karonnan**

B.Tech Computer Science Engineering
Model Engineering College, Kerala

---

## 📄 License

This project is created for educational and project-development purposes.
