# 탄자니아 탭 사진: Wikimedia Commons에서 자유 라이선스 사진을 찾아 img/tz/<key>.jpg (가로 720px) + credits.json으로 저장.
# usage: python3 photos_tz.py <outdir>   (outdir/img/tz, outdir/credits_tz.json). PICK에 파일 이름을 적으면 그 파일을 씀.
import sys, os, json, re, io, urllib.request, urllib.parse
from PIL import Image
Q = {'dodoma': 'Dodoma', 'parliament': 'Bunge Dodoma', 'shilingi': 'Tanzanian shilling', 'kili': 'Kilimanjaro', 'rain': 'Dar es Salaam rain', 'coast': 'Tanzania beach', 'serengeti': 'Serengeti wildebeest', 'kilwa': 'Kilwa Kisiwani', 'bagamoyo': 'Bagamoyo', 'nyerere': 'Nyerere statue', 'church': 'Azania Front', 'choir': 'Tanzania choir', 'mosque': 'Zanzibar mosque', 'uhuru': 'Tanzania independence day', 'xmas': 'Christmas Tanzania', 'festival': 'Sauti za Busara', 'wedding': 'Tanzanian wedding', 'ugali': 'ugali', 'mishkaki': 'mishkaki', 'spice': 'Zanzibar spices', 'meal': 'Tanzanian food', 'greet': 'Tanzania handshake', 'street': 'Dar es Salaam street', 'daladala': 'daladala', 'market': 'Kariakoo', 'music': 'Tanzania musicians', 'tinga': 'Tingatinga', 'books': 'Swahili books', 'football': 'Benjamin Mkapa Stadium', 'kili2': 'Kilimanjaro Amboseli', 'ngoro': 'Ngorongoro Crater', 'stonetown': 'Stone Town Zanzibar', 'dar': 'Dar es Salaam harbour', 'victoria': 'Mwanza Lake Victoria'}
PICK = {}
OK = re.compile(r'^(CC0|Public domain|PD|CC BY(-SA)? [1-4]\.0)', re.I)
UA = {'User-Agent': 'LanguageAppPhotoFetch/1.0 (educational offline app; python-urllib)'}
import time
def get(u):
    for i in range(6):
        try:
            time.sleep(1.5); return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == 5: raise
            time.sleep(10 * (i + 1))
def api(**k):
    k.update(format='json', action='query')
    return json.loads(get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(k)))
def info(titles):
    r = api(prop='imageinfo', iiprop='url|extmetadata|size|mime', iiurlwidth=900, titles='|'.join(titles))
    out = []
    for pg in r.get('query', {}).get('pages', {}).values():
        ii = pg.get('imageinfo', [{}])[0]; m = ii.get('extmetadata', {})
        lic = m.get('LicenseShortName', {}).get('value', ''); a = re.sub('<[^>]+>', '', m.get('Artist', {}).get('value', '')).strip()
        out.append(dict(t=pg['title'], lic=lic, a=re.sub(r'\s+', ' ', a)[:60], url=ii.get('thumburl'), mime=ii.get('mime'), w=ii.get('width', 0), h=ii.get('height', 0)))
    return out
def cands(key):
    if key in PICK: return info([PICK[key]])
    r = api(list='search', srsearch=Q[key], srnamespace=6, srlimit=12)
    ts = [x['title'] for x in r['query']['search']]
    if not ts: return []
    c = {x['t']: x for x in info(ts)}
    return [c[t] for t in ts if t in c]
if __name__ == '__main__':
    O = sys.argv[1]; os.makedirs(O + '/img/tz', exist_ok=True)
    CR = json.load(open(O + '/credits_tz.json')) if os.path.exists(O + '/credits_tz.json') else {}
    only = sys.argv[2:] or list(Q)
    for k in only:
      if k in CR: continue
      try:
        got = None
        for c in cands(k):
            if c['mime'] != 'image/jpeg' or not OK.match(c['lic']) or c['w'] < 700 or c['h'] > c['w'] * 1.1: continue
            got = c; break
        if not got: print('NONE', k, flush=True); continue
        im = Image.open(io.BytesIO(get(got['url'].replace('//thumb.wikimedia.org/', '//upload.wikimedia.org/')))).convert('RGB')
        W = 720; im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
        if im.height > 540: t = (im.height - 540) // 2; im = im.crop((0, t, W, t + 540))
        im.save(f'{O}/img/tz/{k}.jpg', quality=68, optimize=True, progressive=True)
        a = got['a'] or '작자 미상'
        CR[k] = dict(w=im.width, h=im.height, a=a, lic=got['lic'], src=got['t'])
        json.dump(CR, open(O + '/credits_tz.json', 'w'), ensure_ascii=False, indent=0)
        print(k, got['lic'], a, got['t'], os.path.getsize(f'{O}/img/tz/{k}.jpg') // 1024, 'KB', flush=True)
      except Exception as e: print('ERR', k, str(e)[:80], flush=True)
    json.dump(CR, open(O + '/credits_tz.json', 'w'), ensure_ascii=False, indent=0)
