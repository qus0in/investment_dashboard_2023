import FinanceDataReader as fdr
import yfinance as yf
import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

# OHLCV 데이터를 가져오는 함수
@st.cache_data
def get_ohlcv(code: str) -> pd.Series:
    # 종목 코드가 6자리 미만인 경우 yfinance로 데이터를 가져옴
    if len(code) < 6:
        return yf.Ticker(code).history(period='2y')
    # 2년 전 날짜를 구해서 FinanceDataReader로 데이터를 가져옴
    two_year_ago = (datetime.now() - relativedelta(years=2)
                    ).strftime('%Y-%m-%d')
    return fdr.DataReader(code, start=two_year_ago)

# ETF 이름을 가져오는 함수
@st.cache_data
def get_etf_name(code: str) -> str:
    # 종목 코드가 6자리 미만인 경우 종목 코드를 그대로 반환
    if len(code) < 6:
        return code
    # ETF 종목인 경우 FinanceDataReader로 ETF/KR 데이터를 가져와서 종목명을 반환
    return fdr.StockListing('ETF/KR').query(f"Symbol == '{code}'").iloc[0, 1].split(' ')[-1]