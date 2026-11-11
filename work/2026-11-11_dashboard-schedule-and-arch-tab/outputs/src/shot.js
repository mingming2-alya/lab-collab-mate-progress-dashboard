const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [name,url,w,h,full] of [['schedule-desktop','http://localhost:8765/',1000,1400,false],['mobile','http://localhost:8765/',390,1600,false],['arch','http://localhost:8765/arch.html',1400,1000,true],['dark','http://localhost:8765/',1000,1300,false]]){
 const p=await b.newPage({viewport:{width:w,height:h},colorScheme:name==='dark'?'dark':'light'});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
 await p.goto(url);await p.waitForTimeout(500);
 await p.screenshot({path:name+'.png',fullPage:full});console.log(name,errs);
 if(name==='mobile'){console.log('scrollW',await p.evaluate(()=>document.documentElement.scrollWidth));}
}
await b.close();})();
