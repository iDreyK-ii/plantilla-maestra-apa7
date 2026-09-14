# Plantilla Maestra APA 7 · Studio

**Entrega única actualizada · 14 de septiembre de 2026 · edición técnica 5.6.0**

Tu espacio para escribir trabajos académicos, aprender APA 7 y descargar documentos Word editables. La evolución conserva el editor y las funciones anteriores; incorpora un dashboard más diseñado, una interfaz kawaii de colores vivos y documentos académicos sobrios.

## Abre el archivo adecuado

| Archivo | Para qué sirve |
|---|---|
| `Plantilla_Maestra_APA7.html` | Aplicación completa y autónoma. Incluye editor, guías y archivos de descarga. |
| `Plantilla_Maestra_APA7_Word.docx` | La plantilla normal APA 7, lista para completar directamente en Word. |
| `plantillas/` | Los 14 modelos por tipo de trabajo, cada uno en su propio DOCX. |
| `Guia_APA7_Estudio.docx` | Guía de estudio: 13 módulos con ejemplos, pasos y respuestas explicadas. |
| `Plantillas_APA7_Word.zip` | **15 plantillas + una guía**: 16 archivos Word. |
| `descargas.html` | Descargas directas, sin editor. También funciona como un único HTML, sin JavaScript ni archivos vecinos. |
| `Word_APA_GitHub_5_6_0.zip` | Único paquete vigente para GitHub: aplicación, Word, documentación, código y pruebas. |
| `FUENTES_Y_MODELOS_APA7.md` | Investigación, procedencia, límites y guías de los modelos. |
| `REVISION_APA7.md` | Pruebas realizadas, resultados y limitaciones verificadas. |

`index.html` es un alias idéntico de la aplicación para el servidor, no otra versión. El original proporcionado se conserva dentro de `proyecto/` como fuente de compilación. Las publicaciones actuales sustituyen las entregas anteriores; no se crean archivos de aplicación con nombres de versiones viejas.

## Descargas en visores y marcos de otro origen

Si apareció `Cross origin sub frames aren't allowed to show a file picker`, el navegador estaba bloqueando **el selector de guardado**, no indicando falta de archivos. La versión anterior comprobaba si existía la API `showSaveFilePicker`, pero eso no acredita permiso para usarla dentro de un marco.

Ahora el selector solo se ofrece en una pestaña de nivel superior y contexto seguro con API disponible. En marcos se usan los enlaces de descarga normales, que no necesitan esa API. Si una llamada residual intenta usar el selector en un marco, se redirige al archivo preparado sin llamarlo. Si el selector falla por seguridad en una pestaña normal, se ofrece/inicia la alternativa directa y se oculta el selector durante esa sesión.

Todas las plantillas están incorporadas: **plantilla normal + 14 modelos**, además de guía y ZIP. No requieren base de datos, cuenta ni documentos guardados. Se comprobó su descarga byte a byte desde un marco real de otro origen con la colección de documentos vacía.

Si el contenedor prohíbe también las descargas normales, la página no puede eludirlo. Cuando hay una URL HTTP(S), el aviso ofrece **Abrir aplicación fuera del visor** en pestaña nueva. Esto requiere que el contenedor permita ventanas nuevas. Si también las bloquea, descarga el HTML desde la entrega y ábrelo directamente en el navegador. La nueva pestaña no traslada automáticamente cambios sin guardar: conserva antes Copia APA de tu trabajo, cuando sea posible.

La entrega vigente sustituye los paquetes anteriores; se conserva el código necesario para reconstruirla.

## La descarga del HTML local se rediseñó

Los enlaces de las plantillas contienen los bytes completos del Word dentro del HTML. **No necesitan que arranque el editor, JavaScript, internet, un servidor ni otros archivos en la misma carpeta.**

1. Descarga la aplicación actual y ábrela en un navegador normal.
2. Pulsa **Plantilla normal** en la bienvenida, o el botón de la tarjeta principal.
3. En **Modelos por tipo de trabajo**, elige uno de los 14 enlaces `.docx`.
4. Para obtener todo a la vez, elige **Todos los Word (.zip)**. El paquete incluye también la guía de estudio.
5. Si no aparece el archivo, revisa el gestor de descargas del navegador. Cuando el editor está activo, el aviso ofrece **Guardar archivo preparado**, **Enlace de archivo directo** y, si estás en una pestaña normal segura y tu navegador lo admite, **Guardar en mi equipo…**.

La aplicación no puede confirmar que un navegador haya terminado una descarga automática. Solo anuncia un guardado confirmado cuando la API de selección de archivos comunica que se escribió y cerró el archivo correctamente.

**Importante:** un visor de archivos, una aplicación de mensajería o un iframe con restricciones pueden bloquear descargas incluso si muestran la página. Abre el HTML con Chrome, Edge, Firefox o Safari fuera de ese visor. Si JavaScript está desactivado, las plantillas directas siguen disponibles, pero el editor y sus botones de herramientas requieren JavaScript.

No uses «Guardar página como MHTML» para obtener Word: MHTML o HTML son páginas web, no documentos `.docx`.

## Tu nuevo escritorio

- Navegación lateral: documentos, plantillas, apertura de Word, aprendizaje y ayuda.
- Bienvenida con creación de documentos, apertura de DOCX y descarga de la plantilla normal.
- Contadores reales: documentos guardados localmente y prácticas completadas, sin estadísticas de usuarios inventadas.
- Búsqueda y filtro de modelos por procedencia.
- Tarjetas con identificación **APA 7 · .docx**, fuentes y precauciones institucionales.
- Ruta de cuatro pasos para principiantes: elegir, escribir, revisar y conservar.
- Trece prácticas cortas con explicación de la respuesta. Su progreso se guarda localmente; no constituye una calificación ni certificación.
- Colores vivos, paneles redondeados e ilustración kawaii; la decoración no se exporta al trabajo académico.

## Escribir aquí

1. Crea un documento con el asistente de cinco pasos: tipo, datos, portada, estructura y confirmación.
2. Escribe en las páginas. Usa los encabezados para organizar el contenido, no espacios para simular sangrías o saltos.
3. La barra organiza herramientas en **Todas, Inicio, Insertar, Referencias, Revisar y Vista**. «Todas» conserva acceso conjunto a las herramientas anteriores.
4. Usa **Guía del apartado** para saber qué desarrollar. La ayuda permanece fuera de la hoja por defecto.
5. Abre **Buscar / reemplazar** o pulsa Ctrl/Cmd + F mientras estás en el editor. La búsqueda es literal y admite mayúsculas opcionales. Los reemplazos conservan los estilos y se pueden deshacer.
6. **Concentración** oculta los paneles laterales sin alterar el documento. **Meta de escritura** guarda una meta personal, no un requisito APA.
7. Revisa contenido, citas y formato. Descarga **Mi trabajo Word** para obtener tu texto actual, y una **Copia APA** para respaldar los datos de la aplicación.

La búsqueda trabaja dentro de cada fragmento de formato. Una palabra partida entre negritas, cursivas u otros nodos puede necesitar revisión manual. No reemplaza automáticamente portada, índice, citas vinculadas ni referencias gestionadas; estas últimas se modifican desde la biblioteca.

## Planificar, proteger y entregar

### 1. Planifica tu trabajo

Abre un documento y pulsa **Planifica tu trabajo** o **Ficha de planificación**. Anota tema, pregunta, objetivo o postura, procedimiento, fuentes, ética, guía institucional y próxima acción. Agrega conexiones entre objetivos/argumentos, procedimientos y evidencia.

- **Guardar ficha** conserva estas anotaciones dentro de ese documento, pero fuera del texto académico.
- **Guardar y revisar campos** comprueba qué campos tienen anotaciones; no juzga si la metodología es correcta.
- **Guardar y descargar ficha Word** produce un documento de apoyo separado.
- Cerrar o cancelar sin guardar descarta los cambios de la ficha.
- El Word académico, el HTML de entrega y la impresión no incluyen estas notas. **Copia APA y el respaldo completo sí las conservan.**

### 2. Protección y respaldo

Acceso desde la bienvenida, el menú lateral, las herramientas del editor o Mis documentos.

- **Guardado local:** conserva el trabajo en el navegador. Si falla, el estado lo advierte; no confundas escribir en pantalla con haber guardado.
- **Historial:** primer guardado y cambios separados por al menos dos minutos; puedes crear un punto manual. Hasta ocho puntos por documento, cuarenta en total y doce MiB. Los más antiguos se descartan al alcanzar los límites.
- **Recuperar:** revisa una vista previa y recupera como copia, sin sobrescribir el documento original.
- **Eliminar:** se intenta archivar un punto antes del borrado; si falla, se pide una segunda confirmación. El historial puede conservar trabajos eliminados. **Borrar historial** elimina los puntos existentes sin borrar los documentos actuales; los guardados futuros pueden generar puntos nuevos.
- **Respaldo completo:** descarga documentos, borrador abierto diferente de la versión guardada, historial disponible, ficha, confirmaciones y preferencias. Si solo quedan puntos de trabajos eliminados, también se pueden respaldar.
- **Abrir respaldo completo:** muestra una confirmación y agrega copias nuevas. No reemplaza documentos. Puedes restaurar prácticas y meta de escritura. Los puntos conservados se informan al terminar y siguen sujetos a los límites de historial.

El formato completo es `Respaldo_completo_APA7.apa.json`, distinto de la Copia APA individual. Admite hasta cien documentos, cuarenta MiB de archivo y ocho millones de caracteres aproximadamente por HTML individual (8 × 1024²). Si no cabe, conserva copias APA individuales. La cuota de almacenamiento del navegador puede ser menor: una importación puede rechazarse por falta de espacio.

**Importante:** ni el historial ni el guardado local son copias externas. El archivo de respaldo no está cifrado y puede incluir notas privadas y trabajos eliminados; no lo uses como entrega académica. Guárdalo en un lugar de confianza y comprueba que puedas restaurarlo antes de borrar originales.

### 3. Cambios desde otra pestaña

La aplicación compara la versión cargada con la guardada y evita sobrescribir cambios conocidos. En **Protección**, elige **Conservar borrador como copia** o **Abrir versión guardada**. El segundo camino requiere confirmación y descarta los cambios abiertos no conservados.

Es una defensa ante conflictos detectables, no edición colaborativa ni un bloqueo atómico entre pestañas. Evita editar el mismo trabajo simultáneamente en dos ventanas.

### 4. Antes de entregar

Este centro diferencia:

1. **Señales automáticas limitadas:** guardado local, algunos marcadores de plantilla, saltos de encabezado, imágenes sin descripción y avisos de citas disponibles.
2. **Confirmaciones personales:** revisión de contenido, fuentes, ética, identidad, Word final y copia externa. Las marcas son declaraciones del estudiante, no comprobaciones de la web. Un cambio de contenido, requisitos, modelo o ficha solicita revisarlas de nuevo.
3. **Revisión institucional:** confirmar consigna, guía vigente, asesor y requisitos de publicación.

Descarga una **Hoja de revisión Word** por separado o tu **trabajo Word**. No hay porcentaje de aprobación APA, informe de similitud, verificación de fuentes en internet ni aceptación institucional automática.

## Abrir un documento de Word

Pulsa **Abrir mi Word**, **Abrir Word** o utiliza **Mis documentos → Abrir Word (.docx)**.

- Conversión local de DOCX de hasta 20 MB. No se sube el documento a un servicio externo.
- Se abre como **copia nueva**, sin sobrescribir el trabajo actual.
- Se recuperan texto, estilos reconocidos, encabezados, listas, tablas e imágenes compatibles.
- Se reaplica la base APA 7 y se calcula la paginación del editor.
- Los archivos cifrados, macros, formatos DOC/DOCM y archivos con estructuras o tamaños descomprimidos fuera de los límites de seguridad se rechazan.

**No es una reproducción exacta de Microsoft Word.** Revisa ecuaciones, formas, comentarios, cambios controlados, pies de página, índices y campos complejos. Algunos pueden omitirse, convertirse a contenido estático o requerir reconstrucción. Las referencias importadas no se convierten automáticamente en la biblioteca gestionada.

Para recuperar fielmente los datos que maneja esta web —biblioteca, vínculos, estructura y configuración— utiliza **Copia APA**, no el DOCX como único respaldo de ida y vuelta.

## Plantillas y formato APA 7

Todas las plantillas descargables utilizan la base: **Carta 8,5 × 11 pulgadas, márgenes de 2,54 cm, Times New Roman 12, doble espacio, sangría de primera línea de 1,27 cm, sangría francesa en referencias y numeración automática PAGE**. Incluyen estilos reutilizables de encabezados 1–5.

La plantilla normal se ofrece aparte de estos 14 modelos:

1. Trabajo académico.
2. Ensayo.
3. Informe.
4. Monografía.
5. Proyecto — perfil UPeU.
6. Tesis en formato artículo — UPeU FE-03.
7. Artículo de investigación — adaptación basada en FE-03.
8. Revisión bibliográfica básica — UPeU FE-01.
9. Artículo de revisión — UPeU FE-03.
10. Proyecto de tesis doctoral — UPeU FE-04.
11. Tesis tradicional — Anexo 03 de catálogo anterior, uso condicionado.
12. Trabajo de Enfermería — modelo didáctico propio, no guía clínica.
13. Ensayo para revista Educación — adaptación estructural de normas PUCP.
14. Otro / documento libre.

### Antes de entregar

- Sustituye las indicaciones entre corchetes por tu contenido.
- Retira la ficha de uso y fuentes de la plantilla. No son referencias de tu investigación.
- Decide con tu asesor si corresponden los apartados opcionales.
- Actualiza el índice en Word con **Actualizar campo → toda la tabla**.
- Revisa el Word abierto, no solo la apariencia del editor.
- Comprueba la guía del programa o revista: la estructura institucional no es una regla universal APA.

### Diferencias institucionales explícitas

El perfil UPeU consultado muestra 2020 en su portada y pide Arial 14 en algunas partes. El Anexo 03 tradicional indica A4 y preliminares específicos. La revista Educación pide A4, Arial 11, interlineado 1,5 y otras condiciones. **Las descargas de esta aplicación conservan la base APA 7 solicitada y no se presentan como formularios oficiales listos para trámite o envío editorial.**

No se fabrican firmas, actas, aprobaciones éticas, referencias, resultados ni informes de similitud. La consulta de un enlace oficial no confirma vigencia para todas las facultades. Consulta las fichas y `FUENTES_Y_MODELOS_APA7.md`.

## Funciones conservadas

Editor, portada, párrafos y estilos, subtítulos auxiliares, encabezados 1–5, citas largas, selección, deshacer/rehacer, pegado limpio, tablas editables, operaciones de filas/columnas, figuras locales con texto alternativo, biblioteca de seis tipos de referencias, citas narrativas y parentéticas, comprobación de correspondencia, esquema, navegación y reorganización, índice, saltos y paginación, documentos independientes, autosave, duplicación, eliminación, importación HTML/JSON, revisor básico, tutor, progreso, trece módulos y ocho pasos para configurar Word.

La exportación DOCX es OOXML editable real, no HTML renombrado. HTML limpio, Copia APA e impresión/PDF siguen disponibles como acciones separadas.

## Privacidad y respaldo

Los documentos y preferencias permanecen en el navegador. No hay cuentas, anuncios de terceros ni carga del trabajo a universidades o servicios de IA. Los enlaces de fuentes se abren solo por elección del usuario.

El almacenamiento depende del navegador, perfil y origen. Cambiar de dispositivo, borrar datos, usar navegación privada o cambiar la ruta de un HTML local puede afectar el acceso a los guardados. Conserva copias APA y Word. La actualización no borra las claves de documentos existentes.

Los archivos que ya descargaste en tu computadora están fuera del alcance de la limpieza del espacio de trabajo.

## Límites honestos

La revisión automática no certifica el cumplimiento completo de APA, la metodología, las fuentes, la originalidad, la calidad clínica ni la aceptación institucional. La disponibilidad de Times New Roman y la distribución de páginas varían por dispositivo.

Se probaron los flujos en Chromium y muestras en Firefox y WebKit. WebKit de Playwright no equivale a haber probado Safari o iOS en un dispositivo real. Microsoft Word de escritorio no está disponible en este entorno. Consulta el informe de revisión para conocer exactamente qué se comprobó.

## Reconstruir y probar

```bash
pip install -r requirements.txt
npm ci
npx playwright install chromium
npm run build
npm start
```

Con el servidor en el puerto 3000, desde otra terminal:

```bash
npm test
npm run test:word
npm run test:release
npm run test:modelos
npm run test:descargas
npm run test:studio
```

Pruebas adicionales de motores de navegador:

```bash
npx playwright install firefox webkit
npx playwright install-deps firefox webkit
npm run test:cross-browser
npm run test:confianza
npm run test:marcos
npm run test:github
```

Finalmente:

```bash
npm run package
```

LibreOffice es opcional para las comprobaciones adicionales de apertura y renderizado. Los PDF, capturas y descargas temporales de las pruebas se retiraron en la limpieza. Se conservan los scripts, el fixture `figura.png` y los resultados JSON vigentes; las pruebas generan de nuevo los archivos que necesitan.

## Dos maneras de empezar

- **Escribe aquí:** ejemplos explicados de APA general o una hoja en blanco. Crear otra hoja conserva el documento anterior.
- **Continúa en Word:** descarga directa de APA general o uno de los modelos por categoría: trabajos de clase, tesis/proyectos, artículos/revisiones y áreas específicas.

La base general muestra portada, párrafos, encabezados, citas, tabla, figura y referencias. Sustituye los ejemplos y sus marcadores antes de entregar. Las estructuras especializadas conservan sus fuentes y advertencias.

## Apariencia y movimiento

Rosado bebé, turquesa, lila y amarillo suave en la interfaz; papel académico blanco. La enfermera es un SVG kawaii 2D con pestañeo, saludo del brazo e inclinación suave de cabeza, y tiene un botón de pausa, sin afectar tus documentos. Se respeta el movimiento reducido del dispositivo. Sin JavaScript, la ilustración es estática y el control de pausa se oculta.

## Compatibilidad de los Word

Además de revisar OOXML y descargas, se abrieron y renderizaron los 16 Word descargables y una exportación de los ejemplos con LibreOffice Writer. Se corrigió la división de la tabla breve entre páginas y se retiró una imagen huérfana de la guía. Consulta el informe para conocer motor, tipografía y alcance exactos. No equivale a una certificación de todos los programas o requisitos institucionales.

## Inicio en cajones

1. **Plantilla normal APA 7:** descarga el Word o consulta los ejemplos en el editor.
2. **Escribir o editar:** crea un documento en blanco, abre un Word como copia o retoma uno guardado.
3. **Plantillas específicas:** los 14 modelos permanecen separados de la plantilla principal y organizados por categorías.
4. **Ayuda y herramientas:** aprendizaje y respaldo tienen sus bloques; los accesos adicionales están en «Más herramientas».

La animación cambia partes del dibujo, no desplaza una fotografía. Respeta el movimiento reducido y la pausa; sin JavaScript queda estática.
