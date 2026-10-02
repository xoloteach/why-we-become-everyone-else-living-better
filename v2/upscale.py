import sys;sys.path.insert(0,'/data/cv_sr')
import cv2,numpy as np,os,glob,json,zipfile
os.chdir('/data/why-we-become-everyone-else-living-better');cv2.setNumThreads(2)
for d in ['native','upscaled','layers','qa']:os.makedirs('v2/'+d,exist_ok=True)
os.makedirs('sheets_raw',exist_ok=True)
with zipfile.ZipFile('/data/restore/Pictures.zip') as z:
 for f in z.namelist():
  if f.lower().endswith('.png'):open('sheets_raw/'+os.path.basename(f),'wb').write(z.read(f))
sr=cv2.dnn_superres.DnnSuperResImpl_create();sr.readModel('/data/sr_models/FSRCNN_x4.pb');sr.setModel('fsrcnn',4)
mp={1:1,5:2,3:3,6:4,10:5,9:6,2:7,8:8,4:9,7:10};report={}
for i,f in enumerate(sorted(glob.glob('sheets_raw/*.png')),1):
 im=cv2.imread(f);g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY);h,w=g.shape;s=mp[i]
 def bounds(prof,size):
  out=[]
  for k in range(4):
   c=round(size*k/3);lo=max(0,c-24);hi=min(size,c+24);out.append(lo+int(np.argmin(prof[lo:hi])))
  return out
 xs=bounds(g.mean(0),w);ys=bounds(g.mean(1),h)
 for p in range(1,10):
  r,c=divmod(p-1,3);a=im[ys[r]+8:ys[r+1]-8,xs[c]+8:xs[c+1]-8];name=f's{s:02d}_p{p}.png';cv2.imwrite('v2/native/'+name,a)
  b=sr.upsample(a);l=cv2.resize(a,(b.shape[1],b.shape[0]),interpolation=cv2.INTER_LANCZOS4);b=cv2.addWeighted(b,.78,l,.22,0);b=cv2.addWeighted(b,1.12,cv2.GaussianBlur(b,(0,0),.8),-.12,0);cv2.imwrite('v2/upscaled/'+name,b)
  sample=np.median(np.concatenate([b[:20].reshape(-1,3),b[-20:].reshape(-1,3),b[:,:20].reshape(-1,3),b[:,-20:].reshape(-1,3)]),axis=0);delta=np.max(abs(b.astype(float)-sample),axis=2);alpha=np.clip((delta-9)/35,0,1).astype(np.float32)
  solid=(alpha>.4).astype(np.uint8)*255;ct,_=cv2.findContours(solid,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);hull=np.zeros_like(solid)
  for x in ct:
   if cv2.contourArea(x)>120:cv2.drawContours(hull,[x],-1,255,-1)
  alpha=np.maximum(alpha,cv2.GaussianBlur(hull,(5,5),0)/255);cv2.imwrite('v2/layers/'+name,np.dstack([b,(alpha*255).astype(np.uint8)]))
  yy,xx=np.where(alpha>.5);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)] if len(xx) else [0,0,b.shape[1],b.shape[0]];report[f'{s:02d}-{p}']={'native':list(a.shape[:2][::-1]),'upscaled':list(b.shape[:2][::-1]),'bbox':box};print(f'{s:02d}-{p}',flush=True)
json.dump(report,open('v2/upscale_report.json','w'),indent=1);print('DONE',flush=True)
