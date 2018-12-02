from __future__ import annotations
import requests
from requests.auth import HTTPBasicAuth
from dataclasses import dataclass, asdict
from mashumaro import DataClassJSONMixin


@dataclass
class Response(DataClassJSONMixin):
    statusCode: int = 200
    body: str = ''

    @classmethod
    def of(cls, status_code: int, msg: Message) -> Response:
        return Response(status_code, msg.to_json())

    def respond(self) -> dict:
        return asdict(self)


@dataclass
class Message(DataClassJSONMixin):
    message: str


def say_hello(msg: Message) -> dict:
    resp = requests.post(
        'https://httpbin.org/post',
        json=msg.to_dict(),
        auth=HTTPBasicAuth('username', 'password'),
        verify=False,
        timeout=2)
    try:
        return resp.json()['json']
    except Exception as e :
        return { 'msg': f'No body in response {e} -> {resp.text}' }


def handler(event: dict, context) -> dict:
    try:
        payload: dict = say_hello(Message("Hello World"))
        payload.update({'message': f"Received from httpbin: {payload['message']}"})
        msg: Message = Message.from_dict(payload)
        return Response.of(200, msg).respond()
    except Exception as e:
        return Response.of(500, Message(str(e))).respond()


