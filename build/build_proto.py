import re, base64, os
SCR='/Users/shahnawaz/Documents/sfl-niki/screens'; os.chdir(SCR)

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
allsrc={fn:open(fn).read() for fn,_,_ in ALL}  # READ ONLY

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
.ppcount{font-size:12px;font-weight:800;opacity:.6;font-variant-numeric:tabular-nums;min-width:70px;text-align:center}\n.phone .scroll,.phone .hscroll,.phone .lscroll,.phone .msgs,.phone .chatwrap,.phone .dbody,.phone .lbody,.phone .body,.phone .scrollarea,.phone .feed,.phone .list,.phone .content{overflow-y:auto!important;-webkit-overflow-scrolling:touch;scrollbar-width:none}
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
   +'.sfl-nav .nc .ic{font-size:19px;line-height:1}.sfl-nav .nc .nl{font-size:7px;font-weight:800;margin-top:1px}';
   document.head.appendChild(st); }
  function injectNav(phone,dark){ var tab=phone.getAttribute&&phone.getAttribute('data-nav'); if(!tab)return; if(phone.querySelector(':scope > .sfl-nav'))return; ensureNavCss();
   function it(id,ic,l){return '<div class="nit'+(tab===id?' on':'')+'"><span class="ic">'+ic+'</span>'+l+'</div>';}
   var nav=document.createElement('div'); nav.className='sfl-nav'+(dark?' dark':'');
   nav.innerHTML=it('home','🏠','Home')+it('market','🔁','Market')+'<div class="nc"><span class="ic">🏟️</span><span class="nl">Stadium</span></div>'+it('games','🎮','Games')+it('wallet','◆','Wallet');
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
    var gc=tgt.closest('.gcat'); if(gc&&gc.parentElement){ [].forEach.call(gc.parentElement.children,function(c){c.classList&&c.classList.remove('on');}); gc.classList.add('on'); var gx=(gc.textContent||'').toLowerCase(); var key=/match/.test(gx)?'matchday':/troph/.test(gx)?'trophies':/support/.test(gx)?'support':/legend/.test(gx)?'legends':'popular'; [].forEach.call(scope.querySelectorAll('.gtile'),function(tl){var cats=(tl.getAttribute('data-cat')||''); tl.style.display=(cats.indexOf(key)>=0)?'':'none';}); return true; }
    if(tgt.closest('.btn')){ if(onClose)onClose(); return true; }
    return false;
  }
  function openGiftSheet(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflgiftoverlay'))return;
    var ov=document.createElement('div'); ov.className='sflgiftoverlay'; ov.style.cssText='position:absolute;inset:0;z-index:700'; ov.innerHTML=GIFTSHEET;
    phone.appendChild(ov); SFLcoinify(ov); SFLcrest(ov);
    ov.addEventListener('click',function(e){ e.stopPropagation(); SFLgiftInteract(ov,e.target,function(){ov.remove();}); });
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
    if(scr.fnum==='PV-04'){SFLpred={match:SFLpredMatch,score:'2–1'};}
    if(scr.fnum==='PV-01'){applyPredDone(mount);}
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
  var hist=[]; var SFLdone={}; var SFLpred=null; var SFLpredMatch='Red Devils'; var SFLmember=false; var ANCH={"home": [19, "G-02"], "profile": [19, "G-05"], "notifications": [19, "G-03"], "kyc": [19, "G-06A"], "support": [19, "G-07A"], "market": [5, "PL-01"], "games": [16, 0], "wallet": [12, 0], "coinstore": [2, "J3-02"], "club": [1, "J2-16"], "tasks": [3, "FT-01"], "predictions": [4, "PV-01"], "rewards": [15, 0], "managerhq": [13, "MC-01"], "inbox": [18, 0], "kitbag": [9, 0], "progression": [11, 0], "live": [20, 0],"convert":[12,"WA-02"],"gtransfer":[12,"WA-03"],"withdraw":[12,"WA-04A"],"wallethist":[12,"WA-05"],"move":[14,0],"tasksdaily":[3,"FT-01"],"tasksweekly":[3,"FT-02"],"tasksdone":[3,"FT-07"],"tasksweeklydone":[3,"FT-07W"],"watch":[17,0],"golive":[6,"GL-01"],"pk":[8,"PK-01"],"register":[0,"3"],"signin":[0,"10"],"clubs":[1,"J2-02"],"league":[11,"PR-02"],"clubdetail":[1,"J2-05"],"clubapply":[1,"J2-06"],"vote":[4,"PV-05"],"awards":[4,"PV-08"],"playerdetail":[5,"PL-02"],"chatthread":[18,"MSG-04"],"rewarddetail":[15,"RW-01A"],"rewardclaim":[15,"RW-01B"],"rewardinprog":[15,"RW-01D"],"rewardhistory":[15,"RW-01F"],"clubblocked":[1,"J2-13b"],"clubsubmitted":[1,"J2-07"],"clubconfirmed":[1,"J2-10"],"createclub":[24,"CC-01T"],"mgrapplications":[13,"MC-05"],"mgrapprovals":[13,"MC-07"],"clubchat":[18,"MSG-05"],"watchcomplete":[17,"CS-01C"],"choosestart":[0,"9"],"mgrfanlist":[13,"MC-04"],"mgrrecruit":[13,"MC-02"],"mgraddid":[13,"MC-06"],"mgrrewards":[13,"MC-03"],"mgrbreakdown":[13,"MC-01B"],"liveroom":[6,"GL-03V"],"squadroom":[6,"GL-05"],"giftmenu":[9,"GK-01"],"confirmseat":[6,"GL-05A"],"chatgift":[18,"MSG-06"],"pkrandom":[8,"PK-01A"],"pkinvite":[8,"PK-01B"],"pkcountdown":[8,"PK-02A"],"pkbattle":[8,"PK-03"],"pkrematch":[8,"PK-04D"],"liveroomhost":[6,"GL-03H"],"callvoice":[18,"CALL-01"],"callvideo":[18,"CALL-04"],"callsettings":[18,"MSG-08"],"leaguespend":[11,"PR-02C"],"leagueprev":[11,"PR-02D"]};
  function idxOfFnum(j,fn){var a=(JOUR[j]&&JOUR[j].screens)||[];for(var i=0;i<a.length;i++)if(a[i].fnum===fn)return i;return 0;}
  function goTo(a){var d=ANCH[a]; if(!d)return false; hist.push({j:curJ,s:curS,html:mount.innerHTML}); curJ=FLOWN+d[0]; curS=(typeof d[1]==='number')?d[1]:idxOfFnum(d[0],d[1]); render(); return true;}
  function goBack(){ if(hist.length){var h=hist.pop(); curJ=h.j; curS=h.s; render(); if(h.html){mount.innerHTML=h.html;} var sc=VIEWS[curJ].screens[curS]||{}; SFLcoinify(mount); SFLcrest(mount); SFLchat(mount); if(sc.fnum==='FT-01'||sc.fnum==='FT-02'){applyTaskDone(mount);} if(sc.fnum==='PV-01'){applyPredDone(mount);} } else prev(); }
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
  function destOf(t){
    if(t.closest('.coinpill'))return 'coinstore';
    if(t.closest('.hqbtn'))return 'managerhq';
    var nav=t.closest('.sfl-nav .nit,.sfl-nav .nc,.navpill .nav,.navpill .navc'); if(nav){var n=nav.textContent.toLowerCase(); if(n.indexOf('home')>=0)return 'home'; if(n.indexOf('market')>=0)return 'market'; if(n.indexOf('stadium')>=0||n.indexOf('live')>=0)return 'live'; if(n.indexOf('games')>=0)return 'games'; if(n.indexOf('wallet')>=0)return 'wallet'; return null;}
    var hic=t.closest('.hicon'); if(hic){var e=hic.textContent; if(e.indexOf('🔔')>=0)return 'notifications'; if(e.indexOf('💬')>=0)return 'inbox';}
    if(t.closest('.ha')||t.closest('.selavatar'))return 'profile';
    var lab=t.closest('.btn,.dbtn,.lbtn,.short,.mod,.tile,.tplay,.listrow,.rolerow,.pjoin,.ab,.mgo,.cgo,.gj,.rw,.cat,.reccard,.mbanner,.clubcard,.hqbtn,.nrow,.txrow,.hrow,.crow,.callrow,.qt,.mom,.hjoin,.nextfix,.hfol,.livecard,.act,.explorelink,a'); var x=(lab?lab.textContent:'').toLowerCase();
    var K=[['go live','golive'],['join a pk','pk'],['pk battle','pk'],['start a pk','pk'],['matchday','live'],['watchalong','live'],['join live','live'],['north stand','live'],['watch sfl','watch'],['watch','watch'],['make a prediction','predictions'],['predict','predictions'],['transfer gold','gtransfer'],['send gold','gtransfer'],['gold transfer','gtransfer'],['convert','convert'],['withdraw','withdraw'],['buy coins','coinstore'],['coin store','coinstore'],['top up','coinstore'],['manager hq','managerhq'],['manager dashboard','managerhq'],['open hq','managerhq'],['enter hq','managerhq'],['kit bag','kitbag'],['reward ready','rewards'],['ready to claim','rewards'],['see winners','rewards'],['monthly winners','rewards'],['claim','rewards'],['rewards','rewards'],['you won','rewards'],['invited you','club'],['invitation','club'],['application','club'],['open club','club'],['club home','club'],['view club','club'],['other clubs','clubs'],['explore other','clubs'],['browse clubs','clubs'],['discover clubs','clubs'],['explore clubs','clubs'],['find a club','clubs'],['join a fan club','clubs'],['join a club','clubs'],['join club','clubs'],['gold received','wallethist'],['sent you','wallethist'],['refund','wallethist'],['transaction','wallethist'],['loan offer','move'],['transfer offer','move'],['loan/transfer','move'],['awaiting fan consent','move'],['join live','live'],['watchalong','live'],['matchday','live'],['north stand','live'],['pk battle','live'],['go live','live'],['watch party','live'],['stadium','live'],['live room','live'],['notification','notifications'],['messages','inbox'],['message','inbox'],['chat','inbox'],['prediction','predictions'],['tasks','tasks'],['duties','tasks'],['progression','progression'],['fan level','progression'],['verify identity','kyc'],['kyc','kyc'],['withdrawals unlocked','kyc'],['contact support','support'],['get support','support'],['report a problem','support'],['raise dispute','support'],['my players','market'],['player market','market'],['escrow','market'],['market','market'],['edit profile','profile'],['my stats','profile'],['wallet','wallet'],['games','games']];
    for(var i=0;i<K.length;i++){if(x.indexOf(K[i][0])>=0)return K[i][1];}
    return null;
  }
  stage.addEventListener('click',function(e){
    var mEl=document.getElementById('scaler').firstElementChild; if(!mEl||!mEl.contains(e.target))return;
    var t=e.target;
    if(t.closest('.sfl-statusbar'))return;
    var _cf=(VIEWS[curJ].screens[curS]||{}).fnum||'';
    if(_cf==='CC-01T'){var lgc=t.closest('.lgchip'); if(lgc){var grp=lgc.parentElement; [].forEach.call(grp.children,function(c){c.classList&&c.classList.remove('on');}); lgc.classList.add('on'); var key=lgc.getAttribute('data-league')||''; [].forEach.call(mEl.querySelectorAll('.lgroup'),function(g){g.style.display=(!key||g.getAttribute('data-league')===key)?'':'none';}); return;}}
    var ffc=t.closest('.filters .fchip'); if(ffc){var fgrp=ffc.parentElement;[].forEach.call(fgrp.children,function(c){c.classList&&c.classList.remove('on');});ffc.classList.add('on');var fl=(ffc.textContent||'').toLowerCase();var fk=/follow/.test(fl)?'following':/premier/.test(fl)?'prem':/champion/.test(fl)?'champions':'';var rc=mEl.querySelectorAll('.carousel .rcard, .rcard');[].forEach.call(rc,function(r){var cats=(r.getAttribute('data-cat')||'');r.style.display=(!fk||cats.indexOf(fk)>=0)?'':'none';});return;}
    if(_cf==='RW-01'){var bchip=t.closest('.chip'); if(bchip&&bchip.querySelector('.cv')){goTo('wallet');return;}}
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
    if(/create account|sign up/i.test(lbl)){goTo('register');return;}
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
    if(t.closest('.predict')){var fc=t.closest('.fixcard'),tn=fc&&fc.querySelector('.tn'); if(tn)SFLpredMatch=tn.textContent; next(); return;}
    if(t.closest('.pcard')){goTo('playerdetail');return;}
    if(t.closest('.crow')){goTo('chatthread');return;}
    if(cf==='RW-01'){ if(t.closest('.mgo')||/see winners/i.test(lbl)){goTo('league');return;} if(t.closest('.chip')){goTo('wallet');return;} var rhb=t.closest('.back'); if(rhb){var rhg=rhb.textContent||''; if(/📜|🧾/.test(rhg)){goTo('rewardhistory');return;} if(/\?|❓/.test(rhg)){goTo('support');return;}} }
    var rwrow=t.closest('.rw'); if(rwrow){var rb=t.closest('.btn,.act'); if(rb&&/claim/i.test(rb.textContent)){goTo('rewardclaim');return;} goTo('rewarddetail');return;}
    if(cf.indexOf('RW')===0&&/^\s*claim/i.test(lbl)){goTo('rewardclaim');return;}
    /* home surfaces: fan / manager / guest */
    if(cf==='G-02G'&&t.closest('.ha')){goTo('register');return;}
    if(t.closest('.guestbanner')||t.closest('.gj')){goTo('register');return;}
    if(t.closest('.gclub')){goTo('clubs');return;}
    if(t.closest('.gfix')||t.closest('.guestwhy')){goTo('register');return;}
    var hf=t.closest('.hfol'); if(hf){ if(/(^|\s)add(\s|$)/.test(hf.className)){goTo('clubs');} else if(hf.classList.contains('off')){goTo('chatthread');} else {goTo('liveroom');} return;}
    var cbn=t.closest('.callbtn'); if(cbn){var cbt=cbn.textContent||''; if(/📹/.test(cbt)){goTo('callvideo');return;} if(/📞/.test(cbt)){goTo('callvoice');return;} goTo('callsettings');return;}
    if(t.closest('.golive')){goTo('golive');return;}
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
    if(t.closest('.livecard')||t.closest('.lvcard')){goTo('live');return;}
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

open('sfl-prototype.html','w').write(page)
print('wrote sfl-prototype.html', round(len(page)/1048576,2),'MB · journeys:',len(ALL))
