import json
import time

from app.openai_client import client

stable_instructions = """
Eres el generador oficial del contenido de la marca "Mi Marca".
Susa siempre un tono cercano, claro, educativo y profesional.
Evita hype exagerado y promesas irreales.
"""

def generate_with_cache(prompt: str) -> str:
    """llamada normal, pero con instrucciones estables al inicio (cacheables)."""
    response = client.responses.create(
        model="gpt-5.4",
        instructions=stable_instructions,
        input=prompt,
    )
    
    return response.output_text

#batchAPI

def build_batch_file(ideas: list[str], path: str = "batch/requests.jsonl") -> str:
    """Construye un archivo JSONL con una linea por request."""
    with open(path, "w", encoding="utf-8") as file:
        for index, idea in enumerate(ideas, start=1):
            line = {
                "custom_id": f"req-{index}",
                "method": "POST",
                "url": "/v1/responses",
                "body": {
                    "model": "gpt-5.4-mini",
                    "input": f"Clasifica esta idea por canal recomendado {idea}",
                }
            }
            file.write(json.dumps(line, ensure_ascii=False) + "\n")
    return path

def submit_batch(path: str = "batch/requests.jsonl"):
    """Sube el JSONL y crea el batch. luego se consulat estado y se descargan los resultados (no es inmediato)."""
    batch_file = client.files.create(file=open(path, "rb"), purpose="batch")
    
    batch = client.batches.create(
            input_file_id=batch_file.id,
            endpoint="/v1/responses",
            completion_window="24h",
        )
    return batch

def save_batch_results(batch_id: str, output_path: str = "batch/results.txt") -> str:
    """Espera a que el batch se complete y descarga los resultados en un archivo de texto."""
    # 1) Consultamos el esta cada 10s hasta que el batch deje de procesar.
    batch = client.batches.retrieve(batch_id)
    while batch.status in ("validating", "in_progress", "finalizing"):
        print(f"Estado del batch: {batch.status}. Esperando...")
        time.sleep(10)
        batch = client.batches.retrieve(batch_id)

    if batch.status != "completed":
        raise Exception(f"El batch no se completó correctamente. Estado: {batch.status}")

    # 2) Descargamos el archivo con los resultados que genero OPEN AI.
    output = client.files.content(batch.output_file_id)
    
    # 3) Guardamos una linea por resultado: custom_id = texto generado.

    with open(output_path, "w", encoding="utf-8") as file:
        for line in output.text.splitlines():
            result = json.loads(line)
            custom_id = result["custom_id"]
            text = result["response"]["body"]["output"][0]["content"][0]["text"]
            file.write(f"{custom_id}: {text}\n")

    return output_path
