'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 08:07:32
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-04 16:45:15
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/data_structures/io_object.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''

import json
import datetime
from typing import Any, Dict, List, Optional, Set, Union
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field, HttpUrl, SecretStr

class IOObject(object):
    def __init__(self, params: dict):
        self.__params = params
        for k, v in params.items():
            self.__dict__[k] = v

    def to_dict(self):
        return self.__params

    def to_json_str(self):
        return json.dumps(self.__params)

    def add_data(self, key, value):
        self.__params[key] = value
        self.__dict__[key] = value

    def get_data(self, key, default=None):
        return self.__params.get(key, default)

def orjson_dumps(v, *, default, **kwargs):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, **kwargs).decode()


def now_tz():
    # Need datetime w/ timezone for cleanliness
    # https://stackoverflow.com/a/24666683
    return datetime.datetime.now(datetime.timezone.utc)

class ChatMessage(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[str] = None
    received_at: datetime.datetime = Field(default_factory=now_tz)
    finish_reason: Optional[str] = None
    prompt_length: Optional[int] = None
    completion_length: Optional[int] = None
    total_length: Optional[int] = None

    def __str__(self) -> str:
        return str(self.model_dump(exclude_none=True))

class ChatSession(BaseModel):
    id: Union[str, UUID] = Field(default_factory=uuid4)
    created_at: datetime.datetime = Field(default_factory=now_tz)
    auth: Dict[str, SecretStr]
    api_url: HttpUrl
    model: str
    system: str
    params: Dict[str, Any] = {}
    messages: List[ChatMessage] = []
    input_fields: Set[str] = {}
    recent_messages: Optional[int] = None
    save_messages: Optional[bool] = True
    total_prompt_length: int = 0
    total_completion_length: int = 0
    total_length: int = 0
    title: Optional[str] = None

    def __str__(self) -> str:
        sess_start_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        last_message_str = self.messages[-1].received_at.strftime("%Y-%m-%d %H:%M:%S")
        return f"""Chat session started at {sess_start_str}:
        - {len(self.messages):,} Messages
        - Last message sent at {last_message_str}"""

    def format_input_messages(
        self, system_message: ChatMessage, user_message: ChatMessage
    ) -> list:
        recent_messages = (
            self.messages[-self.recent_messages :]
            if self.recent_messages
            else self.messages
        )
        return (
            [system_message.model_dump(include=self.input_fields, exclude_none=True)]
            + [
                m.model_dump(include=self.input_fields, exclude_none=True)
                for m in recent_messages
            ]
            + [user_message.model_dump(include=self.input_fields, exclude_none=True)]
        )

    def add_messages(
        self,
        user_message: ChatMessage,
        assistant_message: ChatMessage,
        save_messages: bool = None,
    ) -> None:
        # if save_messages is explicitly defined, always use that choice
        # instead of the default
        to_save = isinstance(save_messages, bool)

        if to_save:
            if save_messages:
                self.messages.append(user_message)
                self.messages.append(assistant_message)
        elif self.save_messages:
            self.messages.append(user_message)
            self.messages.append(assistant_message)