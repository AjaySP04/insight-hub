# chat/chat.py

from fastapi import APIRouter
from openai import OpenAI

from app.chat.models import ChatInput
from app.configs import config

import openai

# Initialize your OpenAI client using API key
client = OpenAI(
    # This is the default and can be omitted
    api_key=config.OPENAI_API_KEY,
)


router = APIRouter()

@router.post("/chat/")
async def chat_with_gpt(input_data: ChatInput):
    try:
        # Define your GPT prompt
        prompt = input_data.prompt
        # Call the new interface for GPT-3 model
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )
        return {"response": chat_completion.choices[0].text.strip()}
    except Exception as e:
        return {"error": str(e)}
