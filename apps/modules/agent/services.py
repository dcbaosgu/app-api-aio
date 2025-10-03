from openai import OpenAI
from anthropic import Anthropic
from .config import *


openai_client = OpenAI(api_key=OPENAI_API_KEY)
gemini_client = OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)
claude_client = Anthropic(api_key=CLAUDE_API_KEY)


class GeminiServices:
    def __init__(self, client: OpenAI):
        self.client = client

    async def generate(self, content: str, model: str, prompt: None):
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        messages.append({"role": "user", "content": content})

        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return resp.choices[0].message.content


class OpenAIServices:
    def __init__(self, client: OpenAI):
        self.client = client

    async def generate(self, content: str, model: str, prompt: None):
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        messages.append({"role": "user", "content": content})

        resp = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return resp.choices[0].message.content
    

class ClaudeServices:
    def __init__(self, client: Anthropic):
        self.client = client

    async def generate(self, content: str, model: str, prompt: None):
        messages = []
        if prompt:
            messages.append({"role": "system", "content": prompt})
        messages.append({"role": "user", "content": content})

        resp = self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": m["role"], "content": m["content"]} for m in messages]
        )
        return resp.content[0].text


gemini_services = GeminiServices(gemini_client)
openai_services = OpenAIServices(openai_client)
claude_services = ClaudeServices(claude_client)