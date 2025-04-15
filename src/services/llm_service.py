import httpx
from dotenv import load_dotenv
import os

load_dotenv()

class LLMService():
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_base_url = os.getenv("GROQ_BASE_URL")
        self.groq_chat_url = f"{self.groq_base_url}/chat/completions"
        self.timeout = httpx.Timeout(
                        connect=60.0,  # Time to establish a connection
                        read=300.0,    # Time to read the response
                        write=300.0,   # Time to send data
                        pool=60.0      # Time to wait for a connection from the pool
                    )

    async def groq_api_call(self, model_name, system_prompt, user_prompt, **params):

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.groq_api_key}"
        }

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **params
        }

        try:
            async with httpx.AsyncClient(verify=False) as client:
                response = await client.post(self.groq_chat_url, headers=headers, json=payload)
                response.raise_for_status()
                response_data = response.json()
                return response_data
        except httpx.HTTPStatusError as e:
            print(f"HTTP error in groq api call: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request error in groq api call: {str(e)}")
        except httpx.HTTPError as e:
            print(f"HTTP error in groq api call: {str(e)}")
        except Exception as e:
            print(f"Error in groq api call: {str(e)}")