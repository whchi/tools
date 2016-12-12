<?php
include 'pest/PestJSON.php';
date_default_timezone_set('Asia/Taipei');
// 每個時間的title
echo "| sendtime | google '/' | {$argv[1]} '/' | {$argv[1]} '{$argv[2]}' | \n";
for ($i = 0; $i < 20; $i++) {
    //發送時間
    $ts = date('y-m-d h:i:s', time());
    //連到google.com的 / 花費時間,作為基準
    $t1 = httpReq('https://google.com', '/');
    // 連到特定FQDN(要測試的站台)的 / 花費時間,作為基準
    $t2 = httpReq($argv[1], '/');
    //有送值的API取得回應所花費時間,指定為想要測試的站台,hostname會和$t2一樣
    $t3 = appReqAuth($argv);
    //寫入之後可以匯入excel，進行比對
    $fp = fopen('./log.txt', 'a+');
    fwrite($fp, "$ts,$t1,$t2,$t3\n");
    fclose($fp);
    echo "$ts,$t1,$t2,$t3\n";
    sleep(5);
}
/**
 * 取得遠端host 根目錄所需時間
 * @param  string $api_url  遠端主機名稱
 * @param  string $api_path 遠端web service路徑
 * @return double           request~response的時間
 */
function httpReq($api_url, $api_path)
{
    $pest = new Pest($api_url);
    $start_time = microtime(true);
    $thing = $pest->get($api_path, '/');
    if (isset($thing)) {
        $end_time = microtime(true);
    }
    $intval_time = $end_time - $start_time;
    return $intval_time;
}
/**
 * 取得遠端host 任一api動作所需時間
 * @return double  request~response的時間
 */
function appReqAuth($argv)
{
	// API動作所需的值
    $json_raw = array(
        'KEY' => '',
        'PASS' => '',
    );
    $api_url = $argv[1];
    $api_path = $argv[2];
    $pest = new Pest($api_url);
    $headers = array('Content-Type: application/json; charset=utf-8');
    $start_time = microtime(true);
    $thing = $pest->post($api_path, json_encode($json_raw), $headers);
    if (isset($thing)) {
        $end_time = microtime(true);
    }
    $intval_time = $end_time - $start_time;
    return $intval_time;
}
