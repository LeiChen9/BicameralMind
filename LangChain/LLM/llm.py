'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-07-04 14:36:34
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-04 14:39:20
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/LangChain/LLM/llm.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''
from abc import abstractmethod
from typing import Optional, Any, AsyncIterator, Iterator, Union

class LLM:
    """The basic class for llm model.

    Attributes:
        client (Any): The client of the llm.
        async_client (Any): The async client of the llm.
        name (Optional[str]): The name of the llm class.
        description (Optional[str]): The description of the llm model.
        model_name (Optional[str]): The name of the llm model, such as gpt-4, gpt-3.5-turbo.
        temperature (Optional[float]): The temperature of the llm model,
        what sampling temperature to use, between 0 and 2.
        request_timeout (Optional[int]): The request timeout for chat http requests.
        max_tokens (Optional[int]): The maximum number of [tokens](/tokenizer) that can be generated in the completion.
        streaming (Optional[bool]): Whether to stream the results or not.
        ext_info (Optional[dict]): The extended information of the llm model.
    """

    client: Any = None
    async_client: Any = None
    name: Optional[str] = None
    description: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = 0.5
    request_timeout: Optional[int] = None
    max_tokens: Optional[int] = 1024
    max_retries: Optional[int] = 2
    streaming: Optional[bool] = False
    ext_info: Optional[dict] = None
    tracing: Optional[bool] = None
    _max_context_length: Optional[int] = None

    def __init__(self, **kwargs):
        """Initialize the llm."""
        super().__init__(**kwargs)

    def _new_client(self):
        """Initialize the client."""
        pass

    def _new_async_client(self):
        """Initialize the async client."""
        pass

    @abstractmethod
    def call(self, *args: Any, **kwargs: Any):
        """Run the LLM."""

    @abstractmethod
    async def acall(self, *args: Any, **kwargs: Any):
        """Asynchronously run the LLM."""

    def as_langchain(self):
        """Convert to the langchain llm class."""
        pass

    def set_by_agent_model(self, **kwargs) -> None:
        """ Assign values of parameters to the LLM model in the agent configuration."""
        if 'model_name' in kwargs and kwargs['model_name']:
            self.model_name = kwargs['model_name']
        if 'temperature' in kwargs and kwargs['temperature']:
            self.temperature = kwargs['temperature']
        if 'request_timeout' in kwargs and kwargs['request_timeout']:
            self.request_timeout = kwargs['request_timeout']
        if 'max_tokens' in kwargs and kwargs['max_tokens']:
            self.max_tokens = kwargs['max_tokens']
        if 'max_retries' in kwargs and kwargs['max_retries']:
            self.max_retries = kwargs['max_retries']
        if 'streaming' in kwargs and kwargs['streaming']:
            self.streaming = kwargs['streaming']
        if 'max_context_length' in kwargs and kwargs['max_context_length']:
            self._max_context_length = kwargs['max_context_length']

    def max_context_length(self) -> int:
        """Max context length.

        The total length of input tokens and generated tokens is limited by the model's context length.
        """
        return self._max_context_length

    @abstractmethod
    def get_num_tokens(self, text: str) -> int:
        """Get the number of tokens present in the text.

        Useful for checking if an input will fit in a model's context window.

        Args:
            text: The string input to tokenize.

        Returns:
            The integer number of tokens in the text.
        """