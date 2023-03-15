from typing import Any

from flask import json


class ModelEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if hasattr(o, "encode"):
            return o.encode()
        else:
            return super().default(o)
