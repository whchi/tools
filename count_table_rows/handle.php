<?php
include 'db_lib.php';
$dbname = $_POST['dbname'];
$sql = "SELECT TABLE_SCHEMA DB_NAME,
       TABLE_NAME
FROM `TABLES`
WHERE `TABLE_SCHEMA` = '{$dbname}'";

$db = new PdoDatabase('information_schema');
$db->prepareQuery($sql);
$tables = $db->getQuery();

$table_count = "SELECT";
foreach ($tables as $value) {
    $db_table = "`" . $value['DB_NAME'] . "`.`" . $value['TABLE_NAME'] . "`";
    $table_alias = $value['DB_NAME'] . "_OWNS_" . $value['TABLE_NAME'];
    $table_count .= "\r\n(SELECT count(*) FROM " . $db_table . " ) AS '" . $table_alias . "',";
}
$table_count = substr($table_count, 0, -1);
$table_count .= "\r\nFROM DUAL";
$db->prepareQuery($table_count);
$rst = $db->getQuery();
$db->closeDbConn();
echo json_encode($rst);
