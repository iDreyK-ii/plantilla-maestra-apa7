# Revisión de la entrega vigente

**Edición 5.6.0 · 14 de septiembre de 2026**

## Cambios y correcciones

- Inicio reordenado: cajón principal de plantilla normal, cajón del editor (nuevo, abrir Word y documentos guardados), catálogo específico, ayuda/respaldo y herramientas adicionales desplegables. Sin duplicar la plantilla general dentro del catálogo.
- Se reemplaza el render 3D anterior por un SVG 2D propio, incorporado en ambos HTML. Ojos, brazo, cabeza y detalles se animan por separado; la pausa y el movimiento reducido detienen todas las partes.
- Cinco casos adicionales verifican jerarquía, crear/retomar, importación desde el nuevo botón, cambios reales en la línea de tiempo de la animación y herramientas desplegables. Las comprobaciones de imagen se adaptan a la representación SVG, conservando la verificación autónoma y sin recursos externos.

- Paleta más viva: rosado bebé y turquesa, con lila, amarillo y durazno. Se mantienen contraste legible, adaptación móvil y papel académico blanco.
- Una sola enfermera kawaii 2D de piel clara, uniforme blanco, pestañeo y saludo con pausa. La marca continúa siendo APA para cualquier persona.
- Se corrigió el contraste de etiquetas y una pestaña del editor tras cambiar los fondos, sin excluir reglas de accesibilidad.
- La apertura real en LibreOffice mostró una tabla breve partida entre dos páginas. Se mantienen juntos su número, título y filas en la plantilla general y las tablas breves exportadas. Las tablas largas pueden continuar en otras páginas.
- Se retiró una imagen huérfana de la guía Word sin figuras. Se conservan la figura académica de ejemplo y las fuentes investigadas.
- README breve, capturas actuales y un único paquete de entrega. El usuario autorizó expresamente reiniciar el historial de main con una sola versión; las actualizaciones posteriores usan la sincronización normal, no subidas forzadas automáticas.

## Verificación de esta edición

Se actualizaron los localizadores de pruebas afectados por las etiquetas nuevas y por el cajón desplegable de herramientas; no se retiraron comprobaciones. La animación de brazo, ojos y cabeza y su pausa se verificaron también en Chromium, Firefox y WebKit.

**Resultado local: 353/353 aprobados**, con salida 0. La batería principal comprende **353 casos**: 345 en 18 archivos JSON y 8 pruebas unitarias de sincronización. Incluye 19 de diseño y 8 de estructura Word general. Las repeticiones no se suman como pruebas nuevas.

La comprobación adicional `npm run test:office` abre y renderiza **17 DOCX** (15 plantillas, guía y una exportación real), mediante LibreOffice Writer 25.2.3.2. Comprueba papel Carta, texto dentro de la página, ausencia de páginas vacías, contenido final y, en APA general, figura visible y tabla breve en una sola página. El informe `pruebas/office-resultados.json` corresponde a esta ejecución local opcional; **no forma parte de test:all ni demuestra una ejecución de LibreOffice en GitHub Actions**.

Times New Roman está declarada en los DOCX, pero no instalada en este entorno: el renderizador utiliza Liberation Serif. Se inspeccionó visualmente la página de tabla y figura antes y después de corregirla. Esto es apertura y renderizado real con LibreOffice, no una prueba manual en Microsoft Word, que no está disponible aquí.

Los PDF, perfiles y documentos sintéticos de las pruebas no se publican. El despliegue remoto y las descargas HTTPS se confirman por separado en Actions y en los registros locales sin secretos de `.git/`.

## Alcance y límites

- Base APA: Carta, márgenes de 2,54 cm, TNR12, doble espacio, sangrías reales de 1,27 cm, encabezados 1–5 y número de página. APA admite otras fuentes; la estructura depende del género y del encargo.
- Los requisitos UPeU históricos y de revistas no se presentan como normas universales vigentes. Se conservan las diferencias con A4, formatos institucionales y rúbricas en `FUENTES_Y_MODELOS_APA7.md`.
- El revisor no certifica originalidad, metodología, fuentes verdaderas, ética o aceptación institucional. Los ejemplos con marcadores no son investigaciones ni bibliografía reales.
- Chromium, Firefox y WebKit de Playwright no cubren todos los equipos; WebKit no equivale a Safari/iOS real. Las auditorías axe-core no sustituyen una evaluación manual integral de accesibilidad.
- Los 17 recursos se descargan con enlaces nativos y se contrastan sus bytes. El navegador o visor conserva autoridad sobre descargas, ventanas nuevas y selectores. Detectar la API no demuestra permiso; cancelaciones y errores no se anuncian como éxito.
- El selector solo se ofrece en contexto superior seguro. Se conserva recuperación para SecurityError/NotAllowedError y enlaces alternativos, sin intentar eludir restricciones.

## Importación de DOCX

Se integró conversión local con Mammoth, empaquetado dentro del HTML. No se utiliza un servicio externo.

- Abre DOCX como copia nueva, previa confirmación.
- Recupera texto, estilos reconocidos, encabezados 1–5, listas, tablas e imágenes compatibles.
- Reconstruye la portada de las plantillas reconocidas y mantiene sus campos editables.
- Reaplica la base APA 7 y recalcula páginas.
- Conserva el trabajo previo, con guardado independiente.
- Rechaza archivos falsos, cifrados, con macros o tamaños declarados fuera de los límites.
- Sanitiza el HTML convertido; no carga imágenes remotas del contenido importado.

Durante las pruebas se detectó que el mapeo de párrafo APA anulaba las listas. Se corrigió dando prioridad a los mapeos de listas ordenadas y no ordenadas, incluidos niveles anidados. También se corrigió la reconstrucción de la portada para que el título no desplazara los campos de autor e institución.

**Límites de la conversión:** no es una representación exacta de Office. Ecuaciones, formas, comentarios, cambios controlados, pies, índices y campos complejos necesitan revisión y algunos pueden omitirse o volverse estáticos. La biblioteca de referencias no se recupera automáticamente a partir de texto bibliográfico; para los datos gestionados por la web se mantiene Copia APA.

## Aprendizaje

- Trece módulos conservados y revisados con instrucciones más concretas.
- Corrección del módulo de exportación, que había quedado centrado en HTML/PDF: ahora distingue plantilla, trabajo Word, importación DOCX y Copia APA.
- Ejemplos con marcadores identificados como orientativos, no referencias reales para copiar.
- Trece prácticas con respuesta explicada y progreso local.
- Ruta de cuatro pasos para principiantes.
- Guía completa descargable en Word: `Guia_APA7_Estudio.docx`.
- Guías por apartado y procedencia institucional conservadas.

Las prácticas son ejercicios de aprendizaje, no calificaciones ni certificaciones.

## Protección, planificación y entrega

### Protección implementada

- Persistencia que lee la colección actual antes de guardar: conserva los otros documentos y detecta cambios conocidos del documento abierto.
- Resolución de conflicto como nueva copia o apertura explícita de la versión guardada. No se presenta como colaboración simultánea ni transacción atómica entre pestañas.
- Historial local IndexedDB con primer guardado, intervalo automático de dos minutos y puntos manuales. Recuperación siempre como documento independiente.
- Retención: ocho puntos por documento, cuarenta globales y doce MiB; se descartan los más antiguos. Un documento que supera el límite no recibe un falso éxito.
- Punto antes de eliminar, segunda confirmación si la protección falla y acceso al historial de documentos eliminados. Borrado explícito del historial por privacidad.
- Respaldo completo con borrador no guardado como copia, historial disponible y preferencias. Se conservan fechas y etiquetas de los puntos importados que caben en los límites.
- Importación confirmada, identificadores nuevos y sin reemplazo. Validación de formato, tamaño, identificadores, historial y referencias; sanitización HTML y eliminación de claves de contaminación de prototipo.
- El guardado de documentos precede a la importación del historial. Si IndexedDB falla o la retención descarta puntos, la importación puede conservar documentos y solo parte del historial; se informa cuántos puntos permanecen y se pide conservar el respaldo.
- Errores de cuota o de acceso no se anuncian como guardado exitoso. No se promete que un cierre abrupto permita terminar un punto asíncrono.

### Planificación y entrega

Ficha privada por documento con ocho campos y hasta veinte conexiones objetivo/argumento → procedimiento → evidencia. Guardado explícito, revisión de presencia de campos y Word de apoyo separado. No propone resultados, fuentes, aprobaciones éticas ni hipótesis ficticias.

El centro de entrega separa cinco señales automáticas limitadas, siete confirmaciones del estudiante y la revisión institucional. Los cambios relevantes invalidan las confirmaciones anteriores mediante una huella local de cambios, no una firma de autenticidad. El centro no emite una nota de calidad, porcentaje APA ni informe antiplagio.

**Separación comprobada:** el Word académico y el HTML de entrega excluyen la ficha y las confirmaciones. Las copias APA y el respaldo completo sí las conservan. La ficha y la hoja de revisión se descargan como DOCX distintos del trabajo. El historial y el respaldo no están cifrados y pueden incluir documentos eliminados.

### Cobertura de protección

Primer punto, deduplicación, intervalo, recuperación independiente, recuperación de borrado, límites de ocho/cuarenta puntos/doce MiB, rechazo de punto excesivo, persistencia y cancelación de ficha, conexiones, Word de apoyo, exclusión de notas privadas, invalidación de checklist, señales de marcadores/encabezados/imágenes, backup con borrador, restauración y preferencias, entradas inválidas y hostiles, rechazo previo a lectura por tamaño, cuota agotada, dos pestañas con conflicto, preservación de documentos ajenos, no resurrección silenciosa de borrado, borrado del historial, fallo de IndexedDB/localStorage, accesibilidad y anchos 360/768/1440.

Chromium, Firefox y WebKit también abrieron el HTML mediante `file://`, con solicitudes HTTP/HTTPS bloqueadas, guardaron la ficha, crearon historial, recuperaron una copia y descargaron un respaldo completo válido. No se afirma haber probado todos los navegadores de todos los equipos.

Se corrigió además una transición de opacidad del aviso de estado que podía reducir temporalmente su contraste. Las auditorías se repitieron con el texto completamente contrastado, sin desactivar la regla de accesibilidad.


## Reproducir

```bash
python -m pip install -r requirements-build.txt
npm ci
npx playwright install --with-deps chromium firefox webkit
npm run build
npm start
```

En otra terminal: `npm run test:all`. Opcionalmente, con LibreOffice Writer instalado, `npm run test:office`. Después: `npm run build:pages` y `npm run package`.

Las credenciales, documentos personales y cachés no pertenecen al repositorio. El HTML original de compilación y el alias index tienen propósitos necesarios y se conservan.
