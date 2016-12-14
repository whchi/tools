<?php
/**
 * callingWs
 * @param  string  $url       FQDN
 * @param  string  $jsondata  要送到restful service的資料
 * @param  integer $timeout   connect timeout
 * @param  string  $proxy_url 如網路環境有proxy須設定
 * @return http-response body
 */
function callingWs($url, $jsondata = '', $timeout = 30, $proxy_url = '') {
	$proxy = $proxy_url;
	$curl = curl_init($url);
	if ($proxy !== '') {
		// set proxy
		curl_setopt($curl, CURLOPT_PROXY, $proxy);
		// go proxy
		curl_setopt($curl, CURLOPT_HTTPPROXYTUNNEL, 1);
	}
	// return curl_exec result as string
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1);
	// show all details
	curl_setopt($curl, CURLOPT_VERBOSE, 1);
	curl_setopt($curl, CURLOPT_POST, 1);
	//或是使用這個來指定方法為POST,這個方法通常用在GET/POST之外的地方
	//curl_setopt($curl, CURLOPT_CUSTOMREQUEST, 'POST');
	if (!empty($jsondata)) {
		//if $jsondata not set as string,use http_build_query($jsondata)
		curl_setopt($curl, CURLOPT_POSTFIELDS, $jsondata);
	}
	//不走ssl
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, 0);
	//ensure if the url is redirected
	curl_setopt($curl, CURLOPT_FOLLOWLOCATION, 1);
	//automatically update the referer header
	curl_setopt($curl, CURLOPT_AUTOREFERER, 1);
	//default 30 sec
	curl_setopt($curl, CURLOPT_TIMEOUT, $timeout);
	//include header in output
	curl_setopt($curl, CURLOPT_HEADER, 1);
	// get real host name
	// $real_url = curl_getinfo($curl, CURLINFO_EFFECTIVE_URL);
	$rst = curl_exec($curl);
	// $info = curl_getinfo($curl);
	/**
	 * curl有支援的request-response之間的時間,視情況使用
	 */
	// 建立連線的時間
	$connect_time = curl_getinfo($curl, CURLINFO_CONNECT_TIME);
	// 建立連線到準備傳輸的時間
	$pretransfer_time = curl_getinfo($curl, CURLINFO_PRETRANSFER_TIME);
	// 建立連線到開始傳輸的時間
	$start_transfer_time = curl_getinfo($curl, CURLINFO_STARTTRANSFER_TIME);
	// 最後一次傳輸消耗的時間
	$total_time = curl_getinfo($curl, CURLINFO_TOTAL_TIME);

	$error = curl_error($curl);
	$errno = curl_errno($curl);
	// get header and content apart
	list($header, $content) = explode("\r\n\r\n", $rst, 2);
	curl_close($curl);
	if (!empty($error)) {
		return $error;
	}
  // 取得http-response所花費的時間
	if (!empty($rst)) {
		$res_time = microtime(true);
		return $res_time;
	}
}
?>
