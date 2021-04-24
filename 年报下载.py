import requests
import pathlib
import pandas as pd
import numpy as np


base_url = 'http://www.cninfo.com.cn/new/announcement/download'
root_dir = pathlib.Path.cwd()
pdf_dir = root_dir.joinpath('pdf')
pdf_dir.mkdir(exist_ok=True)


df = pd.read_csv('./pdf_to_download.csv', dtype={'secCode': np.object})
df['announcementTime'] = pd.to_datetime(df['announcementTime'], format='%Y-%m-%d').dt.date


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}


for i in range(len(df)):
    params = {
        'bulletinId': df['announcementId'][i],
        'announceTime': df['announcementTime'][i]
    }

    code_name = df['secCode'][i]
    firm_name = df['secName'][i]


    code_dir = pdf_dir.joinpath(code_name)
    code_dir.mkdir(exist_ok=True)
    pdf_name = firm_name + '：' + df['announcementTitle'][i]
    

    print(f'正在下载 -- {pdf_name}')
    response = requests.get(url=base_url, params=params, headers=headers)
    pdf_path = code_dir.joinpath(pdf_name + '.pdf')
    with open(pdf_path, 'wb') as f:
        f.write(response.content)

print('\n全部文件下载完毕！')
    