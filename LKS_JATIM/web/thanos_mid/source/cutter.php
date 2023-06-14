<?php
function get_file_size($file)
{
    $cmd = "stat --printf=\"%s\" $file 2>&1";
    echo "Executing $cmd" . "<br>";

    exec($cmd, $output);
    var_dump($output);

    if (is_array($output) && ctype_digit($size = trim(implode("\n", $output)))) {
        return $size;
    }

    return filesize($file);
}

if ($_SERVER['REQUEST_METHOD'] == "POST" && isset($_POST['thanosed'])) {
    $upload_key = basename($_POST['upload_key']);

    $base_path = "./storage/$upload_key/";
    echo "Accessing $base_path" . "<br>";

    if (!file_exists($base_path)) {
        echo "Your upload key cannot be found!";
    }
    else {
        $files = scandir($base_path);
        foreach ($files as $f) {
            if ($f == "." || $f == "..") {
                continue;
            }
    
            echo "File: " . $f . "<br>";
    
            $file_size = get_file_size($base_path . $f);
            echo "Old Size: " . $file_size . "<br>";
    
            $handle = fopen($base_path . $f, 'r+');
            $size_to_truncate = (int) $file_size / 2;
    
            ftruncate($handle, $size_to_truncate);
            fclose($handle);
    
            $file_size = get_file_size($base_path . $f);
            echo "New Size: " . $file_size . "<br>";
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ThanosMind: Reduce your file size by 50%.</title>
</head>

<body style="text-align: center;">
    <h3>ThanosMind: File Size Reducer.</h3>
    <form method="POST" style="text-align: left">
        <div>
            <label>Upload Key</label>
            <br>
            <input type="text" name="upload_key" placeholder="Input Upload Key" />
        </div>
        <br>
        <div>
            <br>
            <input type="submit" name="thanosed" />
        </div>
    </form>
</body>

</html>