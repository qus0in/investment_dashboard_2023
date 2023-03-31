from layout.content import content  # layout 패키지에서 content 모듈을 import
from layout.sidebar import sidebar  # layout 패키지에서 sidebar 모듈을 import
import streamlit as st

def main():  # main 함수 정의
    st.set_page_config(
        page_title="돈 복사기",
        page_icon=":moneybag:",
        layout="wide",
    )
    sidebar()  # sidebar 함수 호출
    content()  # content 함수 호출

if __name__ == "__main__":  # 현재 모듈이 최상위 모듈일 경우
    main()  # main 함수 호출
