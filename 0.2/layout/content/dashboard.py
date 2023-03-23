import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import data.finance as finance

def dashboard():
    tickers = pd.read_csv("./0.2/data/dashboard.csv", dtype=str).ticker
    for i in range(0, len(tickers), 2):
        col1, col2 = st.columns(2)
        with col1:
            handle_dashboard(tickers.iloc[i])
        with col2:
            handle_dashboard(tickers.iloc[i+1])

def handle_dashboard(
    ticker: str):
    data = finance.get_ohlcv(ticker).tail(int(st.session_state['days'])).iloc[:,:4]
    label = finance.get_etf_name(ticker)
    make_candle_chart(label, data)

def make_candle_chart(
    title: str,
    data: pd.DataFrame):
    df = data.tail(int(st.session_state['days']))
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
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={'displayModeBar': False})
