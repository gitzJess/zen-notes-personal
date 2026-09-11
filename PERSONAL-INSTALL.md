# Zen Notes — personal version 2.6.0-personal.1

A minimal note-taking mod based on jjspscl/zen-notes (MIT).

## What's new
- Clean header with just a note dropdown and gear button.
- Gear opens an inline manager: create a note, edit its name, or delete it with confirmation.
- Select text to reveal bold, italic, underline, strikethrough, bullet/numbered list, checklist and link tools. The toolbar sits above the selection when space permits, or below it to avoid covering the header. It wraps in narrow sidebars.
- Drag the handle above the widget down to collapse, then up to reopen. The chosen expanded height is saved.
- Minimal last-edited date and word count. No permanent formatting row.
- Existing text wrapping and independent note storage are retained.

## Update your personal installation
You do not need to install the original mod.

1. Keep automatic updates disabled for this mod. Its inherited homepage metadata still references the upstream repository.
2. In Zen, open about:support > Profile Folder > Open Folder.
3. Exit Zen completely, then back up prefs.js and your installed personal mod folder under chrome/sine-mods/.
4. Extract zen-notes-2.6.0-personal.1.zip. Copy the contents of its zen-notes folder into the folder of your installed personal version, replacing matching files.
5. Start Zen. If needed, toggle the mod off and on in Sine.

If you installed from your own GitHub repository, also upload the new package contents to that repository's root (theme.json at top level) so your repository contains the updated version. Set homepage and readme in theme.json to your own repository URLs before using repository-driven updates. Do not use the upstream repository's update button to obtain this personal build.

## Fresh installation through your repository
Upload the contents of the ZIP's zen-notes folder to your own public GitHub repository. In Sine's custom repository field, enter YOUR-USERNAME/YOUR-REPOSITORY. If custom scripts are blocked, enable sine.allow-unsafe-js in about:config. The ZIP itself is not a Sine import package. Installing the original mod is unnecessary.

## Controls
- Dropdown: switch notes. Edits save before switching.
- Gear: manage notes. Edit the name and click Save name (or Enter). + New note creates and selects a blank note.
- Select text: formatting tools appear. Existing Ctrl+B/I/U/K shortcuts still work. Alt+F10 focuses the visible formatting toolbar.
- Resize handle: drag down to collapse, up to reopen. Keyboard: Up/Down resize, Home collapses, End maximizes, Enter toggles. The collapsed Zen Notes button is also clickable.
- Escape dismisses the manager or formatting tools while focused inside notes; it does not collapse notes when used elsewhere in the browser.

## Notes and rollback
This release keeps schema v5 and the same preference keys as 2.5.0-personal.1. Existing notes and selection are preserved. Rolling back to 2.5.0-personal.1 only requires restoring that version's files. Upstream's single-note versions cannot read this library: retain a profile backup before switching to an upstream version.

## Validation
Storage tests, XHTML DOM tests, and real Chromium/Firefox browser tests pass. Browser tests cover selection-based formatting, header controls, long unbroken text at sidebar widths of 200/240/320 pixels, and drag collapse/reopen. Screenshots of the expanded, selected, manager and collapsed states were reviewed.

These tests use a simulated sidebar. Sine injection and interaction with your other mods still require checking in your own Zen window. This package has not been installed into your profile automatically.

Developer tests: node scripts/test-notes.js; npm install --prefix .test-runtime jsdom@26; node scripts/test-ui.js. Browser tests require Playwright and its Chromium/Firefox binaries; scripts/test-browser.js accepts PLAYWRIGHT_MODULE and CHROMIUM_EXECUTABLE overrides.
