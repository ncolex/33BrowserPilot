# Despliegue en Render.com + Neon Database

## Arquitectura

- **Aplicación**: Render.com (Docker)
- **Base de Datos**: Neon PostgreSQL (gratis, 500MB)
- **Outputs**: Disco persistente en Render (5GB)

## Paso 1: Crear la Base de Datos en Neon

1. **Ir a Neon**
   - Visitá https://neon.tech
   - Click en "Sign Up" (usá GitHub para más facilidad)

2. **Crear un nuevo proyecto**
   - Click en "New Project"
   - **Name**: `browserpilot-db`
   - **Region**: Us-West (Oregon) - misma que Render
   - Click en "Create Project"

3. **Obtener la DATABASE_URL**
   - En el dashboard del proyecto, vas a ver la "Connection String"
   - Copiá el string que dice algo como:
     ```
     postgresql://user:password@ep-xxx.us-west-2.aws.neon.tech/dbname?sslmode=require
     ```
   - Guardala para el próximo paso

4. **Configuración opcional**
   - Podés ver la base de datos desde el dashboard de Neon
   - Las tablas se crean automáticamente al iniciar la app

## Paso 2: Desplegar en Render

### Opción 1: Usando el Dashboard de Render (Recomendado)

1. **Crear una cuenta en Render**
   - Ir a https://render.com y registrarse

2. **Crear un nuevo Web Service**
   - Click en "New +" → "Web Service"
   - Conectar tu repositorio de GitHub

3. **Configurar el servicio**
   - **Name**: `browserpilot` (o el nombre que quieras)
   - **Region**: Oregon (us-west-2) - misma que Neon
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Docker`
   - **Docker Command**: (dejar vacío)

4. **Configurar Variables de Entorno**
   En la sección "Environment", agregar:
   
   | Key | Value |
   |-----|-------|
   | `GOOGLE_API_KEY` | `AIzaSyBDl98MXre7ecN9jW16EVltBlaf38awkdo` |
   | `DATABASE_URL` | (pegá el connection string de Neon) |
   | `SCRAPER_PROXIES` | `[]` (o tu configuración de proxies si tenés) |

5. **Configurar Disk (opcional pero recomendado)**
   - Click en "Add Disk"
   - **Name**: `outputs`
   - **Mount Path**: `/app/outputs`
   - **Size**: 5 GB (mínimo)

6. **Seleccionar Plan**
   - **Starter** ($7/mes) - recomendado para empezar
   - El plan free no soporta Docker

7. **Deploy**
   - Click en "Create Web Service"
   - Esperar a que se complete el despliegue (~5-10 minutos)

### Opción 2: Usando Render CLI

```bash
# Instalar Render CLI
npm install -g @render-cloud/renderctl

# Login
renderctl login

# Deploy usando el render.yaml
cd /home/ncx/BROPILOT/33BrowserPilot
renderctl up -f render.yaml
```

## Configuración del render.yaml

El archivo `render.yaml` ya está configurado con:
- Tipo: Web Service con Docker
- Región: Oregon
- Plan: Starter
- Health check: `/`
- Disco persistente para outputs

## Después del despliegue

1. **Verificar el deploy**
   - Ir al dashboard de Render
   - Ver los logs en tiempo real
   - Verificar que el health check pase

2. **Acceder a la aplicación**
   - La URL será algo como: `https://browserpilot-xxxx.onrender.com`

3. **Configurar dominio personalizado (opcional)**
   - En el dashboard → Settings → Custom Domain

## Variables de Entorno Requeridas

| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `GOOGLE_API_KEY` | ✅ Sí | API key de Google Gemini |
| `DATABASE_URL` | ✅ Sí | Connection string de Neon PostgreSQL |
| `SCRAPER_PROXIES` | ❌ No | Configuración de proxies (JSON array) |

## Costos Estimados

| Servicio | Plan | Costo |
|----------|------|-------|
| **Render** | Starter | $7/mes |
| **Render Disk** | 5GB | ~$0.50/mes |
| **Neon** | Free | $0/mes (500MB) |
| **Total** | | ~$7.50/mes |

## Endpoints de la API

### Jobs
- `POST /job` - Crear un nuevo job
- `GET /jobs` - Listar todos los jobs (con paginación)
- `GET /job/{job_id}` - Obtener detalles de un job
- `DELETE /job/{job_id}` - Eliminar un job
- `GET /download/{job_id}` - Descargar el resultado

### Streaming
- `GET /streaming/{job_id}` - Obtener info de streaming
- `POST /streaming/create/{job_id}` - Crear sesión de streaming
- `DELETE /streaming/{job_id}` - Limpiar sesión
- `WS /stream/{job_id}` - WebSocket para streaming

### Sistema
- `GET /stats` - Estadísticas del sistema
- `GET /proxy/stats` - Estadísticas de proxies
- `POST /proxy/reload` - Recargar proxies

## Notas Importantes

⚠️ **Importante**: Render no soporta el plan free para servicios Docker.

⚠️ **Importante**: Los servicios en el plan starter se duermen después de 15 minutos de inactividad. El primer request después de dormir puede tardar ~30 segundos.

⚠️ **Importante**: Neon tiene un límite de 500MB en el plan free. Si necesitás más espacio, considerá upgrade a Neon Pro ($19/mes).

## Troubleshooting

### El deploy falla
- Verificar los logs en el dashboard de Render
- Asegurarse de que el Dockerfile sea correcto
- Verificar que las variables de entorno estén configuradas
- Checkear que la DATABASE_URL de Neon sea correcta

### La aplicación no responde
- Verificar el health check en el dashboard
- Revisar los logs de errores
- Verificar que la GOOGLE_API_KEY sea válida
- Verificar que la conexión a Neon funcione

### Problemas de memoria
- El plan starter tiene 512MB RAM
- Si necesitás más, upgrade al plan Standard ($15/mes)

### La base de datos no conecta
- Verificar que la DATABASE_URL incluya `?sslmode=require`
- Checkear que la región de Neon sea la misma que Render (us-west-2)
- Verificar los logs de error de conexión
