"""Swahili -> Korean reading (한글 독음). Swahili spelling is regular, so the reading is rule-based.
Rules: a e i o u = 아 에 이 오 우 (each vowel its own syllable: saa 사아, chai 차이);
ch = ㅊ, j = ㅈ, sh = ㅅ+y (sha 샤), ny = 냐 녜 니 뇨 뉴, ng' = ㅇ (ng'ombe 응옴베), ng = 응+ㄱ (ngoma 응고마),
th = ㅅ (thelathini 셀라시니), dh = ㄷ (dhahabu 다하부), gh = ㄱ (ghali 갈리), kh = ㅎ,
k = ㅋ, t = ㅌ, p = ㅍ, f = ㅍ, v = ㅂ, b = ㅂ, d = ㄷ, g = ㄱ, z = ㅈ, s = ㅅ, h = ㅎ, r = ㄹ,
l = ㄹ (ㄹㄹ after a vowel: kula 쿨라, so l and r look different: kura 쿠라);
consonant + w = one syllable (kwa 콰, mwa 뫄, bwa 봐); consonant + y = 야 계열 (mya 먀);
m/n before a consonant = 받침 (kumbe 쿰베, kanga 캉가), or 음/은/응 at the start (mtu 음투, nchi 은치, ndizi 은디지)."""
import re
CH={'b':7,'c':14,'d':3,'f':17,'g':0,'h':18,'j':12,'k':15,'l':5,'m':6,'n':2,'p':17,'r':5,'s':9,'t':16,'v':7,'z':12,'':11}
V={'a':0,'e':5,'i':20,'o':8,'u':13}
VY={'a':2,'e':7,'i':20,'o':12,'u':17}
VW={'a':9,'e':15,'i':16,'o':14,'u':13}
FIN={'n':4,'l':8,'m':16,'ng':21}
ONS=["ng'",'ch','sh','ny','th','dh','gh','kh','b','c','d','f','g','h','j','k','l','m','n','p','r','s','t','v','z']
MAP={"ng'":'',"ch":'c','sh':'s','ny':'n','th':'s','dh':'d','gh':'g','kh':'h'}
PAL={'sh','ny'}
def syl(i,v,f=0): return [i,v,f]
def word(w):
    w=w.lower().replace("’","'").replace('-','')
    w=re.sub(r"[^a-z']",'',w)
    S=[];i=0;n=len(w)
    def coda(c):
        k={'b':'m','p':'m','f':'m','v':'m','m':'m','k':'ng','g':'ng'}.get(c,'n')
        if S and S[-1][2]==0: S[-1][2]=FIN[k]
        else: S.append(syl(11,18,FIN[k]))   # 은/음/응
    while i<n:
        ch=w[i]
        if w.startswith("ng'",i):
            # ng' = velar nasal: 받침 ㅇ on the last syllable, or 응 at the start; next vowel starts with ㅇ
            if S and S[-1][2]==0: S[-1][2]=FIN['ng']
            else: S.append(syl(11,18,FIN['ng']))
            i+=3;continue
        if ch=="'": i+=1;continue
        # nasal before a consonant (not ny/ng', not a vowel, not a y/w glide on the nasal itself)
        if ch in 'nm' and i+1<n and w[i+1] not in "aeiouyw'" and not (ch=='n' and w[i+1]=='y'):
            nx=w[i+1]
            if ch=='n' and nx=='g': coda('g'); i+=1; continue
            if ch=='m':
                if S and S[-1][2]==0: S[-1][2]=FIN['m']
                else: S.append(syl(11,18,FIN['m']))
                i+=1;continue
            coda(nx); i+=1; continue
        if ch in 'aeiou':
            S.append(syl(11,V[ch]));i+=1;continue
        if ch in 'yw':
            if i+1<n and w[i+1] in 'aeiou':
                S.append(syl(11,(VY if ch=='y' else VW)[w[i+1]]));i+=2;continue
            i+=1;continue
        on=next((o for o in ONS if w.startswith(o,i)),None)
        if on is None: i+=1;continue
        base=MAP.get(on,on);j=i+len(on);gy=on in PAL;gw=False
        if j<n and w[j]=='y' and on not in PAL: gy=True;j+=1
        if j<n and w[j]=='w': gw=True;j+=1
        if j>=n or w[j] not in 'aeiou':
            # consonant with no vowel (loan words, abbreviations): 으
            nx=w[j] if j<n else ''
            if on in ('p','k') and nx and nx not in "lrwy'" and S and S[-1][2]==0 and i>0 and w[i-1] in 'aeiou':
                S[-1][2]=17 if on=='p' else 1   # Septemba 셉템바, daktari 닥타리
            elif base=='s' and on=='sh': S.append(syl(9,20))   # 시
            else: S.append(syl(CH.get(base,11),18,8 if nx=='l' else 0))   # ghafla 가플라
            i=j;continue
        v=w[j]
        if on=='l' and S and S[-1][2]==0 and i>0 and w[i-1] in 'aeiou': S[-1][2]=8
        if on=='l' and S and S[-1][2]==8 and i>0 and w[i-1] not in 'aeiou': pass
        if gw and base not in ('k','g','m'): S.append(syl(CH[base],18));S.append(syl(11,VW[v]))
        elif gw: S.append(syl(CH[base],VW[v]))
        elif gy: S.append(syl(CH[base],16 if (on=='sh' and v=='i') else VY[v]))   # shi 쉬 (si 시와 구별)
        else: S.append(syl(CH[base],V[v]))
        i=j+1
    return ''.join(chr(0xAC00+(a*21+b)*28+c) for a,b,c in S)
def reading(t):
    out=[]
    for tk in re.findall(r"[A-Za-z][A-Za-z'’\-]*|\d[\d.,:]*|[?!.,…—–:;]",t.replace("…"," … ")):
        if re.match(r"[A-Za-z]",tk): out.append(word(tk))
        elif tk in '?!.,:;':
            if out: out[-1]+=tk
        else: out.append(tk)
    return re.sub(r'\s+',' ',' '.join(out)).strip()
if __name__=='__main__':
    for x in "Jambo Habari mwalimu asante sana Kiswahili Tanzania Kenya mtu watu nchi ndizi ng'ombe ngoma nyumba chai saa kula kura thelathini dhahabu ghali shule mbwa kumbe kanga mkate mwanafunzi Dar es Salaam Mombasa Zanzibar kwenda nyama Nairobi Kilimanjaro baba papa shikamoo marahaba ugali chapati mzungu kwaheri tafadhali ninakwenda".split():
        print(x,word(x))
    print(reading("Habari za asubuhi, mwalimu?"))
