# v1.8: break up 짝말비교 '동사짝·예절' (content c206, P4-F): opposites -> P4-A, verb forms -> P2-C (before 총정리), greetings/polite -> P5-K. Run once.
import re, glob, os
C = '/home/user/sw/src/content/'
M = {'2-06-01': '2-05-12', '2-06-02': '2-05-13', '2-06-03': '4-03-06', '2-06-04': '4-03-07', '2-06-05': '4-03-08', '4-03-06': '4-03-09', '2-06-06': '1-01-08', '2-06-07': '1-01-09'}
src = open(C + 'c206.txt').read()
blocks = {}
for part in re.split(r'\n(?=@ )', src)[1:]:
    blocks[part[2:9]] = part.rstrip('\n') + '\n'
assert len(blocks) == 7, blocks.keys()
def ren(s): return re.sub(r'\b(\d-\d\d-\d\d)\b', lambda m: M.get(m.group(1), m.group(1)), s)
def add(f, ids, before=None):
    s = open(C + f).read()
    new = '\n'.join(blocks[i] for i in ids)
    if before:
        k = s.index('@ ' + before); s = s[:k] + new + '\n' + s[k:]
    else:
        s = s.rstrip('\n') + '\n\n' + new
    open(C + f, 'w').write(s)
add('c205.txt', ['2-06-01', '2-06-02'])
add('c402.txt', ['2-06-03', '2-06-04', '2-06-05'], before='4-03-06')
add('c101.txt', ['2-06-06', '2-06-07'])
os.remove(C + 'c206.txt')
for f in glob.glob(C + 'c*.txt'):
    s = open(f).read(); t = ren(s)
    if t != s: open(f, 'w').write(t)
print('moved')
