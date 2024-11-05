import streamlit as st
import os
import openai
from pathlib import Path

openai.api_key = os.environ["OPENAI_API_KEY"]

st.title("Traffic Accident Audio to Text")
st.write("Record your voice of what accident you saw, along with details such as the date, time, location, individuals involved, and a brief description of what occurred. Be as specific as possible about any notable actions, words, or outcomes to ensure the record is accurate and thorough.")

#st.sidebar.markdown("Report Audio Transcriptions")

audio_value = st.experimental_audio_input(" ")

st.write ("or")

# File upload for user to submit their audio recordings
uploaded_audio_file = st.file_uploader("Upload an audio file that contains your voice recording of an accident you saw:", type=["mp3", "wav", "m4a"])

# Function to transcribe the uploaded audio
def transcribe_audio(audio_file):
    transcription = openai.Audio.transcribe("whisper-1", audio_file)
    return transcription['text']

# Helper functions for summarizing and analyzing the transcription
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

# Generate transcription and analysis only if an audio file is uploaded
if uploaded_audio_file:
    st.audio(uploaded_audio_file, format="audio/mp3")
    st.write("Transcribing and analyzing audio... Please wait.")
    
    # Transcribe audio
    transcription = transcribe_audio(uploaded_audio_file)
    
    # Run analyses on transcription
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription)
    action_items = action_item_extraction(transcription)
    sentiment = sentiment_analysis(transcription)
    
    # Display the analysis results
    option = st.radio(
        "Select your desired output:",
        ["Summary", "Sentiment", "Action Items", "Key Points"]
    )
    
    if option == "Summary":
        st.write("**Summary:**")
        st.write (abstract_summary)
    elif option == "Sentiment":
        st.write("**Sentiment Analysis:**")
        st.write(sentiment)
    elif option == "Action Items":
        st.write("**Action Items:**")
        st.write(action_items)
    elif option == "Key Points":
        st.write("**Key Points:**")
        st.write(key_points)