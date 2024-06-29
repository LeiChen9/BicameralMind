'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-29 20:21:42
FilePath: /Code/BicameralMind/agents/agent_manager.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

"""Agents manager."""
from utils.singleton import singleton
from utils.tools import config_parse
from .agent import Agent
from .agent_enum import AgentEnum
import os
import pdb 

@singleton
class AgentManager(object):
    """The AgentManager class, which is used to manage the agents."""

    def __init__(self, config_path):
        """Initialize the Agent manager.""" 
        self._agent_obj_map: dict[str, Agent] = {}
        self.initialize(config_path=config_path)
    
    def initialize(self, config_path):
        self.config_data = config_parse(config_path)
        if 'custom_key_path' in self.config_data['SUB_CONFIG_PATH']:
            custom_key_path = self.config_data['SUB_CONFIG_PATH']['custom_key_path']
            key, value = config_parse(custom_key_path).popitem()
            os.environ[key] = value
        for agent_type, agent_name in self.config_data['AGENTS'].items():
            assert agent_type in AgentEnum.get_list()
            self.register(agent_name, agent_type)
        self.executor = self._agent_obj_map['EXECUTOR']
        self.mentor = self._agent_obj_map['MENTOR']
        return
    
    def register(self, agent_name: str, agent_type: str):
        """Register the agent instance."""
        if agent_name in self._agent_obj_map.values():
            return
        self._agent_obj_map[agent_type] = Agent(role=agent_type, name=agent_name)

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