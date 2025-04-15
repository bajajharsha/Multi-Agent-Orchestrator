import sys
import os
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.base_agent import Agent
from src.tools.weather_tool import WeatherTool
from src.tools.time_tool import TimeTool
from src.tools.google_search_tool import GoogleSearchTool
from src.orchestrator import AgentOrchestrator
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Create Weather Agent
weather_agent = Agent(
    Name="Weather Agent",
    Description="Provides weather information for a given location",
    Tools=[WeatherTool()],
    Model="gpt-4o-mini"
)

# Create Time Agent
time_agent = Agent(
    Name="Time Agent",
    Description="Provides the current time for a given city",
    Tools=[TimeTool()],
    Model="gpt-4o-mini"
)

# Create Google Search Agent
google_search_agent = Agent(
    Name="Google Search Agent",
    Description="Performs Google searches and returns the top results",
    Tools=[GoogleSearchTool()],
    Model="gpt-4o-mini"
)

# Create AgentOrchestrator
agent_orchestrator = AgentOrchestrator([weather_agent, time_agent, google_search_agent])

# Run the orchestrator
if __name__ == "__main__":
    asyncio.run(agent_orchestrator.run())
