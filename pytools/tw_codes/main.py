# coding=utf-8
import pandas as pd
import numpy as np
import json
import argparse
import requests
from bs4 import BeautifulSoup
import unicodedata
import re


def get_valid_counties():
    with open('tw_counties.json', 'r') as f:
        map_ = json.load(f)
    return map_


def remove_control_characters(s):
    return ''.join(ch for ch in s if unicodedata.category(ch)[0] != "C")


def get_county(valid_county_codes):
    with open('縣市代碼-utf8.txt') as f:
        codes = [
            remove_control_characters(r.replace('臺',
                                                '台').replace('\n',
                                                             '')).split('=')
            for r in f.readlines()
        ]
    df = pd.DataFrame(data=codes,
                      dtype=np.str,
                      columns=['county_code', 'county_name'])

    return df[df['county_code'].isin(valid_county_codes)].reset_index(drop=True)


def get_town():
    with open('省市縣市鄉鎮市區代碼-utf8.txt') as f:
        codes = [
            remove_control_characters(
                r.replace('臺',
                          '台').replace('台灣省',
                                       '').replace('福建省',
                                                   '').replace('\n',
                                                               '')).split('=')
            for r in f.readlines()
        ]
    df = pd.DataFrame(data=codes,
                      dtype=np.str,
                      columns=['town_code', 'town_name'])
    return df


def get_village(year):
    yr_switcher = {
        2016: '歷史村里代碼檔-106年03月（UTF8）.txt',
        2020: '村里代碼檔-107年06月-UTF8.txt'
    }
    with open(f'{MAPCODES_DATA_DIR}/raw/{yr_switcher[year]}') as f:
        codes = [
            remove_control_characters(r.replace('臺',
                                                '台').replace('\n',
                                                             '')).split(',')
            for r in f.readlines()
        ]

    df = pd.DataFrame(data=codes,
                      dtype=np.str,
                      columns=['ris_village_code', 'town_code', 'village_name'])

    return df


def get_village_raw_by_year(history, ym):
    ris_prefix = 'https://www.ris.gov.tw'

    if history:
        uri = ris_prefix + '/documents/html/5/1/558.html'
        res = requests.get(uri)
        res.encoding = res.apparent_encoding
        if res.status_code == requests.codes.ok:
            year, month = ym.split('-')
            year = int(year) - 1911
            soup = BeautifulSoup(res.text, 'lxml')
            to_download = soup.find_all(
                'a',
                href=True,
                attrs={'download': re.compile(f'{year}年{month}月（UTF8）')})
            if not to_download:
                raise Exception('no such year and month')
            else:
                history_file = requests.get(ris_prefix + to_download[0]['href'])
                f_name = to_download[0]['download']
                open(f_name, 'wb').write(history_file.content)
    else:
        # default download latest
        uri = ris_prefix + '/documents/html/5/1/167.html'
        res = requests.get(uri)
        res.encoding = res.apparent_encoding
        if res.status_code == requests.codes.ok:
            soup = BeautifulSoup(res.text, 'lxml')
            to_download = soup.find_all(
                'a', href=True, attrs={'download': re.compile('UTF8.txt')})[0]
            res_file = requests.get(ris_prefix + to_download['href'])
            f_name = to_download['download']
            open(f_name, 'wb').write(res_file.content)
    with open(f_name, 'r') as f:
        codes = [
            remove_control_characters(r.replace('臺',
                                                '台').replace('\n',
                                                             '')).split(',')
            for r in f.readlines()
        ]

        df = pd.DataFrame(
            data=codes,
            dtype=np.str,
            columns=['ris_village_code', 'town_code', 'village_name'])

    return df, f_name


def create_mapping(df_c, df_t, df_v, file_name):
    year = int(re.search(r'\d{3}', file_name).group(0)) + 1911
    month = re.search(r'\d{2}', file_name).group(0)
    df_t = df_t[(~df_t['town_name'].str.contains('民政局|民政處')) & (
        df_t['town_name'].str.contains('|'.join(df_c['county_name'].tolist())))
                & (df_t['town_name'].str.len() > 3)].reset_index(drop=True)
    df_t['county_code'] = df_t['town_code'].apply(lambda s: s[:5])
    df_v['county_code'] = df_v['town_code'].apply(lambda s: s[:5])
    df = pd.merge(df_v, df_t, on='town_code', how='left')
    df = df.merge(df_c,
                  left_on='county_code_x',
                  right_on='county_code',
                  how='left').drop(['county_code_x', 'county_code_y'], axis=1)
    df.rename(columns={'town_name': 'countytown_name'}, inplace=True)
    df['town_name'] = df[['county_name', 'countytown_name']].apply(
        lambda s: clean_town_name(s['county_name'], s['countytown_name']),
        axis=1)
    df.drop(['countytown_name'], axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.loc[:,].to_csv(f'{year}_{month}-mapping.csv', index=False)


def clean_town_name(county_name, countytown_name):
    return countytown_name[len(county_name):]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='fma mp3 to npy')
    parser.add_argument('-history', action='store_true')
    parser.add_argument('-ym',
                        help='date to download, yyyymm',
                        type=str,
                        required=False,
                        default='2017-12')
    args = parser.parse_args()
    if args.history and not args.ym:
        raise Exception('should input ym')
    if args.ym and not re.search(r'\d{4}-\d{2}', args.ym):
        raise Exception('invalid ym format, should be yyyy-mm')

    valid_counties = get_valid_counties()
    df_county = get_county(valid_counties.keys())
    df_town = get_town()
    df_village, file_name = get_village_raw_by_year(args.history, args.ym)
    create_mapping(df_county, df_town, df_village, file_name)
