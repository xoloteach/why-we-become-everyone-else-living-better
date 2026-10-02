import cv2, numpy as np, os, glob, json
os.chdir('/data/why-we-become-everyone-else-living-better')
files = sorted(glob.glob('sheets_raw/*.png'))
idx2sheet = {1:1, 5:2, 3:3, 6:4, 10:5, 9:6, 2:7, 8:8, 4:9, 7:10}
os.makedirs('frames', exist_ok=True)

def find_lines(profile, size):
    res = [0]
    for k in (1, 2):
        c = int(size * k / 3); w = int(size * 0.06)
        lo, hi = max(c - w, 0), min(c + w, size)
        res.append(lo + int(np.argmin(profile[lo:hi])))
    res.append(size)
    return res

for i, f in enumerate(files, 1):
    sh = idx2sheet[i]
    img = cv2.imread(f)
    h, w = img.shape[:2]
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float)
    xs = find_lines(g.mean(axis=0), w); ys = find_lines(g.mean(axis=1), h)
    inset = 6
    n = 0
    for r in range(3):
        for c in range(3):
            n += 1
            x0 = xs[c] + (inset if c > 0 else 8); x1 = xs[c+1] - (inset if c < 2 else 8)
            y0 = ys[r] + (inset if r > 0 else 8); y1 = ys[r+1] - (inset if r < 2 else 8)
            crop = img[y0:y1, x0:x1]
            ch, cw = crop.shape[:2]
            tw = int(ch * 16 / 9)
            if tw <= cw:
                o = (cw - tw) // 2; crop = crop[:, o:o+tw]
            else:
                th = int(cw * 9 / 16); o = (ch - th) // 2; crop = crop[o:o+th]
            up = cv2.resize(crop, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
            blur = cv2.GaussianBlur(up, (0, 0), 1.6)
            up = cv2.addWeighted(up, 1.5, blur, -0.5, 0)
            cv2.imwrite(f'frames/s{sh:02d}_p{n}.png', up)
print('ok')
