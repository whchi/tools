import os
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path='.env')

PANDAS_TO_JSON_PARAMS = {'force_ascii': False, 'orient': 'records'}


def clean_bank_name(bank_name):
    try:
        p = re.compile(r'[農|漁]會')
        pos = p.search(bank_name).end()
        return bank_name[:pos]
    except Exception as e:
        return None


def make_love_code_map():
    url = 'https://quality.data.gov.tw/dq_download_csv.php?nid=31868&md5_url=4d4f544023dda33ac54a3adca1aec4c9'
    df_raw = pd.read_csv(url, dtype={'捐贈碼': str})
    df_all = df_raw[['受捐贈機關或團體名稱', '捐贈碼']].rename(columns={
        '受捐贈機關或團體名稱': 'name',
        '捐贈碼': 'code'
    })
    df_all.to_json('tw_love_code_mapping.json', **PANDAS_TO_JSON_PARAMS)


def make_tw_bank_map():
    post_office_url = 'https://quality.data.gov.tw/dq_download_csv.php?nid=5950&md5_url=21483be4e8097acbd4f1e2f24e1bb3c1'
    bank_url = 'https://www.fisc.com.tw/TC/OPENDATA/R2_Location.csv'
    post_csv = pd.read_csv(post_office_url, dtype={'六碼郵遞區號': str})
    bank_csv = pd.read_csv(bank_url, dtype={'銀行代號': str, '分支機構代號': str})

    df_post = post_csv[post_csv['六碼郵遞區號'].notna()]
    df_bank = bank_csv[bank_csv['銀行代號'].notna()]
    bank_primary = df_bank[df_bank['分支機構代號'].notna()]
    # cleanup 金融機構名稱
    bank_primary.loc[bank_primary['金融機構名稱'].str.contains('[農|漁]會')].apply(
        lambda x: clean_bank_name(x))

    banks = bank_primary[['銀行代號', '分支機構代號', '金融機構名稱', '分支機構名稱', '地址']].rename(
        columns={
            '銀行代號': 'code',
            '分支機構代號': 'branch_code',
            '金融機構名稱': 'name',
            '分支機構名稱': 'branch_name',
            '地址': 'address'
        })
    posts = df_post.copy()
    posts = posts[['電腦局號', '局名', '縣市', '鄉鎮市區', '地址']]
    posts.rename(columns={
        '電腦局號': 'branch_code',
        '局名': 'branch_name'
    },
                 inplace=True)
    posts['address'] = posts['縣市'] + posts['鄉鎮市區'] + posts['地址']
    posts.drop(columns=['縣市', '鄉鎮市區', '地址'], inplace=True)
    posts['code'] = '700'
    posts['name'] = '中華郵政股份有限公司'

    df_all = pd.concat([posts, banks])
    df_all.to_json('tw_bank_code_mapping.json', **PANDAS_TO_JSON_PARAMS)


if __name__ == '__main__':
    make_tw_bank_map()
    make_love_code_map()
