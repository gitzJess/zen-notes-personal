from pathlib import Path
p=Path('zen-notes-ui.uc.js'); s=p.read_text(encoding='utf-8'); s=s.replace('top >= 4 ? top : rect.bottom + 8','top >= bounds.top ? top : rect.bottom + 8'); p.write_text(s,encoding='utf-8')
