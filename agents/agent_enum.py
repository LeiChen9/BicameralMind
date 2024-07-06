'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 14:33:27
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 14:34:39
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/agents/agent_enum.py
Description: Agent Enum, make sure no out of boarder situation

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

from enum import Enum 

class AgentEnum(Enum):
    MENTOR = "MENTOR"
    EXECUTOR = "EXECUTOR"
    
    @staticmethod
    def get_list():
        return [item.value for item in AgentEnum]