import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Un unico cliente reutilizable para todo el proyecto.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text(prompt: str) -> dict:
    """Genera texto a partir de un prompt usando la
    Responses API."""
    response = client.responses.create(
        model="gpt-4o-mini",
        # instructions define el comportamiento del modelo.
        instructions="Eres un asistente experto en estrategia de contenido.",
        # input contiene la peticion del usuario.
        input=prompt,
    )

    return {
        "text": response.output_text,
        "usage": response.usage,
        "response_id": response.id,
    }

def generate_text_with_chat_completions(prompt: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {
                "role": "system",
                "content": "Eres un asistente experto en estrategia de contenido.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return completion.choices[0].message.content