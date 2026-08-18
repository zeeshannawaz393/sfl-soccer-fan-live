import re, base64, os
SCR=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'screens'); os.chdir(SCR)

CORE=[('onboarding.dev.html','1','Onboarding & Sign-in'),('journey2.dev.html','2','Join a Fan Club'),
 ('journey3.dev.html','3','Buy Coins'),('journey4.dev.html','4','Fan Tasks & Duties'),
 ('journey5.dev.html','5','Predictions & Voting'),('journey6.dev.html','6','Player Transfer Market'),
 ('journey7.dev.html','7','Formation Live Rooms'),('journey8.dev.html','8','Live Engagement'),
 ('journey9.dev.html','9','PK Battle'),('journey10.dev.html','10','Gifts & Kit Bag'),
 ('journey11.dev.html','11','Fan Value Activation'),('journey12.dev.html','12','Progression & Leagues'),
 ('journey13.dev.html','13','Wallet'),('journey14.dev.html','14','Manager Console'),
 ('journey15.dev.html','15','Fan Transfer & Loan'),('journey16.dev.html','16','Rewards & Winners'),
 ('journey17.dev.html','17','Mini-Games'),('journey18.dev.html','18','Content & Social'),
 ('journey19.dev.html','19','Messaging & Calls'),('global-shell.dev.html','G','Global Shell')]
EXTRAS=[('discovery-live.dev.html','E1','Discovery / Live'),('missions.dev.html','E2','Fan Missions'),
 ('room-templates.dev.html','E3','Room Templates'),('light-mode.dev.html','E4','Light Mode Set'),
 ('create-club.dev.html','E5','Create a Club')]
ALL=CORE+EXTRAS
allsrc={fn:open(fn,encoding='utf-8').read() for fn,_,_ in ALL}  # READ ONLY

# dedup images -> :root vars
img_map={}
def vn(fn): return '--img-'+re.sub(r'[^a-zA-Z0-9]','_',fn)
for s in allsrc.values():
    for m in re.finditer(r"url\(['\"]?assets/([\w.\-]+)['\"]?\)", s):
        a=m.group(1)
        if not a.endswith('.woff2'): img_map.setdefault(a,vn(a))
def datauri(path):
    mime='image/jpeg' if path.lower().endswith(('.jpg','.jpeg')) else ('image/png' if path.lower().endswith('.png') else 'application/octet-stream')
    return f'data:{mime};base64,'+base64.b64encode(open('assets/'+path,'rb').read()).decode()
root_vars=':root{\n'+'\n'.join(f'  {v}: url("{datauri(a)}");' for a,v in sorted(img_map.items()))+'\n}'
font_css="@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;src:url('data:font/woff2;base64,"+base64.b64encode(open('assets/manrope.woff2','rb').read()).decode()+"') format('woff2')}"

def split_commas(sel):
    out=[];d=0;cur=''
    for ch in sel:
        if ch in '([':d+=1
        elif ch in ')]':d-=1
        if ch==',' and d==0: out.append(cur);cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur)
    return out
def scope_sels(prelude,scope):
    res=[]
    for s in split_commas(prelude):
        s=s.strip()
        if not s: continue
        if re.match(r'^(html|body)\b', s): res.append(re.sub(r'^(html|body)', scope, s)); continue  # map -> keep inherited color/font
        if s=='*': continue  # global reset handles this
        elif s.startswith(':root'): res.append(s.replace(':root',scope,1))
        else: res.append(scope+' '+s)
    return ', '.join(res)
def scope_css(css,scope):
    res='';i=0;n=len(css)
    while i<n:
        b=css.find('{',i)
        if b==-1: res+=css[i:];break
        prelude=css[i:b].strip();d=1;j=b+1
        while j<n and d>0:
            if css[j]=='{':d+=1
            elif css[j]=='}':d-=1
            j+=1
        body=css[b+1:j-1];low=prelude.lower()
        if prelude.startswith('@'):
            at=low.split()[0] if low.split() else ''
            if at in ('@media','@supports','@document'): res+=prelude+'{'+scope_css(body,scope)+'}'
            else: res+=prelude+'{'+body+'}'
        else:
            sel=scope_sels(prelude,scope)
            if sel: res+=sel+'{'+body+'}'
        i=j
    return res
def imgvar(t):
    def rep(m):
        a=m.group(1)
        return m.group(0) if a.endswith('.woff2') else f'var({img_map[a]})'
    return re.sub(r"url\(['\"]?assets/([\w.\-]+)['\"]?\)",rep,t)

styleblocks=[]; framedata=[]; options=[]
for idx,(fn,num,title) in enumerate(ALL):
    s=allsrc[fn]
    css=re.search(r'<style>(.*?)</style>',s,re.S).group(1)
    css=re.sub(r'@font-face\{[^}]*\}','',css); css=imgvar(css); css=scope_css(css,'#j'+str(idx))
    css+='#j%d{background:transparent!important;padding:0!important;min-height:0!important}'%idx
    styleblocks.append(css)
    fi=s.find('<div class="frames">'); end=s.find('<style id="sfl-chrome"'); end=end if end>0 else s.rfind('</body>')
    frames=imgvar(s[fi:end].rstrip())
    framedata.append(f'<script type="text/plain" class="jframes" data-idx="{idx}">{frames}</script>')
    label=('Global Shell' if num=='G' else ('Extra · '+title if num.startswith('E') else 'J'+num+' · '+title))
    options.append(f'<option value="{idx}">{label}</option>')

# extract GK-01 gift bottom-sheet so it can be overlaid on the current room (not a separate screen)
def _extract_div(html, marker):
    i=html.find(marker)
    if i<0: return ''
    depth=0; j=i; n=len(html)
    while j<n:
        if html.startswith('<div', j): depth+=1; j+=4; continue
        if html.startswith('</div>', j):
            depth-=1; j+=6
            if depth==0: return html[i:j]
            continue
        j+=1
    return html[i:]
_J10IDX=[i for i,(fn,_,_) in enumerate(ALL) if fn=='journey10.dev.html'][0]
_gk=allsrc['journey10.dev.html']; _gk=_gk[_gk.find('<div class="fnum">GK-01</div>'):]
GIFTSHEET_HTML='<div id="j%d" class="sflgiftwrap">%s</div>'%(_J10IDX, imgvar(_extract_div(_gk,'<div class="sheet-scrim">')))

PPNAV_CSS="""
.ppnav{flex:none;display:flex;align-items:center;justify-content:center;gap:16px;padding:10px;background:rgba(10,12,18,.72);border-top:1px solid rgba(255,255,255,.08)}
body[data-stage="light"] .ppnav{background:rgba(255,255,255,.82);border-top-color:#DCE2EC}
.ppnavbtn{font-family:inherit;font-weight:800;font-size:13.5px;padding:11px 24px;border-radius:12px;border:1px solid rgba(255,255,255,.16);background:#171b24;color:#EAEEF5;cursor:pointer}
body[data-stage="light"] .ppnavbtn{background:#fff;color:#14161C;border-color:#DCE2EC}
.ppnavbtn.primary{background:#C9FF3D;color:#0A1400;border-color:#C9FF3D}
.ppcount{font-size:12px;font-weight:800;opacity:.6;font-variant-numeric:tabular-nums;min-width:70px;text-align:center}\n.phone .scroll,.phone .hscroll,.phone .lscroll,.phone .msgs,.phone .chatwrap,.phone .dbody,.phone .lbody,.phone .body,.phone .scrollarea,.phone .feed,.phone .list,.phone .content,.phone .detailbody{overflow-y:auto!important;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.phone .detailbody{flex:1;min-height:0}
.phone .detailbody::-webkit-scrollbar{display:none}
.phone .scrollarea>*,.phone .scroll>*,.phone .lscroll>*,.phone .hscroll>*,.phone .lbody>*,.phone .dbody>*{flex-shrink:0}\n.phone .scroll::-webkit-scrollbar,.phone .hscroll::-webkit-scrollbar,.phone .lscroll::-webkit-scrollbar,.phone .dbody::-webkit-scrollbar,.phone .lbody::-webkit-scrollbar,.phone .body::-webkit-scrollbar,.phone .msgs::-webkit-scrollbar,.phone .scrollarea::-webkit-scrollbar{display:none}
"""
CHROME_CSS="""
/*GLOBAL_RESET_ADDED*/
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{background:#0d1017;font-family:'Manrope',-apple-system,'Segoe UI',sans-serif;color:#EAEEF5;overflow:hidden;display:flex;flex-direction:column}
body[data-stage="light"]{background:#E7ECF6;color:#14161C}
header{flex:none;display:flex;align-items:center;gap:14px;padding:11px 16px;background:rgba(10,12,18,.7);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08);z-index:10}
body[data-stage="light"] header{background:rgba(255,255,255,.8);border-bottom-color:#DCE2EC}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;font-size:14px;letter-spacing:-.3px}
.bc{width:30px;height:30px;border-radius:9px;background:linear-gradient(150deg,#E4362B,#8E1912);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#fff}
select#jsel{font-family:inherit;font-weight:800;font-size:13px;padding:8px 12px;border-radius:10px;border:1px solid rgba(255,255,255,.14);background:#171b24;color:#EAEEF5;cursor:pointer;max-width:230px}
body[data-stage="light"] select#jsel{background:#fff;color:#14161C;border-color:#DCE2EC}
.cap{margin-left:auto;text-align:right;line-height:1.25}
.cap .sc{font-size:13px;font-weight:800}
.cap .ct{font-size:11px;font-weight:700;opacity:.6;font-variant-numeric:tabular-nums}
.ctrls{display:flex;gap:8px}
.ppbtn{width:40px;height:40px;border-radius:11px;border:1px solid rgba(255,255,255,.14);background:#171b24;color:#EAEEF5;font-size:18px;font-weight:800;cursor:pointer;display:flex;align-items:center;justify-content:center}
body[data-stage="light"] .ppbtn{background:#fff;color:#14161C;border-color:#DCE2EC}
.ppbtn:hover{border-color:#C9FF3D}
.ppbtn.sm{width:38px;height:38px;font-size:15px}
.ppstage{flex:1;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;background:radial-gradient(60% 60% at 50% 30%,rgba(47,127,209,.10),transparent 60%)}
.scaler{width:390px;height:844px;flex:none;transform-origin:center center;filter:drop-shadow(0 40px 80px rgba(0,0,0,.5))}
#mount{width:390px;height:844px}
.ppzone{position:absolute;top:0;bottom:0;border:none;background:transparent;cursor:pointer;z-index:5}
.ppzone.l{left:0;width:32%}
.ppzone.r{right:0;width:68%}
.ppzone:focus{outline:none}
.hintl,.hintr{position:absolute;top:50%;transform:translateY(-50%);font-size:26px;opacity:0;transition:opacity .15s;pointer-events:none;z-index:6;color:#C9FF3D}
.ppzone.l:hover ~ .hintl{opacity:.5}.ppzone.r:hover ~ .hintr{opacity:.5}
.hintl{left:16px}.hintr{right:16px}
footer{flex:none;text-align:center;padding:8px;font-size:11px;font-weight:700;opacity:.55;background:rgba(10,12,18,.7);border-top:1px solid rgba(255,255,255,.06)}
body[data-stage="light"] footer{background:rgba(255,255,255,.7);border-top-color:#DCE2EC}
.dotbar{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:5px;z-index:6;max-width:80%;flex-wrap:wrap;justify-content:center}
.ppdot{width:6px;height:6px;border-radius:50%;background:rgba(255,255,255,.28)}
body[data-stage="light"] .ppdot{background:rgba(20,30,60,.22)}
.ppdot.on{background:#C9FF3D;width:16px;border-radius:3px}
.sflcoin{background:transparent!important;background-image:none!important;border:none!important;box-shadow:none!important;color:transparent!important;overflow:visible!important;padding:0!important;display:inline-flex!important;align-items:center;justify-content:center;line-height:0;font-size:0!important}
.sflcoin svg{width:100%;height:100%;display:block}
.sflemoji{display:inline-flex;width:1.15em;height:1.15em;vertical-align:-.2em;flex:none}
.sflemoji svg{width:100%;height:100%;display:block}
/* ---- header menu + modal ---- */
.hdrscreen{flex:1;min-width:0;text-align:center;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding:0 8px;font-size:13px;font-weight:800;color:#EAEEF5;letter-spacing:-.2px}
body[data-stage="light"] .hdrscreen{color:#14161C}
.sflmodal{position:fixed;inset:0;z-index:1000;background:rgba(4,6,10,.62);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);display:none;align-items:flex-start;justify-content:center;padding:56px 16px 16px}
.sflmodal.open{display:flex}
.sflmodal-card{background:#12151d;border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:16px;width:min(430px,94vw);box-shadow:0 30px 80px rgba(0,0,0,.6)}
body[data-stage="light"] .sflmodal-card{background:#fff;border-color:#DCE2EC}
.mm-top{display:flex;align-items:center;margin-bottom:15px}
.mm-top .brand{margin-right:auto}
.mm-lbl{font-size:11px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;color:#8892A4;margin-bottom:8px}
.sflmodal-card select#jsel{width:100%;max-width:none;font-size:14px;padding:12px 14px}
.mm-nav{display:flex;align-items:center;gap:12px;margin-top:15px}
.mm-nav .ppnavbtn{flex:1}
.mm-nav .ppcount{margin:0;min-width:auto}
/* ---- responsive: same page works on phone ---- */
html,body{height:100%}
@media (max-width:600px){
  footer{display:none}
  header{padding:8px 12px;gap:10px}
  .hdrscreen{font-size:12px}
  .ppbtn.sm{width:34px;height:34px;font-size:15px}
  .ppnav{gap:10px;padding:9px}
  .ppnavbtn{padding:12px 22px;font-size:13.5px}
}
"""
SB_INJECT=r"""
  var SIG='<svg width="18" height="13" viewBox="0 0 18 13" fill="currentColor"><rect x="0" y="9" width="3" height="4" rx="1"/><rect x="5" y="6.5" width="3" height="6.5" rx="1"/><rect x="10" y="3.5" width="3" height="9.5" rx="1"/><rect x="15" y="0" width="3" height="13" rx="1"/></svg>';
  var WIFI='<svg width="17" height="13" viewBox="0 0 17 13" fill="currentColor"><path d="M8.5 2.2C5.6 2.2 2.9 3.3 1 5.2l1.5 1.5C4 5.2 6.2 4.2 8.5 4.2s4.5 1 6 2.5L16 5.2c-1.9-1.9-4.6-3-7.5-3z"/><path d="M8.5 6.6c-1.7 0-3.3.7-4.5 1.9l1.6 1.6c.8-.7 1.8-1.2 2.9-1.2s2.1.5 2.9 1.2l1.6-1.6C11.8 7.3 10.2 6.6 8.5 6.6z"/><circle cx="8.5" cy="11.6" r="1.4"/></svg>';
  var BAT='<svg width="27" height="13" viewBox="0 0 27 13" fill="none"><rect x="0.6" y="0.6" width="22.8" height="11.8" rx="3.4" stroke="currentColor" stroke-opacity="0.45"/><rect x="2.1" y="2.1" width="15" height="8.8" rx="1.8" fill="currentColor"/><path d="M25 4.6c1 .5 1 3.3 0 3.8z" fill="currentColor" fill-opacity="0.6"/></svg>';
  function lum(c){var m=(c||'').match(/[\d.]+/g);if(!m)return 1;return 0.2126*m[0]/255+0.7152*m[1]/255+0.0722*m[2]/255;}
  function injectBar(phone){
    if(!phone||phone.querySelector(':scope > .sfl-statusbar'))return;
    var dark=lum(getComputedStyle(phone).backgroundColor)<0.5;
    phone.style.paddingTop='50px';
    var sb=document.createElement('div');sb.className='sfl-statusbar';
    sb.style.cssText='position:absolute;top:0;left:0;right:0;z-index:600;height:50px;display:flex;align-items:center;justify-content:space-between;padding:2px 40px 0 42px;box-sizing:border-box;background:inherit;font-family:Manrope,sans-serif;font-size:15px;font-weight:800;letter-spacing:-.3px;color:'+(dark?'#F4F6FA':'#0E1016');
    sb.innerHTML='<span style="position:relative;z-index:2">9:41</span><div style="position:absolute;left:50%;top:9px;transform:translateX(-50%);width:116px;height:30px;background:#04060A;border-radius:16px"></div><span style="position:relative;z-index:2;display:flex;align-items:center;gap:7px">'+SIG+WIFI+BAT+'</span>';
    phone.insertBefore(sb,phone.firstChild);
    injectNav(phone,dark);
  }

  var NAVCSS=false;
  function ensureNavCss(){ if(NAVCSS)return; NAVCSS=true; var st=document.createElement('style'); st.textContent=
   '.sfl-nav{position:absolute;left:14px;right:14px;bottom:14px;height:60px;border-radius:22px;display:flex;align-items:center;justify-content:space-around;padding:0 8px;z-index:590;font-family:Manrope,-apple-system,sans-serif;background:rgba(255,255,255,.93);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.7);box-shadow:0 12px 34px rgba(20,30,60,.2)}'
   +'.sfl-nav.dark{background:rgba(20,24,32,.9);border-color:rgba(255,255,255,.1);box-shadow:0 12px 34px rgba(0,0,0,.5)}'
   +'.sfl-nav .nit{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:9px;font-weight:800;color:#A6ADBC}'
   +'.sfl-nav.dark .nit{color:#606a78}'
   +'.sfl-nav .nit .ic{font-size:18px;line-height:1}'
   +'.sfl-nav .nit.on{color:#E4362B}'
   +'.sfl-nav .nc{width:52px;height:52px;border-radius:50%;background:linear-gradient(150deg,#E4362B,#8E1912);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:-24px;box-shadow:0 8px 22px rgba(228,54,43,.45);border:3px solid #F4F6FB}'
   +'.sfl-nav.dark .nc{border-color:#12151C}'
   +'.sfl-nav .nc.on{box-shadow:0 0 0 4px rgba(228,54,43,.35),0 10px 24px rgba(228,54,43,.6)}'
   +'.sfl-nav .nc .ic{font-size:19px;line-height:1}.sfl-nav .nc .nl{font-size:7px;font-weight:800;margin-top:1px}';
   document.head.appendChild(st); }
  function injectNav(phone,dark){ var tab=phone.getAttribute&&phone.getAttribute('data-nav'); if(!tab)return; if(phone.querySelector(':scope > .sfl-nav'))return; ensureNavCss();
   function it(id,ic,l){return '<div class="nit'+(tab===id?' on':'')+'"><span class="ic">'+ic+'</span>'+l+'</div>';}
   var nav=document.createElement('div'); nav.className='sfl-nav'+(dark?' dark':'');
   nav.innerHTML=it('home','🏠','Home')+it('market','🔁','Market')+'<div class="nc'+((tab==='stadium'||tab==='live')?' on':'')+'"><span class="ic">🏟️</span><span class="nl">Stadium</span></div>'+it('games','🎮','Games')+it('chats','💬','Chats');
   phone.appendChild(nav);
   var body=phone.querySelector('.scrollarea,.scroll,.lscroll,.hscroll,.feed,.list')||phone.querySelector('.dbody,.lbody,.body'); if(body) body.style.paddingBottom='84px'; }
"""

PLAYER_JS = """
<script>
(function(){
%SB%
  var JOUR=[], BYF=[], meta=%META%;
  document.querySelectorAll('.jframes').forEach(function(sc){
    var idx=+sc.dataset.idx; var tmp=document.createElement('div'); tmp.innerHTML=sc.textContent;
    var screens=[]; BYF[idx]={}; var fws=tmp.querySelectorAll('.fw');
    if(fws.length){fws.forEach(function(fw){var ph=fw.querySelector('.phone'); if(!ph)return;
      var cap=(fw.querySelector('.flabel')?fw.querySelector('.flabel').textContent.replace(/\\s+/g,' ').trim():'');
      var fnEl=fw.querySelector('.fnum'); var fn=fnEl?fnEl.textContent.trim():'';
      var scr={fnum:fn, cap:cap, html:ph.outerHTML, srcJ:idx};
      screens.push(scr); if(fn) BYF[idx][fn]=scr;});}
    else {tmp.querySelectorAll('.phone').forEach(function(ph,i){screens.push({cap:'Screen '+(i+1), html:ph.outerHTML, srcJ:idx});});}
    JOUR[idx]={title:meta[idx], screens:screens};
  });
  var FLOWS=%FLOWS%, JLABELS=%JLABELS%;
  var flowViews=FLOWS.map(function(f){return {label:f.name, flow:true, screens:f.refs.map(function(r){return BYF[r[0]]&&BYF[r[0]][r[1]];}).filter(Boolean)};});
  var jViews=JOUR.map(function(j,i){return {label:JLABELS[i], screens:j.screens};});
  var VIEWS=flowViews.concat(jViews);
  var FLOWN=flowViews.length;
  var curJ=0, curS=0;
  var mount=document.getElementById('mount'), scaler=document.getElementById('scaler');
  var jsel=document.getElementById('jsel'), scap=document.getElementById('scap'), ct=document.getElementById('counter'), dotbar=document.getElementById('dotbar');
  var og1='<optgroup label="\\u2605 Prototyped flows">', og2='<optgroup label="All journeys">';
  VIEWS.forEach(function(v,i){var o='<option value="'+i+'">'+v.label+'</option>'; if(i<FLOWN)og1+=o; else og2+=o;});
  jsel.innerHTML=og1+'</optgroup>'+og2+'</optgroup>';
  function fit(){var st=document.getElementById('stage'); var sh=(st.clientHeight-18)/844; var sw=(st.clientWidth-24)/390; var sc=Math.min(1.02, sh, sw); if(sc>0)scaler.style.transform='scale('+sc+')';}
  var COIN='<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11.2" fill="#C9820C"/><circle cx="12" cy="12" r="9.6" fill="#F4C23A"/><path d="M6 8.5a9 9 0 0 1 12 0" stroke="#FCE7A6" stroke-width="1.1" fill="none" opacity=".7"/><circle cx="12" cy="12" r="4.7" fill="#fff"/><path d="M12 8.1l2.6 1.9-1 3.1h-3.2l-1-3.1z" fill="#22252B"/><circle cx="12" cy="7.4" r=".7" fill="#22252B"/><circle cx="16.2" cy="10.6" r=".7" fill="#22252B"/><circle cx="14.6" cy="15.5" r=".7" fill="#22252B"/><circle cx="9.4" cy="15.5" r=".7" fill="#22252B"/><circle cx="7.8" cy="10.6" r=".7" fill="#22252B"/></svg>';
  var GOLD='<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11.2" fill="#8A5606"/><circle cx="12" cy="12" r="9.6" fill="#E7A62A"/><path d="M6 8.5a9 9 0 0 1 12 0" stroke="#FFDE9B" stroke-width="1.1" fill="none" opacity=".65"/><path d="M12 6.6l1.7 3.7 4 .4-3 2.6.9 3.9-3.6-2.1-3.6 2.1.9-3.9-3-2.6 4-.4z" fill="#7A4B00"/></svg>';
  function SFLcoinify(root){
    root.querySelectorAll('.coin,.gc,.gg,.g-coin,.g-gold,.g-tgold').forEach(function(e){
      if(e.getAttribute('data-ic'))return; var cn=e.className||'', tx=(e.textContent||'').trim();
      if(tx.length>1)return;
      var gold=/(^|\s)gg(\s|$)|g-gold|g-tgold/.test(cn)||tx==='G'||tx==='g';
      e.setAttribute('data-ic','1'); e.classList.add('sflcoin'); if(gold)e.classList.add('isgold');
      e.innerHTML=gold?GOLD:COIN;
    });
    ['.coinpill','.coinbal'].forEach(function(s){root.querySelectorAll(s).forEach(function(e){ if(e.getAttribute('data-ic2'))return; if(e.innerHTML.indexOf('🪙')>=0){e.setAttribute('data-ic2','1'); e.innerHTML=e.innerHTML.replace(/🪙/g,'<span class="sflemoji">'+COIN+'</span>');}});});
  }
  var COLMAP={red:['#F0564A','#A81C12'],blue:['#5AA0E6','#1B569B'],gold:['#F3CC55','#B0800A'],green:['#5FC27E','#1C8348'],purple:['#B07CF0','#6A34B8'],teal:['#43C4C9','#157B7F']};
  var INITCOL={RD:'red',RF:'red',BV:'blue',BW:'blue',BL:'blue',CF:'blue',RL:'gold',NS:'gold',NSH:'green',MTL:'green',SFL:'red'};
  var PALK=['red','blue','gold','green','purple','teal'];
  function crestCols(cn,tx){var t=cn.replace('cr-','');
    if(/(^|\s)(cr-red|red)(\s|$)/.test(cn))return COLMAP.red; if(/(^|\s)(cr-blue|blue)(\s|$)/.test(cn))return COLMAP.blue;
    if(/(^|\s)(cr-gold|gold)(\s|$)/.test(cn))return COLMAP.gold; if(/(^|\s)(cr-green|green)(\s|$)/.test(cn))return COLMAP.green;
    if(INITCOL[tx])return COLMAP[INITCOL[tx]];
    var h=0;for(var i=0;i<tx.length;i++)h=(h*31+tx.charCodeAt(i))>>>0;return COLMAP[PALK[h%PALK.length]];}
  function shield(c1,c2){return 'data:image/svg+xml;utf8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 46"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+c1+'"/><stop offset="1" stop-color="'+c2+'"/></linearGradient></defs><path d="M20 2 L37 6.8 V21 C37 32.5 29.5 40 20 43.6 C10.5 40 3 32.5 3 21 V6.8 Z" fill="url(#g)" stroke="#ffffff" stroke-width="2"/><path d="M20 5 L34 8.8 V20 C34 24 31 27 20 22 C9 27 6 24 6 20 V8.8 Z" fill="#ffffff" opacity="0.12"/></svg>');}
  function SFLcrest(root){
    root.querySelectorAll('.crest,.ccrest,.crestbig,.cbadge').forEach(function(e){
      if(e.getAttribute('data-cr'))return; var tx=(e.textContent||'').trim(); if(tx.length>4)return;
      var cols=crestCols(e.className||'',tx); e.setAttribute('data-cr','1'); e.classList.add('sflcrest');
      e.style.backgroundImage='url("'+shield(cols[0],cols[1])+'")'; e.style.backgroundColor='transparent';
      e.style.backgroundSize='contain'; e.style.backgroundRepeat='no-repeat'; e.style.backgroundPosition='center';
      e.style.borderRadius='0'; e.style.boxShadow='none'; e.style.border='none';
      e.style.color='#fff'; e.style.textShadow='0 1px 2px rgba(0,0,0,.4)'; e.style.fontWeight='800';
    });
  }
  var GIFTSHEET=%GIFTSHEET%;
  function SFLgiftInteract(scope,tgt,onClose){
    if(tgt.classList&&(tgt.classList.contains('sheet-scrim')||tgt.classList.contains('sflgiftoverlay'))){ if(onClose)onClose(); return true; }
    var gt=tgt.closest('.gtile'); if(gt){ [].forEach.call(scope.querySelectorAll('.gtile'),function(c){c.classList.remove('on');}); gt.classList.add('on'); var nm=((gt.querySelector('.gn')||{}).textContent||'Gift').trim(); var pr=((gt.querySelector('.gp')||{}).textContent||'').replace(/\s+/g,''); var sb=scope.querySelector('.gsheet .btn')||scope.querySelector('.btn'); if(sb)sb.innerHTML='Send '+nm+' to Reds · '+pr; return true; }
    var gc=tgt.closest('.gcat'); if(gc&&gc.parentElement){ [].forEach.call(gc.parentElement.children,function(c){c.classList&&c.classList.remove('on');}); gc.classList.add('on'); var gx=(gc.textContent||'').toLowerCase(); var key=/match/.test(gx)?'matchday':/troph/.test(gx)?'trophies':/golden boot/.test(gx)?'goldenboot':/golden glove/.test(gx)?'goldenglove':/support/.test(gx)?'support':/pk|penalty/.test(gx)?'pk':/refer/.test(gx)?'referee':/stadium/.test(gx)?'stadium':/club/.test(gx)?'clubkit':/world/.test(gx)?'worldcup':/legend/.test(gx)?'legends':/vip|luxury|diamond/.test(gx)?'vip':'popular'; [].forEach.call(scope.querySelectorAll('.gtile'),function(tl){var cats=(tl.getAttribute('data-cat')||''); tl.style.display=(cats.indexOf(key)>=0)?'':'none';}); return true; }
    if(tgt.closest('.btn,.gbtn')){ if(onClose)onClose(); return true; }
    return false;
  }
  function openGiftSheet(){
    if(SFLguest){goTo('gate');return;}
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflgiftoverlay'))return;
    var ov=document.createElement('div'); ov.className='sflgiftoverlay'; ov.style.cssText='position:absolute;inset:0;z-index:700'; ov.innerHTML=GIFTSHEET;
    phone.appendChild(ov); SFLcoinify(ov); SFLcrest(ov);
    ov.addEventListener('click',function(e){ e.stopPropagation(); var isSend=!!e.target.closest('.btn,.gbtn'); var selEl=isSend&&(ov.querySelector('.gtile.on .ge')||ov.querySelector('.gtile.on')); var em=selEl?(selEl.textContent||'').trim():'🎁'; SFLgiftInteract(ov,e.target,function(){ov.remove(); if(isSend)flyGift(em);}); });
  }
  function showSeatCard(seat){
    if(!seat||seat.classList.contains('open'))return false;
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return false;
    var nm=((seat.querySelector('.nm')||{}).textContent||'').trim(); if(!nm||nm==='Open')return false;
    if(phone.querySelector('.sflseatwrap'))return true;
    var av=seat.querySelector('.av'); var bg=(av&&av.style.backgroundImage)||''; var pos=((seat.querySelector('.pos')||{}).textContent||'').trim();
    var isYou=/^you$/i.test(nm);
    var h=0; for(var i=0;i<nm.length;i++)h=(h*31+nm.charCodeAt(i))>>>0;
    var lvl=8+(h%13), fp=(2+(h%9))+'.'+(h%10)+'k', gifts=40+(h%210), streak=3+(h%22);
    var stat=function(v,l){return '<div style="flex:1"><div style="font-size:15px;font-weight:800;color:#fff">'+v+'</div><div style="font-size:9.5px;font-weight:800;letter-spacing:.3px;color:#8892A4;margin-top:2px;text-transform:uppercase">'+l+'</div></div>';};
    var wrap=document.createElement('div'); wrap.className='sflseatwrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:720;display:flex;align-items:center;justify-content:center;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)';
    wrap.innerHTML='<div style="position:relative;width:272px;background:linear-gradient(180deg,#1b2030,#12151d);border:1px solid rgba(255,255,255,.14);border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.65);color:#EAEEF5;font-family:Manrope,-apple-system,sans-serif">'
      +'<div class="ssc-close" style="position:absolute;top:11px;right:11px;width:26px;height:26px;border-radius:50%;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;cursor:pointer;z-index:3">✕</div>'
      +'<div style="height:66px;background:linear-gradient(135deg,#E4362B,#8E1912)"></div>'
      +'<div style="padding:0 18px 18px;margin-top:-40px;text-align:center">'
      +'<div style="width:80px;height:80px;border-radius:50%;margin:0 auto;background-image:'+bg+';background-color:#222;background-size:cover;background-position:center;border:3px solid #12151d;box-shadow:0 8px 20px rgba(0,0,0,.5)"></div>'
      +'<div style="font-size:18px;font-weight:800;margin-top:9px">'+nm+' <span style="color:#3FA9F5;font-size:14px">✓</span></div>'
      +'<div style="display:flex;gap:6px;align-items:center;justify-content:center;font-size:12px;font-weight:750;color:#B7C0CE;margin-top:3px"><span style="display:inline-flex;width:16px;height:18px;background:linear-gradient(150deg,#E4362B,#8E1912);border-radius:3px;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:#fff">RD</span> Red District FC'+(pos?(' · '+pos):'')+'</div>'
      +'<div style="display:flex;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:11px 4px;margin-top:14px">'+stat('Lv '+lvl,'Level')+'<div style="width:1px;background:rgba(255,255,255,.09)"></div>'+stat(fp,'Fan Power')+'<div style="width:1px;background:rgba(255,255,255,.09)"></div>'+stat(gifts,'Gifts')+'</div>'
      +'<div style="display:flex;gap:6px;justify-content:center;margin-top:11px"><span style="font-size:10px;font-weight:800;background:rgba(201,255,61,.16);color:#C9FF3D;padding:5px 10px;border-radius:8px">🔥 '+streak+'-day streak</span><span style="font-size:10px;font-weight:800;background:rgba(255,255,255,.08);padding:5px 10px;border-radius:8px">'+(isYou?'That\\'s you':'Supporter')+'</span></div>'
      +(isYou
        ? '<div class="ssc-profile" style="margin-top:14px;display:flex;align-items:center;justify-content:center;gap:7px;background:rgba(255,255,255,.08);font-weight:800;font-size:13px;padding:12px;border-radius:12px;cursor:pointer">👤 View Profile</div>'
        : '<div style="display:flex;gap:8px;margin-top:14px"><div class="ssc-msg" style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(255,255,255,.08);font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">💬 Message</div><div class="ssc-profile" style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(255,255,255,.08);font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">👤 Profile</div></div>'
          +'<div class="ssc-gift" style="margin-top:9px;background:linear-gradient(140deg,#F3CC55,#B0800A);color:#3A2400;font-weight:800;font-size:13.5px;padding:12px;border-radius:13px;cursor:pointer">🎁 Send '+nm+' a Gift</div>')
      +'</div></div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.ssc-close')){wrap.remove();return;} if(e.target.closest('.ssc-gift')){wrap.remove(); openGiftSheet(); return;} if(e.target.closest('.ssc-msg')){wrap.remove(); goTo('chatthread'); return;} if(e.target.closest('.ssc-profile')){wrap.remove(); goTo('userprofile'); return;} });
    return true;
  }
  var _FLYCSS=false;
  function ensureFlyCss(){ if(_FLYCSS)return; _FLYCSS=true; var st=document.createElement('style'); st.textContent='@keyframes sflflyup{0%{transform:translateY(0) scale(.5);opacity:0}12%{opacity:1;transform:translateY(-16px) scale(1)}75%{opacity:1}100%{transform:translateY(-340px) scale(1.15);opacity:0}}.sflfly{position:absolute;bottom:96px;z-index:735;pointer-events:none;animation:sflflyup 1.9s cubic-bezier(.25,.7,.4,1) forwards;filter:drop-shadow(0 4px 10px rgba(0,0,0,.5))}'; document.head.appendChild(st); }
  function flyGift(emoji){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return; ensureFlyCss();
    for(var k=0;k<6;k++){(function(i){
      var g=document.createElement('div'); g.className='sflfly'; g.textContent=emoji||'🎁';
      g.style.left=(24+Math.random()*50)+'%'; g.style.fontSize=(24+Math.random()*20)+'px'; g.style.animationDelay=(i*110)+'ms';
      phone.appendChild(g);
      setTimeout(function(){ if(g.parentNode)g.parentNode.removeChild(g); }, 2100+i*110);
    })(k);}
  }
  function sflToast(msg){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return;
    var old=phone.querySelector('.sfltoast'); if(old)old.remove();
    var tst=document.createElement('div'); tst.className='sfltoast';
    tst.style.cssText='position:absolute;left:50%;bottom:120px;transform:translateX(-50%);z-index:760;background:rgba(18,21,29,.96);color:#EAEEF5;font-family:Manrope,-apple-system,sans-serif;font-size:13px;font-weight:800;padding:11px 18px;border-radius:12px;border:1px solid rgba(255,255,255,.14);box-shadow:0 12px 30px rgba(0,0,0,.5);max-width:82%;text-align:center';
    tst.textContent=msg; phone.appendChild(tst);
    setTimeout(function(){ if(tst.parentNode)tst.parentNode.removeChild(tst); },1700);
  }
  function showMoveSheet(name){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflmovewrap'))return;
    var pos=['RW','CB','CM'];
    var chips=pos.map(function(p){return '<div class="mv-pos" data-p="'+p+'" style="min-width:58px;text-align:center;padding:12px 14px;border-radius:13px;background:rgba(201,255,61,.12);border:1px solid rgba(201,255,61,.3);color:#C9FF3D;font-weight:800;font-size:14px;cursor:pointer">'+p+'</div>';}).join('');
    var wrap=document.createElement('div'); wrap.className='sflmovewrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:745;display:flex;align-items:flex-end;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)';
    wrap.innerHTML='<div style="width:100%;background:linear-gradient(180deg,#1b2030,#12151d);border-top-left-radius:22px;border-top-right-radius:22px;padding:16px 18px 26px;box-shadow:0 -20px 50px rgba(0,0,0,.5);color:#EAEEF5;font-family:Manrope,-apple-system,sans-serif">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:rgba(255,255,255,.2);margin:0 auto 14px"></div>'
      +'<div style="font-size:16px;font-weight:800">Move '+name+' to…</div>'
      +'<div style="font-size:12px;font-weight:700;color:#8892A4;margin-top:3px">Choose an open position on the pitch</div>'
      +'<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:15px">'+chips+'</div>'
      +'<div class="mv-cancel" style="text-align:center;margin-top:18px;font-size:13px;font-weight:800;color:#8892A4;cursor:pointer">Cancel</div>'
      +'</div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.mv-cancel')){wrap.remove();return;} var mp=e.target.closest('.mv-pos'); if(mp){var p=mp.getAttribute('data-p'); wrap.remove(); goBack(); sflToast(name+' moved to '+p);} });
  }
  function showDestSheet(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sfldestwrap'))return;
    var clubs=[['BW','Blue Wolves','Grade B · #7 · accepting moves','blue'],['GS','Green Storm','Grade A · #3 · accepting moves','green'],['SC','Steel City','Grade C · #12 · open','red']];
    var rows=clubs.map(function(c){return '<div class="ds-club" data-cn="'+c[1]+'" data-cm="'+c[2]+'" data-cr="'+c[0]+'" data-cc="'+c[3]+'" style="display:flex;align-items:center;gap:12px;padding:13px;border:1px solid #ECEEF5;border-radius:14px;margin-top:9px;cursor:pointer"><div style="width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:18px;background:'+(c[3]==='blue'?'linear-gradient(150deg,#2F7FD1,#1E5E9E)':c[3]==='green'?'linear-gradient(150deg,#0FB753,#0a8f40)':'linear-gradient(150deg,#E4362B,#B4241B)')+'">'+c[0]+'</div><div style="flex:1"><div style="font-size:15px;font-weight:800;color:#14161C">'+c[1]+'</div><div style="font-size:11.5px;font-weight:700;color:#707786;margin-top:2px">'+c[2]+'</div></div></div>';}).join('');
    var wrap=document.createElement('div'); wrap.className='sfldestwrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:745;display:flex;align-items:flex-end;background:rgba(20,30,60,.42);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)';
    wrap.innerHTML='<div style="width:100%;background:#fff;border-top-left-radius:22px;border-top-right-radius:22px;padding:16px 18px 26px;box-shadow:0 -20px 50px rgba(20,30,60,.25);font-family:Manrope,-apple-system,sans-serif">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:#D7DDEA;margin:0 auto 14px"></div>'
      +'<div style="font-size:17px;font-weight:800;color:#10121A">Choose destination club</div>'
      +'<div style="font-size:12px;font-weight:700;color:#707786;margin-top:3px">Only clubs accepting moves are shown</div>'
      +rows
      +'<div class="ds-cancel" style="text-align:center;margin-top:16px;font-size:13px;font-weight:800;color:#707786;cursor:pointer">Cancel</div>'
      +'</div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.ds-cancel')){wrap.remove();return;} var dc=e.target.closest('.ds-club'); if(dc){ var cn=dc.getAttribute('data-cn'),cm=dc.getAttribute('data-cm'),cr=dc.getAttribute('data-cr'),cc=dc.getAttribute('data-cc'); var cp=phone.querySelector('.clubprev'); if(cp){ var crest=cp.querySelector('.crest'); if(crest){crest.textContent=cr; crest.className='crest'+(cc==='blue'?' blue':cc==='green'?' green':'');} var nm=cp.querySelector('.cn'); if(nm)nm.textContent=cn; var mt=cp.querySelector('.cm'); if(mt)mt.textContent=cm; } wrap.remove(); sflToast('Destination set · '+cn); } });
  }
  function showTermSheet(row){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sfltermwrap'))return;
    var f=row.getAttribute('data-field');
    var MAP={start:['Start date',['18 Aug 2026 · today','20 Aug 2026','1 Sep 2026','1 Jan 2027']],
             end:['End / return',['30 days','Half season · 2 Jan','1 season · 31 May','90 days']],
             early:['Early return',['Not allowed','Allowed with notice']],
             expires:['Offer expires',['in 3 days','in 7 days','in 14 days']]};
    var m=MAP[f]; if(!m)return;
    var cur=((row.querySelector('.v')||{}).textContent||'').trim();
    var opts=m[1].map(function(o){var on=(o.indexOf(cur)>=0||cur.indexOf(o)>=0); return '<div class="tm-opt" data-v="'+o+'" style="display:flex;align-items:center;justify-content:space-between;padding:13px;border:1.5px solid '+(on?'#2F7FD1':'#ECEEF5')+';border-radius:13px;margin-top:9px;font-size:14px;font-weight:750;color:#14161C;cursor:pointer;background:'+(on?'#F0F7FF':'#fff')+'">'+o+(on?'<span style="color:#2F7FD1;font-weight:800">✓</span>':'')+'</div>';}).join('');
    var wrap=document.createElement('div'); wrap.className='sfltermwrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:746;display:flex;align-items:flex-end;background:rgba(20,30,60,.42);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px)';
    wrap.innerHTML='<div style="width:100%;background:#fff;border-top-left-radius:22px;border-top-right-radius:22px;padding:16px 18px 26px;box-shadow:0 -20px 50px rgba(20,30,60,.25);font-family:Manrope,-apple-system,sans-serif">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:#D7DDEA;margin:0 auto 14px"></div>'
      +'<div style="font-size:17px;font-weight:800;color:#10121A">'+m[0]+'</div>'
      +'<div style="font-size:12px;font-weight:700;color:#707786;margin-top:3px">Set the term for this offer</div>'
      +opts
      +'<div class="tm-cancel" style="text-align:center;margin-top:16px;font-size:13px;font-weight:800;color:#707786;cursor:pointer">Cancel</div>'
      +'</div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.tm-cancel')){wrap.remove();return;} var op=e.target.closest('.tm-opt'); if(op){var v=op.getAttribute('data-v'); var vel=row.querySelector('.v'); if(vel)vel.textContent=v; wrap.remove(); sflToast('Updated · '+v);} });
  }
  function setEditPhoto(url){ var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return; var av=phone.querySelector('.epavatar'); if(av){ av.style.backgroundImage=url||'none'; av.style.backgroundColor=url?'':'#DCE2EC'; } }
  function showPhotoSheet(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflphotowrap'))return;
    var wrap=document.createElement('div'); wrap.className='sflphotowrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:745;display:flex;align-items:flex-end;background:rgba(4,6,10,.5)';
    wrap.innerHTML='<div style="width:100%;background:#fff;border-top-left-radius:22px;border-top-right-radius:22px;padding:14px 16px 24px;box-shadow:0 -20px 50px rgba(0,0,0,.3);font-family:Manrope,-apple-system,sans-serif">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:#DCE2EC;margin:0 auto 14px"></div>'
      +'<div style="font-size:15px;font-weight:800;color:#14161C;margin-bottom:6px">Change display picture</div>'
      +'<div class="pp-cam" style="display:flex;align-items:center;gap:12px;padding:13px 8px;border-bottom:1px solid #EEF1F7;cursor:pointer;font-weight:750;font-size:14px;color:#14161C">📷 Take a photo</div>'
      +'<div class="pp-gal" style="display:flex;align-items:center;gap:12px;padding:13px 8px;border-bottom:1px solid #EEF1F7;cursor:pointer;font-weight:750;font-size:14px;color:#14161C">🖼️ Choose from gallery</div>'
      +'<div class="pp-rm" style="display:flex;align-items:center;gap:12px;padding:13px 8px;cursor:pointer;font-weight:750;font-size:14px;color:#E4362B">🗑️ Remove current photo</div>'
      +'<div class="pp-cancel" style="text-align:center;margin-top:12px;padding:12px;background:#F0F2F7;border-radius:12px;font-weight:800;color:#14161C;cursor:pointer">Cancel</div>'
      +'</div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.pp-cancel')){wrap.remove();return;} if(e.target.closest('.pp-cam')){wrap.remove();showCameraOverlay();return;} if(e.target.closest('.pp-gal')){wrap.remove();showGallerySheet();return;} if(e.target.closest('.pp-rm')){wrap.remove();setEditPhoto('');sflToast('Photo removed');return;} });
  }
  function showCameraOverlay(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return;
    var wrap=document.createElement('div'); wrap.className='sflcamwrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:750;background:#000;display:flex;flex-direction:column;font-family:Manrope,-apple-system,sans-serif';
    wrap.innerHTML='<div style="flex:1;background:url(assets/fb_host.jpg) center/cover;position:relative">'
      +'<div class="cam-close" style="position:absolute;top:16px;left:16px;width:34px;height:34px;border-radius:50%;background:rgba(0,0,0,.5);color:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;cursor:pointer">✕</div>'
      +'<div style="position:absolute;left:50%;top:44%;transform:translate(-50%,-50%);width:200px;height:200px;border-radius:50%;border:3px solid rgba(255,255,255,.7)"></div>'
      +'<div style="position:absolute;bottom:24px;left:0;right:0;text-align:center;color:#fff;font-weight:750;font-size:13px">Center your face, then tap the shutter</div></div>'
      +'<div style="height:120px;background:#000;display:flex;align-items:center;justify-content:center"><div class="cam-shot" style="width:66px;height:66px;border-radius:50%;background:#fff;border:4px solid rgba(255,255,255,.35);cursor:pointer"></div></div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target.closest('.cam-close')){wrap.remove();return;} if(e.target.closest('.cam-shot')){setEditPhoto("url('assets/fb_host.jpg')");wrap.remove();sflToast('Photo updated');return;} });
  }
  function showGallerySheet(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return;
    var imgs=['q1_t.jpg','fb_host.jpg','fb_f2.jpg','fb_m1.jpg','nadia_t.jpg','sara_t.jpg','kojo_t.jpg','mb_t.jpg','dk_t.jpg'];
    var cells=''; for(var i=0;i<imgs.length;i++){cells+='<div class="gal-pick" data-img="'+imgs[i]+'" style="padding-bottom:100%;position:relative;border-radius:10px;cursor:pointer;background:url(assets/'+imgs[i]+') center/cover"></div>';}
    var wrap=document.createElement('div'); wrap.className='sflgalwrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:750;background:#0d1017;display:flex;flex-direction:column;font-family:Manrope,-apple-system,sans-serif';
    wrap.innerHTML='<div style="display:flex;align-items:center;gap:12px;padding:16px;color:#fff"><div class="gal-close" style="width:34px;height:34px;border-radius:50%;background:rgba(255,255,255,.12);display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer">‹</div><div style="font-size:17px;font-weight:800">Choose a photo</div></div>'
      +'<div style="flex:1;overflow-y:auto;padding:0 12px 12px"><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">'+cells+'</div></div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target.closest('.gal-close')){wrap.remove();return;} var g=e.target.closest('.gal-pick'); if(g){setEditPhoto("url('assets/"+g.getAttribute('data-img')+"')");wrap.remove();sflToast('Photo updated');return;} });
  }
  function sflSheet(title, inner){ var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflsheetwrap'))return null; var wrap=document.createElement('div'); wrap.className='sflsheetwrap'; wrap.style.cssText='position:absolute;inset:0;z-index:748;display:flex;align-items:flex-end;background:rgba(4,6,10,.5)'; wrap.innerHTML='<div style="width:100%;background:#fff;border-top-left-radius:22px;border-top-right-radius:22px;padding:14px 16px 24px;box-shadow:0 -20px 50px rgba(0,0,0,.3);font-family:Manrope,-apple-system,sans-serif"><div style="width:38px;height:4px;border-radius:2px;background:#DCE2EC;margin:0 auto 14px"></div><div style="font-size:15px;font-weight:800;color:#14161C;margin-bottom:10px">'+title+'</div>'+inner+'</div>'; phone.appendChild(wrap); return wrap; }
  function showLanguageSheet(){
    var langs=['English','Español','Français','Deutsch','العربية','हिन्दी','Português']; var rows='';
    for(var i=0;i<langs.length;i++){rows+='<div class="lang-opt" data-l="'+langs[i]+'" style="display:flex;align-items:center;padding:12px 8px;border-bottom:1px solid #EEF1F7;font-weight:750;font-size:14px;color:#14161C;cursor:pointer">'+langs[i]+(i===0?'<span style="margin-left:auto;color:#0FA04C">✓</span>':'')+'</div>';}
    var wrap=sflSheet('Language', rows+'<div class="sh-cancel" style="text-align:center;margin-top:12px;padding:12px;background:#F0F2F7;border-radius:12px;font-weight:800;color:#14161C;cursor:pointer">Cancel</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} var lo=e.target.closest('.lang-opt'); if(lo){var l=lo.getAttribute('data-l'); var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); [].forEach.call(phone.querySelectorAll('.listrow'),function(r){if(/language/i.test(r.textContent)){var a=r.querySelector('.arr'); if(a)a.textContent=l+' ›';}}); wrap.remove(); sflToast('Language set to '+l); return;} });
  }
  function showWithdrawSheet(){
    var wrap=sflSheet('Withdraw application?', '<div style="font-size:12.5px;font-weight:700;color:#5A6472;margin-bottom:14px">Your application to Red District FC will be removed. You can re-apply anytime.</div><div class="wd-yes" style="text-align:center;padding:13px;background:#E4362B;color:#fff;border-radius:12px;font-weight:800;cursor:pointer">Withdraw application</div><div class="sh-cancel" style="text-align:center;margin-top:10px;padding:12px;background:#F0F2F7;border-radius:12px;font-weight:800;color:#14161C;cursor:pointer">Keep it</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} if(e.target.closest('.wd-yes')){ wrap.remove(); var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); var body=phone&&phone.querySelector('.body'); if(body){ body.innerHTML='<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 24px"><div style="width:80px;height:80px;border-radius:50%;background:#F0F2F7;display:flex;align-items:center;justify-content:center;font-size:34px">📭</div><div style="font-size:20px;font-weight:800;color:#14161C;margin-top:16px">No applications</div><div style="font-size:13px;font-weight:650;color:#707786;margin-top:8px;max-width:250px">You withdrew your application. Discover clubs and apply anytime.</div><div class="wd-discover" style="margin-top:20px;padding:14px 22px;background:#E4362B;color:#fff;border-radius:14px;font-weight:800;cursor:pointer">Discover Clubs</div></div>'; } sflToast('Application withdrawn'); return;} });
  }
  function showLogoutSheet(){
    var wrap=sflSheet('Log out of SFL?', '<div style="font-size:12.5px;font-weight:700;color:#5A6472;margin-bottom:14px">You can sign back in anytime. Your account and progress stay safe.</div><div class="lo-yes" style="text-align:center;padding:13px;background:#E4362B;color:#fff;border-radius:12px;font-weight:800;cursor:pointer">Log out</div><div class="sh-cancel" style="text-align:center;margin-top:10px;padding:12px;background:#F0F2F7;border-radius:12px;font-weight:800;color:#14161C;cursor:pointer">Cancel</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} if(e.target.closest('.lo-yes')){wrap.remove(); hist.length=0; goTo('signin'); return;} });
  }
  function showEditSheet(title, val, msg){
    var wrap=sflSheet(title, '<div contenteditable="true" class="es-field" style="height:46px;border-radius:12px;background:#F0F2F7;display:flex;align-items:center;padding:0 14px;font-size:14px;font-weight:700;color:#14161C;outline:none">'+val+'</div><div style="font-size:11.5px;font-weight:700;color:#8892A4;margin-top:8px">'+(msg||'')+'</div><div class="es-save" style="text-align:center;margin-top:14px;padding:13px;background:#C9FF3D;color:#0A1400;border-radius:12px;font-weight:800;cursor:pointer">Save</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap){wrap.remove();return;} if(e.target.closest('.es-field')){return;} if(e.target.closest('.es-save')){wrap.remove();sflToast(title+' updated · verification sent');return;} });
  }
  function SFLchat(root){
    function sendFrom(e){ var ph=e.getAttribute('data-ph')||''; var txt=(e.textContent||'').trim(); if(!txt||txt===ph)return; var clean=txt.replace(/[<>&]/g,''); var box=root.querySelector('.rchat')||root.querySelector('.msgs')||root.querySelector('.chatwrap')||root.querySelector('.chatprev'); if(box){var isMsg=box.classList.contains('msgs')||box.classList.contains('chatwrap'); var d=document.createElement('div'); d.className=isMsg?'msg out':'cm'; d.innerHTML=isMsg?clean:'<b style="color:#DCFF8A">You</b> '+clean; box.appendChild(d); box.scrollTop=box.scrollHeight;} e.textContent=''; }
    root.querySelectorAll('.rsay,.cin,.chatin,.msgin,.rsayb').forEach(function(e){
      if(e.getAttribute('data-chat'))return; if(/speaking on/i.test(e.textContent||''))return;
      e.setAttribute('data-chat','1'); e.setAttribute('contenteditable','true'); e.style.outline='none'; e.style.cursor='text';
      var ph=(e.textContent||'').trim(); e.setAttribute('data-ph',ph);
      e.addEventListener('focus',function(){ if((e.textContent||'').trim()===ph){e.textContent='';} });
      e.addEventListener('blur',function(){ if(!(e.textContent||'').trim()){e.textContent=ph;} });
      e.addEventListener('keydown',function(ev){ ev.stopPropagation(); if(ev.key==='Enter'){ ev.preventDefault(); sendFrom(e); } });
    });
    root.querySelectorAll('.cbtn.send').forEach(function(b){ if(b.getAttribute('data-send'))return; b.setAttribute('data-send','1'); b.addEventListener('click',function(ev){ ev.stopPropagation(); var inp=b.parentElement.querySelector('.cin'); if(inp)sendFrom(inp); }); });
  }
  function render(){
    var v=VIEWS[curJ]; if(!v||!v.screens.length)return;
    if(curS>=v.screens.length)curS=v.screens.length-1;
    var scr=v.screens[curS];
    mount.id='j'+scr.srcJ; mount.innerHTML=scr.html;
    injectBar(mount.querySelector('.phone'));
    SFLcoinify(mount); SFLcrest(mount); SFLchat(mount);
    if(scr.fnum==='FT-01'||scr.fnum==='FT-02'){applyTaskDone(mount);}
    if(scr.fnum==='PV-04'){SFLpred={match:SFLpredMatch,score:SFLpredScore};}
    if(scr.fnum==='PV-05'){applyVoteDone(mount,'motm');}
    if(scr.fnum==='PV-09'){applyVoteDone(mount,'award');}
    if(scr.fnum==='GK-01E'){setTimeout(function(){flyGift('🥇');},180);}
    if(scr.fnum==='J2-21'&&SFLfvActive){var _j21b=mount.querySelector('.btn'); if(_j21b)_j21b.textContent='✓ Fan Value Active';}
    if(scr.fnum==='FV-00'&&SFLfvActive){var _fv0b=mount.querySelector('.btn'); if(_fv0b)_fv0b.textContent='✓ Already Active';}
    if(scr.fnum==='MSG-04'&&SFLchatGift){ var _cg=SFLchatGift; SFLchatGift=null; var _mb=mount.querySelector('.msgs'); if(_mb){ var _gcard=document.createElement('div'); _gcard.className='giftcard'; _gcard.innerHTML='<div class="gi">'+_cg.em+'</div><div class="gt">You sent a '+_cg.gn+'</div><div class="gs">Sent via Gifts · '+_cg.gp+' Coins</div>'; _mb.appendChild(_gcard); _mb.scrollTop=_mb.scrollHeight; } setTimeout(function(){flyGift(_cg.em);},160); }
    if(scr.fnum==='PK-00'){SFLpkViewer=false;}
    if(scr.fnum==='G-02G'){SFLguest=true;}
    if(scr.fnum==='G-02'||scr.fnum==='G-02M'){SFLguest=false;}
    if(scr.fnum==='PK-03'){ var _pgb=mount.querySelector('.giftbtns'); if(_pgb)_pgb.style.display=SFLpkViewer?'':'none'; if(!SFLpkViewer){setTimeout(function(){flyGift('🎁');},500);setTimeout(function(){flyGift('🥇');},1300);} }
    if((scr.fnum==='PK-04A'||scr.fnum==='PK-04C')&&SFLpkViewer){var _reb=mount.querySelector('.winbtns .re'); if(_reb)_reb.style.display='none'; var _exb=mount.querySelector('.winbtns .ex'); if(_exb)_exb.style.flex='1';}
    if(scr.fnum==='PV-01'){applyPredDone(mount);}
    if(scr.fnum==='G-05'){ var _pf=mount.querySelector('.pv-fan'),_pm=mount.querySelector('.pv-mgr'); if(_pf)_pf.style.display=SFLmgrMode?'none':''; if(_pm)_pm.style.display=SFLmgrMode?'block':'none'; var _rm=mount.querySelector('.rolemgr'); if(_rm)_rm.style.display=SFLmgrMode?'':'none'; }
    if(scr.fnum==='G-02'||scr.fnum==='J2-16'||scr.fnum==='J2-10'||scr.fnum==='J2-15'){SFLmember=true;}
    if(/^[1-9]$|^1[0-6]$|^[1-9][a-z]$/.test(scr.fnum)||scr.fnum==='G-02G'){SFLmember=false;}
    scap.textContent=(scr.cap||'').slice(0,46);
    ct.textContent=(curS+1)+' / '+v.screens.length;
    var c2=document.getElementById('counter2');if(c2)c2.textContent=ct.textContent;
    jsel.value=curJ;
    var d=''; for(var i=0;i<v.screens.length;i++) d+='<span class="ppdot'+(i===curS?' on':'')+'"></span>'; dotbar.innerHTML=d;
    fit();
  }
  function next(){var v=VIEWS[curJ]; if(curS<v.screens.length-1){curS++;} else if(curJ<VIEWS.length-1){curJ++;curS=0;} render();}
  function prev(){if(curS>0){curS--;} else if(curJ>0){curJ--;curS=VIEWS[curJ].screens.length-1;} render();}
  document.getElementById('bnext2').onclick=next; document.getElementById('bprev2').onclick=goBack;
  document.getElementById('bnext').onclick=next; document.getElementById('bprev').onclick=goBack;
  jsel.onchange=function(){curJ=+jsel.value;curS=0;render();};
  document.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();next();}else if(e.key==='ArrowLeft'){goBack();}});
  var tx=0; var stage=document.getElementById('stage');
  stage.addEventListener('touchstart',function(e){tx=e.changedTouches[0].clientX;},{passive:true});
  stage.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>45){dx<0?next():prev();}},{passive:true});
  var MULTI='.tchip,.chip', SINGLE='.fchip,.lchip,.tab,.dtab,.segopt,.reasonopt,.srcopt,.laopt,.opt,.giftopt,.pt,.sw,.em,.teamrow,.lgchip,.formcard', SEG='.seg,.tabs,.dtabs';
  function singleSel(el,grp){[].forEach.call(grp.children,function(c){if(c.classList)c.classList.remove('on');});el.classList.add('on');}
  var hist=[]; var SFLdone={}; var SFLpred=null; var SFLpredMatch='Red Devils'; var SFLpredScore='2–1'; var SFLvote={motm:null,award:null}; var SFLmember=false; var SFLpkViewer=false; var SFLchatGift=null; var SFLpickOrigin='vote'; var SFLfvActive=false; var SFLguest=false; var SFLmoveType='loan'; var SFLmgrMode=false; var ANCH={"home": [19, "G-02"], "profile": [19, "G-05"], "userprofile": [19, "G-05U"], "settings": [19, "G-05B"], "security": [19, "G-05C"], "deleteacct": [19, "G-05E"], "editprofile": [19, "G-05ED"], "changepw": [19, "G-05P"], "blockedusers": [19, "G-05BL"], "legal": [19, "G-05T"], "notifications": [19, "G-03"], "kyc": [19, "G-06A"], "support": [19, "G-07A"], "market": [5, "PL-01"], "myplayers":[5,"PL-06"], "plbuy":[5,"PL-03"], "plescrow":[5,"PL-04"], "plcomplete":[5,"PL-05"], "pllist":[5,"PL-07"], "pllistlive":[5,"PL-08"], "plsold":[5,"PL-10"], "plfilters":[5,"PL-01A"], "games": [16, 0], "gameshub": [16, "MG-01"], "gamerules": [16, "MG-01R"], "gamehistory": [16, "MG-05"], "penalty": [16, "MG-02"], "penaltygoal": [16, "MG-02G"], "penaltysaved": [16, "MG-02S"], "wheel": [16, "MG-03"], "wheelspin": [16, "MG-03A"], "wheelresult": [16, "MG-04C"], "giftresult": [16, "MG-04G"], "wallet": [12, 0], "coinstore": [2, "J3-02"], "selectrecipient": [2, "J3-03"], "reviewpurchase": [2, "J3-05"], "coinrecipientconfirm":[2,"J3-04"], "coinpayment":[2,"J3-06"], "coinprocessing":[2,"J3-07"], "coinsuccess":[2,"J3-08"], "coinreceipt":[2,"J3-09"], "coinboost":[2,"J3-10"], "club": [1, "J2-16"], "tasks": [3, "FT-01"], "taskdetail":[3,"FT-03"], "taskwatch":[3,"FT-03W"], "clubevents":[19,"EV-01"],"fvunlocked":[10,"FV-00"],"fvexplain":[10,"FV-01"],"fvconfirm":[10,"FV-02"],"fvprocessing":[10,"FV-03"],"fvsuccess":[10,"FV-04"],"fvdashboard":[10,"FV-05"],"fvhistory":[10,"FV-06"],"fvalready":[10,"FV-10"], "tasklocked":[3,"FT-04"], "taskverify":[3,"FT-05"], "taskcomplete":[3,"FT-06"], "taskclaim":[3,"FT-08"], "taskclaimed":[3,"FT-10"], "mystats":[3,"FT-11"], "predictions": [4, "PV-01"], "rewards": [15, 0], "managerhq": [13, "MC-01"], "mgrclubs":[13,"MC-00"], "mgrcommission":[13,"MC-01A"], "mgrfandetail":[13,"MC-04A"], "mgrremovefan":[13,"MC-04B"], "inbox": [18, 0], "newmessage": [18, "MSG-02"], "msgrequests": [18, "MSG-03"], "kitbag": [9, 0], "progression": [11, 0], "live": [20, 0],"convert":[12,"WA-02"],"gtransfer":[12,"WA-03"],"withdraw":[12,"WA-04A"],"wallethist":[12,"WA-05"],"walletrules":[12,"WA-01A"],"convertconfirm":[12,"WA-02B"],"convertdone":[12,"WA-02D"],"transferamount":[12,"WA-03A"],"transferconfirm":[12,"WA-03B"],"kycverify":[12,"KYC-01"],"kycdoc":[12,"KYC-02"],"kycselfie":[12,"KYC-03"],"withdrawconfirm":[12,"WA-04C"],"withdrawproc":[12,"WA-04D"],"txdetail":[12,"WA-05A"],"move":[14,0],"movereq":[14,"ML-00"],"createoffer":[14,"ML-01"],"reviewoffer":[14,"ML-01A"],"offersent":[14,"ML-01S"],"fanconsentloan":[14,"ML-02"],"fanconsentperm":[14,"ML-02P"],"acceptconfirm":[14,"ML-02A"],"moveoffer":[14,"ML-02"],"moveproc":[14,"ML-03"],"transfercomplete":[14,"ML-03A"],"loanactive":[14,"ML-03B"],"loanreturn":[14,"ML-03C"],"termschanged":[14,"ML-X1"],"offerexpired":[14,"ML-X2"],"offerdeclined":[14,"ML-X3"],"tasksdaily":[3,"FT-01"],"tasksweekly":[3,"FT-02"],"tasksdone":[3,"FT-07"],"tasksweeklydone":[3,"FT-07W"],"watch":[17,0],"golive":[6,"GL-01A"],"stadiumhub":[6,"GL-00"],"eligibility":[6,"GL-01A"],"permissions":[6,"GL-01B"],"golivesetup":[6,"GL-01"],"formation":[6,"GL-02"],"prelive":[6,"GL-02A"],"manageseats":[6,"GL-04"],"manageparticipant":[6,"GL-04A"],"endlive":[6,"GL-06"],"livesummary":[6,"GL-07"],"pk":[8,"PK-00"],"pkmatch":[8,"PK-01"],"pkincoming":[8,"PK-01C"],"pkmatchup":[8,"PK-01E"],"pkside":[8,"PK-03A"],"pkleadchange":[8,"PK-03B"],"pkfinalizing":[8,"PK-03D"],"pkwin":[8,"PK-04A"],"pkdraw":[8,"PK-04C"],"register":[0,"3"],"signin":[0,"10"],"clubs":[1,"J2-02"],"guesthome":[19,"G-02G"],"guestregister":[1,"J2-22"],"guestlive":[6,"GL-03Vg"],"gate":[19,"GATE-01"],"clubsearch":[1,"J2-03"],"clubapplications":[1,"J2-08"],"clubinvite":[1,"J2-13"],"clubdecline":[1,"J2-14"],"clubinviteaccepted":[1,"J2-15"],"clubleave":[1,"J2-18"],"clubleaveconfirm":[1,"J2-19"],"clubleft":[1,"J2-20"],"league":[11,"PR-02"],"prohub":[11,"PR-00"],"fanlevel":[11,"PR-01"],"tournament":[11,"PR-03"],"clubgrade":[11,"PR-04"],"prizeeligibility":[11,"PR-04B"],"howtoearn":[11,"PR-01A"],"levelroadmap":[11,"PR-01B"],"clubdetail":[1,"J2-05"],"clubapply":[1,"J2-06"],"vote":[4,"PV-05"],"awards":[4,"PV-08"],"predictscore":[4,"PV-02"],"predictconfirm":[4,"PV-03"],"predictdone":[4,"PV-04"],"picksubmitted":[4,"PV-07"],"awardcandidates":[4,"PV-09"],"matchlive":[4,"PV-11"],"predictwin":[4,"PV-12"],"predictclose":[4,"PV-12b"],"playerdetail":[5,"PL-02"],"chatthread":[18,"MSG-04"],"rewarddetail":[15,"RW-01A"],"rewardclaim":[15,"RW-01B"],"rewardsuccess":[15,"RW-01C"],"rewardreview":[15,"RW-01E"],"rewardinprog":[15,"RW-01D"],"rewardhistory":[15,"RW-01F"],"clubblocked":[1,"J2-13b"],"clubsubmitted":[1,"J2-07"],"clubconfirmed":[1,"J2-10"],"createclub":[24,"CC-01T"],"ccbasics":[24,"CC-01"],"ccidentity":[24,"CC-02"],"cctype":[24,"CC-03"],"ccagree":[24,"CC-04"],"ccreview":[24,"CC-05"],"cccreated":[24,"CC-06"],"mgrapplications":[13,"MC-05"],"mgrapprovals":[13,"MC-07"],"mgrapprovaldetail":[13,"MC-07D"],"clubchat":[18,"MSG-05"],"watchcomplete":[17,"CS-01C"],"choosestart":[0,"9"],"mgrfanlist":[13,"MC-04"],"mgrrecruit":[13,"MC-02"],"mgrshare":[13,"MC-02A"],"mgrinvitesent":[13,"MC-06R"],"mgrhistory":[13,"MC-02H"],"mgraddid":[13,"MC-06"],"mgrrewards":[13,"MC-03"],"mgrbreakdown":[13,"MC-01B"],"liveroom":[6,"GL-03V"],"squadroom":[6,"GL-05"],"giftmenu":[9,"GK-01"],"giftdetailq":[9,"GK-01A"],"giftconfirm":[9,"GK-01B"],"giftsending":[9,"GK-01D"],"giftsent":[9,"GK-01E"],"confirmseat":[6,"GL-05A"],"fanseated":[6,"GL-05B"],"seattaken":[6,"GL-05C"],"guestgate":[6,"GL-03Vg"],"chatgift":[18,"MSG-06"],"pkrandom":[8,"PK-01A"],"pkinvite":[8,"PK-01B"],"pkcountdown":[8,"PK-02A"],"pkbattle":[8,"PK-03"],"pkrematch":[8,"PK-04D"],"liveroomhost":[6,"GL-03H"],"callvoice":[18,"CALL-01"],"callvideo":[18,"CALL-04"],"callsettings":[18,"MSG-08"],"callperm":[18,"CALL-P"],"callactivevoice":[18,"CALL-03"],"callmissed":[18,"CALL-05"],"callhistory":[18,"CALL-06"],"leaguespend":[11,"PR-02C"],"leagueprev":[11,"PR-02D"]};
  function idxOfFnum(j,fn){var a=(JOUR[j]&&JOUR[j].screens)||[];for(var i=0;i<a.length;i++)if(a[i].fnum===fn)return i;return 0;}
  var GUESTOK={guesthome:1,gate:1,clubs:1,clubdetail:1,clubsearch:1,guestlive:1,live:1,register:1,signin:1,notifications:1,guestregister:1,market:1,playerdetail:1,plfilters:1,liveroom:1,pkbattle:1,stadiumhub:1,userprofile:1,squadroom:1,confirmseat:1,fanseated:1,pkfinalizing:1,pkwin:1,pkdraw:1,pkleadchange:1,pkcountdown:1,pkmatchup:1};
  function goTo(a){
    if(a==='register'||a==='signin'){SFLguest=false;}
    if(a==='managerhq'||a==='mgrclubs'||a==='cccreated'||a.indexOf('mgr')===0){SFLmgrMode=true;}
    else if(a==='guesthome'||a==='clubconfirmed'||a==='clubinviteaccepted'){SFLmgrMode=false;}
    if(SFLguest){ if(a==='home'){a='guesthome';} else if(!GUESTOK[a]){a='gate';} }
    var d=ANCH[a]; if(!d)return false; hist.push({j:curJ,s:curS,html:mount.innerHTML}); curJ=FLOWN+d[0]; curS=(typeof d[1]==='number')?d[1]:idxOfFnum(d[0],d[1]); render(); return true;}
  function goBack(){ if(hist.length){var h=hist.pop(); curJ=h.j; curS=h.s; render(); if(h.html){mount.innerHTML=h.html;} var sc=VIEWS[curJ].screens[curS]||{}; SFLcoinify(mount); SFLcrest(mount); SFLchat(mount); if(sc.fnum==='FT-01'||sc.fnum==='FT-02'){applyTaskDone(mount);} if(sc.fnum==='PV-01'){applyPredDone(mount);} if(sc.fnum==='PV-05'){applyVoteDone(mount,'motm');} if(sc.fnum==='PV-09'){applyVoteDone(mount,'award');} } else prev(); }
  function endCall(){ while(hist.length){ var _t=hist[hist.length-1]; var _f=((VIEWS[_t.j]&&VIEWS[_t.j].screens[_t.s])||{}).fnum||''; if(_f.indexOf('CALL')===0){hist.pop();} else break; } if(hist.length){goBack();} else {goTo('chatthread');} }
  function cleanTo(anchor, re){ while(hist.length){var _ch=hist[hist.length-1];var _cff=((VIEWS[_ch.j]&&VIEWS[_ch.j].screens[_ch.s])||{}).fnum||'';if(re.test(_cff)){hist.pop();}else break;} var _cd=ANCH[anchor]; if(!_cd)return; curJ=FLOWN+_cd[0]; curS=(typeof _cd[1]==='number')?_cd[1]:idxOfFnum(_cd[0],_cd[1]); render(); }
  function jumpTab(anchor){ var _jd=ANCH[anchor]; if(!_jd)return; curJ=FLOWN+_jd[0]; curS=(typeof _jd[1]==='number')?_jd[1]:idxOfFnum(_jd[0],_jd[1]); render(); }
  function returnTo(fnum, anchor){ while(hist.length){ var _rt=hist[hist.length-1]; var _rf=((VIEWS[_rt.j]&&VIEWS[_rt.j].screens[_rt.s])||{}).fnum||''; if(_rf===fnum){ goBack(); return; } hist.pop(); } if(anchor)goTo(anchor); }
  function applyTaskDone(root){
    var rows=root.querySelectorAll('.trow'), added=0;
    rows.forEach(function(r){var tt=r.querySelector('.tt'); if(!tt)return; var k=tt.textContent.trim();
      if(SFLdone[k] && !r.classList.contains('complete')){ r.classList.add('complete'); var side=r.querySelector('.side'); if(side){side.innerHTML='<div class="done">\u2713</div>';} added++; }});
    if(added){ var fr=root.querySelector('.frac'); if(fr){ var mm=fr.textContent.match(/(\d+)\s*\/\s*(\d+)/); var base=mm?+mm[1]:0, tot=mm?+mm[2]:6; var n=Math.min(tot, base+added); fr.innerHTML=n+'<small>/'+tot+'</small>'; var pc=root.querySelector('.pct'); if(pc)pc.textContent=Math.round(n/tot*100)+'%'; } }
  }
  function applyPredDone(root){
    if(!SFLpred)return;
    var cards=root.querySelectorAll('.fixcard');
    cards.forEach(function(c){
      var tns=c.querySelectorAll('.tn'); var names=[].map.call(tns,function(n){return n.textContent;}).join(' ');
      if(names.indexOf(SFLpred.match)>=0){
        var cta=c.querySelector('.cta2'); if(cta&&!cta.querySelector('.yourpick')){cta.innerHTML='<div class="yourpick">✓ Your pick: '+SFLpred.score+' · Awaiting match</div>';}
      }
    });
  }
  function selCand(cd){ var grid=cd.parentElement; [].forEach.call(grid.querySelectorAll('.cand'),function(c){ c.classList.remove('on'); var s=c.querySelector('.sel'); if(s)s.remove(); var r=c.querySelector('.radio'); if(r)r.style.visibility=''; }); cd.classList.add('on'); if(!cd.querySelector('.sel')){ var s=document.createElement('div'); s.className='sel'; s.textContent='✓'; cd.insertBefore(s,cd.firstChild); } }
  function applyVoteDone(root, which){
    var v=SFLvote[which]; if(!v)return;
    [].forEach.call(root.querySelectorAll('.cand'),function(c){
      var n=((c.querySelector('.n')||{}).textContent||'').trim();
      var on=(n===v);
      c.classList.toggle('on',on);
      var sel=c.querySelector('.sel');
      if(on){ if(!sel){sel=document.createElement('div');sel.className='sel';sel.textContent='✓';c.insertBefore(sel,c.firstChild);} c.style.opacity=''; }
      else { if(sel)sel.remove(); c.style.opacity='.55'; }
      var rad=c.querySelector('.radio'); if(rad)rad.style.visibility=on?'':'hidden';
    });
    var btn=root.querySelector('.btn'); if(btn){ btn.innerHTML='✓ You voted · '+v; }
    var open=root.querySelector('[style*="var(--green1)"]'); if(open&&/voting open/i.test(open.textContent||'')){ open.innerHTML='✓ Vote locked · you voted for '+v; }
  }
  function destOf(t){
    if(t.closest('.coinpill'))return 'coinstore';
    if(t.closest('.hqbtn'))return 'managerhq';
    var nav=t.closest('.sfl-nav .nit,.sfl-nav .nc,.navpill .nav,.navpill .navc'); if(nav){var n=nav.textContent.toLowerCase(); if(n.indexOf('home')>=0)return 'home'; if(n.indexOf('market')>=0)return 'market'; if(n.indexOf('stadium')>=0||n.indexOf('live')>=0)return 'live'; if(n.indexOf('games')>=0)return 'games'; if(n.indexOf('chat')>=0)return 'inbox'; if(n.indexOf('wallet')>=0)return 'wallet'; return null;}
    var hic=t.closest('.hicon'); if(hic){var e=hic.textContent; if(e.indexOf('🔔')>=0)return 'notifications'; if(e.indexOf('💬')>=0)return 'inbox';}
    if(t.closest('.ha')||t.closest('.selavatar'))return 'profile';
    var lab=t.closest('.btn,.dbtn,.lbtn,.short,.mod,.tile,.tplay,.listrow,.rolerow,.pjoin,.ab,.mgo,.cgo,.gj,.rw,.cat,.reccard,.mbanner,.clubcard,.hqbtn,.nrow,.txrow,.hrow,.crow,.callrow,.qt,.mom,.hjoin,.nextfix,.hfol,.livecard,.act,.explorelink,a'); var x=(lab?lab.textContent:'').toLowerCase();
    var K=[['go live','golive'],['join a pk','pk'],['pk battle','pk'],['start a pk','pk'],['matchday','live'],['watchalong','live'],['join live','live'],['north stand','live'],['watch sfl','watch'],['watch','watch'],['make a prediction','predictions'],['predict','predictions'],['transfer gold','gtransfer'],['send gold','gtransfer'],['gold transfer','gtransfer'],['convert','convert'],['withdraw','withdraw'],['buy coins','coinstore'],['coin store','coinstore'],['top up','coinstore'],['manager hq','managerhq'],['manager dashboard','managerhq'],['open hq','managerhq'],['enter hq','managerhq'],['kit bag','kitbag'],['reward ready','rewards'],['ready to claim','rewards'],['see winners','rewards'],['monthly winners','rewards'],['claim','rewards'],['rewards','rewards'],['you won','rewards'],['invited you','club'],['invitation','club'],['application','club'],['open club','club'],['club home','club'],['view club','club'],['other clubs','clubs'],['explore other','clubs'],['browse clubs','clubs'],['discover clubs','clubs'],['explore clubs','clubs'],['find a club','clubs'],['join a fan club','clubs'],['join a club','clubs'],['join club','clubs'],['gold received','wallethist'],['sent you','wallethist'],['refund','wallethist'],['transaction','wallethist'],['loan offer','moveoffer'],['transfer offer','moveoffer'],['loan/transfer','move'],['awaiting fan consent','moveproc'],['move status','moveproc'],['loan activated','loanactive'],['loan completed','loanreturn'],['join live','live'],['watchalong','live'],['matchday','live'],['north stand','live'],['pk battle','live'],['go live','live'],['watch party','live'],['stadium','live'],['live room','live'],['notification','notifications'],['messages','inbox'],['message','inbox'],['chat','inbox'],['prediction','predictions'],['tasks','tasks'],['duties','tasks'],['progression','progression'],['fan level','progression'],['verify identity','kyc'],['kyc','kyc'],['withdrawals unlocked','kyc'],['contact support','support'],['get support','support'],['report a problem','support'],['raise dispute','support'],['my players','market'],['player market','market'],['escrow','market'],['market','market'],['edit profile','profile'],['my stats','profile'],['wallet','wallet'],['games','games']];
    for(var i=0;i<K.length;i++){if(x.indexOf(K[i][0])>=0)return K[i][1];}
    return null;
  }
  stage.addEventListener('click',function(e){
    var mEl=document.getElementById('scaler').firstElementChild; if(!mEl||!mEl.contains(e.target))return;
    var t=e.target;
    if(t.closest('.sfl-statusbar'))return;
    var _navEl=t.closest('.sfl-nav .nit,.sfl-nav .nc,.navpill .nav,.navpill .navc'); if(_navEl){var _n=(_navEl.textContent||'').toLowerCase(); if(_n.indexOf('home')>=0){goTo(SFLguest?'guesthome':'home');} else if(_n.indexOf('market')>=0){goTo('market');} else if(_n.indexOf('stadium')>=0||_n.indexOf('live')>=0){goTo('live');} else if(_n.indexOf('games')>=0){goTo(SFLguest?'gate':'games');} else if(_n.indexOf('chat')>=0){goTo(SFLguest?'gate':'inbox');} else if(_n.indexOf('wallet')>=0){goTo('wallet');} return;}
    if(t.closest('.coinbal')){goTo('wallet');return;}
    if(t.closest('.statgrid')){return;}
    var _cf=(VIEWS[curJ].screens[curS]||{}).fnum||'';
    if(_cf==='1'){ if(!t.closest('.btn,.altlink,a')){next();return;} }
    if(_cf==='G-03'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.ico')){[].forEach.call(mEl.querySelectorAll('.unread'),function(u){u.style.display='none';}); sflToast('All notifications marked read'); return;} var _nfc=t.closest('.fchip'); if(_nfc){singleSel(_nfc,_nfc.parentElement);return;} }
    if(_cf==='MSG-01'){var _rq=t.closest('.fchip'); if(_rq&&/request/i.test(_rq.textContent)){goTo('msgrequests');return;}}
    if(t.closest('.pkcard')){SFLpkViewer=true;goTo('pkbattle');return;}
    var _dvc=t.closest('.filters .fchip'); if(_dvc&&mEl.querySelector('.pkcard')){ singleSel(_dvc,_dvc.parentElement); var _pk=/pk/i.test(_dvc.textContent); var _dh=mEl.querySelector('.hero'); if(_dh)_dh.style.display=_pk?'none':''; [].forEach.call(mEl.querySelectorAll('.rcard'),function(r){var _isp=r.classList.contains('pkcard'); r.style.display=(_pk?_isp:!_isp)?'':'none';}); var _rh=mEl.querySelector('.rowhead .t'); if(_rh)_rh.textContent=_pk?'Live PK battles':'Rooms heating up'; return; }
    if(_cf==='CC-01T'){var lgc=t.closest('.lgchip'); if(lgc){var grp=lgc.parentElement; [].forEach.call(grp.children,function(c){c.classList&&c.classList.remove('on');}); lgc.classList.add('on'); var key=lgc.getAttribute('data-league')||''; [].forEach.call(mEl.querySelectorAll('.lgroup'),function(g){g.style.display=(!key||g.getAttribute('data-league')===key)?'':'none';}); return;}}
    var ffc=t.closest('.filters .fchip'); if(ffc){var fgrp=ffc.parentElement;[].forEach.call(fgrp.children,function(c){c.classList&&c.classList.remove('on');});ffc.classList.add('on');var fl=(ffc.textContent||'').toLowerCase();var fk=/follow/.test(fl)?'following':/premier/.test(fl)?'prem':/champion/.test(fl)?'champions':'';var rc=mEl.querySelectorAll('.carousel .rcard, .rcard');[].forEach.call(rc,function(r){var cats=(r.getAttribute('data-cat')||'');r.style.display=(!fk||cats.indexOf(fk)>=0)?'':'none';});return;}
    if(_cf==='RW-01'){var bchip=t.closest('.chip'); if(bchip&&bchip.querySelector('.cv')){goTo('wallet');return;}}
    if(_cf.indexOf('J3-')===0){
      var _j3bk=t.closest('.top .back'); if(_j3bk){var _j3t=(_j3bk.textContent||'').trim(); if(/🧾/.test(_j3t)){goTo('coinreceipt');return;} if(/↗/.test(_j3t)){sflToast('Sharing receipt…');return;} goBack(); return;}
      if(_cf==='J3-01'){ if(t.closest('.btn')){goTo('register');return;} return; }
      if(_cf==='J3-02'){ if(t.closest('.ch')){goTo('selectrecipient');return;} var _pk=t.closest('.pkg'); if(_pk){[].forEach.call(_pk.parentElement.children,function(c){c.classList&&c.classList.remove('on');});_pk.classList.add('on');return;} if(t.closest('.btn')){goTo('reviewpurchase');return;} return; }
      if(_cf==='J3-03'){ var _sg=t.closest('.segtabs i'); if(_sg){singleSel(_sg,_sg.parentElement);return;} if(t.closest('.btn')){goTo('coinrecipientconfirm');return;} return; }
      if(_cf==='J3-04'){ var _b4=t.closest('.btn'); if(_b4){ if(/search again/i.test(_b4.textContent)){goBack();return;} goTo('reviewpurchase');return;} return; }
      if(_cf==='J3-05'){ if(t.closest('.confirm')){t.closest('.confirm').classList.toggle('on');return;} if(t.closest('.btn')){goTo('coinpayment');return;} return; }
      if(_cf==='J3-06'){ if(t.closest('.btn')){goTo('coinprocessing');return;} return; }
      if(_cf==='J3-07'){ goTo('coinsuccess'); return; }
      if(_cf==='J3-08'){ var _b8=t.closest('.btn'); if(_b8){ if(/receipt/i.test(_b8.textContent)){goTo('coinreceipt');return;} while(hist.length){var _j8=hist[hist.length-1];var _j8f=((VIEWS[_j8.j]&&VIEWS[_j8.j].screens[_j8.s])||{}).fnum||'';if(/^J3-/.test(_j8f)){hist.pop();}else break;} goBack(); return;} return; }
      if(_cf==='J3-09'){ if(t.closest('.link')){goTo('support');return;} if(t.closest('.btn')){sflToast('Receipt downloaded');return;} return; }
      if(_cf==='J3-10'){ var _b10c=t.closest('.btn,.link'); if(_b10c){ if(/later/i.test(_b10c.textContent)){goTo('home');return;} goTo('fvconfirm');return;} return; }
      if(_cf==='J3-11'){ var _b11=t.closest('.btn,.link'); if(_b11){ if(/support/i.test(_b11.textContent)){goTo('support');return;} if(/another method/i.test(_b11.textContent)){goTo('coinpayment');return;} goTo('reviewpurchase');return;} return; }
      if(_cf==='J3-12'){ var _b12=t.closest('.btn'); if(_b12){ if(/coin store/i.test(_b12.textContent)){goTo('coinstore');return;} goTo('reviewpurchase');return;} return; }
      if(_cf==='J3-13'){ var _b13=t.closest('.btn'); if(_b13){ if(/background/i.test(_b13.textContent)){goTo('home');return;} goTo('coinsuccess');return;} return; }
      if(_cf==='J3-14'){ var _b14c=t.closest('.btn,.link'); if(_b14c){ if(/support/i.test(_b14c.textContent)){goTo('support');return;} goTo('coinsuccess');return;} return; }
      if(_cf==='J3-15'){ var _b15=t.closest('.btn'); if(_b15){ if(/return to app/i.test(_b15.textContent)){goTo('home');return;} goTo('coinstore');return;} return; }
      if(_cf==='J3-16'){ if(t.closest('.btn')){goTo('coinreceipt');return;} return; }
      if(_cf==='J3-17'){ if(t.closest('.link')){goTo('support');return;} if(t.closest('.btn')){goTo('coinreceipt');return;} return; }
    }
    if(_cf==='MSG-01'){ if(t.closest('.search')){goTo('newmessage');return;} var msgico=t.closest('.ico'); if(msgico){ if(/✎/.test(msgico.textContent)){goTo('newmessage');return;} if(/⚙/.test(msgico.textContent)){goTo('callsettings');return;} }}
    if(_cf==='MSG-06'){ if(t.closest('.btn')){ var _ge=mEl.querySelector('.giftopt.on .ge'),_gnn=mEl.querySelector('.giftopt.on .gn'),_gcc=mEl.querySelector('.giftopt.on .gc'); SFLchatGift={em:(_ge?_ge.textContent:'🎁').trim(),gn:(_gnn?_gnn.textContent:'Gift').trim(),gp:(_gcc?_gcc.textContent:'').replace(/[^0-9]/g,'')}; while(hist.length){var _h=hist[hist.length-1];var _hf=((VIEWS[_h.j]&&VIEWS[_h.j].screens[_h.s])||{}).fnum||'';if(_hf==='MSG-06'||_hf==='MSG-04'){hist.pop();}else break;} var _dc=ANCH['chatthread']; curJ=FLOWN+_dc[0]; curS=idxOfFnum(_dc[0],_dc[1]); render(); return;} }
    if(_cf==='G-05U'){ var _ub=t.closest('.back'); if(_ub){ if(/‹|←/.test(_ub.textContent)){goBack();} return; } if(t.closest('.umsg')){goTo('chatthread');return;} if(t.closest('.ugift')){goTo('giftmenu');return;} var _uf=t.closest('.ufollow'); if(_uf){ if(SFLguest){goTo('gate');return;} var _un=((mEl.querySelector('.pn')||{}).textContent||'this fan').replace(/[✓✔]/g,'').trim(); var _on=/following/i.test(_uf.textContent); _uf.textContent=_on?'Follow':'Following'; _uf.style.background=_on?'#C9FF3D':'rgba(255,255,255,.18)'; _uf.style.color=_on?'#0A1400':'#fff'; sflToast(_on?('Unfollowed '+_un):('Following '+_un)); return;} if(t.closest('.listrow')){return;} }
    if(_cf==='GATE-01'){ if(t.closest('.top .back')||t.closest('.altlink')){goBack();return;} var _gt=t.closest('.btn'); if(_gt){ if(/sign in/i.test(_gt.textContent)){goTo('signin');return;} goTo('register');return;} return; }
    if(_cf==='G-05ED'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.epphoto')){showPhotoSheet();return;} if(t.closest('.epname')){return;} if(t.closest('.btn')){goBack();sflToast('Profile updated');return;} return; }
    if(_cf==='G-05'){ if(t.closest('.pt .back')){goTo('editprofile');return;} if(t.closest('.mgo')){goTo('managerhq');return;} if(t.closest('.rgo')){goTo('managerhq');return;} var _ml=t.closest('.mgrlink'); if(_ml){goTo(_ml.getAttribute('data-go'));return;} if(t.closest('.rolerow')){return;} if(t.closest('.levelcard')){goTo('fanlevel');return;} var _p5=t.closest('.listrow'); if(_p5){var _p5t=(_p5.textContent||'').toLowerCase(); if(/wallet/.test(_p5t)){goTo('wallet');return;} if(/kit bag/.test(_p5t)){goTo('kitbag');return;} if(/kyc/.test(_p5t)){goTo('kyc');return;} if(/settings/.test(_p5t)){goTo('settings');return;} return;} return; }
    if(_cf==='G-05B'){ if(t.closest('.top .back')){goBack();return;} var _sw=t.closest('.sw'); if(_sw){_sw.classList.toggle('on');return;} var _sl=t.closest('.listrow'); if(_sl){var _st=(_sl.textContent||'').toLowerCase(); if(/email/.test(_st)){showEditSheet('Email','z•••@gmail.com','We\\'ll send a verification link to confirm.');return;} if(/phone/.test(_st)){showEditSheet('Phone','+44 •••• ••• 021','We\\'ll text a verification code.');return;} if(/change password/.test(_st)){goTo('changepw');return;} if(/active devices/.test(_st)){goTo('security');return;} if(/blocked/.test(_st)){goTo('blockedusers');return;} if(/language/.test(_st)){showLanguageSheet();return;} if(/delete account/.test(_st)){goTo('deleteacct');return;} if(/log out/.test(_st)){showLogoutSheet();return;} if(/terms|privacy|guidelines/.test(_st)){goTo('legal');return;} return;} return; }
    if(_cf==='G-05P'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.pwfield')){return;} if(t.closest('.btn')){goBack();sflToast('Password updated');return;} return; }
    if(_cf==='G-05BL'){ if(t.closest('.top .back')){goBack();return;} var _bl=t.closest('.blbtn'); if(_bl){var _row=t.closest('.blrow'); var _nm=((_row.querySelector('div')||{}).textContent||'User'); if(_row)_row.remove(); sflToast('Unblocked'); return;} return; }
    if(_cf==='G-05T'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.listrow')){var _lg=(t.closest('.listrow').textContent||'').trim(); sflToast('Opening '+_lg+'…');return;} return; }
    if(_cf==='G-05C'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){sflToast('Account secured');return;} if(t.closest('.listrow')){return;} return; }
    if(_cf==='G-05E'){ if(t.closest('.top .back')){goBack();return;} var _de=t.closest('.btn,.altlink'); if(_de){ if(/resolve/i.test(_de.textContent)){goBack();return;} sflToast('Deletion request submitted');return;} return; }
    if(_cf==='MSG-02'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.search')){return;} if(t.closest('.uresult')||t.closest('.act')){goTo('chatthread');return;} return; }
    if(_cf==='MSG-03'){ var _rc=t.closest('.reqcard'); if(_rc&&(t.closest('.btn')||/block\s*&?\s*report/i.test(t.textContent||''))){ _rc.remove(); var _left=mEl.querySelectorAll('.reqcard').length; if(!_left){var _sc=mEl.querySelector('.scroll'); if(_sc)_sc.innerHTML='<div class="dnote info" style="margin-top:20px">No pending requests. You\\'re all caught up.</div>';} return; } }
    if((_cf==='MSG-04'||_cf==='MSG-05'||_cf==='MSG-04B')&&t.closest('.msgs')){return;}
    if(_cf.indexOf('MG-')===0){
      var MGRESULT={'MG-02G':1,'MG-02S':1,'MG-04C':1,'MG-04G':1,'MG-01X':1,'MG-REC':1,'MG-REF':1,'MG-LIM':1};
      var mgbk=t.closest('.top .back'); if(mgbk){var mb=(mgbk.textContent||'').trim(); if(/📜/.test(mb)){goTo('gamehistory');return;} if(mb==='?'){goTo('gamerules');return;} if(/[‹←]/.test(mb)){ if(MGRESULT[_cf]){goTo('gameshub');} else {goBack();} return; }}
      if(_cf==='MG-01'){ var bchip=t.closest('.balchip'); if(bchip){ if(bchip.querySelector('.gc')){goTo('wallet');} return; } if(t.closest('.tile.penalty')){goTo('penalty');return;} if(t.closest('.tile.wheel')){goTo('wheel');return;} }
      if(_cf==='MG-01R'){ if(t.closest('.btn')){goBack();return;} }
      if(_cf==='MG-01X'){ var xb=t.closest('.btn'); if(xb){ if(/buy coins/i.test(xb.textContent)){goTo('coinstore');return;} goTo('penalty');return; } }
      if(_cf==='MG-02'){ var z=t.closest('.zone'); if(z&&z.parentElement){singleSel(z,z.parentElement);return;} if(t.closest('.altlink')){goTo('gamerules');return;} if(t.closest('.btn')||t.closest('.ball')||t.closest('.pitch')){goTo('penaltygoal');return;} }
      if(_cf==='MG-02G'){ if(t.closest('.btn')){goTo('penalty');return;} if(t.closest('.altlink')){goTo('gameshub');return;} }
      if(_cf==='MG-02S'){ if(t.closest('.btn')){goTo('penalty');return;} if(t.closest('.altlink')){goTo('gameshub');return;} }
      if(_cf==='MG-03'){ if(t.closest('.btn')){goTo('wheelspin');return;} }
      if(_cf==='MG-03A'){ goTo('wheelresult');return; }
      if(_cf==='MG-04C'){ if(t.closest('.btn')){goTo('wheel');return;} if(t.closest('.altlink')){goTo('gameshub');return;} }
      if(_cf==='MG-04G'){ if(t.closest('.btn')){goTo('kitbag');return;} if(t.closest('.altlink')){goTo('gameshub');return;} }
      if(_cf==='MG-REC'){ if(t.closest('.btn')){goTo('gameshub');return;} }
      if(_cf==='MG-PEND'){ if(t.closest('.btn')){goTo('wheelresult');return;} if(t.closest('.altlink')){goTo('support');return;} }
      if(_cf==='MG-REF'){ if(t.closest('.btn')){goTo('gameshub');return;} }
      if(_cf==='MG-LIM'){ if(t.closest('.btn')){goTo('gamehistory');return;} if(t.closest('.altlink')){goTo('live');return;} }
      if(MGRESULT[_cf]){return;}
    }
    if(_cf.indexOf('CALL')===0){
      var clbk=t.closest('.top .back'); if(clbk){goBack();return;}
      if(_cf==='CALL-06'){ var crow=t.closest('.callrow'); if(crow){ var cbi=(crow.querySelector('.cb')||{}).textContent||''; goTo(/📹/.test(cbi)?'callvideo':'callvoice'); return; } }
      if(_cf==='CALL-P'){ var pb=t.closest('.btn'); if(pb){ goTo(/voice/i.test(pb.textContent)?'callactivevoice':'callvideo'); return; } if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='CALL-05'){ var m5=t.closest('.btn'); if(m5){ if(/call again/i.test(m5.textContent)){goTo('callvoice');}else{endCall();} return; } return; }
      var cc=t.closest('.cc'); if(cc){ var cb=cc.querySelector('.b'); var clab=(cc.textContent||'').toLowerCase();
        if(cb&&cb.classList.contains('accept')){goTo('callperm');return;}
        if(cb&&cb.classList.contains('end')){endCall();return;}
        if(/message/.test(clab)){endCall();return;}
        if(/video/.test(clab)){goTo('callvideo');return;}
        if(cb){cb.classList.toggle('on');} return; }
      if(_cf==='CALL-02'&&/reply with message/i.test(t.textContent||'')){endCall();return;}
      if(_cf==='CALL-01'){goTo('callactivevoice');return;}
      return;
    }
    if(t.closest('.hjoin')){goTo('liveroom');return;}
    var _seatEl=t.closest('.formfield .seat'); if(_seatEl&&!_seatEl.classList.contains('open')){ if(showSeatCard(_seatEl))return; }
    if(_cf==='GL-03V'){ if(t.closest('.rrb.join')){goTo('squadroom');return;} if(t.closest('.rrb.gift')){openGiftSheet();return;} if(t.closest('.seat.open')){goTo('confirmseat');return;} if(t.closest('.htool')){goTo('squadroom');return;} if(t.closest('.rsay')||t.closest('.cin')||t.closest('.rchat')){return;} return; }
    if(_cf==='GL-05'){ var _pr=t.closest('.posrow'); if(_pr){ if(_pr.querySelector('.pb.open')||_pr.querySelector('.opentag')){goTo('confirmseat');} return; } return; }
    if(_cf==='GL-05A'){ if(t.closest('.btn')){goTo('fanseated');return;} if(t.closest('.altlink')){goTo('squadroom');return;} return; }
    if(_cf==='GL-05B'){ if(t.closest('.rrb.gift')){openGiftSheet();return;} var _lv=t.closest('.rrb'); if(_lv){ if(/🚪|leave|end/i.test(_lv.textContent)){goTo('live');return;} _lv.classList.toggle('on'); return; } if(t.closest('.rsay')||t.closest('.cin')||t.closest('.rchat')){return;} return; }
    if(_cf==='GL-05C'){ if(t.closest('.btn')){goTo('squadroom');return;} if(t.closest('.altlink')){goTo('liveroom');return;} return; }
    if(_cf==='GL-03Vg'){ var _gb=t.closest('.b'); if(_gb){ if(/create/i.test(_gb.textContent)){goTo('register');return;} if(/sign in/i.test(_gb.textContent)){goTo('signin');return;} } if(t.closest('.altlink')){return;} return; }
    if(_cf==='GL-00'){ if(t.closest('.golivecard')){goTo(SFLguest?'gate':'eligibility');return;} if(t.closest('.roomcard')){goTo('liveroom');return;} var _t0=t.closest('.tab'); if(_t0){singleSel(_t0,_t0.parentElement);return;} }
    if(_cf==='GL-01A'){ if(t.closest('.btn')){goTo('permissions');return;} }
    if(_cf==='GL-01B'){ if(t.closest('.btn')){goTo('golivesetup');return;} if(t.closest('.allow')){return;} }
    if(_cf==='GL-01'){ if(t.closest('.btn')){goTo('formation');return;} var _sm=t.closest('.smcard'); if(_sm){singleSel(_sm,_sm.parentElement);return;} }
    if(_cf==='GL-02'){ if(t.closest('.btn')){goTo('prelive');return;} var _fcc=t.closest('.formcard'); if(_fcc){singleSel(_fcc,_fcc.parentElement);return;} }
    if(_cf==='GL-02A'){ if(t.closest('.rrb')||t.closest('.btn')){goTo('liveroomhost');return;} }
    if(_cf==='GL-03H'){ var _hr=t.closest('.rrb'); if(_hr){var _ht=_hr.textContent||''; if(/manage/i.test(_ht)){goTo('manageseats');return;} if(_hr.classList.contains('pk')||/⚔/.test(_ht)){goTo('pk');return;} if(_hr.classList.contains('gift')||/🎁/.test(_ht)){openGiftSheet();return;} if(/⏹|end|stop/i.test(_ht)){goTo('endlive');return;} return;} if(t.closest('.htool')){goTo('manageseats');return;} if(t.closest('.seat.open')){goTo('manageseats');return;} if(t.closest('.rchat')||t.closest('.rsay')||t.closest('.cin')){return;} }
    if(_cf==='GL-04'){ if(t.closest('.btn')){goTo('endlive');return;} var _orow=t.closest('.optrow'); if(_orow){ if(/·\s*open|close/i.test(_orow.textContent)){return;} goTo('manageparticipant');return;} var _t4=t.closest('.tab,.fillbadge'); if(_t4){singleSel(_t4,_t4.parentElement);return;} }
    if(_cf==='GL-04A'){ var _or=t.closest('.optrow'); if(_or){ var _ot=(_or.textContent||'').toLowerCase(); var _pn=((mEl.querySelector('.seathead .nm')||{}).textContent||'this fan').split('·')[0].trim();
      if(/block/.test(_ot)){goBack();sflToast(_pn+' removed & blocked');return;}
      if(/remove/.test(_ot)){goBack();sflToast(_pn+' removed from position');return;}
      if(/unmute/.test(_ot)){goBack();sflToast('Unmute requested from '+_pn);return;}
      if(/move/.test(_ot)){showMoveSheet(_pn);return;}
      if(/mute/.test(_ot)){goBack();sflToast(_pn+' muted');return;}
      goBack();return; } return; }
    if(_cf==='GL-06'){ var _eb=t.closest('.btn'); if(_eb){ if(/end/i.test(_eb.textContent)){goTo('livesummary');return;} goBack();return; } }
    if(_cf==='GL-07'){ if(t.closest('.altlink')){goTo('live');return;} if(t.closest('.btn')){sflToast('Highlights shared to your feed 🎬');return;} }
    if(_cf.indexOf('PK-')===0){
      var _pbk=t.closest('.top .back'); if(_pbk){goBack();return;}
      if(_cf==='PK-00'){ if(t.closest('.btn')){goTo('pkmatch');return;} if(t.closest('.altlink')){goTo('live');return;} return; }
      if(_cf==='PK-01'){ var _mc=t.closest('.modecard'); if(_mc){var _mct=(_mc.textContent||'').toLowerCase(); if(/quick/.test(_mct)){goTo('pkrandom');return;} if(/id/.test(_mct)){goTo('pkinvite');return;} goTo('live');return;} return; }
      if(_cf==='PK-01B'){ if(t.closest('.btn')){goTo('pkmatchup');return;} return; }
      if(_cf==='PK-01A'){ if(t.closest('.btn')){goTo('pkinvite');return;} if(/cancel search/i.test(t.textContent||'')){goTo('pkmatch');return;} goTo('pkmatchup'); return; }
      if(_cf==='PK-01C'){ var _ca=t.closest('.a'); if(_ca){ if(_ca.classList.contains('acc')||/accept/i.test(_ca.textContent)){goTo('pkcountdown');return;} goTo('live');return;} return; }
      if(_cf==='PK-01E'){ var _rb=t.closest('.b'); if(_rb){ if(_rb.classList.contains('ready')||/ready/i.test(_rb.textContent)){goTo('pkcountdown');return;} goTo('pkrandom');return;} return; }
      if(_cf==='PK-02A'){ goTo('pkbattle'); return; }
      if(_cf==='PK-03'){ if(t.closest('.gbtn')){goTo('pkside');return;} if(t.closest('.pktimer')||t.closest('.vid')||t.closest('.scrim')){goTo('pkfinalizing');return;} return; }
      if(_cf==='PK-03A'){ if(t.closest('.btn')){goTo('pkleadchange');return;} if(t.closest('.altlink')){goTo('coinstore');return;} var _gi=t.closest('.gi'); if(_gi){singleSel(_gi,_gi.parentElement);return;} return; }
      if(_cf==='PK-03B'){ goTo('pkfinalizing'); return; }
      if(_cf==='PK-03D'){ goTo('pkwin'); return; }
      if(_cf==='PK-04A'||_cf==='PK-04C'){ var _wb=t.closest('.b'); if(_wb){ if((_wb.classList.contains('re')||/rematch/i.test(_wb.textContent))&&!SFLpkViewer){goTo('pkrematch');return;} goTo('live');return;} return; }
      if(_cf==='PK-04D'){ if(t.closest('.btn')){goTo('pkcountdown');return;} if(t.closest('.altlink')){goTo('live');return;} return; }
    }
    if(_cf.indexOf('PL-')===0){
      var _plbk=t.closest('.top .back, .dnav .back'); if(_plbk){goBack();return;}
      if(_cf==='PL-00'){ if(t.closest('.btn')){goTo('market');return;} return; }
      if(_cf==='PL-01'){ if(t.closest('.plsearch')){goTo('plfilters');return;} if(t.closest('.pcard')){goTo('playerdetail');return;} var _pfc=t.closest('.fchip'); if(_pfc){singleSel(_pfc,_pfc.parentElement);return;} return; }
      if(_cf==='PL-01A'){ if(t.closest('.btn')){goBack();return;} var _pf2=t.closest('.fchip'); if(_pf2){singleSel(_pf2,_pf2.parentElement);return;} return; }
      if(_cf==='PL-02'){ if(t.closest('.btn')){goTo(SFLguest?'gate':'plbuy');return;} return; }
      if(_cf==='PL-02A'){ if(t.closest('.btn')){goTo('plbuy');return;} if(t.closest('.altlink')){goTo('market');return;} return; }
      if(_cf==='PL-03'){ if(t.closest('.btn')){goTo('plescrow');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PL-03A'){ var _b3=t.closest('.btn,.link'); if(_b3){ if(/buy coins/i.test(_b3.textContent)){goTo('coinstore');return;} goTo('market');return;} return; }
      if(_cf==='PL-04'){ if(t.closest('.link')){goTo('support');return;} goTo('plcomplete'); return; }
      if(_cf==='PL-04A'){ var _b4=t.closest('.btn,.link'); if(_b4){ if(/wallet/i.test(_b4.textContent)){goTo('wallet');return;} goTo('market');return;} return; }
      if(_cf==='PL-05'){ if(t.closest('.btn')){cleanTo('myplayers', /^PL-0[1-5]$/);return;} if(t.closest('.link')){cleanTo('market', /^PL-0[1-5]$/);return;} return; }
      if(_cf==='PL-06'){ if(t.closest('.prow')){goTo('pllist');return;} var _ptb=t.closest('.tabs i'); if(_ptb){singleSel(_ptb,_ptb.parentElement);return;} return; }
      if(_cf==='PL-07'){ if(t.closest('.btn')){goTo('pllistlive');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PL-08'){ var _pl8=t.closest('.btn')?'market':(t.closest('.link')?'myplayers':''); if(_pl8){ while(hist.length){var _hh=hist[hist.length-1];var _hf=((VIEWS[_hh.j]&&VIEWS[_hh.j].screens[_hh.s])||{}).fnum||'';if(_hf==='PL-06'||_hf==='PL-07'||_hf==='PL-08'){hist.pop();}else break;} var _dm=ANCH[_pl8]; curJ=FLOWN+_dm[0]; curS=(typeof _dm[1]==='number')?_dm[1]:idxOfFnum(_dm[0],_dm[1]); render(); return;} return; }
      if(_cf==='PL-09'){ goTo('plsold'); return; }
      if(_cf==='PL-10'){ var _b10=t.closest('.btn,.link'); if(_b10){ if(/wallet/i.test(_b10.textContent)){goTo('wallet');return;} goTo('market');return;} return; }
    }
    if(_cf.indexOf('FT-')===0){
      var _ftb=t.closest('.top .back, .dnav .back'); if(_ftb){ if(/🔔/.test(_ftb.textContent)){goTo('notifications');return;} if(/↗/.test(_ftb.textContent)){return;} goBack(); return; }
      if(_cf==='FT-00'){ if(t.closest('.btn')){goTo('register');return;} return; }
      if(_cf==='FT-01'||_cf==='FT-02'){
        var _ftab=t.closest('.tabs i'); if(_ftab){jumpTab(/week/i.test(_ftab.textContent)?'tasksweekly':'tasksdaily');return;}
        var _row=t.closest('.trow'); if(_row){ var _tt=((_row.querySelector('.tt')||{}).textContent||'').toLowerCase();
          if(/predict/.test(_tt)){goTo('predictions');return;}
          if(/award/.test(_tt)){goTo('awards');return;}
          if(/vote|motm|man of|woman of/.test(_tt)){goTo('vote');return;}
          if(/go live/.test(_tt)){goTo('golive');return;}
          if(/live stream|join a live/.test(_tt)){goTo('liveroom');return;}
          if(/pk|battle/.test(_tt)){goTo('pk');return;}
          if(/recruit/.test(_tt)){goTo('mgrrecruit');return;}
          if(/buy|sell|player/.test(_tt)){goTo('market');return;}
          if(/active day/.test(_tt)){goTo('progression');return;}
          if(/support/.test(_tt)){goTo('clubchat');return;}
          if(/event/.test(_tt)){goTo('clubevents');return;}
          if(/watch/.test(_tt)){goTo('taskdetail');return;}
          goTo('taskdetail'); return; }
        if(t.closest('.btn')){goTo(_cf==='FT-02'?'tasksweeklydone':'tasksdone');return;}
        if(t.closest('.ringhero')){return;}
      }
      if(_cf==='FT-03'){ if(t.closest('.btn')){goTo('taskwatch');return;} if(t.closest('.link')){return;} return; }
      if(_cf==='FT-03W'){ if(t.closest('.back')){goBack();return;} if(t.closest('.btn')){goTo('taskcomplete');return;} return; }
      if(_cf==='FT-04'){ if(t.closest('.btn')){goTo('coinstore');return;} return; }
      if(_cf==='FT-05'){ var _f5=t.closest('.btn'); if(_f5){ if(/other tasks/i.test(_f5.textContent)){goTo('tasks');return;} goTo('taskcomplete');return;} return; }
      if(_cf==='FT-06'){ if(t.closest('.btn')){goTo('tasks');return;} return; }
      if(_cf==='FT-07'||_cf==='FT-07W'){ if(t.closest('.btn')){goTo('taskclaim');return;} if(t.closest('.link')){goTo('tasks');return;} return; }
      if(_cf==='FT-08'){ if(t.closest('.btn')){goTo('taskclaimed');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='FT-10'){ var _f10=t.closest('.btn'); if(_f10){ if(/stats/i.test(_f10.textContent)){goTo('mystats');return;} cleanTo('home', /^FT-/);return;} return; }
      if(_cf==='FT-11'){ return; }
    }
    if(_cf.indexOf('PR-')===0){
      var _prbk=t.closest('.top .back'); if(_prbk){goBack();return;}
      if(_cf==='PR-02C'&&t.closest('.spr')){goTo('clubdetail');return;}
      if(t.closest('.lgr')||t.closest('.pod')||t.closest('.podium')||t.closest('.lgtable')||t.closest('.ttr')||t.closest('.ttable')||t.closest('.thd')||t.closest('.lgcount')||t.closest('.spendhero')||t.closest('.grouplabel')){return;}
      var _lgt2=t.closest('.lgtab'); if(_lgt2){var _lx2=_lgt2.textContent.toLowerCase(); if(/spend/.test(_lx2)){goTo('leaguespend');return;} if(/previous|prev/.test(_lx2)){goTo('leagueprev');return;} singleSel(_lgt2,_lgt2.parentElement); return;}
      var _ttb=t.closest('.ttab'); if(_ttb){singleSel(_ttb,_ttb.parentElement);return;}
      if(_cf==='PR-00'){ var _hc=t.closest('.hubcard'); if(_hc){ if(_hc.classList.contains('lvl')){goTo('fanlevel');return;} if(_hc.classList.contains('league')){goTo('league');return;} if(_hc.classList.contains('tour')){goTo('tournament');return;} if(_hc.classList.contains('grade')){goTo('clubgrade');return;} } return; }
      if(_cf==='PR-01'){ if(t.closest('.btn')){goTo('howtoearn');return;} if(t.closest('.altlink')){goTo('levelroadmap');return;} return; }
      if(_cf==='PR-04'){ if(t.closest('.btn,.altlink')){goTo('prizeeligibility');return;} return; }
      if(_cf==='PR-04B'){ if(t.closest('.btn')){goTo('rewards');return;} return; }
      if(_cf==='PR-02D'){ if(t.closest('.btn')){goBack();return;} return; }
      if(_cf==='PR-01C'){ var _c1c=t.closest('.btn,.altlink'); if(_c1c){ if(/benefit/i.test(_c1c.textContent)){goTo('levelroadmap');return;} goBack();return;} return; }
    }
    if(_cf.indexOf('WA-')===0||_cf.indexOf('KYC-')===0){
      var _wbk=t.closest('.top .back'); if(_wbk){ if(/🧾/.test(_wbk.textContent)){goTo('wallethist');return;} goBack(); return; }
      if(_cf==='WA-01'){ var _ab=t.closest('.ab'); if(_ab){var _at=_ab.textContent.toLowerCase(); if(/buy coins/.test(_at)){goTo('coinstore');return;} if(/convert/.test(_at)){goTo('convert');return;} if(/transfer/.test(_at)){goTo('gtransfer');return;} if(/withdraw/.test(_at)){goTo('withdraw');return;}} if(t.closest('.kycrow')){goTo('kycverify');return;} return; }
      if(_cf==='WA-01A'){ if(t.closest('.btn')){goBack();return;} return; }
      if(_cf==='WA-02'){ if(t.closest('.swapbtn')){return;} if(t.closest('.btn')){goTo('convertconfirm');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-02B'){ if(t.closest('.btn')){goTo('convertdone');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-02D'){ if(t.closest('.btn')){returnTo('WA-01','wallet');return;} if(t.closest('.altlink')){goTo('convert');return;} return; }
      if(_cf==='WA-03'){ if(t.closest('.btn')){goTo('transferamount');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-03A'){ if(t.closest('.btn')){goTo('transferconfirm');return;} return; }
      if(_cf==='WA-03B'){ if(t.closest('.btn')){returnTo('WA-01','wallet'); sflToast('200 Gold sent to Mikael K.'); return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-03F'){ var _f3=t.closest('.btn'); if(_f3){ if(/withdraw/i.test(_f3.textContent)){goTo('withdraw');return;} goTo('gtransfer');return;} return; }
      if(_cf==='KYC-01'){ if(t.closest('.btn')){goTo('kycdoc');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='KYC-02'){ if(t.closest('.btn')){goTo('kycselfie');return;} return; }
      if(_cf==='KYC-03'){ if(t.closest('.btn')){goTo('withdraw');return;} return; }
      if(_cf==='WA-04A'){ var _so=t.closest('.srcopt'); if(_so){singleSel(_so,_so.parentElement);return;} if(t.closest('.btn')){goTo('withdrawconfirm');return;} return; }
      if(_cf==='WA-04C'){ if(t.closest('.btn')){goTo('withdrawproc');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-04D'){ if(t.closest('.btn')){returnTo('WA-01','wallet');return;} return; }
      if(_cf==='WA-05'){ var _wfc=t.closest('.fchip'); if(_wfc){singleSel(_wfc,_wfc.parentElement);return;} if(t.closest('.txrow')){goTo('txdetail');return;} return; }
      if(_cf==='WA-05A'){ if(t.closest('.btn')){goTo('support');return;} return; }
    }
    if(_cf.indexOf('PV-')===0){
      var _pvbk=t.closest('.top .back'); if(_pvbk){goBack();return;}
      var _pvtab=t.closest('.tabs i'); if(_pvtab){var _pt=_pvtab.textContent.toLowerCase(); if(/vote/.test(_pt)){jumpTab('vote');return;} if(/award/.test(_pt)){jumpTab('awards');return;} jumpTab('predictions'); return;}
      if(_cf==='PV-00'){ if(t.closest('.btn')){goTo('register');return;} return; }
      if(_cf==='PV-01'){ var _fc=t.closest('.fixcard'); if(t.closest('.predict')){var _tn=_fc&&_fc.querySelector('.tn'); if(_tn)SFLpredMatch=_tn.textContent; goTo('predictscore');return;} if(_fc&&_fc.querySelector('.yourpick')){goTo('matchlive');return;} var _pfc=t.closest('.fchip'); if(_pfc){singleSel(_pfc,_pfc.parentElement);return;} return; }
      if(_cf==='PV-02'){ var _stb=t.closest('.step b'); if(_stb){ var _scEl=_stb.closest('.sc'); var _nb=_scEl&&_scEl.querySelector('.num-big'); if(_nb){ var _v=parseInt(_nb.textContent,10)||0; _v=/\+/.test(_stb.textContent)?Math.min(20,_v+1):Math.max(0,_v-1); _nb.textContent=_v; var _scs=mEl.querySelectorAll('.board .sc .num-big'); if(_scs.length>=2){ SFLpredScore=_scs[0].textContent+'–'+_scs[1].textContent; var _pr=mEl.querySelector('.pickrow .num'); if(_pr)_pr.textContent=_scs[0].textContent+' – '+_scs[1].textContent; } } return; } if(t.closest('.btn')){goTo('predictconfirm');return;} return; }
      if(_cf==='PV-03'){ if(t.closest('.btn')){goTo('predictdone');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PV-04'){ if(t.closest('.btn')||t.closest('.link')){ while(hist.length){var _ph=hist[hist.length-1];var _pf=((VIEWS[_ph.j]&&VIEWS[_ph.j].screens[_ph.s])||{}).fnum||'';if(/^PV-0[1-4]$/.test(_pf)){hist.pop();}else break;} var _dp=ANCH['predictions']; curJ=FLOWN+_dp[0]; curS=idxOfFnum(_dp[0],_dp[1]); render(); return;} return; }
      if(_cf==='PV-05'){ var _cd=t.closest('.cand'); if(_cd){ if(SFLvote.motm)return; selCand(_cd);return;} if(t.closest('.btn')){ if(SFLvote.motm){goTo('picksubmitted');return;} SFLvote.motm=((mEl.querySelector('.cand.on .n')||{}).textContent||'').trim()||'your pick'; SFLpickOrigin='vote';goTo('picksubmitted');return;} return; }
      if(_cf==='PV-07'){ if(t.closest('.btn')||t.closest('.link')){cleanTo(SFLpickOrigin==='awards'?'awards':'vote', /^PV-(05|07|09)$/);return;} return; }
      if(_cf==='PV-08'){ var _aw=t.closest('.award'); if(_aw){ if(_aw.querySelector('.voted')||/opacity:\.6/.test(_aw.getAttribute('style')||'')){return;} goTo('awardcandidates');return;} return; }
      if(_cf==='PV-09'){ var _cd9=t.closest('.cand'); if(_cd9){ if(SFLvote.award)return; selCand(_cd9);return;} if(t.closest('.btn')){ if(SFLvote.award){goTo('picksubmitted');return;} SFLvote.award=((mEl.querySelector('.cand.on .n')||{}).textContent||'').trim()||'your pick'; SFLpickOrigin='awards';goTo('picksubmitted');return;} return; }
      if(_cf==='PV-11'){ if(t.closest('.btn')){goTo('predictwin');return;} return; }
      if(_cf==='PV-12'){ if(t.closest('.link')){goTo('rewards');return;} if(t.closest('.btn')){goTo('wallet');return;} return; }
      if(_cf==='PV-12b'){ if(t.closest('.btn')){goTo('predictions');return;} return; }
      if(_cf==='PV-10'){ var _p10=t.closest('.btn,.link'); if(_p10){ if(/buy coins/i.test(_p10.textContent)){goTo('coinstore');return;} goTo('predictions');return;} return; }
      if(_cf==='PV-10b'){ if(t.closest('.btn')){goTo('predictions');return;} return; }
      if(_cf==='PV-13'){ if(t.closest('.btn')){goTo('wallet');return;} return; }
    }
    if(_cf.indexOf('CC-')===0){
      var _ccbk=t.closest('.top .back'); if(_ccbk){ if(_cf==='CC-01T'){goBack();} else {prev();} return; }
      if(t.closest('.searchbar')){return;}
      if(_cf==='CC-01T'){ var _lg=t.closest('.lgchip'); if(_lg){var _grp=_lg.parentElement;[].forEach.call(_grp.children,function(c){c.classList&&c.classList.remove('on');});_lg.classList.add('on');var _key=_lg.getAttribute('data-league')||'';[].forEach.call(mEl.querySelectorAll('.lgroup'),function(g){g.style.display=(!_key||g.getAttribute('data-league')===_key)?'':'none';});return;} var _tr=t.closest('.teamrow'); if(_tr){[].forEach.call(mEl.querySelectorAll('.teamrow'),function(r){r.classList.remove('on');});_tr.classList.add('on'); var _ub=mEl.querySelector('.cta .btn'); if(_ub){var _tn=(_tr.querySelector('.tn')||{}).textContent||''; _ub.textContent='Use '+_tn+' ›';} return;} if(t.closest('.btn')){goTo('ccbasics');return;} return; }
      if(_cf==='CC-01'){ if(t.closest('.chg')){goTo('createclub');return;} if(t.closest('.btn')){goTo('ccidentity');return;} return; }
      if(_cf==='CC-02'){ var _sw2=t.closest('.sw'); if(_sw2){singleSel(_sw2,_sw2.parentElement);return;} var _em=t.closest('.em'); if(_em){singleSel(_em,_em.parentElement);return;} if(t.closest('.btn')){goTo('cctype');return;} return; }
      if(_cf==='CC-03'){ var _so=t.closest('.segopt'); if(_so){singleSel(_so,_so.parentElement); var _inv=/invite/i.test(_so.textContent); var _io=mEl.querySelector('.invonly'),_po=mEl.querySelector('.pubonly'); if(_io)_io.style.display=_inv?'':'none'; if(_po)_po.style.display=_inv?'none':''; return;} var _tg=t.closest('.tog'); if(_tg){_tg.classList.toggle('off');return;} if(t.closest('.ilb')){sflToast('Invite link copied');return;} if(t.closest('.btn')){goTo('ccagree');return;} return; }
      if(_cf==='CC-04'){ var _ck=t.closest('.chk'); if(_ck){_ck.classList.toggle('off');return;} if(t.closest('.btn')){goTo('ccreview');return;} return; }
      if(_cf==='CC-05'){ if(t.closest('.btn')){goTo('cccreated');return;} return; }
      if(_cf==='CC-06'){ var _cli=t.closest('.cli'); if(_cli){var _ct=(_cli.textContent||'').toLowerCase(); if(/invite/.test(_ct)){goTo('mgrrecruit');return;} if(/task/.test(_ct)){goTo('tasks');return;} if(/go live/.test(_ct)){goTo('golive');return;} if(/prediction/.test(_ct)){goTo('predictions');return;} } if(t.closest('.btn')){goTo('managerhq');return;} return; }
    }
    if(_cf==='EV-01'){ if(t.closest('.back')){goBack();return;} var _ev=t.closest('.evcard'); if(_ev&&t.closest('.evjoin')){var _et=(_ev.textContent||'').toLowerCase(); if(/pk|tournament/.test(_et)){SFLpkViewer=true;goTo('pkbattle');return;} if(/predict|league/.test(_et)){goTo('predictions');return;} if(/recruit/.test(_et)){goTo('mgrrecruit');return;} goTo('live');return;} return; }
    if(_cf==='J2-16'){
      var _j16bk=t.closest('.hnav .back'); if(_j16bk){ if(/‹|←/.test(_j16bk.textContent||'')){goBack();} return; }
      if(t.closest('.sbtn')){goTo('clubchat');return;}
      var _q16=t.closest('.qa'); if(_q16){var _qq=(_q16.textContent||'').toLowerCase(); if(/task/.test(_qq)){goTo('tasks');return;} if(/live/.test(_qq)){goTo('live');return;} if(/reward/.test(_qq)){goTo('rewards');return;} if(/league/.test(_qq)){goTo('league');return;} return;}
      var _lv16=t.closest('.lvcard'); if(_lv16){var _lvb2=_lv16.querySelector('.lvb'); if(_lvb2&&/pk/i.test(_lvb2.textContent)){SFLpkViewer=true;goTo('pkbattle');return;} goTo('liveroom');return;}
      if(t.closest('.btn.club')){goTo('squadroom');return;}
      return;
    }
    if(_cf==='J2-21'){ if(t.closest('.btn')){goTo(SFLfvActive?'fvalready':'fvconfirm');return;} if(t.closest('.link')){goTo('fvexplain');return;} return; }
    if(_cf.indexOf('J2-')===0){
      var _j2bk=t.closest('.top .back, .hnav .back'); if(_j2bk){ if(/‹|←/.test(_j2bk.textContent||'')){goBack();} return; }
      if(_cf==='J2-01'){ var _b1=t.closest('.btn'); if(_b1){ if(/recruit/i.test(_b1.textContent)){goTo('clubdetail');return;} goTo('clubs');return;} return; }
      if(_cf==='J2-02'){ var _ct=t.closest('.ctab'); if(_ct){var _cx=_ct.textContent.toLowerCase(); if(/my club/.test(_cx)){goTo('club');return;} if(/league/.test(_cx)){goTo('league');return;} jumpTab('clubs'); return;} var _ico=t.closest('.ico'); if(_ico){ if(/🔍/.test(_ico.textContent)){goTo('clubsearch');return;} if(/🔔/.test(_ico.textContent)){goTo('notifications');return;} return;} if(t.closest('.vcard')||t.closest('.apply')){goTo('clubdetail');return;} return; }
      if(_cf==='J2-03'){ if(t.closest('.searchbar')){return;} var _f3=t.closest('.fchip'); if(_f3){singleSel(_f3,_f3.parentElement);return;} if(t.closest('.vcard')||t.closest('.recent')){goTo('clubdetail');return;} return; }
      if(_cf==='J2-04'){ goTo('clubdetail'); return; }
      if(_cf==='J2-05'){ if(t.closest('.roomtile')){goTo('liveroom');return;} var _b5=t.closest('.btn'); if(_b5){ if(/preview/i.test(_b5.textContent)){goTo(SFLguest?'gate':'club');return;} goTo(SFLguest?'gate':(SFLmember?'clubblocked':'clubapply'));return;} return; }
      if(_cf==='J2-06'){ if(t.closest('.btn')){goTo('clubsubmitted');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='J2-07'){ var _b7=t.closest('.btn'); if(_b7){ var _t7=_b7.textContent.toLowerCase(); if(/application/.test(_t7)){cleanTo('clubapplications',/^J2-0[456]$/);return;} if(/live/.test(_t7)){cleanTo('live',/^J2-0/);return;} cleanTo('clubs',/^J2-0/);return;} return; }
      if(_cf==='J2-08'){ if(t.closest('.wd-discover')){cleanTo('clubs',/^J2-0/);return;} var _b8=t.closest('.btn'); if(_b8&&/withdraw/i.test(_b8.textContent)){showWithdrawSheet();return;} return; }
      if(_cf==='J2-10'){ SFLmember=true; var _b10=t.closest('.btn'); if(_b10){ if(/task/i.test(_b10.textContent)){goTo('tasks');return;} goTo('club');return;} return; }
      if(_cf==='J2-11'){ if(t.closest('.btn')){goTo('clubs');return;} return; }
      if(_cf==='J2-12'){ if(t.closest('.btn')){goTo('clubinvite');return;} return; }
      if(_cf==='J2-13'){ var _b13=t.closest('.btn'); if(_b13){ if(/decline/i.test(_b13.textContent)){goTo('clubdecline');return;} goTo(SFLmember?'clubblocked':'clubinviteaccepted');return;} return; }
      if(_cf==='J2-14'){ var _r14=t.closest('.radio'); if(_r14){singleSel(_r14,_r14.parentElement);return;} var _b14=t.closest('.btn'); if(_b14){ if(/keep/i.test(_b14.textContent)){goBack();return;} goTo('clubs');return;} return; }
      if(_cf==='J2-15'){ SFLmember=true; if(t.closest('.btn')){goTo('club');return;} return; }
      if(_cf==='J2-18'){ var _b18=t.closest('.btn,.link'); if(_b18){ if(/continue leaving/i.test(_b18.textContent)){goTo('clubleaveconfirm');return;} goBack();return;} return; }
      if(_cf==='J2-19'){ var _b19=t.closest('.btn'); if(_b19){ if(/leave club/i.test(_b19.textContent)){SFLmember=false;goTo('clubleft');return;} goBack();return;} return; }
      if(_cf==='J2-20'){ var _b20=t.closest('.btn'); if(_b20){ if(/live/i.test(_b20.textContent)){goTo('live');return;} goTo('clubs');return;} return; }
      if(_cf==='J2-17'){ var _b17=t.closest('.btn,.link'); if(_b17){ if(/support/i.test(_b17.textContent)){goTo('support');return;} if(/transfer/i.test(_b17.textContent)){goTo('move');return;} goTo('clubs');return;} return; }
      if(_cf==='J2-22'){ var _b22=t.closest('.btn,.altlink'); if(_b22){ if(/create/i.test(_b22.textContent)){goTo('register');return;} if(/sign in/i.test(_b22.textContent)){goTo('signin');return;} goBack();return;} return; }
      if(_cf==='J2-13b'){ var _b13b=t.closest('.btn'); if(_b13b){ if(/transfer/i.test(_b13b.textContent)){goTo('move');return;} goTo('club');return;} return; }
      if(_cf==='J2-05b'){ var _b5b=t.closest('.btn'); if(_b5b){ if(/discover|similar/i.test(_b5b.textContent)){goTo('clubs');return;} sflToast('We\\'ll notify you when a place opens');return;} return; }
      if(_cf==='J2-04b'){ var _b4b=t.closest('.btn'); if(_b4b){ if(/search/i.test(_b4b.textContent)){goTo('clubsearch');return;} goTo('clubs');return;} return; }
    }
    if(_cf.indexOf('FV-')===0){
      var _fvbk=t.closest('.top .back'); if(_fvbk){goBack();return;}
      if(_cf==='FV-00'){ if(t.closest('.btn')){goTo(SFLfvActive?'fvalready':'fvconfirm');return;} if(t.closest('.altlink')){goTo('fvexplain');return;} return; }
      if(_cf==='FV-01'){ if(t.closest('.btn')||t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='FV-02'){ if(t.closest('.btn')){SFLfvActive=true;goTo('fvprocessing');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='FV-03'){ goTo('fvsuccess'); return; }
      if(_cf==='FV-04'){ if(t.closest('.btn')){ while(hist.length){var _h4=hist[hist.length-1];var _f4=((VIEWS[_h4.j]&&VIEWS[_h4.j].screens[_h4.s])||{}).fnum||'';if(/^FV-0[0-4]$/.test(_f4)||_f4==='J2-21'){hist.pop();}else break;} var _cl=ANCH['club']; hist.push({j:FLOWN+_cl[0],s:idxOfFnum(_cl[0],_cl[1]),html:''}); var _dd4=ANCH['fvdashboard']; curJ=FLOWN+_dd4[0]; curS=idxOfFnum(_dd4[0],_dd4[1]); render(); return;} if(t.closest('.altlink')){cleanTo('club', /^FV-0[0-4]$|^J2-21$/);return;} return; }
      if(_cf==='FV-07'){ if(t.closest('.btn')){goTo('fvdashboard');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='FV-08'){ var _f8=t.closest('.btn,.altlink'); if(_f8){ if(/buy coins/i.test(_f8.textContent)){goTo('coinstore');return;} goTo('club');return;} return; }
      if(_cf==='FV-09'){ if(t.closest('.btn')){goTo('clubs');return;} return; }
      if(_cf==='FV-10'){ var _f10a=t.closest('.btn,.altlink'); if(_f10a){ if(/history/i.test(_f10a.textContent)){goTo('fvhistory');return;} goTo('fvdashboard');return;} return; }
      if(_cf==='FV-11'){ if(t.closest('.btn')){goTo('fvdashboard');return;} return; }
      return;
    }
    if(_cf.indexOf('RW-')===0){
      var _rbk=t.closest('.top .back'); if(_rbk){var _rt=(_rbk.textContent||'').trim(); if(/📜/.test(_rt)){goTo('rewardhistory');return;} if(_rt==='?'){goTo('support');return;} goBack(); return;}
      var _rtab=t.closest('.tabs .tab'); if(_rtab){var _rx=_rtab.textContent.toLowerCase(); if(/progress/.test(_rx)){goTo('rewardinprog');return;} if(/history/.test(_rx)){goTo('rewardhistory');return;} singleSel(_rtab,_rtab.parentElement); return;}
      if(_cf==='RW-01'){ if(t.closest('.chip')){goTo('wallet');return;} if(t.closest('.mgo')||t.closest('.mbanner')){goTo('league');return;} var _rw=t.closest('.rw'); if(_rw){var _rb=t.closest('.btn'); if(_rb&&/claim/i.test(_rb.textContent)){goTo('rewardclaim');return;} goTo('rewarddetail');return;} return; }
      if(_cf==='RW-01A'){ if(t.closest('.btn')){goTo('rewardclaim');return;} return; }
      if(_cf==='RW-01B'){ if(t.closest('.btn')){goTo('rewardsuccess');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='RW-01C'){ cleanTo(t.closest('.btn')?'wallet':'rewards', /^RW-01/); return; }
      if(_cf==='RW-01D'){ if(t.closest('.btn')){goTo('tasks');return;} return; }
      if(_cf==='RW-01F'){ var _hfc=t.closest('.fchip'); if(_hfc){singleSel(_hfc,_hfc.parentElement);return;} return; }
      if(_cf==='RW-01E'){ if(t.closest('.btn')){goTo('support');return;} return; }
    }
    if(_cf==='MC-02'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.cp')||t.closest('.linkbox')){sflToast('Invite link copied');return;} if(t.closest('.byidbtn')){goTo('mgraddid');return;} if(t.closest('.row2')){goTo('mgrshare');return;} if(t.closest('.btn')){goTo('mgrhistory');return;} return; }
    if(_cf==='MC-02H'){ if(t.closest('.htop .back')){goBack();return;} var _hf=t.closest('.hfilt'); if(_hf){singleSel(_hf,_hf.parentElement);return;} return; }
    if(_cf==='MC-02A'){ if(t.closest('.htop .back')){goBack();return;} var _msb=t.closest('.btn'); if(_msb){ if(/sfl chat/i.test(_msb.textContent)){goTo('clubchat');return;} sflToast('Invite link copied');return;} if(t.closest('.altlink')){sflToast('Opening share…');return;} return; }
    if(_cf==='MC-05'){ if(t.closest('.htop .back')){goBack();return;} var _sc=t.closest('.scout'); if(_sc){var _sb=t.closest('.btn'); if(_sb){var _acc=/accept/i.test(_sb.textContent); var _snm=((_sc.querySelector('.sn')||{}).textContent||'Fan').trim(); _sc.remove(); sflToast(_acc?(_snm+' accepted into the club'):(_snm+' rejected')); if(!mEl.querySelectorAll('.scout').length){var _scr=mEl.querySelector('.scroll'); if(_scr)_scr.innerHTML='<div class="note info" style="margin-top:20px">No pending applications right now.</div>';} return;} } return; }
    if(_cf==='MC-06'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.btn')){goTo('mgrinvitesent');return;} return; }
    if(_cf==='MC-06R'){ if(t.closest('.htop .back')){cleanTo('managerhq', /^MC-0[26]/);return;} var _r6=t.closest('.btn,.altlink'); if(_r6){ if(/another/i.test(_r6.textContent)){goTo('mgraddid');return;} goTo('mgrapplications');return;} return; }
    if(_cf==='MC-07'){ if(t.closest('.htop .back')){goBack();return;}
      var _mtab=t.closest('.tabs .tab'); if(_mtab){singleSel(_mtab,_mtab.parentElement);return;}
      var _tf=t.closest('.transfer'); if(_tf){ var _ab=t.closest('.btn'); if(_ab){ if(_ab.classList.contains('dis')){return;} var _appr=/approve/i.test(_ab.textContent); var _tnm=((_tf.querySelector('.fnm')||{}).textContent||'Request').trim(); _tf.remove(); sflToast(_appr?(_tnm+' — transfer approved'):(_tnm+' — rejected')); return;} goTo('mgrapprovaldetail'); return; }
      return; }
    if(_cf==='MC-07D'){ if(t.closest('.htop .back')||t.closest('.top .back')){goBack();return;} var _b7d=t.closest('.btn'); if(_b7d){ if(/reject/i.test(_b7d.textContent)){goBack();sflToast('Move rejected · fan notified');return;} if(/chat/i.test(_b7d.textContent)){goTo('chatthread');return;} goBack();sflToast('Move approved · membership updating');return;} return; }
    if(_cf==='MC-00'){ if(t.closest('.htop .back')){goBack();return;} var _cr0=t.closest('.clubrow'); if(_cr0){ if(_cr0.classList.contains('susp')){sflToast('This club is suspended · review pending');return;} [].forEach.call(mEl.querySelectorAll('.clubrow'),function(c){c.classList.remove('sel');}); _cr0.classList.add('sel'); goTo('managerhq'); return;} var _mb0=t.closest('.btn'); if(_mb0){ if(/create/i.test(_mb0.textContent)){goTo('createclub');return;} goTo('managerhq');return;} return; }
    if(_cf==='MC-01'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.fanview')){goTo('club');return;} var _mhi=t.closest('.hicon'); if(_mhi){ if(/🔔/.test(_mhi.textContent)){goTo('notifications');return;} goTo('profile');return;} if(t.closest('.cname')){goTo('mgrclubs');return;} var _msh=t.closest('.short'); if(_msh){var _mst=(_msh.textContent||'').toLowerCase(); if(/fan list/.test(_mst)){goTo('mgrfanlist');return;} if(/application/.test(_mst)){goTo('mgrapplications');return;} if(/add by id/.test(_mst)){goTo('mgraddid');return;} if(/recruit/.test(_mst)){goTo('mgrrecruit');return;} if(/reward/.test(_mst)){goTo('mgrrewards');return;} if(/approval/.test(_mst)){goTo('mgrapprovals');return;} return;} if(t.closest('.recruit')){goTo('mgrrecruit');return;} if(t.closest('.target')){goTo('mgrbreakdown');return;} var _mst2=t.closest('.stat'); if(_mst2){var _msx=(_mst2.textContent||'').toLowerCase(); if(/wallet/.test(_msx)){goTo('wallet');return;} if(/tier|commission/.test(_msx)){goTo('mgrcommission');return;} if(/league|grade/.test(_msx)){goTo('league');return;} goTo('mgrfanlist');return;} return; }
    if(_cf==='MC-01A'){ if(t.closest('.htop .back')){goBack();return;} return; }
    if(_cf==='MC-01B'){ if(t.closest('.htop .back')){goBack();return;} return; }
    if(_cf==='MC-03'){ if(t.closest('.htop .back')){goBack();return;} var _r3=t.closest('.tabs .tab'); if(_r3){singleSel(_r3,_r3.parentElement);return;} if(t.closest('.btn')){sflToast('350 Coins claimed to Club Wallet');return;} return; }
    if(_cf==='MC-04'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.search')){return;} var _f4=t.closest('.fchip'); if(_f4){singleSel(_f4,_f4.parentElement);return;} if(t.closest('.fanrow')){goTo('mgrfandetail');return;} return; }
    if(_cf==='MC-04A'){ if(t.closest('.htop .back')){goBack();return;} var _b4a=t.closest('.btn,.altlink'); if(_b4a){ if(/remove/i.test(_b4a.textContent)){goTo('mgrremovefan');return;} if(/chat/i.test(_b4a.textContent)){goTo('chatthread');return;} if(/move/i.test(_b4a.textContent)){goTo('createoffer');return;} } return; }
    if(_cf==='MC-04B'){ if(t.closest('.htop .back')){goBack();return;} var _ro=t.closest('.reasonopt'); if(_ro){singleSel(_ro,_ro.parentElement);return;} var _b4b=t.closest('.btn,.altlink'); if(_b4b){ if(/confirm/i.test(_b4b.textContent)){goBack();sflToast('Fan removed from club');return;} goBack();return;} return; }
    if(_cf.indexOf('ML-')===0){
      if(t.closest('.top .back')){goBack();return;}
      var _seg=t.closest('.seg .segopt'); if(_seg){ [].forEach.call(_seg.parentElement.children,function(c){c.classList&&c.classList.remove('on');}); _seg.classList.add('on'); SFLmoveType=_seg.classList.contains('perm')?'perm':'loan'; var _lbl=mEl.querySelector('.termslbl'); if(_lbl)_lbl.textContent=(SFLmoveType==='perm'?'Transfer terms':'Loan terms'); [].forEach.call(mEl.querySelectorAll('.loanonly'),function(r){r.style.display=(SFLmoveType==='perm')?'none':'';}); return; }
      if(_cf==='ML-00'){ var _b0=t.closest('.btn,.altlink'); if(_b0){ if(/cancel/i.test(_b0.textContent)){goBack();return;} hist.length=0; SFLmgrMode=false; jumpTab('home'); sflToast('Move request sent to your Manager');return;} return; }
      if(_cf==='ML-01'){ if(t.closest('.clubprev')){showDestSheet();return;} var _er=t.closest('.editrow'); if(_er){showTermSheet(_er);return;} var _b1=t.closest('.btn,.altlink'); if(_b1){ if(/save draft|cancel/i.test(_b1.textContent)){goBack();return;} goTo('reviewoffer');return;} return; }
      if(_cf==='ML-01A'){ var _b1a=t.closest('.btn,.altlink'); if(_b1a){ if(/edit/i.test(_b1a.textContent)){goBack();return;} sflToast('Offer sent · awaiting fan consent'); goTo('offersent');return;} return; }
      if(_cf==='ML-01S'){ var _b1s=t.closest('.btn,.altlink'); if(_b1s){ if(/pending offers/i.test(_b1s.textContent)){cleanTo('mgrapprovals',/^ML-/);return;} returnTo('MC-04','mgrfanlist');return;} return; }
      if(_cf==='ML-02'||_cf==='ML-02P'){ var _b2=t.closest('.btn'); if(_b2){ if(/decline/i.test(_b2.textContent)){cleanTo('club',/^ML-/);sflToast('Offer declined · your membership is unchanged');return;} if(/ask manager/i.test(_b2.textContent)){goTo('chatthread');return;} goTo('acceptconfirm');return;} return; }
      if(_cf==='ML-02A'){ var _b2a=t.closest('.btn,.altlink'); if(_b2a){ if(/go back/i.test(_b2a.textContent)){goBack();return;} goTo(SFLmoveType==='perm'?'transfercomplete':'loanactive');return;} return; }
      if(_cf==='ML-03'){ var _b3=t.closest('.btn'); if(_b3){ if(/support/i.test(_b3.textContent)){goTo('support');return;} cleanTo('home',/^ML-/);return;} return; }
      if(_cf==='ML-03A'){ var _b3a=t.closest('.btn,.altlink'); if(_b3a){ if(/home/i.test(_b3a.textContent)){cleanTo('home',/^ML-/);return;} cleanTo('club',/^ML-/);return;} return; }
      if(_cf==='ML-03B'){ var _b3b=t.closest('.btn,.altlink'); if(_b3b){ if(/home/i.test(_b3b.textContent)){cleanTo('home',/^ML-/);return;} cleanTo('club',/^ML-/);return;} return; }
      if(_cf==='ML-03C'){ if(t.closest('.btn')){cleanTo('club',/^ML-/);return;} return; }
      if(_cf==='ML-X1'){ var _bx1=t.closest('.btn'); if(_bx1){ if(/decline/i.test(_bx1.textContent)){cleanTo('club',/^ML-/);sflToast('Offer declined');return;} goTo(SFLmoveType==='perm'?'fanconsentperm':'fanconsentloan');return;} return; }
      if(_cf==='ML-X2'){ var _bx2=t.closest('.btn,.altlink'); if(_bx2){ if(/manager/i.test(_bx2.textContent)){goTo('chatthread');return;} cleanTo('club',/^ML-/);return;} return; }
      if(_cf==='ML-X3'){ var _bx3=t.closest('.btn,.altlink'); if(_bx3){ if(/new offer/i.test(_bx3.textContent)){goTo('createoffer');return;} goTo('mgrfanlist');return;} return; }
      return;
    }
    if(_cf.indexOf('GK-')===0){
      if(_cf==='GK-01D'){goTo('giftsent');return;}
      var gbt=t.closest('.gbtn'), glk=t.closest('.glink');
      if(gbt){
        if(_cf==='GK-01'){goTo('giftdetailq');return;}
        if(_cf==='GK-01A'){goTo('giftconfirm');return;}
        if(_cf==='GK-01B'){goTo('giftsending');return;}
        if(_cf==='GK-01C'){goTo('coinstore');return;}
        if(_cf==='GK-01E'){goTo('giftmenu');return;}
      }
      if(glk){
        if(_cf==='GK-01E'){ while(hist.length){var _gh=hist[hist.length-1];var _gf=((VIEWS[_gh.j]&&VIEWS[_gh.j].screens[_gh.s])||{}).fnum||'';if(/^GK-/.test(_gf)){hist.pop();}else break;} goBack(); return;}
        goTo('giftmenu');return;
      }
    }
    if(_cf.indexOf('GK-')===0){ if(SFLgiftInteract(mEl,t,null))return; }
    if(_cf==='CC-03'){var cso=t.closest('.seg .segopt'); if(cso){singleSel(cso,cso.parentElement); var isInv=/invite/i.test(cso.textContent); var io=mEl.querySelector('.invonly'),po=mEl.querySelector('.pubonly'); if(io)io.style.display=isInv?'':'none'; if(po)po.style.display=isInv?'none':''; return;}}
    if(_cf==='9'){var o9e=t.closest('.opt'); if(o9e){var o9=(o9e.textContent||'').toLowerCase(); if(/join a club/.test(o9)){goTo('clubs');return;} if(/start a club|create/.test(o9)){goTo('createclub');return;} if(/explore/.test(o9)){goTo('home');return;}}}
    if(!t.closest('.sfl-nav')){
      var tg=t.closest('.tog'); if(tg){tg.classList.toggle('off');return;}
      var ck=t.closest('.chk'); if(ck){ck.classList.toggle('off');return;}
      var chip=t.closest(MULTI); if(chip){chip.classList.toggle('on');return;}
      var opt=t.closest(SINGLE); if(opt&&opt.parentElement){singleSel(opt,opt.parentElement);return;}
      var seg=t.closest(SEG); if(seg){var kid=[].filter.call(seg.children,function(c){return c.contains(t);})[0]; if(kid){var kt=kid.textContent.toLowerCase(); var cf0=(VIEWS[curJ].screens[curS]||{}).fnum||''; if(cf0.indexOf('PV')===0){ if(/vote/.test(kt)){goTo('vote');return;} if(/award/.test(kt)){goTo('awards');return;} if(/predict/.test(kt)){if(cf0!=='PV-01')goTo('predictions');else singleSel(kid,seg);return;} } if(cf0==='RW-01'){ if(/progress/.test(kt)){goTo('rewardinprog');return;} if(/history/.test(kt)){goTo('rewardhistory');return;} if(/claim/.test(kt)){singleSel(kid,seg);return;} } if(kt.indexOf('weekly')>=0){goTo('tasksweekly');return;} if(kt.indexOf('daily')>=0){goTo('tasksdaily');return;} singleSel(kid,seg);} return;}
    var ctab=t.closest('.ctab'); if(ctab&&mEl.contains(ctab)){var ctx=ctab.textContent.toLowerCase(); if(/my club/.test(ctx)){goTo('club');return;} if(/league/.test(ctx)){goTo('league');return;} if(/discover/.test(ctx)){goTo('clubs');return;}}
    var lgt=t.closest('.lgtab'); if(lgt&&mEl.contains(lgt)){var lgx=lgt.textContent.toLowerCase(); if(/spend/.test(lgx)){goTo('leaguespend');return;} if(/previous|prev/.test(lgx)){goTo('leagueprev');return;} if(/performance|table|club/.test(lgx)){singleSel(lgt,lgt.parentElement);return;}}
    var hchip=t.closest('.hchip'); if(hchip&&mEl.contains(hchip)){var hc=((hchip.getAttribute('data-club')||'')+' '+hchip.textContent).toLowerCase(); if(/explore/.test(hc)){goTo('clubs');return;} singleSel(hchip,hchip.parentElement);return;}
    }
    var bk=t.closest('.back'); if(bk){var bg=(bk.textContent||'').trim(); if(/[‹←✕×╳]/.test(bg)||bg===''){ if(_cf==='CC-01T'){if(hist.length)goBack();else goTo('choosestart');return;} if(/^CC-/.test(_cf)||/^\d+[a-z]?$/.test(_cf)){prev();return;} goBack();return;}}
    var lblEl=t.closest('.btn,.dbtn,.lbtn,.act,.hjoin,.cgo,.laopt,.segopt,.mgo,.link,.altlink,.pd,a'); var lbl=lblEl?lblEl.textContent:'';
    var cf=(VIEWS[curJ].screens[curS]||{}).fnum||'';
    if((cf==='FT-01'||cf==='FT-02')&&t.closest('.act')){var rr=t.closest('.trow'),ttl=rr&&rr.querySelector('.tt'); if(ttl)SFLdone[ttl.textContent.trim()]=true;}
    if(/continue tasks/i.test(lbl)){goTo(cf==='FT-02'?'tasksweeklydone':'tasksdone');return;}
    if(/explore as guest|explore as a visitor|browse as guest/i.test(lbl)){SFLguest=true;goTo('guesthome');return;}
    if(/create.{0,4}account|sign up/i.test(lbl)){goTo('register');return;}
    if(/(sign in|log in)/i.test(lbl)){goTo(cf==='10'?'home':'signin');return;}
    if(cf==='8'){var s8=(t.closest('.btn,.dbtn,.act')||t).textContent||''; if(/copy|share/i.test(s8)){return;} if(/continue|get started|done|next|enter/i.test(s8)){goTo('choosestart');return;}}
    if(cf==='9'){if(/(join|browse|explore|discover)/i.test(lbl)){goTo('clubs');return;} goTo('home');return;}
    if(t.closest('.streakstrip')){goTo('progression');return;}
    if(t.closest('.chg')){goTo('createclub');return;}
    if(/apply to join/i.test(lbl)){goTo(SFLmember?'clubblocked':'clubapply');return;}
    if(t.closest('.vcard')||t.closest('.apply')){goTo('clubdetail');return;}
    /* onboarding "Choose how to start" */
    var opt9=t.closest('.opt'); if(opt9&&cf==='9'){var o9=(opt9.textContent||'').toLowerCase(); if(/join a club/.test(o9)){goTo('clubs');return;} if(/start a club|create/.test(o9)){goTo('createclub');return;} goTo('home');return;}
    /* join chain: review -> submitted -> confirmed -> club home */
    if(cf==='J2-06'&&/submit|apply|confirm|send/i.test(lbl)){goTo('clubsubmitted');return;}
    if(cf==='J2-07'&&/done|continue|view|ok|got it/i.test(lbl)){goTo('clubconfirmed');return;}
    if(cf==='J2-10'&&/enter|open|go to|view club|start/i.test(lbl)){goTo('club');return;}
    var _ccard=t.closest('.clubcard'); if(_ccard&&mEl.contains(_ccard)){ if(t.closest('.pd')||t.closest('.nextfix')){goTo('predictions');return;} goTo('club');return; }
    if(t.closest('.predict')){var fc=t.closest('.fixcard'),tn=fc&&fc.querySelector('.tn'); if(tn)SFLpredMatch=tn.textContent; next(); return;}
    if(t.closest('.pcard')){goTo('playerdetail');return;}
    if(t.closest('.crow')){goTo('chatthread');return;}
    if(cf==='RW-01'){ if(t.closest('.mgo')||/see winners/i.test(lbl)){goTo('league');return;} if(t.closest('.chip')){goTo('wallet');return;} var rhb=t.closest('.back'); if(rhb){var rhg=rhb.textContent||''; if(/📜|🧾/.test(rhg)){goTo('rewardhistory');return;} if(/\?|❓/.test(rhg)){goTo('support');return;}} }
    var rwrow=t.closest('.rw'); if(rwrow){var rb=t.closest('.btn,.act'); if(rb&&/claim/i.test(rb.textContent)){goTo('rewardclaim');return;} goTo('rewarddetail');return;}
    if(cf.indexOf('RW')===0&&/^\s*claim/i.test(lbl)){goTo('rewardclaim');return;}
    /* home surfaces: fan / manager / guest */
    if(cf==='G-02G'&&t.closest('.ha')){goTo('gate');return;}
    if(t.closest('.guestbanner')||t.closest('.gj')){goTo('gate');return;}
    if(t.closest('.gclub')){goTo('clubs');return;}
    if(t.closest('.gfix')||t.closest('.guestwhy')){goTo('gate');return;}
    var hf=t.closest('.hfol'); if(hf){ if(/(^|\s)add(\s|$)/.test(hf.className)){goTo('clubs');} else {goTo('liveroom');} return;}
    var cbn=t.closest('.callbtn'); if(cbn){var cbt=cbn.textContent||''; if(/📹/.test(cbt)){goTo('callvideo');return;} if(/📞/.test(cbt)){goTo('callvoice');return;} goTo('callsettings');return;}
    if(t.closest('.golive')){goTo(SFLguest?'gate':'golive');return;}
    if(t.closest('.joinbtn')||t.closest('.rcard')){goTo('liveroom');return;}
    if(t.closest('.reacts')||t.closest('.rowhead')||t.closest('.ball')||t.closest('.logo')){return;}
    var lhb=t.closest('.hbtn'); if(lhb){if(/🔔/.test(lhb.textContent)){goTo('notifications');return;} return;}
    var lhero=t.closest('.hero'); if(lhero&&lhero.querySelector('.reacts')){goTo('liveroom');return;}
    /* live/formation room controls */
    if(cf.indexOf('PK-')===0){
      var mc=t.closest('.modecard'); if(mc){var mct=(mc.textContent||'').toLowerCase(); if(/quick|random/.test(mct)){goTo('pkrandom');return;} if(/challenge|by id/.test(mct)){goTo('pkinvite');return;} if(/browse|host/.test(mct)){goTo('live');return;}}
      var pkb=(t.closest('.btn,.b,.altlink,.rbtns>*,.winbtns>*')||t); var pkt=(pkb.textContent||'').toLowerCase();
      if(/switch side/.test(pkt)){goTo('coinstore');return;}
      if(/golden boot|send/.test(pkt)&&t.closest('.btn')){goTo('pkbattle');return;}
      if(/i'?m ready|start|accept/.test(pkt)){goTo('pkcountdown');return;}
      if(/find another/.test(pkt)){goTo('pkrandom');return;}
      if(/rematch/.test(pkt)){goTo('pkrematch');return;}
      if(/exit|stadium|leave|done|home/.test(pkt)){goTo('live');return;}
    }
    if(/^GL-0/.test(cf)){ if(/choose formation|preview/i.test(lbl)){next();return;} if(/go live now|start.*live|start broadcast|start room/i.test(lbl)){goTo('liveroomhost');return;} }
    var giftel=t.closest('.rrb.gift,.rb.gift,.cbtn.gift,.giftbtn,.pkgift'); if(!giftel){var gbt=t.closest('.gbtn'); if(gbt&&/gift/i.test(gbt.textContent))giftel=gbt;} if(giftel){ if(/^MSG/.test(cf)){goTo('chatgift');} else {openGiftSheet();} return; }
    var rrb=t.closest('.rrb'); if(rrb){var rrt=rrb.textContent||''; if(/🎁/.test(rrt)){goTo('giftmenu');return;} if(/🚪|🔴|leave|end/i.test(rrt)){goTo('live');return;} return;}
    if(t.closest('.rmeta')||t.closest('.ractbar')||t.closest('.coincap')||t.closest('.rchat')||t.closest('.rsay')||t.closest('.composer')||t.closest('.cin')){return;}
    if(t.closest('.seat.open')||t.closest('.posrow')||t.closest('.opentag')){goTo('confirmseat');return;}
    if(t.closest('.seat')){goTo('chatthread');return;}
    if(cf==='CS-01'&&t.closest('.taskcard')){goTo('watchcomplete');return;}
    if(t.closest('.vact')){return;}
    if(t.closest('.upnext')){goTo('watch');return;}
    if(cf==='CS-01C'){var cst=(t.closest('.btn,.altlink,.dcta')||t).textContent||''; if(/view reward|claim/i.test(cst)){goTo('rewards');return;} if(/task|keep watching/i.test(cst)){goTo('tasks');return;}}
    if(t.closest('.hspot')){goTo('live');return;}
    var _lvc=t.closest('.livecard,.lvcard'); if(_lvc){ var _lvb=_lvc.querySelector('.lb'); if(_lvb&&/pk/i.test(_lvb.textContent)){SFLpkViewer=true;goTo('pkbattle');return;} goTo('liveroom');return; }
    if(t.closest('.qt.players')){goTo('myplayers');return;}
    if(t.closest('.sbtn')||t.closest('.onlinebar')||t.closest('.chatprev')){goTo('clubchat');return;}
    if(t.closest('.giftlead')){goTo('rewards');return;}
    if(/preview club feed/i.test(lbl)||/enter squad|squad room/i.test(lbl)){goTo(/squad/i.test(lbl)?'squadroom':'club');return;}
    var qae=t.closest('.qa'); if(qae){var q=(qae.textContent||'').toLowerCase(); if(/task/.test(q)){goTo('tasks');return;} if(/live/.test(q)){goTo('live');return;} if(/reward/.test(q)){goTo('rewards');return;} if(/league/.test(q)){goTo('league');return;}}
    var dutye=t.closest('.duty'); if(dutye){var dz=(dutye.textContent||'').toLowerCase(); if(/application/.test(dz)){goTo('mgrapplications');return;} if(/transfer|approve|loan/.test(dz)){goTo('mgrapprovals');return;} if(/live/.test(dz)){goTo('live');return;} if(/chat|announcement/.test(dz)){goTo('clubchat');return;} goTo('managerhq');return;}
    var modt=t.closest('.mod'); if(modt){var mt=(modt.textContent||'').toLowerCase(); if(/application/.test(mt)){goTo('mgrapplications');return;} if(/approval/.test(mt)){goTo('mgrapprovals');return;} if(/task/.test(mt)){goTo('tasks');return;} if(/reward/.test(mt)){goTo('rewards');return;} goTo('managerhq');return;}
    var sal=t.closest('.sa'); if(sal){var stx=(sal.textContent||'').toLowerCase(); if(/explore/.test(stx)){goTo('clubs');return;} if(/reward/.test(stx)){goTo('rewards');return;} if(/member/.test(stx)){goTo('clubchat');return;} if(/home/.test(stx)){goTo('home');return;} goTo('live');return;}

    if(t.closest('.fanview')){goTo('club');return;}
    if(cf==='MC-01'){
      if(/view breakdown/i.test(lbl)){goTo('mgrbreakdown');return;}
      if(t.closest('.recruit')){goTo('mgrrecruit');return;}
      var msh=t.closest('.short'); if(msh){var mst=(msh.textContent||'').toLowerCase(); if(/fan list/.test(mst)){goTo('mgrfanlist');return;} if(/application/.test(mst)){goTo('mgrapplications');return;} if(/add by id/.test(mst)){goTo('mgraddid');return;} if(/recruit/.test(mst)){goTo('mgrrecruit');return;} if(/reward/.test(mst)){goTo('mgrrewards');return;} if(/approval/.test(mst)){goTo('mgrapprovals');return;} goTo('managerhq');return;}
      var mstt=t.closest('.stat'); if(mstt){var msx=(mstt.textContent||'').toLowerCase(); if(/wallet/.test(msx)){goTo('wallet');return;} if(/league/.test(msx)){goTo('league');return;} if(/week|fans|\bfan\b/.test(msx)){goTo('mgrfanlist');return;} goTo('mgrbreakdown');return;}
    }
    var d=destOf(t); if(d&&goTo(d))return;
    if(t.closest('.sfl-nav')||t.closest('.navpill')||t.closest('.tabbar'))return;
    if(t.closest('.searchbar'))return;
    if(t.matches&&t.matches('.phone,.body,.dbody,.lbody,.scroll,.scrollarea,.feed,.list,.hscroll,.lscroll,.msgs,.chatwrap,.frames,.top,.dtop,.hbar,.hero,.phero,.lhero,.chdr,#mount'))return;
    if(/^CC-/.test(cf)&&!t.closest('.btn')){return;}
    next();
  });
  document.getElementById('stageToggle').onclick=function(){document.body.setAttribute('data-stage', document.body.getAttribute('data-stage')==='light'?'dark':'light');};
  var _mm=document.getElementById('menuModal');
  document.getElementById('menuBtn').onclick=function(){_mm.classList.add('open');};
  document.getElementById('menuClose').onclick=function(){_mm.classList.remove('open');};
  _mm.onclick=function(e){if(e.target===_mm)_mm.classList.remove('open');};
  jsel.addEventListener('change',function(){_mm.classList.remove('open');});
  window.addEventListener('resize',fit);
  render();
})();
</script>
"""
import json
FLOWS=[
 {"name":"1 · First-time user (Sign up)","refs":[[0,"1"],[0,"2"],[0,"3"],[0,"4"],[0,"5"],[0,"6"],[0,"7"],[0,"8"],[0,"16"],[0,"9"]]},
 {"name":"⭐ First-time fan · join a club","refs":[[0,"2"],[0,"3"],[0,"4"],[0,"7"],[0,"8"],[0,"9"],[1,"J2-02"],[1,"J2-05"],[1,"J2-06"],[1,"J2-07"],[1,"J2-10"],[1,"J2-16"]]},
 {"name":"⭐ Start a club (become manager)","refs":[[0,"8"],[0,"9"],[24,"CC-01T"],[24,"CC-01"],[24,"CC-02"],[24,"CC-03"],[24,"CC-04"],[24,"CC-05"],[24,"CC-06"],[19,"G-02M"]]},
 {"name":"2 · Returning user (Sign in)","refs":[[0,"1"],[0,"2"],[0,"10"],[19,"G-02"]]},
 {"name":"3 · Forgot password","refs":[[0,"10"],[0,"12"],[0,"13"],[0,"14"],[0,"14b"],[0,"10"]]},
 {"name":"4 · Daily tasks (do & claim)","refs":[[3,"FT-01"],[17,"CS-01"],[3,"FT-06"],[3,"FT-01"],[4,"PV-01"],[3,"FT-06"],[3,"FT-01"],[3,"FT-07"],[3,"FT-08"],[3,"FT-10"]]},
]
JLABELS=[ ('Global Shell' if num=='G' else ('Extra · '+title if num.startswith('E') else 'J'+num+' · '+title)) for (fn,num,title) in ALL]
PLAYER_JS=PLAYER_JS.replace('%SB%',SB_INJECT).replace('%META%',json.dumps([m for _,_,m in ALL])).replace('%FLOWS%',json.dumps(FLOWS)).replace('%JLABELS%',json.dumps(JLABELS)).replace('%GIFTSHEET%',json.dumps(GIFTSHEET_HTML))

page=('<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">'
 '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">'
 '<title>SFL — Flow Prototype</title>\n<style>\n'+font_css+'\n'+root_vars+'\n'+CHROME_CSS+PPNAV_CSS+'\n'+'\n'.join(styleblocks)+'\n</style></head>'
 '<body data-stage="dark">'
 '<header>'
 '<button class="ppbtn sm" id="menuBtn" title="Menu">☰</button>'
 '<div class="hdrscreen"><span class="sc" id="scap"></span></div>'
 '<button class="ppbtn sm" id="stageToggle" title="Toggle theme">◐</button>'
 '</header>'
 '<div class="sflmodal" id="menuModal"><div class="sflmodal-card">'
 '<div class="mm-top"><div class="brand"><div class="bc">SFL</div>Flow Prototype</div><button class="ppbtn sm" id="menuClose">✕</button></div>'
 '<div class="mm-lbl">Jump to a flow or journey</div>'
 '<select id="jsel"></select>'
 '<div class="mm-nav"><button class="ppnavbtn" id="bprev">‹ Prev</button><span class="ppcount" id="counter"></span><button class="ppnavbtn" id="bnext">Next ›</button></div>'
 '</div></div>'
 '<div class="ppstage" id="stage">'
 '<div class="scaler" id="scaler"><div id="mount"></div></div>'
 '<div class="dotbar" id="dotbar"></div>'
 '</div>'
 '<div class="ppnav"><button class="ppnavbtn" id="bprev2">‹ Back</button><span class="ppcount" id="counter2"></span><button class="ppnavbtn primary" id="bnext2">Next ›</button></div>'
 '<footer>Tap chips, tabs &amp; options to select · tap a primary button to continue · ← / → keys · swipe · ◐ toggles stage</footer>'
 +''.join(framedata)+'\n'+PLAYER_JS+'</body></html>')

open('sfl-prototype.html','w',encoding='utf-8').write(page)
print('wrote sfl-prototype.html', round(len(page)/1048576,2),'MB · journeys:',len(ALL))

# ---------------------------------------------------------------------------
# Multi-page SITE: hub index + one self-contained gallery page per journey
# ---------------------------------------------------------------------------
import shutil
SITE=os.path.join(SCR,'..','site')
if os.path.isdir(SITE): shutil.rmtree(SITE)
os.makedirs(os.path.join(SITE,'journeys'))
FONT_B64=base64.b64encode(open('assets/manrope.woff2','rb').read()).decode()

def slugify(t):
    return re.sub(r'[^a-z0-9]+','-', t.lower()).strip('-')

def inline_assets(html):
    used={}
    def rep(m):
        a=m.group(1)
        if a.endswith('.woff2'): return m.group(0)
        used.setdefault(a, '--g-'+re.sub(r'[^a-zA-Z0-9]','_',a))
        return 'var('+used[a]+')'
    out=re.sub(r"url\(['\"]?assets/([\w.\-]+)['\"]?\)", rep, html)
    out=out.replace("url('assets/manrope.woff2')", "url('data:font/woff2;base64,"+FONT_B64+"')")
    if used:
        vars_css=':root{'+''.join(v+':url("'+datauri(a)+'");' for a,v in used.items())+'}'
        out=out.replace('</style>', vars_css+'</style>', 1)
    return out

# code -> section for the hub ("journey" vs "reference")
REF={'E2','E3','E4'}
entries=[]  # (code,label,slug,filename,screens)
for fn,code,label in ALL:
    src=allsrc[fn]
    nscr=src.count('class="fnum"')
    slug=slugify(label)
    outname=(code+'-'+slug)+'.html'
    open(os.path.join(SITE,'journeys',outname),'w',encoding='utf-8').write(inline_assets(src))
    entries.append((code,label,slug,'journeys/'+outname,nscr,'reference' if code in REF else 'journey'))

# copy the interactive prototype into the site as prototype.html
shutil.copyfile('sfl-prototype.html', os.path.join(SITE,'prototype.html'))

def cards(kind):
    out=''
    for code,label,slug,href,nscr,k in entries:
        if k!=kind: continue
        out+=('<a class="jcard" href="'+href+'">'
              '<div class="jcode">'+code+'</div>'
              '<div class="jmeta"><div class="jname">'+label+'</div>'
              '<div class="jscr">'+str(nscr)+' screens</div></div>'
              '<div class="jarrow">→</div></a>')
    return out

hub=('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
 '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
 '<title>SFL - Prototype Hub</title>'
 "<style>@font-face{font-family:'Manrope';font-weight:200 800;src:url('data:font/woff2;base64,"+FONT_B64+"') format('woff2')}"
 '*{margin:0;padding:0;box-sizing:border-box}'
 "body{font-family:'Manrope',-apple-system,'Segoe UI',sans-serif;background:#0B0E14;color:#EAEEF5;"
 'background-image:radial-gradient(60% 40% at 12% 0%,rgba(228,54,43,.16),transparent 60%),radial-gradient(50% 35% at 92% 4%,rgba(201,255,61,.10),transparent 60%);'
 'min-height:100vh;padding:44px 22px 80px}'
 '.wrap{max-width:1100px;margin:0 auto}'
 '.kick{font-size:12px;font-weight:800;letter-spacing:4px;color:#C9FF3D;text-transform:uppercase}'
 'h1{font-size:40px;font-weight:800;letter-spacing:-1.2px;margin-top:8px}'
 '.sub{color:#8C97A8;font-size:15px;font-weight:550;margin-top:10px;max-width:640px;line-height:22px}'
 '.hero{display:flex;align-items:center;gap:18px;margin:30px 0 12px;padding:22px;border-radius:20px;'
 'background:linear-gradient(135deg,#E4362B,#8F1109);box-shadow:0 20px 50px rgba(228,54,43,.28);text-decoration:none;color:#fff}'
 '.hero .pl{width:56px;height:56px;border-radius:16px;background:rgba(255,255,255,.18);display:flex;align-items:center;justify-content:center;font-size:26px;flex:none}'
 '.hero .ht{font-size:21px;font-weight:800}.hero .hs{font-size:13px;font-weight:650;color:rgba(255,255,255,.85);margin-top:3px}'
 '.hero .go{margin-left:auto;font-size:14px;font-weight:800;background:#fff;color:#B4241B;padding:11px 18px;border-radius:999px}'
 '.lbl{font-size:12px;font-weight:800;letter-spacing:1.5px;color:#8C97A8;text-transform:uppercase;margin:30px 0 12px}'
 '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px}'
 '.jcard{display:flex;align-items:center;gap:14px;padding:15px 16px;border-radius:14px;background:#141922;'
 'border:1px solid #232A36;text-decoration:none;color:#EAEEF5;transition:border-color .15s,transform .15s}'
 '.jcard:hover{border-color:#C9FF3D;transform:translateY(-2px)}'
 '.jcode{min-width:40px;height:40px;padding:0 8px;border-radius:10px;background:#0B0E14;border:1px solid #2A3140;'
 'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#C9FF3D;flex:none}'
 '.jname{font-size:15px;font-weight:800}.jscr{font-size:11.5px;font-weight:700;color:#8C97A8;margin-top:2px}'
 '.jarrow{margin-left:auto;color:#8C97A8;font-size:18px;font-weight:800}'
 '.foot{margin-top:40px;color:#5C6675;font-size:12px;font-weight:600}'
 '</style></head><body><div class="wrap">'
 '<div class="kick">Soccer Fan Live</div><h1>Prototype Hub</h1>'
 '<div class="sub">Open the full clickable prototype, or browse any single journey as a one-page gallery of every screen.</div>'
 '<a class="hero" href="prototype.html"><div class="pl">▶</div>'
 '<div><div class="ht">Full Interactive Prototype</div><div class="hs">The complete wired app - tap through every flow end to end</div></div>'
 '<div class="go">Open →</div></a>'
 '<div class="lbl">Journeys - all screens on one page</div><div class="grid">'+cards('journey')+'</div>'
 '<div class="lbl">Design &amp; reference sets</div><div class="grid">'+cards('reference')+'</div>'
 '<div class="foot">Generated from source by build/build_proto.py - '+str(len(entries))+' journeys.</div>'
 '</div></body></html>')
open(os.path.join(SITE,'index.html'),'w',encoding='utf-8').write(hub)
print('wrote site/ :', len(entries),'journey pages + index.html + prototype.html')
