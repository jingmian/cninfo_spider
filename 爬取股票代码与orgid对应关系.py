import requests
import json



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

info_url =  'http://www.cninfo.com.cn/new/data/szse_stock.json'
response = requests.get(info_url, headers=headers)

with open('stock_info.json', 'w', encoding='utf-8') as f:
    f.write(response.text)

print('公司信息更新成功！')