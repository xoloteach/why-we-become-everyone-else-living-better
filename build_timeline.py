import json, re, os, difflib, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
os.chdir('/data/why-we-become-everyone-else-living-better')
FD = '/data/fonts/'
def F(w, s): return ImageFont.truetype(FD + f'Montserrat-{w}.ttf', s)

words = json.load(open('voiceover.json'))
VO_END = words[-1]['end']
END_CARD = 5.0
TOTAL = VO_END + END_CARD

# ---------- parse script ----------
items = []  # ('say', text) or ('tag', kind, arg)
for raw in open('script.md', encoding='utf-8').read().split('\n'):
    l = raw.strip()
    if not l or l.startswith('# '): continue
    m = re.match(r'^\[([A-Z]+)(?:[:\s]\s*(.*))?\]$', l)
    if m: items.append(('tag', m.group(1), (m.group(2) or '').strip()))
    else: items.append(('say', l))
norm = lambda t: re.findall(r'[a-z0-9]+', t.lower().replace("'", '').replace('\u2019', ''))
say = [(i, it[1]) for i, it in enumerate(items) if it[0] == 'say']
stoks, tline = [], []
for k, (i, t) in enumerate(say):
    for tk in norm(t): stoks.append(tk); tline.append(k)
wtoks = [(norm(w.get('punctuated_word') or w['word']) or [''])[0] for w in words]
sm = difflib.SequenceMatcher(None, stoks, wtoks, autojunk=False)
mi, mt = [], []
for a, b, n in sm.get_matching_blocks():
    for d in range(n): mi.append(a + d); mt.append(words[b + d]['start'])
print('matched', len(mi), 'of', len(stoks), flush=True)
tok_time = np.interp(np.arange(len(stoks)), mi, mt)
line_start = {}
for idx, k in enumerate(tline):
    line_start.setdefault(k, float(tok_time[idx]))
line_start[0] = 0.0
# map item index -> time of next say line
say_idx = {i: k for k, (i, _) in enumerate(say)}
def time_of_item(i):
    for j in range(i, len(items)):
        if j in say_idx: return line_start[say_idx[j]]
    return VO_END

# ---------- sheets / panels ----------
sheet_marks = [(int(it[2]), time_of_item(i)) for i, it in enumerate(items) if it[0] == 'tag' and it[1] == 'SHEET']
sheet_marks[0] = (sheet_marks[0][0], 0.0)
panels = []
for si, (sh, ts) in enumerate(sheet_marks):
    te = sheet_marks[si + 1][1] if si + 1 < len(sheet_marks) else VO_END
    starts = sorted(set(round(v, 3) for v in line_start.values() if ts < v < te - 1.0))
    bps = [ts]
    for k in range(1, 9):
        tgt = ts + k * (te - ts) / 9
        cand = [s for s in starts if s > bps[-1] + 2.0 and abs(s - tgt) < (te - ts) / 9 * 0.6]
        bps.append(min(cand, key=lambda s: abs(s - tgt)) if cand else max(tgt, bps[-1] + 2.0))
    bps.append(te)
    for p in range(9):
        panels.append({'sheet': sh, 'panel': p + 1, 'start': bps[p], 'end': bps[p + 1], 'img': f'frames/s{sh:02d}_p{p+1}.png'})
panels[-1]['end'] = VO_END
print('panels', len(panels), 'min dur', min(p['end'] - p['start'] for p in panels), flush=True)

# ---------- overlay renderers ----------
GOLD = (232, 179, 58); OBS = (22, 21, 15); RUST = (200, 98, 60); PAPER = (247, 244, 238)
def wrap(draw, text, font, maxw):
    out, cur = [], ''
    for w in text.split():
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: out.append(cur); cur = w
    if cur: out.append(cur)
    return out
def glow_card(w, h, pad=30):
    W, H = w + pad * 2, h + pad * 2
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(g).rounded_rectangle([pad, pad, pad + w, pad + h], 28, outline=GOLD + (200,), width=6)
    g = g.filter(ImageFilter.GaussianBlur(14))
    d = ImageDraw.Draw(g)
    d.rounded_rectangle([pad, pad, pad + w, pad + h], 28, fill=OBS + (240,), outline=GOLD + (230,), width=3)
    return g, pad
def spaced(d, xy, text, font, fill, sp=4):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += d.textlength(ch, font=font) + sp
def info_card(header, main, sub=None, width=1000):
    tmp = ImageDraw.Draw(Image.new('RGBA', (10, 10)))
    fm, fs = F('ExtraBold', 62), F('Bold', 34)
    ml = wrap(tmp, main, fm, width - 100)
    sl = wrap(tmp, sub, fs, width - 100) if sub else []
    h = 40 + 38 + 20 + len(ml) * 78 + (30 + len(sl) * 46 if sl else 0) + 40
    g, pad = glow_card(width, h)
    d = ImageDraw.Draw(g)
    y = pad + 40
    spaced(d, (pad + 50, y), header.upper(), F('Black', 28), GOLD); y += 38 + 20
    for t in ml: d.text((pad + 50, y), t, font=fm, fill=(255, 255, 255)); y += 78
    if sl:
        d.rectangle([pad + 50, y + 8, pad + 50 + 120, y + 12], fill=RUST); y += 30
        for t in sl: d.text((pad + 50, y), t, font=fs, fill=(200, 196, 186)); y += 46
    return g
def node_box(d, cx, cy, text, w=470, h=130, fill=(40, 38, 28), ol=GOLD):
    d.rounded_rectangle([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], 22, fill=fill + (255,), outline=ol + (255,), width=3)
    f = F('ExtraBold', 32); ls = wrap(d, text, f, w - 40)
    y = cy - len(ls) * 21; 
    for t in ls:
        d.text((cx - d.textlength(t, font=f) / 2, y), t, font=f, fill=(255, 255, 255)); y += 42
def arrow(d, a, b, col=RUST, wd=8):
    d.line([a, b], fill=col + (255,), width=wd)
    ang = math.atan2(b[1] - a[1], b[0] - a[0]); L = 28
    p1 = (b[0] - L * math.cos(ang - .45), b[1] - L * math.sin(ang - .45))
    p2 = (b[0] - L * math.cos(ang + .45), b[1] - L * math.sin(ang + .45))
    d.polygon([b, p1, p2], fill=col + (255,))
def loop_card(parts):
    nodes = [p.strip() for p in parts.split('>')]
    w, h = 1300, 560
    g, pad = glow_card(w, h); d = ImageDraw.Draw(g)
    spaced(d, (pad + 50, pad + 36), 'THE LOOP', F('Black', 28), GOLD)
    cx0, cy0 = pad + w // 2, pad + h // 2 + 30
    pos = [(cx0 - 330, cy0 - 110), (cx0 + 330, cy0 - 110), (cx0 + 330, cy0 + 130), (cx0 - 330, cy0 + 130)][:len(nodes)]
    if len(nodes) != 4: pos = [(pad + 140 + i * (w - 280) // max(1, len(nodes) - 1), cy0) for i in range(len(nodes))]
    if len(nodes) == 4:
        arrow(d, (pos[0][0] + 240, pos[0][1]), (pos[1][0] - 245, pos[1][1]))
        arrow(d, (pos[1][0], pos[1][1] + 66), (pos[2][0], pos[2][1] - 70))
        arrow(d, (pos[2][0] - 240, pos[2][1]), (pos[3][0] + 245, pos[3][1]))
        arrow(d, (pos[3][0], pos[3][1] - 66), (pos[0][0], pos[0][1] + 70))
    for (x, y), t in zip(pos, nodes): node_box(d, x, y, t)
    return g
def split_card(a, b):
    w, h = 1500, 400
    g, pad = glow_card(w, h); d = ImageDraw.Draw(g)
    mid = pad + w // 2
    d.line([(mid, pad + 40), (mid, pad + h - 40)], fill=RUST + (255,), width=5)
    for k, t in enumerate([a, b]):
        x0 = pad + 50 + k * (w // 2)
        head, _, val = t.partition(':')
        spaced(d, (x0, pad + 50), head.strip().upper(), F('Black', 26), GOLD if k == 0 else RUST)
        f = F('ExtraBold', 58); y = pad + 120
        for l in wrap(d, val.strip(), f, w // 2 - 110): d.text((x0, y), l, font=f, fill=(255, 255, 255)); y += 72
    return g
def arrow_card(parts):
    n = [p.strip() for p in parts.split('>')]
    w, h = 1300, 260
    g, pad = glow_card(w, h); d = ImageDraw.Draw(g)
    y = pad + h // 2
    node_box(d, pad + 330, y, n[0], 520, 150); node_box(d, pad + w - 330, y, n[1], 520, 150, ol=RUST)
    arrow(d, (pad + w // 2 - 100, y), (pad + w // 2 + 100, y), RUST, 10)
    return g
def banner_img(num, title):
    W, H = 1920, 270
    g = Image.new('RGBA', (W, H), PAPER + (246,)); d = ImageDraw.Draw(g)
    d.rectangle([0, 0, W, 6], fill=RUST + (255,)); d.rectangle([0, H - 6, W, H], fill=RUST + (255,))
    spaced(d, (150, 38), f'CHAPTER {num}', F('ExtraBold', 34), RUST, 8)
    f = F('Black', 104); d.text((150, 88), title, font=f, fill=(24, 22, 16))
    d.rectangle([150, 218, 150 + 420, 226], fill=RUST + (255,))
    return g

os.makedirs('overlays', exist_ok=True)
events = []
DUR = {'CHAPTER': 3.6, 'TERM': 5.0, 'STAT': 4.8, 'CHART': 6.5, 'ARROW': 5.0}
side = 0
for i, it in enumerate(items):
    if it[0] != 'tag' or it[1] in ('SHEET',): continue
    kind, arg = it[1], it[2]; t0 = time_of_item(i)
    if kind == 'CHAPTER' and t0 < 0.5: t0 = 0.5
    segs = [s.strip() for s in arg.split(' | ')]
    wipe = False
    if kind == 'CHAPTER': img = banner_img(segs[0], segs[1]); pos = 'center'
    elif kind == 'TERM': img = info_card('Key term', segs[0], segs[1] if len(segs) > 1 else None); pos = 'left' if side % 2 == 0 else 'right'; side += 1
    elif kind == 'STAT': img = info_card(segs[0], segs[1] if len(segs) > 1 else '', None, 1000); pos = 'left' if side % 2 == 0 else 'right'; side += 1
    elif kind == 'CHART':
        if segs[0] == 'Loop': img = loop_card(segs[1]); wipe = True
        else: img = split_card(segs[1], segs[2]); wipe = True
        pos = 'top'
    elif kind == 'ARROW': img = arrow_card(segs[0]); pos = 'top'; wipe = True
    else: continue
    fn = f'overlays/ev{len(events):02d}.png'; img.save(fn)
    events.append({'kind': kind, 'start': t0, 'dur': DUR[kind], 'img': fn, 'pos': pos, 'wipe': wipe, 'w': img.size[0], 'h': img.size[1]})
chs=[e['start'] for e in events if e['kind']=='CHAPTER']
for e in events:
    if e['kind']!='CHAPTER' and any(0<=e['start']-c<3.8 for c in chs): e['start']=max(c for c in chs if 0<=e['start']-c<3.8)+3.9
events.sort(key=lambda e: e['start'])
for a, b in zip(events, events[1:]):
    if a['start'] + a['dur'] > b['start'] - 0.2: a['dur'] = max(2.0, b['start'] - 0.2 - a['start'])

# ---------- subtitles (ASS) ----------
def ts(t):
    t = max(t, 0); cs = int(round(t * 100)); h, r = divmod(cs, 360000); m, r = divmod(r, 6000); s, c = divmod(r, 100)
    return f'{h}:{m:02d}:{s:02d}.{c:02d}'
groups, cur = [], []
for w in words:
    cur.append(w); pw = (w.get('punctuated_word') or w['word'])
    chars = sum(len(x.get('punctuated_word') or x['word']) + 1 for x in cur)
    if re.search(r'[.?!\u201d]$', pw) or (pw.endswith(',') and len(cur) >= 3) or chars > 26 or len(cur) >= 6:
        groups.append(cur); cur = []
if cur: groups.append(cur)
hdr = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Montserrat ExtraBold,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5.5,2,2,100,100,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
lines = [hdr]
for gi, g in enumerate(groups):
    texts = [(x.get('punctuated_word') or x['word']).replace('{', '').replace('}', '') for x in g]
    nxt = groups[gi + 1][0]['start'] if gi + 1 < len(groups) else VO_END
    for k, x in enumerate(g):
        s = x['start']; e = g[k + 1]['start'] if k + 1 < len(g) else min(nxt, x['end'] + 0.3)
        if e <= s: e = s + 0.05
        parts = [('{\\c&H003C62C8&}' + t + '{\\c&H00FFFFFF&}') if j == k else t for j, t in enumerate(texts)]
        lines.append(f'Dialogue: 0,{ts(s)},{ts(e)},Default,,0,0,0,,{" ".join(parts)}')
open('subs.ass', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

json.dump({'vo_end': VO_END, 'total': TOTAL, 'panels': panels, 'events': events}, open('timeline.json', 'w'), indent=1)
for e in events: print(e['kind'], round(e['start'], 1), e['pos'])
print('groups', len(groups), 'total', TOTAL)
