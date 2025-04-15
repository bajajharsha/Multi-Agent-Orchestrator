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
        
        print(f"Context: {context}")

        response_format = {"action":"", "input":"", "next_action":""}
        
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
            user_prompt=user_prompt
        )
        
        res = response['choices'][0]['message']['content']

                
        llm_response = json_parser(input_string=res)
        self.memory.append(f"Orchestrator: {llm_response}")
        
        action = llm_response.get("action")
        user_input = llm_response.get("input")
        
        print(f"Action identified by LLM: {action}")
        
        if action == "respond_to_user":
            return llm_response
        
        for agent in self.agents:
            if agent.name.lower() == action.lower():
                print(f"*******************Found Agent Name :: {action} *******************************")
                agent_response = await agent.process_input(user_input)
                print(f"{action} response: {agent_response}")
                self.memory.append(f"Agent Response for Task: {agent_response}")
                print(self.memory)
                return agent_response  
        
    async def run(self):
        print("LLM Agent: Hello! How can I assist you today?")
        user_input = input("You: ")
        self.memory.append(f"User: {user_input}")
        
        while True:
            if user_input.lower() in ["exit", "bye", "close"]:
                print("LLM Agent: Goodbye!")
                break
            
            response = await self.orchestrate_task(user_input)
            
            print(f"Final response of orchestrator {response}")
            
            if isinstance(response, dict) and response["action"] == "respond_to_user":                
                # print(f"Reponse from Agent: {response['input']}")
                user_input = input("You: ") 
                self.memory.append(f"User: {user_input}")                
            elif response == "No action or agent needed":
                print("Reponse from Agent: ", response)
                user_input = input("You: ")
            else:
                user_input = response  
            
