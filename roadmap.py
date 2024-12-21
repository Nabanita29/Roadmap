import time
from dotenv import load_dotenv
from gtts import gTTS
import streamlit as st
import os
import google.generativeai as genai
import tempfile
import pygame
from threading import Thread

# Load Environment Variables
load_dotenv()

# Configure the Gemini Pro Model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')


def generate_roadmap(grade, subject, daily_time, needs_audio, needs_visuals):
    """
    Generate a personalized study roadmap based on user input.
    """
    prompt = (
        f"Create a study roadmap for a student in grade {grade} who finds {subject} difficult. "
        f"They can dedicate {daily_time} minutes daily. The roadmap should consider their needs: "
        f"{'audio-based materials' if needs_audio else ''} "
        f"{'visual-based content' if needs_visuals else ''}. Provide detailed per-chapter study plans."
    )

    # Generate content using the model
    response = model.generate_content(prompt)

    # Extract content from the response
    if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
        content = response.candidates[0].content.parts[0].text
        return content
    else:
        return "Failed to generate roadmap."


def save_audio(content, filename):
    """Convert the generated roadmap text to speech and save as an audio file."""
    tts = gTTS(text=content, lang='en')
    tts.save(filename)

# Streamlit UI
st.title("Personalized Study Roadmap")

# User Inputs
grade = st.selectbox("Select your class/grade:", options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
subject = st.text_input("Which subject do you find difficult?", placeholder="e.g., Math, Science")
daily_time = st.slider("How much time can you spend studying daily (in minutes)?", min_value=10, max_value=180, step=10)
needs_audio = st.checkbox("Do you prefer audio-based materials?")
needs_visuals = st.checkbox("Do you prefer visual-based materials?")

# Generate roadmap when button is clicked
if st.button("Generate Roadmap"):
    if not subject:
        st.error("Please enter a subject.")
    else:
        # Generate the roadmap using the function
        roadmap = generate_roadmap(grade, subject, daily_time, needs_audio, needs_visuals)
        
        # Display the generated roadmap
        st.subheader("Your Personalized Study Roadmap")
        st.write(roadmap)

        # Offer audio version of the roadmap
        if needs_audio:
            audio_filename = "roadmap_audio.mp3"
            save_audio(roadmap, audio_filename)
            with open(audio_filename, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

# Optional Style Customizations
st.markdown(
    """
    <style>
    .stButton>button { background-color: #4CAF50; color: white; }
    </style>
    """,
    unsafe_allow_html=True
)
