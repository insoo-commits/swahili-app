# v1.5: Lao app v2.75–v2.78 keyboard features ported into base/app.js + base/index.html (run once; asserts each anchor).
import re
A = '/home/user/sw/src/base/app.js'; H = '/home/user/sw/src/base/index.html'
s = open(A).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a)); s = s.replace(a, b)
rep('let REP=store.get("lao-rep",2);', 'let REP=store.get("lao-rep",2);/* v1.5 (Lao v2.76): K = Korean voice on/off */let SAYKO=store.get("lao-sayko",true)!==false;')
# v2.78: drop the Lao-only review pass after word-card bundle play
m = re.search(r'  if\(!single&&items\.every\(it=>it&&/\^cd-/\.test\(it\.id\|\|""\)\)\)\{.*?\}\)\}\n', s); assert m, 'review'
s = s.replace(m.group(0), '  /* v1.5 (Lao v2.78): no Lao-only review pass after 단어공부 묶음 재생; K turns Korean off instead */\n')
rep('function stopPlay(){P.token++;', 'function stopPlay(){P.rel=0;P.token++;')
rep('setTimeout(()=>{if(AUD){blobUrl("_gap450")', 'setTimeout(()=>{if(AUD){blobUrl("_gap150").catch(()=>{});blobUrl("_gap450")')
rep('Promise.all([blobUrl("_gap450"),blobUrl("_gap900")]', 'Promise.all([blobUrl("_gap150"),blobUrl("_gap450"),blobUrl("_gap900")]')
rep('function gapThen(tok,ms){', '/* v1.5 (Lao v2.76): the same sentence again = short pause only */\nfunction gapMs(it){const q=P.queue;if(P.i>=q.length||(q[P.i].rv&&q[P.i].rv0===P.i))return 900;let j=P.i;if(!SAYKO)while(j<q.length&&q[j].ko)j++;const n=q[j];return n&&!it.ko&&!n.ko&&n.text===it.text?150:450}\nfunction gapThen(tok,ms){')
rep('advQ();gapThen(tok,P.i>=P.queue.length||(P.queue[P.i].rv&&P.queue[P.i].rv0===P.i)?900:450)', 'advQ();gapThen(tok,gapMs(it))')
rep('function advQ(){if(P.hold!=null){P.i=P.hold;P.k++;return}const it=P.queue[P.i];if(!it){P.i++;return}', 'function advQ(){if(P.hold!=null){P.i=P.hold;P.k++;return}const it=P.queue[P.i];if(!it){P.i++;return}/* Enter released the loop: go on to the next item */if(P.rel){P.rel=0;P.k=0;P.i=it.ge+1;return}')
rep('const it=P.queue[P.i];cardSync(it);mark(it.id);showPlayer();', 'const it=P.queue[P.i];if(it.ko&&!SAYKO){advQ();nextPlay(tok);return}cardSync(it);mark(it.id);showPlayer();')
rep('function chainNext(){', 'function setSayKo(v){SAYKO=!!v;store.set("lao-sayko",SAYKO);const c=document.getElementById("koChk");if(c)c.checked=SAYKO}\nfunction chainNext(){')
# key badges on generated buttons
rep('${RPT}<span>연속 재생</span></button>', '${RPT}<span>연속 재생</span><kbd class="kc">C</kbd></button>', 2)
rep('${RPT}<span>묶음 재생</span></button>', '${RPT}<span>묶음 재생</span><kbd class="kc">G</kbd></button>', 2)
rep('<span class="nbl">← 이전 묶음</span>', '<span class="nbl"><kbd class="kc">&lt;</kbd>← 이전 묶음</span>')
rep('<span class="nbl">다음 묶음 →</span>', '<span class="nbl">다음 묶음 →<kbd class="kc">&gt;</kbd></span>')
# keyboard handler (Lao v2.78), placed before the main click handler
KB = r'''/* v1.5 = Lao v2.71–v2.78 keyboard: Space C G Esc ←→ , . Enter 1-5 - = Q W E K ? (Korean IME keys too) */
document.addEventListener("keydown",e=>{if(e.ctrlKey||e.metaKey||e.altKey)return;const t=e.target,tn=t&&t.tagName;if(tn==="INPUT"||tn==="TEXTAREA"||tn==="SELECT"||(t&&t.isContentEditable))return;
  if((e.key===","||e.key==="."||e.key==="<"||e.key===">")&&!S.q.trim()){const L=PARTS.flatMap(p=>p.subs.flatMap(x=>x.b)),k=L.indexOf(curBun());if(k>=0){e.preventDefault();if(P.active)stopPlay();const md=S.mode;goto(L[(k+(e.key==="."||e.key===">"?1:-1)+L.length)%L.length]);if(md!=="dlg"&&!B[curBun()].info){S.mode=md;save();render()}}return}
  if(e.key==="k"||e.key==="K"||e.key==="ㅏ"){e.preventDefault();setSayKo(!SAYKO);return}
  {const h=document.getElementById("kbhelp");if(h){h.remove();e.preventDefault();return}else if(e.key==="?"){e.preventDefault();const d=document.createElement("div");d.id="kbhelp";d.style.cssText="position:fixed;inset:0;z-index:9999;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.35)";d.innerHTML='<div style="background:var(--sheet,#fff);color:var(--ink,#222);border-radius:16px;padding:18px 22px;max-width:92vw;max-height:88vh;overflow:auto;font-size:15px;line-height:1.75;box-shadow:0 10px 40px rgba(0,0,0,.3)"><b style="font-size:17px">키보드 단축키</b><table style="border-collapse:collapse;margin-top:8px">'+[["Space","묶음 재생 시작 · 일시정지 · 재개"],["C","연속 재생"],["G","묶음 재생"],["Esc","정지"],["← →","이전 · 다음 문장"],["< >  (, .)","이전 · 다음 묶음"],["Enter","지금 문장 무한 반복 켜기 · 끄기"],["1 ~ 5","반복 횟수"],["-  =","배속 느리게 · 빠르게"],["Q W E","예문보기 · 단어공부 · 확인퀴즈"],["K","한국어 말하기 켜기 · 끄기"],["?","이 목록 열기 · 닫기"]].map(r=>'<tr><td style="padding:1px 16px 1px 0;white-space:nowrap"><b>'+r[0]+'</b></td><td>'+r[1]+'</td></tr>').join("")+'</table></div>';d.addEventListener("click",()=>d.remove());document.body.appendChild(d);return}}
  {const k=e.key.toLowerCase(),ctl=document.getElementById("controls");if(ctl&&!ctl.hidden&&!S.q.trim()){
    if(k==="c"||k==="ㅊ"||k==="g"||k==="ㅎ"){const b=document.querySelector(k==="c"||k==="ㅊ"?'#bact [data-playbundle][data-chain]':'#bact [data-playbundle]:not([data-chain])');if(b){e.preventDefault();b.click()}return}
    if(/^[1-5]$/.test(e.key)){const r=document.getElementById("repSel");if(r){e.preventDefault();r.value=e.key;r.dispatchEvent(new Event("change",{bubbles:true}))}return}
    if(e.key==="-"||e.key==="_"||e.key==="="||e.key==="+"){const r=document.getElementById("rateSel");if(r){e.preventDefault();const j=Math.max(0,Math.min(r.options.length-1,r.selectedIndex+(e.key==="="||e.key==="+"?1:-1)));if(j!==r.selectedIndex){r.selectedIndex=j;r.dispatchEvent(new Event("change",{bubbles:true}))}}return}
    {const m={q:"m-dlg","ㅂ":"m-dlg",w:"m-cards","ㅈ":"m-cards",e:"m-quiz","ㄷ":"m-quiz"}[k];if(m){const b=document.getElementById(m);if(b){e.preventDefault();if(P.active)stopPlay();b.click()}return}}
    if((e.key===" "||e.code==="Space")&&!P.active&&tn!=="BUTTON"&&tn!=="A"){const b=document.querySelector('#bact [data-playbundle]:not([data-chain])');if(b){e.preventDefault();b.click()}return}}}
  if(!P.active)return;
  if(e.key===" "||e.code==="Space"){e.preventDefault();if(P.hold!=null)releaseHold();else setPaused(!P.paused);showPlayer();return}
  if(e.key==="Escape"){e.preventDefault();stopPlay();return}
  if(e.key==="Enter"){e.preventDefault();if(P.single)return;if(P.hold!=null){P.hold=null;holdMark(null);P.rel=1;P.k=0}else{const q=P.queue,c=q[Math.min(P.i,q.length-1)];if(!c)return;const j=c.ko?q.findIndex(x=>x&&x.gi===c.gi&&!x.ko):P.i;if(j<0)return;P.rel=0;P.hold=j;P.k=0;holdMark(j)}showPlayer();return}
  if(e.key==="ArrowRight"||e.key==="ArrowLeft"){e.preventDefault();if(P.single||P.hold!=null)return;const tok=P.token;try{aud().pause()}catch(_){}P.k=0;P.rel=0;{const q=P.queue,c=q[Math.min(P.i,q.length-1)]||{},R=e.key==="ArrowRight";let j=-1;if(c.gi!=null&&!c.rv){const g=c.gi+(R?1:-1);j=q.findIndex(x=>x&&!x.rv&&x.gi===g);if(j<0&&R){j=q.findIndex((x,ix)=>ix>P.i&&x&&x.gi!==c.gi);if(j<0)j=q.length}if(j<0&&!R)j=q.findIndex(x=>x&&x.gi===c.gi)}if(j<0)j=R?P.i+1:Math.max(0,P.i-1);P.i=j}if(P.paused)setPaused(false);nextPlay(tok)}});
{const c=document.getElementById("koChk");if(c){c.checked=SAYKO;c.addEventListener("change",()=>{setSayKo(c.checked);try{c.blur()}catch(e){}})}}
'''
rep('document.addEventListener("click",e=>{\n  const ko=', KB + 'document.addEventListener("click",e=>{\n  const ko=')
open(A, 'w').write(s)

h = open(H).read()
def hr(a, b):
    global h
    assert h.count(a) == 1, (a[:70], h.count(a)); h = h.replace(a, b)
hr('<span class="ll">예문보기</span></button>', '<span class="ll">예문보기</span><kbd class="kc">Q</kbd></button>')
hr('<span class="ll">단어공부</span></button>', '<span class="ll">단어공부</span><kbd class="kc">W</kbd></button>')
hr('<span class="ll">확인퀴즈</span></button>', '<span class="ll">확인퀴즈</span><kbd class="kc">E</kbd></button>')
hr('<span class="ll olab">반복</span>', '<span class="ll olab">반복<kbd class="kc">1~5</kbd></span>')
hr('<span class="ll olab">배속</span>', '<span class="ll olab">배속<kbd class="kc">±</kbd></span>')
hr('<div class="bact" id="bact"></div>', '<div class="bact" id="bact"></div>\n      <div class="kbinfo" id="kbinfo"><span><kbd class="kc">Esc</kbd>재생 정지</span><span><kbd class="kc">Enter</kbd>무한 반복/취소</span><span><kbd class="kc">←</kbd>이전 문장</span><span><kbd class="kc">→</kbd>다음 문장</span><label class="kok"><input type="checkbox" id="koChk" checked><kbd class="kc">K</kbd>한국어 말하기</label></div>')
CSS = '''
/* v1.5 = Lao v2.75–v2.77: key badges (PC and pad only), key info line under 연속/묶음 재생, flatter header */
.kc{display:none;font:600 10.5px/1 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;min-width:17px;height:17px;padding:0 4px;box-sizing:border-box;align-items:center;justify-content:center;border:1px solid currentColor;border-bottom-width:2.5px;border-radius:5px;margin-left:6px;opacity:.72;vertical-align:1px;letter-spacing:0;white-space:nowrap}
html.tab .kc{display:inline-flex;font-size:12.5px;min-width:21px;height:21px;border-radius:6px}
@media (hover:hover) and (pointer:fine){.kc{display:inline-flex}}
.nextbun .nbl{display:inline-flex;align-items:center}.nextbun.prevbun .kc{margin-left:0;margin-right:6px}
.kbinfo{display:none;order:99;flex-basis:100%;justify-content:center;flex-wrap:wrap;gap:4px 16px;color:var(--muted);margin-top:2px;font-size:11.5px}
.kbinfo span,.kbinfo label{display:inline-flex;align-items:center;gap:0;white-space:nowrap}.kbinfo .kc{margin:0 5px 0 0;font-size:10px;height:16px;min-width:16px}
.kbinfo label{cursor:pointer;color:var(--muted)}.kbinfo input{margin:0 6px 0 0;width:15px;height:15px;accent-color:var(--accent);cursor:pointer}
html.tab .kbinfo{display:flex;font-size:14px}html.tab .kbinfo input{width:18px;height:18px}html.tab .kbinfo .kc{font-size:11.5px;height:19px;min-width:19px}
@media (hover:hover) and (pointer:fine){.kbinfo{display:flex}}
header{padding-top:12px!important;padding-bottom:10px!important;min-height:0!important}
header .eyebrow{line-height:1.15;display:block}
h1.lotitle{line-height:.98!important;margin-top:-.06em!important}
'''
h = h.replace('</style>', CSS + '</style>', 1)
open(H, 'w').write(h)
print('ok')
