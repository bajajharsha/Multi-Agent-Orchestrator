import os
import json
import requests

from src.tools.base_tool import Tool


class GoogleSearchTool(Tool):
    def name(self):
        return "Google Search Tool"

    def description(self):
        return "Performs a Google search and returns the top results. The payload is the search query."

    def use(self, query: str):
        api_key = os.getenv("SERPER_DEV_API_KEY")
        url = "https://google.serper.dev/search"
        
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'q': query,
            'engine': 'google'
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code != 200:
            return f"Error: Failed to get results (Status code: {response.status_code})"
        
        data = response.json()
        results = []
        
        # Extract answer box if present
        if "answerBox" in data:
            answer_box = data["answerBox"]
            results.append(f"Search Result: {answer_box}" )
        elif "organic" in data:
            results.append("SEARCH RESULTS:")
            for i, result in enumerate(data["organic"][:2], 1):
                results.append(f"   {result.get('snippet', '')}")
        
        # If no results found
        if not results:
            return "No search results found."
        
        return "\n".join(results)