---
name: final-page-ia
description: Sends the exact prompt from bo-page-compiler and its identified approved illustration PNG to the OpenAI Images API to create full pages with text. Supports explicit full-book batches, processing pages sequentially without intermediate approvals.
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

No selecciones por tu cuenta una ilustración distinta o una versión más reciente: usa exactamente la ruta que especificó el compiler. Confirma que el archivo existe y es un PNG válido. Rechaza un prompt si no incluye literalmente el texto aprobado completo, conserva sus saltos de párrafo o todavía tiene instrucciones de plantilla sin completar. En modo individual, si falta algún insumo, detente y solicítalo; en modo lote, marca esa página como bloqueada y continúa con las demás páginas elegibles, sin interrumpir el lote.

## Confirmación y privacidad

- Cada generación o corrección puede tener coste API. Solicita confirmación explícita antes de cada llamada, salvo autorización clara para esa llamada concreta en el mensaje actual o una petición explícita de maquetar/generar todas las páginas de un lote definido.
- Interpreta «haz/maqueta/genera todas las páginas», «el libro completo» o una petición equivalente como autorización explícita del lote cuando el plan define su alcance. Esta autorización cubre una llamada inicial por cada página elegible cuyo texto e ilustración estén aprobados.
- En modo lote, trabaja página por página y en secuencia, pero no solicites aprobación ni confirmación entre páginas, ni esperes aprobación de cada resultado para empezar la siguiente. No interrumpas el lote para mostrar avances o pedir permiso para continuar.
- Al terminar, presenta juntas todas las páginas generadas y sus resultados de auditoría, y solicita una sola aprobación del lote. La autorización del lote no cubre correcciones, páginas añadidas después ni reintentos de llamadas fallidas; solicita nueva autorización para ellas.
- Informa que el prompt y las imágenes de referencia se enviarán a la API de OpenAI.
- Envía solo el prompt, la ilustración exacta y, para una corrección, la versión anterior de esa página. Procesa cada página como solicitud independiente, en secuencia; nunca envíes contenido combinado de páginas distintas.
- No leas, muestres, registres ni solicites la clave API en el chat. El script la obtiene de `OPENAI_API_KEY`.
- No reintentes una solicitud fallida automáticamente; pide nueva autorización antes de volver a llamar.

## Flujo

1. Comprueba el prompt y la coincidencia literal del texto con `--expected-text-file`.
2. Comprueba que la ruta de ilustración indicada por el compiler existe. Envía ese PNG como referencia de composición, sin sustituirlo por `Bo_image.jpg` ni por otro destino.
3. En una corrección, incluye la versión anterior de la página como segunda imagen de referencia y conserva todos los detalles ya aprobados salvo los cambios pedidos.
4. Comprueba que la solicitud individual está confirmada o que pertenece a un lote explícitamente autorizado. Ejecuta `scripts/create_final_page.py` con el prompt, texto, ilustración exacta, continente, número de página y, si corresponde, página anterior.
5. El script utiliza la API oficial de edición de imágenes de OpenAI, guarda el PNG en la siguiente versión libre y adapta cada página al mismo lienzo fijo de **2550 × 3300 px, 300 DPI** (8.5 × 11 pulgadas), conservando la proporción y sin recortar contenido. No altera ni inventa texto a posteriori.
6. En modo individual, presenta la ruta exacta creada y la imagen para revisión; no la marques como aprobada ni continúes hasta que `bo-page-quality-auditor` la audite y el usuario la apruebe.
7. Comprueba que el rectángulo ocupado por el archivo completo de ilustración (incluido su fondo blanco original, pero sin espacio añadido alrededor) representa al menos el 70% del área total de página, con objetivo cercano al 75% cuando lo permitan la proporción aprobada y los márgenes KDP. Comprueba que el panel se ajusta al espacio seguro restante (normalmente hasta unos 645 px de alto), no al marco de 954 px de la referencia de seis líneas, y que el texto conserva el estilo de `pages/africa/page_6.v3.png`: sans serif redondeada de aspecto manuscrito, bloque centrado y “Stamp!” en negrita sin aumentar su tamaño aparente. La letra, su peso y su altura aparente deben ser prácticamente idénticos entre páginas; permite como máximo un ajuste del 5%, aplicado uniformemente a todo el libro, no solo a la página que no quepa. Usa las dimensiones y separaciones de la referencia como guías visuales; no las conviertas a puntos ni las impongas si hacen que la ilustración baje del 70%. Si el texto no cabe legiblemente con esos ajustes tipográficos mínimos, los márgenes de impresión y la ilustración al 70% o más, no lo generes: pide al compiler que revise el diseño o marque el insumo como bloqueado.
8. En modo lote explícitamente solicitado, procesa las páginas elegibles en secuencia y realiza una llamada inicial por página sin pausas para aprobación o confirmación entre ellas. Registra las páginas bloqueadas o fallidas, continúa con las demás y no reintentes ninguna llamada fallida. Una vez acabado el lote, pasa todas las páginas generadas a `bo-page-quality-auditor` y presenta juntas las imágenes y sus resultados; pide una sola aprobación del lote, no aprobaciones página por página. La aprobación del lote no convierte en aptas para impresión las páginas que no hayan obtenido `PASS`.
9. Si una página falla por texto, composición, resolución o cualquier otro defecto, registra el fallo y pide al compiler que revise el prompt si es necesario. Generar su corrección es una nueva solicitud facturable: requiere autorización explícita nueva y crea una versión mayor. Una página fallida no se borra ni se incluye en el PDF.

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
- No enviar páginas a `bo-kdp-formatter` sin resultado `PASS` del auditor para cada versión y aprobación explícita del usuario para esa versión en modo individual, o para todo el lote en modo lote.
- Si la página generada no puede normalizarse sin deformar la relación de aspecto, falla en lugar de recortar contenido importante.
