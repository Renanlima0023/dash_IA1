import pandas as pd
from typing import Dict, List, Any

def createDataProfile(df: pd.DataFrame, filename: str) -> Dict[str, Any]:
    print(f"\n{'='*60}")
    print(f"🔍 GERANDO PROFILE PARA: {filename}")
    print(f"📊 Total de colunas no DataFrame: {len(df.columns)}")
    print(f"📋 Nomes das colunas: {list(df.columns)}")
    
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
        col_dtype = str(df[col].dtype)
        colInfo = {
            "name": str(col),
            "type": "unknown",
            "dtype": col_dtype,
            "nullCount": int(df[col].isnull().sum()),
            "uniqueValues": int(df[col].nunique()),
            "sampleValues": [str(v) for v in df[col].dropna().head(5).tolist()]
        }
        
        is_numeric = pd.api.types.is_numeric_dtype(df[col])
        is_datetime = pd.api.types.is_datetime64_any_dtype(df[col])
        
        if is_numeric:
            colInfo["type"] = "numeric"
            profile["numericColumns"].append(str(col))
            print(f"   🔢 {col} é NUMÉRICO")
        elif is_datetime:
            colInfo["type"] = "date"
            profile["dateColumns"].append(str(col))
            print(f"   📅 {col} é DATA")
        else:
            colInfo["type"] = "categorical"
            profile["categoricalColumns"].append(str(col))
            print(f"   📝 {col} é CATEGÓRICO")
            
        profile["columns"].append(colInfo)
    
    print(f"\n✅ RESUMO DO PROFILE:")
    print(f"   - Total em profile.columns: {len(profile['columns'])}")
    print(f"   - numericColumns: {profile['numericColumns']}")
    print(f"   - categoricalColumns: {profile['categoricalColumns']}")
    print(f"{'='*60}\n")
    
    return profile

def getSampleData(df: pd.DataFrame, limit: int = 100) -> list:
    sample = df.head(limit).to_dict(orient='records')
    for row in sample:
        for key, value in row.items():
            if pd.isna(value):
                row[key] = None
            elif hasattr(value, 'item'):
                row[key] = value.item()
            elif isinstance(value, (pd.Timestamp, pd.DatetimeTZDtype)):
                row[key] = str(value)
    return sample
