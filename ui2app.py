import streamlit as st

st.set_page_config(page_title="AI 스타일 추천기", layout="wide")
st.markdown("## 👗 AI 스타일 추천기")

# 1단계: 입력
with st.container():
    st.subheader("📸 1단계: 이미지 입력")
    col1, col2 = st.columns(2)
    with col1:
        uploaded_image = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])
    with col2:
        selected_item = st.selectbox("의류 카테고리 선택", ["코트", "자켓", "티셔츠", "팬츠", "기타"])

st.markdown("---")

# 2단계: 분석 결과
with st.container():
    st.subheader("🧠 2단계: 분석 결과")
    st.write("👕 옷종류: 코트")
    st.write("🎨 색상: 잿색")
    st.write("🧵 소재: 울 (Wool)")
    st.button("상황/계절 추가 선택")

st.markdown("---")

# 3단계: 상황/계절 선택
with st.container():
    st.subheader("🌦️ 3단계: 상황/계절 선택")
    col1, col2 = st.columns(2)
    with col1:
        gender = st.radio("성별 선택", ["남성", "여성"])
    with col2:
        season = st.radio("상황 선택", ["미팅", "출근", "캐주얼"])
    st.button("추천 스타일 받기")

st.markdown("---")

# 4단계: 추천 스타일
with st.container():
    st.subheader("🎯 4단계: 추천 스타일")
    st.markdown("● 어울리는 어두운 색 코디\n● 아이보리 톤 악세서리 추천")
    st.image("https://via.placeholder.com/100", caption="코디1")
    st.image("https://via.placeholder.com/100", caption="코디2")
    st.button("Pinterest에서 더 보기")

st.markdown("---")

# 5단계: 결과 저장/공유
with st.container():
    st.subheader("📦 5단계: 결과 저장/공유")
    st.download_button("결과 저장하기", "추천 스타일 내용", file_name="style_result.txt")
    st.button("공유하기")
