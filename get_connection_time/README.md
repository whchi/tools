###說明
本程式目的為為測試網路連線時間
###原因
由於可能影響連線速度的因素有很多,因此撰寫此程式來協助MIS人員找出影響網路連線速度的可能原因
###使用方式
`php index.php hostname /path/to/action`
e.g:
`php index.php https://api.xxx.com.tw /user/get_a_user/`
###備註
* 輸出的log.txt使用excel打開
* 如不使用pest,可以用calling_ws.php
* 適用於動作為**post**的API
* function appReqAuth裡面的json_raw視情況修改
