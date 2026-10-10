from app.openai_client import generate_with_web_search

result = generate_with_web_search("Quiero comprar unas zapatillas jordan dame un listado de las mejores tiendas online para comprar")
print(result)