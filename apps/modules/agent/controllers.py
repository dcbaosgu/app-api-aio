from .services import gemini_services, openai_services, claude_services


class GeminiController:
    def __init__(self):
        self.service = gemini_services

    async def generate(self, content: str, model: str, prompt: None):
        result = await self.service.generate(content, model, prompt)
        return result


class OpenAIController:
    def __init__(self):
        self.service = openai_services

    async def generate(self, content: str, model: str, prompt: None):
        result = await self.service.generate(content, model, prompt)
        return result


class ClaudeController:
    def __init__(self):
        self.service = claude_services

    async def generate(self, content: str, model: str, prompt: None):
        result = await self.service.generate(content, model, prompt)
        return result