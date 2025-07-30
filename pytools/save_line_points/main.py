import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRIVER_PATH = BASE_DIR + '/chromedriver'
CHROME_OPTIONS = Options()
settings = {
    'ACCOUNT': os.getenv('ACCOUNT'),
    'PASSWD': os.getenv('PASSWD'),
    'SEE_BROWSER': os.getenv('SEE_BROWSER', 'n'),
}
with open(f'{BASE_DIR}/toskip.txt', 'r') as f:
    to_skip = list(filter(None, f.readline().strip('\n').split(',')))
CHROME_OPTIONS.headless = False if settings['SEE_BROWSER'] == 'y' else True


def gogogo(account, passwd):
    df = pd.read_excel(f'{BASE_DIR}/pincodes.xlsx', header=None)
    df.columns = ['uri']

    uri_prefix = 'https://points.line.me/pointcode?pincode='
    point_codes = df.uri.apply(lambda s: s[len(uri_prefix):]).tolist()
    not_login_uri_prefix = 'https://access.line.me/dialog/oauth/weblogin'
    browser = webdriver.Chrome(executable_path=DRIVER_PATH,
                               options=CHROME_OPTIONS)

    browser.get(uri_prefix)
    new_skip = to_skip
    try:
        for code in point_codes:
            if code in to_skip:
                continue
            print(code)
            page_src = browser.page_source
            if '此點數代碼已兌換完畢。' in page_src:
                new_skip.append(code)
                time.sleep(3)
            elif '錯誤' in page_src or '30分鐘' in page_src:
                time.sleep(3)
                raise Exception('input rate limit')

            browser.implicitly_wait(1)

            pin_code = browser.find_element_by_id('pincode')
            send_btn = browser.find_element_by_css_selector(
                'form div.MdBtn01>button[type="submit"]')
            pin_code.clear()
            pin_code.send_keys(code)
            send_btn.send_keys(Keys.ENTER)
            if not_login_uri_prefix in browser.current_url:
                # login
                browser.find_element_by_id('id').send_keys(account)
                browser.find_element_by_id('passwd').send_keys(passwd)
                time.sleep(0.1)
                browser.find_element_by_css_selector(
                    'input[type="submit"]').send_keys(Keys.ENTER)
                time.sleep(0.3)

                if '此點數代碼已兌換完畢。' in page_src:
                    new_skip.append(code)
                    time.sleep(3)
                elif '錯誤' in page_src or '30分鐘' in page_src:
                    time.sleep(3)
                    raise Exception('input rate limit')

            new_skip.append(code)
            browser.find_element_by_css_selector(
                '#mainView div.MdBtn01>a').send_keys(Keys.ENTER)

    except WebDriverException as we:
        raise we
    except Exception as e:
        raise e
    finally:
        with open(f'{BASE_DIR}/toskip.txt', 'w') as f:
            f.write(','.join(new_skip))

        browser.close()


if __name__ == '__main__':
    gogogo(settings['ACCOUNT'], settings['PASSWD'])
