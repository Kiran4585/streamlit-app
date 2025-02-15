import os
import threading
import streamlit as st
import speech_recognition as sr
import pyttsx3
import webbrowser
import google.generativeai as genai

# Load Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set this in environment variables
if not GEMINI_API_KEY:
    st.error("❌ API key missing. Set GEMINI_API_KEY as an environment variable.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# Function to get AI response
def Reply(question):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(question)
    return response.text if response else "No response from Gemini AI."

# Initialize Text-to-Speech
engine = pyttsx3.init()
voices = engine.getProperty("voices")
if voices:
    engine.setProperty("voice", voices[0].id)

def speak(text):
    def run():
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
    thread = threading.Thread(target=run)
    thread.start()

# Function to capture speech
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening...")
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-in")
            st.write(f"🗣 User Said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            st.write("❌ Could not understand audio, please try again.")
        except sr.RequestError:
            st.write("❌ Speech Recognition service is unavailable.")
        return "none"

# Streamlit Web App
st.title("🎙 AI Voice Assistant")

query = st.text_input("Type or Speak a Command:", "")
if st.button("Speak"):
    query = takeCommand()

if query and query != "none":
    st.write("🤖 Processing...")
    response = Reply(query)
    st.write(f"💬 AI Response: {response}")
    speak(response)

    # Handle web commands
    if "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
    elif "open google" in query:
        webbrowser.open("https://www.google.com")
    elif "bye" in query:
        st.write("👋 Goodbye!")
