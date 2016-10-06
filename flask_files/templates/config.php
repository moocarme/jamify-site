<?php
$host_name = "localhost";
$database = "reco_db"; // Change your database name
$username = "matt-666";          // Your database user id 
$password = "test";          // Your password

//////// Do not Edit below /////////
try {
$dbo = new PDO('postgresql:host='.$host_name.';dbname='.$database, $username, $password);
} catch (PDOException $e) {
print "Error!: " . $e->getMessage() . "<br/>";
die();
}
?>