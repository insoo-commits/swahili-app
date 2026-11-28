# 탄자니아 탭(P8) 정보 화면을 만든 앱에 넣어요. usage: python3 info_patch.py <pwa dir> [credits.json]
import sys,json,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import info_tz as li
R=sys.argv[1];CR=json.load(open(sys.argv[2])) if len(sys.argv)>2 else {}
def ph(m):
    k,cap=m.group(1),m.group(2);c=CR.get(k)
    if not c: return ''
    return f'<figure class="ph"><img src="img/tz/{k}.jpg" width="{c["w"]}" height="{c["h"]}" loading="lazy" alt=""><figcaption>{cap}<small>사진: {c["a"]} · {c["lic"]} · Wikimedia Commons</small></figcaption></figure>'
B={};blab={}
for bid,(t,lo,html) in li.B.items():
    html=re.sub(r'@@PHOTO:([a-z0-9]+):(.*?)@@',ph,html)
    html=html.replace('<div class="top2"><div></div><div>','<div class="top1"><div>')
    B[bid]=dict(t=t,h=lo,i="",w=[],tp=[],nx=[],pr=[],dl=[],sm=None,qz=[],info=f'<h2>{t}</h2><div class="sub2 lo">{lo}</div>'+html)
    blab[bid]=[t,lo]
part=dict(id='P8',ko='탄자니아',desc='탄자니아를 이해하기 위한 자료',subs=[dict(id=sid,name=nm,b=[k for k in li.B if k.startswith('8-%02d-'%(n+1))]) for n,(sid,nm) in enumerate(li.SUBS)])
line='/* 탄자니아 탭(P8) = info pages, no words/audio (src/info_tz.py, info_patch.py) */const TZINFO='+json.dumps(dict(part=part,B=B,blab=blab),ensure_ascii=False,separators=(',',':'))+';DATA.P.push(TZINFO.part);Object.assign(DATA.B,TZINFO.B);\n'
s=open(R+'/app.js').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:60],s.count(a)); s=s.replace(a,b)
rep('const PARTEN=',line+'const PARTEN=')
rep('P7:"GRAMMAR"}','P7:"GRAMMAR",P8:"TANZANIA"}')
rep('const L=PARTS.flatMap(p=>p.subs.flatMap(x=>x.b)),cur=','const L=PARTS.flatMap(p=>p.subs.flatMap(x=>x.b)).filter(x=>!B[x].info),cur=')
rep('const all=Object.values(B),nw=','const all=Object.values(B).filter(b=>!b.info),nw=')
rep('${cs.b.length}묶음 ${nwd.toLocaleString()}단어 ${nsb.toLocaleString()}문장`}','${cs.b.length}묶음`+(B[cs.b[0]].info?"":` ${nwd.toLocaleString()}단어 ${nsb.toLocaleString()}문장`)}')
rep('  $("#controls").hidden=false;renderBand();\n','  if(typeof TZINFO!=="undefined"&&!BLAB["8-01-01"])Object.assign(BLAB,TZINFO.blab);{const ib=B[curBun()];if(ib&&ib.info){$("#controls").hidden=true;renderBand();$("#view").innerHTML=`<article class="info">${ib.info}</article>`+nextRow(curBun());snapLater();return}}\n  $("#controls").hidden=false;renderBand();\n')
open(R+'/app.js','w').write(s)
CSS='''<style>/* 탄자니아 탭 info pages */
:root{--p8:#1C6FA8;--p8-soft:#E2EFF8}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--p8:#7DBDEB;--p8-soft:#14283A}}
:root[data-theme="dark"]{--p8:#7DBDEB;--p8-soft:#14283A}
[data-g="P8"]{--accent:var(--p8);--accent-soft:var(--p8-soft)}
.info{padding:6px 4px 12px;font-size:15.5px;line-height:1.65;color:var(--ink)}
.info h2{font-size:21px;margin:4px 0 0;line-height:1.3}
.info .sub2{color:var(--muted);font-size:14px;margin-bottom:14px}
.info figure{margin:0 0 14px;text-align:center}
.info figure svg.flag,.info figure img{display:block;width:100%;max-width:420px;height:auto;margin:0 auto;border-radius:8px;box-shadow:0 1px 6px rgba(0,0,0,.18)}
.info figure img{background:var(--line)}
.info figcaption{font-size:13px;color:var(--muted);margin-top:6px;line-height:1.5}
.info figcaption small{display:block;font-size:11px;opacity:.85}
.info .facts{width:100%;border-collapse:collapse;margin:2px 0 14px;font-size:14.5px}
.info .facts th{width:31%;text-align:left;font-weight:700;color:var(--accent);padding:7px 6px;vertical-align:top;border-bottom:1px solid var(--line)}
.info .facts td{padding:7px 6px;border-bottom:1px solid var(--line)}
.info h3{font-size:16.5px;margin:18px 0 6px;padding-left:9px;border-left:4px solid var(--accent);line-height:1.35}
.info p{margin:0 0 8px}
.info .r{color:var(--accent)}
.info .clr{display:flex;flex-direction:column;gap:7px;margin:6px 0 10px}
.info .clr div{display:flex;gap:10px;align-items:flex-start}
.info .clr i{flex:none;width:22px;height:22px;border-radius:5px;margin-top:2px;border:1px solid var(--line)}
.info .terms{background:var(--accent-soft);border-radius:12px;padding:8px 14px;margin:8px 0 14px}
.info .terms div{padding:5px 0;border-bottom:1px dashed var(--line)}.info .terms div:last-child{border:0}
.info .terms .lo{font-size:17px;font-weight:700}.info .terms .r{margin:0 8px 0 6px}
@media (min-width:860px){.info{padding:8px 14px 14px}.info .top2{display:grid;grid-template-columns:44% 1fr;gap:28px;align-items:start}.info .two{display:grid;grid-template-columns:1fr 1fr;gap:32px}.info .facts th{width:28%}}
/* v1.18 (Lao v3.18/v3.22): 탄자니아 탭 - 줄간격 줄이고 내용별 상자 */.info{line-height:1.5;font-size:15px}.info .sub2{margin-bottom:8px}.info h3{margin:10px 0 4px;font-size:15.5px}.info p{margin:0 0 4px}.info figure{margin:0 0 8px}.info figcaption{margin-top:3px;line-height:1.35}.info .facts{margin:0 0 8px;font-size:14px}.info .facts th,.info .facts td{padding:4px 6px}.info .terms{padding:4px 12px;margin:6px 0 8px}.info .terms div{padding:3px 0}.info .terms .lo{font-size:16px}.info .two{display:grid;gap:8px;margin-top:8px}.info .two>div{border:1px solid var(--line);border-radius:12px;padding:2px 12px 8px;background:var(--sheet)}.info .two>div>h3:first-child{margin-top:8px}.info .top2,.info .top1{margin-bottom:4px}.info .cards{display:grid;grid-template-columns:1fr;gap:8px;margin:8px 0}.info .card{border:1px solid var(--line);border-radius:12px;padding:8px 12px;background:var(--sheet)}.info .card h4{margin:0 0 4px;font-size:15px;color:var(--accent);padding-bottom:3px;border-bottom:1px dashed var(--line)}.info .card ul,.info .card ol{margin:0;padding-left:1.15em}.info .card li{margin:1px 0}.info .card .facts{margin:0}.info .note{background:var(--accent-soft);border-radius:10px;padding:6px 12px;font-size:14px;margin:8px 0}.info .warn{border-left:4px solid #c0392b;background:rgba(192,57,43,.08);border-radius:6px;padding:6px 12px;font-size:14px;margin:8px 0}.info ol.steps{counter-reset:st;list-style:none;padding:0;margin:6px 0 8px}.info ol.steps li{counter-increment:st;position:relative;padding:3px 0 3px 30px}.info ol.steps li::before{content:counter(st);position:absolute;left:0;top:3px;width:21px;height:21px;border-radius:50%;background:var(--accent);color:var(--sheet);font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center}.info .phr{border:1.5px solid var(--accent);border-radius:12px;padding:4px 12px;margin:8px 0}.info .phr .ph-t{font-size:13px;font-weight:700;color:var(--accent);padding:2px 0}.info .phr>div:not(.ph-t){padding:3px 0;border-top:1px dashed var(--line)}.info .phr .lo{font-size:16px;font-weight:700}.info .phr .r{margin:0 8px 0 6px}.info .phr .m{color:var(--muted)}.info .asof{font-size:12.5px;color:var(--muted);margin-top:8px}.info .rph figure img{max-width:360px}.info .rph+.rph{margin-top:4px}.info .gal{margin:10px 0 4px}.info .gal-t{font-size:13px;font-weight:700;color:var(--accent);margin-bottom:4px}.info .gal-g{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}.info .gal figure{margin:0}.info .gal figure img{width:100%;height:84px;object-fit:cover;border-radius:6px;box-shadow:none;max-width:none}.info .gal figcaption{font-size:11.5px;margin-top:2px}.info figure img{cursor:zoom-in}@media (min-width:860px){.info .two{grid-template-columns:1fr 1fr;gap:12px}.info .cards{grid-template-columns:1fr 1fr;gap:10px}.info .gal-g{grid-template-columns:repeat(5,1fr)}.info .gal figure img{height:110px}.info .top2{gap:20px}}
.info h3.more{margin-top:18px;padding-top:12px;border-top:1px dashed var(--line,#ccc)}.info .card h4{border-left:0;padding-left:0}.info .cards>.warn{grid-column:1/-1;margin:0}
</style>'''
h=open(R+'/index.html').read()
assert '</head>' in h and '탄자니아 탭 info pages' not in h
h=h.replace('</head>',CSS+'</head>',1)
open(R+'/index.html','w').write(h)
print('info pages',len(B),'bytes',len(line))
