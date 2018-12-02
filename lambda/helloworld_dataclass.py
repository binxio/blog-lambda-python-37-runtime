from __future__ import annotations
import json
from dataclasses import dataclass, asdict


@dataclass
class Response:
    statusCode: int = 200
    body: str = ''

    @classmethod
    def of(cls, status_code: int, body: dict) -> Response:
        return Response(status_code, json.dumps(body))

    def respond(self) -> dict:
        return asdict(self)


def handler(event: dict, context) -> dict:
    return Response.of(200, { 'msg': 'Hello World' }).respond()
