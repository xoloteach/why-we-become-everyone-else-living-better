import os,sys,json,math,subprocess,wave,bisect,re,functools
from pathlib import Path
import cv2,numpy as np
R=Path(__file__).resolve().parents[1];os.chdir(R);sys.path.insert(0,str(R/'v2'))
import render_motion as B
B.W=1080;B.H=1920;W,H=1080,1920;cv2.setNumThreads(1)
O=R/'shorts/output';O.mkdir(parents=True,exist_ok=True);(O/'qa').mkdir(exist_ok=True)
WORDS=json.load(open('voiceover.json'));P,I,RC,G,WH=B.PAPER,B.INK,B.RUST,B.GOLD,B.WHITE
CLIPS=[{'slug':'01-highlight-reel','title':"Your Feed Isn't Everyone's Life",'topic':'THE HIGHLIGHT REEL','ranges':[(159.770,201.960)]},{'slug':'02-borrowed-goals','title':'Would You Still Want It If Nobody Saw It?','topic':'BORROWED GOALS','ranges':[(323.190,344.070),(353.915,368.200),(375.480,381.595)]},{'slug':'03-behind-according-to-who','title':'Behind According to Who?','topic':'YOUR SCOREBOARD','ranges':[(494.495,538.670)]}]
PLANS=['''159.770;04-1;dots;YOUR FEED / ISN'T EVERYONE.;100 PEOPLE;162.010
164.410;04-2;dots;95 ORDINARY / DAYS.;95 ORDINARY;164.410
168.170;04-3;dots;FIVE EXCITING / MOMENTS.;5 EXCITING;168.170
170.650;04-3;feed;ONLY THE / BEST PARTS.;PROMOTION|TRAVEL|BUSINESS|ENGAGEMENT;170.650,172.465,174.705,176.465
177.985;04-4;window;THE CAMERA / CHOOSES.;100 IN THE ROOM|5 IN THE FRAME;177.985,180.225
182.625;04-5;window;WHAT WOULD / YOU THINK?;SELECTED FOOTAGE|YOUR IMPRESSION;182.625,184.305
187.185;04-6;feed;EVERYONE LOOKS / EXTRAORDINARY.;THE HIGHLIGHTS|THE IMPRESSION;187.185,188.360
190.600;04-7;split;REALITY. / A SELECTION OF IT.;WHOLE ROOM|SELECTED FIVE;190.600,193.000;dark
195.080;04-8;window;THE REST / STAYS INVISIBLE.;ONLINE HIGHLIGHTS|THE WHOLE STORY;195.080,197.160
199.080;04-9;window;WORTH SHOWING. / NOT THE WHOLE STORY.;SELECTED MOMENTS|LIFE OUTSIDE THE FRAME;199.080,199.800''','''323.190;07-4;thought;WOULD YOU / STILL WANT IT?;IF NOBODY COULD SEE IT|WOULD YOU STILL WANT IT?;323.190,325.105;dark
328.785;07-5;thought;A BETTER LIFE. / OR A BETTER LOOK?;FEELS BETTER|LOOKS BETTER;329.665,333.025
335.185;07-5;thought;NOT ALWAYS / THE SAME THING.;YOUR LIFE|THE APPEARANCE;335.185,335.185
337.105;07-1;switch;REMOVE / THE AUDIENCE.;VISIBLE|PRIVATE;337.105,338.385
340.630;07-2;counter;NO AUDIENCE. / STILL YOUR LIFE.;INSTAGRAM|FOLLOWERS|LIKES|NO ONE TO IMPRESS;340.630,341.670,342.390,343.030
353.915;07-2;thought;YOUR LIFE / IS STILL YOURS.;YOUR LIFE|NO AUDIENCE;353.915,355.275
356.875;07-9;paths;WHAT WOULD / YOU CHOOSE?;YOUR CHOICE|WHAT STILL MATTERS;356.875,359.835
361.355;07-6;thought;WHOSE GOALS / ARE THEY?;LOOK CLOSER|YOUR GOALS?;361.355,363.675
366.920;07-6;thought;BORROWED / GOALS.;WANTED BY YOU?|BORROWED FROM THEM?;366.920,366.920;dark
375.480;07-7;thought;AMBITION ISN'T / THE PROBLEM.;AMBITION|WHO DEFINES YOUR LIFE?;375.480,377.080
378.120;07-9;paths;CHOOSE / YOUR OWN LIFE.;SOMEONE ELSE'S LIFE|YOUR LIFE;378.120,378.120''','''494.495;01-6;thought;BEHIND / ACCORDING TO WHO?;ACCORDING TO WHO?|WHO SET THE RULE?;494.495,498.575;dark
498.575;10-2;paths;WHO SAID / YOU SHOULD BE THERE?;THEIR EXPECTATION|YOUR LIFE;498.575,498.575
500.815;10-2;paths;NOT THE / SAME TIMELINE.;THEIR TIMELINE|YOUR TIMELINE;500.815,500.815
503.855;07-9;paths;NOT THE / SAME SEQUENCE.;THEIR ROUTE|YOUR ROUTE;503.855,503.855
506.920;10-2;paths;MAYBE YOU'RE / NOT BEHIND.;NOT BEHIND|A DIFFERENT PATH;508.120,509.560
509.560;07-9;paths;A DIFFERENT / PATH.;YOUR OWN PATH|NOT A WRONG ONE;509.560,509.560
511.400;10-3;thought;CHANGE / THE QUESTION.;ONE BETTER QUESTION;511.400;dark
515.000;10-3;split;BETTER / THAN THEM?;BETTER THAN THEM?|BETTER THAN I WAS?;515.000,517.240
517.240;10-3;split;BETTER / THAN I WAS?;BETTER THAN THEM?|BETTER THAN I WAS?;515.000,517.240
520.885;10-3;paths;YOUR PAST SELF. / YOUR REFERENCE.;PAST YOU|PRESENT YOU;520.885,522.005
524.405;10-4;stack;REAL / PROGRESS.;LEARNED|DISCIPLINE|A HARD DECISION;524.405,525.685,527.605
529.605;10-4;stack;SMALL CHANGES. / REAL PROGRESS.;GOT BETTER|SELF-UNDERSTANDING|KEPT GOING;529.605,530.965,532.965
532.965;10-8;paths;YOU / KEPT GOING.;YOUR EFFORT|YOUR PROGRESS;532.965,532.965
535.310;10-5;thought;INVISIBLE. / STILL REAL.;NOT IMPRESSIVE ONLINE|STILL REAL;535.310,537.630;dark''']
def local(c,t):
 off=0
 for a,b in c['ranges']:
  if a-.002<=t<b-.002:return off+t-a
  off+=b-a
 return None
for c,p in zip(CLIPS,PLANS):
 c['vo']=sum(b-a for a,b in c['ranges']);c['duration']=c['vo']+2.5;c['scenes']=[]
 for row in p.splitlines():
  q=row.split(';');cues=[]
  for t in map(float,q[5].split(',')):
   z=local(c,t);cues.append(z if z is not None else (-1 if t<c['ranges'][0][0] else c['duration']+1))
  c['scenes'].append(dict(id=len(c['scenes']),start=local(c,float(q[0])),art=q[1],kind=q[2],title=q[3].replace(' / ','\n'),labels=q[4].split('|'),cues=cues,dark=len(q)>6,feature=False,layout='right',chapter=1))
 for j,s in enumerate(c['scenes']):
  s['end']=c['scenes'][j+1]['start'] if j+1<len(c['scenes']) else c['vo'];s['cues']=[s['end']+1 if t>=s['end']-.04 else t for t in s['cues']]
 assert c['duration']<50 and all(s['start']<s['end'] for s in c['scenes']);c['starts']=[s['start'] for s in c['scenes']]
grain=np.random.default_rng(321).normal(0,.5,(H,W,1));BG={False:np.clip(np.array(P)[None,None,:]+grain,0,255).astype(np.uint8),True:np.clip(np.array(I)[None,None,:]+grain*.4,0,255).astype(np.uint8)}
@functools.lru_cache(maxsize=8)
def hero(art,dark):
 a,ink,ps=B.hero(art,False,dark);h,w=a.shape[:2];sc=min(830/w,435/h);wh=(round(w*sc),round(h*sc));a=cv2.resize(a,wh,interpolation=cv2.INTER_AREA);ink=cv2.resize(ink,wh,interpolation=cv2.INTER_AREA);ps=[(cv2.resize(p,(max(1,round(p.shape[1]*sc)),wh[1]),interpolation=cv2.INTER_AREA),round(off*sc)) for p,off in ps];return a,ink,ps
def art(f,s,t):
 a,ink,ps=hero(s['art'],s['dark']);h,w=a.shape[:2];r=t-s['start'];u=min(1,max(0,r/(s['end']-s['start'])));x=495-w/2;y=742-h/2;cap=int(w*B.ease((r+.04)/.45));fill=B.ease((r-.08)/.55)
 for j,(p,off) in enumerate(ps):
  n=min(p.shape[1],cap-off)
  if n<=0:continue
  dx=(1-B.spring(r/.6))*28*(1 if s['id']%2 else -1)+(B.ease(u)-.5)*(14 if j==0 else -10);dy=(1-B.spring(max(0,r-j*.06)/.6))*(20 if j==0 else -20)+(B.ease(u)-.5)*(6 if j==0 else -6);B.blit(f,ink[:,off:off+n],x+off+dx,y+dy,1-fill);B.blit(f,p[:,:n],x+off+dx,y+dy,fill)
def dots(f,c,s,t):
 st=c['ranges'][0][0]+t;phase=5 if st>=168.17 else (95 if st>=164.41 else 100);fg=WH if s['dark'] else I;mut=(119,124,128)
 for j in range(100):
  a=B.ease((t-s['start']-j*.001)/.45);col=RC if phase==5 and j>=95 else (mut if phase!=100 else fg);cv2.circle(f,(110+j%10*27,1040+j//10*27),max(1,int(7*a)),col,1 if phase==95 and j>=95 else -1,cv2.LINE_AA)
 a=B.ease((t-max(s['start'],2.24))/.4);B.text(f,str(phase),456,1037,132,RC if phase==5 else fg,390,alpha=a,weight='Black');B.text(f,'EXCITING' if phase==5 else ('ORDINARY' if phase==95 else 'PEOPLE'),456,1212,32,fg,390,alpha=a);B.text(f,'THOUGHT EXPERIMENT',110,1322,24,mut,780)
def native_paths(f,s,t):
 x,y,w=87,1030,790;r=t-s['start'];D=s['end']-s['start'];fg=WH if s['dark'] else I;mut=(155,164,174) if s['dark'] else (114,121,127)
 for j,l in enumerate(s['labels'][:2]):
  a=B.spring((t-s['cues'][j])/.55);yy=y+85+j*144;B.text(f,l,x,yy-73,30,fg,w,alpha=a)
  ps=np.array([(x+15,yy),(x+w-20,yy)] if j==0 else [(x+15,yy),(x+150,yy),(x+300,yy-30),(x+440,yy+20),(x+610,yy),(x+w-20,yy-45)],float);B.path(f,ps,mut if j==0 else RC,4,a,True)
  if a>.8:
   lengths=np.linalg.norm(np.diff(ps,axis=0),axis=1);d=lengths.sum()*(r/max(D,1)*.65+.12)
   for k,L in enumerate(lengths):
    if d<=L:pt=ps[k]+(ps[k+1]-ps[k])*d/max(L,.001);break
    d-=L
   else:pt=ps[-1]
   cv2.circle(f,tuple(pt.astype(int)),11,RC if j else fg,-1,cv2.LINE_AA)
def scene(c,j,t):
 s=c['scenes'][j];r=t-s['start'];fg=WH if s['dark'] else I;f=BG[s['dark']].copy();B.text(f,'WHY WE BECOME',85,119,26,fg,400,weight='Black');B.text(f,c['topic'],534,124,21,RC,350);B.line(f,(85,181),(900,181),(52,61,66) if s['dark'] else (222,231,237),1);sz=86;a=B.glyph(s['title'],sz,fg,805,'Black')
 while a.shape[0]>244 and sz>62:sz-=2;a=B.glyph(s['title'],sz,fg,805,'Black')
 assert a.shape[0]<=260
 en=1 if j==0 else B.spring(r/.42);B.blit(f,a,87,225+(1-en)*17,en);B.line(f,(90,490),(230,490),RC,5,B.ease((r+.05)/.45));art(f,s,t)
 if s['kind']=='dots':dots(f,c,s,t)
 elif s['kind']=='paths':native_paths(f,s,t)
 else:B.diagram(f,s,t,87,1030,790,320)
 B.line(f,(85,1620),(900,1620),(55,62,67) if s['dark'] else (220,230,236),2);B.line(f,(85,1620),(900,1620),RC,4,t/c['duration']);B.text(f,'THINK DEEPER. LIVE BETTER.',85,1672,22,fg,810);return f
end=cv2.imread('assets/subscribe-end-card.jpeg');ew=935;eh=round(end.shape[0]*ew/end.shape[1]);end=cv2.resize(end,(ew,eh),interpolation=cv2.INTER_LANCZOS4)
def frame(c,t):
 if t>=c['vo']:
  f=BG[False].copy();B.text(f,'WHY WE BECOME',85,145,28,I,800,weight='Black');B.text(f,'THINK\nDEEPER.',85,310,100,I,815,weight='Black');x=(W-ew)//2;f[660:660+eh,x:x+ew]=end;B.text(f,'LIVE BETTER.\nBECOME MORE.',85,1265,53,I,815,weight='Black');B.line(f,(90,1508),(900,1508),RC,5,B.ease((t-c['vo']-.2)/.8));a=B.ease((t-c['vo'])/.28);return cv2.addWeighted(scene(c,len(c['scenes'])-1,c['vo']-.001),1-a,f,a,0)
 j=max(0,bisect.bisect_right(c['starts'],t)-1);f=scene(c,j,t);r=t-c['starts'][j]
 if j and r<.18:
  prev=scene(c,j-1,c['starts'][j]-.01);a=B.ease(r/.18)
  if j%3==0 and c['scenes'][j]['dark']==c['scenes'][j-1]['dark']:y=int(H*a);f[y:]=prev[y:];cv2.line(f,(0,y),(W,y),RC,3)
  else:f=cv2.addWeighted(prev,1-a,f,a,0)
 return f
def tm(t):
 v=max(0,round(t*100));h,v=divmod(v,360000);m,v=divmod(v,6000);s,v=divmod(v,100);return f'{h}:{m:02d}:{s:02d}.{v:02d}'
def captions(c):
 arr=[];off=0
 for a,b in c['ranges']:
  for w in WORDS:
   if a-.015<=w['start']<b-.025:
    z=dict(w);z['start']=max(off,off+w['start']-a);z['end']=min(off+b-a,off+w['end']-a);arr.append(z)
  off+=b-a
 json.dump(arr,open(O/(c['slug']+'-words.json'),'w'),indent=1)
 text='''[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Montserrat ExtraBold,60,&H00FFFFFF,&H003C62C8,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,1.5,2,80,200,420,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n''';groups=[];cur=[]
 for w in arr:
  if cur and (len(cur)>=5 or w['start']-cur[-1]['end']>.24):groups.append(cur);cur=[]
  cur.append(w)
  if re.search(r'[.!?]$',w.get('punctuated_word',w['word'])):groups.append(cur);cur=[]
 if cur:groups.append(cur)
 for g in groups:
  start=g[0]['start'];stop=min(c['vo'],max(start+.08,g[-1]['end']+.025));parts=[];line='';nl=1
  for w in g:
   word=w.get('punctuated_word',w['word']).replace('{','').replace('}','');z=(line+' '+word).strip()
   if B.glyph(z,60,I,2000).shape[1]>790 and line:parts.append('\\N');line=word;nl+=1
   else:line=z
   lo=max(0,round((w['start']-start)*1000));hi=max(lo+25,round((w['end']-start)*1000));parts.append('{\\1c&HFFFFFF&\\t('+str(lo)+','+str(lo+12)+',\\1c&H3C62C8&)\\t('+str(hi)+','+str(hi+12)+',\\1c&HFFFFFF&)}'+word+' ')
  assert nl<=2
  text+='Dialogue: 0,'+tm(start)+','+tm(stop)+',Default,,0,0,0,,'+''.join(parts).strip()+'\n'
 (O/(c['slug']+'.ass')).write_text(text);(O/(c['slug']+'-script.md')).write_text('# '+c['title']+'\n\n'+' '.join(w.get('punctuated_word',w['word']) for w in arr)+'\n');(O/(c['slug']+'-seo.md')).write_text('# '+c['title']+'\n\nOriginal script excerpts, supplied artwork and narration-synced motion graphics.\nThink deeper. Live better. Become more.\n\n#Shorts #Psychology #SocialComparison #SelfImprovement #WhyWeBecome\n')
def audio(c,vo,sr):
 ps=[]
 for a,b in c['ranges']:
  p=vo[round(a*sr):round(b*sr)].copy();n=min(660,len(p)//2);p[:n]*=np.linspace(0,1,n);p[-n:]*=np.linspace(1,0,n);ps.append(p)
 speech=np.concatenate(ps);N=round(c['duration']*sr);v=np.zeros(N,np.float32);v[:len(speech)]=speech;vr=float(np.sqrt(np.mean(speech**2)));t=np.arange(N,dtype=np.float32)/sr;music=np.zeros(N,np.float32)
 for j,fs in enumerate([[220,261.626,329.628],[174.614,220,261.626],[130.813,164.814,196],[196,246.942,293.665]]*3):
  a=j*5.5;b=min(c['duration'],a+7)
  if a>=c['duration']:break
  ix=(t>=a)&(t<b);x=t[ix]-a;en=np.minimum(1,x/.75)*np.minimum(1,(b-t[ix])/.9)
  for f in fs:music[ix]+=en*(np.sin(2*np.pi*f*x)+.18*np.sin(2*np.pi*f*2*x))*.2
 st=round(sr/100);bins=np.pad(v,(0,(-N)%st)).reshape(-1,st);en=np.sqrt(np.mean(bins*bins,1));en=np.convolve((en>vr*.2).astype(float),np.ones(25)/25,'same');duck=np.interp(np.arange(N)/st,np.arange(len(en)),en);music*=vr*.0794/max(float(np.sqrt(np.mean(music**2))),1e-5);music*=1-.72*duck;mix=np.column_stack([v+music,v+music]).astype(np.float32)
 def put(x,t,g):
  k=round(t*sr)
  if k<0:x=x[-k:];k=0
  n=min(len(x),N-k)
  if n>0:mix[k:k+n]+=x[:n,None]*g
 x=np.arange(round(sr*.085))/sr;tick=np.sin(2*np.pi*(950-700*x)*x)*np.exp(-x*65);x=np.arange(round(sr*.24))/sr;wh=np.random.default_rng(31).normal(0,1,len(x));wh=np.convolve(wh,np.ones(5)/5,'same');wh*=np.sin(np.pi*np.minimum(1,x/.24))**2;wh/=max(abs(wh))
 for j,s in enumerate(c['scenes']):
  if j and (s['dark'] or j%3==0):put(wh,s['start']-.075,vr*.15)
  if s['kind'] in ('feed','stack','switch','counter','dots'):
   for q in s['cues']:
    if 0<=q<s['end']:put(tick,q+.015,vr*.1)
 put(tick,c['vo']+.3,vr*.1);n=round(sr*.35);mix[-n:]*=np.linspace(1,0,n)[:,None]
 with wave.open(str(O/(c['slug']+'-raw.wav')),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(mix,-.98,.98)*32767).astype('<i2').tobytes())
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(O/(c['slug']+'-raw.wav')),'-af','loudnorm=I=-16:LRA=11:TP=-1.5','-ar','44100',str(O/(c['slug']+'.wav'))],check=True)
def render(c):
 f=O/('short-'+c['slug']+'.mp4');p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1080x1920','-r','30','-i','-','-i',str(O/(c['slug']+'.wav')),'-vf',f'ass={O/(c["slug"]+".ass")}:fontsdir=/data/fonts','-c:v','libx264','-preset','veryfast','-crf','18','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(f)],stdin=subprocess.PIPE)
 try:
  for j in range(math.ceil(c['duration']*30)):
   p.stdin.write(frame(c,j/30).tobytes())
   if j%300==0:print(c['slug'],j,flush=True)
 finally:p.stdin.close()
 assert p.wait()==0;cv2.imwrite(str(O/('thumbnail-'+c['slug']+'.png')),frame(c,1.1))
 for j,s in enumerate(c['scenes']):cv2.imwrite(str(O/'qa'/f'{c["slug"]}-scene{j:02d}.png'),frame(c,min(s['end']-.04,s['start']+max(.55,(s['end']-s['start'])*.7))))
 for j,t in enumerate([1.1,c['vo']*.55,c['vo']-.35,c['vo']+1.2]):subprocess.run(['ffmpeg','-y','-loglevel','error','-ss',str(t),'-i',str(f),'-frames:v','1',str(O/'qa'/f'{c["slug"]}-actual{j}.png')],check=True)
 pr=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(f)],capture_output=True,text=True,check=True).stdout);s=next(x for x in pr['streams'] if x['codec_type']=='video');d=float(pr['format']['duration']);assert s['width']==W and s['height']==H and s['r_frame_rate']=='30/1' and d<50 and abs(d-c['duration'])<.2
 log=subprocess.run(['ffmpeg','-i',str(f),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr;ld=json.loads(log[log.rfind('{'):log.rfind('}')+1]);assert -17.5<=float(ld['input_i'])<=-14.5 and float(ld['input_tp'])<=-.8;(O/(c['slug']+'-technical-qa.json')).write_text(json.dumps(dict(probe=pr,loudness=ld),indent=2));return dict(file=f.name,title=c['title'],duration=d,voice_duration=c['vo'],scene_count=len(c['scenes']),loudness=float(ld['input_i']),thumbnail='thumbnail-'+c['slug']+'.png',source_ranges=c['ranges'])
if __name__=='__main__':
 with wave.open('voiceover.wav','rb') as w:sr=w.getframerate();assert w.getnchannels()==1;vo=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
 results=[]
 for c in CLIPS:captions(c);audio(c,vo,sr);results.append(render(c))
 json.dump(results,open(O/'shorts-manifest.json','w'),indent=2);json.dump([{k:v for k,v in c.items() if k!='starts'} for c in CLIPS],open(O/'scene-plans.json','w'),indent=2);(O/'release-notes.md').write_text('# Three native motion-first Shorts\n\n'+'\n'.join(f'- **{x["title"]}** — {x["duration"]:.2f}s, 1080×1920, 30fps, {x["loudness"]:.2f} LUFS.' for x in results)+'\n\nOriginal narration and supplied artwork, natively recomposed. Each duration includes a 2.5-second ending. Older releases preserved.\n');print(json.dumps(results),flush=True)
