const { chromium, firefox } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const assert = require('node:assert/strict');
(async()=>{
 for (const engine of ['chromium','firefox']) {
 const browser = await (engine === 'firefox' ? firefox.launch() : chromium.launch(process.env.CHROMIUM_EXECUTABLE ? {executablePath:process.env.CHROMIUM_EXECUTABLE} : {}));
 try {
 const page = await browser.newPage({viewport:{width:850,height:800},deviceScaleFactor:1});
 page.setDefaultTimeout(10000); const errors=[];page.on('pageerror',e=>{errors.push(e.message);console.error(e.message)});
 await page.setContent('<html><head></head><body><aside id="TabsToolbar"><div class="tabs">Zen Browser<br/><br/>⌕ Search tabs<br/><br/>Your workspace<br/><br/>Getting started</div><div id="zen-sidebar-foot-buttons">Workspace · Personal</div></aside><main>Notes, close at hand.</main></body></html>');
 await page.addStyleTag({content:'body{margin:0;background:#11121b;color:#aeb1c5;font:13px system-ui;display:flex} #TabsToolbar{display:flex;flex-direction:column;justify-content:flex-end;width:280px;height:780px;background:#252630;flex-shrink:0}.tabs{flex:1;padding:24px} #zen-sidebar-foot-buttons{padding:15px;text-align:center}main{padding:50px}'});
 await page.addStyleTag({path:'style.css'});
 await page.evaluate(()=>{const prefs=new Map([['zen.notes.height',440],['zen.notes.appearance','dark']]);window.testPrefs=prefs;window.Services={prefs:{getStringPref:(k,d)=>prefs.get(k)??d,getBoolPref:(k,d)=>prefs.get(k)??d,getIntPref:(k,d)=>prefs.get(k)??d,setStringPref:(k,v)=>prefs.set(k,v),setBoolPref:(k,v)=>prefs.set(k,v),setIntPref:(k,v)=>prefs.set(k,v),addObserver(){},removeObserver(){}}};});
 for(const f of ['core','editor','ui'])await page.addScriptTag({path:`zen-notes-${f}.uc.js`});
 const editor=page.locator('.zen-notes-editor');
 await editor.fill('A little space to think.\n\nKeep an idea, a useful link, or the next thing you want to do.');
 await page.screenshot({path:`tmp/pdfs/${engine}-clean.png`});
 await page.evaluate(()=>{const e=document.querySelector('.zen-notes-editor');const r=document.createRange();r.setStart(e.firstChild,0);r.setEnd(e.firstChild,23);getSelection().removeAllRanges();getSelection().addRange(r);});
 await page.waitForFunction(()=>!document.querySelector('.zen-notes-toolbar').hidden);
 const toolbar=page.locator('.zen-notes-toolbar');
 const tb=await toolbar.boundingBox(); assert.ok(tb.x>=0 && tb.x+tb.width<=280);
 await page.screenshot({path:`tmp/pdfs/${engine}-selected.png`});
 await page.locator('[data-command="bold"]').click();
 assert.ok(await editor.locator('b,strong').count());
 await page.locator('.zen-notes-gear').click();
 await page.locator('#zen-notes-name').fill('Daily notes');
 await page.screenshot({path:`tmp/pdfs/${engine}-manager.png`});
 await page.getByRole('button',{name:'Save name'}).click();
 await editor.fill('a'.repeat(2000));
 for(const width of [200,240,320]){
 await page.evaluate(width=>document.querySelector('#TabsToolbar').style.width=width+'px',width);
 await page.waitForTimeout(80);
 const result=await page.evaluate(()=>{const w=document.querySelector('#zen-notes-widget'),e=document.querySelector('.zen-notes-editor');return {widget:w.getBoundingClientRect().width,editor:e.clientWidth,scroll:e.scrollWidth,sidebar:document.querySelector('#TabsToolbar').getBoundingClientRect().width}});
 assert.ok(result.widget<=width && result.sidebar===width && result.scroll<=result.editor+1,JSON.stringify(result));
 }
 const handle=page.locator('.zen-notes-drag-bar');let rect=await handle.boundingBox();
 await page.mouse.move(rect.x+rect.width/2,rect.y+rect.height/2);await page.mouse.down();await page.mouse.move(rect.x+rect.width/2,rect.y+400);await page.mouse.up();
 assert.equal(await page.locator('#zen-notes-widget').getAttribute('data-collapsed'),'true');
 await page.screenshot({path:`tmp/pdfs/${engine}-collapsed.png`});
 rect=await handle.boundingBox();await page.mouse.move(rect.x+rect.width/2,rect.y+rect.height/2);await page.mouse.down();await page.mouse.move(rect.x+rect.width/2,rect.y-280);await page.mouse.up();
 assert.equal(await page.locator('#zen-notes-widget').getAttribute('data-collapsed'),'false');
 assert.deepEqual(errors,[]);
 console.log(`PASS ${engine}: real selection, bold formatting, floating toolbar bounds, manager, long text wrapping at 200/240/320px, drag collapse/reopen`);
 } finally {await browser.close();}
 }
})().catch(e=>{console.error(e);process.exitCode=1});



