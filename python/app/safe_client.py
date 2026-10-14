import time 
from openai import APIError, APITimeoutError, RateLimitError

def safe_openai_call(callback, retries: int = 3):

    """Ejecuta una llamada a la OpenAI con reintentos y backoff exponencial


    - 429 (rate limit) y timeouts conviene reintertarlos.
    - 400 / 401 normalmente NO se arreglan teintentando (revisar request o key).
    """

    for attempt in range(retries):
        try:
            return callback()

        except RateLimitError:
            wait_time = 2 ** attempt
            print(f"Rate limit. Reintentando en {wait_time}s...")
            time.sleep(wait_time)

        except APITimeoutError:
            wait_time = 2 ** attempt
            print(f"Timeout. Reintentando en {wait_time}s...")
            time.sleep(wait_time)

        except APIError as error:
            wait_time = 2 ** attempt
            print(f"Error API. {error}. Reintentando en {wait_time}s...")
            time.sleep(wait_time)

    raise Exception("No se pudo completar la llamada a OpenAI.")
