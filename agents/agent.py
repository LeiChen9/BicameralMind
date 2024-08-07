'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-07-03 16:20:57
FilePath: /SpeechDepDiag/Users/lei/Documents/Code/BicameralMind/agents/agent.py
=======
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''
from .agent_model import AgentModel
from pydantic import BaseModel
from abc import abstractmethod
from typing import Optional
from datetime import datetime
import dashscope
import os, copy
from http import HTTPStatus
from data_structures.io_object import IOObject
import pdb 

class Agent(BaseModel):
    """The parent class of all agent models, containing only attributes."""

    agent_model: Optional[AgentModel] = None
    role: Optional[str] = None
    name: Optional[str] = None
    api_info: Optional[str] = None

    def __init__(self, role: str = 'EXECUTOR', name: Optional[str] = None, api_info=None, **kwargs):
        """Initialize the AgentModel with the given keyword arguments."""
        super().__init__()
        self.role = role
        self.name = name
        self.api_configure(api_info)
    
    def api_configure(self, api_info):
        key, value = api_info
        os.environ[key] = value

    def input_keys(self) -> list:
        """Return the input keys of the Agent."""
        pass

    def output_keys(self) -> list:
        """Return the output keys of the Agent."""
        pass

    def parse_input(self, input_object: IOObject, agent_input: dict) -> dict:
        """Agent parameter parsing.

        Args:
            input_object (IOObject): input parameters passed by the user.
            agent_input (dict): agent input preparsed by the agent.
        Returns:
            dict: agent input parsed from `input_object` by the user.
        """
        pass

    def parse_result(self, planner_result: dict) -> dict:
        """Planner result parser.

        Args:
            planner_result(dict): Planner result
        Returns:
            dict: Agent result object.
        """
        pass

    def run(self, input_text="", mentor_dictum="", history=""):
        """Agent instance running entry.

        Returns:
            OutputObject: Agent execution result
        """
        if self.role == "EXECUTOR":
            messages = self.build_executor_messages(input_text, mentor_dictum)
        elif self.role == 'MENTOR':
            messages = self.build_mentor_messages(history)

        response = dashscope.Generation.call(
            dashscope.Generation.Models.qwen_turbo,
            messages=messages,
            result_format='message',  # 将返回结果格式设置为 message
            api_key=os.getenv('DASHSCOPE_API_KEY')
        )
        
        if response.status_code == HTTPStatus.OK:
            return response["output"]["choices"][0]["message"]["content"]
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return None

    def build_executor_messages(self, input_text, mentor_dictum):
        return [
            {"role": "system", "content": "You are a helpful assistant. Answer the user's question base on your knowledge. If you are not sure with the answer, response \"maybe\", don't make up anything. Based on the input text from user, and key messages in your head about previous dialog, and evaluation of your answer from your mentor, you need to provide a response.\
                                    history theme, key words, key phrases and evaluation are: " + mentor_dictum},
            {"role": "user", "content": "(Mentor whisper: " + mentor_dictum + ") " + input_text}
        ]
    
    def build_mentor_messages(self, history):
        prompt = "Do not explain what you are doing. Do not self reference. You are an expert text analyst and mentor. Please summary the theme of the dialog and extract only the most relevant keywords and key phrases from a piece of text, and evaluate how good or bad the dialog is, is there anything need to be improved. Please showcase the results in 4 list: theme, keywords, key phrases, evaluation. Please analyze the following text: "
        return [
            {"role": "system", "content": "You are a mentor of executive model. Your job is extracting, organizing, analyzing and summarizing the history information, and distill important information for executive model and make him works better."},
            {"role": "user", "content": prompt + history}
        ]

    def get_dictum(self, mentor_input: dict) -> dict:
        """Execute agent instance.

        Args:
            input_object (IOObject): input parameters passed by the user.
            agent_input (dict): agent input parsed from `input_object` by the user.

        Returns:
            dict: planner result generated by the planner execution.
        """
        result = mentor_input
        return result

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