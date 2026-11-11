import os
import json
import urllib.request
import time

# O .strip() retira automaticamente qualquer espaço ou quebra de linha invisível
TOKEN = "9058904513:AAE9T6K4PMZf0tHvLSbL-LQYAFhGcZTMpu8".strip()

def run_bot():
    print("🤖 GuruBot a escutar na Railway com token limpo...")
    
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
                        print(f"📥 Mensagem recebida com sucesso do chat ID: {chat_id}")
                        
                        text = "🔍 Mestre, mensagem recebida com sucesso! A analisar as odds..."
                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
                        
                        send_req = urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'})
                        urllib.request.urlopen(send_req, timeout=10)
                        print("✅ Resposta enviada com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro no ciclo de polling: {e}")
            time.sleep(5)

if __name__ == '__main__':
    run_bot()
