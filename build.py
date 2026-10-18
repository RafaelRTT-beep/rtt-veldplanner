#!/usr/bin/env python3
"""Bouwt index.html uit src/app.html en voegt jsPDF en qrcode-generator in.

Daardoor werken PDF en QR ook zonder internet, en is index.html meteen de offline-versie.

  python3 build.py                     -> index.html
  python3 build.py --icloud            -> ook de offline-kopie in iCloud bijwerken
"""
import base64, hashlib, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent
ICLOUD = pathlib.Path.home() / 'Library/Mobile Documents/com~apple~CloudDocs/RtT files/05 Locaties & Plattegronden/RTT Veldplanner/RTT Veldplanner (offline).html'

# SRI-hashes zoals cdnjs ze publiceert; zo weet je zeker dat de ingebouwde bibliotheken ongewijzigd zijn
VENDOR = {
    'jspdf': ('vendor/jspdf.umd.min.js', 'jsPDF 2.5.1 (MIT)', 'qZvrmS2ekKPF2mSznTQsxqPgnpkI4DNTlrdUmTzrDgektczlKNRRhy5X5AAOnx5S09ydFYWWNSfcEqDTTHgtNA=='),
    'qrcode': ('vendor/qrcode.min.js', 'qrcode-generator 1.4.4 (MIT)', 'ZDSPMa/JM1D+7kdg2x3BsruQ6T/JpJo3jWDWkCZsP+5yVyp1KfESqLI+7RqB5k24F7p2cV7i2YHh/890y6P6Sw=='),
}

html = (ROOT / 'src/app.html').read_text(encoding='utf-8')
for key, (path, name, sri) in VENDOR.items():
    data = (ROOT / path).read_bytes()
    got = base64.b64encode(hashlib.sha512(data).digest()).decode()
    if got != sri:
        sys.exit(f'{path}: hash klopt niet met cdnjs ({got[:16]}…)')
    js = data.decode('utf-8')
    if '</script' in js.lower():
        sys.exit(f'{path} bevat </script en kan niet ingebouwd worden')
    marker = f'<!--VENDOR:{key}-->'
    if html.count(marker) != 1:
        sys.exit(f'markering {marker} niet precies één keer gevonden')
    html = html.replace(marker, f'<script>/* {name}, ingebouwd zodat het ook zonder internet werkt */\n{js}\n</script>')

out = ROOT / 'index.html'
out.write_text(html, encoding='utf-8')
print(f'index.html  {len(html.encode()) / 1024:.0f} KB')

if '--icloud' in sys.argv:
    shutil.copyfile(out, ICLOUD)
    print(f'offline-kopie bijgewerkt: {ICLOUD}')
