from post_request import request_and_receive_pkg, confirm_received
from unpack_pkg import unpack_pkg, verify_pkg
import time

def main():
    while True:
        result = request_and_receive_pkg()
        if not result["success"]:
            print("错误：", result["message"])
            time.sleep(5)
            continue

        pkg_filename = result["pkg_filename"]
        expected_hash = result["hash"]
        print(f"接收到 pkg: {pkg_filename}，期望哈希: {expected_hash}")

        local_path = result["pkg_path"]
        while not verify_pkg(local_path, expected_hash)["success"]:
                    for attempt in range(2):
                        print(f"哈希校验失败，尝试重新下载（第{attempt+1}次）")
                        retry_result = request_and_receive_pkg(pkg_filename)
                        if not retry_result["success"]:
                            print(f"下载失败（重试第{attempt+1}次）：{retry_result['message']}")
                            time.sleep(2)
                            continue
                        print(f"网络波动，文件校验出错，重新下载 pkg: {pkg_filename}")
                        continue
        
        print("哈希校验通过，开始解包")
        unpack_result = unpack_pkg(local_path)
        if unpack_result["success"]:
            for img in unpack_result["images"]:
                print(f"已解包图像：{img['img_id']}，模型：{img['model']}，保存路径：{img['path']}")
            confirm_received(pkg_filename)
            continue
        else:
            print("解包失败：", unpack_result["message"])
            continue


if __name__ == "__main__":
    main()