'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 07:59:56
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 08:00:01
FilePath: /Code/BicameralMind/agents/agent_model.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
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