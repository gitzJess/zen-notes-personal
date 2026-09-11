from pathlib import Path
p=Path('scripts/test-ui.js'); s=p.read_text().replace("editor.textContent = 'Select this text';", "editor.getBoundingClientRect = () => ({top:100,bottom:400});\neditor.textContent = 'Select this text';"); p.write_text(s)
