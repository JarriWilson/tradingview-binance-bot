from flask import Flask, request
from binance.client import Client
import os

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    symbol = data['symbol'].replace("BINANCE:", "").replace("PERP", "")
    side = data.get('side')
    sl = float(data.get('sl', 0))
    tp = float(data.get('tp', 0))

    balance = float(client.futures_account_balance()[6]['balance'])
    risk_pct = 0.01
    risk_usdt = balance * risk_pct

    price = float(client.futures_mark_price(symbol=symbol)['markPrice'])
    qty = round(risk_usdt / abs(price - sl), 3)

    if side == "BUY":
        client.futures_create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
        client.futures_create_order(symbol=symbol, side="SELL", type="STOP_MARKET", stopPrice=sl, closePosition=True)
        client.futures_create_order(symbol=symbol, side="SELL", type="TAKE_PROFIT_MARKET", stopPrice=tp, closePosition=True)

    elif side == "SELL":
        client.futures_create_order(symbol=symbol, side="SELL", type="MARKET", quantity=qty)
        client.futures_create_order(symbol=symbol, side="BUY", type="STOP_MARKET", stopPrice=sl, closePosition=True)
        client.futures_create_order(symbol=symbol, side="BUY", type="TAKE_PROFIT_MARKET", stopPrice=tp, closePosition=True)

    return {"status": "ok"}

app.run(host="0.0.0.0", port=8080)
