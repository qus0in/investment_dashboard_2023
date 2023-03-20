import FinanceDataReader as fdr
import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

@st.cache_data
def get_ohlcv(code: str) -> pd.Series:
    two_year_ago = (datetime.now() - relativedelta(years=2)).strftime('%Y-%m-%d')
    return fdr.DataReader(code, start=two_year_ago)

@st.cache_data
def get_etf_name(code: str) -> str:
    if len(code) < 6:
        return code
    return fdr.StockListing('ETF/KR').query(f"Symbol == '{code}'").iloc[0, 1].split(' ')[-1]
