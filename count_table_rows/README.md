### 說明
此程式目的為計算mysql正確的innoDB總列數，只適用於mysql5.6之前的版本的innoDB列數計算
### 原因
由於在mysql5.6之前的innoDB建立在information_schema.TABLES裡的列數總計只是估計值，因此寫了此程式正確計算每張表的值
### 備註
* 建議使用`php5.4~`內建的web server, 使用方法`php -S {hostname:port} -t {documentroot}`
* `db_config.php`視環境修改
