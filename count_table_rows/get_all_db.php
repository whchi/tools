<?php
require 'db_lib.php';
// get all db name except system db
$sql = "SELECT SCHEMA_NAME AS DB_NAME
FROM `SCHEMATA`
WHERE SCHEMA_NAME NOT IN ( 'information_schema',
	'mysql',
	'phpmyadmin',
	'performance_schema',
	'webauth',
	'cdcol'
	)";
$db = new PdoDatabase('information_schema');
$db->prepareQuery($sql);
$alldb = $db->getQuery();
$count = $db->getAffetedRows();
for ($i = 0; $i < $count; $i++) {
	echo '<option value="' . $alldb[$i]['DB_NAME'] . '">' . $alldb[$i]['DB_NAME'] . '</option>';
}
$db->closeDbConn();