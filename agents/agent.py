'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-27 22:05:41
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 08:12:56
FilePath: /Code/BicameralMind/agents/agent.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
from agent_model import AgentModel
from pydantic import BaseModel
from abc import abstractmethod
from typing import Optional
from datetime import datetime
from data_structures.io_object import IOObject

class Agent(BaseModel):
    """The parent class of all agent models, containing only attributes."""

    agent_model: Optional[AgentModel] = None

    def __init__(self, name: str = 'default', **kwargs):
        """Initialize the AgentModel with the given keyword arguments."""
        super().__init__()
        self.name = name

    @abstractmethod
    def input_keys(self) -> list[str]:
        """Return the input keys of the Agent."""
        pass

    @abstractmethod
    def output_keys(self) -> list[str]:
        """Return the output keys of the Agent."""
        pass

    @abstractmethod
    def parse_input(self, input_object: IOObject, agent_input: dict) -> dict:
        """Agent parameter parsing.

        Args:
            input_object (IOObject): input parameters passed by the user.
            agent_input (dict): agent input preparsed by the agent.
        Returns:
            dict: agent input parsed from `input_object` by the user.
        """
        pass

    @abstractmethod
    def parse_result(self, planner_result: dict) -> dict:
        """Planner result parser.

        Args:
            planner_result(dict): Planner result
        Returns:
            dict: Agent result object.
        """
        pass

    def run(self, **kwargs) -> IOObject:
        """Agent instance running entry.

        Returns:
            OutputObject: Agent execution result
        """
        self.input_check(kwargs)
        input_object = IOObject(kwargs)

        agent_input = self.pre_parse_input(input_object)

        planner_result = self.execute(input_object, agent_input)

        agent_result = self.parse_result(planner_result)

        self.output_check(agent_result)
        output_object = IOObject(agent_result)
        return output_object

    def execute(self, input_object: IOObject, agent_input: dict) -> dict:
        """Execute agent instance.

        Args:
            input_object (IOObject): input parameters passed by the user.
            agent_input (dict): agent input parsed from `input_object` by the user.

        Returns:
            dict: planner result generated by the planner execution.
        """

        planner_base: Planner = PlannerManager().get_instance_obj(self.agent_model.plan.get('planner').get('name'))
        planner_result = planner_base.invoke(self.agent_model, agent_input, input_object)
        return planner_result

    def pre_parse_input(self, input_object) -> dict:
        """Agent execution parameter pre-parsing.

        Args:
            input_object (IOObject): input parameters passed by the user.
        Returns:
            dict: agent input preparsed by the agent.
        """
        agent_input = dict()
        agent_input['chat_history'] = input_object.get_data('chat_history') or ''
        agent_input['background'] = input_object.get_data('background') or ''
        agent_input['image_urls'] = input_object.get_data('image_urls') or []
        agent_input['date'] = datetime.now().strftime('%Y-%m-%d')

        self.parse_input(input_object, agent_input)
        return agent_input

    def input_check(self, kwargs: dict):
        """Agent parameter check."""
        for key in self.input_keys():
            if key not in kwargs.keys():
                raise Exception(f'Input must have key: {key}.')

    def output_check(self, kwargs: dict):
        """Agent result check."""
        if not isinstance(kwargs, dict):
            raise Exception('Output type must be dict.')
        for key in self.output_keys():
            if key not in kwargs.keys():
                raise Exception(f'Output must have key: {key}.')