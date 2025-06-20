import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime

# PARAMETRES DE SELECTION
symbols = ["METTRE LE SYMBOLE DE L'ENTREPRISE ICI"] # sélectionner les entreprises souhaitées
api_key = ['METTRE LA CLE API ICI'] # ID Alpha Vantage
industry = "METTRE LE SECTEUR ICI" # renseigner le secteur d'activité


# REQUETES POUR BILAN ET COMPTE DE RESULTAT
report_types = ['BALANCE_SHEET', 'INCOME_STATEMENT']
all_data = {'INCOME_STATEMENT': [], 'BALANCE_SHEET': []}

for symbol in symbols:
    for report_type in report_types:
        url = f'https://www.alphavantage.co/query?function={report_type}&symbol={symbol}&apikey={api_key}'
        r = requests.get(url)
        data = r.json()

        #key = "quarterlyReports" possible également
        key = "annualReports" if "annualReports" in data else None

        if key:
            for report in data[key]:
                report["symbol"] = symbol
                report["industry"] = industry
                all_data[report_type].append(report)


df_income = pd.DataFrame(all_data['INCOME_STATEMENT'])
df_balance = pd.DataFrame(all_data['BALANCE_SHEET'])

df_balance['reportedCurrency'] = df_balance['reportedCurrency'].replace({'None': np.nan})
df_income['reportedCurrency'] = df_income['reportedCurrency'].replace({'None': np.nan})
df_balance['reportedCurrency'] = df_balance.groupby('symbol')['reportedCurrency'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else None))
df_income['reportedCurrency'] = df_income.groupby('symbol')['reportedCurrency'].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else None))

# check pour vérifier que les imports ont bien fonctionnés
print("Import Balance sheet ok")
print("Import Income statement ok")


# REQUETE STOCK PRICE
report_type_stock = 'TIME_SERIES_DAILY'
# Stocker les résultats
stock_historicals = {'TIME_SERIES_DAILY': []}

# Requête pour chaque symbols
for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function={report_type_stock}&symbol={symbol}&outputsize=full&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    # Vérifier si la clé "Time Series (Daily)" est bien présente
    if "Time Series (Daily)" in data:
        time_series = data["Time Series (Daily)"]

        for date, values in time_series.items():
            stock_data = {
                "symbol": symbol,
                "industry": industry,
                "date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            }
            stock_historicals["TIME_SERIES_DAILY"].append(stock_data)

    else:
        print(f"⚠️ Erreur pour {symbol}: {data}")

# Convertir en DataFrame Pandas
df_stock = pd.DataFrame(stock_historicals['TIME_SERIES_DAILY'])

# check imports réalisés
print('Import stock price ok')


# REQUETE DIVIDENDES
report_type_dividends = 'DIVIDENDS'
# Stocker les résultats
dividend_historicals = {'DIVIDENDS': []}

default_row = {
    'ex_dividend_date': None,
    'declaration_date': None,
    'record_date': None,
    'payment_date': datetime(2025,2,15).date(),
    'amount': 0,
    'symbol': None,
    'industry': None
}

for symbol in symbols:
    url = f'https://www.alphavantage.co/query?function={report_type_dividends}&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    key = data.get("data", None)

    if key:
        for report in key:
            report["symbol"] = symbol
            report["industry"] = industry
            dividend_historicals[report_type_dividends].append(report)

    else:
        # Si aucune donnée, ajouter une ligne par défaut avec l'entreprise et l'industrie
        empty_row = default_row.copy()
        empty_row["symbol"] = symbol
        empty_row["industry"] = industry
        dividend_historicals[report_type_dividends].append(empty_row)

df_dividend = pd.DataFrame(dividend_historicals['DIVIDENDS'])

# check imports réalisés
print("Import des dividendes ok")