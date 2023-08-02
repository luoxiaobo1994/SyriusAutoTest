# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/7/14 11:13
# Desc:

import requests


def login_get_token():
    data = {"clientId": "2n3qhd0l4gm503t7p930eolal", "authFlow": "EMAIL_PASSWORD_AUTH",
            "authParameters": {"email": "wengying@syriusrobotics.com", "password": "Wengying@123"}}
    res = requests.post(url='https://gogoinsight.flexgalaxy.com' + '/api/authenication/login', json=data)
    # with open('token.json', 'w', encoding='utf-8') as f:
    #     json.dump(res.json(), f)
    return res.json()['tokenResult']['accessToken']


data = [{
    "id": "asda11a",
    "businessType": "Picking",
    "businessFlow": "Total Picking",
    "priority": "1",
    "batchId": "a",
    "items": [{
        "barcode": "123456",
        "name": "测试商品1",
        "imageUrl": "https://www.baidu.com",
        "quantity": "10",
        "binLocations": ["A01010101"],
        "attributes": {
            "notifyUrl": "",
            "storageSerialNo": ""
        }
    }],
    "storages": [{
        "type": "1A_container"
    }],
    "sequentialExecution": "FALSE",
    "attributes": {
        "batchOrderSequence": 1
    },
    "type": "TOTAL_PICKING",
    "timestamp": 1689304356733,
    "warehouseId": "1676409775058386945",
    "expectedFinishTime": 1689304356733,
    "expectedExecutionTime": 1689304356733
}]

url = 'https://gogoinsight.flexgalaxy.com/api/order/warehouse-order/'
token = 'eyJraWQiOiIzOGMzNGM1YmFlNjQ0ZDE5ODEzYzc3YWExOTY0ZDg5MCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiI1N2FlYmU2Yy0wMTMwLTQxYWQtOGI1OS03MmNmMGM4OWQxNGMiLCJuYmYiOjE2ODkzMDQyMjgsImNsaWVudElkIjoiIiwib3BlbklkIjoiNTdhZWJlNmMtMDEzMC00MWFkLThiNTktNzJjZjBjODlkMTRjIiwiaXNzIjoiaHR0cHM6XC9cL3d3dy5zeXJpdXNyb2JvdGljcy5jb21cL2ZsZXhnYWxheHkiLCJ0ZW5hbnRJZCI6IjcxIiwiZXhwIjoxNjg5MzkwNjI4LCJ0eXBlIjoiQkFTRV9UT0tFTiIsImlhdCI6MTY4OTMwNDIyOCwidXNlcklkIjoiMTUwNDAxMDc3MTcyMjA3MjA3OSIsImp0aSI6IjYxMGJlNzM0LWViYTEtNGQ2YS1iMDRhLWNiM2M0OTg2NTU5ZSJ9.J82QXUGs8Muf9A6YeDAWU-n6_6mS0HTC2i_pgnG5BMp4-e-ZBvTeAm-pofy0QoL1d7ZeTRBJzz__Crb66l8q5HsDw7aGkNJ9JU5M2MlrkW05ZxDuuDQILDg1LFuc2PrneeYqv6l4EXMS0DlDesaqa2aaUBOVATUjXSwysTt4vzSnSAcoUquREprShrJQfyxIwhvM4XH8-c8Fq3gjv2RM4Avn3GxqF-EAlBw6VWo7mBfve_eHrl61-GohvBFasNMWSq3IRccaTmY2lAYrbObZasLe74kCzKGnK6sBSP4Fu2rwGm62mhqRkCwYzlNhxUGTUsq5lmttN1gL-ZhkkHnMPw'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + login_get_token()
    # "Authorization": "Bearer " + token
}

res = requests.post(url=url, headers=headers, json=data)
print(res.status_code, res.json())
# print(login_get_token())
