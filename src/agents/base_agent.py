from src.prompts.agent_prompt import AGENT_PROMPT, SYSTEM_PROMPT
from src.services.llm_service import LLMService
from src.utils.json_parser import json_parser
from abc import ABC, abstractmethod
import ast
import os
from colorama import Fore, Style
import json

class Agent:
    def __init__(self, Name: str, Description: str, Tools: list, Model: str):
        self.memory = []
        self.name = Name
        self.description = Description
        self.tools = Tools
        self.model = Model
        self.max_memory = 10
        self.llm_service = LLMService()
        
    async def process_input(self, user_input: str):
        self.memory.append(f"User: {user_input}")
        
        context = "\n".join(self.memory)
        # tool_descriptions = "\n".join(f"- {tool['name']}: {tool['description']}" for tool in self.tools)
        tool_descriptions = "\n".join(f"- {tool.name()}: {tool.description()}" for tool in self.tools)

        
        response_format = {"action": "","args": "", "reasoning": ""}
        
        user_prompt = AGENT_PROMPT.format(
            context=context,
            user_input=user_input,
            tool_descriptions=tool_descriptions,
            response_format=response_format
        )
        
        response = await self.llm_service.groq_api_call(
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            # model_name="llama-3.3-70b-versatile",
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt
        )
        
        
        res = response['choices'][0]['message']['content']
        
        self.memory.append(f"Agent: {res}")

        response_dict = json_parser(res)
        
        print(f"{Fore.LIGHTCYAN_EX}Parsed Response: {response_dict} {Style.RESET_ALL}")
        
        # Check if any tool can handle the input
        for tool in self.tools:
            if tool.name().lower() == response_dict["action"].lower():
                return tool.use(response_dict["args"])

        return response_dict
        
