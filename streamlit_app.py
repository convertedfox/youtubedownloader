import streamlit as st
from pytube import YouTube
import os

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = int(percentage_of_completion)
    return per

def startDownload(ytLink, download_type):
    try:
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        if download_type == "Video":
            stream = ytObject.streams.get_highest_resolution()
        else:
            stream = ytObject.streams.filter(only_audio=True).first()

        # Zeige den Titel des Videos an
        st.write(f"Titel: {ytObject.title}")

        # Fortschrittsbalken
        progress_bar = st.progress(0)
        status_text = st.empty()

        # Download starten
        file_path = stream.download()

        # Fortschritt aktualisieren
        while True:
            progress = on_progress(stream, None, stream.filesize)
            progress_bar.progress(progress / 100)
            status_text.text(f"{progress}% abgeschlossen")
            if progress == 100:
                break

        # Erfolgsmeldung
        st.success(f"Download abgeschlossen! Die Datei wurde gespeichert als: {os.path.basename(file_path)}")

    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

# Streamlit App
st.set_page_config(page_title="YouTube Downloader für Video und Audio")

st.title("YouTube Downloader für Video und Audio")

# Link Input
ytLink = st.text_input("Hier den Link zum Video einfügen:")

# Auswahloptionen
download_type = st.radio("Downloadtyp auswählen:", ["Video", "Nur Audio"])

# Download Button
if st.button("Download starten"):
    if ytLink:
        startDownload(ytLink, download_type)
    else:
        st.warning("Bitte geben Sie einen YouTube-Link ein.")

# Autor Information
st.markdown("---")
st.text("N. Batke 2024 - V. 1.0 (Streamlit Version)")