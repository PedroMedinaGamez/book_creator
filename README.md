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
| `bo-page-compiler` | Prepara el prompt con el texto exacto y registra la ruta exacta, incluida la versión, de la ilustración que debe usar la IA. |
| `final-page-ia` | Verifica el texto del prompt, envía prompt e ilustración identificada a la API de OpenAI y guarda la página en `pages/<continente>/page_<n>.vN.png`. |
| `bo-page-quality-auditor` | Audita cada página final y su versión concreta: arte, Bo, texto, marcos y requisitos de impresión. Emite PASS/FAIL/BLOCKED. |
| `bo-kdp-formatter` | Tras aprobar todas las páginas, usa la versión más alta auditada de cada una y crea el PDF KDP con una página blanca entre cada par de páginas. |

## Flujo de trabajo sugerido

1. **Elegir monumentos:** `continental-explorer` devuelve una lista breve en JSON; el usuario elige los lugares.
2. **Planear la historia:** `bo-adventure-storyteller` crea el plan de páginas usando solo los monumentos elegidos.
3. **Producir cada página:** `bo-page-artist` diseña el prompt y `creadora-imagen-ia` envía el prompt y `Bo_image.jpg` a la API de OpenAI, descarga el PNG y lo guarda como `images/<continente>/<país>/v1/<monumento>.png`. Las correcciones crean `v2`, `v3`, etc. La API requiere `OPENAI_API_KEY` local y puede facturarse aparte de ChatGPT; confirma cada generación, configura la clave localmente y no la compartas en el chat. El artista revisa la imagen y espera aprobación. Si se necesita otro idioma, `bo-professional-translator` prepara los textos aprobados para la traducción. Para generar manualmente en ChatGPT, usa `bo-image-generator`.
4. **Maquetar y revisar:** `bo-page-compiler` entrega el prompt con el texto exacto y la ruta exacta de la ilustración aprobada. `final-page-ia` verifica el texto, envía ambos a la API y guarda `pages/<continente>/page_<n>.v1.png`. Cada corrección crea una versión nueva. El auditor revisa y aprueba la versión correspondiente.
5. **Preparar el libro:** solo después de auditar todas las páginas, `bo-kdp-formatter` usa la versión más alta de cada página, confirma que esa versión pasó QA y crea el PDF con una página blanca entre páginas consecutivas.

Respeta los límites de cada skill: el compiler identifica la ilustración exacta; `final-page-ia` la combina con el texto del prompt; el auditor aprueba la versión concreta; el formateador solo elige versiones auditadas y las ensambla, sin rediseñar su contenido.

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
        │   ├── SKILL.md
        │   ├── requirements.txt
        │   └── scripts/
        │       ├── format_interior.py
        │       └── test_format_interior.py
        ├── bo-page-artist/
        │   └── SKILL.md
        ├── bo-page-compiler/
        │   └── SKILL.md
        ├── bo-page-quality-auditor/
        │   └── SKILL.md
        ├── final-page-ia/
        │   ├── SKILL.md
        │   ├── requirements.txt
        │   └── scripts/
        │       ├── create_final_page.py
        │       └── test_create_final_page.py
        ├── bo-professional-translator/
        │   └── SKILL.md
        └── continental-explorer/
            └── SKILL.md
```

## Skills y la sección «Agents» de GitHub

No son lo mismo. Una **skill** contiene instrucciones especializadas que un asistente puede reutilizar para una tarea, como revisar una página o preparar un PDF. Un **agent** es un asistente configurado para trabajar con cierto rol, instrucciones y herramientas; por ejemplo, un agente de programación puede tomar una tarea del repositorio y proponer o realizar cambios.

En un repositorio, las definiciones de agentes personalizados suelen guardarse aparte, en archivos bajo `.github/agents/`; las skills de este proyecto están en `.github/skills/`. Una sección llamada «Agents» en la interfaz de GitHub puede referirse a las funciones de agentes de Copilot disponibles en esa página o cuenta. No es otra carpeta de skills ni hace que estas skills se ejecuten por sí solas.
