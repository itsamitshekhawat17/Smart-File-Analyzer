import streamlit as st 
import requests  #backend se baat krne ke liye use 


st.title("Smart File Analyzer")

uploaded_file = st.file_uploader("Upload your CSV or excel File")

if uploaded_file is not None:
    st.success("File Uploaded")
    st.write("Filename:", uploaded_file.name)

    if st.button(" 🔍 Analyse File"):
        try:
            with st.spinner("Analyzing...."):

                files = {"file":(uploaded_file.name,uploaded_file.getvalue())}
                response = requests.post("https://smart-file-analyzer.onrender.com/upload-file/",files = files )

                if response.status_code ==200:
                    try:
                      result = response.json()
                    #   st.json(result)

                      if "summary" in result:
                        summary = result["summary"]
                        st.success("✅ Analysis Complete")


                        st.subheader("📌 File Summary")
                        st.write("Rows:",summary["rows"])
                        st.write("Columns:",summary["columns"])
                        st.write("Column Names:",summary["columns_list"])
                        st.write("Nulls per Column:",summary["nulls_per_column"])
                        st.write("Data Types",summary["dtypes"])
                    
                      elif "error" in result:
                        st.error(f"❌ Error from backend: {result['error']}")
                    
                      else:
                
                        st.error("Unexpected response from backend.")
                    except Exception as parse_error:
                       st.error(f"❌ Failed to parse JSON: {str(parse_error)}")
                       st.write("Raw Response Text:", response.text)
                    

                else:
                    st.error(f"❌ Failed with status code {response.status_code}")
                    st.text(response.text)


            
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

