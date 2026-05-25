import requests
import streamlit as st
from bs4 import BeautifulSoup


# 웹페이지 HTML 가져오기
def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return response.text

    except requests.exceptions.MissingSchema:
        st.error("올바른 URL 형식이 아닙니다.")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"페이지 연결 실패: {e}")
        return None


# p.etc 내부의 span.cell 추출
def extract_items(html):
    soup = BeautifulSoup(html, "html.parser")

    items = []

    for p_tag in soup.find_all("p", class_="etc"):
        for span in p_tag.find_all("span", class_="cell"):
            text = span.get_text(strip=True)

            if text:
                items.append(text)

    return items


# 결과 출력
def display_items(items):
    if not items:
        st.warning("추출된 데이터가 없습니다.")
        return

    st.subheader("크롤링 결과")

    for idx, item in enumerate(items, start=1):
        st.write(f"{idx}. {item}")


# 메인 함수
def main():
    st.title("잡코리아 크롤링")

    # URL 입력창
    url = st.text_input("URL 입력")

    # 크롤링 시작 버튼
    if st.button("크롤링 시작"):

        if not url.strip():
            st.error("URL을 입력하세요.")
            return

        html = get_html(url)

        if html:
            items = extract_items(html)
            display_items(items)


# 프로그램 실행
if __name__ == "__main__":
    main()
