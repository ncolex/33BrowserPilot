# KeepAlive para Hugging Face Spaces

## ¿Qué es esto?

Este es un cron job gratuito que hace ping a tu Hugging Face Space cada **13 minutos** para evitar que se duerma.

## Deploy en Vercel (100% GRATIS)

### Opción 1: Desde la CLI de Vercel

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
cd /home/ncx/BROPILOT/33BrowserPilot/keepalive
vercel --prod
```

### Opción 2: Desde GitHub

1. **Subí este folder a un repo separado** (o al mismo en una carpeta)
2. **Andá a Vercel**: https://vercel.com/new
3. **Importá el repo**
4. **Configurá la variable de entorno**:
   - `HF_SPACE_URL` = `https://huggingface.co/spaces/ncolex/browserpilot`
5. **Deploy**

### Configurar el Cron

Una vez desplegado:

1. Andá a tu proyecto en Vercel
2. **Settings** → **Cron Jobs**
3. **Create Cron Job**
4. **Schedule**: `*/13 * * * *` (cada 13 minutos)
5. **URL**: `/api/keepalive`

O simplemente usá el `vercel.json` que ya incluye la configuración del cron.

## Variables de Entorno

En Vercel, configurá:

| Variable | Valor |
|----------|-------|
| `HF_SPACE_URL` | `https://huggingface.co/spaces/ncolex/browserpilot` |

## Costo: **$0/mes**

- **Vercel Hobby Plan**: Gratis
- **Cron jobs**: 100 gratis/mes (vos usás ~67/mes)
- **Funciones serverless**: 100GB-hrs/mes

## Verificación

Una vez configurado:

1. **Logs**: https://vercel.com/dashboard/activity
2. **Cron executions**: Settings → Cron Jobs
3. **Test manual**: `https://tu-proyecto.vercel.app/api/keepalive`

## Alternativa: Netlify Functions

Si preferís Netlify:

```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Init
netlify init

# Deploy
netlify deploy --prod
```

Configurar `netlify.toml`:

```toml
[functions]
  directory = "api"

[schedules]
  [schedules.keepalive]
    function = "keepalive"
    cron = "*/13 * * * *"
```

## Notas

- El cron job hace un **GET simple** al Space
- No consume recursos significativos
- Mantiene el Space "despierto" indefinidamente
- Funciona con cualquier Hugging Face Space Docker
