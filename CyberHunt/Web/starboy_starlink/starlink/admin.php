<?php
session_start();
if (empty($_SESSION['login']) || $_SESSION['login'] !== true) {
    header("Location: /index.php");
    exit;
}

if ($_SESSION['admin'] === true) {
    $mode = 'admin';
    $flag = file_get_contents("/flag.txt");
} else {
    $mode = 'guest';
    $flag = "***** Access Denied *****";
}
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Admin Panel - SpaceX</title>
        <style>table, td { margin: auto; border: 1px solid #000; }</style>
    </head>
    <body style="text-align: center;">
        <h1>Starlink Control Panel</h1>
        <table><tbody>
            <tr><td><b>Status Orbit</b></td><td>SERVER UP</td></tr>
            <tr><td><b>Router IP</b></td><td>192.168.1.1</td></tr>
            <tr><td><b>Your IP</b></td><td>127.0.0.1</td></tr>
            <tr><td><b>Access Mode</b></td><td><?= $mode ?></td></tr>
            <tr><td><b>FLAG</b></td><td><?= $flag ?></td></tr>
        </tbody></table>
    </body>
</html>