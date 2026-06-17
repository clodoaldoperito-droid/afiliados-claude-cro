import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Carrega as chaves da raiz do projeto (.env)
# Como sabemos que o env real está em ARQUITETURA_JARVIS, 
# podemos tentar carregar de lá para este teste, ou de variáveis locais.
load_dotenv(r"C:\Users\hytec\.gemini\antigravity\scratch\ARQUITETURA_JARVIS\.env")

# Vamos usar a chave do Groq que estava no arquivo do usuário, mas usando
# a interface da OpenAI (Groq suporta a mesma API).
api_key = os.getenv("GROQ") or os.getenv("OPENROUTER_API_KEY")
base_url = "https://api.groq.com/openai/v1" if os.getenv("GROQ") else "https://openrouter.ai/api/v1"
model = "llama-3.1-8b-instant" if os.getenv("GROQ") else "google/gemma-2-9b-it:free"

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def generate_cro_copy(product_title, current_price):
    print(f"[*] Agente CRO ativado: Escrevendo copy para '{product_title}'...")
    
    prompt = f"""
    Você é um especialista em Marketing de Afiliados e Copywriting (CRO).
    Sua missão é criar um texto altamente persuasivo para vender um produto.
    
    Produto Base: {product_title}
    Preço: R$ {current_price}
    
    Crie o seguinte:
    1. Um título muito mais chamativo e focado em benefícios (máximo 60 caracteres).
    2. Um texto de venda persuasivo (2 parágrafos curtos) usando gatilhos de Escassez e Novidade. Fale como se estivesse recomendando para um amigo.

    Retorne APENAS um JSON válido no seguinte formato exato, sem markdown ao redor:
    {{
        "catchyTitle": "Seu Titulo Aqui",
        "catchyText": "Sua copy aqui."
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um gerador de JSON estrito. Sempre responda apenas com um JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        content = response.choices[0].message.content.strip()
        # Tratamento simples caso o modelo coloque as crases de markdown (```json)
        if content.startswith("```json"):
            content = content[7:-3]
        elif content.startswith("```"):
            content = content[3:-3]
            
        data = json.loads(content)
        return data.get("catchyTitle", product_title), data.get("catchyText", "Aproveite esta oferta incrível!")
        
    except Exception as e:
        print(f"[!] Erro ao gerar copy com a IA: {e}")
        return product_title, "Aproveite esta promoção incrível diretamente da nossa curadoria de ofertas."

if __name__ == "__main__":
    t, c = generate_cro_copy("Smartwatch Relógio Inteligente D20", 35.90)
    print("Título:", t)
    print("Copy:", c)
