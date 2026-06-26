import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot

# --- CONFIGURAÇÕES DO TELEGRAM ---
TOKEN_DO_BOT = "8605026473:AAFONUDjz8Oe_p-rN8bWunQkmWLFvy6wFp0" 
SEU_CHAT_ID = "8800030466" 

# Link do leite Ninho que você inspecionou no Mercado Livre
URL_PRODUTO = "https://www.mercadolivre.com.br/supermercado/market#nav-header"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

bot = Bot(token=TOKEN_DO_BOT)

def pegar_preco_mercado_livre():
    resposta = requests.get(URL_PRODUTO, headers=HEADERS)
    soup = BeautifulSoup(resposta.text, "html.parser")
    
    # Usando a div e a classe que você encontrou na inspeção!
    preco_box = soup.find("div", class_="poly-component__price")
    
    # Pega o texto (ex: R$ 13,90) e limpa os espaços
    return preco_box.text.strip() if preco_box else "Preço não encontrado"

async def enviar_alerta_telegram(mensagem):
    await bot.send_message(chat_id=SEU_CHAT_ID, text=mensagem)

async def main():
    # Colocamos um valor falso no início para ele disparar o primeiro Alerta de teste
    preco_salvo = "R$ 0,00" 
    print("Iniciando o Monitor do Mercado Livre...")

    while True:
        try:
            preco_atual = pegar_preco_mercado_livre()
            print(f"Checando Mercado Livre... Preço atual: {preco_atual}")
            
            if preco_atual != preco_salvo:
                msg = f"🚨 ALERTA DE PREÇO NO MERCADO LIVRE!\nO produto mudou para: {preco_atual}"
                print(msg)
                
                # Envia o alerta real para o seu celular
                await enviar_alerta_telegram(msg)
                
                preco_salvo = preco_atual
            else:
                print("✅ O preço continua o mesmo.")
                
        except Exception as e:
            print(f"Erro ao ler site: {e}")
            
        # Espera 30 segundos para não ser bloqueado pelo site
        await asyncio.sleep(30)

# Inicia o robô
asyncio.run(main())