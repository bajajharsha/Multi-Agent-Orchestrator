# Multi-Agent-Orchestrator

## Overview

This is a modular system designed to handle user requests by orchestrating specialized agents. Each agent is equipped with tools to perform specific tasks, such as fetching weather information, performing Google searches, or providing the current time for a given timezone.

The system uses a Large Language Model (LLM) to classify intents, select the appropriate agent, and generate structured responses. The framework is built with Python and leverages APIs for external services.

## Features

- **Agent-Oriented Design**: Specialized agents for tasks like weather, time, and Google search.
- **Tool Integration**: Tools are modular and reusable, enabling agents to perform specific tasks.
- **LLM-Powered Orchestration**: Uses LLM to classify intents and route tasks to the appropriate agent.
- **Extensible**: Easily add new agents and tools to expand functionality.
- **Structured Responses**: Ensures all responses are in a structured JSON format for programmatic use.

## Project Structure

```
AGENTS/
├── requirements.txt          # Project dependencies
├── src/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Entry point for the application
│   ├── orchestrator.py       # Orchestrates tasks between agents
│   ├── agents/
│   │   └── base_agent.py     # Base class for all agents
│   ├── prompts/
│   │   ├── agent_prompt.py   # Prompts for individual agents
│   │   └── orchestrator_prompt.py # Prompts for the orchestrator
│   ├── services/
│   │   └── llm_service.py    # Handles LLM API calls
│   ├── tools/
│   │   ├── base_tool.py      # Base class for all tools
│   │   ├── google_search_tool.py # Tool for Google search
│   │   ├── time_tool.py      # Tool for fetching current time
│   │   └── weather_tool.py   # Tool for fetching weather information
│   └── utils/
│       └── json_parser.py    # Utility for parsing JSON responses
└── .gitignore                # Git ignore file
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AGENTS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add the following keys:
     ```
     SERPER_DEV_API_KEY=<Your Serper API Key>
     OPENWEATHERMAP_API_KEY=<Your OpenWeatherMap API Key>
     GROQ_API_KEY=<Your Groq API Key>
     GROQ_BASE_URL=<Your Groq Base URL>
     ```

## Usage

1. Run the application:
   ```bash
   python src/main.py
   ```

2. Interact with the system:
   - Provide user input to request tasks like weather information, current time, or Google search results.
   - Type "exit" to terminate the application.

## Agents and Tools

### Agents
- **Weather Agent**: Provides weather information for a given location.
- **Time Agent**: Provides the current time for a given timezone.
- **Google Search Agent**: Performs Google searches and returns the top results.

### Tools
- **Weather Tool**: Fetches weather data using the OpenWeatherMap API.
- **Time Tool**: Fetches the current time for a given timezone using `pytz`.
- **Google Search Tool**: Performs Google searches using the Serper API.

## Extending the Framework

### Adding a New Tool
1. Create a new tool class in `src/tools/` that inherits from `Tool`.
2. Implement the `name`, `description`, and `use` methods.

### Adding a New Agent
1. Create a new agent in `src/agents/` that inherits from `Agent`.
2. Define the agent's name, description, tools, and model in `src/main.py`.

## Dependencies

- Python 3.8+
- `dotenv`
- `httpx`
- `pytz`
- `requests`
- `python-dotenv`
- `streamlit>=1.25.0`
