import json, csv
import sys, os
import re
import time, datetime

from config import *

###############
# Global Vars #
###############
curdir = os.path.dirname(__file__)
curdir = '.' if curdir == '' else curdir
errors = []
f = True
jsonFile = sys.argv[1]

def checkIfUnicodeExists(s):
    return re.search('[\u4e00-\u9fff]+', s)

def getValidateOidAndOrg():
    global curdir
    orgoid = {}
    with open(curdir + '/GDS.csv', newline = '', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
        # skip first line
        next(reader)
        for row in reader:
            orgoid[row[1]] = row[0]
        return orgoid

def dateTimeisNotValidate(dateTime):
    if not dateTime:
        return ''

    t = datetime.datetime.strptime(dateTime, "%Y-%m-%d %H:%M:%S")
    try:
        time.mktime(t.timetuple())
        return ''
    except Exception as e:
        return '['+dateTime +'] ' + str(e)

if os.path.isfile(jsonFile):
    fn, fext = os.path.splitext(jsonFile)
    if fext != '.json':
        errors.append('input file ext name must be json')
    try:
        tochk = json.loads(open(jsonFile, encoding='utf-8').read())
    except ValueError:
        errors.append('json format is not validate')
else:
    errors.append('no such file named ' + jsonFile)

if not errors:
    # 檢查第一層是否都已填
    for key in requiredField:
        f = True
        if key not in tochk.keys():
            f = False
            errors.append('必填欄位 ' + key + ' 未填')
        if f:
            if tochk[key] is None or tochk[key] == '':
                errors.append('欄位 ' + key + ' 不應為空')
    if errors:
        print('error messages:')
        for i in errors:
            print(i)
    else:
        # 中文字串檢查
        if checkIfUnicodeExists(tochk['identifier']) is not None:
            errors.append('欄位【identifier】不應含中文字')
        if checkIfUnicodeExists(tochk['publisher']) is None:
            errors.append('欄位【publisher】應含中文字')

        # 檢查傳入時間格式是否符合
        if dateTimeisNotValidate(tochk['temporalCoverageFrom']):
            errors.append('欄位【temporalCoverageFrom】格式錯誤:' + dateTimeisNotValidate(tochk['temporalCoverageFrom']))
        if dateTimeisNotValidate(tochk['temporalCoverageTo']):
            errors.append('欄位【temporalCoverageTo】格式錯誤:' + dateTimeisNotValidate(tochk['temporalCoverageTo']))
        if dateTimeisNotValidate(tochk['issued']):
            errors.append('欄位【issued】格式錯誤:' + dateTimeisNotValidate(tochk['issued']))
        if dateTimeisNotValidate(tochk['modified']):
            errors.append('欄位【modified】格式錯誤:' + dateTimeisNotValidate(tochk['modified']))

        # 檢查傳入oid是否存在於政府oid清單
        validateOrgOid = getValidateOidAndOrg()
        if tochk['publisherOID'] not in validateOrgOid.keys():
            errors.append('資料集提供機關oid【' + tochk['publisherOID'] +'】不存在')
        # 檢查oid與機關名稱是否相符
        if validateOrgOid[tochk['publisherOID']] != tochk['publisher']:
            errors.append('資料集提供機關【'+ tochk['publisher'] +'】與其oid不符，應為【'+ validateOrgOid[tochk['publisherOID']] +'】')
        # 檢查categoryCode 是否正確
        if tochk['categoryCode'] not in dataClassification:
            errors.append('分類錯誤，不應有【'+tochk['categoryCode']+'】分類')

        # 資料類型是否正確
        if tochk['type'].lower() not in datasetType:
            errors.append('資料類型錯誤: 不應有【' + tochk['type'].lower() +'】類型')
        # distribution 已有值
        for i in tochk['distribution']:
            if dateTimeisNotValidate(i['resourceModified']):
                errors.append('resourceID: ' + i['resourceID'] + ' 欄位【resourceModified】格式錯誤:' + dateTimeisNotValidate(i['resourceModified']))
            for dkey in requiredDistField:
                if dkey not in i.keys():
                    errors.append('resourceID: ' + i['resourceID'] + ' 必填欄位【' + dkey + '】未填')
                if i[dkey] is None or i[dkey] == '':
                    errors.append('resourceID: ' + i['resourceID'] + ' 欄位【' + dkey + '】不應為空')
                if dkey == 'format':
                    if i[dkey] not in dataFormat:
                        errors.append('resourceID: ' + i['resourceID'] + ' format填寫錯誤: 不應有【' + i[dkey] + '】')
        if errors:
            print('error messages:')
            for i in errors:
                print(i)
        else:
            print('通過驗證')
else:
    print('error messages:')
    for i in errors:
        print(i)
