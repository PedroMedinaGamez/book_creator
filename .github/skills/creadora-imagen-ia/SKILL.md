---
name: creadora-imagen-ia
description: Generates a Bo storybook illustration from the exact prompt prepared by bo-page-artist, sends Bo_image.jpg as a visual reference to the OpenAI Images API, downloads the PNG, and saves each revision in images/<continent>/<country>/vN/.
argument-hint: "Prompt aprobado, continente, país, monumento y, si es corrección, la versión anterior"
---

# Creadora de imagen IA

## Objetivo

Recibir el prompt final de `bo-page-artist`, enviarlo junto con `Bo_image.jpg` como referencia visual al endpoint oficial de edición de imágenes de OpenAI, descargar el PNG generado y guardarlo en el repositorio sin sobrescribir versiones anteriores.

Esta skill solo genera la ilustración. No crea marcos, texto editorial ni la página interior completa.

## Entradas necesarias

- Prompt completo y definitivo de `bo-page-artist`, sin campos pendientes.
- Continente, país y monumento de la ilustración.
- `Bo_image.jpg` del repositorio. Se envía en cada solicitud; el prompt determina si Bo debe aparecer en la escena.
- Para una corrección: archivo PNG de la versión anterior y prompt revisado por `bo-page-artist`.
- Variable local `OPENAI_API_KEY`, configurada fuera del chat.

No inventes ni completes el prompt artístico. Si faltan el prompt, el destino, la imagen de referencia requerida o la versión previa para una corrección, solicítalos antes de llamar a la API.

## Confirmación y privacidad

- Una generación o corrección realiza una solicitud de pago a la API de OpenAI, facturada aparte de ChatGPT. Pide confirmación explícita antes de cada llamada, salvo que el usuario ya haya autorizado claramente esa generación concreta en su mensaje actual.
- No leas, muestres, registres ni solicites la clave API en el chat. El script la obtiene de `OPENAI_API_KEY` y nunca debe imprimirla.
- Informa al usuario de que el prompt y las imágenes de referencia se enviarán a la API de OpenAI.
- Envía solo el prompt de la ilustración y las imágenes necesarias. No envíes el resto del repositorio, la historia completa ni datos personales.
- No realices una llamada de prueba facturable. Si falta la clave, detente e indica cómo configurarla localmente.

## Flujo de generación

1. Confirma que el prompt está completo y aprobado por `bo-page-artist`.
2. Adjunta siempre como imagen de referencia el `Bo_image.jpg` ubicado en la raíz del repositorio. El prompt determina si Bo aparece en la escena.
3. Si se trata de una corrección, adjunta también la última imagen generada del mismo monumento. Conserva los aspectos aprobados y cambia únicamente lo que el prompt de corrección solicite.
4. Comprueba que se ha confirmado esta llamada con coste y que `OPENAI_API_KEY` está disponible localmente.
5. Ejecuta el script de esta skill pasando el prompt, metadatos de continente/país/monumento, referencia de Bo y, para una corrección, la imagen previa.
6. El script llama a `POST https://api.openai.com/v1/images/edits` con un modelo GPT Image, `output_format=png`, calidad alta y una imagen de salida vertical por defecto. No cambies el prompt de artista al enviarlo.
7. El script valida y guarda el PNG en `images/<continente>/<país>/vN/<monumento>.png`. La primera imagen del monumento va a `v1`; la primera corrección a `v2`, y así sucesivamente. Cada monumento mantiene su propio contador de versiones. Nunca sobrescribas una versión existente.
8. Presenta la ruta devuelta y la imagen generada al usuario. No afirmes que la ilustración superó la revisión artística; `bo-page-artist` debe inspeccionarla y pedir aprobación.
9. Si la llamada o la descarga falla, informa el error claramente. No guardes una respuesta incompleta como PNG ni afirmes éxito.

## Uso del script

Guarda el prompt completo en un archivo UTF-8 temporal y ejecuta desde la raíz del repositorio:

```powershell
python .github\skills\creadora-imagen-ia\scripts\create_image.py `
  --prompt-file "<ruta-al-prompt.txt>" `
  --continent "<continente>" `
  --country "<país>" `
  --monument "<monumento>" `
  --reference ".\Bo_image.jpg" `
  --confirm-paid-request
```

Para una corrección, añade la ruta del PNG anterior:

```powershell
  --previous-image ".\images\<continente>\<país>\v1\<monumento>.png"
```

El script usa `OPENAI_API_KEY` del entorno y guarda la imagen bajo `images/`. No pases la clave como argumento ni la escribas en archivos versionados. El modelo predeterminado es `gpt-image-2.5-sunburst`; solo cambia el modelo si el usuario lo solicita o si la API indica que ya no está disponible.

## Errores y límites

- Si la API devuelve un error HTTP, un rechazo de seguridad, una respuesta sin imagen o datos que no sean un PNG válido, explica el fallo y detente.
- Si la clave no está configurada o la cuenta no tiene acceso al modelo, no intentes usar otra clave ni otro servicio.
- No reintentes automáticamente solicitudes que puedan generar cargos. Pide autorización antes de volver a llamar.
- No marques la versión como aprobada; la aprobación artística corresponde al usuario tras la revisión de `bo-page-artist`.
- Consulta la documentación oficial vigente si cambian los modelos o los parámetros: [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation) y [Images edit API](https://developers.openai.com/api/reference/resources/images/methods/edit).
