import pandas as pd
import re


def clean_bank_name(bank_name):
    try:
        p = re.compile(r'[農|漁]會')
        pos = p.search(bank_name).end()
        return bank_name[:pos]
    except Exception as e:
        return None


post_office_url = 'https://quality.data.gov.tw/dq_download_csv.php?nid=5950&md5_url=21483be4e8097acbd4f1e2f24e1bb3c1'
bank_url = 'https://www.fisc.com.tw/TC/OPENDATA/R2_Location.csv'

if __name__ == '__main__':
    post_csv = pd.read_csv(post_office_url, dtype={'六碼郵遞區號': str})
    bank_csv = pd.read_csv(bank_url, dtype={'銀行代號': str, '分支機構代號': str})
    df_post = post_csv[post_csv['六碼郵遞區號'].notna()]
    df_bank = bank_csv[bank_csv['銀行代號'].notna()]
    bank_primary = df_bank[df_bank['分支機構代號'].notna()]
    # cleanup 金融機構名稱
    bank_primary.loc[bank_primary['金融機構名稱'].str.contains('[農|漁]會')].apply(lambda x: clean_bank_name(x))

    banks = bank_primary[['銀行代號', '分支機構代號', '金融機構名稱', '分支機構名稱', '地址']].rename(columns={
        '銀行代號': 'code',
        '分支機構代號': 'branch_code',
        '金融機構名稱': 'name',
        '分支機構名稱': 'branch_name',
        '地址': 'address'
    })
    posts = df_post.copy()
    posts = posts[['電腦局號', '局名', '縣市', '鄉鎮市區', '地址']]
    posts.rename(columns={'電腦局號': 'branch_code', '局名': 'branch_name'}, inplace=True)
    posts['address'] = posts['縣市'] + posts['鄉鎮市區'] + posts['地址']
    posts.drop(columns=['縣市', '鄉鎮市區', '地址'], inplace=True)
    posts['code'] = '700'
    posts['name'] = '中華郵政股份有限公司'

    df_all = pd.concat([posts, banks])
    df_rst = df_all.to_json(orient='records', force_ascii=False)
    # [{"branch_code":"000100-6","branch_name":"臺北北門郵局","address":"臺北市中正區忠孝西路一段120號1樓","code":"700","name":"中華郵政股份有限公司"} ...]
