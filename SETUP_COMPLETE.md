# 🚀 BrowserPilot - Configuración Lista

## ✅ Lo que ya está hecho:

1. **Base de datos Neon creada**
   - Proyecto: `browserpilot-db`
   - ID: `late-king-86238640`
   - Región: `aws-us-east-1`
   - ✅ Conectada y lista para usar

2. **Código actualizado en GitHub**
   - Repo: https://github.com/ncolex/33BrowserPilot
   - ✅ Con integración a PostgreSQL
   - ✅ Endpoints para listar jobs: `GET /jobs`

3. **Variables configuradas localmente**
   - `GOOGLE_API_KEY`: ✅ Configurada
   - `DATABASE_URL`: ✅ Configurada

---

## 📋 Lo que tenés que hacer AHORA en Hugging Face:

### Paso 1: Crear el Space
1. Entrá a https://huggingface.co/spaces
2. Click en **"Create new Space"**
3. Completar:
   - **Space name**: `browserpilot`
   - **License**: MIT
   - **SDK**: **Docker** ⚠️ (¡importante!)
   - **Visibility**: Public
4. **Create Space**

### Paso 2: Importar desde GitHub
1. En el Space, click en **"Import from GitHub repo"**
2. Autorizá Hugging Face a acceder a tu GitHub
3. Seleccioná: `ncolex/33BrowserPilot`
4. **Import**

### Paso 3: Configurar Variables (Settings → Variables and secrets)

**Secrets:**
```
GOOGLE_API_KEY = AIzaSyBDl98MXre7ecN9jW16EVltBlaf38awkdo
DATABASE_URL = postgresql://neondb_owner:npg_obFVM76KLule@ep-twilight-field-aiwca4xu.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

**Variables:**
```
PYTHONUNBUFFERED = 1
```

### Paso 4: Esperar el deploy
- El build tarda **5-10 minutos**
- Cuando diga **"Running"**, ¡está listo!
- URL: `https://huggingface.co/spaces/tu-usuario/browserpilot`

---

## 🎯 URLs útiles:

| Servicio | URL |
|----------|-----|
| **GitHub Repo** | https://github.com/ncolex/33BrowserPilot |
| **Neon Dashboard** | https://console.neon.tech |
| **Hugging Face Spaces** | https://huggingface.co/spaces |

---

## 📊 Endpoints de la API (una vez desplegado):

```bash
# Crear un job
curl -X POST https://huggingface.co/spaces/tu-usuario/browserpilot/job \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Go to Hacker News and save top stories as JSON", "format": "json"}'

# Listar jobs
curl https://huggingface.co/spaces/tu-usuario/browserpilot/jobs

# Ver stats
curl https://huggingface.co/spaces/tu-usuario/browserpilot/stats
```

---

## 💰 Costo: $0/mes

- **Hugging Face Spaces**: 100% gratis
- **Neon Database**: 100% gratis (500MB)
- **Total**: $0/mes

---

## ⚠️ Importante:

1. Los **Secrets** en HF no se ven en la UI, solo se usan internamente
2. La **DATABASE_URL** guarda el historial de jobs permanentemente
3. Los archivos en `/outputs` **NO persisten** si el Space se reinicia
4. El Space se **duerme** después de ~48h de inactividad

---

## 🔧 Comandos útiles de Neon CLI:

```bash
# Ver proyectos
neonctl projects list

# Ver connection string
neonctl connection-string --project-id late-king-86238640

# Ver branches
neonctl branches list --project-id late-king-86238640

# Ver queries (si está habilitado)
neonctl operations list --project-id late-king-86238640
```
