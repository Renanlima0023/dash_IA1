import json
from groq import Groq
import os

def generateDashboardSuggestions(profile: dict) -> dict:
    """
    Usa a API do Groq para gerar sugestões de KPIs e gráficos com base no DataProfile
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Monta o prompt com base no DataProfile
    prompt = f"""
    Você é um especialista em análise de dados. Com base nas informações do arquivo de dados abaixo, 
    gere sugestões de KPIs e tipos de gráficos apropriados para visualização.

    Dados do arquivo:
    - Nome do arquivo: {profile['fileName']}
    - Total de registros: {profile['rowCount']}
    - Total de colunas: {profile['columnCount']}
    - Colunas numéricas: {', '.join(profile['numericColumns'])}
    - Colunas categóricas: {', '.join(profile['categoricalColumns'])}
    - Colunas de data: {', '.join(profile['dateColumns'])}
    
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
