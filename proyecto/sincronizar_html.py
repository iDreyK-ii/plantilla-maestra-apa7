"""Alias idéntico al HTML canónico, sin depender del comando Unix cp."""
from pathlib import Path
from shutil import copyfile
root = Path(__file__).resolve().parent.parent
copyfile(root / 'Plantilla_Maestra_APA7.html', root / 'index.html')
assert (root / 'index.html').read_bytes() == (root / 'Plantilla_Maestra_APA7.html').read_bytes()
print('Alias index.html sincronizado byte a byte.')
