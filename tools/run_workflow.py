#!/usr/bin/env python3
"""File-based graph prototype. Run gate checks in order; optional content rebuild.

CLI: python tools/run_workflow.py [--rebuild]
Only reuses curated source material; no automatic network access/LLM API calls.
"""
from pathlib import Path
from html.parser import HTMLParser
import subprocess,sys,shutil,json
ROOT=Path(__file__).resolve().parents[1]

class ScriptFinder(HTMLParser):
    def __init__(self):super().__init__();self.inscript=False;self.data=[]
    def handle_starttag(self,tag,attrs):
        if tag=='script':self.inscript=True
    def handle_endtag(self,tag):
        if tag=='script':self.inscript=False
    def handle_data(self,data):
        if self.inscript:self.data.append(data)

def call(args):
    print('RUN:', ' '.join(map(str,args)),flush=True)
    r=subprocess.run(args,cwd=ROOT)
    if r.returncode:raise SystemExit('STOP: Gate failed. Please fix only the failing node before retrying.')

if '--rebuild' in sys.argv:
    # Source → evidence → Wiki → outline → draft → render: deterministic rebuild.
    call([sys.executable,str(ROOT/'tools/build.py')])
for src,dst in [('slides/index.html','slides_script_0.js'),('wiki/index.html','wiki_script_0.js')]:
    finder=ScriptFinder();finder.feed((ROOT/src).read_text(encoding='utf-8'))
    (ROOT/'qa'/dst).write_text('\n'.join(finder.data),encoding='utf-8')
# QA node (fail fast).
call([sys.executable,str(ROOT/'qa/check.py')])
if shutil.which('node'):
    call(['node',str(ROOT/'qa/test_interactions.js')])
else:print('NOTE: Node.js absent; interactive logic checks pending.')
try:
    from weasyprint import HTML
    import fitz
    target=ROOT/'qa/print_preview.pdf'
    HTML(filename=str(ROOT/'slides/index.html')).write_pdf(str(target))
    doc=fitz.open(target)
    expected=len(json.loads((ROOT/'slides/slide_manifest.json').read_text(encoding='utf-8')))
    print(f'PRINT QA: {len(doc)} PDF pages vs {expected} HTML slides')
    if len(doc)!=expected:raise SystemExit('STOP: Render failed. Return to CSS/HTML render node.')
except ImportError:print('NOTE: WeasyPrint / PyMuPDF absent; optional print QA pending.')
print('WORKFLOW COMPLETE: available automated gates passed. Real browser visual check still requires a normal desktop browser.')
