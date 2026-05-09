import streamlit as st
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
import os

st.set_page_config(page_title="Voice Translator Chatbot")
st.title("🌍 Voice Translator Chatbot")


LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn",
    "Arabic": "ar",
    "Hindi": "hi",
    "Turkish": "tr",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko"
}


recognizer = sr.Recognizer()

def voice_to_text():
    with sr.Microphone() as source:
        st.info("Listening... Speak now 🎤")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
        except:
            st.error("Could not understand audio")
            return ""
def text_to_speech(text, lang_code):
    tts = gTTS(text=text, lang=lang_code)
    file_path = "output.mp3"
    tts.save(file_path)
    return file_path


input_method = st.radio("Choose Input Method:", ["Text", "Voice"])

if input_method == "Text":
    text = st.text_input("Enter your text:")
else:
    if st.button("🎤 Speak"):
        text = voice_to_text()
    else:
        text = ""


target = st.selectbox("Translate to:", list(LANGUAGES.keys()))


if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter or speak text.")
    else:
        try:
            translated = GoogleTranslator(
                source='auto',
                target=LANGUAGES[target]
            ).translate(text)

            st.success(f"**Translated Text:** {translated}")

            
            audio_file = text_to_speech(translated, LANGUAGES[target])
            audio_bytes = open(audio_file, 'rb').read()
            st.audio(audio_bytes, format='audio/mp3')

        except Exception as e:
            st.error(f"Error: {e}")