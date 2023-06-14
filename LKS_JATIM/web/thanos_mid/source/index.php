<?php

if ($_SERVER['REQUEST_METHOD'] == "POST" && isset($_POST['upload'])) {
    $upload_key = basename($_POST['upload_key']);

    if (!isset($_FILES["file"])) {
        die("There is no file to upload.");
    }

    $filepath = $_FILES['file']['tmp_name'];
    $fileSize = filesize($filepath);
    $fileinfo = finfo_open(FILEINFO_MIME_TYPE);
    $filetype = finfo_file($fileinfo, $filepath);

    if ($fileSize === 0) {
        die("The file is empty.");
    }

    if ($fileSize > 3145728) { 
        die("The file is too large");
    }

    $filename = basename($_FILES['file']['name']);

    $base_path = "./storage/$upload_key";
    if (!file_exists($base_path)) {
        mkdir($base_path, 0755, true);
    }

    $newFilepath = $base_path . "/" . $filename . ".fff";

    if (!copy($filepath, $newFilepath)) {
        die("Can't move file.");
    }
    unlink($filepath);

    echo "File has been uploaded to: $base_path/$filename" . "<br>";
    echo "Now go to <a href='/cutter.php'>cutter.php</a> to optimize your file(s). " . "<br>";
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
    <h3>File Uploader for ThanosMind</h3>
    <form method="POST" enctype="multipart/form-data" style="text-align: left">
        <div>
            <label>Upload Key</label>
            <br>
            <input type="text" name="upload_key" placeholder="Input Upload Key" />
        </div>
        <br>
        <div>
            <label>File</label>
            <br>
            <input type="file" name="file" />
        </div>
        <div>
            <br>
            <input type="submit" name="upload" value="Upload" />
        </div>
    </form>
</body>

</html>