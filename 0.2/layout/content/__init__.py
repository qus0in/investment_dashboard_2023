import streamlit as st
from .momentum import momentum

def content():
    tab1, tab2 = st.tabs(
        ["Long & Short", "Long Only"]
    )
    with tab1:
        momentum("./0.2/data/long_short.csv")
    with tab2:
        momentum("./0.2/data/long_only.csv")