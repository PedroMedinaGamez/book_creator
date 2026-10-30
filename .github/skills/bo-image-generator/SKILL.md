---
name: bo-image-generator
description: "Entrega al usuario el prompt final preparado por bo-page-artist para copiarlo en ChatGPT y generar allí la ilustración. No llama a ninguna API. Use when the user wants the image prompt to generate manually in ChatGPT."
argument-hint: "Prompt final de bo-page-artist"
---

# Bo Image Generator

## Objetivo

Entregar el prompt final de `bo-page-artist` para que el usuario lo copie en ChatGPT y genere la imagen manualmente. Esta skill no genera imágenes, no usa ninguna API y no requiere claves.

## Procedimiento

1. Recibe el prompt completo y definitivo de `bo-page-artist`.
2. Devuelve el prompt íntegro, sin resumirlo, traducirlo ni modificarlo, en un bloque de código fácil de copiar.
3. Si Bo aparece, añade fuera del bloque una indicación breve para adjuntar `Bo_image.jpg` como referencia visual en ChatGPT.
4. Detente y deja que el usuario haga la generación en ChatGPT. No pidas una API key, no afirmes que la imagen se generó y no solicites una ruta de descarga.

Si el prompt está incompleto o aún contiene campos entre corchetes, pide a `bo-page-artist` que lo complete antes de entregarlo.

## Importar una imagen (opcional)

Solo si el usuario vuelve con una imagen PNG descargada y pide expresamente guardarla en el repositorio, impórtala sin sobrescribir versiones existentes:

```powershell
python .github\skills\bo-image-generator\scripts\import_image.py `
  --source "<ruta-al-PNG-descargado>" `
  --continent "<continente>" `
  --country "<país>" `
  --monument "<monumento>"
```

El script guarda el archivo en `images/<continente>/<país>/<monumento>_vN.png`. Esta importación es opcional; el flujo principal termina al entregar el prompt.
