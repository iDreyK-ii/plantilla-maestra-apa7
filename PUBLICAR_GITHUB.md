# Desarrollo y publicación

Edición vigente: **5.6.0** · [Repositorio](https://github.com/iDreyK-ii/plantilla-maestra-apa7) · [Aplicación](https://idreyk-ii.github.io/plantilla-maestra-apa7/)

## Reconstruir y verificar

```bash
python -m pip install -r requirements-build.txt
npm ci
npx playwright install --with-deps chromium firefox webkit
npm run build
npm start
```

En otra terminal:

```bash
npm run test:all
npm run build:pages
npm run package
```

La comprobación opcional `npm run test:office` requiere LibreOffice Writer y una ejecución previa de `test:general`. Renderiza los Word en una carpeta temporal, sin subirlos a ningún servicio. Su informe declara el motor y la sustitución tipográfica utilizada; no acredita pruebas en Microsoft Word.

## Sincronización asistida habitual

```bash
npm run package
npm run sync:github
npm run sync:github -- --publicar --mensaje "Describir los cambios verificados"
```

El primer comando prepara `Word_APA_GitHub_5_6_0.zip`. El segundo solo compara. El tercero verifica el paquete, crea un commit y publica sin force-push. Se detiene si main cambió desde la última confirmación. El registro local está en `.git/apa7-sincronizacion.json`; nunca contiene credenciales.

Se necesita GitHub CLI autenticado con permiso sobre el repositorio. Las credenciales se gestionan fuera del proyecto y pueden desaparecer al reiniciar el entorno. Para cambios de workflows se requiere también el alcance `workflow`. Utiliza `gh auth login --web --git-protocol https --scopes workflow`; no envíes contraseñas ni tokens por chat.

La sincronización no es un servicio permanente y no transmite documentos del navegador. En una conexión nueva, revisa primero el SHA remoto y utiliza `--base-remota SHA`; nunca para ignorar cambios ajenos.

## Limpieza excepcional del historial

El titular autorizó expresamente, el 14 de septiembre de 2026, sustituir el historial anterior de main por un único commit con la versión vigente. Es una operación puntual, con comprobación del SHA remoto y `--force-with-lease` limitado a ese SHA, no una nueva política de subidas forzadas.

Tras la sustitución se verifica el árbol completo, la ausencia de padres del commit, el despliegue y las descargas. Los clones anteriores deben descargarse de nuevo; no deben fusionar el historial antiguo de vuelta. Las actualizaciones futuras conservan normalmente el historial desde esta nueva base. GitHub puede retener objetos antiguos temporalmente, de modo que no se promete liberación inmediata de todo su almacenamiento.

## GitHub Pages

Settings → Pages → Source: **GitHub Actions**. Cada push a main construye y ejecuta `test:all`; solo después publica `dist/`. El éxito de un push no demuestra el éxito de Pages: comprueba ambos jobs y la URL pública.

El sitio contiene 27 archivos: dos HTML de la aplicación, descargas, 16 DOCX, ZIP de Word, seis recursos visuales y `.nojekyll`. No entrega las pruebas, perfiles ni credenciales.

## Qué conservar

Fuentes modulares, HTML autónomo, index idéntico, Word, guía, investigación, dependencias fijadas, licencias de bibliotecas, pruebas y documentación vigente. El original de compilación se conserva como fuente necesaria; no es un respaldo de publicación.

El paquete completo no se sube además como copia redundante a Git: se publican sus archivos. El ZIP de plantillas es distinto y necesario para descargar los 16 Word juntos. No publiques JSON académicos, perfiles, capturas de pruebas, cachés, secretos ni paquetes de entregas anteriores.

El titular no ha definido una licencia propia. Los avisos de dependencias están en `proyecto/LICENCIAS_WORD.txt`, `proyecto/LICENCIA_MAMMOTH.txt` y los archivos LEGAL asociados.
