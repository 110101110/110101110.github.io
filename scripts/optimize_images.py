#!/usr/bin/env python3
"""Generate committed image variants and Jekyll metadata. Requires Pillow."""
import json
import re
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assets/img'
OUTPUT = SOURCE / 'optimized'
OUTPUT.mkdir(exist_ok=True)
names = {'homepage_1.png', 'homepage_2.png'}
for post in (ROOT / '_posts').glob('*.md'):
    text = post.read_text()
    names.update(re.findall(r'^image:\s*(.+)$', text, re.M))
    names.update(re.findall(r'src="/assets/img/([^"]+)"', text))
    names.update(re.findall(r'{% include image.html file="([^"]+)"', text))
metadata = {}
for name in sorted(names):
    try:
        opened = Image.open(SOURCE / name)
    except UnidentifiedImageError:
        # Some legacy uploads have JPEG names but contain HEIC data.
        with tempfile.TemporaryDirectory() as directory:
            converted = Path(directory) / 'converted.png'
            subprocess.run(['heif-convert', str(SOURCE / name), str(converted)], check=True, capture_output=True)
            opened = Image.open(converted)
            opened.load()
    with opened as original:
        image = ImageOps.exif_transpose(original)
        record = {'width': image.width, 'height': image.height, 'original': '/assets/img/' + name}
        if getattr(original, 'is_animated', False):
            record['fallback'] = record['original']
        else:
            stem = re.sub(r'[^a-z0-9_-]+', '-', Path(name).stem.lower()).strip('-')
            pixel_art = name.startswith('fish')
            alpha = 'A' in image.getbands() and image.getchannel('A').getextrema()[0] < 255
            extension = 'png' if alpha or pixel_art else 'jpg'
            image = image.convert('RGBA' if alpha else 'RGB')
            max_width = 2200 if name == 'homepage_1.png' else 1200
            widths = sorted(set(min(w, image.width) for w in (480, 800, 1200, max_width)))
            variants = []
            for width in widths:
                height = round(image.height * width / image.width)
                resized = image.resize((width, height), Image.Resampling.NEAREST if pixel_art else Image.Resampling.LANCZOS)
                basename = f'{stem}-{width}'
                resized.save(OUTPUT / (basename + '.webp'), 'WEBP', quality=85, method=6, lossless=pixel_art)
                options = {'optimize': True} if extension == 'png' else {'quality': 85, 'optimize': True, 'progressive': True}
                resized.save(OUTPUT / (basename + '.' + extension), **options)
                variants.append({'width': width, 'height': height, 'webp': '/assets/img/optimized/' + basename + '.webp', 'fallback': '/assets/img/optimized/' + basename + '.' + extension})
            record['variants'] = variants
            fallback = min(variants, key=lambda v: abs(v['width'] - (1200 if name.startswith('homepage') else 800)))
            record['fallback'] = fallback['fallback']
        metadata[name] = record
(ROOT / '_data/images.json').write_text(json.dumps(metadata, indent=2) + '\n')
print(f'Generated variants for {len(metadata)} images; animated originals preserved.')
