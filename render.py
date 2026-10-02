import json, os, sys, subprocess, bisect, time
import numpy as np, cv2
os.chdir('/data/why-we-become-everyone-else-living-better')
TL = json.load(open('timeline.json'))
FPS, W, H = 30, 1920, 1080
TOTAL, VO_END = TL['total'], TL['vo_end']
t_start = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
t_end = float(sys.argv[2]) if len(sys.argv) > 2 else TOTAL
OUT = sys.argv[3] if len(sys.argv) > 3 else 'final.mp4'
test = len(sys.argv) > 1
panels = TL['panels']; starts = [p['start'] for p in panels]
XF = 0.45
def ss(x): x = min(max(x, 0.0), 1.0); return x * x * (3 - 2 * x)
_cache = {}
def img(path):
    if path not in _cache:
        if len(_cache) > 4: _cache.pop(next(iter(_cache)))
        _cache[path] = cv2.imread(path)
    return _cache[path]
end_card = cv2.resize(cv2.imread('assets/subscribe-end-card.jpeg'), (W, H), interpolation=cv2.INTER_AREA if False else cv2.INTER_LANCZOS4)

def cam(idx, p):
    d = 1 if idx % 2 == 0 else -1
    kf = [(0.0, 1.06, -0.8 * d, -0.2), (0.54, 1.15, 0.8 * d, 0.2), (0.60, 1.22, 0.7 * d, 0.2), (1.0, 1.11, -0.8 * d, -0.2)]
    p = min(max(p, 0), 1)
    for a, b in zip(kf, kf[1:]):
        if p <= b[0]:
            u = ss((p - a[0]) / (b[0] - a[0])); s = a[1] + (b[1] - a[1]) * u
            fx = a[2] + (b[2] - a[2]) * u; fy = a[3] + (b[3] - a[3]) * u
            return s, fx * (s - 1) * W / 2, fy * (s - 1) * H / 2
    s, fx, fy = kf[-1][1:]; return s, fx * (s - 1) * W / 2, fy * (s - 1) * H / 2
def panel_frame(idx, t):
    pn = panels[idx]; D = max(pn['end'] - pn['start'], 0.1)
    s, px, py = cam(idx, (t - pn['start']) / D)
    M = np.array([[s, 0, (1 - s) * W / 2 + px], [0, s, (1 - s) * H / 2 + py]], np.float32)
    return cv2.warpAffine(img(pn['img']), M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

evs = []
for e in TL['events']:
    im = cv2.imread(e['img'], cv2.IMREAD_UNCHANGED).astype(np.float32)
    rgb = im[:, :, :3]; a = im[:, :, 3:4] / 255.0
    h, w = im.shape[:2]
    if e['pos'] == 'center': x, y = 0, 330
    elif e['pos'] == 'left': x, y = 60, 90
    elif e['pos'] == 'right': x, y = W - w - 60, 90
    else: x, y = (W - w) // 2, 60
    evs.append({**e, 'rgb': rgb, 'a': a, 'x': x, 'y': y, 'h': h, 'w': w})

def overlay(frame, t):
    for e in evs:
        r = t - e['start']
        if r < 0 or r > e['dur']: continue
        fi = ss(r / 0.5); fo = ss((e['dur'] - r) / 0.45); al = min(fi, fo)
        if al <= 0: continue
        y0 = int(e['y'] + (1 - fi) * 36); x0 = e['x']; h, w = e['h'], e['w']
        yy0, yy1 = max(y0, 0), min(y0 + h, H); xx0, xx1 = max(x0, 0), min(x0 + w, W)
        if yy1 <= yy0 or xx1 <= xx0: continue
        a = e['a'][yy0 - y0:yy1 - y0, xx0 - x0:xx1 - x0] * al
        rgb = e['rgb'][yy0 - y0:yy1 - y0, xx0 - x0:xx1 - x0]
        if e['wipe']:
            prog = ss(r / 1.0); cols = int(rgb.shape[1] * prog)
            m = np.zeros((1, rgb.shape[1], 1), np.float32); m[:, :cols] = 1; a = a * m
        reg = frame[yy0:yy1, xx0:xx1].astype(np.float32)
        frame[yy0:yy1, xx0:xx1] = (reg * (1 - a) + rgb * a).astype(np.uint8)
    return frame

def make(t):
    if t >= VO_END:
        last = panel_frame(len(panels) - 1, VO_END)
        k = ss((t - VO_END) / 0.7)
        return cv2.addWeighted(last, 1 - k, end_card, k, 0)
    idx = max(bisect.bisect_right(starts, t) - 1, 0)
    f = panel_frame(idx, t)
    if idx > 0 and t - panels[idx]['start'] < XF:
        k = ss((t - panels[idx]['start']) / XF)
        f = cv2.addWeighted(panel_frame(idx - 1, t), 1 - k, f, k, 0)
    return overlay(f, t)

vf = 'ass=subs.ass:fontsdir=/data/fonts'
if test: vf = f'setpts=PTS+{t_start}/TB,{vf},setpts=PTS-STARTPTS'
cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-']
if not test: cmd += ['-i', 'mix_final.wav']
cmd += ['-vf', vf, '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', str(FPS)]
if not test: cmd += ['-c:a', 'aac', '-b:a', '192k', '-shortest']
cmd += ['-movflags', '+faststart', OUT]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
n0, n1 = int(t_start * FPS), int(min(t_end, TOTAL) * FPS)
t0 = time.time()
for n in range(n0, n1):
    pr.stdin.write(make(n / FPS).tobytes())
    if (n - n0) % 300 == 0: print(f'{n - n0}/{n1 - n0} {time.time() - t0:.0f}s', flush=True)
pr.stdin.close(); pr.wait()
print('rendered', OUT, time.time() - t0, flush=True)
