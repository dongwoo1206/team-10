import requests
import streamlit as st
from bs4 import BeautifulSoup


# URL의 HTML 가져오기
def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.text

    except requests.exceptions.RequestException as e:
        st.error(f"페이지 요청 실패: {e}")
        return None


# p.dsc 태그 내용 추출
def extract_titles(html):
    soup = BeautifulSoup(html, "html.parser")

    titles = []

    for tag in soup.find_all("p", class_="dsc"):
        text = tag.get_text(strip=True)

        if text:
            titles.append(text)

    return titles


# 결과 출력
def display_titles(titles):
    if not titles:
        st.warning("추출된 데이터가 없습니다.")
        return

    st.subheader("크롤링 결과")

    for idx, title in enumerate(titles, start=1):
        st.write(f"{idx}. {title}")


# 메인 화면
def main():
    st.title("잡코리아 크롤링")

    # URL 입력
    url = st.text_input("URL 입력")

    # 크롤링 시작 버튼
    if st.button("크롤링 시작"):

        if not url.strip():
            st.error("URL을 입력하세요.")
            return

        html = get_html(url)

        if html:
            titles = extract_titles(html)
            display_titles(titles)


if __name__ == "__main__":
    main()
