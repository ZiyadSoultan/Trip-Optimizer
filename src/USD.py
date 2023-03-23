import requests


def update_USD() -> None:
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=CAD&to_currency=USD&apikey=2T56EF7IAN2IKNHO'
    rate = requests.get(url).json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
    with open("USD.txt", "w") as file:
        file.write(rate)
