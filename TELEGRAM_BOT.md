# 🤖 Telegram Bot Integration

## Bot: @Error33yobot

### Configuración Requerida

**En Hugging Face Spaces** (Settings → Variables and secrets):

| Type | Key | Value |
|------|-----|-------|
| Secret | `TELEGRAM_BOT_TOKEN` | `8246977072:AAHItyl6wYcrkNwTcj5Teu0lsVwTeMKZZqU` |
| Secret | `TELEGRAM_CHAT_ID` | (tu chat ID - ver abajo) |

**En GitHub Secrets** (Settings → Secrets and variables → Actions):

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | `8246977072:AAHItyl6wYcrkNwTcj5Teu0lsVwTeMKZZqU` |
| `TELEGRAM_CHAT_ID` | (tu chat ID - ver abajo) |

---

## Cómo obtener tu Chat ID

1. **Abrí Telegram**
2. **Buscá**: `@Error33yobot`
3. **Iniciá el bot**: Click en "Start" o mandale "hola"
4. **Ejecutá este comando**:
   ```bash
   curl -s "https://api.telegram.org/bot8246977072:AAHItyl6wYcrkNwTcj5Teu0lsVwTeMKZZqU/getUpdates" | python3 -m json.tool
   ```
5. **Buscá** en el resultado: `"chat": {"id": 123456789, ...}`
6. **Ese número** es tu `TELEGRAM_CHAT_ID`

---

## Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Mostrar ayuda y comandos disponibles |
| `/ping` | Verificar que el bot está activo |
| `/status` | Ver estado del sistema (jobs activos, proxies, etc.) |
| `/jobs` | Listar los últimos 5 jobs |

---

## Crear Jobs desde Telegram

Simplemente **enviá un mensaje** al bot con tu tarea:

```
Go to Hacker News and save the top 10 stories as JSON
```

El bot va a:
1. ✅ Crear el job
2. 📋 Confirmarte con el Job ID
3. 🔔 Avisarte cuando termine con el link de descarga

---

## Notificaciones Automáticas

### Job Started
```
🚀 Job Started
ID: abc123...
Task: Go to Hacker News...
Format: json
⏳ Processing...
```

### Job Completed
```
✅ Job Completed!
ID: abc123...
Format: json
📥 Download Result
```

### Job Failed
```
❌ Job Failed
ID: abc123...
Error: [error message]
```

### KeepAlive Alert
```
⚠️ KeepAlive Alert
🔴 HF Space health check failed!
Status: 503
The Space might be sleeping or down.
```

### KeepAlive Restored
```
✅ KeepAlive OK
🟢 HF Space health check passed!
Status: 200
The Space is awake and running.
```

---

## Flujo de Uso

1. **Configurá** las variables en HF Spaces y GitHub
2. **Iniciá** el bot en Telegram (`/start`)
3. **Enviá** tu tarea como mensaje
4. **Esperá** la notificación de completado
5. **Descargá** el resultado desde el link

---

## Ejemplos de Comandos

### Buscar en Google
```
Search for "AI engineers in San Francisco" on LinkedIn and save as CSV
```

### Extraer datos
```
Go to amazon.com and get the top 5 wireless headphones under $100
```

### Navegación compleja
```
Visit hackernews.com, click on "Ask HN", and save all posts from today
```

---

## Troubleshooting

### El bot no responde
- Verificá que `TELEGRAM_BOT_TOKEN` esté configurado
- Verificá que `TELEGRAM_CHAT_ID` sea correcto
- Revisá los logs del Space

### No llegan las notificaciones
- Verificá que el bot tenga permisos para enviarte mensajes
- Asegurate de haber iniciado el bot (`/start`)

### El keepalive no notifica
- Verificá los secrets de GitHub Actions
- Revisá el workflow en: https://github.com/ncolex/33BrowserPilot/actions

---

## Costo: **$0/mes**

- Telegram Bot API: Gratis
- GitHub Actions: 2000 min/mes (usás ~1)
- Total: $0
