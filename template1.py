import json
import requests
import pandas as pd
import numpy as np

reso = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false&price_change_percentage=1h%2C24h%2C7d%2C30d")
json_data = json.loads(reso.text)
Table = pd.DataFrame(json_data)

Table1 = Table.filter( items = ['name','current_price','market_cap','market_cap_rank','circulating_supply','total_supply','ath','total_volume','high_24h','low_24h','price_change_24h','price_change_percentage_24h','market_cap_change_24h','market_cap_change_percentage_24h','last_updated'], axis = 1)

Table1['current_price'] = '$' + Table1['current_price'].astype(str) #adds dollar sign to price
Table1['total_volume'] = '$' + Table1['total_volume'].astype(str).replace('\.0', '', regex=True)
Table1['market_cap'] = '$' + Table1['market_cap'].astype(str).replace('\.0', '', regex=True)
Table1['circulating_supply'] = Table1['circulating_supply'].round(0).astype(str)
Table1['total_supply'] = Table1['total_supply'].round(0).astype(str).replace('nan', '', regex=True)
Table1['market_cap_change_24h'] = np.where( Table1['market_cap_change_24h'] < 0, '-$' + Table1['market_cap_change_24h'].round(0).astype(str).str[1:].replace('\.0', '', regex=True), '$' + Table1['market_cap_change_24h'].round(0).astype(str).replace('\.0', '', regex=True))

Table1['price_change_percentage_24h'] = Table1['price_change_percentage_24h'].astype(str) + '%'
Table1['market_cap_change_percentage_24h'] = Table1['market_cap_change_percentage_24h'].astype(str) + '%'

Table2 = Table1.rename(columns = {'current_price':'Price','name':'Name','market_cap_rank': 'Rank','market_cap': 'Market Capitalization','circulating_supply': 'Circulating Supply','total_supply': 'Total Supply','ath':'All Time High','total_volume':'24h Volume','high_24h':'Price (24h High)','low_24h':'Price (24h Low)','price_change_24h':'24h Price Change','price_change_percentage_24h':'24h Price % Change','market_cap_change_24h':'Market Cap 24h Change','market_cap_change_percentage_24h':'Market Cap 24h % Change','last_updated':'Last Updated'})
    
Table2.set_index('Name',inplace =True)
Table3 = Table2.loc[['Bitcoin','Ethereum','XRP','EOS','Bitcoin Cash','Litecoin','Binance Coin','Bitcoin SV','Cardano','Stellar','IOST','Steem','TomoChain','IoTeX']] #filters based on symbol

#set additional decimal to those ending wih 1 zero
x = 0
while x < 14:
    if len(Table3['Price'][x]) < 8 and Table3['Price'][x][-3] != ".":
        Table3['Price'][x] = Table3['Price'][x] + "0"
    if Table3['Price'][x][-2] == ".":
        Table3['Price'][x] = Table3['Price'][x][0:6]
    x = x + 1
Table3 = Table3.reset_index()
Table3 = Table3[['Rank','Name','Price','24h Volume','Market Capitalization','Circulating Supply','Total Supply','All Time High','Price (24h High)','Price (24h Low)','24h Price Change','24h Price % Change','Market Cap 24h Change','Market Cap 24h % Change','Last Updated']]

print(Table3) #prints test result

Table3.to_csv(r'C:\Users\Forge-15R\Desktop\Template1.csv',index = False, header =True) #exports csv ,change path based on user