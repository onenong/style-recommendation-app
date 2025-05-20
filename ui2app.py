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

# 예시 값 (향후 AI 모델 분석 결과로 대체 가능)
color = "잿색"
material = "울 (Wool)"

# 2단계: 분석 결과
with st.container():
    st.subheader("🧠 2단계: 분석 결과")
    st.write(f"👕 옷종류: {selected_item}")
    st.write(f"🎨 색상: {color}")
    st.write(f"🧵 소재: {material}")
    show_season_options = st.button("상황/계절 추가 선택")

st.markdown("---")

# 3단계: 상황/계절 선택
if show_season_options:
    with st.container():
        st.subheader("🌦️ 3단계: 상황/계절 선택")
        col1, col2 = st.columns(2)
        with col1:
            gender = st.radio("성별 선택", ["남성", "여성"])
        with col2:
            season = st.radio("상황 선택", ["미팅", "출근", "캐주얼"])
        get_recommendation = st.button("추천 스타일 받기")

    st.markdown("---")

    # 4단계: 추천 스타일
    if get_recommendation:
        with st.container():
            st.subheader("🎯 4단계: 추천 스타일")

            # 검색 키워드 생성
            search_query = f"{selected_item} {color} {gender} {season} 스타일 site:pinterest.com"

            def get_pinterest_images(query, max_images=3):
                headers = {"User-Agent": "Mozilla/5.0"}
                res = requests.get(f"https://www.google.com/search?q={query}&tbm=isch", headers=headers)
                soup = BeautifulSoup(res.text, 'html.parser')
                img_tags = soup.find_all("img")
                image_urls = [img["src"] for img in img_tags if "src" in img.attrs]
                return image_urls[1:max_images+1]  # 첫 번째는 로고일 수 있으니 제외

            image_urls = get_pinterest_images(search_query)

            for i, url in enumerate(image_urls):
                st.image(url, caption=f"코디 {i+1}", width=200)

            st.button("Pinterest에서 더 보기", on_click=lambda: st.markdown(f"[Pinterest 검색 링크](https://www.pinterest.com/search/pins/?q={search_query.replace(' ', '%20')})"))

        st.markdown("---")

# 5단계: 결과 저장/공유
with st.container():
    st.subheader("📦 5단계: 결과 저장/공유")
    result_text = f"""추천 스타일:
- 옷종류: {selected_item}
- 색상: {color}
- 소재: {material}
"""
    st.download_button("결과 저장하기", result_text, file_name="style_result.txt")
    st.button("공유하기")

