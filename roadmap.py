import time
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
        f"{'visual-based content' if needs_visuals else ''}. Provide a detailed per-chapter study plan."
    )

    # Generate content using the model
    response = model.generate_content(prompt)

    # Extract content from the response
    if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
        content = response.candidates[0].content.parts[0].text
        return content
    else:
        return "Failed to generate roadmap."


def save_roadmap_to_pdf(roadmap):
    """
    Save the generated roadmap to a PDF file.
    """
    file_name = "study_roadmap.pdf"
    c = canvas.Canvas(file_name, pagesize=letter)
    c.setFont("Helvetica", 12)
    
    # Add Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 750, "Personalized Study Roadmap")
    
    # Add Roadmap Content
    c.setFont("Helvetica", 12)
    text = c.beginText(30, 730)
    text.setTextOrigin(30, 730)
    text.textLines(roadmap)
    c.drawText(text)
    
    c.save()
    return file_name


# Streamlit UI
st.title("Personalized Study Roadmap")

# User Inputs
grade = st.selectbox("Select your class/grade:", options=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
subject = st.text_input("Which subject do you find difficult?", placeholder="e.g., Math, Science")
daily_time = st.slider("How much time can you spend studying daily (in minutes)?", min_value=10, max_value=180, step=10)

# Additional Help Options
st.write("Do you need any specific help?")
needs_audio = st.checkbox("Audio-based materials")
needs_visuals = st.checkbox("Visual-based materials")

# Submit button for roadmap generation
if st.button("Generate Roadmap"):
    if subject:
        # Generate the roadmap using the function
        roadmap = generate_roadmap(grade, subject, daily_time, needs_audio, needs_visuals)

        # Display the generated roadmap in a collapsible section
        st.subheader("Your Personalized Study Roadmap")
        st.write(roadmap)

        # Allow the user to download the roadmap as a .pdf file
        file_name = save_roadmap_to_pdf(roadmap)
        with open(file_name, "rb") as f:
            st.download_button(
                label="Download PDF Roadmap",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )
    else:
        st.warning("Please enter a subject before generating the roadmap.")

# Optional Style Customizations
st.markdown(
    """
    <style>
    body {
        background-color: #f4f7fb;
        font-family: "Arial", sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 14px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSlider>div>div>div>input {
        background-color: #e0f7fa;
    }
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
    }
    .stTextArea>div>div>textarea {
        background-color: #f9fbe7;
    }
    .stSubheader {
        color: #00796b;
    }
    </style>
    """,
    unsafe_allow_html=True
)
