# Despliegue en Render.com

## Pasos para desplegar

### Opción 1: Usando el Dashboard de Render (Recomendado)

1. **Crear una cuenta en Render**
   - Ir a https://render.com y registrarse

2. **Crear un nuevo Web Service**
   - Click en "New +" → "Web Service"
   - Conectar tu repositorio de GitHub

3. **Configurar el servicio**
   - **Name**: `browserpilot` (o el nombre que quieras)
   - **Region**: Oregon (us-west-2) - recomendado para mejor performance
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Docker`
   - **Docker Command**: (dejar vacío)

4. **Configurar Variables de Entorno**
   En la sección "Environment", agregar:
   
   | Key | Value |
   |-----|-------|
   | `GOOGLE_API_KEY` | `AIzaSyBDl98MXre7ecN9jW16EVltBlaf38awkdo` |
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
| `SCRAPER_PROXIES` | ❌ No | Configuración de proxies (JSON array) |

## Costos Estimados

- **Starter Plan**: $7/mes
- **Disco 5GB**: ~$0.50/mes
- **Total**: ~$7.50/mes

## Notas Importantes

⚠️ **Importante**: Render no soporta el plan free para servicios Docker.

⚠️ **Importante**: Los servicios en el plan starter se duermen después de 15 minutos de inactividad. El primer request después de dormir puede tardar ~30 segundos.

## Troubleshooting

### El deploy falla
- Verificar los logs en el dashboard de Render
- Asegurarse de que el Dockerfile sea correcto
- Verificar que las variables de entorno estén configuradas

### La aplicación no responde
- Verificar el health check en el dashboard
- Revisar los logs de errores
- Verificar que la GOOGLE_API_KEY sea válida

### Problemas de memoria
- El plan starter tiene 512MB RAM
- Si necesitás más, upgrade al plan Standard ($15/mes)
