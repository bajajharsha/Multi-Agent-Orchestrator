import sys
from colorama import Fore, Style

from src.agents.base_agent import Agent
from src.utils.json_parser import json_parser
from src.prompts.orchestrator_prompt import USER_PROMPT, SYSTEM_PROMPT
from src.services.llm_service import LLMService

class AgentOrchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = agents
        self.memory = []
        self.max_memory = 10
        self.llm_service = LLMService()
        
    async def orchestrate_task(self, user_input: str):
        self.memory = self.memory[-self.max_memory:]
        context = "\n".join(self.memory)
    
        response_format = {"action":"", "input":"", "next_action":"", "reasoning": ""}
        
        response = ""
        loop_count = 0
        self.memory = self.memory[-10:]
        
        user_prompt = USER_PROMPT.format(
            context=context,
            agents_description="\n".join([f"{agent.name}: {agent.description}" for agent in self.agents]),
            user_input=user_input,
            response_format=response_format
        )
        
        response = await self.llm_service.groq_api_call(
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        
        res = response['choices'][0]['message']['content']

                
        llm_response = json_parser(input_string=res)
        self.memory.append(f"Orchestrator: {llm_response}")
        
        print(f"{Fore.LIGHTCYAN_EX}Parsed Orchestrator Response: {llm_response} {Style.RESET_ALL}")
        
        action = llm_response.get("action")
        user_input = llm_response.get("input")
                
        if action == "respond_to_user":
            return llm_response
        
        for agent in self.agents:
            if agent.name.lower() == action.lower():
                print(f"{Fore.LIGHTMAGENTA_EX}*******************Found Agent Name :: {action} *******************************")
                agent_response = await agent.process_input(user_input)
                self.memory.append(f"Agent for Task: {agent_response}")
                return agent_response  
        
    async def run(self):
        print(f"{Fore.CYAN}LLM Agent: Hello! How can I assist you today?{Style.RESET_ALL}")
        user_input = input(f"{Fore.YELLOW}You: {Style.RESET_ALL}")
        self.memory.append(f"User: {user_input}")

        while True:
            if user_input.lower() in ["exit", "bye", "close"]:
                print(f"{Fore.CYAN}LLM Agent: Goodbye!{Style.RESET_ALL}")
                break

            response = await self.orchestrate_task(user_input)

            print(f"{Fore.MAGENTA}Final response: {response}{Style.RESET_ALL}")

            if isinstance(response, dict) and response["action"] == "respond_to_user":                
                print(f"{Fore.GREEN}Final response: {response['input']}{Style.RESET_ALL}")
                user_input = input(f"{Fore.YELLOW}You: {Style.RESET_ALL}") 
                self.memory.append(f"User: {user_input}")                
            elif response == "No action or agent needed":
                print(f"{Fore.MAGENTA}Response from Agent: {response}{Style.RESET_ALL}")
                user_input = input(f"{Fore.YELLOW}You: {Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Final Agent Response: {response}{Style.RESET_ALL}")
                user_input = response
                

