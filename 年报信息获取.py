import requests
import pathlib
from datetime import datetime
import json


# 指定项目根路径为当前文件所处文件夹
root_dir = pathlib.Path.cwd()


# 定义查询目标
stock_code = '003816'
category_cn = '年报'
today = datetime.today().date().strftime('%Y-%m-%d')
seDate = f'2000-01-01~{today}'

category_map = {
    "年报": "category_ndbg_szsh",
    "半年报": "category_bndbg_szsh",
    "一季报": "category_yjdbg_szsh",
    "三季报": "category_sjdbg_szsh",
    "业绩预告": "category_yjygjxz_szsh",
    "权益分派": "category_qyfpxzcs_szsh",
    "董事会": "category_dshgg_szsh",
    "监事会": "category_jshgg_szsh",
    "股东大会": "category_gddh_szsh",
    "日常经营": "category_rcjy_szsh",
    "公司治理": "category_gszl_szsh",
    "中介报告": "category_zj_szsh",
    "首发": "category_sf_szsh",
    "增发": "category_zf_szsh",
    "股权激励": "category_gqjl_szsh",
    "配股": "category_pg_szsh",
    "解禁": "category_jj_szsh",
    "公司债": "category_gszq_szsh",
    "可转债": "category_kzzq_szsh",
    "其他融资": "category_qtrz_szsh",
    "股权变动": "category_gqbd_szsh",
    "补充更正": "category_bcgz_szsh",
    "澄清致歉": "category_cqdq_szsh",
    "风险提示": "category_fxts_szsh",
    "特别处理和退市": "category_tbclts_szsh",
    "退市整理期": "category_tszlq_szsh"
}
if category_cn != '':
    category = category_map[category_cn]
else:
    category = ''


with open('stock_info.json', 'r', encoding='utf-8') as f:
    stock_info = json.load(f)

for stock in stock_info['stockList']:
    if stock['code'] == stock_code:
        orgId = stock['orgId']
        full_stock_code = f'{stock_code},{orgId}'
        break



query_url = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'


# 定义请求头文件
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}


# 定义需要获取的数据字段
results = {
    'secCode': list(),
    'secName': list(),
    'announcementTitle': list(),
    'announcementId': list(),
    'announcementTime': list()
}


# 创建存放数据的文件，定义列名
results_path = root_dir.joinpath(f'pdf_to_download.csv')
# if results_path.exists() == False:
#     with open(results_path, 'w') as f:
#         row_to_write = ','.join([column_name for column_name in results.keys()]) + '\n'
#         print(row_to_write)
#         f.write(row_to_write)

with open(results_path, 'w', encoding='utf-8') as f:
    row_to_write = ','.join([column_name for column_name in results.keys()]) + '\n'
    print(row_to_write)
    f.write(row_to_write)


# 定义循环判断参数
hasMore = True
cur_pageNum = 1


while hasMore:
    form_data = {
        'pageNum': cur_pageNum,
        'pageSize': 30,
        'column': 'szse',
        'tabName': 'fulltext',
        'isHLtitle': True,
        'stock': full_stock_code,
        'category': category,
        'seDate': seDate
    }

    response = requests.post(query_url, headers=headers, data=form_data)
    r_json = json.loads(response.text)
    response.close()

    hasMore = r_json['hasMore']
    cur_pageNum += 1

    for announcement in r_json['announcements']:
        for key, value_list in results.items():
            value_list.append(announcement[key])

    with open(results_path, 'a', encoding='utf-8') as f:
        for i in range(len(results['secCode'])):
            row_to_write = ','.join([str(column[i]) for column in results.values()]) + '\n'
            print(row_to_write[:-1])
            f.write(row_to_write)
    
    # 初始化字典，每轮将数据保存至csv文件后清空
    results = {column_name: list() for column_name in results.keys()}



