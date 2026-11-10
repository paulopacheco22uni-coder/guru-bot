import os
import json
import urllib.request

P1 = "9126886161"
P2 = "AAGEWjgU2PxjczZnAxWolelYvVs71tKvpoc"
TOKEN = f"{P1}:{P2}"

PORT = int(os.environ.get("PORT", "10000"))

def handler(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if environ['REQUEST_METHOD'] == 'POST':
        body = environ['wsgi.input'].read(request_body_size)
        try:
            data = json.loads(body.decode('utf-8'))
            print(f"📥 Dados recebidos do Telegram: {data}")
            
            if 'message' in data:
                chat_id = data['message']['chat']['id']
                text = "🔍 Mestre, print recebido com sucesso! A analisar as odds e a cruzar dados do SofaScore..."
                
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
                payload = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
                req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
                
                try:
                    urllib.request.urlopen(req, timeout=5)
                    print("✅ Mensagem de resposta enviada ao Telegram com sucesso!")
                except Exception as e_send:
                    print(f"❌ Erro ao enviar resposta para o Telegram: {e_send}")
                    
        except Exception as e:
            print(f"❌ Erro ao ler JSON: {e}")

    start_response('200 OK', [('Content-Type', 'application/json')])
    return [b'{"status":"ok"}']

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    print(f"🤖 Bot nativo a arrancar na porta {PORT}...")
    httpd = make_server('0.0.0.0', PORT, handler)
    httpd.serve_forever()
