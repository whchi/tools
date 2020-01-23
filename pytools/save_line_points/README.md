### 前言
因為某次意外，抽到了 10000 點 line points，拿到的時候居然是 10x1000 個 uri...\
所以寫了這個程式處理它
### demo
<a href="https://www.youtube.com/watch?v=CYc8CBqm5Lw&feature=player_embedded&v=-pdYK9Xg8Jw
" target="_self"><img src="https://img.youtube.com/vi/CYc8CBqm5Lw/0.jpg"
alt="" width="100%" height="auto" border="10" /></a>
### 作法
1. 一份滿滿的兌換 uri xlsx，組成如下

||
|:--|
|https://points.line.me/pointcode?pincode=XXXXX|
|https://points.line.me/pointcode?pincode=XXXXX|
|https://points.line.me/pointcode?pincode=XXXXX|
|https://points.line.me/pointcode?pincode=XXXXX|
2. 使用 pandas 讀取它，擷取 pointcode 字串作為每次 loop 的 input
3. 使用 selenium 模擬操作行為
### 用法
0. **擁有一份得獎清單**
1. cfg.txt 裡面設定 line 帳密以及要不要看到瀏覽器
2. 建立 toskip.txt
3. `pip install -r requiremennts.txt`
4. `python main.py`
5. wait until finish
