const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [name,w,scheme,open,hash] of [['page',1000,'light',false,''],['gantt',1000,'light',true,''],['mobile',390,'light',false,''],['dark',1000,'dark',false,''],['old',1000,'light',false,'#d20261030']]){
 const p=await b.newPage({viewport:{width:w,height:900},colorScheme:scheme});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>m.type()==='error'&&errs.push(m.text()));
 await p.goto('http://localhost:8765/'+hash);await p.waitForTimeout(300);
 if(open){await p.click('#gbox > summary');await p.waitForTimeout(200);}
 if(open){const el=await p.$('#gbox');await el.screenshot({path:name+'.png'});}
 else await p.screenshot({path:name+'.png',fullPage:true});
 console.log(name,errs,await p.evaluate(()=>document.documentElement.scrollWidth));
}
await b.close();})();
