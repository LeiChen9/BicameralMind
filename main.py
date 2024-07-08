'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-30 14:25:28
FilePath: /Code/BicameralMind/main.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''
from agents.agent_manager import AgentManager
from agents.agent import Agent 
import pdb

if __name__ == '__main__':
    manager: AgentManager = AgentManager(config_path='./config.toml')
    input_text = "给我介绍一下GLy-P1这款药物"
    # mentor_ideas = ""
    # response = manager.executor.run(input_text=input_text)
    # print("Chat said: ", response)
    # history = {
    #     'role': "user", "content": input_text,
    #     'role': "executive model", "contenct": response}
    # mentor_ideas = manager.mentor.run(history=str(history))
    # print("Mentor thought: ,", mentor_ideas)
    print(manager.run(input_text=input_text))