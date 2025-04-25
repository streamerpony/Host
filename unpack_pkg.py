import struct
import hashlib

MODEL_MAP_REVERSE = {
    0: 'model_a',
    1: 'model_b',
    2: 'model_c',
}

def unpack_pkg(pkg_path):
    try:
        with open(pkg_path, 'rb') as f:
            content = f.read()

        offset = 0
        image_list = []

        while offset < len(content):
            # 图片 ID（4字节）
            img_id = struct.unpack_from('I', content, offset)[0]
            offset += 4

            # 模型类型（1字节，低2位）
            model_byte = struct.unpack_from('B', content, offset)[0]
            model_code = model_byte & 0b11
            model_name = MODEL_MAP_REVERSE.get(model_code, 'unknown_model')
            offset += 1

            # 图片数据长度（4字节）
            img_len = struct.unpack_from('I', content, offset)[0]
            offset += 4

            # 图片数据
            img_data = content[offset:offset + img_len]
            offset += img_len

            # 将图像数据保存在内存中
            image_list.append({
                "img_id": str(img_id),
                "model": model_name,
                "data": img_data
            })

        return {"success": True, "images": image_list}

    except Exception as e:
        return {"success": False, "message": str(e)}

    
def verify_pkg(pkg_path, expected_hash):
    try:
        with open(pkg_path, 'rb') as f:
            file_data = f.read()

        actual_hash = hashlib.sha256(file_data).hexdigest()

        if actual_hash != expected_hash:
            return {"success": False, "message": "哈希不一致", "expected": expected_hash, "actual": actual_hash}
        return {"success": True}

    except Exception as e:
        return {"success": False, "message": str(e)}