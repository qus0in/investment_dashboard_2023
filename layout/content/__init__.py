import streamlit as st
from .dashboard import dashboard
from .momentum import momentum

def content():
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Dashboard", "Long & Short", "Long Only", "Korea Only"]
    )
    with tab1:
        dashboard()
    with tab2:
        momentum("./data/long_short.csv")
    with tab3:
        momentum("./data/long_only.csv")
    with tab4:
        momentum("./data/kor_only.csv")
