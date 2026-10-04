# 🌱 Plant Doctor — AI Vision Plant Health Assistant

An AI-powered plant health assistant that allows users to upload plant images, ask questions about their plants, receive visual health analysis, and get a personalized plant-health report delivered directly to their email.

Built with **Python, Streamlit, Google Gemini, and Gmail SMTP**.

---

## ✨ Features

### 🌿 AI Plant Vision

Upload a photo of a plant or leaf and Plant Doctor analyzes the image using Gemini.

The assistant can help identify:

- The plant
- Visible symptoms
- Possible causes
- Watering requirements
- Light requirements
- Things the user should check
- Recommended next steps
- Confidence level

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

- Text-only questions
- Plant images
- Plant images with questions

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

### 🔐 Secure API Configuration

API keys and Gmail credentials are stored using Streamlit secrets rather than being hard-coded into the application.

Required secrets:

```toml
GEMINI_API_KEY = "your-gemini-api-key"

GMAIL_ADDRESS = "your-gmail-address@gmail.com"

GMAIL_APP_PASSWORD = "your-gmail-app-password"