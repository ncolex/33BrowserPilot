# KeepAlive para Hugging Face Spaces - GitHub Actions

## ¿Qué es esto?

GitHub Actions ejecuta un workflow cada **13 minutos** que hace ping a tu Hugging Face Space para evitar que se duerma.

## Configuración

### 1. Agregar el secreto en GitHub

1. Andá a tu repo: https://github.com/ncolex/33BrowserPilot
2. **Settings** → **Secrets and variables** → **Actions**
3. **New repository secret**
4. **Name**: `HF_SPACE_URL`
5. **Value**: `https://huggingface.co/spaces/ncolex/browserpilot`
6. **Add secret**

### 2. ¡Listo!

El workflow se ejecuta automáticamente cada 13 minutos.

## Verificación

- **Actions tab**: https://github.com/ncolex/33BrowserPilot/actions
- **Workflow**: "Keep HF Space Awake"
- **Runs**: Cada ~13 minutos

## Trigger manual

Podés ejecutar manualmente el workflow:
1. Andá a **Actions** → **Keep HF Space Awake**
2. **Run workflow** → **Run workflow**

## Costo: **$0/mes**

- **GitHub Actions**: 2000 minutos/mes gratis
- **Este workflow**: ~1 minuto/mes (segundos realmente)
- **Total usado**: <1% del límite gratis

## Notas

- Los workflows se pueden ejecutar cada 5 minutos como mínimo
- 13 minutos es un buen balance (no muy frecuente, no muy raro)
- El workflow falla si el Space está caído (esperado)
