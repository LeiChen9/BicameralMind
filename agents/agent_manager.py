'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 15:02:48
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/agents/agent_manager.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

"""Agents manager."""
from utils.singleton import singleton
from .agent import Agent
from .agent_enum import AgentEnum
import tomli, yaml
import pdb 

@singleton
class AgentManager(object):
    """The AgentManager class, which is used to manage the agents."""

    def __init__(self, config_path):
        """Initialize the Agent manager.""" 
        self._agent_obj_map: dict[str, Agent] = {}
        self.initialize(config_path=config_path)
    
    def initialize(self, config_path):
        if config_path.split(".")[-1] == 'toml':
            with open(config_path, 'rb') as f:
                config_data = tomli.load(f)
        elif config_path.split(".")[-1] == 'yaml':
            with open(config_path, 'r', encoding='utf-8') as stream:
                config_data = yaml.safe_load(stream)
        else:
            raise ValueError("Config format not supported, please use toml or yaml")
        self.config_data = config_data
        for agent_name, agent_type in config_data['AGENTS'].items():
            assert agent_type in AgentEnum.get_list()
            self.register(agent_name, agent_type)
        return
    
    def register(self, agent_name: str, agent_type: str):
        """Register the agent instance."""
        if agent_name in self._agent_obj_map:
            return
        self._agent_obj_map[agent_name] = Agent(role=agent_type)

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