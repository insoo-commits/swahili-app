"""slow.py picks.json [passes] : trickle download. One request every ~25 s; metadata cached in meta.json; out/<key>.jpg + credits.json."""
import sys, re, time, html, json, os, io, hashlib, urllib.request, urllib.parse
from PIL import Image
UA = 'language-app-builder/1.0'
D = os.path.dirname(os.path.abspath(__file__)); os.makedirs(D + '/out', exist_ok=True)
def load(p): return json.load(open(p)) if os.path.exists(p) else {}
CRP = D + '/credits.json'; MP = D + '/meta.json'; CR = load(CRP); META = load(MP)
GAP = 8
def get(u, binary=False):
    import subprocess
    r = subprocess.run(['curl', '-s', '-L', '-m', '60', '-A', UA, '-w', '\\n%{http_code}', u], capture_output=True)
    time.sleep(GAP)
    body, _, code = r.stdout.rpartition(b'\n')
    if code != b'200':
        print('  fail', code, flush=True); return None
    return body if binary else body.decode('utf-8', 'replace')
def strip(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', s))).strip()
OK_LIC = re.compile(r'^(CC BY(-SA)? [0-9.]+|CC0|Public domain|CC BY-SA|CC BY)', re.I)
PICKS = json.load(open(sys.argv[1])); passes = int(sys.argv[2]) if len(sys.argv) > 2 else 6
for ps in range(passes):
    todo = [k for k in PICKS if not (k in CR and os.path.exists(f'{D}/out/{k}.jpg')) and META.get(PICKS[k]) != 'bad']
    print('pass', ps, 'todo', len(todo), flush=True)
    if not todo: break
    for key in todo:
        name = PICKS[key]; q = urllib.parse.quote(name.replace(' ', '_'))
        if name not in META:
            h = get('https://commons.wikimedia.org/wiki/File:' + q)
            if not h: continue
            h = h.replace('&#95;', '_')
            m = re.search(r'class="licensetpl_short"[^>]*>(.*?)</span>', h, re.S); lic = strip(m.group(1)) if m else ''
            m = re.search(r'id="fileinfotpl_aut".*?<td[^>]*>(.*?)</td>', h, re.S); aut = strip(m.group(1)) if m else ''
            aut = re.sub(r'\s*\(talk.*$', '', aut)[:60]
            if not OK_LIC.match(lic) or not aut:
                print('  SKIP', key, name, '| lic:', lic, '| author:', aut, flush=True); META[name] = 'bad'
            else: META[name] = [aut, lic]
            json.dump(META, open(MP, 'w'), ensure_ascii=False)
            if META[name] == 'bad': continue
        aut, lic = META[name]
        md = hashlib.md5(name.replace(' ', '_').encode()).hexdigest()
        b = get(f'https://upload.wikimedia.org/wikipedia/commons/thumb/{md[0]}/{md[:2]}/{q}/960px-{q}', True)
        if not b: continue
        try: im = Image.open(io.BytesIO(b)).convert('RGB')
        except Exception as e: print('  BADIMG', key, e, flush=True); continue
        w, hh = im.size
        if hh > w * 0.8:
            nh = int(w * 0.75); t = (hh - nh) // 2; im = im.crop((0, t, w, t + nh))
        im.thumbnail((800, 800))
        for qv in (72, 64, 56, 48):
            buf = io.BytesIO(); im.save(buf, 'JPEG', quality=qv, optimize=True, progressive=True)
            if buf.tell() <= 110_000: break
        open(f'{D}/out/{key}.jpg', 'wb').write(buf.getvalue())
        CR[key] = dict(w=im.size[0], h=im.size[1], a=aut, lic=lic, src=name)
        json.dump(CR, open(CRP, 'w'), ensure_ascii=False, indent=0)
        print('ok', key, im.size, buf.tell() // 1024, 'KB |', aut, '|', lic, flush=True)
