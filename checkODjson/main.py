import json, csv
import sys, os
import re
from config import *

def checkIfUnicodeExists(s):
    return re.search('[\u4e00-\u9fff]+', s)

def getValidateOidAndOrg():
    org = {}
    with open('GDS.csv', newline = '', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # skip first line
        next(reader)
        for row in reader:
            org[row[1]] = row[0]
        return org

jsonFile = 'example.json'
# 下載後把 jsonFile 修改為下方
# jsonFile = sys.argv[1]

if os.path.isfile(jsonFile):
    fn, fext = os.path.splitext(jsonFile)
    if fext != '.json':
        sys.exit('input file ext name must be json')
else:
    sys.exit('no such file named ' + jsonFile)

validateOrgOid = getValidateOidAndOrg()
tochk = json.loads(open(jsonFile, encoding='utf-8').read())
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

# 檢查傳入oid是否存在於政府oid清單
if tochk['publisherOID'] not in validateOrgOid.keys():
    sys.exit('資料集提供機關oid【' + tochk['publisherOID'] +'】不存在')
# 檢查oid與機關名稱是否相符
if validateOrgOid[tochk['publisherOID']] != tochk['publisher']:
    sys.exit('資料集提供機關【'+ tochk['publisher'] +'】與其oid不符，應為【'+ validateOrgOid[tochk['publisherOID']] +'】')
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
