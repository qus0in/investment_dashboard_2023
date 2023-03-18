import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import data.finance as finance

def long_short():
    tickers = pd.read_csv("./data/long_short.csv", dtype=str).ticker

    days = int(st.session_state['days'])
    hs = pd.concat([finance.get_ohlcv(t).Close for t in tickers], axis=1)
    hs.columns = tickers

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
    today['종목명'] = [finance.get_etf_name(c) for c in hs.columns]
    today['종목코드'] = hs.columns.copy()
    today.sort_values(
        ascending=False,
        by='모멘텀 스코어',
        inplace=True
    )
    today['진입'] = today['모멘텀 스코어'].apply(
        lambda x: ('👑' if x >= today.iloc[1, 0] else '🔎') if x >= 0 else '✋'
    )
    today = today.set_index('종목코드')
    today = today.iloc[:,[1,2,0]]
    st.table(today)
    scores.columns = [finance.get_etf_name(c) for c in hs.columns]
    fig = go.Figure()
    for ppi in scores:
        fig.add_trace(go.Scatter(
            x=scores.index, y=scores[ppi], 
            mode='lines+markers',
            name=ppi))
    fig.update_layout(
        title=f"1+3+6+12개월 모멘텀 스코어 트렌드 ({days}일)",
        height=320,
        margin={
            'l':0, 'r':0, 't':30, 'b':0,
            'pad':1
        },
        yaxis_range=[-0.5,0.5]
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
