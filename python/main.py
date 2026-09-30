from app.openai_client import (generate_text, generate_text_with_chat_completions)
from app.cost import estimate_cost

prompt = "Quiero lanzar un workshop de IA para developers."

result = generate_text(prompt)

usage = result["usage"]

print(result["text"])
print(usage)

cost = estimate_cost(
    input_tokens=usage.input_tokens,
    output_tokens=usage.output_tokens,
)
print(f"Costo Aproximado: ${cost:.2f}")