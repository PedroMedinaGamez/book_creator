---
name: creadora-imagen-ia
description: Generates a Bo storybook illustration from the exact prompt prepared by bo-page-artist, sends Bo_image.jpg as a visual reference to the OpenAI Images API, downloads the PNG, and saves each revision in images/<continent>/<country>/vN/.
argument-hint: "Prompt aprobado, continente, país, monumento y, si es corrección, la versión anterior"
---

# Creadora de imagen IA

## Objetivo

Recibir el prompt final de `bo-page-artist`, enviarlo junto con `Bo_image.jpg` como referencia visual al endpoint oficial de edición de imágenes de OpenAI, descargar el PNG generado y guardarlo en el repositorio sin sobrescribir versiones anteriores.

Esta skill solo genera la ilustración. No crea marcos, texto editorial ni la página interior completa.

## Formato y fidelidad visual

- Todas las ilustraciones guardadas deben medir exactamente **1024 × 1085 px**, con una proporción ancho:alto aproximada de **0,944:1** (casi 17:18, casi cuadrada y solo un poco más alta que ancha). Esta proporción permite al compiler maximizar el área visible en una página KDP de 8,5 × 11 pulgadas sin recortar ni deformar la ilustración. No uses 2:3.
- La API genera un original cuadrado de **1024 × 1024 px**. El script lo centra en un lienzo blanco fijo de 1024 × 1085 px, añadiendo 30 px blancos arriba y 31 px abajo; no recorta ni deforma el dibujo. Rechaza respuestas de la API con otras dimensiones.
- En una página KDP de 2550 × 3300 px, el compiler debe colocar la ilustración completa dentro del mayor marco superior permitido por el margen interior/gutter y el margen exterior requeridos, conservando su proporción y sin recorte ni deformación. El compiler debe colocar la ilustración completa dentro del marco superior, conservando su proporción y sin recorte ni deformación.
- El prompt aprobado debe pedir la proporción final 1024 × 1085 px (0,944:1), y que el monumento o paisaje conserve su silueta, rasgos distintivos, escala y proporciones reales reconocibles, simplificadas para colorear. La representación debe ser más fiel a la realidad, no fotográfica ni cargada de texturas. Si el prompt pide 2:3 o deja ambigua la fidelidad del lugar, pide que `bo-page-artist` lo corrija; no reescribas ni completes el prompt por tu cuenta.

## Entradas necesarias

- Prompt completo y definitivo de `bo-page-artist`, sin campos pendientes.
- Continente, país y monumento de la ilustración.
- `Bo_image.jpg` del repositorio. Se envía en cada solicitud; el prompt determina si Bo debe aparecer en la escena.
- Para una corrección: archivo PNG de la versión anterior y prompt revisado por `bo-page-artist`.
- Variable local `OPENAI_API_KEY`, configurada fuera del chat.

No inventes ni completes el prompt artístico. Si faltan el prompt, el destino, la imagen de referencia requerida o la versión previa para una corrección, solicítalos antes de llamar a la API.

## Confirmación y privacidad

- Una generación o corrección realiza una solicitud de pago a la API de OpenAI, facturada aparte de ChatGPT. Pide confirmación explícita antes de cada llamada, salvo que el usuario haya autorizado claramente esa generación concreta en su mensaje actual o haya pedido explícitamente crear de una vez todas las ilustraciones de un lote definido.
- En un lote explícitamente autorizado, la instrucción del usuario cubre cada generación del conjunto especificado: no pidas aprobación individual entre imágenes y pasa `--confirm-paid-request` en cada llamada. Limita la autorización a ese lote; no incluye revisiones, nuevos destinos ni lotes futuros. Si no está claro qué imágenes abarca «todas», pregunta una sola vez por el alcance antes de generar.
- No leas, muestres, registres ni solicites la clave API en el chat. El script la obtiene de `OPENAI_API_KEY` y nunca debe imprimirla.
- Informa al usuario de que el prompt y las imágenes de referencia se enviarán a la API de OpenAI.
- Envía solo el prompt de la ilustración y las imágenes necesarias. No envíes el resto del repositorio, la historia completa ni datos personales.
- No realices una llamada de prueba facturable. Si falta la clave, detente e indica cómo configurarla localmente.

## Flujo de generación

1. Confirma que el prompt está completo y aprobado por `bo-page-artist`.
2. Adjunta siempre como imagen de referencia el `Bo_image.jpg` ubicado en la raíz del repositorio. El prompt determina si Bo aparece en la escena.
3. Si se trata de una corrección, adjunta también la última imagen generada del mismo monumento. Conserva los aspectos aprobados y cambia únicamente lo que el prompt de corrección solicite.
4. Comprueba que esta llamada está cubierta por una confirmación individual o por la autorización explícita del lote, y que `OPENAI_API_KEY` está disponible localmente.
5. Ejecuta el script de esta skill pasando el prompt, metadatos de continente/país/monumento, referencia de Bo y, para una corrección, la imagen previa.
6. El script llama a `POST https://api.openai.com/v1/images/edits` con un modelo GPT Image, `output_format=png`, calidad alta y tamaño cuadrado de API **1024 × 1024 px**. Comprueba esas dimensiones y centra el resultado sobre el lienzo blanco final de **1024 × 1085 px** sin recortar ni deformar. No cambies el prompt de artista al enviarlo.
7. El script valida y guarda el PNG en `images/<continente>/<país>/vN/<monumento>.png`. La primera imagen del monumento va a `v1`; la primera corrección a `v2`, y así sucesivamente. Cada monumento mantiene su propio contador de versiones. Nunca sobrescribas una versión existente.
8. Presenta la ruta devuelta y la imagen generada al usuario. No afirmes que la ilustración superó la revisión artística. Si la solicitud cubre un lote, genera primero todas las imágenes de ese lote sin detenerte entre ellas; después, preséntalas juntas para revisión. La aprobación visual de cada ilustración sigue siendo necesaria antes de componer su página final, pero no bloquea la generación de las demás imágenes del mismo lote.
9. Si la llamada o la descarga falla, informa el error claramente. No guardes una respuesta incompleta como PNG ni afirmes éxito. No reintentes automáticamente una solicitud fallida aunque forme parte de un lote.

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

El script lee `OPENAI_API_KEY` del entorno local y la utiliza unicamente para crear el encabezado de autenticacion de la solicitud; nunca la imprime ni la pasa como argumento. No pases la clave en la linea de comandos ni la escribas en archivos versionados. Guarda la imagen bajo `images/`. El modelo predeterminado es `gpt-image-2.5-sunburst`; solo cambia el modelo si el usuario lo solicita o si la API indica que ya no esta disponible.

Ejecuta el script con la herramienta `execute` disponible en el agente. Si el usuario pide explícitamente generar de una vez todas las ilustraciones de un conjunto definido, esa instrucción autoriza todas las llamadas de pago de ese conjunto: genera las imágenes en secuencia sin pedir aprobación individual y pasa `--confirm-paid-request` en cada llamada. La autorización se limita a ese lote; no incluye revisiones, nuevos destinos ni otros lotes. Si el alcance de «todas» no está definido, acláralo una sola vez antes de llamar a la API. Informa del lote y de que los prompts e imágenes de referencia necesarios se envían a OpenAI, sin interrumpirlo con confirmaciones por imagen.

No afirmes que la sesion carece de ejecucion sin intentar invocar esa herramienta; si no esta disponible, comunica la limitacion concreta observada. No inspecciones ni imprimas el valor de `OPENAI_API_KEY`: deja que el script compruebe su presencia y gestione el error de forma segura.

Instala el requisito de imagen solo si falta: `python -m pip install -r .github\skills\creadora-imagen-ia\requirements.txt`.


## Errores y límites

- Si la API devuelve un error HTTP, un rechazo de seguridad, una respuesta sin imagen o datos que no sean un PNG válido, explica el fallo y detente.
- Si la clave no está configurada o la cuenta no tiene acceso al modelo, no intentes usar otra clave ni otro servicio.
- No reintentes automáticamente solicitudes que puedan generar cargos. Pide autorización antes de volver a llamar.
- No marques la versión como aprobada; la aprobación artística corresponde al usuario tras la revisión de `bo-page-artist`.
- Consulta la documentación oficial vigente si cambian los modelos o los parámetros: [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation) y [Images edit API](https://developers.openai.com/api/reference/resources/images/methods/edit).
