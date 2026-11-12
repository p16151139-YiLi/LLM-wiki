/** Headless logic checks, no Chromium required. Simulated DOM, not a visual browser test. */
const fs=require('fs'),vm=require('vm'),path=require('path');
const base=path.resolve(__dirname,'..');
const issues=[]; let count=0;
function test(cond,description){count++;console.log((cond?'PASS ':'FAIL ')+description);if(!cond) issues.push(description)}
function element(){return {dataset:{},attrs:{},style:{},disabled:false,listener:{},addEventListener(name,cb){this.listener[name]=cb},setAttribute(k,v){this.attrs[k]=v},getAttribute(k){return k==='data-slide'?this.dataset.slide:this.attrs[k]}}}
const slides=Array.from({length:13},(_,i)=>{const e=element();e.dataset.slide=String(i+1);e.on=false;e.classList={toggle(name,bool){if(name==='active')e.on=bool}};return e})
const prev=element(),next=element(),label=element(),bar=element(),print=element();
const els={'#prev':prev,'#next':next,'#pageLabel':label,'#progress':bar,'#print':print};
const docListener={};const winListener={};let location={hash:''};let printed=false;
const document={querySelector:s=>els[s],querySelectorAll:s=>s==='.slide'?slides:[],addEventListener:(ev,cb)=>{docListener[ev]=cb}};
const window={print:()=>{printed=true},addEventListener:(ev,cb)=>{winListener[ev]=cb}};
const history={replaceState:(a,b,frag)=>{location.hash=frag}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'slides_script_0.js'),'utf-8'),{document,window,history,location});
let active=()=>slides.findIndex(x=>x.on)+1;
test(active()===1 && prev.disabled,'Initial deck state is slide 1, Prev disabled');
next.listener.click();test(active()===2,'Next button advances to slide 2');
prev.listener.click();test(active()===1,'Prev button returns to slide 1');
docListener.keydown({key:'End',target:{tagName:'BODY'},preventDefault(){}});test(active()===13 && next.disabled,'End key jumps to last slide');
docListener.keydown({key:'Home',target:{tagName:'BODY'},preventDefault(){}});test(active()===1,'Home key jumps to first slide');
docListener.keydown({key:'ArrowRight',target:{tagName:'BODY'},preventDefault(){}});test(active()===2,'Right arrow advances');
print.listener.click();test(printed,'Print control triggers window.print');
location.hash='#9';winListener.hashchange();test(active()===9,'Direct #9 URL navigation works');
test(bar.style.width==='69.23076923076923%' || bar.style.width.startsWith('69.2307'),'Progress bar updates for slide 9');
const inp=element(),nohits={style:{}}, chapters=['SiC 介紹 寬能隙','物性 遷移率','長晶 單晶','磊晶 CVD','MOSFET 元件','SiC 應用'].map(search=>({dataset:{search},hidden:false}));
const wikiDoc={getElementById:id=>id==='search'?inp:nohits,querySelectorAll:s=>s==='.chapter'?chapters:[]};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'wiki_script_0.js'),'utf8'),{document:wikiDoc});
inp.value='磊晶';inp.listener.input();test(chapters.filter(c=>!c.hidden).length===1,'Wiki search filters to matching section');
inp.value='';inp.listener.input();test(chapters.every(c=>!c.hidden),'Clearing Wiki search restores all chapters');
inp.value='xyznotexists';inp.listener.input();test(nohits.style.display==='block','Wiki shows no-results prompt');
console.log(`RESULT: ${count-issues.length}/${count} successful`);
process.exitCode=issues.length?1:0;
