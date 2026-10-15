# AI Content Operations Studio

🌐 [English](README.md) · **Español**

Aplicación web que reúne en una sola interfaz varias operaciones de contenido con IA: convertir ideas en briefs, generar contenido por canal, analizar y generar imágenes, transcribir notas de voz, convertir texto en audio y buscar en la web. Construida con **FastAPI** y la **API de OpenAI**, y desplegada en **Railway**.

**Demo:** https://curso-openai-api-production.up.railway.app/

#![Captura de la app](docs/captura.png)

## Funciones

| Función | Qué hace |
|---|---|
| Generar idea | Genera una idea a partir de un texto |
| Convertir idea en brief | Estructura una idea desordenada en un brief de campaña |
| Generar contenido por canal | Crea contenido a partir de un texto base y el canal elegido (por ejemplo, Twitter) |
| Analizar imagen de referencia | Recibe una imagen subida por el usuario y la analiza |
| Generar imagen para campaña | Crea una imagen a partir de una descripción |
| Generar contenido largo (streaming) | Muestra la respuesta mientras se va generando |
| Transcribir nota de voz | Convierte un audio subido en texto |
| Escuchar un guion (texto a voz) | Convierte un texto en audio |
| Búsqueda web | Usa la tool nativa de búsqueda web de OpenAI |

## Endpoints

| Método | Ruta | Recibe | Devuelve |
|---|---|---|---|
| GET | `/` | — | Página con los formularios de todas las funciones |
| POST | `/generate` | `idea` (texto) | HTML con el texto generado |
| POST | `/brief` | `idea` (texto) | HTML con el brief generado |
| POST | `/content` | `idea` y `channel` (`twitter`, `linkedin` o `instagram`) | HTML con título, canal, cuerpo y call to action. Primero genera un brief estructurado y luego la pieza para el canal |
| POST | `/analyze-image` | `file` (imagen) | HTML con el análisis de la imagen |
| POST | `/generate-image` | `idea` (texto) | HTML con la imagen generada. Parte de un brief estructurado para armar el prompt visual |
| POST | `/stream-content` | `idea` (texto) | Texto en streaming (`text/plain`) a medida que se genera |
| POST | `/transcribe-audio` | `file` (audio) | JSON con la transcripción: `{"text": "..."}` |
| POST | `/text-to-speech` | `text` (texto) | HTML con un reproductor de audio |
| POST | `/web-search` | `prompt` (texto) | HTML con el resultado de la búsqueda web |

La API key se usa solo en el backend, por lo que nunca llega al navegador. Las imágenes y el audio generados se incrustan en la respuesta en base64.

## Tecnologías

- Python
- FastAPI
- Uvicorn
- Jinja2 (plantillas HTML)
- python-multipart (subida de archivos)
- Pydantic (salidas estructuradas)
- python-dotenv (variables de entorno)
- OpenAI API
- Railway (despliegue)

## Modelos de OpenAI

| Uso | Modelo |
|---|---|
| Texto, briefs, contenido por canal, análisis de imagen, streaming y búsqueda web | `gpt-5.4` (Responses API) |
| Clasificación de ideas por canal con Batch API | `gpt-5.4-mini` |
| Generación de imágenes | `gpt-image-1` |
| Voz a texto | `gpt-4o-transcribe` |
| Texto a voz | `gpt-4o-mini-tts` (voz `alloy`) |

## Conceptos aplicados

- **Responses API** para generación de texto, con `instructions` para definir el comportamiento del modelo.
- **Structured Outputs** con Pydantic (`responses.parse`): el brief de campaña y la pieza de contenido se devuelven como objetos tipados (`CampaignBrief` y `ContentPiece`).
- **Entrada multimodal**: la imagen se envía en base64 junto con el texto.
- **Streaming**: los fragmentos se reenvían al navegador con `StreamingResponse`.
- **Tool hospedada** de búsqueda web, ejecutada por OpenAI sin un loop manual en el backend.
- **Cliente de OpenAI reutilizable** en un solo módulo.
- **Audio**: transcripción de notas de voz y síntesis de voz.
- **Prompt caching**: las instrucciones estables van al inicio del prompt (`generate_with_cache`), de modo que el prefijo se pueda reutilizar entre solicitudes.
- **Batch API** para tareas sin urgencia y a menor costo: `build_batch_file` crea un archivo JSONL con una solicitud por línea, `submit_batch` lo sube y crea el batch (ventana de 24 h) y `save_batch_results` consulta el estado cada 10 segundos y guarda los resultados en un archivo de texto.
- **Estimación de costos**: función `estimate_cost` que calcula el costo aproximado de una solicitud a partir de los tokens de entrada y salida (con precios de ejemplo por millón de tokens, que hay que ajustar al modelo y verificar en la documentación oficial).
- **Manejo de errores**: función `safe_openai_call` que reintenta con backoff exponencial (1 s, 2 s, 4 s) ante rate limits, timeouts y errores de la API.

## Estructura del proyecto

```
Curso-openai-api/
├── python/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── costs.py           # Estimación de costos por tokens
│   │   ├── models.py          # Modelos Pydantic (CampaignBrief, ContentPiece)
│   │   ├── openai_client.py   # Cliente reutilizable y funciones que consumen la API
│   │   ├── optimization.py    # Prompt caching y Batch API
│   │   ├── safe_client.py     # Reintentos con backoff exponencial
│   │   └── server.py          # Endpoints de FastAPI
│   ├── batch/                 # Archivos de entrada y resultados del Batch API
│   ├── main.py
│   └── requirements.txt
├── source/
├── typescript/
├── PLAN_PROYECTO.md
├── README.md
└── README.es.md
```

## Cómo correrlo en local

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Johankantor/Curso-openai-api.git
   cd Curso-openai-api/python
   ```

2. Crea un entorno virtual e instala las dependencias:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` con tu clave de OpenAI:

   ```
   OPENAI_API_KEY=tu_clave_aqui
   ```

4. Inicia el servidor:

   ```bash
   uvicorn app.server:app --reload
   ```

5. Abre http://127.0.0.1:8000 en el navegador.

## Despliegue en Railway

1. Conecta el repositorio de GitHub a un proyecto nuevo en Railway.
2. Define `python` como carpeta raíz del build (*Root Directory*).
3. Agrega la variable `OPENAI_API_KEY` en la pestaña *Variables*.
4. Configura el comando de inicio:

   ```bash
   uvicorn app.server:app --host 0.0.0.0 --port $PORT
   ```

5. Genera un dominio público y selecciona el puerto.

**Nota:** el sistema de archivos de Railway es efímero. Los archivos generados (imágenes y audios) se pierden al reiniciar o volver a desplegar, así que para conservarlos hay que usar un Volume o almacenamiento externo.

## Seguridad

La clave de API se lee desde variables de entorno y el archivo `.env` está en `.gitignore`, por lo que no se sube al repositorio.

## Próximas mejoras

- Exponer el flujo de Batch desde la app, por ejemplo con un endpoint para enviar ideas y consultar el estado del batch
- Mostrar el costo estimado de cada solicitud usando el `usage` de la respuesta y `estimate_cost`
- Usar `safe_openai_call` en las llamadas de los endpoints y evitar reintentar errores 400 y 401, que no se arreglan reintentando
- Conectar las reglas de marca (function tool `get_brand_voice`) a la generación de contenido por canal
- Escapar el texto antes de insertarlo en el HTML de las respuestas
- Usar archivos temporales únicos para imágenes y audios, y así evitar que dos solicitudes simultáneas se sobrescriban
- Guardar el historial de briefs y contenidos en una base de datos
- Agregar autenticación de usuarios
- Sumar más canales
- Almacenamiento persistente para imágenes y audios generados

## Autor

[LinkedIn](https://www.linkedin.com/in/johanalexandercantor/) · [GitHub](https://github.com/Johankantor)