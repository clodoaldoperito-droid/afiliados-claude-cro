import requests
import urllib.parse

def search_shopee_offers(keyword="smartphone"):
    print(f"[*] Caçador (API Shopee) ativado: Buscando ofertas para '{keyword}' na Shopee...")
    
    encoded_keyword = urllib.parse.quote(keyword)
    url = f"https://shopee.com.br/api/v4/search/search_items?by=relevancy&keyword={encoded_keyword}&limit=5&newest=0&order=desc&page_type=search&scenario=PAGE_GLOBAL_SEARCH&version=2"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://shopee.com.br/",
        "x-api-source": "pc"
    }
    
    products = []
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        items = data.get("items", [])
        
        for item_wrapper in items:
            try:
                item = item_wrapper.get("item_basic", {})
                title = item.get("name", "Sem Título")
                
                # Shopee armazena preços multiplicados por 100000
                price = float(item.get("price", 0)) / 100000
                original_price = float(item.get("price_before_discount", 0)) / 100000
                if original_price == 0:
                    original_price = price * 1.2
                
                itemid = item.get("itemid", "")
                shopid = item.get("shopid", "")
                
                # Montar link (simplificado)
                title_url = title.replace(" ", "-").lower()[:30]
                link = f"https://shopee.com.br/{title_url}-i.{shopid}.{itemid}"
                
                image_id = item.get("image", "")
                image_url = f"https://cf.shopee.com.br/file/{image_id}" if image_id else ""
                
                products.append({
                    "title": title,
                    "currentPrice": price,
                    "originalPrice": original_price,
                    "buyLink": link,
                    "image": image_url
                })
            except Exception as e:
                print(f"[!] Erro ao parsear produto da Shopee: {e}")
                continue
                
    except Exception as e:
        print(f"[!] Erro ao acessar a API da Shopee: {e}")
        
    print(f"[*] Encontrados {len(products)} produtos reais na Shopee via API!")
    return products

if __name__ == "__main__":
    ofertas = search_shopee_offers("smartphone")
    for o in ofertas:
        print(o)
