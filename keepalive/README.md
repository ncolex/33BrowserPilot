# KeepAlive para Hugging Face Spaces - Netlify Functions

## Deploy en Netlify (100% GRATIS)

### Opción 1: Usando Netlify CLI (Recomendado)

```bash
# 1. Instalar dependencias
cd /home/ncx/BROPILOT/33BrowserPilot/keepalive
npm install

# 2. Login
npx netlify login

# 3. Init
npx netlify init

# 4. Deploy
npx netlify deploy --prod
```

### Opción 2: Desde GitHub

1. **Subí el código a GitHub** (ya está en el repo)
2. **Andá a Netlify**: https://app.netlify.com/new
3. **Importá el repo**: `ncolex/33BrowserPilot`
4. **Base directory**: `keepalive`
5. **Deploy**

### Configurar Variables de Entorno

En Netlify Dashboard:
1. **Site settings** → **Environment variables**
2. **Add variable**:
   - **Key**: `HF_SPACE_URL`
   - **Value**: `https://huggingface.co/spaces/ncolex/browserpilot`
3. **Save**

### Verificar el Schedule

1. **Functions** → **keepalive**
2. **Schedules** tab
3. Debería mostrar: `*/13 * * * *`

## Costo: **$0/mes**

- **Netlify Starter**: Gratis
- **Functions**: 125k invocaciones/mes (vos usás ~3300/mes)
- **Schedules**: Ilimitados

## URLs

- **Function**: `https://browserpilot-keepalive.netlify.app/.netlify/functions/keepalive`
- **Dashboard**: https://app.netlify.com/dashboard

## Test manual

```bash
curl https://browserpilot-keepalive.netlify.app/.netlify/functions/keepalive
```
