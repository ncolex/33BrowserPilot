# Deploy en Render.com - Instrucciones

## 🚀 Deploy Rápido

### Paso 1: Entrá a Render
https://render.com

### Paso 2: Crear Web Service
1. **New +** → **Web Service**
2. Conectá tu GitHub
3. Seleccioná: `ncolex/33BrowserPilot`

### Paso 3: Configuración

**Basic Settings:**
- **Name**: `browserpilot`
- **Region**: Oregon (us-west-2)
- **Branch**: `main`
- **Root Directory**: (vacío)
- **Runtime**: `Docker`
- **Docker Command**: (vacío)

**Environment Variables:**
```
GOOGLE_API_KEY=AIzaSyBDl98MXre7ecN9jW16EVltBlaf38awkdo
DATABASE_URL=postgresql://neondb_owner:npg_obFVM76KLule@ep-twilight-field-aiwca4xu.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
TELEGRAM_BOT_TOKEN=8246977072:AAHItyl6wYcrkNwTcj5Teu0lsVwTeMKZZqU
TELEGRAM_CHAT_ID=5858991844
PYTHONUNBUFFERED=1
```

**Disk:**
- Click en **Add Disk**
- **Name**: `outputs`
- **Mount Path**: `/app/outputs`
- **Size**: `5 GB`

### Paso 4: Plan
- **Starter Plan**: $7/mes
- (El plan free no soporta Docker)

### Paso 5: Deploy
- Click en **Create Web Service**
- Esperá 5-10 minutos
- ¡Listo!

---

## 📍 URL de tu servicio

Una vez desplegado:
```
https://browserpilot-<random>.onrender.com
```

---

## ✅ Todo incluido

- ✅ Google Gemini IA
- ✅ Base de datos Neon (gratis)
- ✅ Bot de Telegram
- ✅ KeepAlive automático (GitHub Actions)
- ✅ Disco persistente para outputs

---

## 💰 Costo Total

| Servicio | Costo |
|----------|-------|
| Render Starter | $7/mes |
| Render Disk 5GB | ~$0.50/mes |
| Neon Database | $0 |
| GitHub Actions | $0 |
| Telegram | $0 |
| **TOTAL** | **~$7.50/mes** |

---

## 🔗 Links

- **Render Dashboard**: https://dashboard.render.com
- **Tu Repo**: https://github.com/ncolex/33BrowserPilot
- **Neon DB**: https://console.neon.tech
