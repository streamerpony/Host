import struct
import io
from post_progress import post_progress

def pack_processed_images(images):
    try:
        buffer = io.BytesIO()

        for image_dict in images['images']:
            img_id = int(image_dict['img_id'])
            img_data = image_dict['data']

            #发送进度
            post_progress(img_id, 'remote_processed')
            
            # 写入图片 ID（4字节）
            buffer.write(struct.pack('I', img_id))
            print(f"打包的 img_id: {img_id} -> struct.pack: {struct.pack('I', img_id)}")

            # 写入图像数据长度（4字节）+ 数据
            buffer.write(struct.pack('I', len(img_data)))
            buffer.write(img_data)

        return {"success": True, "binary_data": buffer.getvalue()}

    except Exception as e:
        return {"success": False, "message": str(e)}