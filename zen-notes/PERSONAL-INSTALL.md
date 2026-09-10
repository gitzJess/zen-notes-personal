# Zen Notes — personal version 2.5.0-personal.1

Based on jjspscl/zen-notes (MIT), retaining the original rich-text editor and themes.

## Changes
- Sidebar width is contained independently of note contents. Long words, URLs and formatted text wrap inside the editor.
- Separate notes with a picker, New, Rename and confirmed Delete controls.
- Pending edits flush before switching notes; active selection survives restart.
- Existing v4 note migrates into the library, with the original JSON backed up in zen.notes.dataBackup.
- Keyboard-accessible collapse control and hidden collapsed contents.

## Install over your existing mod
1. In Sine, turn off auto-update for Zen Notes.
2. Open about:support in Zen and use Profile Folder > Open Folder.
3. Exit Zen completely so the existing note is saved.
4. Back up prefs.js and the chrome/sine-mods/zen-notes folder somewhere safe.
5. Extract the supplied ZIP. Copy the contents of its zen-notes folder into the existing chrome/sine-mods/zen-notes folder, replacing matching files.
6. Start Zen. If needed, toggle Zen Notes off and on in Sine.

The ZIP is a replacement file bundle, not a Sine ZIP importer package. The existing mod must already be registered in Sine. Nothing has been installed into your browser by this workspace.

Use + New to create a blank note, the dropdown to switch, and Rename to give each note a name. Drag the normal Zen sidebar edge to adjust width; the handle above the widget changes its height.

## Data and rollback
This version uses schema v5 in zen.notes.data. Do not re-enable upstream automatic updates: the upstream single-note version cannot read this library. To roll back, first back up the current profile, restore the old mod folder and the pre-install prefs.js while Zen is closed. That returns to the pre-install notes. Keep the current profile backup to retain newer notes.

## Validation
Storage regression tests and XHTML UI integration tests cover migration, reload, separate contents, immediate switching before autosave, rename, deletion cancellation, deleting the last note, and cleanup. All repository validation and JavaScript syntax checks pass.

A real Zen browser check is still required for native sidebar dragging, visual layout, toolbar editing, and interaction with your other mods. These cannot be verified by the XHTML DOM test.

To run tests: node scripts/test-notes.js; npm install --prefix .test-runtime jsdom@26; node scripts/test-ui.js.
