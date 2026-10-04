import streamlit as st

import smtplib
from email.mime.text import MIMEText

from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, SUMMARY_REQUEST_PROMPT


# ============================================================
# 1. SESSION STATE INITIALIZATION
# ============================================================

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "chat" not in st.session_state:
    st.session_state.chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# 2. API / EMAIL CONFIGURATION
# ============================================================

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]

GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]


# ============================================================
# 3. GEMINI CLIENT
# ============================================================

@st.cache_resource
def get_gemini_client():
    """
    Create and cache the Gemini client.

    @st.cache_resource prevents Streamlit from creating
    a new Gemini client every time the app reruns.
    """

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


client = get_gemini_client()


# ============================================================
# 4. EMAIL
# ============================================================

def send_email(recipient_email, report):
    """
    Send the generated plant-health report by Gmail.
    """

    # Create email message
    message = MIMEText(
        report
    )

    # Email subject
    message["Subject"] = "🌱 Your Plant Doctor Report"

    # Sender
    message["From"] = GMAIL_ADDRESS

    # Recipient
    message["To"] = recipient_email

    # Connect to Gmail SMTP
    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        # Login to Gmail
        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD
        )

        # Send email
        server.send_message(
            message
        )


# ============================================================
# 5. GENERATE EMAIL REPORT
# ============================================================

def generate_report():
    """
    Ask Gemini to create a concise plant-health report
    based on the current conversation.
    """

    response = st.session_state.chat.send_message(
        SUMMARY_REQUEST_PROMPT
    )

    return response.text


# ============================================================
# 6. MESSAGE RENDERING
# ============================================================

def render_message(message):
    """
    Display one message in the Streamlit chat interface.

    A message can currently be:
        - text
        - image
    """

    with st.chat_message(
        message["role"]
    ):

        if message["kind"] == "text":

            st.markdown(
                message["content"]
            )

        elif message["kind"] == "image":

            st.image(
                message["content"]
            )


# ============================================================
# 7. ADD MESSAGE
# ============================================================

def add_message(role, kind, content):
    """
    Save a message to session state and immediately
    display it in the chat interface.
    """

    message = {
        "role": role,
        "kind": kind,
        "content": content
    }

    # Save message
    st.session_state.messages.append(
        message
    )

    # Display message
    render_message(
        message
    )


# ============================================================
# 8. CHECK IF USER HAS ACTUALLY SENT SOMETHING
# ============================================================

def has_user_conversation():
    """
    Return True if the user has sent at least one
    message or image.
    """

    return any(
        message["role"] == "user"
        for message in st.session_state.messages
    )


# ============================================================
# 9. ONBOARDING
# ============================================================

if not st.session_state.onboarded:

    st.title("🌱 Plant Doctor")

    st.write(
        "Your AI-powered plant health assistant."
    )

    st.write(
        "Upload a photo of your plant and ask questions "
        "about its health and care."
    )

    name = st.text_input(
        "Your name"
    )

    email = st.text_input(
        "Your email"
    )

    if st.button("Start 🌱"):

        # Make sure both fields contain something
        if name.strip() and email.strip():

            # Save user information
            st.session_state.name = name.strip()

            st.session_state.email = email.strip()

            # ------------------------------------------------
            # Create Gemini conversation
            # ------------------------------------------------

            st.session_state.chat = client.chats.create(

                model="gemini-3.5-flash-lite",

                config=types.GenerateContentConfig(

                    system_instruction=SYSTEM_PROMPT
                )
            )

            # Mark onboarding as completed
            st.session_state.onboarded = True

            # Reload application
            st.rerun()

        else:

            st.warning(
                "Please enter both your name and email."
            )


# ============================================================
# 10. MAIN APPLICATION
# ============================================================

else:

    st.title("🌱 Plant Doctor")

    st.write(
        f"Welcome, {st.session_state.name}!"
    )


    # ========================================================
    # 11. NEW CONVERSATION
    # ========================================================

    if st.button("🔄 New conversation"):

        # Clear previous messages
        st.session_state.messages = []

        # Create a new Gemini conversation
        st.session_state.chat = client.chats.create(

            model="gemini-3.5-flash-lite",

            config=types.GenerateContentConfig(

                system_instruction=SYSTEM_PROMPT
            )
        )

        # Reload application
        st.rerun()


    # ========================================================
    # 12. CREATE WELCOME MESSAGE
    # ========================================================

    if not st.session_state.messages:

        welcome_message = {
            "role": "assistant",
            "kind": "text",
            "content": f"""
Hi {st.session_state.name}! 🌱

I'm Plant Doctor, your AI plant health assistant.

Upload a photo of your plant or leaf and I'll help you
understand its visible condition, possible causes,
and practical care steps.

You can also ask follow-up questions about the same plant.
"""
        }

        # Only save the welcome message here.
        # It will be rendered by the history loop below.
        st.session_state.messages.append(
            welcome_message
        )


    # ========================================================
    # 13. DISPLAY CHAT HISTORY
    # ========================================================

    for message in st.session_state.messages:

        render_message(
            message
        )



    # ========================================================
    # 15. CHAT INPUT
    # ========================================================

    user_input = st.chat_input(

        "Ask a question, or attach a plant photo...",

        accept_file=True,

        file_type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )


    # ========================================================
    # 16. PROCESS USER INPUT
    # ========================================================

    if user_input:

        # ----------------------------------------------------
        # Get uploaded image
        # ----------------------------------------------------

        photo = (
            user_input.files[0]
            if user_input.files
            else None
        )


        # ----------------------------------------------------
        # Get text
        # ----------------------------------------------------

        text = user_input.text


        # ----------------------------------------------------
        # Create Gemini content parts
        # ----------------------------------------------------

        parts = []


        # ====================================================
        # 17. HANDLE IMAGE
        # ====================================================

        if photo is not None:

            # Convert uploaded image to bytes
            photo_bytes = photo.getvalue()


            # Display/store image in chat history
            add_message(
                "user",
                "image",
                photo_bytes
            )


            # Convert image into a Gemini Part
            image_part = types.Part.from_bytes(

                data=photo_bytes,

                mime_type=photo.type
            )


            # Add image to Gemini request
            parts.append(
                image_part
            )


        # ====================================================
        # 18. HANDLE TEXT
        # ====================================================

        if text:

            # Display/store user question
            add_message(
                "user",
                "text",
                text
            )


            # Add question to Gemini request
            parts.append(
                text
            )


        # ====================================================
        # 19. IMAGE WITHOUT TEXT
        # ====================================================

        elif photo is not None:

            parts.append(
                """
Analyze the attached plant image using the Plant Doctor
guidelines.

Identify the plant if reasonably possible.

Describe only visible symptoms first.

Then provide possible causes, clearly distinguishing
possibilities from confirmed observations.

Provide relevant watering and light guidance, things the
user should check, recommended next steps, and a
qualitative confidence level.

If the image does not provide enough evidence,
clearly say so.
"""
            )


        # ====================================================
        # 20. SEND TO GEMINI
        # ====================================================

        if parts:

            try:

                with st.spinner(
                    "🌱 Examining your plant..."
                ):

                    response = (
                        st.session_state.chat.send_message(
                            parts
                        )
                    )


                # ------------------------------------------------
                # Display Gemini response ONCE
                # ------------------------------------------------

                add_message(
                    "assistant",
                    "text",
                    response.text
                )


            except Exception as e:

                st.error(
                    f"Gemini error: {e}"
                )

                st.exception(e)


    # ========================================================
    # 14. SEND REPORT BUTTON
    # ========================================================

    if has_user_conversation():

        if st.button("📧 Send Report To EMAIL"):

            try:

                # ------------------------------------------------
                # Generate report using Gemini
                # ------------------------------------------------

                with st.spinner(
                    "📄 Preparing your plant report..."
                ):

                    report = generate_report()


                # ------------------------------------------------
                # Send report by Gmail
                # ------------------------------------------------

                with st.spinner(
                    "📧 Sending report to your email..."
                ):

                    send_email(
                        st.session_state.email,
                        report
                    )


                st.success(
                    f"✅ Report sent to {st.session_state.email}"
                )


            except Exception:

                st.error(
                    "Sorry, I couldn't send the report. "
                    "Please try again."
                )

