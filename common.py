from pandas import DataFrame as DF

import streamlit as st
from streamlit.delta_generator import DeltaGenerator as Component

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz

import FinanceDataReader as fdr

etf_list = fdr.StockListing("ETF/KR")
get_today = datetime.now(tz=pytz.timezone('Asia/Seoul')).date

@st.cache_data
def get_etf_name(code: str):
    return etf_list.query(f'Symbol == "{code}"').iloc[0, 1].split()[1]

@st.cache_data
def get_history(code: str):
    two_year_ago = (get_today() - relativedelta(years=2)).strftime('%Y-%m-%d')
    return fdr.DataReader(code, start=two_year_ago)

emoji_map = {
    "코스피": "🐳",
    "코스닥": "🐜",
    "달러": "💵",
    "원유": "🛢️",
    "기술": "🚀",
    "채권": "🏦",
    "원자재": "📦",
}