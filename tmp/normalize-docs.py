from pathlib import Path
for f in ['README.md','CHANGELOG.md']:
 p=Path(f);p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n',encoding='utf-8')
