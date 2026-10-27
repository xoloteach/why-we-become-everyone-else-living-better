import {chromium} from 'playwright';
import {createServer} from 'vite';
import {spawn,spawnSync} from 'node:child_process';
import {mkdir,writeFile} from 'node:fs/promises';
import {Document,NodeIO} from '@gltf-transform/core';
import {dedup} from '@gltf-transform/functions';
const tools=['Anime.js','React Spring','PixiJS','p5.js','Paper.js','Matter.js','Three.js','Rapier','OGL','tsParticles','glTF Transform','GL Transitions','Tone.js'];
await mkdir('output',{recursive:true});
const doc=new Document(), buffer=doc.createBuffer(), scene=doc.createScene('example');
for(let i=0;i<15;i++){let pos=doc.createAccessor().setType('VEC3').setArray(new Float32Array([0,0,0,1,0,0,0,1,0])).setBuffer(buffer);let mesh=doc.createMesh().addPrimitive(doc.createPrimitive().setAttribute('POSITION',pos));scene.addChild(doc.createNode().setMesh(mesh).setTranslation([i,0,0]));}
const io=new NodeIO();let before=(await io.writeBinary(doc)).length;await doc.transform(dedup());let after=(await io.writeBinary(doc)).length;await writeFile('sizes.json',JSON.stringify({before,after}));
const server=await createServer({server:{host:'127.0.0.1',port:4173}});await server.listen();
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
let report=[];
for(let k=0;k<tools.length;k++){
 let name=tools[k],slug=name.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/-$/,'');let page=await browser.newPage({viewport:{width:640,height:360},deviceScaleFactor:1});let errors=[];page.on('pageerror',e=>errors.push(e.message));let out=`output/${String(k+1).padStart(2,'0')}-${slug}.mp4`;
 try{
  await page.goto(`http://127.0.0.1:4173/?tool=${encodeURIComponent(name)}`,{waitUntil:'load',timeout:60000});await page.waitForFunction(()=>window.sampleReady===true,{timeout:60000});
  if(name==='Tone.js'){let samples=await page.evaluate(()=>window.makeAudio());let b=Buffer.alloc(44+samples.length*2);b.write('RIFF',0);b.writeUInt32LE(b.length-8,4);b.write('WAVEfmt ',8);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(44100,24);b.writeUInt32LE(88200,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(samples.length*2,40);samples.forEach((v,i)=>b.writeInt16LE(Math.round(Math.max(-1,Math.min(1,v))*32767),44+i*2));await writeFile('output/tone.wav',b);}
  let args=['-hide_banner','-loglevel','error','-y','-f','image2pipe','-vcodec','png','-framerate','24','-i','pipe:0'];if(name==='Tone.js')args.push('-i','output/tone.wav');else args.push('-f','lavfi','-i','anullsrc=r=44100:cl=mono');args.push('-t','4','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-shortest','-movflags','+faststart',out);
  let ff=spawn('ffmpeg',args,{stdio:['pipe','ignore','pipe']});let err='';ff.stderr.on('data',x=>err+=x);let done=new Promise((resolve,reject)=>{ff.on('error',reject);ff.on('close',c=>c===0?resolve():reject(new Error(err)))});ff.stdin.on('error',()=>{});
  for(let frame=0;frame<96;frame++){await page.evaluate(t=>window.drawFrame(t),frame/24);let img=await page.screenshot();if(frame===24||frame===72)await writeFile(`output/${slug}-${frame}.png`,img);if(!ff.stdin.write(img))await new Promise(r=>ff.stdin.once('drain',r));}ff.stdin.end();await done;
  if(errors.length)throw new Error(errors.join('; '));report.push({tool:name,status:'rendered',file:out});console.log('OK',name);
 }catch(e){report.push({tool:name,status:'failed',error:String(e.message||e)});console.error('FAILED',name,e.message)}finally{await page.close();}
}
await browser.close();await server.close();
let success=report.filter(x=>x.status==='rendered');await writeFile('output/report.json',JSON.stringify({samples:report,glTF: {before,after}},null,2));
if(success.length){await writeFile('output/concat.txt',success.map(x=>`file '${x.file.split('/').pop()}'`).join('\n'));let cmd=spawnSync('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i','output/concat.txt','-c','copy','-movflags','+faststart','output/comparison.mp4'],{encoding:'utf8'});if(cmd.status!==0)console.error(cmd.stderr);}
if(success.length!==tools.length)process.exitCode=1;
