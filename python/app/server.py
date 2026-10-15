import base64
import html
import os
import tempfile
import uuid

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse

from app.openai_client import (
    analyze_reference_image,
    generate_brief,
    generate_campaign_image,
    generate_content_piece,
    generate_structured_brief,
    generate_text,
    generate_with_web_search,
    stream_long_content,
    text_to_speech,
    transcribe_audio_file,
)

app = FastAPI()

# Interfaz rediseñada con un estilo moderno, limpio y profesional (Dark Mode refinado)
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Content Operations Studio</title>
    <style>
        :root {
            --bg-main: #090d16;
            --bg-card: #131d31;
            --bg-input: #1a263f;
            --border-color: #273859;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --accent-glow: rgba(59, 130, 246, 0.2);
        }
        * {
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            margin: 0;
            padding: 30px 20px;
        }
        .container {
            max-width: 1450px;
            margin: 0 auto;
        }
        header {
            margin-bottom: 35px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }
        header h1 {
            font-size: 1.8rem;
            margin: 0;
            background: linear-gradient(135deg, #60a5fa 0%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
        header p {
            color: var(--text-muted);
            font-size: 0.95rem;
            margin: 0;
        }
        .workspace {
            display: grid;
            grid-template-columns: 1.1fr 0.9fr;
            gap: 30px;
            align-items: start;
        }
        @media (max-width: 1024px) {
            .workspace {
                grid-template-columns: 1fr;
            }
        }
        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 18px;
        }
        .card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.25s ease;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .card:hover {
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 8px 15px -3px var(--accent-glow);
            transform: translateY(-2px);
        }
        .card h2 {
            font-size: 0.95rem;
            margin-top: 0;
            margin-bottom: 14px;
            color: #cbd5e1;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        form {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        textarea, select, input[type="file"] {
            width: 100%;
            background-color: var(--bg-input);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-main);
            padding: 10px 12px;
            font-size: 0.9rem;
            font-family: inherit;
            resize: vertical;
            transition: border-color 0.2s, box-shadow 0.2s;
        }
        textarea {
            min-height: 75px;
        }
        textarea:focus, select:focus, input[type="file"]:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }
        button.btn-action {
            background-color: var(--accent);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 9px 16px;
            font-weight: 600;
            font-size: 0.88rem;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }
        button.btn-action:hover {
            background-color: var(--accent-hover);
        }
        button.btn-action:active {
            transform: scale(0.98);
        }
        /* Panel Único de Resultados Profesional */
        .result-panel-wrapper {
            position: sticky;
            top: 30px;
        }
        .result-panel {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 24px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            min-height: 550px;
            max-height: 88vh;
            display: flex;
            flex-direction: column;
        }
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 14px;
            margin-bottom: 16px;
        }
        .result-header h2 {
            margin: 0;
            font-size: 1.1rem;
            color: #60a5fa;
            font-weight: 600;
        }
        .status-badge {
            font-size: 0.75rem;
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            padding: 3px 8px;
            border-radius: 20px;
            font-weight: 500;
        }
        .result-content {
            flex-grow: 1;
            overflow-y: auto;
            padding-right: 4px;
        }
        .result-content::-webkit-scrollbar {
            width: 6px;
        }
        .result-content::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }
        .placeholder-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            min-height: 350px;
            color: var(--text-muted);
            text-align: center;
            gap: 12px;
        }
        .placeholder-state svg {
            width: 48px;
            height: 48px;
            opacity: 0.4;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background: var(--bg-main);
            padding: 16px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            font-size: 0.88rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            color: #e2e8f0;
            margin: 0;
        }
        .spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 50%;
            border-top-color: #fff;
            animation: spin 0.8s linear infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>AI Content Operations Studio</h1>
                <p>Suite inteligente de automatización de contenidos con OpenAI API & FastAPI</p>
            </div>
            <div class="status-badge">● Sistema Activo</div>
        </header>

        <div class="workspace">
            <!-- Izquierda: Tarjetas de Formularios -->
            <div class="cards-grid">
                <!-- 1 -->
                <div class="card">
                    <h2>💡 Generar Idea piensa lo que quieras</h2>
                    <form onsubmit="handleSubmit(event, '/generate', this)">
                        <textarea name="idea" placeholder="Escribe el tema general..."></textarea>
                        <button type="submit" class="btn-action">Ejecutar</button>
                    </form>
                </div>

                <!-- 2 -->
                <div class="card">
                    <h2>📋 Convertir en Brief</h2>
                    <form onsubmit="handleSubmit(event, '/brief', this)">
                        <textarea name="idea" placeholder="Tema para estructurar el brief..."></textarea>
                        <button type="submit" class="btn-action">Ejecutar</button>
                    </form>
                </div>

                <!-- 3 -->
                <div class="card">
                    <h2>📱 Contenido por Canal</h2>
                    <form onsubmit="handleSubmit(event, '/content', this)">
                        <textarea name="idea" rows="2" placeholder="Texto base..."></textarea>
                        <select name="channel">
                            <option value="twitter">Twitter / X</option>
                            <option value="linkedin">LinkedIn</option>
                            <option value="instagram">Instagram</option>
                        </select>
                        <button type="submit" class="btn-action">Generar Pieza</button>
                    </form>
                </div>

                <!-- 4 -->
                <div class="card">
                    <h2>👁️ Analizar Imagen (Vision)</h2>
                    <form onsubmit="handleFileSubmit(event, '/analyze-image', this)">
                        <input type="file" name="file" accept="image/*" required />
                        <button type="submit" class="btn-action">Analizar Imagen</button>
                    </form>
                </div>

                <!-- 5 -->
                <div class="card">
                    <h2>🎨 Imagen de Campaña (DALL-E)</h2>
                    <form onsubmit="handleSubmit(event, '/generate-image', this)">
                        <textarea name="idea" placeholder="Describe la imagen visual..."></textarea>
                        <button type="submit" class="btn-action">Generar Imagen</button>
                    </form>
                </div>
                
                <!-- 6 -->
                <div class="card">
                    <h2>⚡ Streaming de Contenido</h2>
                    <form onsubmit="handleStreamSubmit(event, '/stream-content', this)">
                        <textarea name="idea" placeholder="Tema para redactar en tiempo real..."></textarea>
                        <button type="submit" class="btn-action">Transmitir</button>
                    </form>
                </div>
                
                <!-- 7 -->
                <div class="card">
                    <h2>🎙️ Transcribir Nota de Voz</h2>
                    <form onsubmit="handleJsonFileSubmit(event, '/transcribe-audio', this)">
                        <input type="file" name="file" accept="audio/*" required />
                        <button type="submit" class="btn-action">Transcribir Audio</button>
                    </form>
                </div>
                
                <!-- 8 -->
                <div class="card">
                    <h2>🔊 Texto a Voz (TTS)</h2>
                    <form onsubmit="handleSubmit(event, '/text-to-speech', this)">
                        <textarea name="idea" placeholder="Texto que deseas convertir a audio..."></textarea>
                        <button type="submit" class="btn-action">Convertir Audio</button>
                    </form>
                </div>
                
                <!-- 9 -->
                <div class="card">
                    <h2>🌐 Búsqueda Web (Tool)</h2>
                    <form onsubmit="handleSubmit(event, '/web-search', this)">
                        <textarea name="prompt" placeholder="Consulta web en tiempo real..."></textarea>
                        <button type="submit" class="btn-action">Buscar en Web</button>
                    </form>
                </div>
            </div>

            <!-- Derecha: Cuadro Único de Resultado -->
            <div class="result-panel-wrapper">
                <div class="result-panel">
                    <div class="result-header">
                        <h2>Panel de Resultado</h2>
                        <span style="font-size: 0.8rem; color: var(--text-muted);">Salida en tiempo real</span>
                    </div>
                    <div id="result-box" class="result-content">
                        <div class="placeholder-state">
                            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                            <span>Selecciona cualquier herramienta a la izquierda<br>para visualizar el resultado aquí.</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const resultBox = document.getElementById('result-box');

        // Función auxiliar mejorada con un pequeño retraso para asegurar el scroll en móviles
        function scrollToResult() {
            if (window.innerWidth <= 1024) {
                setTimeout(() => {
                    const panel = document.querySelector('.result-panel-wrapper') || document.querySelector('.result-panel');
                    if (panel) {
                        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }, 100);
            }
        }

        function showLoading(text) {
            resultBox.innerHTML = `
                <div class="placeholder-state">
                    <div class="spinner"></div>
                    <span style="color: #60a5fa; font-weight: 500;">${text}</span>
                </div>`;
            scrollToResult();
        }

        async function handleSubmit(event, url, form) {
            event.preventDefault();
            showLoading('Procesando solicitud con OpenAI...');
            const formData = new FormData(form);
            try {
                const response = await fetch(url, { method: 'POST', body: formData });
                const htmlContent = await response.text();
                resultBox.innerHTML = htmlContent;
                scrollToResult();
            } catch (error) {
                resultBox.innerHTML = '<p style="color: #ef4444; padding: 20px;">Error de conexión con el servidor backend.</p>';
            }
        }

        async function handleFileSubmit(event, url, form) {
            event.preventDefault();
            showLoading('Analizando archivo multimedia con modelo Vision...');
            const formData = new FormData(form);
            try {
                const response = await fetch(url, { method: 'POST', body: formData });
                const htmlContent = await response.text();
                resultBox.innerHTML = htmlContent;
                scrollToResult();
            } catch (error) {
                resultBox.innerHTML = '<p style="color: #ef4444; padding: 20px;">Error al procesar el archivo multimedia.</p>';
            }
        }

        async function handleJsonFileSubmit(event, url, form) {
            event.preventDefault();
            showLoading('Transcribiendo audio con Whisper...');
            const formData = new FormData(form);
            try {
                const response = await fetch(url, { method: 'POST', body: formData });
                const data = await response.json();
                resultBox.innerHTML = `<h3 style="margin-top:0; color:#60a5fa;">Transcripción Completada</h3><pre>${data.text}</pre>`;
                scrollToResult();
            } catch (error) {
                resultBox.innerHTML = '<p style="color: #ef4444; padding: 20px;">Error en la transcripción del audio.</p>';
            }
        }

        async function handleStreamSubmit(event, url, form) {
            event.preventDefault();
            resultBox.innerHTML = '<h3 style="margin-top:0; color:#60a5fa;">Transmitiendo Contenido...</h3><pre id="stream-output"></pre>';
            scrollToResult();
            const outputPre = document.getElementById('stream-output');
            const formData = new FormData(form);
            try {
                const response = await fetch(url, { method: 'POST', body: formData });
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    outputPre.textContent += decoder.decode(value, { stream: true });
                }
            } catch (error) {
                outputPre.textContent += '\n[Error de red durante el streaming]';
            }
        }
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return BASE_LAYOUT


@app.post("/generate", response_class=HTMLResponse)
def generate(idea: str = Form(...)):
    result = generate_text(idea)
    safe_text = html.escape(result.get("text", ""))
    return f'<h3 style="margin-top:0; color:#60a5fa;">Idea Generada</h3><pre>{safe_text}</pre>'


@app.post("/brief", response_class=HTMLResponse)
def brief(idea: str = Form(...)):
    result = generate_brief(idea)
    safe_result = html.escape(str(result))
    return f'<h3 style="margin-top:0; color:#60a5fa;">Brief Estructurado</h3><pre>{safe_result}</pre>'


@app.post("/content", response_class=HTMLResponse)
def content(idea: str = Form(...), channel: str = Form(...)):
    structured_brief = generate_structured_brief(idea)
    piece = generate_content_piece(structured_brief, channel)

    safe_title = html.escape(piece.title)
    safe_channel = html.escape(str(piece.channel))
    safe_body = html.escape(piece.body)
    safe_cta = html.escape(piece.call_to_action)

    return f"""
        <h3 style="margin-top:0; color:#60a5fa;">{safe_title}</h3>
        <p style="color: #94a3b8; font-size: 0.9rem;"><strong>Canal:</strong> {safe_channel}</p>
        <pre>{safe_body}</pre>
        <p style="color: #cbd5e1; font-size: 0.9rem;"><strong>CTA:</strong> {safe_cta}</p>
    """


@app.post("/analyze-image", response_class=HTMLResponse)
async def analyze_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    analysis = analyze_reference_image(image_base64, file.content_type)
    safe_analysis = html.escape(str(analysis))
    return f'<h3 style="margin-top:0; color:#60a5fa;">Análisis Visual</h3><pre>{safe_analysis}</pre>'


@app.post("/generate-image", response_class=HTMLResponse)
def generate_image(idea: str = Form(...)):
    structured_brief = generate_structured_brief(idea)
    unique_filename = f"output_{uuid.uuid4().hex}.png"
    
    generate_campaign_image(structured_brief)
    if os.path.exists("output.png"):
        os.rename("output.png", unique_filename)

    with open(unique_filename, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    try:
        os.remove(unique_filename)
    except Exception:
        pass

    return f"""
        <h3 style="margin-top:0; color:#60a5fa;">Imagen Generada (DALL-E)</h3>
        <div style="text-align: center; margin-top: 10px;">
            <img src="data:image/png;base64,{image_base64}" alt="Imagen generada" style="max-width: 100%; border-radius: 8px; border: 1px solid var(--border-color);" />
        </div>
    """


@app.post("/stream-content")
def stream_content(idea: str = Form(...)):
    return StreamingResponse(
        stream_long_content(idea),
        media_type="text/plain"
    )


@app.post("/transcribe-audio")
async def transcribe_audio(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}_{file.filename}")
    with open(temp_path, "wb") as audio_file:
        audio_file.write(audio_bytes)
    
    try:
        text = transcribe_audio_file(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    return {"text": text}


@app.post("/text-to-speech", response_class=HTMLResponse)
def create_audio(text: str = Form(..., alias="idea")):
    output_path = text_to_speech(text)

    with open(output_path, "rb") as audio_file:
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    
    try:
        if os.path.exists(output_path):
            os.remove(output_path)
    except Exception:
        pass

    return f"""
        <h3 style="margin-top:0; color:#60a5fa;">Audio Generado (TTS)</h3>
        <audio controls src="data:audio/mp3;base64,{audio_base64}" style="width: 100%; margin-top: 15px;"></audio>
    """


@app.post("/web-search", response_class=HTMLResponse)
def web_search(prompt: str = Form(...)):
    result = generate_with_web_search(prompt)
    safe_result = html.escape(str(result))
    return f'<h3 style="margin-top:0; color:#60a5fa;">Resultado de Búsqueda Web</h3><pre>{safe_result}</pre>'