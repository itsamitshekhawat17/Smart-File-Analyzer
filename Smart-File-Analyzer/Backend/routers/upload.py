from fastapi import APIRouter, File, UploadFile 
import pandas as pd  
router = APIRouter()

@router.post("/upload-file")
async def upload_file(file : UploadFile = File(...)):
    try:
        print(f"File received:{file.filename}")
        contents = await file.read()
        print("file read successfully")

        if file.filename.endswith("csv"):
             df = pd.read_csv(pd.io.common.BytesIO(contents))
        elif file.filename.endswith("xlsx"):
            df = pd.read_excel(pd.io.common.BytesIO(contents))
        else :
            return {"Error!!! only csv and xlsx files are allowed"}    
        

        summary = {

            "filename" :file.filename,
            "rows" :df.shape[0],
            "columns":df.shape[1],
            "columns_list":df.columns.tolist(),
            "nulls_per_column":df.isnull().sum().to_dict(),
            "dtypes":df.dtypes.astype(str).to_dict()

        
        }

        print("✅ Summary created successfully")
        print("Returned summary:",summary)

        return {"summary":summary}
    except Exception as e :
        print("Backedn error:",str(e))
        return{"Error":str(e)}