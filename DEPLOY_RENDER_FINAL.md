# Deploy en Render.com

## Opción 1: Usando Render Dashboard (Recomendado)

### Paso 1: Crear cuenta en Render
1. Entrá a https://render.com
2. Sign up con GitHub (más fácil)

### Paso 2: Crear nuevo Web Service
1. Click en **"New +"** → **"Web Service"**
2. Conectá el repositorio: `ncolex/33BrowserPilot`
3. Configurá:
   - **Name**: `browserpilot`
   - **Region**: Oregon (us-west-2)
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Docker`
   - **Docker Command**: (dejar vacío)

### Paso 3: Configurar Variables de Entorno
En la sección "Environment", agregá:

| Key | Value |
|-----|-------|
| `GOOGLE_API_KEY` | `AIzaSyBDl98MXre7ecN9jW16EVltBlaf38awkdo` |
| `DATABASE_URL` | `postgresql://neondb_owner:npg_obFVM76KLule@ep-twilight-field-aiwca4xu.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require` |
| `TELEGRAM_BOT_TOKEN` | `8246977072:AAHItyl6wYcrkNwTcj5Teu0lsVwTeMKZZqU` |
| `TELEGRAM_CHAT_ID` | `5858991844` |
| `PYTHONUNBUFFERED` | `1` |

### Paso 4: Configurar Disco
1. Click en **"Add Disk"**
2. **Name**: `outputs`
3. **Mount Path**: `/app/outputs`
4. **Size**: 5 GB

### Paso 5: Seleccionar Plan
- **Plan**: Starter ($7/mes)
- El plan free no soporta Docker

### Paso 6: Deploy
1. Click en **"Create Web Service"**
2. Esperar 5-10 minutos
3. ¡Listo! URL: `https://browserpilot-xxxx.onrender.com`

---

## Opción 2: Usando Render CLI

```bash
# Instalar Render CLI
npm install -g @render-cloud/renderctl

# Login
renderctl login

# Deploy
cd /home/ncx/BROPILOT/33BrowserPilot
renderctl up -f render.yaml
```

---

## Costos

| Servicio | Costo |
|----------|-------|
| Render Starter | $7/mes |
| Render Disk 5GB | ~$0.50/mes |
| Neon Database | $0 (free 500MB) |
| **TOTAL** | ~$7.50/mes |

---

## Endpoints de la API

- `POST /job` - Crear job
- `GET /jobs` - Listar jobs
- `GET /job/{job_id}` - Ver job
- `DELETE /job/{job_id}` - Eliminar job
- `GET /download/{job_id}` - Descargar resultado
- `GET /stats` - Estadísticas
- `WS /ws/{job_id}` - WebSocket para updates
- `WS /stream/{job_id}` - Streaming del navegador

---

## Comandos de Telegram

El bot `@Error33yobot` responde a:
- `/start` - Ayuda
- `/status` - Estado del sistema
- `/jobs` - Jobs recientes
- `/ping` - Verificar bot
- Enviar mensaje - Crea un job automáticamente

---

## Troubleshooting

### El deploy falla
- Verificar logs en Render Dashboard
- Checkear que el Dockerfile sea correcto
- Verificar variables de entorno

### La app no responde
- Verificar health check en Render Dashboard
- Revisar logs de error
- Verificar que GOOGLE_API_KEY sea válida

### Problemas de memoria
- Starter plan tiene 512MB RAM
- Upgrade a Standard ($15/mes) si necesitás más
