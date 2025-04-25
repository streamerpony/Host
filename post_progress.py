import requests
from config import post_progress_API

def post_progress(img_id, stage):
    data = {
        "img_id": str(img_id),
        "stage": stage
    }
    response = requests.post(post_progress_API, json=data)

#post_progress(2, "pending")
#手动发送进度