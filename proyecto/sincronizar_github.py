"""Sincronización explícita y verificable; sin tokens, force-push ni servicio permanente.

Requiere Git, GitHub CLI autenticado y un ZIP vigente generado por npm run package.
Por defecto solo compara. --publicar crea un commit y hace push si hay cambios.
El primer uso requiere --base-remota SHA revisado; usos posteriores consultan
.git/apa7-sincronizacion.json, estado local sin credenciales y no publicable.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent.parent
REPO = 'iDreyK-ii/plantilla-maestra-apa7'
BRANCH = 'main'
MANIFEST = 'pruebas/entrega-manifiesto.json'
STATE = ROOT / '.git/apa7-sincronizacion.json'
SECRET = re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----)')


def safe_path(name):
    p = PurePosixPath(name)
    forbidden = {'.git', '.env', '.netrc', '.git-credentials', 'node_modules', '.cache', '.local', 'uploads', 'hosts.yml'}
    if p.is_absolute() or '..' in p.parts or '\\' in name or str(p) != name or any(x in forbidden or x.startswith('.env.') for x in p.parts) or name.endswith(('.apa.json', '.pem', '.key')):
        raise ValueError('Ruta no publicable: ' + name)
    return name


def read_package(root=ROOT):
    version = json.loads((root / 'package.json').read_text())['version']
    archive = root / ('Word_APA_GitHub_' + version.replace('.', '_') + '.zip')
    with ZipFile(archive) as z:
        if z.testzip() is not None:
            raise ValueError('ZIP dañado')
        names = z.namelist()
        manifest = json.loads(z.read(MANIFEST))
        if manifest['edition'] != version or len(names) != len(set(names)) or set(names) != set(manifest['files']) | {MANIFEST}:
            raise ValueError('Manifiesto o versión inconsistente')
        payload = {}
        for name in names:
            safe_path(name)
            data = z.read(name)
            local = root / name
            if local.is_symlink() or root.resolve() not in local.resolve().parents:
                raise ValueError('Enlace o ruta fuera del proyecto: ' + name)
            if data != local.read_bytes():
                raise ValueError('ZIP desactualizado: ' + name + '; ejecuta npm run package')
            if name != MANIFEST and hashlib.sha256(data).hexdigest() != manifest['files'][name]:
                raise ValueError('Hash incorrecto: ' + name)
            if name.endswith(('.py', '.js', '.json', '.txt', '.md', '.yml', '.html', '.css')) and SECRET.search(data):
                raise ValueError('Posible secreto: ' + name + '; no se publicará')
            payload[name] = data
        if payload['index.html'] != payload['Plantilla_Maestra_APA7.html']:
            raise ValueError('HTML de entrada diferente del HTML vigente')
        if len([n for n in names if n.startswith('plantillas/') and n.endswith('.docx')]) != 14:
            raise ValueError('Catálogo incompleto')
    return archive, payload


def run(args, cwd=None):
    env = os.environ.copy()
    for key in ['GH_DEBUG', 'GIT_TRACE', 'GIT_TRACE_CURL', 'GIT_CURL_VERBOSE']:
        env.pop(key, None)
    env['GIT_TERMINAL_PROMPT'] = '0'
    env['GH_PROMPT_DISABLED'] = '1'
    result = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError('Falló ' + args[0] + ': ' + result.stderr.strip())
    return result.stdout.strip()


def git(*args, cwd=None):
    return run(['git', '-c', 'credential.helper=', '-c', 'credential.helper=!gh auth git-credential', *args], cwd=cwd)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publicar', action='store_true', help='Autorizar commit y push de esta ejecución')
    parser.add_argument('--base-remota', help='SHA remoto revisado; requerido al conectar por primera vez o reconciliar cambios externos')
    parser.add_argument('--retirar-zip-inicial', action='store_true', help='Migrar la carga inicial del ZIP a archivos fuente; conserva el ZIP local')
    parser.add_argument('--mensaje', default='Sincronizar Plantilla Maestra APA7')
    args = parser.parse_args()
    archive, payload = read_package()
    repo = json.loads(run(['gh', 'api', 'repos/' + REPO]))
    if not repo.get('permissions', {}).get('push') or repo['default_branch'] != BRANCH:
        raise RuntimeError('Se requiere permiso de escritura y rama main; revisar la configuración')
    user = json.loads(run(['gh', 'api', 'user', '--jq', '{login,id}']))
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    expected = args.base_remota or (state.get('commit') if state.get('repo') == REPO else None)
    if not expected:
        raise RuntimeError('Primera sincronización: revisa el remoto e indica --base-remota SHA')
    with tempfile.TemporaryDirectory(prefix='apa7-sync-') as tmp:
        checkout = Path(tmp) / 'repo'
        git('clone', '--quiet', '--single-branch', '--branch', BRANCH, 'https://github.com/' + REPO + '.git', str(checkout))
        before = git('rev-parse', 'HEAD', cwd=checkout)
        if before != expected:
            raise RuntimeError('El remoto cambió desde la última revisión. No se sobrescribe: compara y reconcilia primero. SHA actual: ' + before)
        previous = checkout / MANIFEST
        if previous.exists():
            old = json.loads(previous.read_text())['files']
            for name in set(old) - set(payload):
                safe_path(name)
                target = checkout / name
                if checkout.resolve() not in target.resolve().parents or target.is_symlink():
                    raise ValueError('Ruta previa no segura: ' + name)
                if target.is_file():
                    target.unlink()
        for name, data in payload.items():
            target = checkout / name
            if target.is_symlink() or checkout.resolve() not in target.resolve().parents:
                raise ValueError('Destino no seguro: ' + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        if args.retirar_zip_inicial:
            old_zip = checkout / archive.name
            if old_zip.exists():
                with ZipFile(old_zip) as z:
                    if z.testzip() is not None or z.read('index.html') != payload['index.html']:
                        raise ValueError('El ZIP remoto no corresponde al HTML revisado; no se retira')
                old_zip.unlink()
        git('add', '-A', cwd=checkout)
        # El manifiesto es parte deliberada del árbol público, incluso en clones antiguos.
        git('add', '-f', '--', MANIFEST, cwd=checkout)
        for name, data in payload.items():
            blob = git('rev-parse', ':' + name, cwd=checkout)
            expected_blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if blob != expected_blob:
                raise RuntimeError('Archivo omitido o transformado al preparar Git: ' + name)
        changes = git('diff', '--cached', '--stat', cwd=checkout)
        print(changes or 'Sin cambios: el contenido ya coincide.')
        if not args.publicar:
            print('Solo comparación. No se creó ningún commit ni se modificó GitHub.')
            return
        commit = before
        if changes:
            git('config', 'user.name', user['login'], cwd=checkout)
            git('config', 'user.email', str(user['id']) + '+' + user['login'] + '@users.noreply.github.com', cwd=checkout)
            git('commit', '--quiet', '-m', args.mensaje, '-m', 'Sincronización revisada desde Arena.ai; sin credenciales ni documentos personales.', cwd=checkout)
            commit = git('rev-parse', 'HEAD', cwd=checkout)
            git('push', 'origin', 'HEAD:' + BRANCH, cwd=checkout)
        actual = git('ls-remote', 'origin', 'refs/heads/' + BRANCH, cwd=checkout).split()[0]
        if actual != commit:
            raise RuntimeError('No se puede confirmar HEAD remoto. No se registra éxito.')
        record = {'repo': REPO, 'branch': BRANCH, 'commit': commit, 'files': len(payload), 'zip_sha256': hashlib.sha256(archive.read_bytes()).hexdigest()}
        STATE.parent.mkdir(exist_ok=True)
        STATE.write_text(json.dumps(record, indent=2) + '\n')
        print('Confirmado: https://github.com/' + REPO + '/commit/' + commit)
        print('Estado local sin credenciales: .git/apa7-sincronizacion.json')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, KeyError) as error:
        raise SystemExit(str(error))
