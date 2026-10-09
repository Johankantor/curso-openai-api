import os
import base64

from dotenv import load_dotenv
from openai import OpenAI
from app.models import CampaignBrief, ContentPiece

load_dotenv()

# Un unico cliente reutilizable para todo el proyecto.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text(prompt: str) -> dict:
    """Genera texto a partir de un prompt usando la
    Responses API."""
    response = client.responses.create(
        model="gpt-5.4",
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

def generate_brief (idea: str) -> str:
    """Convierte una idea desordenada en un brief de campana (tecto libre)."""
    response = client.responses.create(
        model="gpt-5.4",
        instructions="""Convierte una ideas desordenadas en un brief claros de contenido. Incluye objetivo, audiencia, tono, canales recomendados y proximos pasos. Responde en español.""",
        input=idea,
    )
    return response.output_text



def generate_structured_brief(idea: str) -> CampaignBrief:
    """Convierte una idea desordenada en un brief de campaña estructurado."""

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
        Convierte ideas desordenadas en briefs claros de contenido.
        Incluye objetivo, audiencia, tono, canales recomendados y próximos pasos.
        Responde en español.
        """,
        input=idea,
        text_format=CampaignBrief  # Modelo de salida
    )

    return response.output_parsed


def generate_content_piece(brief: CampaignBrief, channel: str) -> ContentPiece:

    response = client.responses.parse(
        model="gpt-5.4",
        instructions="""
        Genera una pieza de contenido lista para poublicar. respeta el brief, el canal, el tono, y la audiencia.
        Responde en español.
        """,
        input=f"""
        {brief.model_dump()}

        canal:
        {channel}
        """,
        text_format=ContentPiece  # Modelo de salida
    )

    return response.output_parsed

def analyze_reference_image(image_base64: str, content_type: str) -> str:
    """Analiza una imagen de referencia (input multimodal: texto + imagen)."""
    response = client.responses.create(
        model="gpt-5.4",
        instructions="""
        Analiza esta imagen como referencia visiual para una campana.
        Describe estilo, elementos importantes, colores, tono visual y posibles usos.
        Responde en espanol.
        """,
   input=[
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "Analiza esta imagen para una campana de contenido.",
            },
            {
                "type": "input_image",
                "image_url": f"data:{content_type};base64,{image_base64}",
            },
        ],
    }
  ],
)
    return response.output_text

def generate_campaign_image(brief: CampaignBrief) -> str:
    """Genera un asset visual nuevo usando el brief como fuente del prompt."""
    prompt = f"""
    Crea una imagen promocional para esta  campana.

    titulo: {brief.title}
    Objetivo: {brief.objective}
    Audiencia: {", ".join(brief.audience)}
    Tono: {brief.tone}

    Estilo: moderno, claro, profesional y usable en redes sociales.
    """
    
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
    )
    image_bytes = base64.b64decode(result.data[0].b64_json)
    with open("output.png","wb") as f:
        f.write(image_bytes)

