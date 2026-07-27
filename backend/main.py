from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from app.services.dataProfiler import createDataProfile, getSampleData
from app.services.groqService import generateDashboardSuggestions

app = FastAPI(title="Dashboard AI API", version="1.0.0")

# Permitir que o Frontend acesse este Backend
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
    """Recebe o arquivo, processa e retorna o DataProfile completo"""
    validExtensions = [".csv", ".xlsx", ".xls"]
    fileName, fileExt = os.path.splitext(file.filename)
    fileExt = fileExt.lower()
    
    if fileExt not in validExtensions:
        raise HTTPException(status_code=400, detail="Formato não suportado. Use .xlsx, .xls ou .csv")
    
    try:
        # Ler o arquivo
        if fileExt == ".csv":
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)
        
        print(f"\n{'='*60}")
        print(f"📁 ARQUIVO RECEBIDO: {file.filename}")
        print(f"📊 Shape do DataFrame: {df.shape}")
        print(f"📋 Colunas: {list(df.columns)}")
        print(f"{'='*60}\n")
        
        # Criar o DataProfile COMPLETO
        profile = createDataProfile(df, file.filename)
        sampleData = getSampleData(df, limit=100)
        columnsList = list(df.columns)
        
        print(f"\n🔍 DEBUG - Profile gerado:")
        print(f"   - fileName: {profile.get('fileName')}")
        print(f"   - rowCount: {profile.get('rowCount')}")
        print(f"   - columnCount: {profile.get('columnCount')}")
        print(f"   - numericColumns: {profile.get('numericColumns')}")
        print(f"   - categoricalColumns: {profile.get('categoricalColumns')}")
        print(f"   - dateColumns: {profile.get('dateColumns')}")
        print(f"   - columns (total): {len(profile.get('columns', []))}")
        print(f"   - sampleData (total): {len(sampleData)}")
        print(f"{'='*60}\n")
        
        return {
            "success": True,
            "message": "Arquivo processado com sucesso",
            "fileName": file.filename,
            "rowCount": profile["rowCount"],
            "columnCount": profile["columnCount"],
            "profile": profile,
            "sampleData": sampleData,
            "columns": columnsList
        }
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

@app.get("/api/test")
def testApi():
    return {"status": "ok", "message": "Backend conectado e funcionando"}

@app.post("/api/ai-analyze")
async def aiAnalyze(profile: dict):
    """
    Recebe o DataProfile e gera sugestões de KPIs e gráficos usando a IA do Groq
    """
    try:
        print(f"\n{'='*60}")
        print(f"🤖 PROFILE RECEBIDO PARA ANÁLISE:")
        print(f"   - fileName: {profile.get('fileName')}")
        print(f"   - rowCount: {profile.get('rowCount')}")
        print(f"   - columnCount: {profile.get('columnCount')}")
        print(f"   - numericColumns: {profile.get('numericColumns')}")
        print(f"   - categoricalColumns: {profile.get('categoricalColumns')}")
        print(f"   - dateColumns: {profile.get('dateColumns')}")
        print(f"   - columns (total): {len(profile.get('columns', []))}")
        print(f"{'='*60}\n")
        
        suggestions = generateDashboardSuggestions(profile)
        
        print(f"✅ SUGESTÕES GERADAS:")
        print(f"   - KPIs: {len(suggestions.get('kpis', []))}")
        print(f"   - Charts: {len(suggestions.get('charts', []))}")
        print(f"   - Observations: {bool(suggestions.get('observations'))}")
        print(f"{'='*60}\n")
        
        return {
            "success": True,
            "suggestions": suggestions
        }
    except Exception as e:
        print(f"❌ Erro na IA: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
