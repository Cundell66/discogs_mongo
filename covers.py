import base64
from PIL import Image
import requests
from pymongo_get_database import get_database
import io

def insert_image(release_id, cover_image):
    # get release id and cover_image url
    db = get_database()
    covers = db["covers"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like

    response = requests.get(cover_image, headers = headers)
    cover = response.content
    image_id = covers.insert_one({
        "release_id": release_id,
        "cover": cover
        }).inserted_id
    print(image_id)

def show_images(cover):
    img = Image.open(io.BytesIO(cover['cover']))
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Base64 encoding
    return img_base64
