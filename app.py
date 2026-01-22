import streamlit as st
from PIL import Image
import numpy as np
import easyocr

st.set_page_config(page_title="ScanTeks Scanner", layout="centered")

# ====== INIT SESSION ======
if "ocr_text" not in st.session_state:
    st.session_state.ocr_text = ""

# ====== UI LANGUAGE ======
ui_lang = st.sidebar.selectbox("🌐 Bahasa Aplikasi", ["Indonesia", "English"])

TEXT = {
    "Indonesia": {
        "title": "📄 ScanTeks Scanner",
        "upload": "Upload gambar",
        "ocr_btn": "Mulai OCR",
        "result": "Hasil OCR",
        "success": "OCR selesai",
        "empty": "Silakan upload gambar terlebih dahulu"
    },
    "English": {
        "title": "📄 ScanTeks Scanner",
        "upload": "Upload image",
        "ocr_btn": "Start OCR",
        "result": "OCR Result",
        "success": "OCR completed",
        "empty": "Please upload image first"
    }
}

T = TEXT[ui_lang]

# ====== OCR LANGUAGE ======
ocr_lang_choice = st.sidebar.selectbox("🧠 Bahasa OCR", ["Indonesia", "English", "Multi"])

LANG_MAP = {
    "Indonesia": ["id"],
    "English": ["en"],
    "Multi": ["id", "en"]
}

# ====== TITLE ======
st.title(T["title"])

# ====== IMAGE UPLOAD ======
uploaded_file = st.file_uploader(T["upload"], type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, use_column_width=True)

    if st.button(T["ocr_btn"]):
        with st.spinner("OCR..."):
            reader = easyocr.Reader(LANG_MAP[ocr_lang_choice], gpu=False)
            result = reader.readtext(np.array(image), detail=0)
            st.session_state.ocr_text = "\n".join(result)
        st.success(T["success"])

else:
    st.info(T["empty"])

# ====== RESULT ======
if st.session_state.ocr_text:
    st.subheader(T["result"])
    st.text_area("", st.session_state.ocr_text, height=250)
