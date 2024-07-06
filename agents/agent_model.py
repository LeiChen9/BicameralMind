'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 13:41:58
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/agents/agent_model.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

"""Agent model class."""
from typing import Optional
from pydantic import BaseModel


class AgentModel(BaseModel):
    """The parent class of all agent models, containing only attributes."""

    info: Optional[dict] = dict()
    profile: Optional[dict] = dict()
    plan: Optional[dict] = dict()
    memory: Optional[dict] = dict()
    action: Optional[dict] = dict()