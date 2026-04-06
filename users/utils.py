import os
from django.conf import settings
from PIL import Image
import io
import uuid
from django.core.files.base import ContentFile

def compress_image(image_field, size=(800,800), quality=85):
    image = Image.open(image_field).convert('RGB')

    image.thumbnail(size, Image.LANCZOS)

    uid = str(uuid.uuid4())[:10]
    image_name=f'{uid}.webp'

    output = io.BytesIO()

    image.save(output, format='WEBP', quality=quality)

    output.seek(0)

    optimized_image = ContentFile(output.getvalue())

    return optimized_image, image_name

def save_custom_image(image, size, folder):
    optimized_image, image_name = compress_image(image, size)
    path = os.path.join(folder,image_name)
    full_path = os.path.join(settings.IMAGES_ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "wb") as f:
        f.write(optimized_image.read())
    return image_name