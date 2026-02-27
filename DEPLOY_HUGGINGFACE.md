# Hugging Face Spaces Deployment

## Deploy en Hugging Face Spaces (100% GRATIS)

### Paso 1: Crear cuenta en Hugging Face

1. Ir a https://huggingface.co
2. Click en "Sign Up" (usá GitHub para más facilidad)

### Paso 2: Crear un nuevo Space

1. Click en tu avatar → **"New Space"**
2. Configurar el Space:
   - **Space name**: `browserpilot` (o el nombre que quieras)
   - **License**: MIT
   - **SDK**: **Docker**
   - **Visibility**: Public (o Private si querés)
3. Click en **"Create Space"**

### Paso 3: Conectar el repositorio de GitHub

1. En el dashboard del Space, vas a ver **"Files"**
2. Click en **"Import from GitHub"** (o **"Add file"** → **"Import from GitHub"**)
3. Autorizá Hugging Face a acceder a tu GitHub
4. Seleccioná el repositorio: `ncolex/33BrowserPilot`
5. Click en **"Import"**

### Paso 4: Configurar las Variables de Entorno

1. En el Space, andá a **"Settings"** (pestaña de arriba)
2. Bajá hasta **"Variables and secrets"**
3. Agregá las siguientes variables:

| Type | Key | Value |
|------|-----|-------|
| Secret | `GOOGLE_API_KEY` | `AIzaSyBDl98MXre7ecN9jW16EVltBlaf38awkdo` |
| Secret | `DATABASE_URL` | `postgresql://neondb_owner:npg_obFVM76KLule@ep-twilight-field-aiwca4xu.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require` |
| Variable | `PYTHONUNBUFFERED` | `1` |

**Para agregar cada una:**
- Click en **"New secret"** o **"New variable"**
- Completá el nombre y valor
- Click en **"Save"**

### Paso 5: Esperar el deploy

1. Hugging Face va a empezar a construir el Docker automáticamente
2. El estado va a cambiar: `Building` → `Running`
3. Puede tardar 5-10 minutos la primera vez

### Paso 6: ¡Listo!

Una vez que diga **"Running"**, tu BrowserPilot está disponible en:

```
https://huggingface.co/spaces/tu-usuario/browserpilot
```

## Notas Importantes

⚠️ **Recursos limitados**: Los Spaces free tienen 2 vCPU y 16GB RAM, pero son compartidos.

⚠️ **Se duerme**: Después de ~48 horas de inactividad, el Space se duerme. El primer request puede tardar 1-2 minutos.

⚠️ **Sin GPU**: El plan free no incluye GPU, solo CPU.

⚠️ **Storage temporal**: Los archivos en `/app/outputs` se pierden cuando el Space se reinicia. Para storage persistente, necesitás usar Hugging Face Datasets o un servicio externo.

## Actualizar el Space

Cada vez que hagas push a GitHub:

```bash
cd /home/ncx/BROPILOT/33BrowserPilot
git push origin main
```

Hugging Face va a detectar los cambios y redeployar automáticamente.

## Troubleshooting

### El Space no arranca
- Revisá los logs en la pestaña **"Logs"**
- Verificá que la `GOOGLE_API_KEY` esté configurada
- Checkeá que el Dockerfile sea correcto

### Error de memoria
- El Space free tiene límites de memoria
- Intentá reducir el uso de memoria en el código
- Considerá upgrade al plan Pro ($9/mes) si necesitás más recursos

### Los archivos no persisten
- Los Spaces no tienen storage persistente en el plan free
- Para guardar archivos permanentemente, usá:
  - Hugging Face Datasets
  - Un servicio externo (S3, Google Drive, etc.)
  - La base de datos Neon para metadata

## Opcional: Agregar storage persistente

Para guardar los outputs permanentemente, podés usar Hugging Face Datasets:

1. Crear un Dataset en Hugging Face
2. Montarlo en el Space desde Settings → Datasets
3. Guardar los archivos en `/datasets/tu-usuario/tu-dataset`
