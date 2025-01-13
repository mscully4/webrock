import base64
from io import BytesIO

from PIL import Image

WEBP_FORMAT = "webp"


def load_image(image: bytes) -> Image.Image:
    return Image.open(BytesIO(image))


def convert_image_to_base64(image: Image.Image) -> str:
    output_buffer = BytesIO()
    image.save(output_buffer, format=WEBP_FORMAT)
    return base64.b64encode(output_buffer.getvalue()).decode("utf-8")
