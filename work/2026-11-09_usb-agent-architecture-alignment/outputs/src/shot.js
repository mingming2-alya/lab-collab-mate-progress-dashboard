const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:900}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(800);
const figs=await p.$$('figure');await figs[0].screenshot({path:process.argv[3]+'/f1.png'});await figs[1].screenshot({path:process.argv[3]+'/f2.png'});await figs[2].screenshot({path:process.argv[3]+'/f3.png'});await b.close();})();
