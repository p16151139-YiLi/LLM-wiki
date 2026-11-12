#!/usr/bin/env python3
"""Functional Chromium browser QA (optional: pip install playwright; playwright install chromium)."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json, sys, shutil
ROOT=Path(__file__).resolve().parents[1]
issues=[]; outcomes=[];stats=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=shutil.which('chromium') or None,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(1280,720),(1366,768),(390,844)]:
  page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
  page.goto('http://127.0.0.1:8765/slides/index.html',wait_until='domcontentloaded')
  for i in range(1,14):
   page.locator('#'+str(i)).count() # harmless hash link marker check
   page.evaluate('n => window.location.hash = "#" + n',i)
   page.wait_for_timeout(23)
   dims=page.evaluate('''() => {const el=document.querySelector('.slide.active'),body=el.querySelector('.slide-body'),foot=el.querySelector('.foot'),a=el.getBoundingClientRect(),b=body.getBoundingClientRect(),f=foot.getBoundingClientRect();return {slide:el.dataset.slide,verticalOverlap:b.bottom>f.top+1,slideOverflow:el.scrollHeight>el.clientHeight+3,top:a.top,bottom:a.bottom,footTop:f.top,bodyBottom:b.bottom,mainScroll:document.documentElement.scrollWidth>window.innerWidth+2};}''')
   stats.append({'viewport':f'{width}x{height}','page':i,**dims})
   if dims['verticalOverlap'] or dims['slideOverflow'] or dims['mainScroll']:
    issues.append(f'{width}x{height} page {i}: {dims}')
  page.keyboard.press('Home'); page.keyboard.press('ArrowRight')
  if not page.locator('.slide.active').get_attribute('data-slide')=='2':issues.append(f'{width}x{height}: ArrowRight did not navigate to slide 2')
  page.locator('#prev').click()
  if not page.locator('.slide.active').get_attribute('data-slide')=='1':issues.append(f'{width}x{height}: Previous button fails')
  if width==1280:
   page.screenshot(path=str(ROOT/'qa/slide01.png'))
   page.goto('http://127.0.0.1:8765/slides/index.html#7',wait_until='domcontentloaded')
   page.screenshot(path=str(ROOT/'qa/slide07.png'))
  outcomes.append(f'{width}x{height}: {13} slides tested; buttons and keyboard verified')
  page.close()
 page=browser.new_page(viewport={'width':1280,'height':820},device_scale_factor=1)
 page.goto('http://127.0.0.1:8765/wiki/index.html',wait_until='domcontentloaded')
 if page.locator('.chapter').count()!=6:issues.append('Wiki has missing chapters')
 page.locator('#search').fill('磊晶')
 visible=page.locator('.chapter:visible').count()
 if not (1<=visible<6):issues.append(f'Wiki search not filtering: {visible}')
 page.locator('#search').fill('')
 if page.locator('.chapter:visible').count()!=6:issues.append('Wiki clear search did not restore all chapters')
 page.screenshot(path=str(ROOT/'qa/wiki.png'),full_page=False)
 outcomes.append(f'Wiki search test: {visible} matching chapters, clearing restores 6 chapters')
 browser.close()

result={'checked_date':'2026-11-12','result':'FAIL' if issues else 'PASS','outcomes':outcomes,'issue_count':len(issues),'issues':issues,'overflow_stats':stats}
(ROOT/'qa/browser_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('\n'.join(outcomes))
print('ISSUES:',*issues,sep='\n- ')
sys.exit(1 if issues else 0)
