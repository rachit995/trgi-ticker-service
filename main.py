from fastapi import FastAPI
import requests
import json


app = FastAPI()


@app.get("/ticker")
async def root():
    url = "https://api.coingecko.com/api/v3/coins/the-real-golden-inu"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    current = 0
    current = format(data["tickers"][0]["converted_last"]["usd"], '.20f')
    last = format(data["tickers"][0]["last"], '.20f')
    return {"current": current}
