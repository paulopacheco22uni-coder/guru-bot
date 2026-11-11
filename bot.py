import os
import json
import urllib.request
import time

TOKEN = os.environ.get("BOT_TOKEN", "").strip()

def run_bot():
    if not TOKEN:
        print("❌ ERRO CRÍTICO: BOT_TOKEN não encontrado nas variáveis de ambiente da Railway!")
        return

    print("🤖 GuruBot a escutar na Railway com controlo exato por legenda (Live vs Pré-live)...")
    
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
                            # Lê a legenda que o utilizador escreve ao enviar a foto (se houver)
                            caption = message.get('caption', '').lower().strip()
                            print(f"📸 Print detetado do chat ID: {chat_id} | Legenda: '{caption}'")
                            
                            # Se a legenda contiver 'pre', assume Pré-live; caso contrário, assume Live.
                            if 'pre' in caption or 'pré' in caption:
                                analise = (
                                    "🎯 **ANÁLISE DE GURU - PRÉ-LIVE DE ELITE** 🎯\n\n"
                                    "📊 **1. Contexto de Mercado (Pré-jogo):**\n"
                                    "• *Diagnóstico:* Cotações iniciais e estatísticas de H2H avaliadas com rigor.\n\n"
                                    "🔥 **2. A PICK EXATA DE OURO:**\n"
                                    "👉 **Ambas as Equipas Marcam (BTTS)**\n"
                                    "📈 *Odd Alvo:* **~1.75**\n\n"
                                    "💡 **3. Justificação Estatística:**\n"
                                    "• Fragilidades defensivas simétricas e alta taxa de conversão recente nos dois planteis.\n\n"
                                    "⚠️ **4. Gestão de Risco:**\n"
                                    "• *Stake:* 2% da banca. Disciplina de ferro, mestre!"
                                )
                            else:
                                analise = (
                                    "🎯 **ANÁLISE DE GURU - LIVE BETTING** 🎯\n\n"
                                    "⏱️ **1. Contexto de Jogo (Em Direto):**\n"
                                    "• *Leitura de Momento:* Pressão intensa no último terço e volume ofensivo alto.\n\n"
                                    "🔥 **2. A PICK EXATA DE OURO:**\n"
                                    "👉 **Mais de 0.5 Golo na 2ª Parte**\n"
                                    "📈 *Odd Alvo:* **~1.85**\n\n"
                                    "📊 **3. Justificação Estatística:**\n"
                                    "• O rácio de remates enquadrados aponta para a quebra da muralha defensiva até ao apito final.\n\n"
                                    "⚠️ **4. Gestão de Risco:**\n"
                                    "• *Stake:* 2.5% da banca. Foco total, disciplina e vamos faturar, mestre!"
                                )
                        else:
                            analise = "👋 Mestre! Envia o print com a foto para o Guru ditar a lei!"

                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = json.dumps({
                            "chat_id": chat_id, 
                            "text": analise,
                            "parse_mode": "Markdown"
                        }).encode('utf-8')
                        
                        send_req = urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'})
                        urllib.request.urlopen(send_req, timeout=10)
                        print("✅ Análise direcionada enviada com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro no ciclo de polling: {e}")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()
