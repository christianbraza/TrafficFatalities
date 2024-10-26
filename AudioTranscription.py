import streamlit as st
import openai

openai.api_key = "OPEN-AI-KEY"

def transcribe_audio(audio_file):
    transcription = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file
    )
    return transcription['text']

def main():
    st.title("Traffic Incident Audio to Text")
    st.write("Record what incident you saw, along with details such as the date, time, location, individuals involved, and a brief description of what occurred. Be as specific as possible about any notable actions, words, or outcomes to ensure the record is accurate and thorough.")

    # File uploader for audio files
    audio_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav", "m4a"])

    if audio_file is not None:
        # Display the uploaded file name
        st.write("Uploaded file:", audio_file.name)

        # Add audio playback feature
        st.audio(audio_file, format=audio_file.type)

        # Transcribe the audio
        with st.spinner("Transcribing..."):
            transcription = transcribe_audio(audio_file)
        
        # Display the transcription result
        st.subheader("Transcription Result")
        st.write(transcription)

main()
