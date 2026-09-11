from pathlib import Path
p=Path('zen-notes-ui.uc.js')
s=p.read_text(encoding='utf-8')
a=s.index('    header.setAttribute("role", "button");'); b=s.index('    const titleLabel',a)
s=s[:a]+'''    const collapsedButton = createXHTMLElement("button");
    collapsedButton.className = "zen-notes-collapsed-button";
    collapsedButton.textContent = "Zen Notes";
    collapsedButton.setAttribute("aria-label", "Expand notes");
    collapsedButton.addEventListener("click", () => setCollapsed(false));

'''+s[b:]
s=s.replace('    toolbar.className = "zen-notes-toolbar";', '''    toolbar.className = "zen-notes-toolbar";
    toolbar.hidden = true;
    toolbar.setAttribute("role", "toolbar");
    toolbar.setAttribute("aria-label", "Format selected text");
    toolbar.setAttribute("popover", "manual");''')
a=s.index('    const noteControls ='); b=s.index('    body.appendChild(editor);',a)
s=s[:a]+'''    const notePicker = createXHTMLElement("select");
    notePicker.className = "zen-notes-picker";
    notePicker.setAttribute("aria-label", "Choose note");
    const gear = createXHTMLElement("button");
    gear.className = "zen-notes-gear";
    gear.textContent = "⚙";
    gear.title = "Manage notes";
    gear.setAttribute("aria-label", "Manage notes");
    gear.setAttribute("aria-expanded", "false");
    const manager = createXHTMLElement("div");
    manager.className = "zen-notes-manager";
    manager.id = "zen-notes-manager";
    manager.hidden = true;
    gear.setAttribute("aria-controls", manager.id);
    const managerLabel = createXHTMLElement("label");
    managerLabel.textContent = "Note name";
    managerLabel.htmlFor = "zen-notes-name";
    const nameInput = createXHTMLElement("input");
    nameInput.id = "zen-notes-name";
    nameInput.maxLength = 120;
    const noteControls = createXHTMLElement("div");
    noteControls.className = "zen-notes-library";
    manager.append(managerLabel, nameInput, noteControls);
    function toggleManager(open) {
      manager.hidden = !open;
      gear.setAttribute("aria-expanded", String(open));
      hideToolbar();
      if (open) { nameInput.value = state.note.title; nameInput.focus(); nameInput.select(); }
    }
    gear.addEventListener("click", () => toggleManager(manager.hidden));
    function noteAction(label, action) {
      const button = createXHTMLElement("button");
      button.textContent = label;
      button.type = "button";
      button.addEventListener("click", action);
      noteControls.appendChild(button);
    }
    function chooseNote(id) {
      flushCurrentEditorImmediately();
      state.activeNoteId = id;
      persistState(state);
      lastEditorSelection = null;
      hideToolbar();
      renderAll();
      editor.scrollTop = 0;
      editor.focus();
    }
    notePicker.addEventListener("change", () => { chooseNote(notePicker.value); toggleManager(false); });
    noteAction("+ New note", () => {
      flushCurrentEditorImmediately();
      const note = createNote(`Note ${state.notes.length + 1}`);
      state.notes.push(note);
      chooseNote(note.id);
      toggleManager(true);
    });
    function renameNote() {
      const title = nameInput.value.trim();
      if (!title) { nameInput.focus(); return; }
      flushCurrentEditorImmediately();
      state.note.title = title.slice(0, 120);
      persistState(state);
      renderAll();
      toggleManager(false);
      gear.focus();
    }
    noteAction("Save name", renameNote);
    nameInput.addEventListener("keydown", e => {
      if (e.key === "Enter") { e.preventDefault(); renameNote(); }
    });
    noteAction("Delete", () => {
      if (!window.confirm(`Delete "${state.note.title}"? This cannot be undone.`)) return;
      flushCurrentEditorImmediately();
      state.notes = state.notes.filter(n => n.id !== state.activeNoteId);
      if (!state.notes.length) state.notes.push(createNote("Note 1"));
      state.activeNoteId = state.notes[0].id;
      persistState(state);
      lastEditorSelection = null;
      renderAll();
      toggleManager(false);
      editor.focus();
    });
    header.replaceChildren(notePicker, gear, collapsedButton);
    body.appendChild(manager);
    widget.appendChild(toolbar);
'''+s[b:]
s=s.replace('    let managerOverlay = null;', '')
s=s.replace('`${words}w \\u00b7 ${chars}c`','`${words}w`')
s=s.replace('      notePicker.value = state.activeNoteId;', '      notePicker.value = state.activeNoteId;\n      nameInput.value = state.note.title;')
a=s.index('    const onDocumentKeydown ='); b=s.index('    function isCheckboxHit',a)
s=s[:a]+'''    function hideToolbar() {
      if (toolbar.matches(":popover-open") && toolbar.hidePopover) toolbar.hidePopover();
      toolbar.hidden = true;
    }
    function positionToolbar() {
      const selection = window.getSelection();
      if (!selection || !selection.rangeCount || selection.isCollapsed ||
          !editor.contains(selection.anchorNode) || !editor.contains(selection.focusNode) ||
          widget.getAttribute("data-collapsed") === "true" || !manager.hidden) {
        hideToolbar(); return;
      }
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();
      const bounds = editor.getBoundingClientRect();
      if (rect.bottom < bounds.top || rect.top > bounds.bottom) { hideToolbar(); return; }
      rememberEditorSelection();
      toolbar.hidden = false;
      if (toolbar.showPopover && !toolbar.matches(":popover-open")) toolbar.showPopover();
      const box = widget.getBoundingClientRect();
      toolbar.style.setProperty("--notes-toolbar-width", `${Math.max(100, box.width - 16)}px`);
      const size = toolbar.getBoundingClientRect();
      const left = Math.max(4, Math.min(rect.left + rect.width / 2 - size.width / 2,
        box.right - size.width - 8, window.innerWidth - size.width - 4));
      const top = rect.top - size.height - 8;
      toolbar.style.setProperty("--notes-toolbar-x", `${Math.max(box.left + 8, left)}px`);
      toolbar.style.setProperty("--notes-toolbar-y", `${Math.max(4, Math.min(
        top >= 4 ? top : rect.bottom + 8, window.innerHeight - size.height - 4))}px`);
    }
    function onSelectionChange() {
      if (toolbar.contains(document.activeElement)) return;
      updateToolbarState();
      positionToolbar();
    }
    function onOutsidePointer(e) {
      if (!widget.contains(e.target)) { hideToolbar(); toggleManager(false); }
    }
    const onDocumentKeydown = (e) => {
      if (!widget.contains(e.target) && !toolbar.contains(e.target)) return;
      if (e.key === "Escape") {
        e.preventDefault(); e.stopPropagation();
        if (!manager.hidden) { toggleManager(false); gear.focus(); }
        else if (!toolbar.hidden) { hideToolbar(); editor.focus(); }
      }
      if (e.altKey && e.key === "F10" && !toolbar.hidden) {
        e.preventDefault(); toolbar.querySelector("button").focus();
      }
    };
    document.addEventListener("keydown", onDocumentKeydown);
    document.addEventListener("selectionchange", onSelectionChange);
    document.addEventListener("mousedown", onOutsidePointer);
    window.addEventListener("resize", positionToolbar);
    const onEditorSelectionActivity = () => { updateToolbarState(); rememberEditorSelection(); positionToolbar(); };
    editor.addEventListener("keyup", onEditorSelectionActivity);
    editor.addEventListener("mouseup", onEditorSelectionActivity);
'''+s[b:]
a=s.index('    header.addEventListener("click"'); b=s.index('    /* ── Arrow-key',a)
s=s[:a]+'''    function setCollapsed(collapsed) {
      flushCurrentEditorImmediately();
      hideToolbar();
      toggleManager(false);
      widget.setAttribute("data-collapsed", String(collapsed));
      setPrefBool(PREF_COLLAPSED, collapsed);
      widget.style.height = collapsed ? "" : `${clampHeight(getNumericPref(PREF_HEIGHT, DEFAULT_HEIGHT))}px`;
      dragBar.setAttribute("aria-valuenow", String(collapsed ? COLLAPSED_HEIGHT : getNumericPref(PREF_HEIGHT, DEFAULT_HEIGHT)));
    }

'''+s[b:]
a=s.index('    /* ── Drag ─'); b=s.index('    /* ── Workspace',a)
s=s[:a]+'''    /* Dragging uses a small collapsed stop and a generous expansion threshold. */
    const COLLAPSED_HEIGHT = 42;
    const COLLAPSE_THRESHOLD = 90;
    const RESIZE_STEP = 30;
    let isDragging = false;
    let dragStartY = 0;
    let dragStartHeight = 0;
    let dragHeight = 0;
    dragBar.tabIndex = 0;
    dragBar.setAttribute("role", "separator");
    dragBar.setAttribute("aria-orientation", "horizontal");
    dragBar.setAttribute("aria-label", "Resize notes. Drag down to collapse, up to expand. Use arrow keys or Enter.");
    dragBar.setAttribute("aria-valuemin", String(COLLAPSED_HEIGHT));
    dragBar.setAttribute("aria-valuemax", String(MAX_HEIGHT));
    dragBar.setAttribute("aria-valuenow", String(isCollapsed ? COLLAPSED_HEIGHT : getNumericPref(PREF_HEIGHT, DEFAULT_HEIGHT)));
    function onMouseMove(e) {
      if (!isDragging) return;
      dragHeight = Math.max(COLLAPSED_HEIGHT, Math.min(MAX_HEIGHT, dragStartHeight + dragStartY - e.clientY));
      const collapsed = dragHeight < COLLAPSE_THRESHOLD;
      widget.setAttribute("data-collapsed", String(collapsed));
      widget.style.height = collapsed ? "" : `${Math.max(MIN_HEIGHT, dragHeight)}px`;
      dragBar.setAttribute("aria-valuenow", String(collapsed ? COLLAPSED_HEIGHT : Math.max(MIN_HEIGHT, dragHeight)));
    }
    function onMouseUp() {
      if (!isDragging) return;
      isDragging = false;
      dragBar.classList.remove("zen-notes-drag-bar--active");
      const collapsed = dragHeight < COLLAPSE_THRESHOLD;
      if (!collapsed) setNumericPref(PREF_HEIGHT, clampHeight(dragHeight));
      setCollapsed(collapsed);
    }
    dragBar.addEventListener("mousedown", (e) => {
      if (e.button !== 0) return;
      flushCurrentEditorImmediately();
      hideToolbar(); toggleManager(false);
      isDragging = true;
      dragBar.classList.add("zen-notes-drag-bar--active");
      dragStartY = e.clientY;
      dragStartHeight = widget.getAttribute("data-collapsed") === "true" ? COLLAPSED_HEIGHT : widget.getBoundingClientRect().height;
      dragHeight = dragStartHeight;
      e.preventDefault();
    });
    dragBar.addEventListener("keydown", e => {
      if (!["ArrowUp", "ArrowDown", "Home", "End", "Enter", " "].includes(e.key)) return;
      e.preventDefault(); e.stopPropagation();
      const collapsed = widget.getAttribute("data-collapsed") === "true";
      if (e.key === "Enter" || e.key === " ") { setCollapsed(!collapsed); return; }
      if (e.key === "Home" || (e.key === "ArrowDown" && (collapsed || getNumericPref(PREF_HEIGHT, DEFAULT_HEIGHT) <= MIN_HEIGHT))) { setCollapsed(true); return; }
      const height = e.key === "End" ? MAX_HEIGHT : collapsed ? MIN_HEIGHT : getNumericPref(PREF_HEIGHT, DEFAULT_HEIGHT) + (e.key === "ArrowUp" ? RESIZE_STEP : -RESIZE_STEP);
      setNumericPref(PREF_HEIGHT, clampHeight(height));
      setCollapsed(false);
    });
    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
    window.addEventListener("blur", onMouseUp);
    const resizeObserver = new ResizeObserver(() => { if (!toolbar.hidden) positionToolbar(); });
    resizeObserver.observe(widget);

'''+s[b:]
s=s.replace('      if (!editor) return;\n      const atBottom', '      if (!editor) return;\n      if (!toolbar.hidden) positionToolbar();\n      const atBottom')
s=s.replace('        if (data === PREF_PRESET) renderAll();','        if (data === PREF_PRESET) applyColorMode();')
s=s.replace('      resizeObserver.disconnect();','      hideToolbar();\n      resizeObserver.disconnect();')
s=s.replace('      window.removeEventListener("mouseup", onMouseUp);','''      window.removeEventListener("mouseup", onMouseUp);
      window.removeEventListener("blur", onMouseUp);
      window.removeEventListener("resize", positionToolbar);
      document.removeEventListener("selectionchange", onSelectionChange);
      document.removeEventListener("mousedown", onOutsidePointer);''')
p.write_text(s,encoding='utf-8')
