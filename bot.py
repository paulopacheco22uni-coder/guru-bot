import os
import json
import urllib.request

# Dividido para garantir que o Safari ou o telemóvel não corrompem o token ao copiar
TOKEN_PART1 = "9126886161"
TOKEN_PART2 = "AAFG_yGcdt0FH-_ofjHtGobtG0JWfI_BGzE"
TOKEN = f"{TOKEN_PART1}:{TOKEN_PART2}"

PORT = int(os.environ.get("PORT", "10000"))
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

# Configura o webhook automaticamente ao arrancar no Render
if RENDER_URL:
    webhook_url = f"{RENDER_URL}/"
    api_url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
    try:
        response = urllib.request.urlopen(api_url)
        print(f"✅ Webhook ativado automaticamente: {response.read().decode('utf-8')}")
    except Exception as e:
        print(f"⚠️ Erro ao ativar webhook: {e}")

def handler(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if environ['REQUEST_METHOD'] == 'POST':
        body = environ['wsgi.input'].read(request_body_size)
        try:
            data = json.loads(body.decode('utf-8'))
            if 'message' in data and 'photo' in data['message']:
                chat_id = data['message']['chat']['id']
                text = "🔍 Mestre, print recebido com sucesso! A analisar as odds e a cruzar dados do SofaScore..."
                
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                urllib.request.urlopen(req, timeout=5)
        except Exception as e:
            print(f"Erro no processamento: {e}")

    start_response('200 OK', [('Content-Type', 'application/json')])
    return [b'{"status":"ok"}']

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"🤖 Bot nativo a arrancar na porta {PORT}...")
    httpd = make_server('0.0.0.0', PORT, handler)
    httpd.serve_forever()
