import os
import time
import requests
from bs4 import BeautifulSoup

# Configurações do Telegram
TOKEN = os.environ.get("TELEGRAM_TOKEN")
# Como o canal é privado/link de convite, usamos o ID do canal ou o link de convite formatado
CHAT_ID = "https://t.me/+vST52AN1FTo1YWYx" 

# Configuração de Afiliado do Mercado Livre
AFILIADO_ID = "ig20260216215126"

# Termos de busca para monitorar os iPhones mais vendidos
TERMOS_BUSCA = ["iphone-13", "iphone-14"]

def gerar_link_afiliado(link_original):
    # Remove parâmetros extras do link original para limpar a URL
    link_limpo = link_original.split("#")[0].split("?")[0]
    # Estrutura base de redirecionamento de afiliados do Mercado Livre (formato simplificado de tracking)
    link_afiliado = f"{link_limpo}?matt_pdm=onm&matt_ca=afiliados&matt_mgl={AFILIADO_ID}"
    return link_afiliado

def enviar_mensagem_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")
        return None

def monitorar_precos():
    for termo in TERMOS_BUSCA:
        print(f"Buscando ofertas para: {termo}...")
        url = f"https://lista.mercadolivre.com.br/{termo}_NoIndex_True#D[A:{termo}]"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Seleciona os itens da lista de resultados
            produtos = soup.find_all("div", class_="ui-search-result__wrapper")[:2] # Pega os 2 primeiros resultados de cada
            
            for produto in produtos:
                titulo_el = produto.find("h2", class_="ui-search-item__title")
                preco_el = produto.find("span", class_="andes-money-amount__fraction")
                link_el = produto.find("a", class_="ui-search-link")
                
                if titulo_el and preco_el and link_el:
                    titulo = titulo_el.text.strip()
                    preco = preco_el.text.strip()
                    link_original = link_el["href"]
                    
                    # Gera o link com a sua comissão
                    link_promocional = gerar_link_afiliado(link_original)
                    
                    # Monta a mensagem para o seu Canal de Ofertas
                    mensagem = (
                        f"📱 *OFERTA IMPERDÍVEL: {titulo}*\n\n"
                        f"💰 Por apenas: *R$ {preco}*\n\n"
                        f"🛒 Garanta o seu antes que esgote:\n"
                        f"{link_promocional}"
                    )
                    
                    print(f"Enviando oferta encontrada: {titulo}")
                    enviar_mensagem_telegram(mensagem)
                    time.sleep(5) # Evita spam
                    
        except Exception as e:
            print(f"Erro ao processar termo {termo}: {e}")

if __name__ == "__main__":
    monitorar_precos()