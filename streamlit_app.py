try:
    import streamlit as st
    from pytube import YouTube
    import os
    import threading
except ModuleNotFoundError as e:
    print("Error: A required package is not installed. Make sure 'streamlit' and 'pytube' are installed in your environment.")
    raise e

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    st.session_state.progress_bar.progress(percentage_of_completion / 100)
    st.session_state.status_text.text(f"{int(percentage_of_completion)}% abgeschlossen")

def startDownload(ytLink, download_type):
    try:
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        if download_type == "Video":
            stream = ytObject.streams.get_highest_resolution()
        else:
            stream = ytObject.streams.filter(only_audio=True).first()

        # Zeige den Titel des Videos an
        st.write(f"Titel: {ytObject.title}")

        # Fortschrittsbalken initialisieren
        st.session_state.progress_bar = st.progress(0)
        st.session_state.status_text = st.empty()

        # Download starten
        file_path = stream.download()

        # Erfolgsmeldung
        st.success(f"Download abgeschlossen! Die Datei wurde gespeichert als: {os.path.basename(file_path)}")

    except Exception as e:
        st.error(f"Ein Fehler ist aufgetreten: {str(e)}")

def start_threaded_download(ytLink, download_type):
    download_thread = threading.Thread(target=startDownload, args=(ytLink, download_type))
    download_thread.start()

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
        start_threaded_download(ytLink, download_type)
    else:
        st.warning("Bitte geben Sie einen YouTube-Link ein.")

# Autor Information
st.markdown("---")
st.text("cconverted Fox 2025 - V. 1.0 (Streamlit Version)")