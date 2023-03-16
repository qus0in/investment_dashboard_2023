import streamlit as st
import pandas as pd
from common import Component, DF, get_etf_name, emoji_map

def sidebar():
    sidebar = st.sidebar
    col1, col2 = sidebar.columns(2)
    with col1:
        make_btn(
            col1, label='🪧 처음으로',
            value=f'dashboard')
    with col2:
        st.button('🔄 데이터 최신화', on_click=st.cache_data.clear)
    sidebar.image(
        "./static/invest.png", 
        use_column_width=True)
    sidebar.select_slider(
        "🗓️ 분석 기간",
        [10, 20, 50, 100, 200],
        value = 50,
        key = "days"
    )
    col1, col2 = sidebar.columns(2)
    with col1:
        st.radio(
            '분석 그룹',
            ['ISA', '연금저축'],
            key="group")
    with col2:
        st.radio(
            '분석 방식',
            ['모멘텀', '상관성'],
            key="way")
    sidebar.button(
        '분석',
        use_container_width=True,
        on_click=handle_analysis)
    make_expander(sidebar,
        label='⚔️ ISA',
        group='isa')
    make_expander(sidebar,
        label='🛡️ 연금저축',
        group='psf')

def handle_analysis():
    g = st.session_state['group']
    w = st.session_state['way']
    d = {
        "모멘텀": "momentum",
        "상관성": "correlation",
        "ISA": "isa",
        "연금저축": "psf",
    }
    handle_page(f"{d[w]}_{d[g]}")

def make_expander(
    parent: Component,
    label: str,
    group: str,
    expanded: bool = False
):
    exp = parent.expander(label, expanded)
    make_checkboxs(exp, group)

def make_checkboxs(
    parent: Component,
    group: str,
):
    tickers = pd.read_csv('ticker.csv')
    data = tickers.query(f'group == "{group.lower()}"')
    cats = data.category.unique()
    for i in range(0, len(cats), 2):
        cols = parent.columns(2)
        for j, col in enumerate(cols):
            if i+j == len(cats): break
            cat = cats[i+j]
            col.write(f"{emoji_map[cat]} **{cat}**")
            rows = data[data.category == cat]
            for row in rows.values:
                col.checkbox(
                    label=f"{get_etf_name(row[2])}",
                    value=row[3],
                    key=f"{group}_{row[2]}"
                )

def make_btn(
    parent: Component,
    label: str,
    value: str
):
    parent.button(
        label=label,
        key=value,
        on_click=lambda: handle_page(value)
    )

def handle_page(page: str):
    st.session_state['page'] = page