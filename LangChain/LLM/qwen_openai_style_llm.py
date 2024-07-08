'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-07-04 14:49:03
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-04 14:49:11
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/LangChain/LLM/qwen_openai_style_llm.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''
from typing import Optional, Any, Union, Iterator, AsyncIterator

from dashscope import get_tokenizer
from pydantic import Field
import os

from llm_output import LLMOutput
from openai_style_llm import OpenAIStyleLLM

def get_from_env(env_key: str) -> str:
    if env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]

QWen_Max_CONTEXT_LENGTH = {
    "qwen-turbo": 6000,
    "qwen-plus": 300000,
    "qwen-max": 6000,
    "qwen-max-0428": 6000,
    "qwen-max-0403": 6000,
    "qwen-max-0107": 6000,
    "qwen-max-longcontext": 28000
}


class QWenOpenAIStyleLLM(OpenAIStyleLLM):
    """
        QWen OpenAI style LLM
        Args:
            api_key: API key for the model ,from dashscope : DASHSCOPE_API_KEY
            api_base: API base URL for the model, from dashscope : DASHSCOPE_API_BASE
    """

    api_key: Optional[str] = Field(default_factory=lambda: get_from_env("DASHSCOPE_API_KEY"))
    api_base: Optional[str] = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    proxy: Optional[str] = Field(default_factory=lambda: get_from_env("DASHSCOPE_PROXY"))
    organization: Optional[str] = Field(default_factory=lambda: get_from_env("DASHSCOPE_ORGANIZATION"))

    def call(self, messages: list, **kwargs: Any) -> Union[LLMOutput, Iterator[LLMOutput]]:
        """ The call method of the LLM.

        Users can customize how the model interacts by overriding call method of the LLM class.

        Args:
            messages (list): The messages to send to the LLM.
            **kwargs: Arbitrary keyword arguments.
        """
        return super().call(messages, **kwargs)

    async def acall(self, messages: list, **kwargs: Any) -> Union[LLMOutput, AsyncIterator[LLMOutput]]:
        """ The async call method of the LLM.

        Users can customize how the model interacts by overriding acall method of the LLM class.

        Args:
            messages (list): The messages to send to the LLM.
            **kwargs: Arbitrary keyword arguments.
        """
        return await super().acall(messages, **kwargs)

    def max_context_length(self) -> int:
        if super().max_context_length():
            return super().max_context_length()
        return QWen_Max_CONTEXT_LENGTH.get(self.model_name, 8000)

    def get_num_tokens(self, text: str) -> int:
        tokenizer = get_tokenizer(self.model_name)
        return len(tokenizer.encode(text))