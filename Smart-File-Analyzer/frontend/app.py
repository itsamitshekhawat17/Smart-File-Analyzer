import streamlit as st
import pandas as pd
import numpy as np
import io
import requests
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Smart File Analyzer v2.0",
    page_icon="📊",
    layout="wide"
)

# Constants - Change this URL to your deployed backend URL or local URL
BACKEND_URL = "http://localhost:8000"  # Use "https://smart-file-analyzer.onrender.com" for production

# Helper function to read files
def read_file(uploaded_file):
    try:
        file_type = uploaded_file.name.split('.')[-1].lower()
        
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload a CSV or Excel file."
        
        if len(df) == 0:
            return None, "The file is empty."
            
        return df, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

# Function to send file to backend for analysis
def analyze_with_backend(uploaded_file):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post(f"{BACKEND_URL}/upload-file/", files=files)
        
        if response.status_code == 200:
            try:
                result = response.json()
                return result, None
            except Exception as e:
                return None, f"Failed to parse response: {str(e)}"
        else:
            return None, f"Backend request failed with status code {response.status_code}"
    except Exception as e:
        return None, f"Error connecting to backend: {str(e)}"

# Function to generate KPIs
def generate_kpis(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    missing_values = df.isna().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    kpis = {
        "Total Rows": len(df),
        "Total Columns": len(df.columns),
        "Missing Values": missing_values,
        "Duplicate Rows": duplicate_rows,
        "Numeric Columns": len(numeric_cols),
        "Categorical Columns": len(categorical_cols)
    }
    return kpis

# Main App
st.title("Smart File Analyzer v2.0")

# Sidebar
with st.sidebar:
    st.title("📊 Smart File Analyzer")
    st.markdown("---")
    
    # Theme toggle (simplified)
    theme = st.radio("Choose Theme:", ["light", "dark"], horizontal=True)
    
    # File upload
    st.subheader("📁 Upload Your File")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])

# Main content
if uploaded_file is None:
    st.info("👆 Please upload a file using the sidebar to get started")
else:
    # Process uploaded file
    df, error = read_file(uploaded_file)
    
    if error:
        st.error(error)
    else:
        # Create tabs
        tabs = st.tabs(["📊 Summary", "📄 Data", "🧹 Cleaning"])
        
        # Summary Tab
        with tabs[0]:
            st.header("Dataset Summary")
            
            # Option to use local or backend analysis
            analysis_type = st.radio(
                "Choose Analysis Method",
                ["Local Analysis", "Backend Analysis"],
                horizontal=True
            )
            
            if analysis_type == "Backend Analysis":
                with st.spinner("Analyzing with backend..."):
                    result, error = analyze_with_backend(uploaded_file)
                    
                    if error:
                        st.error(f"❌ {error}")
                        # Fallback to local
                        st.warning("Falling back to local analysis")
                        kpis = generate_kpis(df)
                        
                        # Display KPIs
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Rows", kpis["Total Rows"])
                            st.metric("Missing Values", kpis["Missing Values"])
                        with col2:
                            st.metric("Total Columns", kpis["Total Columns"])
                            st.metric("Duplicate Rows", kpis["Duplicate Rows"])
                        with col3:
                            st.metric("Numeric Columns", kpis["Numeric Columns"])
                            st.metric("Categorical Columns", kpis["Categorical Columns"])
                    else:
                        st.success("✅ Backend Analysis Complete")
                        
                        if "summary" in result:
                            summary = result["summary"]
                            
                            # Display KPIs from backend
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Rows", summary["rows"])
                                null_count = sum(summary["nulls_per_column"].values()) if isinstance(summary["nulls_per_column"], dict) else "N/A"
                                st.metric("Missing Values", null_count)
                            with col2:
                                st.metric("Total Columns", summary["columns"])
                                st.metric("Column Names", ", ".join(summary["columns_list"][:3]) + "..." if len(summary["columns_list"]) > 3 else ", ".join(summary["columns_list"]))
                            with col3:
                                st.metric("Data Types", str(summary["dtypes"]))
                                
                            # Show full backend response
                            with st.expander("View Full Backend Response"):
                                st.json(result)
            else:
                # Local analysis
                kpis = generate_kpis(df)
                
                # Display KPIs
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Rows", kpis["Total Rows"])
                    st.metric("Missing Values", kpis["Missing Values"])
                with col2:
                    st.metric("Total Columns", kpis["Total Columns"])
                    st.metric("Duplicate Rows", kpis["Duplicate Rows"])
                with col3:
                    st.metric("Numeric Columns", kpis["Numeric Columns"])
                    st.metric("Categorical Columns", kpis["Categorical Columns"])
                
                # Show statistics
                with st.expander("Detailed Statistics"):
                    st.dataframe(df.describe())
        
        # Data Tab
        with tabs[1]:
            st.header("Dataset Viewer")
            
            view_option = st.radio("Select View", ["Head", "Tail", "Sample"], horizontal=True)
            
            if view_option == "Head":
                st.dataframe(df.head())
            elif view_option == "Tail":
                st.dataframe(df.tail())
            else:
                st.dataframe(df.sample(min(5, len(df))))
        
        # Cleaning Tab
        with tabs[2]:
            st.header("Data Cleaning")
            
            cleaning_option = st.selectbox(
                "Select cleaning operation",
                ["Remove Duplicates", "Drop Missing Values", "Download Data"]
            )
            
            if cleaning_option == "Remove Duplicates":
                if st.button("Remove Duplicates"):
                    before = len(df)
                    df = df.drop_duplicates()
                    after = len(df)
                    st.success(f"Removed {before - after} duplicate rows")
                    st.dataframe(df.head())
            
            elif cleaning_option == "Drop Missing Values":
                if st.button("Drop Rows with Missing Values"):
                    before = len(df)
                    df = df.dropna()
                    after = len(df)
                    st.success(f"Dropped {before - after} rows with missing values")
                    st.dataframe(df.head())
            
            elif cleaning_option == "Download Data":
                # Create download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    "cleaned_data.csv",
                    "text/csv",
                    key='download-csv'
                )
