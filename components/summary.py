import streamlit as st

def show_summary(summary, lang="English"):
    st.subheader(f"Summary ({lang})")
    st.write(summary)
    st.download_button(
        label=f"Download Summary ({lang})",
        data=summary,
        file_name=f"summary_{lang}.txt"
    ) 