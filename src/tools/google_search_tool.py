import os

import requests

from src.tools.base_tool import Tool


class GoogleSearchTool(Tool):
    def name(self):
        return "Google Search Tool"

    def description(self):
        return "Performs a Google search and returns the top results. The payload is the search query."

    def use(self, query: str):
        api_key = os.getenv("SERP_API_KEY")
        search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        url = f"https://serpapi.com/search.json?q={query}&key={api_key}"
        response = requests.get(url)
        data = response.json()
        if "error" not in data:
            results = data.get("organic_results", [])
            top_results = [
                f"{result['title']}: {result['link']}" for result in results[:5]
            ]
            return "\n".join(top_results)
        else:
            return f"Error: {data.get('error', 'Unknown error')}"
