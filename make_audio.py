import json, os, re, subprocess, requests, sys
os.chdir('/data/why-we-become-everyone-else-living-better')
for l in open('.env'):
    k, _, v = l.strip().partition('=')
    if k: os.environ[k] = v
KEY = os.environ['DEEPGRAM_API_KEY']
H = {'Authorization': f'Token {KEY}'}
paras = json.load(open('paras.json'))
# split into chunks <= 900 chars on sentence boundaries
chunks = []
for p in paras:
    cur = ''
    for s in re.split(r'(?<=[.?!”])\s+', p):
        if len(cur) + len(s) + 1 > 900 and cur:
            chunks.append(cur); cur = s
        else:
            cur = (cur + ' ' + s).strip()
    if cur: chunks.append(cur)
print('chunks', len(chunks), flush=True)
os.makedirs('audio', exist_ok=True)
files = []
for i, c in enumerate(chunks):
    out = f'audio/part{i:02d}.mp3'
    if not os.path.exists(out) or os.path.getsize(out) < 2000:
        for attempt in range(3):
            r = requests.post('https://api.deepgram.com/v2/speak?model=flux-cole-en&encoding=mp3', headers={**H, 'Content-Type': 'application/json'}, json={'text': c}, timeout=120)
            if r.status_code == 200 and len(r.content) > 2000:
                open(out, 'wb').write(r.content); break
            print('retry', i, r.status_code, r.text[:200], flush=True)
        else:
            sys.exit('TTS failed at chunk %d' % i)
    files.append(out)
    print('ok', i, flush=True)
open('audio/list.txt', 'w').write(''.join(f"file '{os.path.basename(f)}'\n" for f in files))
subprocess.run('ffmpeg -y -loglevel error -f concat -safe 0 -i audio/list.txt -c copy audio/raw.mp3', shell=True, check=True)
chain = 'highpass=f=80,equalizer=f=220:width_type=o:width=1.2:g=2.5,equalizer=f=3500:width_type=o:width=1.5:g=-2.2,equalizer=f=10000:width_type=o:width=1.0:g=1.8,acompressor=threshold=0.12:ratio=3.2:attack=15:release=220,silenceremove=stop_periods=-1:stop_duration=0.4:stop_threshold=-45dB,loudnorm=I=-16:LRA=11:TP=-1.0'
subprocess.run(f'ffmpeg -y -loglevel error -i audio/raw.mp3 -af "{chain}" -ar 44100 voiceover.wav', shell=True, check=True)
subprocess.run('ffmpeg -y -loglevel error -i voiceover.wav -b:a 192k voiceover.mp3', shell=True, check=True)
print('mastered', flush=True)
r = requests.post('https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true&punctuate=true&utterances=true', headers={**H, 'Content-Type': 'audio/mpeg'}, data=open('voiceover.mp3', 'rb').read(), timeout=600)
print('stt', r.status_code, flush=True)
r.raise_for_status()
j = r.json()
json.dump(j, open('voiceover_full.json', 'w'))
words = j['results']['channels'][0]['alternatives'][0]['words']
json.dump(words, open('voiceover.json', 'w'), indent=1)
print('words', len(words), 'end', words[-1]['end'], flush=True)
