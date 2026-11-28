
;/* v1.4 RYU: keyboard shortcuts (same keys as the Lao app). Keys by e.code so a Korean IME (ㅊ ㅎ …) works too. */
(function(){
const MODES=["dlg","cards","quiz"];
function typing(t){const tn=t&&t.tagName;return tn==="INPUT"||tn==="TEXTAREA"||tn==="SELECT"||(t&&t.isContentEditable)}
let tT;function toast(s){let d=document.getElementById("kbToast");if(!d){d=document.createElement("div");d.id="kbToast";document.body.appendChild(d)}d.textContent=s;d.classList.add("on");clearTimeout(tT);tT=setTimeout(()=>d.classList.remove("on"),1100)}
function btn(sel){return document.querySelector("#view "+sel)||document.querySelector(sel)}
function click(el){if(el){el.click();return true}return false}
function groupBtn(){return btn("[data-playbundle]:not([data-chain])")}
function chainBtn(){return btn("[data-playbundle][data-chain]")}
function setSel(id,v,lab){const s=document.getElementById(id);if(!s)return;s.value=String(v);s.dispatchEvent(new Event("change",{bubbles:true}));toast(lab+" "+s.options[s.selectedIndex].text)}
function stepRate(d){const s=document.getElementById("rateSel");if(!s)return;const i=Math.max(0,Math.min(s.options.length-1,s.selectedIndex+d));setSel("rateSel",s.options[i].value,"배속")}
function startGroup(){if(!click(groupBtn()))toast("이 화면에는 재생할 묶음이 없어요")}
function holdToggle(){if(!P.active)return;if(P.hold!=null){releaseHold();showPlayer();toast("무한 반복 끔");return}
  const q=P.queue,c=q[Math.min(P.i,q.length-1)];if(!c||c.rv){toast("복습 중에는 무한 반복을 쓸 수 없어요");return}
  let idx=c.id?q.findIndex(x=>x&&x.id===c.id&&!x.ko):P.i;if(idx<0)idx=P.i;holdAt(idx);toast("∞ 이 문장 무한 반복")}
function step(R){if(!P.active||P.single||P.hold!=null)return;const tok=P.token;try{aud().pause()}catch(_){}P.k=0;
  const q=P.queue,c=q[Math.min(P.i,q.length-1)]||{};let j=-1;
  if(c.gi!=null&&!c.rv){const g=c.gi+(R?1:-1);j=q.findIndex(x=>x&&!x.rv&&x.gi===g);if(j<0&&R){j=q.findIndex((x,ix)=>ix>P.i&&x&&x.gi!==c.gi);if(j<0)j=q.length}if(j<0&&!R)j=q.findIndex(x=>x&&x.gi===c.gi)}
  if(j<0)j=R?P.i+1:Math.max(0,P.i-1);P.i=j;if(P.paused)setPaused(false);nextPlay(tok)}
const HELP=[["C","연속 재생 (다시 누르면 멈춤)"],["G","묶음 재생 (다시 누르면 멈춤)"],["Space","일시정지 · 재개 (멈춰 있으면 묶음 재생)"],["← →","이전 · 다음 문장"],[", .","이전 · 다음 묶음"],["1 ~ 5","반복 횟수"],["- =","배속 낮추기 · 높이기"],["Enter","지금 문장 무한 반복 켜기 · 끄기 (∞)"],["Esc","재생 취소"],["Q W E","예문보기 · 단어공부 · 확인퀴즈"],["?","이 단축키 목록"]];
function help(){let d=document.getElementById("kbHelp");if(d){d.remove();return}d=document.createElement("div");d.id="kbHelp";
  d.innerHTML='<div class="kbbox" role="dialog" aria-label="키보드 단축키"><h3>키보드 단축키</h3><table>'+HELP.map(r=>`<tr><th><kbd>${r[0]}</kbd></th><td>${r[1]}</td></tr>`).join("")+'</table><p>한글 자판 상태에서도 돼요. ↑ ↓는 화면 스크롤이에요.</p><button type="button">닫기</button></div>';
  d.addEventListener("click",e=>{if(e.target===d||e.target.tagName==="BUTTON")d.remove()});document.body.appendChild(d)}
document.addEventListener("keydown",e=>{if(e.ctrlKey||e.metaKey||e.altKey||typing(e.target))return;
  const c=e.code,k=e.key,hp=document.getElementById("kbHelp");
  if(hp&&(c==="Escape"||c==="Slash"||c==="Enter"||c==="Space")){e.preventDefault();hp.remove();return}
  if(c==="Slash"&&e.shiftKey||k==="?"){e.preventDefault();help();return}
  if(e.repeat&&c!=="ArrowLeft"&&c!=="ArrowRight")return;
  let done=true;
  switch(c){
  case "Space":if(P.active){if(P.hold!=null)releaseHold();else setPaused(!P.paused);showPlayer()}else startGroup();break;
  case "Escape":if(P.active)stopPlay();else done=false;break;
  case "ArrowRight":case "ArrowLeft":if(P.active)step(c==="ArrowRight");else done=false;break;
  case "KeyC":if(P.active&&P.chain)stopPlay();else if(!click(chainBtn()))toast("이 화면에는 연속 재생이 없어요");break;
  case "KeyG":if(P.active&&!P.chain&&!P.single)stopPlay();else startGroup();break;
  case "Comma":click(document.querySelector(".nextbun.prevbun"));break;
  case "Period":click(document.querySelector(".nextbun:not(.prevbun)"));break;
  case "Digit1":case "Digit2":case "Digit3":case "Digit4":case "Digit5":case "Numpad1":case "Numpad2":case "Numpad3":case "Numpad4":case "Numpad5":setSel("repSel",c.slice(-1),"반복");break;
  case "Minus":case "NumpadSubtract":stepRate(-1);break;
  case "Equal":case "NumpadAdd":stepRate(1);break;
  case "Enter":case "NumpadEnter":if(P.active)holdToggle();else done=false;break;
  case "KeyQ":case "KeyW":case "KeyE":{const m=MODES["QWE".indexOf(c.slice(-1))];const b=document.querySelector(`[data-mode="${m}"]`);if(b){b.click();toast(b.textContent.trim())}else done=false;break}
  default:done=false}
  if(done)e.preventDefault()});
const st=document.createElement("style");st.textContent=`#kbToast{position:fixed;left:50%;top:18px;transform:translateX(-50%);background:var(--ink,#222);color:var(--sheet,#fff);padding:6px 14px;border-radius:999px;font-size:14px;opacity:0;pointer-events:none;transition:opacity .2s;z-index:60}#kbToast.on{opacity:.92}
#kbHelp{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;z-index:70;padding:16px}
#kbHelp .kbbox{background:var(--sheet,#fff);color:var(--ink,#222);border-radius:16px;padding:16px 20px;max-width:420px;width:100%;box-shadow:0 8px 30px rgba(0,0,0,.25);font-size:14.5px}
#kbHelp h3{margin:0 0 10px;font-size:17px}#kbHelp table{width:100%;border-collapse:collapse}#kbHelp th{text-align:left;white-space:nowrap;padding:4px 12px 4px 0;vertical-align:top}#kbHelp td{padding:4px 0}
#kbHelp kbd{display:inline-block;border:1px solid var(--line,#ccc);border-bottom-width:2px;border-radius:6px;padding:0 6px;font:inherit;font-size:13px;background:var(--bg,#f4f4f4)}
#kbHelp p{color:var(--muted,#777);font-size:13px;margin:10px 0}#kbHelp button{border:1.5px solid var(--accent,#1C6FA8);background:none;color:var(--accent,#1C6FA8);border-radius:999px;padding:4px 16px;font:inherit;cursor:pointer}`;
document.head.appendChild(st);
})();
