const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
function boot(initial) {
  const prefs = new Map(Object.entries(initial || {}));
  const context = {window: {}, console, Services: {prefs: {
    getStringPref: (k, d) => prefs.get(k) ?? d,
    getIntPref: (k, d) => prefs.get(k) ?? d,
    setStringPref: (k, v) => prefs.set(k, v),
    setIntPref: (k, v) => prefs.set(k, v)
  }}};
  vm.runInNewContext(fs.readFileSync('zen-notes-core.uc.js', 'utf8'), context);
  return { api: context.window.ZenNotes, prefs };
}
for (const initial of [{}, {'zen.notes.content': '<b>legacy</b>'},
  {'zen.notes.data': JSON.stringify({version: 4, note: {id:'old', title:'Old', contentHTML:'<p>keep me</p>'}})}]) {
  const {api, prefs} = boot(initial);
  const state = api.loadState('workspace');
  assert.equal(state.notes.length, 1);
  const original = state.note.contentHTML;
  const second = api.createNote('Second', {contentHTML:'separate'});
  state.notes.push(second);
  state.activeNoteId = second.id;
  api.persistState(state);
  const reloaded = api.loadState('workspace');
  assert.equal(reloaded.notes.length, 2);
  assert.equal(reloaded.note.contentHTML, 'separate');
  assert.equal(reloaded.notes[0].contentHTML, original);
  assert.equal(JSON.parse(prefs.get('zen.notes.data')).note, undefined);
  if (initial['zen.notes.data']) assert.equal(prefs.get('zen.notes.dataBackup'), initial['zen.notes.data']);
}
const {api} = boot({'zen.notes.data': JSON.stringify({version:5, notes:[{id:'a'},{id:'a'},null],activeNoteId:'missing'})});
const repaired = api.loadState();
assert.equal(new Set(repaired.notes.map(n => n.id)).size, 2);
assert.ok(repaired.note);
console.log('PASS: fresh state, legacy/v4 migration, independent notes, restart, active selection, duplicate IDs');
