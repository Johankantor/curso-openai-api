import base64
import tempfile
import os

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse

from app.openai_client import (generate_text, generate_brief, generate_structured_brief, generate_content_piece, analyze_reference_image, generate_campaign_image, stream_long_content, transcribe_audio_file,
)

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
   <!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generador de texto con OpenAI</title>
</head>
<body>
    <h1>AI Content Operations Studio</h1>

    <!-- 1. Generar Idea General -->
    <section>
        <h2>Generar idea</h2>
        <form action="/generate" method="post">
            <textarea name="idea" rows="6" cols="60" placeholder="Escribe tu idea aquí..."></textarea>
            <br />
            <button type="submit">Generar idea</button>
        </form>
    </section>

    <!-- 2. Convertir Idea en Brief -->
    <section>
        <h2>Convertir idea en brief</h2>
        <form action="/brief" method="post">
            <textarea name="idea" rows="6" cols="60" placeholder="Escribe tu idea para el brief..."></textarea>
            <br />
            <button type="submit">Generar brief</button>
        </form>
    </section>

    <!-- 3. Generar Contenido por Canal -->
    <section>
        <h2>Generar contenido por canal</h2>
        <form action="/content" method="post">
            <textarea name="idea" rows="6" cols="60" placeholder="Escribe el texto base..."></textarea>
            <br />
            <select name="channel">
                <option value="twitter">Twitter</option>
                <option value="linkedin">LinkedIn</option>
                <option value="instagram">Instagram</option>
            </select>
            <br /><br />
            <button type="submit">Generar contenido</button>
        </form>
    </section>

    <!-- 4. Analizar Imagen de Referencia (Vision) -->
    <section>
        <h2>Analizar imagen de referencia</h2>
        <form action="/analyze-image" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*" required />
            <br /><br />
            <button type="submit">Analizar imagen</button>
        </form>
    </section>

    <!-- 5. Generar Imagen para Campaña (DALL-E) -->
    <section>
        <h2>Generar imagen para campaña</h2>
        <form action="/generate-image" method="post">
            <textarea name="idea" rows="6" cols="60" placeholder="Describe la imagen que deseas generar..."></textarea>
            <br />
            <button type="submit">Generar imagen</button>
        </form>
    </section>
    
    <!-- 6. Generar contenido largo (streaming) -->
    <section>
        <h2>Generar contenido largo (streaming)</h2>
        <form method="post" action="/stream-content">
            <textarea name="idea" rows="6" cols="60" placeholder="Escribe el texto base..."></textarea>
            <br />
            <button type="submit">Generar en streaming</button>
        </form>
    </section>
    
    <!-- 7. Transcribir Audio -->
    <section>
        <h2>Transcribir nota de voz</h2>
        <form action="/transcribe-audio" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="audio/*" required />
            <br />
            <button type="submit">Transcribir audio</button>
        </form>
    </section>
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

@app.post("/generate-image", response_class=HTMLResponse)
def generate_image(idea: str = Form(...)):
    # Usamos el brief como fuente del prompt visual.
    brief = generate_structured_brief(idea)
    # Genera y guarda la imagen como output.png.
    generate_campaign_image(brief)

    #Lea el archivo generado dentro del HTML.
    with open("output.png","rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    return f"""
    <html>
  <body>
    <h1>Imagen de campaña</h1>
    <img src="data:image/png;base64,{image_base64}" alt="Imagen generada" style="max-width: 100%;" />
    <br />
    <a href="/">Volver</a>
  </body>
</html>
"""

@app.post("/stream-content")
def stream_content(idea: str = Form(...)):
    # El backend reenvia los fragmentos al cliente a medida que llegan.
    return StreamingResponse(
        stream_long_content(idea),
        media_type="text/plain"
    )


@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    # Leemos el archivo y lo convertimos a base64.
    audio_bytes = await file.read()
    temp_path = os.path.join(tempfile.gettempdir(), file.filename)
    with open(temp_path, "wb") as audio_file:
        audio_file.write(audio_bytes)
    text = transcribe_audio_file(temp_path)
    # Lo enviamos como input multimodal y devolvemos la transcripción en texto.
    
    return {"text": text}