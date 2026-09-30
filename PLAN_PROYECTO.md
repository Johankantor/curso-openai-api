# Plan de Proyecto: AI Content Operations Studio

## Estructura General

```
ai-content-operations-studio/
├── python/                    # Implementación principal del curso
│   ├── app/
│   │   ├── __init__.py
│   │   ├── openai_client.py
│   │   ├── costs.py
│   │   ├── safe_client.py
│   │   ├── models.py
│   │   └── server.py
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
├── typescript/                # Implementación equivalente en TypeScript
│   ├── src/
│   │   ├── openaiClient.ts
│   │   ├── costs.ts
│   │   ├── safeClient.ts
│   │   ├── models.ts
│   │   └── server.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── .env
│   └── .env.example
├── .gitignore
└── README.md
```

## Ramas de Git

### Rama `main`
- Contiene el estado final del proyecto (Clase 18)
- Incluye todas las features implementadas
- Código Python y TypeScript completos
- Documentación y configuración de deploy

### Ramas por Clase

#### `clase-01-primera-llamada`
**Python:**
- `python/main.py` - Primera llamada a OpenAI API
- `python/.env` - Variables de entorno
- `python/.gitignore` - Ignorar .env

**TypeScript:**
- `typescript/src/main.ts` - Primera llamada en TypeScript
- `typescript/package.json` - Dependencias iniciales
- `typescript/.env` - Variables de entorno

**Contenido:**
- Setup del entorno virtual
- Instalación de dependencias (openai, python-dotenv / openai, dotenv)
- Configuración de API key
- Primera llamada usando Responses API

---

#### `clase-02-cliente-reutilizable`
**Python:**
- `python/app/openai_client.py` - Cliente reutilizable
- `python/app/__init__.py`
- `python/main.py` - Actualizado para usar el cliente

**TypeScript:**
- `typescript/src/openaiClient.ts` - Cliente reutilizable
- `typescript/src/main.ts` - Actualizado

**Contenido:**
- Crear carpeta `app/`
- Función `generate_text()` reutilizable
- Separación de configuración y lógica
- Uso de `instructions` vs `input`

---

#### `clase-03-chat-completions`
**Python:**
- `python/app/openai_client.py` - Agregar función comparativa
- `python/main.py` - Demo de comparación

**TypeScript:**
- `typescript/src/openaiClient.ts` - Agregar función comparativa
- `typescript/src/main.ts` - Demo de comparación

**Contenido:**
- Función `generate_text_with_chat_completions()`
- Comparación entre Responses API y Chat Completions
- Diferencias: `instructions` vs `messages`, `output_text` vs `choices[0].message.content`

---

#### `clase-04-modelos-tokens-costos`
**Python:**
- `python/app/costs.py` - Función de estimación de costos
- `python/main.py` - Demo de cálculo de costos

**TypeScript:**
- `typescript/src/costs.ts` - Función de estimación de costos
- `typescript/src/main.ts` - Demo de cálculo de costos

**Contenido:**
- Función `estimate_cost(input_tokens, output_tokens)`
- Lectura del objeto `usage`
- Cálculo de costo aproximado
- Importancia de elegir el modelo correcto

---

#### `clase-05-base-web-fastapi`
**Python:**
- `python/app/server.py` - Servidor FastAPI inicial
- `python/requirements.txt` - Dependencias web
- `python/main.py` - Eliminado o redirigido

**TypeScript:**
- `typescript/src/server.ts` - Servidor Express inicial
- `typescript/package.json` - Dependencias web (express, multer, etc.)

**Contenido:**
- Instalación de FastAPI/Uvicorn o Express
- Endpoint GET `/` con formulario HTML
- Endpoint POST `/generate` para procesar ideas
- UI mínima para probar la integración

---

#### `clase-06-idea-a-brief`
**Python:**
- `python/app/openai_client.py` - Función `generate_brief()`
- `python/app/server.py` - Endpoint `/brief`

**TypeScript:**
- `typescript/src/openaiClient.ts` - Función `generateBrief()`
- `typescript/src/server.ts` - Endpoint `/brief`

**Contenido:**
- Función para transformar ideas desordenadas en briefs
- Endpoint POST `/brief` con formulario
- Prompt específico para generar briefs estructurados
- Salida en texto libre (preparación para structured outputs)

---

#### `clase-07-structured-outputs`
**Python:**
- `python/app/models.py` - Modelos Pydantic
- `python/app/openai_client.py` - Función `generate_structured_brief()`
- `python/requirements.txt` - Agregar pydantic

**TypeScript:**
- `typescript/src/models.ts` - Interfaces TypeScript
- `typescript/src/openaiClient.ts` - Función `generateStructuredBrief()`
- `typescript/package.json` - Agregar zod o similar

**Contenido:**
- Modelo `CampaignBrief` con Pydantic/Interfaces
- Uso de `client.responses.parse()`
- Schema definido en código
- Salida estructurada y tipada

---

#### `clase-08-contenido-por-canal`
**Python:**
- `python/app/models.py` - Modelo `ContentPiece`
- `python/app/openai_client.py` - Función `generate_content_piece()`
- `python/app/server.py` - Endpoint para generar contenido por canal

**TypeScript:**
- `typescript/src/models.ts` - Interface `ContentPiece`
- `typescript/src/openaiClient.ts` - Función `generateContentPiece()`
- `typescript/src/server.ts` - Endpoint correspondiente

**Contenido:**
- Modelo `ContentPiece` (channel, title, body, call_to_action)
- Función que toma brief y canal como input
- Generación de contenido adaptado a canal específico
- Reutilización del brief estructurado

---

#### `clase-09-analizar-imagen`
**Python:**
- `python/app/server.py` - Endpoint `/analyze-image` con UploadFile
- `python/requirements.txt` - Agregar python-multipart

**TypeScript:**
- `typescript/src/server.ts` - Endpoint `/analyze-image` con multer
- `typescript/package.json` - Agregar multer, @types/multer

**Contenido:**
- Endpoint para subir imágenes
- Conversión a base64
- Input multimodal (texto + imagen)
- Análisis visual de referencia

---

#### `clase-10-generar-imagen`
**Python:**
- `python/app/openai_client.py` - Función `generate_campaign_image()`
- `python/app/server.py` - Endpoint `/generate-image`

**TypeScript:**
- `typescript/src/openaiClient.ts` - Función `generateCampaignImage()`
- `typescript/src/server.ts` - Endpoint `/generate-image`

**Contenido:**
- Uso de `client.images.generate()`
- Prompt basado en el brief
- Generación de imagen promocional
- Integración de generación visual en el flujo

---

#### `clase-11-streaming`
**Python:**
- `python/app/openai_client.py` - Función `stream_long_content()`
- `python/app/server.py` - Endpoint `/stream-content` con StreamingResponse

**TypeScript:**
- `typescript/src/openaiClient.ts` - Función `streamLongContent()`
- `typescript/src/server.ts` - Endpoint `/stream-content` con streaming

**Contenido:**
- Uso de `client.responses.stream()`
- Generación de fragmentos (deltas)
- Endpoint con StreamingResponse
- Mejora de percepción de velocidad

---

#### `clase-12-voz-a-texto`
**Python:**
- `python/app/server.py` - Endpoint `/transcribe-audio`
- Manejo de archivos temporales para audio

**TypeScript:**
- `typescript/src/server.ts` - Endpoint `/transcribe-audio`
- Manejo de archivos temporales

**Contenido:**
- Endpoint para subir audio
- Uso de `client.audio.transcriptions.create()`
- Flujo: Audio -> Transcripción -> Idea -> Brief
- Captura de ideas sin escribir

---

#### `clase-13-texto-a-voz`
**Python:**
- `python/app/openai_client.py` - Función `text_to_speech()`
- `python/app/server.py` - Endpoint `/text-to-speech`

**TypeScript:**
- `typescript/src/openaiClient.ts` - Función `textToSpeech()`
- `typescript/src/server.ts` - Endpoint `/text-to-speech`

**Contenido:**
- Uso de `client.audio.speech.create()`
- Generación de audio desde texto
- Preview de guiones
- Validación de ritmo y naturalidad

---

#### `clase-14-function-calling`
**Python:**
- `python/app/openai_client.py` - Función `get_brand_voice()`
- Definición de tool `brand_voice_tool`
- Llamada con tools

**TypeScript:**
- `typescript/src/openaiClient.ts` - Función `getBrandVoice()`
- Definición de tool
- Llamada con tools

**Contenido:**
- Función local con datos internos
- Definición de tool con schema
- Uso de `tools` en la llamada
- Modelo solicita ejecutar tool

---

#### `clase-15-loop-tools`
**Python:**
- `python/app/openai_client.py` - Función `generate_with_brand_voice()`
- Loop completo: detectar, ejecutar, devolver, responder

**TypeScript:**
- `typescript/src/openaiClient.ts` - Función `generateWithBrandVoice()`
- Loop completo

**Contenido:**
- Detección de function_call
- Ejecución de función local
- Devolución de tool_outputs
- Uso de `previous_response_id`
- Respuesta final del modelo

---

#### `clase-16-costos-optimizacion`
**Python:**
- `python/app/openai_client.py` - Ejemplo de prompt caching
- Documentación de Batch API

**TypeScript:**
- `typescript/src/openaiClient.ts` - Ejemplo de prompt caching
- Documentación de Batch API

**Contenido:**
- Prompt caching con instrucciones estables
- Estrategia de prefijos repetidos
- Concepto de Batch API para procesamiento masivo
- JSONL structure para batch

---

#### `clase-17-errores-retries`
**Python:**
- `python/app/safe_client.py` - Wrapper `safe_openai_call()`
- Manejo de RateLimitError, APITimeoutError, APIError
- Estrategia de backoff exponencial

**TypeScript:**
- `typescript/src/safeClient.ts` - Wrapper `safeOpenAICall()`
- Manejo de errores con backoff

**Contenido:**
- Wrapper con reintentos
- Backoff exponencial (2^attempt)
- Manejo específico por tipo de error
- Logs de intentos
- Excepción final después de reintentos

---

#### `clase-18-deploy-guardrails`
**Python:**
- `python/requirements.txt` - Completo y actualizado
- `python/.env.example` - Template de variables
- `python/README.md` - Documentación completa
- `python/.gitignore` - Configurado correctamente

**TypeScript:**
- `typescript/package.json` - Completo y actualizado
- `typescript/.env.example` - Template de variables
- `typescript/README.md` - Documentación completa
- `typescript/.gitignore` - Configurado correctamente
- `typescript/tsconfig.json` - Configuración TypeScript

**Contenido:**
- `requirements.txt` / `package.json` completos
- Documentación de features
- Instrucciones de deploy
- Guardrails: API key segura, límites de tamaño, manejo de errores
- Documentación de modelos y precios
- README con instrucciones de uso

---

## Estrategia de Git

### Flujo de Trabajo

1. **Crear rama main inicial:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   ```

2. **Por cada clase:**
   ```bash
   git checkout -b clase-XX-nombre-clase
   # Implementar cambios de la clase
   git add .
   git commit -m "Clase XX: Nombre de la clase"
   git push origin clase-XX-nombre-clase
   ```

3. **Actualizar main al final:**
   ```bash
   git checkout main
   git merge clase-18-deploy-guardrails
   git push origin main
   ```

### Convención de Commits

- `Clase XX: [feature]` - Para implementaciones principales
- `Clase XX: [fix]` - Para correcciones
- `Clase XX: [refactor]` - Para mejoras de código
- `Clase XX: [docs]` - Para documentación

### Archivos .gitignore

**Python (.gitignore):**
```
.venv/
__pycache__/
*.pyc
.env
*.mp3
*.wav
*.png
*.jpg
.jpeg
.DS_Store
```

**TypeScript (.gitignore):**
```
node_modules/
dist/
.env
*.mp3
*.wav
*.png
*.jpg
.jpeg
.DS_Store
```

---

## Dependencias

### Python (requirements.txt - final)

```
openai
python-dotenv
fastapi
uvicorn
jinja2
python-multipart
pydantic
```

### TypeScript (package.json - final)

```json
{
  "name": "ai-content-operations-studio",
  "version": "1.0.0",
  "description": "AI Content Operations Studio - TypeScript version",
  "main": "dist/server.js",
  "scripts": {
    "dev": "ts-node src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js"
  },
  "dependencies": {
    "openai": "^4.x",
    "dotenv": "^16.x",
    "express": "^4.x",
    "multer": "^1.x",
    "zod": "^3.x"
  },
  "devDependencies": {
    "@types/express": "^4.x",
    "@types/multer": "^1.x",
    "@types/node": "^20.x",
    "ts-node": "^10.x",
    "typescript": "^5.x"
  }
}
```

---

## Checklist de Implementación

### Por Clase

- [ ] Clase 1: Setup y primera llamada
- [ ] Clase 2: Cliente reutilizable
- [ ] Clase 3: Chat Completions comparativo
- [ ] Clase 4: Costos y tokens
- [ ] Clase 5: Base web con FastAPI/Express
- [ ] Clase 6: Idea a brief
- [ ] Clase 7: Structured Outputs
- [ ] Clase 8: Contenido por canal
- [ ] Clase 9: Analizar imagen
- [ ] Clase 10: Generar imagen
- [ ] Clase 11: Streaming
- [ ] Clase 12: Voz a texto
- [ ] Clase 13: Texto a voz
- [ ] Clase 14: Function calling
- [ ] Clase 15: Loop de tools
- [ ] Clase 16: Optimización de costos
- [ ] Clase 17: Errores y retries
- [ ] Clase 18: Deploy y guardrails

### Por Stack

- [ ] Python: Todas las clases implementadas
- [ ] TypeScript: Todas las clases implementadas
- [ ] Ramas de Git creadas
- [ ] Rama main actualizada con versión final
- [ ] Documentación completa
- [ ] README en ambas carpetas

---

## Notas Importantes

1. **Secuencialidad:** Cada rama debe basarse en la anterior para mantener el historial limpio.

2. **TypeScript Paralelo:** La implementación en TypeScript debe ser equivalente pero adaptada a las convenciones de TypeScript/Node.js.

3. **Documentación:** Cada clase debe tener comentarios explicativos en el código.

4. **Testing:** Se recomienda probar cada feature antes de commitear.

5. **API Keys:** Nunca commitear archivos .env reales. Usar .env.example.

6. **Archivos Temporales:** Ignorar archivos generados (audio, imágenes) en .gitignore.

7. **Deploy:** La clase 18 debe incluir instrucciones específicas para Render, Railway o similar.

---

## Próximos Pasos

1. Inicializar repositorio Git
2. Crear estructura base de carpetas
3. Implementar Clase 1 en Python y TypeScript
4. Crear rama `clase-01-primera-llamada`
5. Continuar secuencialmente hasta la Clase 18
6. Actualizar rama main con el estado final
7. Verificar que ambas implementaciones funcionen correctamente
