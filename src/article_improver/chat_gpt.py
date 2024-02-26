import tiktoken
from openai import AsyncOpenAI
from loguru import logger
import json


MODEL_GPT_4 = "gpt-4-turbo-preview"
MODEL_GPT_3 = "gpt-3.5-turbo"

MAX_TOKENS = {MODEL_GPT_3: 4096, MODEL_GPT_4: 128000}


class ChatGpt:
    def __init__(self, client: AsyncOpenAI, temperature: float = 0.5):
        self.client = client
        self.temperature = temperature

    async def get_completion(self, prompt: str, content: str, model: str) -> str:
        try:
            messages = self.create_messages(prompt, content, model)

            response = await self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=self.temperature,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.bind(prompt=prompt, content=content, error=e).error(
                "can't get ChatGPT response"
            )
            raise e

    def create_messages(
        self, prompt: str, content: str, model: str
    ) -> list[dict[str, str]]:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "''''''"},
        ]
        messages_str = json.dumps(messages)
        tokenizer = tiktoken.encoding_for_model(model)
        token_integers = tokenizer.encode(content)
        remaining = MAX_TOKENS[model] - len(tokenizer.encode(messages_str))
        user_content = tokenizer.decode(token_integers[:remaining])

        messages[-1]["content"] = f"'''{user_content}'''"

        return messages
