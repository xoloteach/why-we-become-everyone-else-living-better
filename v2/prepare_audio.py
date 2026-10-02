import os
os.chdir('/data/why-we-become-everyone-else-living-better')
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
