# book_creator

Repositorio de skills para crear libros ilustrados de colorear de **Bo, el castor**. Cada skill define instrucciones especializadas para una parte concreta del proceso editorial.

## ¿Qué es una skill?

Una skill es un conjunto reutilizable de instrucciones que ayuda a un asistente de IA a realizar una tarea específica de forma consistente. Aquí, cada skill tiene su propia carpeta y un archivo `SKILL.md`. Las skills no son programas independientes ni agentes autónomos: describen cómo debe ejecutarse una tarea y qué límites respetar.

## Skills disponibles

| Skill | Para qué sirve |
|---|---|
| `continental-explorer` | Sugiere rápidamente monumentos reconocidos en un continente y devuelve solo un JSON sencillo para que el usuario elija cuáles incluir. |
| `bo-adventure-storyteller` | Usa los monumentos elegidos por el usuario para crear el plan de una historia de Bo, manteniendo el espíritu narrativo y el ritmo por páginas del libro europeo original. |
| `bo-page-artist` | Crea la ilustración en blanco y negro para colorear de una página, siguiendo la referencia maestra de Bo. No añade texto, marcos ni diseño de página y espera aprobación antes de pasar a la ilustración siguiente. |
| `bo-image-generator` | Envía el prompt final del artista a la API de imágenes de OpenAI, descarga el PNG y lo guarda con versiones en `images/<continente>/<país>/<monumento>_vN.png`. |
| `bo-professional-translator` | Transcrea los textos aprobados a otro idioma y variante regional. Conserva el significado, la voz infantil y el ritmo de lectura; entrega una tabla alineada por página. |
| `bo-page-compiler` | Compone una ilustración aprobada con el texto narrativo exacto en una página lista para impresión, con marcos, márgenes y tipografía. No crea ni redibuja ilustraciones. |
| `bo-page-quality-auditor` | Revisa cada página compilada: fidelidad de la ilustración, consistencia de Bo, exactitud de los lugares y textos, marcos, monocromo y dimensiones de impresión. Emite un resultado de aprobado o rechazado y no aprueba si quedan defectos críticos. |
| `bo-kdp-formatter` | Convierte páginas aprobadas en un PDF interior listo para KDP. El tamaño predeterminado es 8.5 × 11 pulgadas; puede usar otro tamaño solicitado. No modifica el arte ni los textos. |

## Flujo de trabajo sugerido

1. **Elegir monumentos:** `continental-explorer` devuelve una lista breve en JSON; el usuario elige los lugares.
2. **Planear la historia:** `bo-adventure-storyteller` crea el plan de páginas usando solo los monumentos elegidos.
3. **Producir cada página:** `bo-page-artist` prepara el prompt y `bo-image-generator` solicita la ilustración, guardándola en `images/` con un número de versión. El artista revisa la imagen y espera su aprobación. La API requiere `OPENAI_API_KEY` y puede facturarse aparte de ChatGPT; configura la clave localmente y no la compartas en el chat. Si se necesita otro idioma, `bo-professional-translator` prepara los textos aprobados para la traducción.
4. **Componer y revisar:** `bo-page-compiler` monta cada página y `bo-page-quality-auditor` verifica el resultado. Corrige cualquier defecto y vuelve a auditar antes de darla por aprobada.
5. **Preparar el libro:** una vez aprobadas las páginas, `bo-kdp-formatter` genera el PDF interior para KDP.

Respeta los límites de cada skill: por ejemplo, el formateador no corrige texto y el compilador no redibuja arte.

## Agente de aventura por continente

El agente personalizado **Bo Continent Adventure** está en `.github/agents/bo-continent-adventure.agent.md`. Úsalo desde el selector de agentes de Copilot para coordinar las dos primeras skills:

1. Ejecuta `continental-explorer` y presenta las sugerencias como JSON breve.
2. Se detiene y espera a que elijas los monumentos.
3. Usa únicamente los lugares elegidos con `bo-adventure-storyteller` para crear el plan completo página por página.

Si pides más opciones o cambias las restricciones, actualiza la lista y vuelve a esperar tu elección. El agente no debe comenzar la historia antes de que elijas.

## Estructura

```text
book_creator/
├── README.md
└── .github/
    ├── agents/
    │   └── bo-continent-adventure.agent.md
    └── skills/
        ├── bo-adventure-storyteller/
        │   └── SKILL.md
        ├── bo-image-generator/
        │   ├── SKILL.md
        │   └── scripts/
        │       ├── generate_image.py
        │       └── test_generate_image.py
        ├── bo-kdp-formatter/
        │   └── SKILL.md
        ├── bo-page-artist/
        │   └── SKILL.md
        ├── bo-page-compiler/
        │   └── SKILL.md
        ├── bo-page-quality-auditor/
        │   └── SKILL.md
        ├── bo-professional-translator/
        │   └── SKILL.md
        └── continental-explorer/
            └── SKILL.md
```

## Skills y la sección «Agents» de GitHub

No son lo mismo. Una **skill** contiene instrucciones especializadas que un asistente puede reutilizar para una tarea, como revisar una página o preparar un PDF. Un **agent** es un asistente configurado para trabajar con cierto rol, instrucciones y herramientas; por ejemplo, un agente de programación puede tomar una tarea del repositorio y proponer o realizar cambios.

En un repositorio, las definiciones de agentes personalizados suelen guardarse aparte, en archivos bajo `.github/agents/`; las skills de este proyecto están en `.github/skills/`. Una sección llamada «Agents» en la interfaz de GitHub puede referirse a las funciones de agentes de Copilot disponibles en esa página o cuenta. No es otra carpeta de skills ni hace que estas skills se ejecuten por sí solas.
