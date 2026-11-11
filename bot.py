import os
import json
import urllib.request
import threading
import time

TOKEN = "9058904513:AAE9T6K4PMZf0tHvLSbL-LQYAFhGcZTMpu8"
PORT = int(os.environ.get("PORT", "10000"))

def run_polling():
    print("🤖 A iniciar o sistema de escuta (Polling) em segundo plano...")
    offset = 0
    # Limpa qualquer webhook anterior para evitar conflitos
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook", timeout=10)
    except:
        pass

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
                        print(f"📥 Mensagem capturada via Polling do chat {chat_id}")
                        
                        text = "🔍 Mestre, print recebido com sucesso! A analisar as odds e a cruzar dados do SofaScore..."
                        send_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                        payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
                        send_req = urllib.request.Request(send_url, data=payload, headers={'Content-Type': 'application/json'})
                        urllib.request.urlopen(send_req, timeout=10)
                        print("✅ Resposta enviada com sucesso!")
        except Exception as e:
            # Em caso de falha de rede temporária, espera 5 segundos e tenta de novo
            time.sleep(5)

# Arranca a escuta numa thread separada para o servidor WSGI continuar feliz no Render
threading.Thread(target=run_polling, daemon=True).start()

def handler(environ, start_response):
    start_response('200 OK', [('Content-Type', 'application/json')])
    return [b'{"status":"polling_active"}']

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"🤖 Servidor WSGI a arrancar na porta {PORT}...")
    httpd = make_server('0.0.0.0', PORT, handler)
    httpd.serve_forever()
