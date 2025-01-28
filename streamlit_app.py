try:
    import streamlit as st
    from pytube import YouTube
    import os
    import threading
except ModuleNotFoundError as e:
    print("Error: A required package is not installed. Make sure 'streamlit' and 'pytube' are installed in your environment.")
    raise e

def download_video(ytLink, download_type, progress_callback):
    try:
        ytObject = YouTube(ytLink, on_progress_callback=progress_callback)
        if download_type == "Video":
            stream = ytObject.streams.get_highest_resolution()
        else:
            stream = ytObject.streams.filter(only_audio=True).first()

        # Download starten
        file_path = stream.download()
        return ytObject.title, file_path

    except Exception as e:
        return None, str(e)

def startDownload(ytLink, download_type):
    st.session_state.progress_bar = st.progress(0)
    st.session_state.status_text = st.empty()

    def progress_callback(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        st.session_state.progress_bar.progress(percentage_of_completion / 100)
        st.session_state.status_text.text(f"{int(percentage_of_completion)}% abgeschlossen")

    def threaded_download():
        title, result = download_video(ytLink, download_type, progress_callback)
        if title:
            st.session_state.progress_bar.progress(1.0)
            st.success(f"Download abgeschlossen! Die Datei wurde gespeichert als: {os.path.basename(result)}")
        else:
            st.error(f"Ein Fehler ist aufgetreten: {result}")

    download_thread = threading.Thread(target=threaded_download)
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
        startDownload(ytLink, download_type)
    else:
        st.warning("Bitte geben Sie einen YouTube-Link ein.")

# Autor Information
st.markdown("---")
st.text("cconverted Fox 2025 - V. 1.0 (Streamlit Version)")
