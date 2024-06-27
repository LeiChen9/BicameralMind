'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-27 21:57:01
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-27 22:06:25
FilePath: /Code/BicameralMind/agents/agent_manager.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
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
    
    def register(self, component_instance_name: str, component_instance_obj: ComponentTypeVar):
        """Register the component instance."""
        pass

    def unregister(self, component_instance_name: str):
        """Unregister the component instance abstractmethod."""
        pass

    def get_instance_obj(self, component_instance_name: str,
                         appname: str = None, new_instance: bool = None) -> ComponentTypeVar:
        """Return the component instance object."""
        pass

    def get_instance_name_list(self) -> list[str]:
        """Return the component instance list."""
        pass

    def get_instance_obj_list(self) -> list[ComponentTypeVar]:
        """Return the component instance object list."""
        pass