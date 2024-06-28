'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 14:01:42
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/main.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''
from agents.agent_manager import AgentManager
from agents.agent import Agent 
import pdb

if __name__ == '__main__':
    manager: AgentManager = AgentManager(config_path='./config.toml')
    pdb.set_trace()