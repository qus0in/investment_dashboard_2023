import streamlit as st

def sidebar():
    sidebar = st.sidebar
    with sidebar:
        st.select_slider(
            "🗓️ 분석 기간",
            [10, 20, 50, 100, 200],
            value = 50,
            key = "days"
        )
        st.button(
            '🔄 데이터 갱신',
            on_click=st.cache_data.clear,
            use_container_width=True)
        st.image(
            './src/money_tree.png'
        )
        st.write(
            """
            [![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/qus0in/investment_dashboard_2023)
            ![Version](https://img.shields.io/badge/version-0.2.2-brightgreen)
            """
        )
