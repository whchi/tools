import json
import sys
import re
from config import *

def checkIfUnicodeExists(s):
    return re.search('[\u4e00-\u9fff]+', s)

if __name__ == '__main__':
    tochk = json.loads(open('tocheck.json', encoding='utf-8').read())
    # 檢查第一層是否都已填
    for key in requiredField:
        if key not in tochk.keys():
            sys.exit('必填欄位 ' + key + ' 未填')
        if tochk[key] is None or tochk[key] == '':
            sys.exit('欄位 ' + key + ' 不應為空')

    # 中文字串檢查
    if checkIfUnicodeExists(tochk['identifier']) is not None:
        sys.exit('欄位【identifier】不應含中文字')
    if checkIfUnicodeExists(tochk['publisher']) is None:
        sys.exit('欄位【publisher】應含中文字')

    # 檢查categoryCode 是否正確
    if tochk['categoryCode'] not in dataClassification:
        sys.exit('分類錯誤，不應有【'+tochk['categoryCode']+'】分類')

    # 資料類型是否正確
    if tochk['type'].lower() not in datasetType:
        sys.exit('資料類型錯誤: 不應有【' + tochk['type'].lower() +'】類型')
    # distribution 已有值
    for i in tochk['distribution']:
        for dkey in requiredDistField:
            if dkey not in i.keys():
                sys.exit('必填欄位【' + dkey + '】未填')
            if i[dkey] is None or i[dkey] == '':
                sys.exit('欄位【' + dkey + '】不應為空')
            if dkey == 'format':
                if i[dkey] not in dataFormat:
                    sys.exit('format填寫錯誤: 不應有【' + i[dkey] + '】')

    sys.exit('通過驗證')
