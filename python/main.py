from app.openai_client import (generate_text, generate_text_with_chat_completions)

prompt = "Quiero lanzar un workshop de IA para developers."

modern = generate_text(prompt)
print("== Responses API ==")
print(modern["text"])
print(modern["usage"])

# Legacy

legacy = generate_text_with_chat_complations(prompt)

print("== Legacy API ==")
print(legacy)