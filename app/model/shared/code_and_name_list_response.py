from __future__ import annotations
from typing import Dict, List
from flask_restx import Model, Namespace
from marshmallow import fields

from app.model.fields import request_status


class CodeAndNameListResponse:

    def __init__(
        self,
        *,
        data: List[Dict[str, str]],
    ) -> None:
        self.data = data

    def encode(self):
        return {
            "status": "ok",
            "data": self.data
        }

    @staticmethod
    def model(ns: Namespace) -> Model:
        return ns.model(
            "CodeAndNameListResponse",
            {
                "status": fields.String(
                    metadata=request_status,
                    required=True,
                ),
                "data": fields.List(
                    fields.Dict(
                        code=fields.String(),
                        name=fields.String(),
                    )
                )
            }
        )
