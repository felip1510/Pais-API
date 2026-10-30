import requests
import os
from dotenv import load_dotenv
load_dotenv()
from requests import get

REST_COUNTRIES_API_KEY = os.getenv("REST_COUNTRIES_API_KEY")

pais_escolhido = input("país desejado?(EM INGLÊS): ").lower()

url = f"https://api.restcountries.com/countries/v5/names.common/{pais_escolhido}"
headers = {"Authorization": f"Bearer {REST_COUNTRIES_API_KEY}"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()

    pais = dados["data"]["objects"][0]
    nome = pais["names"]["common"]
    sigla = pais["codes"]["alpha_2"]
    capital = pais["capitals"]
    regiao = pais["subregion"]
    lingua = pais["languages"]
    populacao = pais["population"]
    dinheiro = pais["currencies"]

    print(f"País: {nome}-{sigla}")
    print(f"Capital: {capital[0]["name"]}")
    print("Região: ", regiao)
    print("Lingua: ", lingua[0]["name"])
    print("População", populacao)
    print("Dinheiro local: ",dinheiro[0]["code"],"-",dinheiro[0]["symbol"])
else:
    print("Capital: Não possui capital cadastrada")