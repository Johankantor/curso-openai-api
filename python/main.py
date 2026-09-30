import os

from dotenv import load_dotenv
from openai import OpenAI

# Carga las variables del archivo .env (entre ellas,
# OPENAI_API_KEY)
load_dotenv()

# El cliente lee la API key desde las variables de
# entorno.
# Nunca escribimos la key directamente en el código.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Primera llamada usando la Responses API (la API
# principal del curso).
response = client.responses.create(
    model="gpt-4o-mini",
    input="Genera una idea corta para una campaña de lanzamiento.",
)

# output_text es la forma simple de leer el texto
# generado.
print(response.output_text)

# Imprime el desglose de métricas sobre el uso de tokens (input_tokens, output_tokens y total_tokens)
print(response.usage)