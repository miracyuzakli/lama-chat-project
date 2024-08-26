from langchain.llms.base import LLM
from typing import Optional, List
import requests
import json
from langdetect import detect

from .config import settings

class OllamaAPI(LLM):
    def __init__(self, model_name: str = f"{settings.MODEL_NAME}:{settings.MODEL_SIZE}", api_url: str = "http://localhost:11434/api/generate", temperature: float = 0.2):
        super().__init__()
        object.__setattr__(self, 'model_name', model_name)
        object.__setattr__(self, 'api_url', api_url)
        object.__setattr__(self, 'temperature', temperature)

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": self.temperature  
            }
        }
        response = requests.post(self.api_url, json=data, headers=headers, stream=True)
        
        complete_response = ""
        for line in response.iter_lines():
            if line:
                line_data = line.decode('utf-8')
                try:
                    json_line = json.loads(line_data)
                    complete_response += json_line.get("response", "")
                    if json_line.get("done", False):
                        break
                except json.JSONDecodeError:
                    print("Failed to parse line:", line_data)
                    continue

        return complete_response

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "ollama_api"