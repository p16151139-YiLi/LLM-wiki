#!/usr/bin/env python3
"""SiC Wiki -> deck static QA. Requires Python stdlib only."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import json, re, sys
ROOT=Path(__file__).resolve().parents[1]
problems=[]
passed=[]
def check(condition,good,bad):
 (passed if condition else problems).append(good if condition else bad)
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
class HTMLAudit(HTMLParser):
 def __init__(self):
  super().__init__();self.href=[];self.sections=[];self.images=[];self.ids=set();self.title=0;self.lang=None
 def handle_starttag(self,t,atts):
  d=dict(atts)
  if t=='html':self.lang=d.get('lang')
  if t=='title':self.title+=1
  if 'id' in d:self.ids.add(d['id'])
  if t=='a' and 'href' in d:self.href.append(d['href'])
  if t=='section' and 'data-slide' in d:self.sections.append(d)
  if t=='img':self.images.append(d)
source=load('source_manifest.json');evidence=load('cards/evidence.json');slide=load('slides/slide_manifest.json');chapters=load('wiki/chapters.json')
sid={s['id'] for s in source};eid={e['id'] for e in evidence}
check(len(source)>=5,f'PASS: 已 ingest {len(source)} 篇來源（>= 5）',f'FAIL: ingest 篇數不足: {len(source)}')
check(len(sid)==len(source),'PASS: 來源 ID 無重複','FAIL: 來源 ID 重複')
check(8<=len(slide)<=15,f'PASS: {len(slide)} 頁教學 HTML（8–15）',f'FAIL: slide count={len(slide)}')
check(set(range(1,len(slide)+1))=={x['no'] for x in slide},'PASS: 投影片頁碼連續','FAIL: slide no not continuous')
check(len(chapters)>=4,f'PASS: Wiki 共 {len(chapters)} 個章節','FAIL: chapter count')
check(all((ROOT/f'raw/{s["id"]}.md').is_file() and urlparse(s['url']).scheme=='https' for s in source),'PASS: 來源皆有 ingested raw 紀錄與 HTTPS URL','FAIL: missing raw or bad source URL')
check(all(e['sources'] and set(e['sources'])<=sid and e.get('position') and (ROOT/f'cards/{e["id"]}.md').is_file() for e in evidence),f'PASS: {len(evidence)} 張證據卡皆有真實來源與位置','FAIL: evidence source/position invalid')
check(all(s['e'] and set(s['e'])<=eid and set(s['sources'])<=sid and len(s['sources'])>=1 for s in slide),'PASS: 每頁投影片對應有效證據卡與來源','FAIL: slide evidence source invalid')
check(all(c['cards'] and set(c['cards'])<=eid and (ROOT/f'wiki/{c["id"]}.md').is_file() for c in chapters),'PASS: Wiki 每章對應證據卡','FAIL: wiki evidence mapping')
check(all((ROOT/f'slides/drafts/{s["no"]:02}.md').is_file() for s in slide),'PASS: 每頁有獨立逐頁草稿','FAIL: draft missing')
check(len({x for s in slide for x in s['e']})>=8,'PASS: 簡報涵蓋至少八種證據卡','FAIL: too few used evidence cards')
for filepath in ('index.html','wiki/index.html','slides/index.html'):
 a=HTMLAudit();a.feed((ROOT/filepath).read_text(encoding='utf-8'))
 check(a.title==1 and a.lang=='zh-Hant',f'PASS: {filepath} HTML 基本結構正確',f'FAIL: {filepath} title/lang')
 for url in a.href:
  if url.startswith(('https://','http://','mailto:','#')):continue
  p=urlparse(url)
  if not p.path:continue
  target=(ROOT/filepath).parent/unquote(p.path)
  if not target.exists():problems.append(f'FAIL: broken local link {filepath} -> {url}')
  elif p.fragment:
   b=HTMLAudit()
   if target.suffix=='.html':
    b.feed(target.read_text(encoding='utf-8'))
    if p.fragment not in b.ids:problems.append(f'FAIL: broken anchor {filepath} -> {url}')
 if filepath=='slides/index.html':
  check(len(a.sections)==len(slide),f'PASS: HTML 實際有 {len(a.sections)} 張 slide section','FAIL: slide html section count')
  raw=(ROOT/filepath).read_text(encoding='utf-8')
  for s in slide:
   find=re.search(rf'<section\b[^>]*data-slide="{s["no"]}".*?</section>',raw,flags=re.S)
   if find is None or any(f'>{sid}↗</a>' not in find.group(0) for sid in s['sources']):problems.append(f'FAIL: 第 {s["no"]} 頁缺原始來源連結')
 check(all('alt' in img for img in a.images),f'PASS: {filepath} 圖像 alt 檢查','FAIL: missing alt')
check((ROOT/'AGENTS.md').is_file() and (ROOT/'workflow_graph.mmd').is_file(),'PASS: AGENTS.md 和 Graph 工作流存在','FAIL: workflow missing')
result={'checked_date':'2026-11-12','source_count':len(source),'evidence_count':len(evidence),'wiki_chapter_count':len(chapters),'slide_count':len(slide),'pass_count':len(passed),'fail_count':len(problems),'passed':passed,'errors':problems}
(ROOT/'qa/static_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('\n'.join(passed+problems))
print(f'RESULT: {len(passed)} pass, {len(problems)} fail')
sys.exit(1 if problems else 0)
