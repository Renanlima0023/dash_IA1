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
    Você é um especialista em análise de dados e visualização.
    
    Analise as informações do arquivo abaixo e gere recomendações PRÁTICAS.

    DADOS DO ARQUIVO:
    - Arquivo: {profile['fileName']}
    - Registros: {profile['rowCount']}
    - Colunas: {profile['columnCount']}
    - Colunas numéricas: {', '.join(profile['numericColumns'])}
    - Colunas categóricas: {', '.join(profile['categoricalColumns'])}
    - Colunas de data: {', '.join(profile['dateColumns'])}
    
    FORNEÇA SUAS RECOMENDAÇÕES NO SEGUINTE FORMATO (ARRAYS DE TEXTO SIMPLES):
    
    1. KPIs: Liste 5-7 KPIs/métricas importantes como STRINGS SIMPLES (ex: "Total de Vendas", "Média por Cliente")
    
    2. Gráficos: Liste 3-5 tipos de gráficos como STRINGS SIMPLES e DESCRITIVAS (ex: "Gráfico de barras mostrando Vendas por Mês", "Gráfico de pizza da Distribuição por Categoria")
    
    3. Observações: Forneça insights relevantes como TEXTO CORRIDO
    
    RESPOSTA EM JSON (use arrays de strings simples, NÃO use objetos):
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
