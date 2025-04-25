from ultralytics import YOLO
import cv2
import numpy as np
import io
from PIL import Image
from post_progress import post_progress

MODEL_MAP = {
    "model_a": "F:/PROJECT/model_yolo/ultralytics/runs/detect/cat_dog_v100/weights/best.pt",
    "model_b": "F:/PROJECT/model_yolo/ultralytics/runs/detect/license_v100/weights/best.pt",
    "model_c": "F:/PROJECT/model_yolo/ultralytics/runs/detect/garbage_v100/weights/best.pt"
}

def binary_to_cv2_image(binary_data):
    """二进制转OpenCV图像"""
    img = Image.open(io.BytesIO(binary_data)).convert("RGB")
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def cv2_image_to_binary(image):
    """OpenCV图像转JPEG二进制"""
    ret, buf = cv2.imencode(".jpg", image)
    return buf.tobytes() if ret else None

def inference(unpack_result):

    processed_images = []

    for item in unpack_result:
        img_id = item["img_id"]
        model_name = item["model"]
        image_data = item["data"]
        
        #发送进度
        post_progress(img_id, 'processing')

        model_path = MODEL_MAP.get(model_name)
        if not model_path:
            print(f"[警告] 未知模型: {model_name}，跳过图像 {img_id}")
            continue

        # 加载模型并推理
        model = YOLO(model_path)
        img = binary_to_cv2_image(image_data)
        results = model(img)[0]
        result_img = results.plot()

        #post_progress(img_id, 'remote_processed')

        # 转换为JPEG二进制并存入结果
        result_data = cv2_image_to_binary(result_img)
        processed_images.append({
            "img_id": img_id,
            "model": model_name,
            "data": result_data
        })

    return {"success": True, "images": processed_images}