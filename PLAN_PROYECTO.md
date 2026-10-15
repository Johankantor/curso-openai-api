# Plan del proyecto: AI Content Operations Studio

## 1. Objetivo

Construir una aplicación web que permita pasar de una **idea desordenada** a **contenido listo para publicar**, y que reúna en un solo lugar las operaciones de contenido con IA: briefs, contenido por canal, análisis y generación de imágenes, voz a texto, texto a voz y búsqueda web.

Es también un proyecto de aprendizaje y portafolio: aplicar de punta a punta la API de OpenAI con Python y desplegarla en producción.

## 2. Alcance

**Incluye**
- Interfaz web simple con un formulario por cada función.
- Backend en FastAPI que protege la API key.
- Generación de texto, briefs estructurados y contenido por canal (Twitter, LinkedIn, Instagram).
- Análisis y generación de imágenes.
- Transcripción de notas de voz y conversión de texto a voz.
- Streaming para contenido largo.
- Búsqueda web con la tool hospedada de OpenAI.
- Utilidades de reintentos, estimación de costos, prompt caching y Batch API.
- Despliegue público en Railway.

**No incluye (por ahora)**
- Cuentas de usuario ni login.
- Base de datos ni historial.
- Almacenamiento permanente de imágenes y audios.

## 3. Arquitectura

```
Navegador (formularios HTML)
        │
        ▼
FastAPI  (python/app/server.py)
        │  llama a
        ▼
Funciones de OpenAI  (python/app/openai_client.py)
        │
        ▼
API de OpenAI  (Responses, Images, Audio)
```

| Archivo | Responsabilidad |
|---|---|
| `server.py` | Endpoints de FastAPI y respuestas HTML |
| `openai_client.py` | Cliente reutilizable y una función por operación |
| `models.py` | Modelos Pydantic de salida estructurada (`CampaignBrief`, `ContentPiece`) |
| `safe_client.py` | Reintentos con backoff exponencial |
| `costs.py` | Estimación de costos por tokens |
| `optimization.py` | Prompt caching y Batch API |
| `batch/` | Archivos de entrada y resultados del Batch API |

## 4. Flujos principales

**Contenido por canal:** idea → brief estructurado → pieza para el canal (título, cuerpo y call to action).

**Imagen de campaña:** idea → brief estructurado → prompt visual → imagen.

**Batch:** lista de ideas → archivo JSONL → batch en OpenAI → consulta de estado cada 10 s → resultados en archivo de texto.

## 5. Decisiones técnicas

| Decisión | Motivo |
|---|---|
| Responses API en lugar de Chat Completions | Está pensada para crecer con tools, multimodalidad y continuidad |
| Structured Outputs con Pydantic | El brief y la pieza llegan como objetos tipados y no como texto libre |
| Un único cliente de OpenAI reutilizable | Evita repetir configuración y centraliza la API key |
| API key solo en el backend (variable de entorno) | Nunca llega al navegador ni al repositorio |
| `gpt-5.4-mini` para el batch de clasificación | Tarea simple que puede esperar y conviene que cueste menos |
| Imágenes y audio en base64 dentro de la respuesta | Evita depender del sistema de archivos del servidor |

## 6. Estado actual

| Fase | Estado |
|---|---|
| Primera llamada a la API y cliente reutilizable | Hecho |
| Base web con FastAPI y formularios | Hecho |
| Brief y contenido por canal (salidas estructuradas) | Hecho |
| Imágenes (análisis y generación) | Hecho |
| Streaming | Hecho |
| Voz a texto y texto a voz | Hecho |
| Búsqueda web | Hecho |
| Reintentos, costos, caching y Batch (como utilidades) | Hecho |
| Despliegue en Railway | Hecho |
| README en español e inglés | Hecho |
| Rediseño de la interfaz | Pendiente |
| Captura de pantalla para el README | Pendiente (después del rediseño) |

## 7. Pendientes y mejoras

**Prioridad alta**
- Revocar la API key que se compartió fuera del `.env`, crear una nueva y actualizarla en Railway.
- Poner un límite de gasto en la cuenta de OpenAI, porque la demo es pública.
- Escapar el texto antes de insertarlo en el HTML de las respuestas.
- Usar nombres de archivo únicos para imágenes y audios, para que dos solicitudes simultáneas no se sobrescriban.
- Corregir `safe_openai_call` para que no reintente errores 400 y 401.

**Prioridad media**
- Rediseñar la interfaz (ver sección 8).
- Conectar la function tool `get_brand_voice` a la generación de contenido por canal.
- Usar `safe_openai_call` en las llamadas de los endpoints.
- Mostrar el costo estimado de cada solicitud con `usage` y `estimate_cost`.
- Ampliar las instrucciones estables para que el prompt caching tenga efecto.
- Exponer el flujo de Batch desde la app.

**Prioridad baja**
- Historial de briefs y contenidos en una base de datos.
- Autenticación de usuarios.
- Más canales.
- Almacenamiento persistente para imágenes y audios.

## 8. Rediseño de la interfaz

Hoy la página es una sola columna con nueve formularios sin estilos.

Ideas por definir:
- Agrupar las funciones por tema (texto, imagen, audio, búsqueda).
- Mostrar el resultado en la misma página, sin salir a otra pantalla.
- Indicadores de carga mientras el modelo responde.
- Streaming visible en pantalla.
- Diseño adaptable a celular.

## 9. Seguridad antes de publicar

- [ ] `.env` está en `.gitignore`
- [ ] `output.png`, `output.mp3` y `batch/results.txt` están en `.gitignore`
- [ ] Ningún archivo del repositorio contiene la API key real
- [ ] La clave de Railway está en *Variables* y no en el código
- [ ] Hay un límite de gasto en la cuenta de OpenAI

## 10. Despliegue

- Plataforma: Railway
- Carpeta raíz del build: `python`
- Comando de inicio: `uvicorn app.server:app --host 0.0.0.0 --port $PORT`
- Variable necesaria: `OPENAI_API_KEY`
- Nota: el sistema de archivos es efímero, así que los archivos generados no persisten tras un reinicio.

**Demo:** https://curso-openai-api-production.up.railway.app/