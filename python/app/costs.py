def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Estima el costo aproximado de un request a partir de los tokens.

    Los precios cambian con el tiempo y dependen del modelo: verifica siempre
    la documentacion oficial de OpenAI antes de grabar o pasar a produccion.
    """
    # Precios de ejemplo (USD por millon de tokens). Ajustalos al modelo real
    input_cost_per_million = 2.50
    output_cost_per_million = 15.00

    input_cost = (input_tokens / 1_000_000) * input_cost_per_million
    output_cost = (output_tokens / 1_000_000) * output_cost_per_million

    return input_cost + output_cost