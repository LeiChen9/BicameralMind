'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 11:26:15
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-30 17:15:30
FilePath: /Code/BicameralMind/agents/agent_manager.py
Description: 

Copyright (c) 2024 by Riceball, All Rights Reserved. 
'''

"""Agents manager."""
from utils.singleton import singleton
from utils.tools import config_parse, calculate_cosine_similarity
from .agent import Agent
from .agent_enum import AgentEnum
import logging.config
import logging
from loguru import logger
import os
import pdb 

@singleton
class AgentManager(object):
    """The AgentManager class, which is used to manage the agents."""

    def __init__(self, config_path):
        """Initialize the Agent manager.""" 
        self._agent_obj_map: dict[str, Agent] = {}
        self.initialize(config_path=config_path)
        self.previous_executor_response = ""
        self.sim_threshold = 0.8
    
    def initialize(self, config_path):
        self.config_data = config_parse(config_path)
        self.setup_logging(self.config_data['SUB_CONFIG_PATH']['log_config_path'])
        
        if 'custom_key_path' in self.config_data['SUB_CONFIG_PATH']:
            custom_key_path = self.config_data['SUB_CONFIG_PATH']['custom_key_path']
            api_info = config_parse(custom_key_path).popitem()
        for agent_type, agent_name in self.config_data['AGENTS'].items():
            assert agent_type in AgentEnum.get_list()
            self.register(agent_name, agent_type, api_info=api_info)
        self.executor = self._agent_obj_map['EXECUTOR']
        self.mentor = self._agent_obj_map['MENTOR']
        return
    
    def setup_logging(self, log_config_path):
        log_config = config_parse(log_config_path)
        log_level = log_config['LOG_CONFIG']['BASIC_CONFIG']['log_level']
        log_path = log_config['LOG_CONFIG']['BASIC_CONFIG']['log_path']
        log_rotation = log_config['LOG_CONFIG']['BASIC_CONFIG']['log_rotation']
        log_retention = log_config['LOG_CONFIG']['BASIC_CONFIG']['log_retention']
        
        if not log_path:
            log_path = "./.test_log_dir/agent_manager.log"

        logger.add(
            log_path,
            level=log_level,
            rotation=log_rotation,
            retention=log_retention,
            format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        )

    def run(self, input_text="", max_iterations=3):
        """Manage multi-turn interaction between executor and mentor."""
        history = ""  # 用于存储对话历史
        previous_executor_response = ""
        mentor_response = ""
        
        for _ in range(max_iterations):
            logger.info(f"Starting iteration {_ + 1}")
            # Executor生成回答
            executor_response = self.executor.run(input_text, mentor_dictum=mentor_response)
            if executor_response is None:
                logger.error("Executor failed to generate a response.")
                return None  # 如果发生错误，则终止交互

            logger.info(f"Executor: {executor_response}")

            # Mentor评估executor的回答
            history = f"User : {input_text}\nExecutor: {executor_response}"
            mentor_response = self.mentor.run(history=history)
            if mentor_response is None:
                logger.error("Mentor failed to generate a response.")
                return None  # 如果发生错误，则终止交互
            
            logger.info(f"Mentor: {mentor_response}")

            # 更新对话历史
            history += f"Executor: {executor_response}\nMentor: {mentor_response}\n"

            # 检查是否满足终止条件
            if self.is_answer_sufficient(executor_response, previous_executor_response):
                logger.info("Answer is sufficiently similar to the previous response. Convergence achieved.")
                break
            # 更新previous_executor_response
            previous_executor_response = executor_response

            # # 准备下一轮的input_text
            # input_text = mentor_response

        return executor_response

    def is_answer_sufficient(self, current_response, previous_response):
        # 这里可以添加逻辑来判断mentor是否认为回答已经足够好
        # 例如，检查mentor_response中是否包含某些关键词或短语
        similarity = calculate_cosine_similarity(current_response, previous_response)
        # 如果相似度小于阈值，则认为回答已经足够好
        return similarity > self.sim_threshold
    
    def register(self, agent_name: str, agent_type: str, api_info=None):
        """Register the agent instance."""
        if agent_name in self._agent_obj_map.values():
            return
        self._agent_obj_map[agent_type] = Agent(role=agent_type, name=agent_name, api_info=api_info)

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