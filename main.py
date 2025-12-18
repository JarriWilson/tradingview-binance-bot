from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook recibido:", data)
    return {"status": "ok"}

if __name__ == "__main__":
    print("Servidor iniciado correctamente SIN Binance")
    app.run(host="0.0.0.0", port=8080)

