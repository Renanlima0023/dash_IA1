import pandas as pd
from typing import Dict, List, Any

def createDataProfile(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
    """Cria um DataProfile completo dos dados para enviar à IA"""
    
    # Debug: mostrar tipos reais das colunas
    print(f"\n🔍 DEBUG - Tipos das colunas no DataFrame:")
    for col in df.columns:
        print(f"   {col}: {df[col].dtype}")
    
    profile = {
        "fileName": filename,
        "rowCount": int(len(df)),
        "columnCount": int(len(df.columns)),
        "columns": [],
        "numericColumns": [],
        "categoricalColumns": [],
        "dateColumns": [],
        "columnTypes": {}  # NOVO: para debug
    }
    
    for col in df.columns:
        col_dtype = str(df[col].dtype)
        colInfo = {
            "name": str(col),
            "type": "unknown",
            "dtype": col_dtype,
            "nullCount": int(df[col].isnull().sum()),
            "uniqueValues": int(df[col].nunique()),
            "sampleValues": [str(v) for v in df[col].dropna().head(5).tolist()]
        }
        
        # Detecção mais robusta de tipos
        is_numeric = pd.api.types.is_numeric_dtype(df[col])
        is_datetime = pd.api.types.is_datetime64_any_dtype(df[col])
        
        # Tenta converter para datetime se for string de data
        if not is_datetime and not is_numeric:
            try:
                converted = pd.to_datetime(df[col], errors='coerce')
                if not converted.isna().all():
                    is_datetime = True
                    print(f"   ⏰ {col} detectado como DATA por conversão")
            except:
                pass
        
        # Se não for numérico nem data, é categórico
        if is_numeric:
            colInfo["type"] = "numeric"
            profile["numericColumns"].append(str(col))
            print(f"    {col} é NUMÉRICO")
        elif is_datetime:
            colInfo["type"] = "date"
            profile["dateColumns"].append(str(col))
            print(f"   📅 {col} é DATA")
        else:
            colInfo["type"] = "categorical"
            profile["categoricalColumns"].append(str(col))
            print(f"   📝 {col} é CATEGÓRICO")
            
        profile["columns"].append(colInfo)
        profile["columnTypes"][str(col)] = colInfo["type"]
    
    print(f"\n✅ Resumo:")
    print(f"   Numéricas: {profile['numericColumns']}")
    print(f"   Categóricas: {profile['categoricalColumns']}")
    print(f"   Datas: {profile['dateColumns']}\n")
    
    return profile

def getSampleData(df: pd.DataFrame, limit: int = 100) -> list:
    """Retorna uma amostra dos dados para usar nos gráficos"""
    sample = df.head(limit).to_dict(orient='records')
    
    # Converte valores não-serializáveis
    for row in sample:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None
            elif hasattr(value, 'item'):
                row[key] = value.item()
            elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                row[key] = str(value)
    
    return sample
