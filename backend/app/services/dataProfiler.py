import pandas as pd
from typing import Dict, List, Any

def createDataProfile(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
    """Cria um DataProfile completo dos dados para enviar à IA"""
    profile = {
        "fileName": filename,
        "rowCount": int(len(df)),
        "columnCount": int(len(df.columns)),
        "columns": [],
        "numericColumns": [],
        "categoricalColumns": [],
        "dateColumns": []
    }
    
    for col in df.columns:
        colInfo = {
            "name": str(col),
            "type": "unknown",
            "dtype": str(df[col].dtype),
            "nullCount": int(df[col].isnull().sum()),
            "uniqueValues": int(df[col].nunique()),
            "sampleValues": [str(v) for v in df[col].dropna().head(5).tolist()]
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            colInfo["type"] = "numeric"
            profile["numericColumns"].append(str(col))
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            colInfo["type"] = "date"
            profile["dateColumns"].append(str(col))
        else:
            colInfo["type"] = "categorical"
            profile["categoricalColumns"].append(str(col))
            
        profile["columns"].append(colInfo)
    
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
