import streamlit as st
from gpt_translate import translate
import os

def main():
    st.title("Context-Aware Audio Translation w/ Captions")

    # Language selection dictionary
    languages = {
        "🇺🇸 English": "English",
        "🇮🇳 Hindi": "Hindi",
        "🇵🇹 Portuguese": "Portuguese",
        "🇨🇳 Chinese": "Chinese",
        "🇪🇸 Spanish": "Spanish",
        "🇫🇷 French": "French",
        "🇩🇪 German": "German",
        "🇯🇵 Japanese": "Japanese",
        "🇦🇪 Arabic": "Arabic",
        "🇷🇺 Russian": "Russian",
        "🇰🇷 Korean": "Korean",
        "🇮🇩 Indonesian": "Indonesian",
        "🇮🇹 Italian": "Italian",
        "🇳🇱 Dutch": "Dutch",
        "🇹🇷 Turkish": "Turkish",
        "🇵🇱 Polish": "Polish",
        "🇸🇪 Swedish": "Swedish",
        "🇵🇭 Filipino": "Filipino",
        "🇲🇾 Malay": "Malay",
        "🇷🇴 Romanian": "Romanian",
        "🇺🇦 Ukrainian": "Ukrainian",
        "🇬🇷 Greek": "Greek",
        "🇨🇿 Czech": "Czech",
        "🇩🇰 Danish": "Danish",
        "🇫🇮 Finnish": "Finnish",
        "🇧🇬 Bulgarian": "Bulgarian",
        "🇭🇷 Croatian": "Croatian",
        "🇸🇰 Slovak": "Slovak",
        "🇮🇳 Tamil": "Tamil"
    }

    # Dropdown for language selection
    selected_language = st.selectbox("Choose your language:", [""] + list(languages.keys()))
    if selected_language:
        st.write("You selected:", languages[selected_language])

    # Radio button for profanity filter
    # Display 'Yes' first but make 'No' the default selection
    profanity_filter = st.radio("Enable profanity filter?", ["Yes", "No"], index=1)
    if profanity_filter == "Yes":
        st.write("Profanity filter is enabled.")
    else:
        st.write("Profanity filter is disabled.")

    # Video upload section
    uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov", "mkv"])
    if uploaded_video is not None:
        save_dir = 'videos'
        file_path = os.path.join(save_dir, uploaded_video.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_video.getbuffer())
        st.success(f"Saved video as {file_path}")


        input_lang = translate(uploaded_video.name,profanity_filter, selected_language)

        st.video(file_path, format="video/mp4", start_time=0, subtitles={input_lang: f"output1.vtt", selected_language: f"output2.vtt"})
    

if __name__ == "__main__":
    main()
