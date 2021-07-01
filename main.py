from fastapi import FastAPI
import requests
import json
import socket
import datetime

hostname = socket.gethostname()
VERSION = "0.1.1"
PRECISION = ".20f"

app = FastAPI()


def get_current_price(coin, wrt="usd"):
    url = "https://api.coingecko.com/api/v3/coins/" + coin
    response = requests.request("GET", url)
    data = json.loads(response.text)
    return format(data["tickers"][0]["converted_last"][wrt], PRECISION)


@app.get("/")
async def root():
    return {
        "name": "trgi-ticker-service",
        "host": hostname,
        "version": VERSION
    }


@app.get("/ticker")
async def ticker():
    current = get_current_price("the-real-golden-inu")
    return {
        "last": current,
        "timestamp": datetime.datetime.now()
    }
