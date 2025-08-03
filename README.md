# 🛣️ Lane Passing Counter - YOLO Object Detection with Streamlit

Deteksi dan pelacakan objek (seperti manusia atau kendaraan) secara otomatis saat melewati garis interaktif menggunakan model YOLO. Dibuat untuk seleksi asisten laboratorium sebagai proyek computer vision berbasis Python + Streamlit + OpenCV.

## 🚀 Fitur Utama

- 📥 Upload video dan jalankan deteksi berbasis model YOLOv11
- 🧠 Pelacakan objek secara real-time
- 🎯 Tentukan garis pemantauan (line passing) dan arah kedatangan
- 🎞️ Tampilkan hasil deteksi langsung di Streamlit UI
- 🧹 Hapus file lama secara otomatis untuk menjaga kebersihan sistem
- 📊 Rencana: Visualisasi statistik dan koneksi database

## 🧩 Teknologi

- [YOLOv11 (Ultralytics)](https://github.com/ultralytics/ultralytics)
- Streamlit untuk antarmuka web interaktif
- OpenCV untuk pemrosesan video
- Python 3.11+
- MoviePy dan FFmpeg untuk codec H.264 (kompatibel HTML5)

## 📸 Demo Antarmuka

| Upload Video | Tentukan Garis | Deteksi & Tampilkan |
|--------------|----------------|----------------------|
| ✅           | ✍️ Klik 2 Titik | 🔍 YOLO Tracking     |

*(tambahkan screenshot jika ada)*

## 📁 Struktur Proyek

lane-passing-counter/
├── app/
│ ├── main.py # UI utama dengan Streamlit
│ └── detection.py # Fungsi YOLO tracking
├── models/
│ └── yolo11m.pt # Model YOLO terlatih
├── videos/ # Tempat file video hasil deteksi
└── requirements.txt


---

## ⚙️ Cara Menjalankan

### 1. Clone Proyek

git clone https://github.com/raintxhanx/lane-passing-counter.git
cd lane-passing-counter 

### 2. Clone Proyek

python -m venv MyEnv
MyEnv\Scripts\activate     # Windows

atau

source MyEnv/bin/activate  # Linux/macOS

### 3. Install Dependensi

pip install -r requirements.txt

### 4. Jalankan Aplikasi
streamlit run app/main.py

buka http://localhost:8501