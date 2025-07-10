from fastapi import APIRouter, File, UploadFile 
import pandas as pd  
router = APIRouter

@router.post("/upload-file")
async def upload_file(file : UploadFile = File(...)):
    try:
        contents = await file.read()

        if file.filename.endswith("csv"):
             df = pd.read_csv(pd.io.common.BytesIO(contents))
        elif file.filename.endswith("xlsx"):
            df = pd.read_excel(pd.io.common.BytesIO(contents))
        else :
            return {"Error!!! only csv and xlsx files are allowed"}    
        

        summary = {

            "Filename" :file.filename,
            "Rows" :df.shape[0],
            "Column":df.shape[1],
            "Column_list":df.columns.tolist(),
            "Nulls_per_column":df.isnull().sum().to_dict(),
            "dtypes":df.dtypes.astype(str).to_dict()

        
        }

        return {"Summary":summary}
    except Exception as e :
        return{"Error":str(e)}