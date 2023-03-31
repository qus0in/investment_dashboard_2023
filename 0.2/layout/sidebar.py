import streamlit as st


def sidebar():
    sidebar = st.sidebar
    with sidebar:
        # 분석 기간을 선택하는 슬라이더
        st.select_slider(
            "🗓️ 분석 기간",
            [20, 60, 120, 240],
            value = 20,
            key = "days"
        )
        # 데이터 갱신 버튼
        st.button(
            '🔄 데이터 갱신',
            on_click=st.cache_data.clear,
            use_container_width=True)
        # 이미지 삽입
        st.image(
            './0.2/src/money_tree.png'
        )
        # 버전 정보와 깃허브 링크
        st.write(
            """
            [![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/qus0in/investment_dashboard_2023)
            ![Version](https://img.shields.io/badge/version-0.2.7-brightgreen)
            """
        )
