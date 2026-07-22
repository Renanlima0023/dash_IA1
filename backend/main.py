from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from app.services.dataProfiler import createDataProfile

app = FastAPI(title="Dashboard AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Dashboard AI Backend está rodando!", "status": "ok"}

@app.post("/api/upload")
async def uploadFile(file: UploadFile = File(...)):
    validExtensions = [".csv", ".xlsx", ".xls"]
    fileName, fileExt = os.path.splitext(file.filename)
    fileExt = fileExt.lower()
    
    if fileExt not in validExtensions:
        raise HTTPException(status_code=400, detail="Formato não suportado. Use .xlsx, .xls ou .csv")
    
    try:
        if fileExt == ".csv":
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        profile = createDataProfile(df, file.filename)
        
        return {
            "success": True,
            "message": "Arquivo processado com sucesso",
            "fileName": file.filename,
            "rowCount": profile["rowCount"],
            "profile": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

@app.get("/api/test")
def testApi():
    return {"status": "ok", "message": "Backend conectado e funcionando"}
