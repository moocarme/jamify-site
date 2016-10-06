<?php
    $connection = mysqli_connect("localhost","matt-666") or die("Error " . mysqli_error($connection));

    //fetch department names from the department table
    $sql = "SELECT artist_name from reco_table";
    $result = mysqli_query($connection, $sql) or die("Error " . mysqli_error($connection));

    $dname_list = array();
    while($row = mysqli_fetch_array($result))
    {
        $dname_list[] = $row['birth_month'];
    }
    echo json_encode($dname_list);
?>