from pathlib import Path
import json, html, textwrap, re
from datetime import date
from jinja2 import Template
P=Path(__file__).resolve().parents[1]
for x in ['raw','wiki','cards','slides/drafts','qa','.agents/workflows']:(P/x).mkdir(parents=True,exist_ok=True)
def write(path,content):
 p=P/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content.strip()+'\n',encoding='utf-8')

sources=[
 dict(id='S01',title='Silicon Carbide in Integrated Energy',author='U.S. Department of Energy, Integrated Energy Systems Office',year='2026（網頁載有 2026/03 圖說；未明示文章發布日）',type='美國政府公開技術解說',url='https://www.energy.gov/cmei/systems/silicon-carbide-integrated-energy',access='公開網頁全文',section='Benefits of Silicon Carbide / The Wide-Bandgap Advantage',keypoints=['SiC 因寬能隙、較高耐壓與耐溫能力，可應用於高效率功率轉換器。','太陽能逆變器、電動車等是具體應用；效率提升需以實際系統設計為準。','較低能量損失可能降低散熱負擔，讓系統更小。'],limits='政府解說包含示例數字，不能推廣為所有 SiC 裝置均達相同效率。'),
 dict(id='S02',title='Recent Progress on Single-Crystal Growth and Epitaxial Growth of 4H Silicon Carbide',author='Yi Lin Liu',year='2022',type='綜述論文（可查公開摘要，全文需機構權限）',url='https://www.scientific.net/SSP.332.73',access='公開摘要',section='Abstract',keypoints=['區分 PVT 單晶成長、晶圓切磨與 CVD 磊晶等技術階段。','SiC 功率元件需兼顧單晶品質、磊晶層摻雜控制與缺陷控制。','微管、差排、堆疊缺陷是研究重點。'],limits='僅依公開摘要整理；未取得付費全文，沒有宣稱已閱讀全文。'),
 dict(id='S03',title='Epitaxial Growth of Silicon Carbide',author='Tsunenobu Kimoto; James A. Cooper',year='2014',type='學術書籍章節（可查公開摘要）',url='https://onlinelibrary.wiley.com/doi/10.1002/9781118313534.ch4',access='公開摘要',section='Summary',keypoints=['磊晶能形成所需厚度及摻雜濃度的主動層，這在塊材長晶時較難精確控制。','同質磊晶常用 step-flow 成長機制，且 C/Si 比例會影響摻雜控制。','長晶所得基板與其上磊晶層的任務不同。'],limits='僅整理出版商可見的 Summary，沒有複製未公開內文。'),
 dict(id='S04',title='Review of Silicon Carbide Processing for Power MOSFET',author='Catherine Langpoklakpam et al.',year='2022',type='同儕審查開放取用綜述（Crystals 12(2),245）',url='https://www.mdpi.com/2073-4352/12/2/245',access='公開網頁全文',section='Introduction / SiC Critical Step / Table 1 / MOSFET',keypoints=['4H-SiC 的能隙約 3.26 eV，而 Si 約 1.12 eV（文中 Table 1）；數值依材料、測試條件而異。','一般單晶塊材可使用 PVT 成長，後續在基板上進行 CVD 磊晶與元件製程。','SiC MOSFET 具低導通電阻、低切換損失潛力，但 SiC/氧化層介面通道遷移率仍是挑戰。'],limits='數據僅引用文章 Table 1，其他不同文獻不合併成單一標準值。'),
 dict(id='S05',title='Structure Defects in CVD-Grown Silicon Carbide Epitaxial Wafers: From Fundamental Principles to Advanced Reduction Strategies',author='Guoliang Zhang et al.',year='2026',type='同儕審查開放取用綜述（Micromachines 17(2),252）',url='https://www.mdpi.com/2072-666X/17/2/252',access='公開網頁全文',section='Abstract / Sections 2–3 / Conclusions',keypoints=['CVD 磊晶晶圓可能含穿通差排、基面差排、堆疊缺陷與三角形缺陷。','基板缺陷傳遞、表面動力學及成長條件會影響磊晶缺陷。','控制基板前處理、切角與 C/Si 比例等，是缺陷減少策略。'],limits='本資料是文獻綜述，所提方法不能解讀成在任何條件都可完全消除缺陷。'),
 dict(id='S06',title='Wide Bandgap Semiconductors for Power Electronics: Comparative Properties, Applications, and Reliability of GaN and SiC Devices',author='Nathaniel Viewegh et al.',year='2026',type='同儕審查開放取用綜述（Hardware 4(1),6）',url='https://www.mdpi.com/2813-6640/4/1/6',access='公開網頁全文',section='Introduction / Section 2.2 / Applications',keypoints=['4H-SiC 是主流功率元件晶型之一，與 Si 相比有較大能隙與較高耐壓能力。','材料遷移率並非 SiC 所有條件都優於 Si；須區分塊材與 MOSFET 界面通道。','製造成本、缺陷、封裝熱管理與可靠度是 SiC 普及的挑戰。'],limits='不同表格可能呈現不同參考數值；本作業的數值一律優先採 S04 Table 1。')
]
write('source_manifest.json',json.dumps(sources,ensure_ascii=False,indent=2))
for s in sources:
 raw=f"""# [{s['id']}] {s['title']}

- 作者／機構：{s['author']}
- 發布年份：{s['year']}
- 資料型態：{s['type']}
- 存取範圍：{s['access']}
- 原始來源：{s['url']}
- 對照位置：{s['section']}
- 本次整理日期：2026-11-12

## Ingest 後可檢索的事實（中文改寫；非原文全文）
"""+'\n'.join(f'{i+1}. {p}' for i,p in enumerate(s['keypoints']))+f"""

## 引用限制與不確定性
{s['limits']}

## 驗證狀態
已核對來源網頁／公開摘要及作者、題名、相關內容；未將付費全文冒稱為已下載。本檔是來源卡與重點索引，不是原文重製。
"""
 write(f"raw/{s['id']}.md",raw)

evidence=[
 dict(id='E01',claim='SiC 是寬能隙半導體，可用於高電壓與高溫功率電子。',sources=['S01','S06'],position='S01 The Wide-Bandgap Advantage；S06 Introduction',tags=['概念','寬能隙']),
 dict(id='E02',claim='S04 的 Table 1 列出室溫 Si 能隙約 1.12 eV、4H-SiC 約 3.26 eV；這不是遷移率的比較。',sources=['S04'],position='S04 Table 1',tags=['數字','材料']),
 dict(id='E03',claim='SiC 的優勢是高崩潰電場與散熱、切換潛力，不能直接推論其電子遷移率必高於 Si。',sources=['S04','S06'],position='S04 Table 1 and MOSFET channel mobility；S06 Section 2.2',tags=['迷思','物性']),
 dict(id='E04',claim='SiC 塊材單晶成長常用 PVT，之後進行晶圓加工以取得基板。',sources=['S02','S04'],position='S02 Abstract；S04 SiC Critical Step',tags=['長晶','製程']),
 dict(id='E05',claim='SiC 磊晶常用 CVD 在晶體基板上沉積受控厚度、摻雜之功能性材料層。',sources=['S03','S04'],position='S03 Summary；S04 Section 2.2',tags=['磊晶','製程']),
 dict(id='E06',claim='可用「單晶成長→晶圓切磨／基板→磊晶→元件製程」認識主要材料到元件流程。',sources=['S02','S04'],position='S02 Abstract；S04 Processing Review',tags=['製程','流程']),
 dict(id='E07',claim='CVD 磊晶缺陷與基板、表面反應及成長條件有關，須檢測並控制。',sources=['S05'],position='S05 Abstract and Sections 2–3',tags=['缺陷','可靠度']),
 dict(id='E08',claim='SiC MOSFET 在適當設計下可降低導通或切換損失，但界面通道遷移率會造成限制。',sources=['S04'],position='S04 Abstract and MOSFET section',tags=['元件','MOSFET']),
 dict(id='E09',claim='電動車驅動、光伏逆變器和功率轉換器是 SiC 常見應用。',sources=['S01','S06'],position='S01 applications；S06 Introduction and Applications',tags=['應用']),
 dict(id='E10',claim='SiC 製造及應用仍受缺陷、成本、封裝與熱管理等因素限制。',sources=['S05','S06'],position='S05 Conclusions；S06 Introduction and Reliability',tags=['挑戰']),
 dict(id='E11',claim='在大量材料成長時，厚度和摻雜的精密控制不易；磊晶提供專門的元件層。',sources=['S03'],position='S03 Summary',tags=['比較','磊晶']),
 dict(id='E12',claim='4H-SiC 是 SiC 的重要晶型之一，晶體堆疊方式影響物性。',sources=['S06','S04'],position='S06 Section 2.2.1；S04 polytypes',tags=['晶型'])
]
write('cards/evidence.json',json.dumps(evidence,ensure_ascii=False,indent=2))
for e in evidence:
 write(f"cards/{e['id']}.md",f"# {e['id']}｜證據卡\n\n**可用陳述**：{e['claim']}\n\n**來源 ID**：{', '.join(e['sources'])}\n\n**原文位置**：{e['position']}\n\n**允許用途**：教學改寫並標明來源；不可擴張成沒有資料支持的定量結論。\n")

chapters=[
 dict(id='intro',title='01｜認識 SiC',summary='從材料名稱、寬能隙到功率半導體的用途。',cards=['E01','E02','E12'],paragraphs=['碳化矽（SiC）是由矽與碳形成的半導體材料。用於功率元件時，常見的是 4H-SiC 晶型。對初學者來說，可以把功率元件想成負責控制大量電能流動的電子開關。','「寬能隙」是 SiC 的關鍵物性之一。它不是代表電子一定跑得更快，而是與高電場耐受性、漏電等工作特性密切相關。'],focus='常見誤解：能隙大 ≠ 電子遷移率一定更高。'),
 dict(id='properties',title='02｜材料特性與效能',summary='分開理解耐壓、導熱、遷移率與系統效率。',cards=['E02','E03','E08'],paragraphs=['文獻整理的室溫材料參考值：Si 約 1.12 eV、4H-SiC 約 3.26 eV。數字用來比較能隙，不能直接比較器件的實際效率。','SiC 的高崩潰電場可讓高耐壓器件設計更有彈性；切換與導通損失還受元件結構、控制策略及封裝影響。','SiC/氧化層介面通道遷移率可能偏低，因此不能把高功率密度簡化成「電子跑得最快」。'],focus='材料潛力與實際成品效能必須分開說明。'),
 dict(id='growth',title='03｜單晶長晶與基板',summary='長晶是取得高品質塊材，接著加工成晶圓基板。',cards=['E04','E06'],paragraphs=['單晶長晶的目標是形成尺寸與品質足以製作晶圓的 SiC 塊材。PVT（物理氣相傳輸）是常見方式。','經過切片、研磨、拋光等晶圓加工後，才能得到供後續製程使用的 SiC 基板。基板是承載後續磊晶與元件的材料平台。'],focus='長晶不是直接長出完整的 MOSFET。'),
 dict(id='epitaxy',title='04｜磊晶與功能層',summary='在基板表面形成厚度與摻雜可設計的晶體層。',cards=['E05','E11','E07'],paragraphs=['磊晶（epitaxy）是以現有晶體為基礎，讓新晶體層沿著基板的晶格排列成長。SiC 功率元件常使用 CVD（化學氣相沉積）形成同質磊晶層。','磊晶的重要價值是把主動層的厚度與摻雜濃度做得更符合元件設計。磊晶層的缺陷會影響可靠度，因此不能只看成長速度。'],focus='長晶決定基板；磊晶設計元件所需的功能層。'),
 dict(id='device',title='05｜MOSFET 製程與缺陷',summary='從磊晶晶圓走向功率元件，品質與界面可靠度重要。',cards=['E07','E08'],paragraphs=['有了磊晶晶圓後，還要透過多個半導體製程階段形成 MOSFET 等功率元件。SiC MOSFET 可在適當使用條件下提升電能轉換效能。','不同缺陷，如差排與堆疊缺陷，可能由基板繼承或在磊晶時生成；通道介面特性也是影響導通性能的因素。'],focus='「材料很強」不能取代元件可靠度測試。'),
 dict(id='application',title='06｜應用與限制',summary='電動車、再生能源與成本、可靠度的取捨。',cards=['E09','E10'],paragraphs=['SiC 常用於電動車電力轉換與太陽能逆變器等需要高效率、高耐壓的系統。','技術並非在所有場合都更合適：價格、元件缺陷、熱管理、封裝與系統設計，都會決定 SiC 是否能帶來預期收益。'],focus='不能將特定示範系統的效率數字視為所有 SiC 系統的保證。'),
]
write('wiki/chapters.json',json.dumps(chapters,ensure_ascii=False,indent=2))
idx='# SiC LLM Wiki｜索引\n\n範圍：入門 SiC 材料、長晶、磊晶、MOSFET 與應用；繁體中文；每項重要論點透過證據卡連到來源。\n\n'
for c in chapters:
 body=f"# {c['title']}\n\n{c['summary']}\n\n"+'\n\n'.join(c['paragraphs'])+f"\n\n> 教學提醒：{c['focus']}\n\n證據卡：{', '.join(c['cards'])}\n"
 write(f"wiki/{c['id']}.md",body)
 idx+=f"- [{c['title']}]({c['id']}.md) — {c['summary']}\n"
write('wiki/index.md',idx+'\n來源見 `../source_manifest.json`；整理紀錄見 `log.md`。\n')
write('wiki/log.md',"""# Ingest 紀錄

日期：2026-11-12（Asia/Taipei）

- 取得來源：六個可辨識來源網址；其中 S02、S03 只依公開摘要／書籍章節 Summary，其餘依公開網頁全文。
- Ingest 內容：逐篇建立 `raw/S01.md`～`raw/S06.md`（來源欄位、中文重點、可見範圍、限制）；不是全文鏡像。
- 索引化：建立 12 張 `cards/E01.md`～`cards/E12.md` 證據卡，標示來源 ID 與位置。
- 合成知識：把證據卡對應到 6 篇 Wiki 章節，每篇有來源與教學誤解提醒。
- 衝突處理：涉及能隙數值時統一採 S04 Table 1（Si 1.12 eV、4H-SiC 3.26 eV），不在不同研究間混用數字。
- 守門：查不到的結論不補寫；付費全文不假裝已下載，超出來源可見範圍即註記。
""")

# slide model: each slide includes source and evidence identifiers
slides=[
 {'no':1,'kicker':'INTRO / 01','title':'碳化矽 SiC','subtitle':'從材料、長晶、磊晶到功率晶片','kind':'cover','bits':['13 頁互動式教學','適合沒有半導體背景的讀者'],'e':['E01','E06']},
 {'no':2,'kicker':'START / 02','title':'今天會學到什麼？','subtitle':'先懂材料，再把製程串起來','kind':'goals','bits':['01 了解 SiC 為何能做高功率元件','02 區分長晶、基板與磊晶','03 看懂 MOSFET 與實際應用'],'e':['E01','E06']},
 {'no':3,'kicker':'MATERIAL / 03','title':'SiC 是什麼？','subtitle':'矽 + 碳，常見功率材料：4H-SiC','kind':'three','bits':['SiC 是半導體材料，不是一種元件','4H-SiC 是重要的晶體結構型態','功率半導體像是控制電流的高速開關'],'e':['E01','E12']},
 {'no':4,'kicker':'PHYSICS / 04','title':'寬能隙，真正代表什麼？','subtitle':'與高耐壓設計有關；不是說電子一定比較快','kind':'band','bits':['Si 能隙 ≈ 1.12 eV','4H-SiC 能隙 ≈ 3.26 eV','不同來源與條件可能報告略有差異'],'e':['E02','E03']},
 {'no':5,'kicker':'DESIGN / 05','title':'材料特性，如何影響產品？','subtitle':'性能要看整個元件和系統，不只看材料','kind':'features','bits':['高崩潰電場 → 高耐壓設計空間','較佳熱特性 → 有利散熱設計','低損失潛力 → 可提升系統效率','仍須考慮控制、封裝與缺陷'],'e':['E01','E03','E08']},
 {'no':6,'kicker':'MYTH / 06','title':'常見迷思：SiC 電子跑得比較快？','subtitle':'不一定。要分清楚能隙、遷移率和效率。','kind':'myth','bits':['能隙：電子能帶間的能量差','遷移率：載子受電場影響的移動能力','元件效率：導通、切換與系統損失共同決定'],'e':['E02','E03','E08']},
 {'no':7,'kicker':'PROCESS / 07','title':'從粉末到功率晶片','subtitle':'四個階段，各有不同任務','kind':'flow','bits':['單晶長晶 (PVT)','晶圓切磨與基板','磊晶 (常見 CVD)','MOSFET 元件製程'],'e':['E04','E05','E06']},
 {'no':8,'kicker':'GROWTH / 08','title':'長晶：先做出高品質基板','subtitle':'單晶長晶 ≠ 直接做出電子元件','kind':'growth','bits':['目標：製作大塊且品質受控的 SiC 單晶','常見方法：PVT 物理氣相傳輸','成長後還須切片、研磨與拋光'],'e':['E04']},
 {'no':9,'kicker':'EPITAXY / 09','title':'磊晶：在基板上設計功能層','subtitle':'厚度、摻雜、缺陷，都是核心品質','kind':'epi','bits':['CVD 在基板表面形成晶體層','厚度與摻雜可依元件需求設計','基板缺陷與製程條件會影響磊晶品質'],'e':['E05','E07','E11']},
 {'no':10,'kicker':'COMPARE / 10','title':'長晶 vs 磊晶，一次分清楚','subtitle':'兩者串接，功能不同','kind':'compare','bits':['長晶：做出塊材 → 加工成基板','磊晶：在基板上成長受控功能層','元件製程：把晶圓做成可開關的電路元件'],'e':['E04','E05','E11']},
 {'no':11,'kicker':'DEVICE / 11','title':'SiC MOSFET 的機會與挑戰','subtitle':'材料潛力，需要精密製程才能實現','kind':'device','bits':['機會：降低導通／切換損失','挑戰：SiC/氧化層界面通道遷移率','挑戰：磊晶缺陷與長期可靠度'],'e':['E07','E08']},
 {'no':12,'kicker':'APPLICATION / 12','title':'SiC 用在哪裡？','subtitle':'重要，但不是所有應用都必然最佳','kind':'applications','bits':['電動車：驅動與電力轉換','太陽能：逆變器','評估條件：效率、成本、散熱、可靠度'],'e':['E09','E10']},
 {'no':13,'kicker':'RECAP / 13','title':'最後用 3 題確認理解','subtitle':'帶著這三句話回去看 Wiki','kind':'quiz','bits':['Q1：寬能隙＝高遷移率嗎？ → 不等於','Q2：長晶的主要目的？ → 製作單晶基板材料','Q3：磊晶用來控制什麼？ → 功能層厚度、摻雜與品質'],'e':['E02','E03','E04','E05']}
]
for s in slides:s['sources']=sorted({ref for eid in s['e'] for x in evidence if x['id']==eid for ref in x['sources']})
write('slides/slide_manifest.json',json.dumps(slides,ensure_ascii=False,indent=2))
write('slides/outline.md','# 教學簡報大綱｜先產生證據卡與大綱，再渲染 HTML\n\n'+'\n'.join(f"{s['no']:02}. {s['title']}（證據卡：{', '.join(s['e'])}；原始文獻：{', '.join(s['sources'])}）" for s in slides)+'\n\n檢核：13 頁；每頁有對應證據卡；不添加 Wiki 尚未支持的新主張。\n')
for s in slides:
 write(f"slides/drafts/{s['no']:02}.md",f"# 第 {s['no']} 頁｜{s['title']}\n\n{s['subtitle']}\n\n"+'\n'.join('- '+b for b in s['bits'])+f"\n\n證據：{', '.join(s['e'])}\n來源：{', '.join(s['sources'])}\n")

source_url={s['id']:s['url'] for s in sources}
def cite_html(ids,small=False):
 cl='citations small' if small else 'citations'
 return f'<div class="{cl}"><span>文獻依據</span> '+''.join(f'<a href="{html.escape(source_url[s])}" title="查看 {s} 的原始網頁" target="_blank" rel="noopener noreferrer">{s}↗</a>' for s in ids)+'</div>'

# Inline vector diagrams, optimized for offline display
illustrations={
'band':'''<div class="band-visual"><div class="band-row"><div class="band-label">Si <small>矽</small></div><div class="band-bar si" style="--bar:.343"><strong>1.12</strong><span>eV</span></div></div><div class="band-row"><div class="band-label">4H-SiC <small>碳化矽</small></div><div class="band-bar sic" style="--bar:1"><strong>3.26</strong><span>eV</span></div></div><div class="note">以上是能隙比較（室溫參考值），不是電子移動速度圖。</div></div>''',
'flow':'''<div class="flow-visual"><div class="stage"><span>01</span><b>長晶</b><small>PVT</small></div><div class="arr">→</div><div class="stage"><span>02</span><b>基板</b><small>切片・拋光</small></div><div class="arr">→</div><div class="stage"><span>03</span><b>磊晶</b><small>CVD</small></div><div class="arr">→</div><div class="stage"><span>04</span><b>元件</b><small>MOSFET</small></div></div>''',
'epi':'''<div class="wafer-visual"><div class="wafer-top">功能性磊晶層 <small>可調整厚度 / 摻雜</small></div><div class="wafer-bottom">4H-SiC 單晶基板 <small>支撐與晶格基礎</small></div><span class="wafer-caption">示意圖，非實際厚度比例</span></div>''',
'growth':'''<div class="growth-visual"><div class="crystal"><i></i><i></i><i></i><i></i></div><div class="growth-arrow">⇢</div><div class="wafer-discs"><span></span><span></span><span></span></div><div class="growth-label"><span>單晶塊材</span><span>加工後的晶圓</span></div></div>'''
}

def content(s):
 k=s['kind'];bits=s['bits']
 if k=='cover':return '<div class="cover-line"><div class="hero-mark">Si<span>C</span></div><p>製程有順序，知識有出處。<br>用 13 頁建立最基本的半導體材料概念。</p></div>'
 if k=='goals':return '<div class="grid-3">'+''.join(f'<div class="idea"><span class="big-index">{i+1:02}</span><p>{html.escape(x[3:])}</p></div>' for i,x in enumerate(bits))+'</div>'
 if k in ('three','features','myth','device','applications'):
  sym={'three':['◇','4H','↔'],'features':['⚡','♨','↗','◉'],'myth':['E','μ','η'],'device':['✓','!','!'],'applications':['EV','☀','⚖']}[k]
  return '<div class="tile-grid '+('tiles-4' if len(bits)==4 else '')+'">'+''.join(f'<div class="tile"><span>{sym[i]}</span><p>{html.escape(v)}</p></div>' for i,v in enumerate(bits))+'</div>'
 if k=='band':return illustrations['band']
 if k=='flow':return illustrations['flow']
 if k=='growth':return illustrations['growth']+'<p class="below">'+'　／　'.join(map(html.escape,bits))+'</p>'
 if k=='epi':return illustrations['epi']+'<p class="below">'+'　／　'.join(map(html.escape,bits))+'</p>'
 if k=='compare':return '<div class="comparison"><div class="compare-col"><span>01</span><h3>長晶</h3><p>先製作單晶塊材，<br>加工成晶圓基板</p></div><div class="compare-mid">+</div><div class="compare-col"><span>02</span><h3>磊晶</h3><p>在基板上成長<br>厚度、摻雜受控的層</p></div></div><div class="note">之後還需要元件製程，才能做成 MOSFET。</div>'
 if k=='quiz':return '<div class="quiz-rows">'+''.join(f'<details><summary>{html.escape(v.split(" → ")[0])}<b>點擊看答案 ＋</b></summary><p>{html.escape(v.split(" → ")[1])}</p></details>' for v in bits)+'</div>'
 return ''.join(f'<p>{html.escape(x)}</p>' for x in bits)

deck_css=r'''
:root{--bg:#071422;--panel:#102437;--text:#f3fbff;--muted:#a8bfd2;--aqua:#71e7da;--lime:#c7f497;--edge:rgba(138,216,227,.22)}*{box-sizing:border-box}html,body{margin:0;min-height:100%;background:var(--bg);color:var(--text);font-family:"Noto Sans TC","Microsoft JhengHei","PingFang TC",system-ui,sans-serif}a{color:inherit}button{font:inherit}.deck{min-height:100vh;min-height:100dvh;display:flex;align-items:center;justify-content:center;padding:24px 28px 92px;background:radial-gradient(circle at 15% 17%,#133c4a 0,transparent 43%),radial-gradient(circle at 90% 80%,#152b4c 0,transparent 36%),var(--bg)}.slide{display:none;width:min(1180px,100%);min-height:min(670px,calc(100dvh - 115px));padding:48px 64px 44px;position:relative;border:1px solid var(--edge);border-radius:24px;box-shadow:0 45px 130px #0005;background:linear-gradient(155deg,rgba(16,39,58,.96),rgba(7,19,33,.97));overflow:hidden}.slide.active{display:flex;flex-direction:column}.slide:after{content:"";position:absolute;right:-90px;top:-145px;width:400px;height:400px;border:1px solid #86e7d516;border-radius:50%;pointer-events:none}.kicker{font-size:13px;letter-spacing:.28em;font-weight:800;color:var(--aqua)}.slide h1{font-size:clamp(32px,4.5vw,65px);line-height:1.23;letter-spacing:-.035em;margin:22px 0 14px;max-width:980px}.slide h2{color:var(--muted);font-size:clamp(17px,2vw,25px);font-weight:450;margin:0 0 26px}.slide-body{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}.foot{border-top:1px solid var(--edge);padding-top:16px;display:flex;justify-content:space-between;align-items:flex-end;gap:16px;font-size:12px;color:var(--muted)}.citations{display:flex;align-items:center;gap:7px;flex-wrap:wrap}.citations a{font-size:12px;text-decoration:none;border:1px solid var(--edge);border-radius:20px;padding:4px 9px;color:var(--aqua)}.citations a:hover{background:#23545a}.page-no{font-weight:800;font-variant-numeric:tabular-nums;white-space:nowrap}.controls{position:fixed;z-index:5;left:50%;bottom:15px;transform:translateX(-50%);width:min(640px,calc(100vw - 28px));border-radius:20px;display:flex;gap:10px;align-items:center;padding:10px 12px;background:#0c2335ee;border:1px solid var(--edge);box-shadow:0 15px 50px #0008;backdrop-filter:blur(18px)}.controls button{padding:9px 13px;border:1px solid #427081;border-radius:11px;background:#183b4d;color:white;cursor:pointer}.controls button:hover{background:#286177}.controls button:disabled{opacity:.4;cursor:not-allowed}.controls .nav-label{font-size:13px;color:var(--muted);white-space:nowrap}.bar{height:6px;flex:1;background:#2c475a;border-radius:20px;overflow:hidden;min-width:40px}.bar i{display:block;width:7.69%;height:100%;background:var(--aqua);border-radius:20px;transition:width .25s}.cover-line{display:flex;align-items:center;gap:44px}.hero-mark{font-size:clamp(92px,16vw,190px);font-weight:900;letter-spacing:-.09em;line-height:1;color:var(--aqua)}.hero-mark span{color:var(--lime)}.cover-line p{font-size:clamp(21px,3vw,33px);line-height:1.65;color:#d6e4ec}.grid-3{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.idea,.tile{border:1px solid var(--edge);border-radius:18px;background:linear-gradient(155deg,#183749dd,#11283bbb);padding:24px}.idea{min-height:245px;display:flex;flex-direction:column;justify-content:space-between}.big-index{font-size:56px;line-height:1;color:var(--aqua);font-weight:900}.idea p{font-size:23px;line-height:1.5}.tile-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:15px}.tile-grid.tiles-4{grid-template-columns:repeat(2,1fr)}.tile{min-height:155px}.tile span{font-size:32px;color:var(--aqua);font-weight:850}.tile p{font-size:21px;line-height:1.5;margin:19px 0 0}.band-visual{padding:12px 0}.band-row{display:grid;grid-template-columns:180px 1fr;align-items:center;gap:24px;margin:24px 0}.band-label{font-size:25px;font-weight:800}.band-label small{display:block;font-size:14px;color:var(--muted);font-weight:400}.band-bar{width:calc(var(--bar) * 100%);height:100px;border-radius:14px;padding:18px 24px;display:flex;align-items:baseline;gap:8px;color:#061622;min-width:115px}.band-bar strong{font-size:45px}.band-bar span{font-size:16px}.band-bar.si{background:linear-gradient(90deg,#9dbed9,#d4e6ee)}.band-bar.sic{background:linear-gradient(90deg,#6ee0d2,#bff08d)}.note{color:var(--muted);margin-top:18px;font-size:15px;line-height:1.6}.flow-visual{display:flex;align-items:stretch;justify-content:center;gap:6px}.stage{width:23%;min-height:190px;padding:18px 12px;border:1px solid #73d8dd70;background:#123546;border-radius:16px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:15px;text-align:center}.stage span{color:var(--aqua);font-weight:800}.stage b{font-size:27px}.stage small{color:var(--muted);font-size:14px}.arr{font-size:30px;color:var(--lime);align-self:center}.wafer-visual{max-width:720px;width:100%;margin:auto}.wafer-top{border:2px solid #d0fba3;background:linear-gradient(90deg,#b0f19a,#76d5b5);padding:25px;color:#0b3330;font-weight:800;font-size:25px;border-radius:16px 16px 0 0;text-align:center}.wafer-bottom{background:linear-gradient(125deg,#23658a,#27506a);border:2px solid #79bfdb;padding:55px 12px;border-radius:0 0 16px 16px;font-size:27px;font-weight:800;text-align:center}.wafer-visual small{display:block;font-size:14px;font-weight:450;margin-top:8px}.wafer-caption{display:block;text-align:center;color:var(--muted);font-size:13px;margin-top:12px}.below{margin-top:18px;color:#c1d6df;font-size:16px;text-align:center}.growth-visual{display:grid;grid-template-columns:1fr .2fr 1fr;align-items:center;position:relative;max-width:740px;width:100%;margin:auto;padding-bottom:35px}.crystal{height:205px;width:205px;margin:auto;clip-path:polygon(25% 0,75% 0,96% 23%,96% 78%,75% 100%,25% 100%,4% 78%,4% 23%);background:linear-gradient(135deg,#89d7c2,#236c81);display:flex;align-items:center;justify-content:center;gap:10px;box-shadow:inset 0 0 0 10px #ffffff20}.crystal i{display:block;height:100%;width:6px;background:#ffffff22;transform:skew(17deg)}.growth-arrow{text-align:center;color:var(--lime);font-size:58px}.wafer-discs{height:215px;position:relative}.wafer-discs span{position:absolute;width:175px;height:69px;border-radius:50%;background:#76d6dc;border:5px solid #c9fdf3;left:50%;transform:translateX(-50%)}.wafer-discs span:nth-child(1){top:36px}.wafer-discs span:nth-child(2){top:76px}.wafer-discs span:nth-child(3){top:116px}.growth-label{grid-column:1/4;display:flex;justify-content:space-around;color:var(--muted);font-size:17px}.comparison{display:flex;align-items:center;gap:22px}.compare-col{flex:1;min-height:255px;padding:30px;border:1px solid var(--edge);border-radius:18px;background:#15364a}.compare-col span{color:var(--aqua);font-weight:800}.compare-col h3{font-size:45px;margin:20px 0}.compare-col p{font-size:23px;line-height:1.45}.compare-mid{font-size:50px;color:var(--lime)}.quiz-rows{display:grid;gap:14px}.quiz-rows details{border:1px solid var(--edge);background:#18394b;border-radius:15px;padding:20px 22px}.quiz-rows summary{cursor:pointer;display:flex;justify-content:space-between;gap:8px;font-size:22px;font-weight:650}.quiz-rows summary b{font-size:13px;align-self:center;color:var(--aqua);white-space:nowrap}.quiz-rows details p{color:var(--lime);font-size:20px;margin:14px 0 0}.print-only{display:none}
@media(max-width:800px){.deck{padding:10px 10px 88px;align-items:stretch}.slide{min-height:calc(100dvh - 105px);padding:26px 21px 20px;border-radius:14px}.slide h1{font-size:clamp(26px,7vw,44px)}.slide h2{font-size:17px}.tile p,.idea p{font-size:17px}.tile{padding:17px;min-height:120px}.grid-3{gap:8px}.idea{padding:14px;min-height:180px}.big-index{font-size:35px}.cover-line{flex-direction:column;gap:12px;align-items:flex-start}.cover-line p{font-size:22px}.hero-mark{font-size:108px}.band-row{grid-template-columns:85px 1fr;gap:10px}.band-label{font-size:17px}.band-bar{height:70px;padding:10px}.band-bar strong{font-size:29px}.stage{width:24%;padding:8px 4px;min-height:140px}.stage b{font-size:17px}.stage small{font-size:11px}.arr{font-size:14px}.wafer-top{font-size:19px}.wafer-bottom{font-size:21px;padding:36px 6px}.growth-visual{transform:scale(.82)}.compare-col{padding:15px;min-height:230px}.compare-col h3{font-size:26px}.compare-col p{font-size:17px}.quiz-rows summary{font-size:17px}.quiz-rows summary b{font-size:11px}.foot{font-size:10px}.controls .nav-label{display:none}}
@media(max-width:430px){.tile-grid,.tile-grid.tiles-4{grid-template-columns:1fr 1fr;gap:9px}.tile{min-height:100px}.tile span{font-size:21px}.tile p{font-size:14px;margin-top:12px}.grid-3{grid-template-columns:1fr}.idea{min-height:70px;display:flex;flex-direction:row;align-items:center;padding:12px}.idea p{margin:0;font-size:15px}.big-index{font-size:26px}.flow-visual{flex-wrap:wrap}.stage{width:40%;min-height:110px}.stage b{font-size:17px}.arr{display:none}}
@media print{@page{size:landscape;margin:0}html,body{background:white!important}.deck{display:block;padding:0!important;background:white!important}.slide,.slide.active{display:flex!important;width:100vw;height:100vh;min-height:100vh;border:0;border-radius:0;box-shadow:none;page-break-after:always;break-after:page;print-color-adjust:exact;-webkit-print-color-adjust:exact;padding:42px 55px}.controls{display:none!important}}
'''

# Fixed-format print rules: prevents splitting a single HTML slide across two PDF pages.
print_override=r"""
@page{size:1280px 720px;margin:0}
@media print{
 html,body{width:1280px!important;height:auto!important;margin:0!important;padding:0!important;background:#071422!important}
 .deck{display:block!important;width:1280px!important;min-height:0!important;height:auto!important;margin:0!important;padding:0!important;background:#071422!important}
 .slide,.slide.active{display:block!important;width:1280px!important;height:720px!important;min-height:720px!important;max-height:720px!important;overflow:hidden!important;position:relative!important;padding:35px 60px!important;border-radius:0!important;border:0!important;break-after:page!important;page-break-after:always!important;background:#0b1d2d!important;box-shadow:none!important}
 .slide h1{font-size:52px!important;margin:22px 0 12px!important;line-height:1.22!important}
 .slide h2{font-size:22px!important;margin-bottom:18px!important}
 .slide-body{display:block!important;height:auto!important;min-height:0!important;max-height:480px!important;overflow:hidden!important}
 .foot{position:absolute!important;bottom:32px!important;left:60px!important;right:60px!important;width:auto!important;margin:0!important;background:#0b1d2d!important}
 .tile{min-height:150px!important;padding:19px!important}
 .tile p{font-size:20px!important;margin:10px 0 0!important}
 .idea{min-height:230px!important}
 .quiz-rows details{padding:15px 22px!important}
 .quiz-rows summary{font-size:21px!important}
 .cover-line{padding:70px 0!important}
 .hero-mark{font-size:150px!important}
 .controls{display:none!important}
}
"""
slides_html=[]
for s in slides:
 body=content(s)
 slides_html.append(f'''<section class="slide{' active' if s['no']==1 else ''}" data-slide="{s['no']}" aria-label="第{s['no']}頁 {html.escape(s['title'])}"><div class="kicker">{html.escape(s['kicker'])}</div><h1>{html.escape(s['title'])}</h1><h2>{html.escape(s['subtitle'])}</h2><div class="slide-body">{body}</div><footer class="foot">{cite_html(s['sources'])}<span class="page-no">{s['no']:02} / 13</span></footer></section>''')
write('slides/index.html',f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="SiC 功率半導體教學簡報：Wiki 知識庫引用的互動式 13 頁 HTML"><title>SiC 教學簡報｜從材料到晶片</title><style>{deck_css}{print_override}</style></head><body>
<main class="deck" id="deck">{''.join(slides_html)}</main>
<nav class="controls" aria-label="簡報操作"><button id="prev" type="button" aria-label="上一頁">← 上一頁</button><div class="bar" aria-hidden="true"><i id="progress"></i></div><span class="nav-label" id="pageLabel">01 / 13</span><button id="next" type="button" aria-label="下一頁">下一頁 →</button><button id="print" title="列印或另存 PDF" type="button">⎙</button><a href="../wiki/index.html" style="text-decoration:none;font-size:12px;color:#71e7da" title="查看 Wiki">Wiki↗</a></nav>
<script>
(()=>{{let current=0;const slides=[...document.querySelectorAll('.slide')],max=slides.length;const p=document.querySelector('#prev'),n=document.querySelector('#next'),label=document.querySelector('#pageLabel'),bar=document.querySelector('#progress');function go(x){{current=Math.max(0,Math.min(max-1,x));slides.forEach((s,i)=>{{s.classList.toggle('active',i===current);s.setAttribute('aria-hidden',String(i!==current));}});p.disabled=current===0;n.disabled=current===max-1;label.textContent=String(current+1).padStart(2,'0')+' / '+max;bar.style.width=((current+1)/max*100)+'%';history.replaceState(null,'','#'+(current+1));}}p.addEventListener('click',()=>go(current-1));n.addEventListener('click',()=>go(current+1));document.querySelector('#print').addEventListener('click',()=>window.print());document.addEventListener('keydown',e=>{{if(['ArrowRight','PageDown',' '].includes(e.key)&&e.target.tagName!=='SUMMARY'){{e.preventDefault();go(current+1);}}if(['ArrowLeft','PageUp'].includes(e.key)){{e.preventDefault();go(current-1);}}if(e.key==='Home')go(0);if(e.key==='End')go(max-1);}});let touchX=null;document.addEventListener('touchstart',e=>{{touchX=e.changedTouches[0].clientX;}},{{passive:true}});document.addEventListener('touchend',e=>{{if(touchX===null)return;let dx=e.changedTouches[0].clientX-touchX;if(Math.abs(dx)>90)go(current+(dx<0?1:-1));touchX=null;}},{{passive:true}});window.addEventListener('hashchange',()=>{{let id=parseInt(location.hash.slice(1),10);if(!isNaN(id))go(id-1);}});go(Math.max(0,(parseInt(location.hash.slice(1),10)||1)-1));}})();
</script></body></html>''')

# interactive local Wiki, all content embedded; supports search without remote APIs
wcss=r'''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#eaf4f7;background:#081625;font-family:"Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif}a{color:#79e8dc}header{padding:32px max(24px,calc((100vw - 1230px)/2));border-bottom:1px solid #254455;background:linear-gradient(110deg,#0e3341,#0b1e30)}header .top{font-size:12px;letter-spacing:.23em;color:#72e4d1;font-weight:900}header h1{font-size:clamp(30px,4vw,52px);margin:14px 0}header p{color:#b9ccd9;font-size:17px;max-width:800px;line-height:1.8}.navlinks{display:flex;gap:13px;flex-wrap:wrap}.navlinks a{padding:9px 14px;background:#174454;border-radius:10px;text-decoration:none;font-weight:700}.page{display:grid;grid-template-columns:265px 1fr;gap:34px;max-width:1230px;margin:auto;padding:25px 24px 70px}.side{position:sticky;top:20px;align-self:start;background:#10283a;border:1px solid #27485a;border-radius:14px;padding:19px}.side label{font-size:12px;letter-spacing:.1em;color:#9bc5d0}.side input{width:100%;margin:9px 0 17px;background:#081d2b;border:1px solid #407180;border-radius:8px;padding:12px;color:white;font-size:14px}.side a{display:block;padding:12px 8px;border-radius:8px;text-decoration:none;color:#d2e6eb;font-size:14px}.side a:hover{background:#1d4655}.content{min-width:0}.summary{border:1px solid #2b5963;background:#143b46;border-radius:13px;padding:21px;color:#ccedee;line-height:1.8;margin-bottom:24px}.chapter{border:1px solid #28485a;background:#10283a;border-radius:15px;padding:32px 35px;margin-bottom:23px;scroll-margin-top:22px}.eyebrow{font-size:11px;color:#76e9d3;letter-spacing:.2em;font-weight:900}.chapter h2{font-size:29px;margin:12px 0}.chapter .lead{font-size:18px;color:#afd4dd}.chapter p{line-height:1.9;font-size:16px;color:#d2e2eb}.focus{padding:12px 17px;border-left:3px solid #bee992;background:#1b3840;color:#d9edcc;margin-top:21px;border-radius:0 8px 8px 0}.proof{margin-top:24px;border-top:1px solid #2a4b5c;padding-top:16px;display:flex;align-items:center;gap:8px;flex-wrap:wrap}.proof span{color:#8fb3c5;font-size:13px}.proof a,.source-code{font-size:12px;background:#163e4d;text-decoration:none;color:#86e4db;border:1px solid #356b73;border-radius:7px;padding:5px 8px}.source-list{border:1px solid #27495a;border-radius:15px;padding:30px;background:#10293b}.source-item{margin-top:14px;padding:18px;border:1px solid #2b4859;background:#0d2333;border-radius:9px}.source-item h3{margin:10px 0 4px;font-size:16px}.source-item p{font-size:13px;color:#a5c5d0;line-height:1.7}.source-item a{font-size:13px}.source-item ul{padding-left:23px;color:#c4dbe5;font-size:14px;line-height:1.8}.nohits{display:none;color:#f7c992;background:#392c20;padding:13px;border-radius:9px;margin-bottom:18px}footer{font-size:13px;color:#9cb7c5;margin:30px 0}mark{background:#bcebb0;color:#071923;border-radius:3px}@media(max-width:820px){.page{grid-template-columns:1fr;padding:15px}.side{position:static}.chapter{padding:20px}.navlinks a{font-size:13px}header{padding:26px 19px}}'''
chapter_html=''
for c in chapters:
 source_ids=sorted({sid for x in evidence if x['id'] in c['cards'] for sid in x['sources']})
 chapter_html+=f'''<article class="chapter" id="{c['id']}" data-search="{html.escape(' '.join([c['title'],c['summary']]+c['paragraphs']+[c['focus']]))}"><div class="eyebrow">LEARNING NOTE / {c['id'].upper()}</div><h2>{html.escape(c['title'])}</h2><p class="lead">{html.escape(c['summary'])}</p>'''+''.join(f'<p>{html.escape(p)}</p>' for p in c['paragraphs'])+f'<div class="focus"><b>需要記住：</b>{html.escape(c["focus"])}</div><div class="proof"><span>對應證據卡</span> '+''.join(f'<a href="../cards/{k}.md" title="{k} 原始證據紀錄">{k}</a>' for k in c['cards'])+f'<span style="margin-left:10px">原始資料</span>'+''.join(f'<a href="{source_url[k]}" target="_blank" rel="noopener">{k}↗</a>' for k in source_ids)+'</div></article>'
source_html=''
for s in sources:
 source_html+=f'''<div class="source-item"><span class="source-code">{s['id']}</span><h3>{html.escape(s['title'])}</h3><p>{html.escape(s['author'])} · {html.escape(s['year'])} · {html.escape(s['access'])}</p><ul>'''+''.join(f'<li>{html.escape(k)}</li>' for k in s['keypoints'])+f'''</ul><p><b>範圍註記：</b>{html.escape(s['limits'])}</p><a href="{html.escape(s['url'])}" target="_blank" rel="noopener noreferrer">查看原始資料 ↗</a> · <a href="../raw/{s['id']}.md">查看 Ingest 記錄 ↗</a></div>'''
write('wiki/index.html',f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SiC LLM Wiki｜來源可追溯的學習筆記</title><style>{wcss}</style></head><body><header><div class="top">LLM WIKI / MATERIAL SCIENCE</div><h1>從材料到晶片：SiC 知識庫</h1><p>六篇可追溯來源，十二張證據卡，六個主題章節。內容以繁體中文重新組織；不是將網路文章整篇複製，也不是無來源的百科摘要。</p><div class="navlinks"><a href="../index.html">專案首頁</a><a href="../slides/index.html">開始教學簡報 ↗</a><a href="#sources">六篇來源列表 ↓</a></div></header><div class="page"><aside class="side"><label for="search">SEARCH WIKI / 搜尋章節</label><input id="search" type="search" placeholder="例如：磊晶、遷移率、缺陷" aria-label="搜尋 Wiki"><nav>'''+''.join(f'<a href="#{c["id"]}">{html.escape(c["title"])}</a>' for c in chapters)+'''<a href="#sources">來源總表</a></nav></aside><main class="content"><div class="summary"><strong>閱讀方法</strong>：先依序讀「材料 → 長晶 → 磊晶 → MOSFET → 應用」。每個章節尾端都有證據卡 ID 與原始資料 ID，點擊可查閱；Wiki 所載能隙數字統一採 S04 的 Table 1。</div><div class="nohits" id="nohits">找不到符合關鍵字的章節，請換一個詞試試。</div>'''+chapter_html+f'''<section class="source-list" id="sources"><div class="eyebrow">BIBLIOGRAPHY</div><h2>6 篇來源與 ingest 範圍</h2>{source_html}</section><footer>整理日期：2026-11-12。本站不依賴網路 API 或遠端字型；外部學術來源連結仍需網路開啟。</footer></main></div><script>const q=document.getElementById('search'),all=[...document.querySelectorAll('.chapter')];q.addEventListener('input',()=>{{const word=q.value.trim().toLocaleLowerCase();let n=0;for(const c of all){{let hit=c.dataset.search.toLocaleLowerCase().includes(word);c.hidden=!hit;if(hit)n++;}}document.getElementById('nohits').style.display=n?'none':'block';}});</script></body></html>''')

home_style='''body{margin:0;min-height:100vh;display:grid;place-items:center;background:radial-gradient(circle at 18% 20%,#19464c,#071423 55%);font-family:system-ui,"Microsoft JhengHei",sans-serif;color:white;padding:20px}.wrap{max-width:920px;width:100%}.ey{letter-spacing:.2em;color:#78e6d7;font-size:12px;font-weight:850}h1{font-size:clamp(35px,5vw,62px);letter-spacing:-.03em;margin:20px 0}p{font-size:17px;line-height:1.75;color:#bdd6e1}.choices{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:39px}.choice{border:1px solid #39727c;border-radius:18px;background:#123143;padding:30px;color:#e9fcfa;text-decoration:none}.choice span{color:#83dfdb;font-size:13px}.choice h2{font-size:30px;margin:14px 0}.choice p{font-size:15px}.choice:hover{background:#1d4653}.bottom{margin-top:30px;color:#87a7b5;font-size:13px}@media(max-width:620px){.choices{grid-template-columns:1fr}}'''
write('index.html',f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SiC LLM Wiki × HTML 教學簡報</title><style>{home_style}</style></head><body><main class="wrap"><div class="ey">SIC · EVIDENCE-BASED LEARNING</div><h1>從材料到晶片<br>碳化矽 SiC 功率半導體入門</h1><p>根據 6 篇外部學術／官方資料建立的知識庫，再利用 12 張證據卡產出可瀏覽的 13 頁 HTML 簡報。流程採取先蒐集、檢查來源，再撰寫、再驗證的 Graph + Loop。</p><div class="choices"><a class="choice" href="wiki/index.html"><span>READ / KNOWLEDGE BASE</span><h2>01　LLM Wiki</h2><p>六個入門章節、六篇來源、全文搜尋與來源連結。</p></a><a class="choice" href="slides/index.html"><span>PLAY / TEACHING DECK</span><h2>02　HTML 簡報</h2><p>13 頁互動、鍵盤翻頁、每頁註明學術依據。</p></a></div><div class="bottom">此為靜態離線可用網站。老師要求的 GitHub Pages 公開網址需在部署後填入繳交文件。</div></main></body></html>''')

write('AGENTS.md',"""# AGENTS.md — SiC Wiki & HTML Deck 的工作規範

## 先討論後生成（需求定義）
- 讀者：沒有 SiC 背景的同學。語言：繁體中文。
- 來源：至少 5 篇真實文獻／官方來源；這版 ingest 6 篇；只使用可讀到的公開部分。
- Wiki：章節與每個有事實性的主要觀點須對應來源 ID／證據卡。
- 最終成品：可直接由瀏覽器開啟的靜態 HTML Wiki 與 8–15 頁教學簡報，GitHub Pages 可部署。
- 內容範圍：定義→物性→長晶→磊晶→MOSFET→應用；不加入沒有來源支持的商業預測。
- 矛盾處理：將不同論文的數據標為不同來源，不混搭；本作業能隙值統一按 S04 Table 1。
- AI 使用：AI 協助規劃與改寫，需保留來源與檢查紀錄，不宣稱 AI 幫你完成了未做的人工工作。

## 節點權限 / 規則
1. ingest 節點只能讀 source_manifest 與原始頁面可見內容，輸出 raw；不得假裝已取得付費全文。
2. evidence 節點只能讀 raw，輸出證據卡；不得加入新事實。
3. outline 節點只能讀 wiki + cards，輸出 8–15 頁大綱；需頁頁有對應 evidence。
4. draft 節點只能讀 outline + cards，逐頁寫稿；超出來源的資訊不寫。
5. render 節點只能按已審核逐頁稿排版，不自行改寫科學結論。
6. check 節點只輸出報告；退回最接近問題的節點修正，不修改其他合格頁。

## Loop（最多 3 輪）
- 觸發：新來源入庫、簡報更新、或檢查不通過。
- 完成標準：>=5 個 ingest、>=8 且 <=15 頁、每頁 source ID 真實存在、連結可導航、無文字溢出。
- 停止條件：全部檢查通過，或修正達 3 輪，或支持資料不足。
- 程式檢查與文意審核分開；AI 審核建議在另一個對話只看來源和成品。
""")
write('.agents/workflows/topic-slides.md',"""# /topic-slides — SiC Wiki → HTML 簡報

輸入：`source_manifest.json` 與 `raw/`，主題為 SiC。完成標準見 `AGENTS.md`。

1. **Source**：來源可訪問、metadata 完整；來源不足 5 → STOP。
2. **Ingest**：每篇生成 `raw/Sxx.md`，標明只讀到公開摘要／全文的哪一部分；缺來源 → 退回 Source。
3. **Evidence**：整理 `cards/E*.md`，每張有可追溯來源 ID；卡片不足 → 退回 Ingest。
4. **Wiki**：彙整 `wiki/*.md` 與 `wiki/index.html`；有超出來源的說法 → 退回 Evidence。
5. **Outline**：產生 `slides/outline.md`，8–15 頁且標明 evidence ID；覆蓋不夠 → 退回 Evidence。
6. **Draft loop**：逐頁草稿 `slides/drafts/`；來源或長度不合格 → 只修有問題頁（最多 2 次）。
7. **Render**：將已通過稿做成 `slides/index.html`；渲染階段不重新撰寫技術結論。
8. **QA gate**：執行 `python qa/check.py` + Chromium 實際翻頁 / overflow；版型錯退回 Render，內容錯退回 Draft；最多 3 輪。
9. **Deliver**：`report.md` + `submission.txt`；公開網址需使用者在 GitHub Pages 部署後補上。

每一步檔案都可查、可重跑；不作無限制自我迴圈。
""")
write('workflow_graph.mmd',"""flowchart LR
    A[確認需求] --> B[蒐集六篇來源]
    B --> C{來源數 ≥ 5?}
    C -- 否 --> X[停止：缺來源]
    C -- 是 --> D[Ingest raw]
    D --> E[證據卡 Evidence]
    E --> F[Wiki 章節]
    F --> G{覆蓋率／來源檢查}
    G -- 不足 --> E
    G -- 合格 --> H[13 頁大綱]
    H --> I[逐頁草稿]
    I --> J{忠實度／字數檢查}
    J -- 不合格，僅修該頁 --> I
    J -- 合格 --> K[渲染 HTML]
    K --> L{程式及瀏覽器檢查}
    L -- 排版錯 --> K
    L -- 內容錯 --> I
    L -- 全過 --> M[產出 report / 交件]
    J -. 修正最多 2 輪 .-> Y[達上限停止並人工介入]
    L -. 整體最多 3 輪 .-> Y
""")
write('requirements_discussion.md',"""# 先討論、後生成：需求釐清紀錄（代理提案版）

**記錄方式說明**：本檔是根據已提供的作業條件與已討論過的 SiC 學習方向所做的需求整理，**不是虛構 AI 在本次先後問了使用者 8 題並得到逐題回覆**。若老師要求訪談截圖，應在 Coding Agent 實際執行一輪訪談後再補上。

| 訪談主題 | 暫定決策與理由 |
|---|---|
| 讀者是誰？ | 未修過半導體的學生；文字需白話但術語正確。 |
| 主題範圍？ | SiC 材料 → 長晶 → 磊晶 → MOSFET → 應用。 |
| 資料類型？ | 政府技術網頁 + 同儕審查綜述 + 出版商公開摘要。 |
| 要用什麼語言？ | 繁體中文，關鍵術語附英文縮寫。 |
| 出處要多細？ | 每張證據卡寫原始來源 ID 和位置；每頁簡報標來源。 |
| 文獻相衝突怎麼辦？ | 數值只採同一表（S04 Table 1）；不同版本保留差異備註。 |
| 一次 ingest 還是批次？ | 首輪先完成 6 篇；允許之後增量 ingest。 |
| 最終輸出？ | Wiki 網頁 + 13 頁 HTML 簡報 + GitHub Pages 部署方式。 |
| lint 要檢查什麼？ | 來源筆數、頁數、引用真實性、連結、功能、溢出。 |
| 人工介入點？ | 需求決策、來源可信度、最後內容審核與公開部署。 |

需求整理 → `AGENTS.md` → `raw/` → `cards/` → `wiki/` → `slides/`。
""")
write('README.md',"""# SiC LLM Wiki × 教學 HTML 簡報

這是一份可離線開啟、可直接部署到 GitHub Pages 的靜態 HTML 教學專案。

## 怎麼開啟
- `index.html`：專案入口，連結 Wiki 與簡報。
- `wiki/index.html`：六章學習內容，可搜尋章節，每篇對應證據卡與來源。
- `slides/index.html`：13 頁 HTML 簡報；可按左右方向鍵、上一頁／下一頁、觸控滑動；「⎙」為列印成 PDF。

## 六篇已 ingest 的來源
`source_manifest.json`、`raw/S01.md`～`raw/S06.md`。**Ingest 是從公開全文或公開摘要進行的原創中文事實摘記，不代表把所有論文全文存進專案。** 每筆明確標明哪篇全文可讀、哪篇只取得摘要。

## Wiki 與投影片對照
- Wiki 6 個章節：`wiki/*.md`，公開版 `wiki/index.html`
- 證據卡：`cards/E01.md`～`cards/E12.md`
- 逐頁稿與引用：`slides/drafts/`、`slides/slide_manifest.json`
- 最後的 HTML：`slides/index.html`
- Workflow 與反思：`workflow_graph.mmd`、`.agents/workflows/topic-slides.md`、`report.md`

## 驗證
```bash
python qa/check.py
```
`qa/` 中包含靜態檢查、Node 模擬 DOM 行為、WeasyPrint 13 頁預覽。Playwright 在原始執行環境受到管理政策攔截，**不能宣稱真實瀏覽器測試通過**。請在自己電腦依 `qa/manual_browser_checklist.md` 補測。

## 發佈 GitHub Pages（需自行操作）
1. 在 GitHub 建立新的公開 Repository（例如 `sic-llm-wiki`）。
2. 解壓縮後，**把本專案資料夾裡面的檔案**上傳到 Repository 根目錄，必須有最上層 `index.html`。
3. 到 Settings → Pages → Build and deployment → Deploy from a branch；選 `main` 與 `/ (root)`，儲存。
4. 等 GitHub Pages 顯示部署完成後，複製實際 URL：首頁 `https://帳號.github.io/儲存庫名稱/`；Wiki `.../wiki/`；簡報 `.../slides/`。
5. 把 **實際能打開的網址** 貼到 `submission.txt` 的空白處。這些 URL 是格式示範，不是假定已發布的網址。

## 注意事項
- 某些來源可能受付費或地區限制；本站本地內容不需要存取外部網路，點原始連結才需要。
- 本專案並不是連接即時 LLM API 的問答服務，而是由 LLM 輔助整理出的**靜態 LLM Wiki**，透過來源 ID 與卡片可追溯。
- 如需同學自行再次 ingestion / 生成，請依 `AGENTS.md` 和 workflow 規格操作；HTML 不會自動產生新內容。
- 繳交時需據實填學校、學號、系級、姓名，並自行部署網址；未經實作的人工審查／訪談畫面不可宣稱完成。
""")
print(f'Built: {P} ; {len(sources)} sources, {len(evidence)} evidence, {len(slides)} slides')
