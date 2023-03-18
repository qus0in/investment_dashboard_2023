import streamlit as st
from .dashboard import dashboard
from .long_short import long_short

def content():
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Long & Short", "Long Only"])
    with tab1:
        dashboard()
    with tab2:
        pass
        long_short()
    with tab3:
        pass
        # long_only()
