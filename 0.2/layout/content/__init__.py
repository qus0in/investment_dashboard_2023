import streamlit as st
from .momentum import momentum

def content():
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Long & Short", "Long Only", "US Market", "Bond"]
    )
    with tab1:
        momentum("./0.2/data/long_short.csv")
    with tab2:
        momentum("./0.2/data/long_only.csv")
    with tab3:
        momentum("./0.2/data/us_market.csv")
    with tab4:
        momentum("./0.2/data/bond.csv")