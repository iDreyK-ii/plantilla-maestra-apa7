# Análisis de la versión adjunta

Se leyeron las 407 líneas del HTML y el archivo de instrucciones antes de modificarlo. Se conserva una copia exacta en `Plantilla_Maestra_APA7_Web_v2_original.html`.

## Base que se conserva y evoluciona
- HTML autónomo en español, CSS APA y editor contenteditable.
- Nombres y acciones de estilos: Párrafo APA, sin sangría, título y tres subtítulos, encabezados 1–5, cita larga y referencia.
- Herramientas de negrita, cursiva, subrayado, alineaciones y listas.
- Inserción de tablas, figuras, citas, referencias y portada; asistente y configuración.
- Panel de estructura, guía y lista de revisión; guardado, duplicado, exportación HTML e impresión.

## Problemas confirmados en el código
1. Se reemplaza solo el bloque del inicio de la selección; el rango queda desconectado al cambiar de estilo.
2. La inserción de bloques puede anidar tablas o encabezados dentro de un párrafo.
3. La figura es solo un marcador sin cargador.
4. Cita fija `(Autor, 2026)`, sin formulario ni relación con fuentes.
5. El formato de referencias no distingue tipos ni escapa todos los campos.
6. Un único registro local: duplicar cambia el nombre pero sobrescribe el original. Los errores de almacenamiento se ocultan.
7. Una sola hoja de altura variable y un número manual: no hay paginación efectiva.
8. El índice copia únicamente niveles 1–3 y no se inserta ni se actualiza.
9. El revisor compara 12 pt contra 12 px (el valor calculado correcto es 16 px); interlineado compara una longitud con un factor.
10. La exportación conserva scripts y contenteditable, aunque elimina controles que esos scripts necesitan.
11. El asistente no usa el tipo seleccionado ni recoge los datos de portada.
12. La revisión solo se muestra en el panel derecho oculto en pantallas pequeñas.
13. No hay seguimiento accesible del estado de guardado ni recuperación multdocumento.

## Decisión arquitectónica
No migrar a un framework. Evolucionar la estructura HTML/CSS original y mantener la API de acciones, reemplazando las implementaciones insuficientes. Código organizado en módulos de fuente y empaquetado sin dependencias en un solo HTML utilizable sin conexión. Contenido, estilos, biblioteca y configuración se almacenan separadamente. Pruebas automatizadas de navegador y exportación PDF. Las limitaciones de revisión heurística y composición de elementos excepcionalmente altos se comunican dentro de la aplicación.
