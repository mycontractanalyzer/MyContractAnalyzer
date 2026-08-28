from openai import OpenAI

import config


def ask_deepseek(system_prompt: str, user_text: str, model: str | None = None) -> str:
    client = OpenAI(api_key=config.DEEPSEEK_API_KEY, base_url=config.DEEPSEEK_BASE_URL)
    response = client.chat.completions.create(
        model=model or config.MODEL_PAID,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content