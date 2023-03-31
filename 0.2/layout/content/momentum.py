import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import data.finance as finance

# momentum 함수 정의
def momentum(path: str):
    # csv 파일에서 ticker 컬럼을 가져옴
    tickers = pd.read_csv(path, dtype=str).ticker

    # 사용자가 입력한 일수를 가져옴
    days = int(st.session_state['days'])

    # 모든 ETF의 종가 데이터를 가져와서 hs에 저장
    hs = pd.concat([finance.get_ohlcv(t).Close for t in tickers], axis=1)
    hs.columns = tickers
    col1, col2 = st.columns(2)
    with col1:
        momentum_graph("최근 가중", days, hs, lambda x, v: v.rolling(
                20 * x).apply(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]) / x)
    with col2:
        momentum_graph("동일 가중", days, hs, lambda x, v: v.rolling(
                20 * x).apply(lambda x: (x.iloc[-1] - x.iloc[0]) / x.iloc[0]) / 4)

def momentum_graph(label, days, df, ppv):
    st.subheader(f"{label} 모멘텀")
    # 모멘텀 스코어 계산
    sc = []
    for i in df.keys():
        v = df.loc[:, i]
        # 1, 3, 6, 12개월 모멘텀 스코어 계산
        r = ppv(1, v) + ppv(3, v) + ppv(6, v) + ppv(12, v)
        # 계산된 모멘텀 스코어를 sc 리스트에 추가
        sc.append(r.tail(days))
    # 모든 ETF의 모멘텀 스코어를 scores에 저장
    scores = pd.concat(sc, axis=1)

    # 오늘의 모멘텀 스코어를 today에 저장
    today = scores.copy().iloc[[-1]].T
    today.columns = ['모멘텀 스코어']
    today['종목명'] = [finance.get_etf_name(c) for c in df.columns]
    today['종목코드'] = df.columns.copy()
    # 모멘텀 스코어를 기준으로 내림차순 정렬
    today.sort_values(
        ascending=False,
        by='모멘텀 스코어',
        inplace=True
    )
    # 모멘텀 스코어가 높은 ETF에는 👑, 그 외에는 🔎, 모멘텀 스코어가 음수인 경우에는 ✋ 표시
    today['진입'] = today[f'모멘텀 스코어'].apply(
        lambda x: ('👑' if x >= today.iloc[1, 0] else '🔎') if x >= 0 else '✋'
    )
    # 종목코드를 인덱스로 설정하고 필요한 컬럼만 추출하여 today에 저장
    today = today.set_index('종목코드')
    today = today.iloc[:, [1, 2, 0]]
    # streamlit의 table을 이용하여 today를 출력
    st.table(today)

    # 모멘텀 스코어 트렌드를 그래프로 출력
    scores.columns = [finance.get_etf_name(c) for c in df.columns]
    fig = go.Figure()
    for ppi in scores:
        fig.add_trace(go.Scatter(
            x=scores.index, y=scores[ppi],
            mode='lines+markers',
            name=ppi))
    fig.update_layout(
        title=f"1+3+6+12개월 {label} 모멘텀 스코어 트렌드 ({days}일)",
        height=320,
        margin={
            'l': 0, 'r': 0, 't': 30, 'b': 0,
            'pad': 1
        },
        # yaxis_range=[-0.5,0.5],
        # colorway=pd.read_csv("./data/colors.csv", dtype=str).hex,
    )
    # streamlit의 plotly_chart를 이용하여 그래프를 출력
    st.plotly_chart(fig, use_container_width=True,
                    config={'displayModeBar': False})