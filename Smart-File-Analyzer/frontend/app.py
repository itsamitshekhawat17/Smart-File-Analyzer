import streamlit as st  # type: ignore

st.title("Smart File Analyzer")

uplaoded_file = st.file_uploader("Upload your CSV or excel File")

if uplaoded_file:
    st.success("File Uploaded")
    st.write("Filename",uplaoded_file.name)

