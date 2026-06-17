import re
import json
import datetime
from agent_cro_writer import generate_cro_copy

def parse_hot_products(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Separa por blocos usando a URL como delimitador do final ou o inicio 🔥
    # O conteúdo não é perfeitamente estruturado, então vamos usar Regex
    blocks = re.split(r'🔗\s*(https?://[^\s]+)', content)
    
    products = []
    
    # blocks contém textos e urls alternados
    current_text = ""
    for i in range(len(blocks)):
        if blocks[i].startswith('http'):
            url = blocks[i].strip()
            # O texto anterior (blocks[i-1]) contém os dados do produto
            text = blocks[i-1].strip()
            
            # Extrair título (segunda linha ou primeira depois do 🔥)
            lines = text.split('\n')
            title = "Produto"
            for line in lines:
                if line.strip() and not line.startswith('🔥') and not line.startswith('❌') and not line.startswith('💚') and not line.startswith('💥') and not line.startswith('✅') and not line.startswith('📊'):
                    title = line.strip()
                    break
            
            # Extrair preço original
            original_price = 0.0
            op_match = re.search(r'❌\s*~R\$\s*([\d\.,]+)', text)
            if op_match:
                op_str = op_match.group(1).replace('.', '').replace(',', '.')
                try:
                    original_price = float(op_str)
                except:
                    pass
                    
            # Extrair preço atual
            current_price = 0.0
            cp_match = re.search(r'💚\s*R\$\s*([\d\.,]+)', text)
            if cp_match:
                cp_str = cp_match.group(1).replace('.', '').replace(',', '.')
                try:
                    current_price = float(cp_str)
                except:
                    pass

            if current_price > 0:
                products.append({
                    "title": title,
                    "currentPrice": current_price,
                    "originalPrice": original_price if original_price > 0 else current_price,
                    "buyLink": url,
                    "image": "https://cf.shopee.com.br/file/br-11134201-7qukw-ligsowwrtz0f67" # Imagem genérica para testes se não tivermos
                })
        else:
            continue
            
    return products

def run_import():
    products = parse_hot_products('hot_products.txt')
    print(f"[*] {len(products)} produtos extraídos do texto.")
    
    final_data = []
    for i, p in enumerate(products):
        print(f"\n[{i+1}/{len(products)}] Processando: {p['title']}")
        catchy_title, catchy_text = generate_cro_copy(p['title'], p['currentPrice'])
        
        final_product = {
            "id": f"shopee-hot-{i}",
            "customId": f"custom-{i}",
            "title": catchy_title,
            "image": p['image'],
            "currentPrice": p['currentPrice'],
            "originalPrice": p['originalPrice'],
            "recurrencePrice": None,
            "buyLink": p['buyLink'],
            "announcement": "Oferta Quente!",
            "productCode": f"SHOPEE-{i}",
            "catchyText": catchy_text,
            "conditionPayment": "Em até 12x",
            "website": "Shopee",
            "cupom": "",
            "cupomValue": 0,
            "totalClicks": 0,
            "totalViews": 0,
            "createdAt": datetime.datetime.utcnow().isoformat() + "Z",
            "updatedAt": datetime.datetime.utcnow().isoformat() + "Z",
            "published": True
        }
        final_data.append(final_product)
        
    output_path = '../web-store/public/products.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
        
    print(f"\n[+] SUCESSO! {len(final_data)} produtos importados e salvos em {output_path}")

if __name__ == "__main__":
    run_import()
