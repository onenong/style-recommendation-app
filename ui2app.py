import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
from bs4 import BeautifulSoup
import requests
import os

# -------------------------------
# 모델 로딩 (Keras 3에서는 TFSMLayer로 로딩)
# -------------------------------
MODEL_PATH = "converted_keras_model/saved_model"

try:
    model = keras.layers.TFSMLayer(MODEL_PATH, call_endpoint="serving_default")
    with open("converted_keras_model/labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
except Exception as e:
    st.error(f"❌ 모델 로딩 실패: {e}")
    st.stop()

# -------------------------------
# UI 시작
# -------------------------------
st.set_page_config(page_title="AI 스타일 추천기", layout="wide")
st.markdown("## 👗 AI 스타일 추천기")

# 1단계: 이미지 업로드
with st.container():
    st.subheader("📸 1단계: 이미지 입력")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    with col2:
        selected_item = st.selectbox("의류 카테고리 선택", ["코트", "자켓", "티셔츠", "팬츠", "기타"])

# 초기값
predicted_color = "분석 중..."
material = "예: 울, 면 등 (기능 추가 예정)"

# 2단계: 색상 분석
if uploaded_image is not None:
    st.image(uploaded_image, caption="업로드한 이미지", use_column_width=True)

    # 이미지 전처리
    image = Image.open(uploaded_image).convert("RGB")
    image = image.resize((224, 224))
    image_array = np.asarray(image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=0)

    # 예측 수행
    try:
        output = model(image_array)  # TFSMLayer는 dict 반환 가능
        if isinstance(output, dict):
            # 자동 키 추출
            prediction_tensor = list(output.values())[0]
        else:
            prediction_tensor = output

        prediction = prediction_tensor.numpy()
        predicted_index = np.argmax(prediction)
        predicted_color = labels[predicted_index].replace(" ", "").replace("_", "")

    except Exception as e:
        st.error(f"❌ 예측 실패: {e}")
        st.stop()

# 분석 결과 출력
st.markdown("---")
with st.container():
    st.subheader("🧠 2단계: 분석 결과")
    st.write(f"👕 옷종류: {selected_item}")
    st.write(f"🎨 색상: {predicted_color}")
    st.write(f"🧵 소재: {material}")
    st.info("※ 색상은 Teachable Machine 모델로 분류된 결과입니다.")

# 3단계: 성별/상황 선택
st.markdown("---")
with st.container():
    st.subheader("🌦️ 3단계: 상황/계절 선택")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("성별 선택", ["남성", "여성"])
    with col2:
        season = st.radio("상황 선택", ["미팅", "출근", "캐주얼"])
    get_recommendation = st.button("추천 스타일 받기")

# 4단계: 스타일 추천 결과
if get_recommendation and uploaded_image is not None:
    st.subheader("🎯 4단계: 추천 스타일")

    search_query = f"{predicted_color} {selected_item} {gender} {season} 스타일 site:pinterest.com"

    def get_pinterest_images(query, max_images=3):
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(f"https://www.google.com/search?q={query}&tbm=isch", headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        img_tags = soup.find_all("img")
        image_urls = [img["src"] for img in img_tags if "src" in img.attrs]
        return image_urls[1:max_images+1]  # 첫 번째 이미지는 Google 로고일 수 있음

    image_urls = get_pinterest_images(search_query)
    for i, url in enumerate(image_urls):
        st.image(url, caption=f"추천 코디 {i+1}", width=200)

    st.markdown(f"[🔍 Pinterest에서 검색하기](https://www.pinterest.com/search/pins/?q={search_query.replace(' ', '%20')})")

# 5단계: 결과 저장
st.markdown("---")
with st.container():
    st.subheader("📦 5단계: 결과 저장/공유")
    result_text = f"""추천 스타일:
- 옷종류: {selected_item}
- 색상: {predicted_color}
- 소재: {material}
- 성별: {gender}
- 상황: {season}
"""
    st.download_button("결과 저장하기", result_text, file_name="style_result.txt")

