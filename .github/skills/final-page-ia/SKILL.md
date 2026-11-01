---
name: final-page-ia
description: Sends the exact prompt from bo-page-compiler and its identified approved illustration PNG to the OpenAI Images API to create the full page with text, then saves pages as pages/<continent>/page_<N>.vN.png.
argument-hint: "Entrega del compiler: prompt completo, texto exacto, ruta exacta de ilustración, continente y número de página"
---

# Final Page IA

## Objetivo

Crear la página interior completa mediante la API de imágenes de OpenAI usando:

1. el prompt final y completo de `bo-page-compiler`, que debe contener el texto aprobado de la página;
2. el archivo PNG exacto de ilustración aprobado e identificado por el compiler.

Guardar cada resultado en `pages/<continente>/page_<N>.v<M>.png`. La primera generación usa `v1`; cada corrección crea la siguiente versión libre, sin sobrescribir páginas anteriores.

## Entradas obligatorias

- Prompt completo de `bo-page-compiler`, sin marcadores ni placeholders.
- Texto aprobado exacto de la página, en archivo de texto para comprobar que está incluido literalmente en el prompt.
- Ruta relativa exacta de la ilustración aprobada, incluyendo continente, país y versión de imagen, por ejemplo `images/europe/france/v2/eiffel-tower.png`.
- Continente y número de página.
- PNG de página anterior para correcciones.
- `OPENAI_API_KEY` configurada localmente.

No selecciones por tu cuenta una ilustración distinta o una versión más reciente: usa exactamente la ruta que especificó el compiler. Confirma que el archivo existe y es un PNG válido. Rechaza un prompt si no incluye literalmente el texto aprobado completo, conserva sus saltos de párrafo o todavía tiene instrucciones de plantilla sin completar. Si falta algún insumo, detente y solicítalo.

## Confirmación y privacidad

- Cada generación o corrección puede tener coste API. Solicita confirmación explícita antes de cada llamada, salvo autorización clara para esa llamada concreta en el mensaje actual.
- Informa que el prompt y las imágenes de referencia se enviarán a la API de OpenAI.
- Envía solo el prompt, la ilustración exacta y, para una corrección, la versión anterior de esa página.
- No leas, muestres, registres ni solicites la clave API en el chat. El script la obtiene de `OPENAI_API_KEY`.
- No reintentes una solicitud fallida automáticamente; pide nueva autorización antes de volver a llamar.

## Flujo

1. Comprueba el prompt y la coincidencia literal del texto con `--expected-text-file`.
2. Comprueba que la ruta de ilustración indicada por el compiler existe. Envía ese PNG como referencia de composición, sin sustituirlo por `Bo_image.jpg` ni por otro destino.
3. En una corrección, incluye la versión anterior de la página como segunda imagen de referencia y conserva todos los detalles ya aprobados salvo los cambios pedidos.
4. Después de la confirmación, ejecuta `scripts/create_final_page.py` con el prompt, texto, ilustración exacta, continente, número de página y, si corresponde, página anterior.
5. El script utiliza la API oficial de edición de imágenes de OpenAI, guarda el PNG en la siguiente versión libre y adapta cada página al mismo lienzo fijo de **2550 × 3300 px, 300 DPI** (8.5 × 11 pulgadas), conservando la proporción y sin recortar contenido. No altera ni inventa texto a posteriori.
6. Presenta la ruta exacta creada y la imagen para revisión. No marques la página como aprobada ni continúes hasta que `bo-page-quality-auditor` la audite y el usuario la apruebe.
7. Si la página falla por texto, composición, resolución o cualquier otro defecto, pide al compiler que revise el prompt si es necesario y genera una nueva versión. Cada intento usa una versión mayor; una página fallida no se borra ni se incluye en el PDF.

## Uso del script

```powershell
python .github\skills\final-page-ia\scripts\create_final_page.py `
  --prompt-file "<ruta-al-prompt-completo.txt>" `
  --expected-text-file "<ruta-al-texto-aprobado.txt>" `
  --illustration ".\images\<continente>\<país>\v1\<monumento>.png" `
  --continent "<continente>" `
  --page-number 1 `
  --confirm-paid-request
```

Para una corrección, añade:

```powershell
  --previous-page ".\pages\<continente>\page_1.v1.png"
```

Todas las páginas deben tener el mismo tamaño objetivo: **2550 × 3300 píxeles a 300 DPI**. El script pide a la API un raster vertical de alta resolución y lo normaliza al lienzo de salida con remuestreo de alta calidad y metadatos de 300 DPI. Verifica las dimensiones finales; no des por supuesto que el modelo respetó el texto.

## Límites

- No crear ni cambiar la historia, el texto aprobado, la ilustración original o el diseño definido por el compiler.
- No afirmar que el texto de una imagen generativa es exacto hasta que el auditor lo compruebe visualmente.
- No enviar una página a `bo-kdp-formatter` sin resultado `PASS` del auditor y aprobación del usuario para esa misma versión.
- Si la página generada no puede normalizarse sin deformar la relación de aspecto, falla en lugar de recortar contenido importante.
