# book_creator

Repositorio de skills para crear libros ilustrados de colorear de **Bo, el castor**. Cada skill define instrucciones especializadas para una parte concreta del proceso editorial.

## ¿Qué es una skill?

Una skill es un conjunto reutilizable de instrucciones que ayuda a un asistente de IA a realizar una tarea específica de forma consistente. Aquí, cada skill tiene su propia carpeta y un archivo `SKILL.md`. Las skills no son programas independientes ni agentes autónomos: describen cómo debe ejecutarse una tarea y qué límites respetar.

## Skills disponibles

| Skill | Para qué sirve |
|---|---|
| `continental-explorer` | Investiga lugares icónicos, reconocibles y aptos para colorear de un continente. Prepara una selección con fuentes y un dossier de investigación para planear la aventura. |
| `bo-adventure-storyteller` | Usa el dossier para crear el plan de una historia de Bo ambientada en un continente, manteniendo el espíritu narrativo y el ritmo por páginas del libro europeo original. |
| `bo-page-artist` | Crea la ilustración en blanco y negro para colorear de una página, siguiendo la referencia maestra de Bo. No añade texto, marcos ni diseño de página y espera aprobación antes de pasar a la ilustración siguiente. |
| `bo-professional-translator` | Transcrea los textos aprobados a otro idioma y variante regional. Conserva el significado, la voz infantil y el ritmo de lectura; entrega una tabla alineada por página. |
| `bo-page-compiler` | Compone una ilustración aprobada con el texto narrativo exacto en una página lista para impresión, con marcos, márgenes y tipografía. No crea ni redibuja ilustraciones. |
| `bo-page-quality-auditor` | Revisa cada página compilada: fidelidad de la ilustración, consistencia de Bo, exactitud de los lugares y textos, marcos, monocromo y dimensiones de impresión. Emite un resultado de aprobado o rechazado y no aprueba si quedan defectos críticos. |
| `bo-kdp-formatter` | Convierte páginas aprobadas en un PDF interior listo para KDP. El tamaño predeterminado es 8.5 × 11 pulgadas; puede usar otro tamaño solicitado. No modifica el arte ni los textos. |

## Flujo de trabajo sugerido

1. **Investigar:** `continental-explorer` crea el dossier del continente.
2. **Planear la historia:** `bo-adventure-storyteller` convierte el dossier en un plan de páginas.
3. **Producir cada página:** `bo-page-artist` genera la ilustración y espera su aprobación. Si se necesita otro idioma, `bo-professional-translator` prepara los textos aprobados para la traducción.
4. **Componer y revisar:** `bo-page-compiler` monta cada página y `bo-page-quality-auditor` verifica el resultado. Corrige cualquier defecto y vuelve a auditar antes de darla por aprobada.
5. **Preparar el libro:** una vez aprobadas las páginas, `bo-kdp-formatter` genera el PDF interior para KDP.

Respeta los límites de cada skill: por ejemplo, el formateador no corrige texto y el compilador no redibuja arte.

## Estructura

```text
book_creator/
├── README.md
└── .github/
    └── skills/
        ├── bo-adventure-storyteller/
        │   └── SKILL.md
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
