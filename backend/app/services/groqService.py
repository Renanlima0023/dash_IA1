import json
from groq import Groq
import os

def generateDashboardSuggestions(profile: dict) -> dict:
    """
    Usa a API do Groq para gerar sugestões de KPIs e gráficos com base no DataProfile
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Extrai os dados do profile com fallback para diferentes formatos de nome
    numeric_cols = profile.get('numericColumns') or profile.get('numeric_columns') or []
    categorical_cols = profile.get('categoricalColumns') or profile.get('categorical_columns') or []
    date_cols = profile.get('dateColumns') or profile.get('date_columns') or []
    
    file_name = profile.get('fileName') or profile.get('file_name') or 'arquivo'
    row_count = profile.get('rowCount') or profile.get('row_count') or 0
    column_count = profile.get('columnCount') or profile.get('column_count') or 0
    
    # Monta o prompt com base no DataProfile
    prompt = f"""
    Você é um especialista em análise de dados. Com base nas informações do arquivo de dados abaixo, 
    gere sugestões de KPIs e tipos de gráficos apropriados para visualização.

    Dados do arquivo:
    - Nome do arquivo: {file_name}
    - Total de registros: {row_count}
    - Total de colunas: {column_count}
    - Colunas numéricas: {', '.join(numeric_cols) if numeric_cols else 'Nenhuma'}
    - Colunas categóricas: {', '.join(categorical_cols) if categorical_cols else 'Nenhuma'}
    - Colunas de data: {', '.join(date_cols) if date_cols else 'Nenhuma'}
    
    Sugestões:
    1. KPIs recomendados (ex: Soma de vendas, Média de notas)
    2. Tipos de gráficos recomendados (ex: Gráfico de barras, Linha)
    3. Observações importantes sobre os dados

    Responda em JSON com as chaves: 'kpis', 'charts', 'observations'
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        # Parse o JSON da resposta
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        raise Exception(f"Erro ao chamar a API do Groq: {str(e)}")
