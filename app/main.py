# app/main.py

import os
import uuid
import streamlit as st
from detection import run_yolo_tracking

# Buat folder uploads jika belum ada
current_path = os.path.abspath(__file__)       # path file ini
UPLOAD_DIR = os.path.dirname(current_path)     # 1 level ke atas
APP_DIR = grandparent_dir = os.path.dirname(UPLOAD_DIR)  # 2 level ke atas

st.title("Deteksi dan Pelacakan Objek dengan YOLO")
model_path = APP_DIR + "/models/yolo11m.pt"

# Upload file
uploaded_file = st.file_uploader("Pilih video", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.write(f"Nama file: {uploaded_file.name}")
    st.write(f"Ukuran file: {round(len(uploaded_file.getbuffer()) / (1024*1024), 2)} MB")

    def save_video(file_data):
        unique_name = f"{uuid.uuid4().hex}.mp4"
        save_path = os.path.join(UPLOAD_DIR, unique_name)
        with open(save_path, "wb") as f:
            f.write(file_data.read())   
        return save_path, unique_name

    def cleanup_previous_video():
        if "saved_path" in st.session_state and os.path.exists(st.session_state["saved_path"]):
            try:
                os.remove(st.session_state["saved_path"])
                print(f"Previous video deleted: {st.session_state['saved_path']}")
            except Exception as e:
                print(f"Error deleting previous video: {e}")

    if st.button("Simpan File"):
        # Clean up previous video if exists
        cleanup_previous_video()
        
        save_path, unique_name = save_video(uploaded_file)

        st.success(f"File berhasil disimpan sebagai: {unique_name}")
        st.write(f"Lokasi file: `{save_path}`")

        # Update session state with new video info
        st.session_state["saved_path"] = save_path
        st.session_state["saved_name"] = unique_name
        st.session_state["is_detection"] = False

        # Show warning about one video limit
        st.info("Catatan: Hanya satu video yang dapat disimpan pada satu waktu. Video sebelumnya akan dihapus otomatis.")

    # Tombol jalankan deteksi muncul setelah file disimpan
    if "saved_path" in st.session_state and st.button("Jalankan Deteksi") and not st.session_state.get("is_detection", False):
        save_path = st.session_state["saved_path"]
        st.write("Menjalankan deteksi pada video...")

        # Jalankan YOLO tracking
        result_path = run_yolo_tracking(video_source=save_path, model_path=model_path)

        #Tampilkan video hasil jika ada (opsional)
        if os.path.exists(result_path):
            with open(result_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.video(video_bytes)

        st.session_state["is_detection"] = False
        st.session_state["result_path"] = result_path

    else:
        st.warning("Hanya bisa menjalankan satu kali deteksi pada video yang sama.")

    if st.button("Hapus Video"):
        if "saved_path" in st.session_state and os.path.exists(st.session_state["saved_path"]):
            os.remove(st.session_state["saved_path"])
            st.success("Video berhasil dihapus.")
            st.session_state.pop("saved_path", None)
            st.session_state.pop("saved_name", None)
            st.session_state["is_detection"] = False
        if "result_path" in st.session_state and os.path.exists(st.session_state["result_path"]):
            os.remove(st.session_state["result_path"])
            st.success("Video hasil deteksi berhasil dihapus.")
            st.session_state.pop("result_path", None)
        else:
            st.warning("Tidak ada video yang disimpan untuk dihapus.")

