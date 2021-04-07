import json
import requests
import pandas as pd
import numpy as np
import scipy as sp

reso1 = requests.get("https://api.covalenthq.com/v1/1/events/topics/0xd013ca23e77a65003c2c659c5442c00c805371b7fc1ebd4c206c41d1536bd90b/?starting-block=9470000&ending-block=10470000&sender-address=0x45f783cce6b7ff23b2ab2d70e416cdb7d6055f51&page-size=20000")
reso2 = requests.get("https://api.covalenthq.com/v1/1/events/topics/0xd013ca23e77a65003c2c659c5442c00c805371b7fc1ebd4c206c41d1536bd90b/?starting-block=10470000&ending-block=11260000&sender-address=0x45f783cce6b7ff23b2ab2d70e416cdb7d6055f51&page-size=20000")

#dataframe 1
json_data = json.loads(reso1.text)
fil = json_data['data']['items']
df = pd.DataFrame(fil)

df1= df.filter(items = ['block_signed_at','block_height','tx_offset','log_offset','tx_hash','sender_address','sender_address_label'], axis = 1) #removes all non-important columns)
df1['sender_address_label'] = df1['sender_address_label'].astype(str).replace('None', 'Curve.fi: y Pool', regex=True)
df1['logged_buyer'] = np.nan
df1['logged_sold_id'] = np.nan
df1['logged_tokens_sold'] = np.nan
df1['logged_bought_id'] = np.nan
df1['logged_tokens_bought'] = np.nan

x = 0
while x < 14364:
    df1['logged_buyer'][x] = df['decoded'][x]['params'][0]['value']
    df1['logged_sold_id'][x] = df['decoded'][x]['params'][1]['value']
    df1['logged_tokens_sold'][x] = df['decoded'][x]['params'][2]['value']
    df1['logged_bought_id'][x] = df['decoded'][x]['params'][3]['value']
    df1['logged_tokens_bought'][x] = df['decoded'][x]['params'][4]['value']
    x = x + 1

#end of dataframe 1

#dataframe 2
json_data2 = json.loads(reso2.text)
fil1 = json_data2['data']['items']
df2 = pd.DataFrame(fil1)

df3= df2.filter(items = ['block_signed_at','block_height','tx_offset','log_offset','tx_hash','sender_address','sender_address_label'], axis = 1) #removes all non-important columns)
df3['sender_address_label'] = df3['sender_address_label'].astype(str).replace('None', 'Curve.fi: y Pool', regex=True)
df3['logged_buyer'] = np.nan
df3['logged_sold_id'] = np.nan
df3['logged_tokens_sold'] = np.nan
df3['logged_bought_id'] = np.nan
df3['logged_tokens_bought'] = np.nan

y = 0
while y < 16238:
    df3['logged_buyer'][y] = df2['decoded'][y]['params'][0]['value']
    df3['logged_sold_id'][y] = df2['decoded'][y]['params'][1]['value']
    df3['logged_tokens_sold'][y] = df2['decoded'][y]['params'][2]['value']
    df3['logged_bought_id'][y] = df2['decoded'][y]['params'][3]['value']
    df3['logged_tokens_bought'][y] = df2['decoded'][y]['params'][4]['value']
    y = y + 1

#end of dataframe 2
#merge both dataframes
df4 = df1.append(df3)
df4.index=range(len(df4))
print(df4)

#print dataframe to csv
df4.to_csv(r'C:\Users\Forge-15R\Desktop\ypool.csv',index = False, header =True) #exports csv ,change path based on user

