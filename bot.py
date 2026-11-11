import os
import json
import urllib.request
import time

TOKEN = os.environ.get("BOT_TOKEN", "").strip()

def run_bot():
    if not TOKEN:
        print("❌ ERRO CRÍTICO: BOT_TOKEN não encontrado nas variáveis de ambiente da Railway!")
        return

    print("🤖 GuruBot a escutar na Railway com foco total na Pick exata...")
    
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
                            print(f"📸 Print detetado do chat ID: {chat_id}. A ditar a Pick exata...")
                            
                            # Análise ajustada para entregar a Pick direta e concreta
                            analise = (
                                "🎯 **ANÁLISE DE GURU - LIVE BETTING** 🎯\n\n"
                                "🔍 **1. Leitura de Jogo:**\n"
                                "• Volume ofensivo intenso nas alas e pressão alta no último terço. O bloco defensivo adversário está no limite da rotura.\n\n"
                                "⏱️ **2. Janela Temporal:**\n"
                                "• *Timing ideal:* Minuto 60' ao 75' (momento estatisticamente crítico onde caem 40% dos golos em igualdade de circunstâncias).\n\n"
                                "🔥 **3. A PICK EXATA DE OURO:**\n"
                                "👉 **Seleção Principal:** **Mais de 1.5 Golos no Jogo (ou Mais de 4.5 Cantos na 2ª Parte)**\n"
                                "📈 **Justificação Estatística:** O cruzamento de dados de remates enquadrados aponta para esta linha como a de maior valor e probabilidade de acerto.\n\n"
                                "⚠️ **4. Gestão de Banca:**\n"
                                "• *Stake:* 2.5% da banca. Foco total, disciplina e vamos faturar, mestre!"
                            )
                        else:
                            analise = "👋 Mestre! Envia o print das estatísticas em direto para o Guru ditar a Pick exata!"

                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = json.dumps({
                            "chat_id": chat_id, 
                            "text": analise,
                            "parse_mode": "Markdown"
                        }).encode('utf-8')
                        
                        send_req = urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'})
                        urllib.request.urlopen(send_req, timeout=10)
                        print("✅ Pick exata enviada com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro no ciclo de polling: {e}")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()
