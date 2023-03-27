from layout.content import content
from layout.sidebar import sidebar
import streamlit as st

def main():
    st.set_page_config(
        page_title="돈 복사기",
        page_icon=":moneybag:"
    )
    sidebar()
    content()

if __name__ == "__main__":
    main()