<!DOCTYPE html>
<html lang="zh-tw">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
	<script src="//code.jquery.com/jquery-2.1.4.min.js"></script>
	<link rel="stylesheet" type="text/css" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
</head>

<body>
	<select class="form-control" name="dbname" id="dbname">
		<option value="">選擇資料庫</option>
		<?php include_once 'get_all_db.php'; ?>
	</select>
	<br /><br />
	<div id="result"></div>
	<div id="errorResult"></div>
	<script src="assets/js/all.js"></script>
</body>
</html>
