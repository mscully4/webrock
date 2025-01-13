import base64
from io import BytesIO

from PIL import Image

WEBP_FORMAT = "webp"


def convert_image_to_base64(image: bytes) -> str:
    img = Image.open(BytesIO(image))
    output_buffer = BytesIO()
    img.save(output_buffer, format=WEBP_FORMAT)
    return base64.b64encode(output_buffer.getvalue()).decode("utf-8")
