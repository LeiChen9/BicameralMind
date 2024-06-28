'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 13:41:31
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/agents/agent_manager.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

"""Agents manager."""
from utils import singleton
from agent import Agent

@singleton
class AgentManager():
    """The AgentManager class, which is used to manage the agents."""

    def __init__(self):
        """Initialize the Agent manager.""" 
        self._agent_obj_map: dict[str, Agent] = {}
    
    def register(self, agent_name: str, agent_obj: Agent):
        """Register the agent instance."""
        if agent_name in self._agent_obj_map:
            return
        self._agent_obj_map[agent_name] = agent_obj

    def unregister(self, agent_name: str):
        """Unregister the agent instance."""
        if agent_name not in self._agent_obj_map:
            return
        del self._agent_obj_map[agent_name]

    def get_instance_obj(self, agent_name: str,
                         appname: str = None, new_instance: bool = None) -> Agent:
        """Return the agent instance object."""
        if agent_name not in self._agent_obj_map:
            raise Exception(f"Agent {agent_name} not found.")
        return self._agent_obj_map[agent_name]

    def get_agent_name_list(self) -> list:
        """Return the agent instance list."""
        return list(self._agent_obj_map.keys())

    def get_agent_obj_list(self) -> list:
        """Return the agent instance object list."""
        return list(self._agent_obj_map.values())