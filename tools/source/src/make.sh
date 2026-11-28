#!/bin/bash
# Full build: bash make.sh <version> <outdir>. Needs edge-tts, ffmpeg.
# Every clip ever made is kept in $AUD (16 kbps); only the clips in use go to <outdir>/audio.
set -e; H=$(cd "$(dirname "$0")"; pwd); V=${1:-0.1}; OUT=${2:-$H/../pwa}; AUD=${AUD:-$H/../audio_all}; W=$(mktemp -d)
python3 $H/build.py $W/out $V
mkdir -p $AUD
(cd $W && python3 $H/tts_gen.py lists/f.json $AUD sw-TZ-RehemaNeural && python3 $H/tts_gen.py lists/m.json $AUD sw-TZ-DaudiNeural && python3 $H/tts_gen.py lists/k.json $AUD ko-KR-SunHiNeural) 2>&1 | grep -v -i warn | grep -v '^todo 0' || true
python3 - $W $H $AUD <<'P'
import json,sys,os,shutil
W,H,AUD=sys.argv[1:4];ks=[];AV=json.load(open(f'{H}/aver.json'))
for n in 'fmk': ks+=list(json.load(open(f'{W}/lists/{n}.json')))
miss=[k for k in ks if not os.path.exists(f'{AUD}/{k}.mp3')];assert not miss,miss[:20]
os.makedirs(f'{W}/out/audio',exist_ok=True)
for k in ks: shutil.copyfile(f'{AUD}/{k}.mp3',f'{W}/out/audio/{k}.mp3')
open(f'{W}/out/audio/index.js','w').write('window.AUDIO_INDEX='+json.dumps({k:AV.get(k,1) for k in sorted(ks)},separators=(',',':'))+';')
print('audio clips',len(ks))
P
cp $W/lint.json $H/../lint.json
rm -rf $OUT; mkdir -p $OUT; cp -r $W/out/. $OUT/; rm -rf $W
mkdir -p $OUT/img/tz && cp $H/photos/*.jpg $OUT/img/tz/ && python3 $H/info_patch.py $OUT $H/photos/credits.json
python3 $H/help_patch.py $OUT
python3 - $OUT/index.html <<'P'
import sys;f=sys.argv[1];s=open(f).read();a='이 기기에만 저장됩니다.</p>';assert s.count(a)==1
open(f,'w').write(s.replace(a,'이 기기에만 저장됩니다. 키보드에서 <kbd>?</kbd>를 누르면 단축키를 볼 수 있어요.</p>'))
P

# RYU 2026-11-24: new design (Lao v3.30-v3.34 look) + sub pictures, then fit tips to the picture height
python3 /mnt/project-files/design4/apply/apply.py swahili-app --out $OUT
python3 /mnt/project-files/design4/apply/fit_tips.py $OUT/app.js $H/fit_removed.json
python3 /mnt/project-files/design4/apply/patch_band.py $OUT
