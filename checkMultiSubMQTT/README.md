## 用途
確認當有多個mqtt subscriber時，訊息有推送成功
## 邏輯
每個新建的subscriber都會產出屬於自己的log檔案，透過check.js去檢查所有檔案的最後修改時間，並將其記錄起來，每次檢查時比對紀錄與實際的最後修改時間，如果數量不匹配表示有漏訊息

於stdout輸出訊息
## 檔案說明
|name|desc|
|:--|:--|
|startServer.sh|啟動mqtt server(需先安裝，我是用mosquitto)|
|stopServer.sh|結束mqtt server|
|submulti.sh|建立subscribers，使用方式為`sh submulti.sh {數量} {qos}`，要修改topic到裡面改|
|stat.sh|查看log黨的大小並排序，如果有不一致表示該subscriber有漏訊息|


## 備註
publisher.js為使用[mqtt.js](https://github.com/mqttjs)的publisher範例，推薦使用[MQTTLens](https://chrome.google.com/webstore/detail/mqttlens/hemojaaeigabkbcookmlgmdigohjobjm?hl=zh-TW)即可
