import requests, json, os
from bs4 import BeautifulSoup

print(">>> start")
r = requests.get(
    'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies',
    headers={'User-Agent': 'Mozilla/5.0'}
)
print(">>> status", r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table', {'id': 'constituents'})
print(">>> table found:", table is not None)

tickers = []
for row in table.find('tbody').find_all('tr')[1:]:
    cell = row.find('td')
    if cell:
        tickers.append(cell.get_text(strip=True))

print(">>> tickers:", len(tickers), tickers[:5])

os.makedirs('tmp', exist_ok=True)
with open('tmp/sp500_tickers.json', 'w') as f:
    json.dump(tickers, f)
print(">>> SAVED")
