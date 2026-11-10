import os
import json
import urllib.request

P1 = "9126886161"
P2 = "AAGEWjgU2PxjczZnAxWolelYvVs71tKvpoc"
TOKEN = f"{P1}:{P2}"

PORT = int(os.environ.get("PORT", "10000"))

def handler(environ, start_response):
    # Se abrires o site no browser (GET), ativamos o webhook automaticamente de forma limpa!
    if environ['REQUEST_METHOD'] == 'GET':
        ext_url = os.environ.get("RENDER_EXTERNAL_URL")
        if ext_url:
            webhook_target = f"{ext_url}/"
            set_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_target}"
            try:
                resp = urllib.request.urlopen(set_url, timeout=10)
                result_text = resp.read().decode('utf-8')
                start_response('200 OK', [('Content-Type', 'application/json')])
                return [f'{{"status": "webhook_registered", "telegram_response": {result_text}}}'.encode('utf-8')]
            except Exception as e:
                start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
                return [f'{{"error": "{str(e)}"}}'.encode('utf-8')]

    # Processamento de mensagens do Telegram (POST)
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if environ['REQUEST_METHOD'] == 'POST':
        body = environ['wsgi.input'].read(request_body_size)
        try:
            data = json.loads(body.decode('utf-8'))
            print(f"📥 MENSAGEM RECEBIDA DO TELEGRAM: {data}")
            
            if 'message' in data:
                chat_id = data['message']['chat']['id']
                text = "🔍 Mestre, print recebido com sucesso! A analisar as odds e a cruzar dados do SofaScore..."
                
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                
                urllib.request.urlopen(req, timeout=5)
                print("✅ Resposta enviada de volta ao Telegram!")
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")

    start_response('200 OK', [('Content-Type', 'application/json')])
    return [b'{"status":"ok"}']

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"🤖 Bot nativo a arrancar na porta {PORT}...")
    httpd = make_server('0.0.0.0', PORT, handler)
    httpd.serve_forever()
