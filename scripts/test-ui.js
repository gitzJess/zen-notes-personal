const assert = require('node:assert/strict');
const fs = require('node:fs');
const {JSDOM} = require('../.test-runtime/node_modules/jsdom');
const dom = new JSDOM('<html xmlns="http://www.w3.org/1999/xhtml"><body><div id="TabsToolbar"><div id="zen-sidebar-foot-buttons"></div></div></body></html>', {contentType:'application/xhtml+xml', runScripts:'outside-only'});
const w = dom.window;
const prefs = new Map();
w.Services = {prefs: {
 getStringPref:(k,d)=>prefs.get(k)??d, getIntPref:(k,d)=>prefs.get(k)??d, getBoolPref:(k,d)=>prefs.get(k)??d,
 setStringPref:(k,v)=>prefs.set(k,v), setIntPref:(k,v)=>prefs.set(k,v), setBoolPref:(k,v)=>prefs.set(k,v),
 addObserver(){}, removeObserver(){}
}};
w.ResizeObserver = class {observe(){} disconnect(){}};
w.document.execCommand = ()=>true;
w.document.queryCommandState = ()=>false;
for (const f of ['core','editor','ui']) w.eval(fs.readFileSync(`zen-notes-${f}.uc.js`,'utf8'));
w.dispatchEvent(new w.Event('DOMContentLoaded'));
const widget = w.document.getElementById('zen-notes-widget');
assert.ok(widget);
const editor = widget.querySelector('.zen-notes-editor');
const picker = widget.querySelector('select');
const buttons = [...widget.querySelectorAll('.zen-notes-library button')];
editor.innerHTML = '<b>First note</b>';
editor.dispatchEvent(new w.Event('input'));
buttons[0].click();
assert.equal(picker.options.length,2);
assert.equal(editor.textContent,'');
editor.textContent = 'Second note';
editor.dispatchEvent(new w.Event('input'));
picker.value = picker.options[0].value;
picker.dispatchEvent(new w.Event('change'));
assert.equal(editor.textContent,'First note');
assert.equal(JSON.parse(prefs.get('zen.notes.data')).notes[1].contentHTML,'Second note');
w.prompt = ()=> 'Renamed'; buttons[1].click();
assert.equal(picker.selectedOptions[0].textContent,'Renamed');
w.confirm = ()=> false; buttons[2].click(); assert.equal(picker.options.length,2);
w.confirm = ()=> true; buttons[2].click(); assert.equal(picker.options.length,1);
assert.equal(editor.textContent,'Second note');
buttons[2].click(); assert.equal(picker.options.length,1); assert.equal(editor.textContent,'');
widget._zenNotesCleanup();
assert.equal(w.document.getElementById('zen-notes-widget'),null);
w.close();
console.log('PASS: XHTML UI, immediate switching with pending edits, rename, cancel/delete, last-note replacement, cleanup');
