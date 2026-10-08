import base64

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse

from app.openai_client import (generate_text, generate_brief, generate_structured_brief, generate_content_piece, analyze_reference_image)

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
            <h2>Convertir idea en brief</h2>
            <form method="post" action="/brief">
                <textarea name="idea" rows="6" cols="60"></textarea>
                <br />
                <button type="submit">Generar brief</button>
            </form>
            
            <h2>Generar contenido por canal</h2>
           <form method="post" action="/content">
                <textarea name="idea" rows="6" cols="60"></textarea>
                <br />
                <select name="channel">
                <option value="twitter">Twitter</option>
                <option value="linkedin">LinkedIn</option>
                <option value="instagram">Instagram</option>
                </select>
                <br />
                <button type="submit">Generar contenido</button>
</form>
<h2>Analizar imagen de referencia</h2>
<form method="post" action="/analyze-image" enctype="multipart/form-data">
    <input type="file" name="file" />
    <br />
    <button type="submit">Analizar imagen</button>
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

@app.post("/brief", response_class=HTMLResponse)
def brief(idea: str = Form(...)):
    # El backend llama a OpenAI: la API key sigue protegida del lado del servidor.
    result = generate_brief(idea)

    return f"""
    <html>
        <head>
            <title>Generador de texto con OpenAI</title>
        </head>
        <body>
            <h1>Resultado</h1>
            <p>{result}</p>
            <a href="/">Volver</a>
        </body>
    </html>
    """

@app.post("/content", response_class=HTMLResponse)
def content(idea: str = Form(...), channel: str = Form(...)):
    # El backend llama a OpenAI: la API key sigue protegida del lado del servidor.
    # idea brief estructurado pieza para el canal
    brief = generate_structured_brief(idea)
    piece = generate_content_piece(brief,channel)

    return f"""
    <html>
        <body>
          <h1>{piece.title}</h1>
          <p><strong>Canal:</strong> {piece.channel}</p>  
          <pre style="white-space: pre-wrap; word-wrap: break-word;">{piece.body}</pre>
          <p><strong>CTA:</strong> {piece.call_to_action}</p>
          <a href="/">Volver</a>
        </body>
    </html>
    """

@app.post("/analyze-image", response_class=HTMLResponse)
async def analyze_image(file: UploadFile = File(...)):
    # Leemos el archivo y lo convertimos a base64.
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Lo enviamos como input multimodal y devolvemos el analisis en texto.
    analysis = analyze_reference_image(image_base64, file.content_type)

    return f"""
<html>
    <body>
        <h1>Análisis de la imagen</h1>
        <p style="white-space: pre-wrap; word-wrap: break-word;">{analysis}</p>
        <a href="/">Volver</a>
    </body>
</html>
"""