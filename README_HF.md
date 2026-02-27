---
title: BrowserPilot
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# BrowserPilot - AI-Powered Browser Automation

Este espacio de Hugging Face ejecuta BrowserPilot, un navegador automatizado con IA que usa Google Gemini para navegar sitios web y extraer datos.

## Cómo usar

1. Agregá tu `GOOGLE_API_KEY` en los **Settings** de este Space (Variables and secrets)
2. Opcional: agregá `DATABASE_URL` de Neon para guardar el historial de jobs
3. El frontend estará disponible en la URL de este Space

## Endpoints de la API

- `POST /job` - Crear un nuevo job
- `GET /jobs` - Listar todos los jobs
- `GET /download/{job_id}` - Descargar resultado
- `WS /stream/{job_id}` - Streaming del navegador

## Ver código fuente

https://github.com/ncolex/33BrowserPilot
