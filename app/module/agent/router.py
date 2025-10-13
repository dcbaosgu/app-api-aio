from fastapi import APIRouter
from . import schema
from .controller import *

router = APIRouter(prefix="/v1/ai", tags=["AI"])

gemini_controller = GeminiController()
openai_controller = OpenAIController()
claude_controller = ClaudeController()


@router.post("/gemini", status_code=200, responses={
                200: {"model": schema.Response, "description": "Generate via Gemini"}})
async def generate_gemini(data: schema.GeminiRequest):
    result = await gemini_controller.generate(data.content, data.model, data.prompt)
    return schema.Response(generate=result)


@router.post("/openai", status_code=200, responses={
                200: {"model": schema.Response, "description": "Generate via OpenAI"}})
async def generate_openai(data: schema.OpenAIRequest):
    result = await openai_controller.generate(data.content, data.model, data.prompt)
    return schema.Response(generate=result)


@router.post("/claude", status_code=200, responses={
                200: {"model": schema.Response, "description": "Generate via Claude"}})
async def generate_claude(data: schema.ClaudeRequest):
    result = await claude_controller.generate(data.content, data.model, data.prompt)
    return schema.Response(generate=result)