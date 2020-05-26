台灣22縣市代碼 mapping 建立


資料來源：[內政部戶政司村里代碼](https://www.ris.gov.tw/documents/html/5/1/167.html)

### 使用方式
* 歷史資料
```sh
python main.py -history -ym yyyy-mm #要符合歷史年月才有資料，比如 106-10 就輸入 2017-10
```
* 最新資料
```sh
python main.py
```
* 備註
1. 檔案編碼要轉成 utf-8
2. 如果有新的縣市就增加在 `tw_counties.json`
3. 省市縣市鄉鎮市區代碼、縣市代碼理論上不會改變，視內政部公告為主

### sample output
```txt
ris_village_code,town_code,village_name,county_code,county_name,town_name
09007010001,09007010,介壽村,09007,連江縣,南竿鄉
09007010002,09007010,復興村,09007,連江縣,南竿鄉
09007010003,09007010,福沃村,09007,連江縣,南竿鄉
09007010004,09007010,清水村,09007,連江縣,南竿鄉
...
```
