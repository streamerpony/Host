import requests
from config import receive_pkg_API

def post_pkg(filename, binary_data):
    try:
        upload_url = f"{receive_pkg_API}?filename={filename}"
        headers = {'Content-Type': 'application/octet-stream'}
        response = requests.post(upload_url, data=binary_data, headers=headers)

        if response.status_code == 200:
            print("上传成功:", response.json())
        else:
            print(f"上传失败 [{response.status_code}]:", response.text)

    except Exception as e:
        print("上传异常:", str(e))
