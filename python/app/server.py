from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from app.openai_client import generate_text

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Generador de texto con OpenAI</title>
        </head>
        <body>
            <h1>AI Content Operations Studio</h1>
            <form action="/generate" method="post">
                <textarea name="idea" rows="6" cols="60"></textarea>
                <br />
                <button type="submit">Generar idea</button>
            </form>
        </body>
    </html>
    """
@app.post("/generate", response_class=HTMLResponse)
def generate(idea: str = Form(...)):
    # El backend llama a OpenAI: la API key sigue protegida del lado del servidor.
    result = generate_text(idea)

    return f"""
    <html>
        <head>
            <title>Generador de texto con OpenAI</title>
        </head>
        <body>
            <h1>Resultado</h1>
            <p>{result["text"]}</p>
            <a href="/">Volver</a>
        </body>
    </html>
    """

