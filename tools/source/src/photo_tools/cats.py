import sys, re, time, html, urllib.request, urllib.parse, json, os
UA = "language-app-builder/1.0"
import subprocess
def get(u):
    r = subprocess.run(['curl','-s','-L','-m','60','-A',UA,u],capture_output=True); time.sleep(2)
    return r.stdout.decode('utf-8','replace')
out = {}
for c in sys.argv[1:]:
    h = get('https://commons.wikimedia.org/wiki/Category:' + urllib.parse.quote(c.replace(' ', '_')))
    fs = sorted(set(html.unescape(urllib.parse.unquote(x)) for x in re.findall(r'href="/wiki/(File:[^"]+?\.(?:jpg|JPG|jpeg))"', h)))
    out[c] = fs
    print('##', c, len(fs))
    for f in fs[:25]: print('  ', f)
    time.sleep(2.5)
