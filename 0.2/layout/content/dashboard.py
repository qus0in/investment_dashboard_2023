import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import data.finance as finance

# 종목별 캔들차트 함수 정의
def handle_dashboard(
        ticker: str):
    # 종목의 최근 일수에 해당하는 데이터 불러오기
    data = finance.get_ohlcv(ticker).tail(
        int(st.session_state['days'])).iloc[:, :4]
    # 종목명 불러오기
    label = finance.get_etf_name(ticker)
    # 캔들차트 생성 함수 호출
    make_candle_chart(label, data)

# 캔들차트 생성 함수 정의
def make_candle_chart(
        title: str,
        data: pd.DataFrame):
    # 최근 일수에 해당하는 데이터만 선택
    df = data.tail(int(st.session_state['days']))
    # 캔들차트 생성
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df.index,
                open=df.iloc[:, 0],
                high=df.iloc[:, 1],
                low=df.iloc[:, 2],
                close=df.iloc[:, 3]
            )]
    )
    # 캔들차트 레이아웃 설정
    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=180,
        margin={
            'l': 0, 'r': 0, 't': 60, 'b': 0,
            'pad': 2
        },
    )
    # 캔들차트 출력
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={'displayModeBar': False})
