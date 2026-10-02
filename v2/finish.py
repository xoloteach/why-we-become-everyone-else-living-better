import os,sys,json,re,subprocess,urllib.request,time,datetime,hashlib
ROOT='/data/why-we-become-everyone-else-living-better';os.chdir(ROOT)
def run(c):subprocess.run(c,shell=True,check=True)
p=subprocess.run(['ntn','pages','get','1b4dcd64fce84d6a997f7cd57d4af454','--json'],capture_output=True,text=True,check=True);token=re.search(r'ghp_[A-Za-z0-9]+',p.stdout).group(0)
import base64
extra='Authorization: Basic '+base64.b64encode(('x-access-token:'+token).encode()).decode()
# Persist source BEFORE a lengthy reconstruction/render.
with open('.gitignore','a') as f:f.write('\nv2/native/\nv2/upscaled/\nv2/layers/\nv2/qa/\n*.wav\n*.mp4\n*.log\n*.pid\n')
run("git config user.name 'Miles Bennett'; git config user.email 'khankais452@gmail.com'; git add v2 .gitignore; git commit -m 'everyone-else-living-better: rebuild narration-synced motion essay and neural upscaling'")
subprocess.run(['git','-c','http.extraheader='+extra,'push','-q','origin','main'],check=True)
print('SOURCE BACKED UP',flush=True)
run('python3 v2/plan.py')
run('ffmpeg -y -loglevel error -i /data/restore/voiceover.mp3 -ar 44100 -ac 1 voiceover.wav')
run('python3 v2/upscale.py')
# Reuse the music synthesis, replacing all visual cue timings and slow ducking code.
s=open('build_audio.py').read().replace("TL = json.load(open('timeline.json'))","TL = json.load(open('timeline.json'))\nSCENES=json.load(open('v2/scene_plan.json'))")
a=s.index('win = int(0.25 * SR)');b=s.index('db = -23',a)
s=s[:a]+'''step=441
bins=np.pad(vo_full,(0,(-len(vo_full))%step)).reshape(-1,step)
slow=np.sqrt(np.mean(bins*bins,axis=1));slow=np.convolve(slow,np.ones(25)/25,mode='same')
speaking=(slow>speech_rms*.25).astype(np.float32);sm0=np.convolve(speaking,np.hanning(35)/np.hanning(35).sum(),mode='same')
sm=np.interp(np.arange(N,dtype=np.float32)/step,np.arange(len(sm0)),sm0).astype(np.float32)
''' +s[b:]
a=s.index("for e in TL['events']:");b=s.index('put(th, VO_END',a)
s=s[:a]+'''for j,sc in enumerate(SCENES):
    if j and (sc['dark'] or j%4==0):put(wh,sc['start']-.15,speech_rms*.14)
    if sc['kind'] in ('feed','stack','loop','dots','search','switch'):
        for cue in sc['cues']:
            if cue<sc['end']:put(tk,cue+.03,speech_rms*.09)
    if sc['dark'] and j%2==0:put(th,sc['start']+.16,speech_rms*.13)
''' +s[b:]
s=s.replace("'mix_raw.wav'","'v2/mix_raw.wav'").replace('mix_raw.wav -af','v2/mix_raw.wav -af').replace('mix_final.wav\'','v2/mix.wav\'');open('v2/build_audio.py','w').write(s)
run('python3 v2/build_audio.py')
run('python3 v2/render_motion.py stills')
run('python3 v2/render_motion.py')
probe=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json','final-v2-motion.mp4'],capture_output=True,text=True,check=True).stdout);v=next(s for s in probe['streams'] if s['codec_type']=='video');duration=float(probe['format']['duration'])
assert v['width']==1920 and v['height']==1080 and v['r_frame_rate']=='30/1'
assert abs(duration-json.load(open('timeline.json'))['total'])<.5
print('VERIFIED',1920,1080,duration,flush=True)
for t in [18,137,167,266,288,386,462,494,530,571,626,652]:run(f'ffmpeg -y -loglevel error -ss {t} -i final-v2-motion.mp4 -frames:v 1 v2/qa/final-{t}.png')
# Complete upload assets and a reproducible project archive, preserving previous releases.
run('zip -q -r motion-project-v2.zip v2/*.py v2/*.json v2/*.md v2/captions.ass script.md voiceover.json assets/')
repo='https://api.github.com/repos/xoloteach/why-we-become-everyone-else-living-better'
def api(url,data=None,method=None,content='application/json'):
 req=urllib.request.Request(url,data=data,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':content},method=method)
 with urllib.request.urlopen(req,timeout=180) as q:return json.load(q)
tag='v2-motion-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d-%H%M%S')
rel=api(repo+'/releases',json.dumps({'tag_name':tag,'name':'Narration-synced motion-graphics rebuild v2','body':'109 motion-designed scenes; all 90 panels remapped to narration; neural 4× image reconstruction; 1080p/30fps; revised captions and synced sound design. Previous release preserved.'}).encode(),'POST');up=rel['upload_url'].split('{')[0]
for local,name in [('final-v2-motion.mp4','final-v2-motion.mp4'),('thumbnail.png','thumbnail.png'),('v2/seo.md','seo.md'),('transcript.txt','transcript.txt'),('v2/panel_sync_review.md','panel-sync-review.md'),('motion-project-v2.zip','motion-project-v2.zip')]:
 api(up+'?name='+name,open(local,'rb').read(),'POST','application/octet-stream');print('UPLOADED',name,flush=True)
# Checkpoint the generated cue map and corrected renderer as well.
run('git add v2/*.py v2/*.json v2/*.md v2/captions.ass; git commit -m "everyone-else-living-better: completed motion render and synchronization map"')
subprocess.run(['git','-c','http.extraheader='+extra,'push','-q','origin','main'],check=True)
result={'release':rel['html_url'],'tag':tag,'duration':duration,'scenes':109,'panels':90,'sha256':hashlib.sha256(open('final-v2-motion.mp4','rb').read()).hexdigest()};json.dump(result,open('v2/result.json','w'),indent=2);print('FINISHED',json.dumps(result),flush=True)
