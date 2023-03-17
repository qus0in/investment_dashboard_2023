import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.figure_factory as ff
from common import get_history, get_etf_name, DF, Component, get_today, emoji_map

def content():
    page = st.session_state.get('page', 'dashboard')
    if page == 'dashboard':
        dashboard()
        return
    st.title(f"{st.session_state['way']} 분석 ({st.session_state['group']}, {get_today()})")
    if page.startswith('momentum'):
        momentum(page.split('_')[-1])
    if page.startswith('correlation'):
        correlation(page.split('_')[-1])

def correlation(group: str):
    con = st.container()
    days = int(st.session_state['days'])
    ts = [k.split('_')[-1] for k in st.session_state.keys() if k.startswith(group)]
    hs = pd.concat([get_history(t).Close for t in ts], axis=1)
    
    hs.columns = [get_etf_name(i) for i in ts.copy()]

    corr_matrix = hs.tail(days).corr()

    fig = ff.create_annotated_heatmap(
            z=corr_matrix.values,
            x=list(corr_matrix.columns),
            y=list(corr_matrix.index),
            colorscale="RdBu",
            showscale=True,
            reversescale=True,
            font_colors=["black", "black"],
            annotation_text=np.round(corr_matrix.values, decimals=2),
            zmax=1.0,
            zmin=-1.0,
            hoverinfo='z'
    )
    fig.update_layout(
        title="히트맵 분석",
        height=480,
        margin={
            'l':0, 'r':0, 't':160, 'b':0,
            'pad': 2
        },
    )
    
    con.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    dissimilarity = 1 - abs(corr_matrix)
    fig = ff.create_dendrogram(
        dissimilarity,
        labels=corr_matrix.columns,
        orientation='left')

    fig.update_layout(
        title="덴드로그램 분석",
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_tickangle=-45,
        height=400,
        margin={
            'l':0, 'r':0, 't':50, 'b':0,
            'pad':1
        },
    )
    
    con.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

def momentum(group: str):
    con = st.container()
    days = int(st.session_state['days'])
    ts = [k.split('_')[-1] for k, v in st.session_state.items() if k.startswith(group) and v]
    hs = pd.concat([get_history(t).Close for t in ts], axis=1)
    hs.columns = ts

    sc = []
    for i in hs.keys():
        v = hs.loc[:, i]
        pv = lambda x: pd.Series(
            [v[vi - pd.DateOffset(months=x):].iloc[0] for vi in v.index],
            index=v.index)
        ppv = lambda x: (v - pv(x)) / pv(x) / x
        r = ppv(1) + ppv(3) + ppv(6) + ppv(12)
        sc.append(r.tail(days))
    scores = pd.concat(sc, axis=1)
    today = scores.copy().iloc[[-1]].T
    today.columns = ['모멘텀 스코어']
    today['종목명'] = [get_etf_name(c) for c in hs.columns]
    today['종목코드'] = hs.columns.copy()
    tickers = pd.read_csv('ticker.csv').astype(str)
    today.sort_values(
        ascending=False,
        by='모멘텀 스코어',
        inplace=True
    )
    today = today.merge(tickers, left_on='종목코드', right_on='code')
    today['진입'] = today['모멘텀 스코어'].apply(
        lambda x: ('👑' if x >= today.iloc[1, 0] else '🔎') if x >= 0 else '✋'
    )
    today = today.drop(['group', 'code'],axis=1).set_index('종목코드')
    today.rename(columns = {'category': '분류'}, inplace=True)
    today['분류'] = today['분류'].apply(lambda x: emoji_map[x])
    today = today.iloc[:,[2,1,4,0]]

    con.table(today)
    scores.columns = [get_etf_name(c) for c in hs.columns]
    fig = go.Figure()
    for ppi in scores:
        fig.add_trace(go.Scatter(
            x=scores.index, y=scores[ppi], 
            mode='lines+markers',
            name=ppi))
    fig.update_layout(
        title=f"1,3,6,12개월 모멘텀 스코어 트렌드 ({days}일)",
        height=270,
        margin={
            'l':0, 'r':0, 't':30, 'b':0,
            'pad':1
        },
    )
    
    con.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def dashboard():
    con = st.container()
    con.title(f'시장 현황 ({get_today()})')
    dashboard = [
        ("🐳 코스피200", "069500"),
        ("🐜 코스닥150", "229200"),
        ("🦖 S&P500", "379800"),
        ("🎰 나스닥100", "379810"),
        ("🏦 국채10년물", '152380'),
        ("💵 달러선물", '261240'),
        ("🧈 금선물", '132030'),
        ("🛢️ 원유선물", '261220'),
        ("🏭 구리선물", '138910'),
    ]
    for i, d in enumerate(dashboard):
        # cols = st.columns(2)
        handle_dashboard(con, *d)

def handle_dashboard(
        parent: Component,
        label: str,
        ticker: str):
    data = get_history(ticker).tail(int(st.session_state['days'])).iloc[:,:4]
    make_candle_chart(parent, label, data)

def make_candle_chart(parent: Component, title: str, data: DF):
    df = data.tail(int(st.session_state['days'])).iloc[:,:4]
    fig = go.Figure(
        data=[
            go.Candlestick(
            x=df.index,
            open=df.iloc[:,0],
            high=df.iloc[:,1],
            low=df.iloc[:,2],
            close=df.iloc[:,3]
            )]
    )
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=180,
        margin={
            'l':0, 'r':0, 't':60, 'b':0,
            'pad':2
        },
    )
    parent.plotly_chart(
        fig,
        use_container_width=True,
        config={'displayModeBar': True})