import streamlit as st
 
def file_uploader():
    return st.file_uploader("Upload audio file (.mp3, .wav, .m4a)", type=["mp3", "wav", "m4a"]) 