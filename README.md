

# Smart File Analyzer

📊 A web-based application designed to analyze CSV and XLSX files, providing detailed summaries and insights.

## 🧠 Project Overview

The Smart File Analyzer is a web-based tool that allows users to upload CSV or XLSX files and receive a comprehensive analysis. The application is built using FastAPI for the backend and Streamlit for the frontend, ensuring efficient processing and a user-friendly interface.

### 🚀 Key Features

- **File Upload:** Supports CSV and XLSX files.
- **Data Summary:** Generates detailed summaries including filename, rows, columns, null counts, and data types.
- **Error Handling:** Provides clear error messages for invalid file types or formats.
- **Modular Structure:** Separates frontend and backend for scalability and maintainability.

## 🛠️ Tech Stack

- **Frontend:** Streamlit, Requests, Pandas
- **Backend:** FastAPI, Uvicorn, Pandas
- **Dependencies Management:** Poetry

## 📦 Installation

### Prerequisites

- Python 3.8+
- Poetry (for dependency management)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Smart-File-Analyzer.git
   cd Smart-File-Analyzer
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Start the backend server:
   ```bash
   uvicorn Backend.main:app --reload
   ```

4. Run the frontend:
   ```bash
   streamlit run frontend/app.py
   ```

## 💻 Usage

1. Access the frontend via the Streamlit UI.
2. Upload a CSV or XLSX file.
3. Click "Analyze" to process the file.
4. View the generated summary and insights.

## 📂 Project Structure

```markdown
Smart-File-Analyzer/
├── Backend/
│   ├── main.py
│   ├── routers/
│   │   └── upload.py
│   ├── services/
│   │   └── analyzer.py
│   └── requirements.txt
└── frontend/
    ├── app.py
    └── requirements.txt
```

## 📸 Screenshots

<img width="1919" height="874" alt="image" src="https://github.com/user-attachments/assets/d684418c-5726-4900-a243-19fc503c4af5" />
<img width="1919" height="860" alt="image" src="https://github.com/user-attachments/assets/bc99cb88-fb4e-43be-b643-c1eb65a839d3" />



## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, please open an issue first to discuss the details.



## 📬 Contact

For questions or suggestions, please contact [Amit Singh](itsmeamitsingh17@gmail.com).

## 💖 Thanks Message

Thank you for using the Smart File Analyzer! This tool was created to simplify data analysis and provide quick insights into your datasets.
