import os
import json
import urllib.request
import urllib.parse

TOKEN = "9126886161:AAFG_yGcdt0FH-_ofjHtGobtG0JWfI_BGzE"
PORT = int(os.environ.get("PORT", "10000"))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

# O próprio bot configura o webhook sozinho assim que arranca no Render
if RENDER_URL:
    webhook_url = f"{RENDER_URL}/"
    api_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
    try:
        urllib.request.urlopen(api_url)
        print("✅ Webhook ativado automaticamente com sucesso no Telegram!")
    except Exception as e:
        print(f"⚠️ Erro ao ativar webhook: {e}")

def handler(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if environ['REQUEST_METHOD'] == 'POST':
        body = environ['wsgi.input'].read(request_body_size)
        data = json.loads(body.decode('utf-8'))
        
        # Se mandares uma foto, o bot responde imediatamente
        if 'message' in data and 'photo' in data['message']:
            chat_id = data['message']['chat']['id']
            text = "🔍 Mestre, print recebido com sucesso! A analisar as odds e a cruzar dados do SofaScore..."
            
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b"Bot do Guru ativo e operacional!"]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"🤖 Bot nativo a arrancar na porta {PORT}...")
    httpd = make_server('0.0.0.0', PORT, handler)
    httpd.serve_forever()
