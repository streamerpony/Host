from post_request import request_and_receive_pkg
from unpack_pkg import unpack_pkg, verify_pkg
from inference import inference
from pack_pkg import pack_processed_images
from post_progress import post_progress
from post_pkg import post_pkg
import time

def main():
    while True:
        result = request_and_receive_pkg()
        if not result["success"]:
            print(result["message"])
            time.sleep(10)
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

            images = unpack_result["images"]
            #向服务器发送接收确认
            for img in images:
                post_progress(img["img_id"],'remote_received')

            #调用 inference 函数处理图像
            print("开始模型推理...")
            processed_images = inference(images)  # 传入解包后的 images 列表

            #重新打包为二进制文件
            print("开始重新打包为二进制文件")
            pack_result = pack_processed_images(processed_images)
            result = post_pkg(pkg_filename,pack_result["binary_data"])
        else:
            print("解包失败:", unpack_result["message"])
            continue
        time.sleep(2)



if __name__ == "__main__":
    main()