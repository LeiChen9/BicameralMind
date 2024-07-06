'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-07-04 14:41:51
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-04 14:41:54
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/LangChain/LLM/llm_output.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''
from typing import Any

from pydantic import BaseModel

class LLMOutput(BaseModel):
    """The basic class for llm output."""

    """The text of the llm output."""
    text: str

    """The raw data of the llm output."""
    raw: Any