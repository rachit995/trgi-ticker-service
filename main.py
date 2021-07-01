from fastapi import FastAPI
import requests
import json
import socket
import datetime

hostname = socket.gethostname()
VERSION = "0.1.1"
PRECISION = ".20f"
COIN_ID = "the-real-golden-inu"
CONTRACT_ADDRESS = "0xb5db7640182042a150ccdb386291f08f23b77a96"

app = FastAPI()


def get_current_price(coin, wrt="usd"):
    # url = "https://api.coingecko.com/api/v3/coins/" + coin
    # response = requests.request("GET", url)
    # data = json.loads(response.text)
    # return format(data["tickers"][0]["converted_last"][wrt], PRECISION)
    url = "https://api.coingecko.com/api/v3/coins/" + coin + "?market_data=true"
    response = requests.request("GET", url)
    data = json.loads(response.text)
    return format(data["market_data"]["current_price"][wrt], PRECISION)

def get_token_status(contract_address):
    url = "https://bscscan.com/token/" + contract_address + "#readContract"
    response = requests.request("GET", url)
    data = response.text
    # marekt caps
    start_pos = data.find("Market Cap")
    if (start_pos < 0):
        return {}
    start_pos = data.find("pricebutton", start_pos)
    if (start_pos < 0):
        return {}
    start_pos = data.find(">", start_pos) + 1
    if (start_pos < 1):
        return {}
    end_pos = data.find("<", start_pos)
    if (end_pos < 0):
        return {}
    market_cap = data[start_pos:end_pos].strip('\n ')
    # holders
    start_pos = data.find("Holders:")
    if (start_pos < 0):
        return {}
    end_pos = data.find("addresses", start_pos)
    if (end_pos < 0):
        return {}
    start_pos = data.rfind('>', 0, end_pos) + 1
    holders = data[start_pos:end_pos].strip().replace(",", "")
    # burned amount
    url = "https://bscscan.com/readContract?m=normal&a=" + contract_address + "&v=" + contract_address
    response = requests.request("GET", url)
    data = response.text
    start_pos = data.find("totalBurn")
    if (start_pos < 0):
        return {}
    start_pos = data.find("form-group", start_pos)
    if (start_pos < 0):
        return {}
    end_pos = data.find("</a>", start_pos)
    if (end_pos < 0):
        return {}
    start_pos = data.rfind(">", 0, end_pos) + 1
    if (start_pos < 1):
        return {}
    burn_fee = data[start_pos:end_pos].strip('\n ')
    
    print(market_cap, ',', holders, ',', burn_fee)
    return {
        "market_cap": market_cap,
        "holders": holders,
        "burned": burn_fee
    }

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


@app.get("/summary")
async def summary():
    status = get_token_status(CONTRACT_ADDRESS)
    print(status)
    status.update({
        "timestamp": datetime.datetime.now()
    })
    return status