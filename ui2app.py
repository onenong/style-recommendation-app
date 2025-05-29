import streamlit as st
import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model
import tempfile
import os
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="AI 스타일 추천기", layout="wide")
st.markdown("## 👗 AI 스타일 추천기")

# ✅ 모델 및 라벨 로드
@st.cache_resource
def load_color_model():
    model = load_model("/mnt/data/converted_keras_model/keras_model.h5")
    with open("/mnt/data/converted_keras_model/labels.txt", "r") as f:
        labels = [line.strip().split(" ", 1)[1] for line in f.readlines()]
    return model, labels

model, class_labels = load_color_model()

def predict_color(image: Image.Image):
    img = image.resize((224, 224))
    img_array = np.asarray(img).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    predictions = model.predict(img_array)[0]
    return class_labels[np.argmax(predictions)]

# =====================
# 📸 1단계: 이미지 입력
# =====================
with st.container():
    st.subheader("📸 1단계: 이미지 입력")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    with col2:
        selected_item = st.selectbox("의류 카테고리 선택", ["코트", "자켓", "티셔츠", "팬츠", "기타"])

st.markdown("---")

# =====================
# 🧠 2단계: 분석 결과
# =====================
with st.container():
    st.subheader("🧠 2단계: 분석 결과")

    if uploaded_image:
        img = Image.open(uploaded_image).convert("RGB")
        predicted_color = predict_color(img)

        st.image(img, caption="업로드한 이미지", use_column_width=True)
        st.write(f"👕 옷종류: {selected_item}")
        st.write(f"🎨 예측된 색상: {predicted_color}")
        color = predicted_color
    else:
        color = "알 수 없음"
        st.warning("이미지를 업로드하면 색상을 자동 추출합니다.")

    material = "울 (Wool)"
    st.write(f"🧵 소재: {material}")
    st.button("상황/계절 추가 선택")

st.markdown("---")

# =====================
# 🌦️ 3단계: 상황/계절 선택
# =====================
with st.container():
    st.subheader("🌦️ 3단계: 상황/계절 선택")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("성별 선택", ["남성", "여성"])
    with col2:
        season = st.radio("상황 선택", ["미팅", "출근", "캐주얼"])

    get_recommendation = st.button("추천 스타일 받기")

st.markdown("---")

# =====================
# 🎯 4단계: 추천 스타일
# =====================
if get_recommendation and uploaded_image:
    with st.container():
        st.subheader("🎯 4단계: 추천 스타일")

        search_query = f"{selected_item} {color} {gender} {season} 스타일 site:pinterest.com"

        def get_pinterest_images(query, max_images=3):
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(f"https://www.google.com/search?q={query}&tbm=isch", headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            img_tags = soup.find_all("img")
            image_urls = [img["src"] for img in img_tags if "src" in img.attrs]
            return image_urls[1:max_images+1]

        image_urls = get_pinterest_images(search_query)

        for i, url in enumerate(image_urls):
            st.image(url, caption=f"코디 {i+1}", width=200)

        st.markdown(f"[🔍 Pinterest에서 검색하기](https://www.pinterest.com/search/pins/?q={search_query.replace(' ', '%20')})")

    st.markdown("---")

# =====================
# 📦 5단계: 결과 저장/공유
# =====================
with st.container():
    st.subheader("📦 5단계: 결과 저장/공유")
    result_text = f"""추천 스타일:
- 옷종류: {selected_item}
- 색상: {color}
- 소재: {material}
- 성별: {gender}
- 상황: {season}
"""
    st.download_button("결과 저장하기", result_text, file_name="style_result.txt")
    st.button("공유하기")

