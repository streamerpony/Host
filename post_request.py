import requests
import os
from config import post_request_API, download_pkg_API, confirm_received_API

def request_and_receive_pkg(pkg_filename=None):
    try:
        # 未传入文件名，发起打包请求
        if not pkg_filename:
            response = requests.post(post_request_API)
            if response.status_code != 200:
                return {"success": False, "message": f"打包请求失败: {response.text}"}

            data = response.json()
            pkg_filename = data.get("binary_filename")
            if not pkg_filename:
                return {"success": False, "message": "未返回 pkg 文件名"}

        # 下载 pkg 文件
        pkg_url = f"{download_pkg_API}?filename={pkg_filename}"
        pkg_response = requests.get(pkg_url)
        if pkg_response.status_code != 200:
            return {"success": False, "message": f"下载失败: {pkg_response.text}"}

        # 文件下载在根目录
        root_dir = os.path.dirname(os.path.abspath(__file__))
        downloads_dir = os.path.join(root_dir, "downloads")
        os.makedirs(downloads_dir, exist_ok=True)

        local_path = os.path.join(downloads_dir, pkg_filename)
        with open(local_path, "wb") as f:
            f.write(pkg_response.content)

        return {"success": True, "pkg_path": local_path, "pkg_filename": pkg_filename, "hash": data.get("hash")}
    
    except Exception as e:
        return {"success": False, "message": str(e)}

def confirm_received(pkg_filename):
    try:
        response = requests.post(confirm_received_API, json={"pkg_filename": pkg_filename})
        if response.status_code == 200:
            return {"success": True}
        else:
            return {"success": False, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}
