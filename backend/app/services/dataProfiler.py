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
