from fastapi import FastAPI 
from routers import upload

app = FastAPI()

app.include_router(upload.router)

@app.get("/")
def read_root():
    return {"message":"Backend of Smart-File-Analyaer is running "}
    

