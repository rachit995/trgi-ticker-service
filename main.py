from fastapi import FastAPI
import requests
import json
import socket

hostname = socket.gethostname()
VERSION = "0.1.1"
PRECISION = ".20f"

app = FastAPI()


@app.get("/")
async def root():
    return {
        "name": "trgi-ticker-service",
        "host": hostname,
        "version": VERSION
    }


@app.get("/ticker")
async def ticker():
    url = "https://api.coingecko.com/api/v3/coins/the-real-golden-inu"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    current = 0
    current = format(data["tickers"][0]["converted_last"]["usd"], PRECISION)
    return {"current": current}
