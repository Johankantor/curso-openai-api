import json
from app.openai_client import client, brand_voice_tool, get_brand_voice

response = client.responses.create(
    model="gpt-5.4",
    input="Genera un post de LinkedIn para una campana de AI",
    tools=[brand_voice_tool],
)

tool_outputs = []

for item in response.output:
    if item.type == "function_call" and item.name == "get_brand_voice":
        result = get_brand_voice() # Ejecutamos la funcion REAL aqui

        tool_outputs.append({
           "type": "function_call_output",
           "call_id": item.call_id,
           "output": json.dumps(result),
        })

final = client.responses.create(
    model="gpt-5.4",
    input=tool_outputs,
    previous_response_id=response.id,
    tools=[brand_voice_tool],
)

print(final.output_text)
