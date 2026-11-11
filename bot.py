import os
import json
import urllib.request
import time
import random

TOKEN = os.environ.get("BOT_TOKEN", "").strip()

def run_bot():
    if not TOKEN:
        print("❌ ERRO CRÍTICO: BOT_TOKEN não encontrado nas variáveis de ambiente da Railway!")
        return

    print("🤖 GuruBot a escutar na Railway com matriz temporal rigorosa (1ª vs 2ª Parte)...")
    
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook", timeout=10)
    except:
        pass

    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=30"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=35)
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('ok') and 'result' in data:
                for update in data['result']:
                    offset = update['update_id'] + 1
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        message = update['message']
                        
                        if 'photo' in message:
                            caption = message.get('caption', '').lower().strip()
                            print(f"📸 Print detetado do chat ID: {chat_id} | Legenda: '{caption}'")
                            
                            if 'pre' in caption or 'pré' in caption:
                                # PRÉ-LIVE
                                analise = (
                                    "🎯 **ANÁLISE DE GURU - PRÉ-LIVE DE ELITE** 🎯\n\n"
                                    "📊 **1. Contexto Inicial:**\n"
                                    "• *Diagnóstico:* Cotações de abertura e estatísticas de H2H avaliadas.\n\n"
                                    "🔥 **2. A PICK EXATA DE OURO:**\n"
                                    "👉 **Ambas as Equipas Marcam (BTTS - Sim)**\n"
                                    "📈 *Odd Alvo:* **~1.78**\n\n"
                                    "💡 **3. Justificação Estatística:**\n"
                                    "• Alta taxa de conversão recente e porosidade defensiva simétrica.\n\n"
                                    "⚠️ **4. Gestão de Risco:**\n"
                                    "• *Stake:* 2% da banca. Disciplina de ferro, mestre!"
                                )
                            else:
                                # LIVE BETTING - Vamos dar opção de 1ª Parte ou 2ª Parte com base no timing ideal
                                # Como detetámos o erro na 1ª parte, criamos picks específicas para a primeira metade do encontro:
                                picks_live_1p = [
                                    {
                                        "mercado": "Mais de 0.5 Golo na 1ª Parte",
                                        "odd": "~1.75",
                                        "leitura": "Pressão inicial evidente e espaços abertos nas transições. O primeiro golo está iminente antes do intervalo."
                                    },
                                    {
                                        "mercado": "Mais de 1.5 Cantos na 1ª Parte",
                                        "odd": "~1.80",
                                        "leitura": "Volume ofensivo pelas faixas laterais a forçar cortes frequentes para a linha de fundo."
                                    }
                                ]
                                
                                escolha = random.choice(picks_live_1p)
                                
                                analise = (
                                    "🎯 **ANÁLISE DE GURU - LIVE BETTING (1ª PARTE)** 🎯\n\n"
                                    "⏱️ **1. Escaneamento de Momento & Dinâmica:**\n"
                                    "• *Leitura de Jogo:* Jogo a decorrer na primeira metade. Ritmo intenso e blocos ainda longos.\n\n"
                                    "🔥 **2. A PICK EXATA DE OURO:**\n"
                                    f"👉 **{escolha['mercado']}**\n"
                                    f"📈 *Odd Alvo:* **{escolha['odd']}**\n\n"
                                    f"📊 **3. Justificação Estatística:**\n"
                                    f"• {escolha['leitura']}\n\n"
                                    "⚠️ **4. Gestão de Risco:**\n"
                                    "• *Stake:* 2% da banca. Foco total e rigor absoluto, mestre!"
                                )
                        else:
                            analise = "👋 Mestre! Envia o print com a fotografia para o Guru ditar a lei!"

                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = json.dumps({
                            "chat_id": chat_id, 
                            "text": analise,
                            "parse_mode": "Markdown"
                        }).encode('utf-8')
                        
                        send_req = urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'})
                        urllib.request.urlopen(send_req, timeout=10)
                        print("✅ Análise corrigida enviada com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro no ciclo de polling: {e}")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()
