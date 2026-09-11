from pathlib import Path
p=Path('zen-notes-ui.uc.js'); s=p.read_text(encoding='utf-8').replace('toolbar.matches(":popover-open") && toolbar.hidePopover','toolbar.hidePopover && toolbar.matches(":popover-open")'); p.write_text(s,encoding='utf-8')
p=Path('scripts/test-ui.js'); s=p.read_text(); s=s.replace("w.ResizeObserver =", "w.Range.prototype.getBoundingClientRect = () => ({left:20, top:150, bottom:170, width:100});\nw.ResizeObserver =")
s=s.replace("w.prompt = ()=> 'Renamed'; buttons[1].click();", "widget.querySelector('#zen-notes-name').value = 'Renamed'; buttons[1].click();")
s=s.replace('widget._zenNotesCleanup();', '''const handle = w.document.querySelector('.zen-notes-drag-bar');
widget.getBoundingClientRect = () => ({height:300, width:280, left:0, right:280});
handle.dispatchEvent(new w.MouseEvent('mousedown', {button:0,clientY:100}));
w.dispatchEvent(new w.MouseEvent('mousemove', {clientY:380}));
w.dispatchEvent(new w.MouseEvent('mouseup'));
assert.equal(widget.getAttribute('data-collapsed'),'true');
assert.equal(prefs.get('zen.notes.collapsed'),true);
handle.dispatchEvent(new w.MouseEvent('mousedown', {button:0,clientY:380}));
w.dispatchEvent(new w.MouseEvent('mousemove', {clientY:180}));
w.dispatchEvent(new w.MouseEvent('mouseup'));
assert.equal(widget.getAttribute('data-collapsed'),'false');
assert.equal(prefs.get('zen.notes.height'),242);
w.document.body.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
assert.equal(widget.getAttribute('data-collapsed'),'false');
widget.querySelector('.zen-notes-gear').click();
assert.equal(widget.querySelector('.zen-notes-manager').hidden,false);
widget.querySelector('#zen-notes-name').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
assert.equal(widget.querySelector('.zen-notes-manager').hidden,true);
editor.textContent = 'Select this text';
const range = w.document.createRange(); range.selectNodeContents(editor);
w.getSelection().removeAllRanges(); w.getSelection().addRange(range);
w.document.dispatchEvent(new w.Event('selectionchange'));
assert.equal(widget.querySelector('.zen-notes-toolbar').hidden,false);
w.getSelection().collapseToEnd();
w.document.dispatchEvent(new w.Event('selectionchange'));
assert.equal(widget.querySelector('.zen-notes-toolbar').hidden,true);
widget._zenNotesCleanup();''')
s=s.replace("console.log('PASS:","console.log('PASS: drag collapse/expand, scoped Escape, gear manager, selection toolbar,")
p.write_text(s)
