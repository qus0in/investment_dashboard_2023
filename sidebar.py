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
    sidebar.select_slider(
        "🗓️ 분석 기간",
        [10, 20, 50, 100, 200],
        value = 50,
        key = "days"
    )
    make_expander(sidebar,
        label='⚔️ ISA',
        group='isa')
    make_expander(sidebar,
        label='🛡️ 연금저축',
        group='psf')

def make_expander(
    parent: Component,
    label: str,
    group: str,
    expanded: bool = False
):
    exp = parent.expander(label, expanded)
    m, c = exp.columns(2)
    make_btn(
        m, label='🏎️ 모멘텀 분석',
        value=f'momentum_{group}')
    make_btn(
        c, label='🌻 상관성 분석',
        value=f'correlation_{group}')
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
            cds = data[data.category == cat].code
            for cd in cds:
                col.checkbox(
                    label=f"{get_etf_name(cd)}",
                    value=True,
                    key=f"{group}_{cd}"
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