# Curso de OpenAI API — AI Content Operations Studio

Repositorio del curso de **OpenAI API**. Construimos un **AI Content Operations Studio**:
una aplicación que transforma ideas desordenadas en piezas de contenido listas para usar.

El foco del curso es **dominar la OpenAI API** (Responses API, multimodalidad, tools,
structured outputs, streaming, costos y prácticas básicas de producción). La interfaz es mínima.

## Stack principal (lo que vemos en clase)

- Python
- OpenAI Python SDK
- FastAPI + Uvicorn
- Jinja2 / HTML simple
- Pydantic para schemas
- python-dotenv

> El stack principal del curso es **Python**. La carpeta `typescript/` replica el mismo
> ejemplo en TypeScript para quienes prefieren ese lenguaje, pero en las clases solo se muestra Python.

## Estructura del repositorio

```
.
├── python/        # Implementación principal (la que se muestra en el curso)
├── typescript/    # Misma app, equivalente en TypeScript (referencia)
├── PLAN_PROYECTO.md
└── README.md
```

## Cómo está organizado el repositorio por clases

El curso tiene 18 clases. Cada clase tiene **dos ramas**:

- `clase-XX-inicio`: el estado del proyecto **al empezar** la clase (igual a como terminó la clase anterior).
- `clase-XX-final`: el estado del proyecto **al terminar** la clase.

La rama `main` contiene el estado **final del curso** (igual a `clase-18-final`).

Para seguir una clase:

```bash
git checkout clase-06-inicio   # empiezas desde aquí
# ... sigues la clase ...
git checkout clase-06-final    # comparas con el resultado esperado
```

## Mapa de clases

| Clase | Título | Foco |
|------|--------|------|
| 1 | Tu primera llamada a OpenAI API con Python | Fundamentos de API |
| 2 | Crear un cliente reutilizable para OpenAI | Fundamentos de API |
| 3 | Chat Completions en código heredado | Fundamentos de API |
| 4 | Modelos, tokens y costo por request | Fundamentos de API |
| 5 | Crear la base web con FastAPI | Brief y contenido |
| 6 | De idea desordenada a brief de campaña | Brief y contenido |
| 7 | Structured Outputs con Pydantic | Brief y contenido |
| 8 | Generar contenido por canal | Brief y contenido |
| 9 | Analizar una imagen de referencia | Imagen, streaming y voz |
| 10 | Generar una imagen para campaña | Imagen, streaming y voz |
| 11 | Streaming para generaciones largas | Imagen, streaming y voz |
| 12 | Voz a texto para capturar ideas | Imagen, streaming y voz |
| 13 | Texto a voz para escuchar un guion | Imagen, streaming y voz |
| 14 | Function calling con reglas de marca | Function calling y tools |
| 15 | Completar el loop de tools | Function calling y tools |
| 16 | Costos: prompt caching y Batch API | Producción y deploy |
| 17 | Errores, retries y rate limits | Producción y deploy |
| 18 | Deploy y guardrails de producción | Producción y deploy |

## Requisitos previos

- Una cuenta de OpenAI y una API key.
- Python 3.10+ (para el stack principal).
- Node.js 18+ (solo si quieres correr la versión de `typescript/`).

> **Nota sobre modelos:** el curso usa nombres de modelo como `gpt-5.4` (y variantes).
> Los nombres de modelo y los precios cambian con el tiempo: verifica siempre la
> documentación oficial de OpenAI y ajusta el modelo/configuración antes de ejecutar en producción.
