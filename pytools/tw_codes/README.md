台灣22縣市代碼 mapping 建立


資料來源：[內政部戶政司村里代碼](https://www.ris.gov.tw/documents/html/5/1/167.html)

### 使用方式
* 歷史資料
```sh
python main.py -history yyyy-mm #要符合歷史年月才有資料，比如 106-10 就輸入 2017-10
```
* 最新資料
```sh
python main.py
```
* 備註
1. 檔案編碼要轉成 utf-8
2. 如果有新的縣市就增加在 `tw_counties.json`
3. 省市縣市鄉鎮市區代碼、縣市代碼理論上不會改變，視內政部公告為主
