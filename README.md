# book_creator

Repositorio de skills para crear libros ilustrados de colorear de **Bo, el castor**. Cada skill define instrucciones especializadas para una parte concreta del proceso editorial.

## ¿Qué es una skill?

Una skill es un conjunto reutilizable de instrucciones que ayuda a un asistente de IA a realizar una tarea específica de forma consistente. Aquí, cada skill tiene su propia carpeta y un archivo `SKILL.md`. Las skills no son programas independientes ni agentes autónomos: describen cómo debe ejecutarse una tarea y qué límites respetar.

## Skills disponibles

| Skill | Para qué sirve |
|---|---|
| `continental-explorer` | Sugiere rápidamente monumentos reconocidos en un continente y devuelve solo un JSON sencillo para que el usuario elija cuáles incluir. |
| `bo-adventure-storyteller` | Usa los monumentos elegidos por el usuario para crear el plan de una historia de Bo, manteniendo el espíritu narrativo y el ritmo por páginas del libro europeo original. |
| `bo-page-artist` | Diseña un prompt detallado y preciso para la ilustración, con composición, exactitud del lugar, referencia de Bo y restricciones visuales. Revisa la imagen generada y espera aprobación. |
| `creadora-imagen-ia` | Envía el prompt aprobado y `Bo_image.jpg` a la API de imágenes de OpenAI, descarga el PNG y lo guarda sin sobrescribir en `images/<continente>/<país>/vN/<monumento>.png`. |
| `bo-image-generator` | Entrega el prompt para generación manual en ChatGPT y puede importar el PNG descargado manualmente. No llama a ninguna API. |
| `bo-professional-translator` | Transcrea los textos aprobados a otro idioma y variante regional. Conserva el significado, la voz infantil y el ritmo de lectura; entrega una tabla alineada por página. |
| `bo-page-compiler` | Prepara un prompt completo para maquetar en ChatGPT una ilustración aprobada con el texto exacto, siguiendo la plantilla fija de marcos, márgenes y tipografía. No genera ni redibuja la ilustración. |
| `bo-page-quality-auditor` | Revisa cada página compilada: fidelidad de la ilustración, consistencia de Bo, exactitud de los lugares y textos, marcos, monocromo y dimensiones de impresión. Emite un resultado de aprobado o rechazado y no aprueba si quedan defectos críticos. |
| `bo-kdp-formatter` | Reúne en un PDF interior para KDP las páginas PNG finales, maquetadas con el prompt del compilador y aprobadas por el auditor. No modifica el diseño, el arte ni los textos. |

## Flujo de trabajo sugerido

1. **Elegir monumentos:** `continental-explorer` devuelve una lista breve en JSON; el usuario elige los lugares.
2. **Planear la historia:** `bo-adventure-storyteller` crea el plan de páginas usando solo los monumentos elegidos.
3. **Producir cada página:** `bo-page-artist` diseña el prompt y `creadora-imagen-ia` envía el prompt y `Bo_image.jpg` a la API de OpenAI, descarga el PNG y lo guarda como `images/<continente>/<país>/v1/<monumento>.png`. Las correcciones crean `v2`, `v3`, etc. La API requiere `OPENAI_API_KEY` local y puede facturarse aparte de ChatGPT; confirma cada generación, configura la clave localmente y no la compartas en el chat. El artista revisa la imagen y espera aprobación. Si se necesita otro idioma, `bo-professional-translator` prepara los textos aprobados para la traducción. Para generar manualmente en ChatGPT, usa `bo-image-generator`.
4. **Maquetar y revisar:** `bo-page-compiler` prepara un prompt completo por página. Adjunta en ChatGPT la ilustración aprobada y copia el prompt para obtener el PNG maquetado. `bo-page-quality-auditor` verifica la página; corrige cualquier defecto y vuelve a auditar antes de aprobarla.
5. **Preparar el libro:** cuando todas las páginas PNG hayan pasado la auditoría, `bo-kdp-formatter` las reúne sin rediseñarlas en el PDF interior para KDP.

Respeta los límites de cada skill: por ejemplo, el compilador prepara el prompt pero no afirma haber generado la página; el formateador solo ensambla páginas finales aprobadas y no corrige texto ni altera su diseño.

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
        │       ├── import_image.py
        │       └── test_import_image.py
        ├── creadora-imagen-ia/
        │   ├── SKILL.md
        │   └── scripts/
        │       ├── create_image.py
        │       └── test_create_image.py
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
