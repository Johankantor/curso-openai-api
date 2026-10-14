from app.openai_client import client
from app.safe_client import safe_openai_call

#Envolvemos la llamada para ue intente ante errores transitorios.

result = safe_openai_call(lambda: client.responses.create(
    model="gpt-5.4",
    input="Genera una campaña corta.",
))

print(result.output_text)
