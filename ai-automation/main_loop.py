import os
import json
import time
from hunter_mercado_livre import search_ml_offers
from agent_cro_writer import generate_cro_copy

AFFILIATE_ID_MOCK = "cefadhcgb19673"

def inject_affiliate_id(url, platform="ML"):
    if platform == "ML":
        # Simples concatenação, na vida real a URL deve ser formatada conforme a API da plataforma
        connector = "&" if "?" in url else "?"
        return f"{url}{connector}affiliate_id={AFFILIATE_ID_MOCK}"
    return url

def run_automation():
    print("==================================================")
    print("[*] INICIANDO CAÇADA AUTÔNOMA DE PRODUTOS")
    print("==================================================")
    
    # 1. Caçador busca os produtos crus
    raw_products = search_ml_offers(keyword="ofertas smartphone")
    
    if not raw_products:
        print("[!] Nenhum produto encontrado hoje.")
        return

    processed_products = []
    
    # 2. Iterar sobre os produtos e passar para a IA Writer
    for i, product in enumerate(raw_products):
        print(f"\n[{i+1}/{len(raw_products)}] Processando: {product['title']}")
        
        # O robô de IA escreve a copy de vendas
        catchy_title, catchy_text = generate_cro_copy(product['title'], product['currentPrice'])
        
        # Injetar o link de afiliado
        affiliate_link = inject_affiliate_id(product['buyLink'], "ML")
        
        # Montar objeto final no padrão que o frontend web-store espera
        final_product = {
            "id": f"ml-{int(time.time())}-{i}",
            "customId": f"custom-{i}",
            "title": catchy_title, # Titulo tunado pela IA
            "image": product['image'],
            "currentPrice": product['currentPrice'],
            "originalPrice": product['originalPrice'],
            "recurrencePrice": None,
            "buyLink": affiliate_link, # Link comissionado
            "announcement": "Oferta Quente!",
            "productCode": f"ML-{i}",
            "catchyText": catchy_text, # Copy Persuasiva
            "conditionPayment": "Em até 12x",
            "website": "Mercado Livre",
            "cupom": "",
            "cupomValue": 0,
            "totalClicks": 0,
            "totalViews": 0,
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "published": True
        }
        
        processed_products.append(final_product)
        # Pausa para não estourar rate limit da IA (Groq é rapido, mas é boa pratica)
        time.sleep(2)
        
    # 3. Salvar o resultado num arquivo JSON
    # Como não temos o backend da loja, este JSON servirá de "Banco de Dados" temporário
    db_path = r"C:\Users\hytec\.gemini\antigravity\scratch\afiliados-claude-cro\web-store\public\products.json"
    
    try:
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(processed_products, f, ensure_ascii=False, indent=4)
        print(f"\n[+] SUCESSO! {len(processed_products)} produtos salvos em {db_path}")
    except Exception as e:
        print(f"\n[!] Erro ao salvar o banco de dados JSON: {e}")

if __name__ == "__main__":
    run_automation()
