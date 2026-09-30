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