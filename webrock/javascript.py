from os import PathLike
from typing import Any

_JS_TAG_UTILS = "./dist/webrock-js/main.min.js"


def load_js(path: PathLike[Any]) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError as e:
        raise ValueError(
            "Could not find tag_utils.js. Please ensure that you complied typescript using `npm run build`"
        ) from e
