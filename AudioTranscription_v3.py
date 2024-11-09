import streamlit as st
import os
import openai
import tempfile
from pathlib import Path

openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("Traffic Accident Audio to Text")
st.write("Record your voice of what accident you saw, along with details such as the date, time, location, individuals involved, and a brief description of what occurred. Be as specific as possible about any notable actions, words, or outcomes to ensure the record is accurate and thorough.")

# Allows user to record their voice with dedicated audio recorder
audio_value = st.experimental_audio_input(" ")

# Function to transcribe audio
def transcribe_audio(audio_file):
    # Pass the file-like object directly to OpenAI's API
    transcription = openai.Audio.transcribe("whisper-1", audio_file)
    return transcription['text']

# I used chatgpt for this def // Function to handle audio transcription for recorded audio
def handle_recorded_audio(audio_value):
    if audio_value is not None:
        # Create a temporary file to save audio data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio_file:
            tmp_audio_file.write(audio_value.read())  # Write audio data to file as bytes
            tmp_audio_file.seek(0)  # Go back to start of file for reading
            
            # Open the file in binary mode and pass it to the transcription function
            with open(tmp_audio_file.name, "rb") as audio_file:
                transcription_text = transcribe_audio(audio_file)
            return transcription_text
    return None

# Helper functions for summarizing, transcribing, and analyzing the transcription
def abstract_summary_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize this audio file into a text report. Be sure to include all details that are in the recording the driver uploaded."},
            {"role": "user", "content": transcription}
        ]
    )
    return response.choices[0].message['content']

def key_points_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Extract key points from this audio file, including the type of accident, location, time and date of occurrence, individuals involved, and any specific details mentioned. Prioritize identifying key phrases and names, noting emotional cues or urgency, and summarizing the main concern expressed by the speaker. The goal is to provide a concise summary to facilitate quick response and categorization of the report."},
            {"role": "user", "content": transcription}
        ]
    )
    return response.choices[0].message['content']

def action_item_extraction(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyze this user-uploaded audio recording to identify and list any specific action items requested or implied by the speaker. Action items might include immediate responses, such as contacting authorities, sending medical assistance, notifying specific personnel, or implementing a containment procedure. Capture any instructions or recommendations given by the speaker regarding the accident. Additionally, extract contextual information to support the action items, such as the type of accident, location, urgency level, individuals involved, potential hazards, and other relevant details."},
            {"role": "user", "content": transcription}
        ]
    )
    return response.choices[0].message['content']

def sentiment_analysis(transcription):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyze the sentiment of this audio recording as positive, negative, or neutral. Additionally,  use sentiment analysis to gauge the tone of urgency or distress, summarizing all critical points for efficient response and categorization."},
            {"role": "user", "content": transcription}
        ]
    )
    return response.choices[0].message['content']

# If audio recording exists, transcribe it
if audio_value:
    st.write("Transcribing recorded audio... Please wait.")
    transcription = handle_recorded_audio(audio_value)
    if transcription:
        st.subheader("Transcription")
        st.write(transcription)

        abstract_summary = abstract_summary_extraction(transcription)
        key_points = key_points_extraction(transcription)
        action_items = action_item_extraction(transcription)
        sentiment = sentiment_analysis(transcription)
    
        # Display results
        st.title("Summary")
        st.write(abstract_summary)
    
        st.title("Key Points")
        st.write(key_points)

        st.title("Action Items")
        st.write(action_items)

        st.title("Sentiment Analysis")
        st.write(sentiment)

# File upload for additional audio options
uploaded_audio_file = st.file_uploader("Upload an audio file that contains your voice recording of an accident you saw:", type=["mp3", "wav", "m4a"])

# Generate transcription and analysis only if an audio file is uploaded
if uploaded_audio_file:
    st.audio(uploaded_audio_file, format="audio/mp3/m4a")
    st.write("Transcribing and analyzing audio... Please wait.")
    
    # Transcribe audio directly using the file-like object
    transcription = transcribe_audio(uploaded_audio_file)
    
    # Run analyses on transcription
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription)
    action_items = action_item_extraction(transcription)
    sentiment = sentiment_analysis(transcription)
    
    # Display results
    st.title("Summary")
    st.write(abstract_summary)
    
    st.title("Key Points")
    st.write(key_points)

    st.title("Action Items")
    st.write(action_items)

    st.title("Sentiment Analysis")
    st.write(sentiment)