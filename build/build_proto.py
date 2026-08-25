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
 ('create-club.dev.html','E5','Create a Club'),('coin-seller.dev.html','E6','Coin Seller')]
ALL=CORE+EXTRAS
allsrc={fn:open(fn,encoding='utf-8').read() for fn,_,_ in ALL}  # READ ONLY

# dedup images -> :root vars
img_map={}
def vn(fn): return '--img-'+re.sub(r'[^a-zA-Z0-9]','_',fn)
for s in allsrc.values():
    for m in re.finditer(r"url\(['\"]?assets/([\w.\-]+)['\"]?\)", s):
        a=m.group(1)
        if not a.endswith('.woff2'): img_map.setdefault(a,vn(a))
    for m in re.finditer(r'src=(["\'])assets/([\w.\-]+)\1', s):
        a=m.group(2)
        if not a.endswith('.woff2'): img_map.setdefault(a,vn(a))
def datauri(path):
    mime='image/jpeg' if path.lower().endswith(('.jpg','.jpeg')) else ('image/png' if path.lower().endswith('.png') else 'application/octet-stream')
    return f'data:{mime};base64,'+base64.b64encode(open('assets/'+path,'rb').read()).decode()
def inline_img_src(t):
    def rep(m):
        q,a=m.group(1),m.group(2)
        return m.group(0) if a.endswith('.woff2') else f'src={q}{datauri(a)}{q}'
    return re.sub(r'src=(["\'])assets/([\w.\-]+)\1', rep, t)
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

def _svic(paths):
    return ('<svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" '
            'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            'style="vertical-align:-.15em;flex:none">'+paths+'</svg>')
_GEAR='<circle cx="12" cy="12" r="3"/><path d="M12 3v2.4M12 18.6V21M5.6 5.6l1.7 1.7M16.7 16.7l1.7 1.7M3 12h2.4M18.6 12H21M5.6 18.4l1.7-1.7M16.7 7.3l1.7-1.7"/>'
_SEARCH=_svic('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>')
_VIDEO=_svic('<rect x="3" y="6.5" width="12" height="11" rx="2"/><path d="M15 10.5 21 7v10l-6-3.5"/>')
ICONMAP={
 '\U0001F50D':_SEARCH, '\U0001F50E':_SEARCH,
 '\U0001F514':_svic('<path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>'),
 '\U0001F512':_svic('<rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 8 0v3.5"/>'),
 '⚙️':_svic(_GEAR), '⚙':_svic(_GEAR),
 '\U0001F4AC':_svic('<path d="M20.5 11.5a8 8 0 0 1-11.6 7.1L4 20l1.4-4.7A8 8 0 1 1 20.5 11.5Z"/>'),
 '\U0001F3A5':_VIDEO, '\U0001F3AC':_VIDEO,
 '\U0001F4F7':_svic('<path d="M4 8.5h3l1.4-2h7.2L17 8.5h3a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1v-8a1 1 0 0 1 1-1Z"/><circle cx="12" cy="13" r="3.2"/>'),
 '\U0001F9FE':_svic('<path d="M6 2.5h12v19l-2-1.3-2 1.3-2-1.3-2 1.3-2-1.3-2 1.3Z"/><path d="M9 7h6M9 11h6M9 15h4"/>'),
}
def iconify(h):
    # Replace functional emoji glyphs with SVG icons, but keep the original glyph
    # as a hidden marker so click handlers that match textContent still work.
    for k,v in ICONMAP.items():
        if k in h: h=h.replace(k, v+'<i class="ic-emo" style="display:none">'+k+'</i>')
    return h
styleblocks=[]; framedata=[]; options=[]
for idx,(fn,num,title) in enumerate(ALL):
    s=allsrc[fn]
    css=re.search(r'<style>(.*?)</style>',s,re.S).group(1)
    css=re.sub(r'@font-face\{[^}]*\}','',css); css=imgvar(css); css=scope_css(css,'#j'+str(idx))
    css+='#j%d{background:transparent!important;padding:0!important;min-height:0!important}'%idx
    styleblocks.append(css)
    fi=s.find('<div class="frames">'); end=s.find('<style id="sfl-chrome"'); end=end if end>0 else s.rfind('</body>')
    frames=inline_img_src(imgvar(iconify(s[fi:end].rstrip())))
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
body[data-stage="light"]{background:#E7ECF6;color:#14161C;--bg:#F4F6FB;--card:#FFFFFF;--raised:#F7F8FC;--raised2:#ECEEF5;--t1:#14161C;--t2:#707786;--t3:#A6ADBC;--line:#ECEEF5;--line2:#E2E6F0;--shadow:0 12px 34px rgba(24,40,80,0);--shadow-sm:0 5px 16px rgba(24,40,80,0)}
body[data-stage="dark"]{--bg:#080A10;--card:#141922;--raised:#171D27;--raised2:#1D242F;--t1:#F2F5FA;--t2:#98A2B3;--t3:#5A6472;--line:rgba(255,255,255,.09);--line2:rgba(255,255,255,.15);--shadow:0 12px 34px rgba(0,0,0,.35);--shadow-sm:0 5px 16px rgba(0,0,0,.25)}
header{flex:none;display:flex;align-items:center;gap:14px;padding:11px 16px;background:rgba(10,12,18,.7);backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,.08);z-index:10}
body[data-stage="light"] header{background:rgba(255,255,255,.8);border-bottom-color:#DCE2EC}
.brand{display:flex;align-items:center;gap:9px;font-weight:800;font-size:14px;letter-spacing:-.3px}
.bc{width:30px;height:30px;border-radius:9px;background:linear-gradient(150deg,#E4362B,#8E1912);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:#fff}
select#flowsel{font-family:inherit;font-weight:800;font-size:14px;padding:12px 14px;border-radius:10px;border:1px solid rgba(255,255,255,.14);background:#171b24;color:#EAEEF5;cursor:pointer;width:100%;height:auto;min-height:44px;flex:none}
body[data-stage="light"] select#flowsel{background:#fff;color:#14161C;border-color:#DCE2EC}
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
#mount,[id^="j"]:not(.sflgiftwrap){width:390px;height:844px}
.ppzone{position:absolute;top:0;bottom:0;border:none;background:transparent;cursor:pointer;z-index:5}
.ppzone.l{left:0;width:32%}
.ppzone.r{right:0;width:68%}
.ppzone:focus{outline:none}
.hintl,.hintr{position:absolute;top:50%;transform:translateY(-50%);font-size:26px;opacity:0;transition:opacity .15s;pointer-events:none;z-index:6;color:#C9FF3D}
.ppzone.l:hover ~ .hintl{opacity:.5}.ppzone.r:hover ~ .hintr{opacity:.5}
.hintl{left:16px}.hintr{right:16px}
body[data-stage="light"] .sfl-nav.dark{background:rgba(255,255,255,.94)!important;border-color:rgba(255,255,255,.75)!important;box-shadow:0 14px 38px rgba(20,30,60,.22)!important}
body[data-stage="light"] .sfl-nav.dark .nit{color:#9AA2B1!important}
body[data-stage="light"] .sfl-nav.dark .nc{border-color:#F4F6FB!important}
/* ---- in-app light / dark: tokens only, no layout change ---- */
body[data-stage="light"] #mount,
body[data-stage="light"] [id^="j"]{
  --arena:#F4F6FB!important;--panel:#FFFFFF!important;--panel2:#F7F8FC!important;--panel3:#ECEEF5!important;
  --bg:#F4F6FB!important;--card:#FFFFFF!important;--deep:#FFFFFF!important;--raised:#FFFFFF!important;--raised2:#F0F2F7!important;
  --t1:#14161C!important;--t2:#707786!important;--t3:#A6ADBC!important;
  --line:#ECEEF5!important;--line2:#D7DDEA!important;--dline:#ECEEF5!important;--dline2:#D7DDEA!important;
  --dt1:#14161C!important;--dt2:#707786!important;--dt3:#A6ADBC!important;
  --shadow:0 12px 34px rgba(24,40,80,0)!important;--shadow-sm:0 5px 16px rgba(24,40,80,0)!important;
}
body[data-stage="dark"] #mount,
body[data-stage="dark"] [id^="j"]{
  --arena:#080A10!important;--panel:#141922!important;--panel2:#1C2330!important;--panel3:#252E3D!important;
  --bg:#080A10!important;--card:#141922!important;--deep:#10141C!important;--raised:#171D27!important;--raised2:#1D242F!important;
  --t1:#F2F5FA!important;--t2:#98A2B3!important;--t3:#5A6472!important;
  --line:rgba(255,255,255,.09)!important;--line2:rgba(255,255,255,.15)!important;--dline:rgba(255,255,255,.09)!important;--dline2:rgba(255,255,255,.15)!important;
  --dt1:#F2F5FA!important;--dt2:#98A2B3!important;--dt3:#5A6472!important;
  --shadow:0 12px 34px rgba(0,0,0,.35)!important;--shadow-sm:0 5px 16px rgba(0,0,0,.25)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room){
  background:#F4F6FB!important;border-color:#D7DDEA!important;color:#14161C;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room){
  background:#080A10!important;border-color:#262C38!important;color:#F2F5FA;
}
/* Ceremony screens — theme-aware (J2-07, J2-10, J2-15, J2-LV) */
body[data-stage="light"] #mount>.phone.ceremony,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony{
  background:radial-gradient(120% 80% at 50% 0%,color-mix(in srgb,var(--ck) 14%,#fff) 0%,color-mix(in srgb,var(--ck) 5%,#F4F6FB) 42%,#F4F6FB 100%)!important;
  border-color:color-mix(in srgb,var(--ck) 20%,#D7DDEA)!important;color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .ch1,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .ch1{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .csub,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .csub{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .cscarf,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cscarf{
  color:var(--ckd)!important;
  background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--ck) 12%,#fff),transparent)!important;
  border-top-color:color-mix(in srgb,var(--ck) 28%,#ECEEF5)!important;
  border-bottom-color:color-mix(in srgb,var(--ck) 28%,#ECEEF5)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .cunlock,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cunlock{
  background:color-mix(in srgb,var(--ck) 7%,#fff)!important;
  border-color:color-mix(in srgb,var(--ck) 16%,#ECEEF5)!important;
  color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .cunlock .ic,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cunlock .ic{
  background:color-mix(in srgb,var(--ck) 12%,#F0F2F7)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .cbtns .btn,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cbtns .btn{
  background:var(--ck)!important;color:#fff!important;box-shadow:0 12px 30px color-mix(in srgb,var(--ck) 32%,transparent)!important;
}
body[data-stage="light"] #mount>.phone.ceremony .cbtns .btn.lvcomplete,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cbtns .btn.lvcomplete{
  background:var(--ck)!important;color:#fff!important;
}
body[data-stage="light"] #mount>.phone.ceremony .cbtns .btn.o,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cbtns .btn.o{
  background:transparent!important;color:var(--ckd)!important;border:1.5px solid color-mix(in srgb,var(--ck) 32%,#D7DDEA)!important;box-shadow:none!important;
}
body[data-stage="light"] #mount>.phone.ceremony .rays,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .rays{
  opacity:.22!important;
}
body[data-stage="dark"] #mount>.phone.ceremony,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony{
  background:radial-gradient(120% 80% at 50% 0%,color-mix(in srgb,var(--ck) 92%,#000) 0%,color-mix(in srgb,var(--ck) 60%,#0B0D13) 45%,#0B0D13 100%)!important;
  border-color:#262C38!important;color:#fff!important;
}
body[data-stage="dark"] #mount>.phone.ceremony .ch1,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .ch1{
  color:#fff!important;
}
body[data-stage="dark"] #mount>.phone.ceremony .csub,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .csub{
  color:rgba(255,255,255,.82)!important;
}
body[data-stage="dark"] #mount>.phone.ceremony .cscarf,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cscarf{
  color:#fff!important;
}
body[data-stage="dark"] #mount>.phone.ceremony .cbtns .btn,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cbtns .btn{
  background:#fff!important;color:var(--ckd)!important;box-shadow:0 12px 30px rgba(0,0,0,.3)!important;
}
body[data-stage="dark"] #mount>.phone.ceremony .cbtns .btn.o,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.ceremony .cbtns .btn.o{
  background:rgba(255,255,255,.12)!important;color:#fff!important;border:1.5px solid rgba(255,255,255,.3)!important;box-shadow:none!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .back,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ico{
  background:#fff;border-color:#ECEEF5;color:#707786;box-shadow:0 4px 14px rgba(24,40,80,0);
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .htitle,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .h1,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cname{
  color:#14161C;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.room) .btn.ghost{
  background:#fff;color:#14161C;border-color:#ECEEF5;
}
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .back,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .ico,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .htitle,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .cname,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .fanview,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .back,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .pn,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .pid,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .htitle{
  color:#fff;
}
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .back,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .back{
  background:rgba(255,255,255,.16);border-color:rgba(255,255,255,.28);box-shadow:none;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room):not(.profile) .back,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room):not(.profile) .ico{
  background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.14);color:#F2F5FA;box-shadow:none;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room):not(.profile) .htitle,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room):not(.profile) .h1{
  color:#F2F5FA;
}
body[data-stage="light"] #j13 .stat .v,
body[data-stage="light"] #j13 .kv .v,
body[data-stage="light"] #j13 .idfield,
body[data-stage="light"] #j13 .rewcard .rt,
body[data-stage="light"] #j13 .ticket .tclub{
  color:#14161C;
}
/* ---- dark: remap hardcoded light surfaces to tokens ---- */
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .card,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mod,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mission,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .feed-item,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .coinpill,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hicon,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .searchbar,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .search,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .inp,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .input,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .amtchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .teamrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .teamsel,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .trow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cli,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .invlink,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fancard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .clubprev,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segopt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .qa,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .onlinebar,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chatprev,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .giftlead,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .vcard .info,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .xpcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .streak,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .clubm,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .active-m,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .em,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .collitem,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rolecard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .statgrid,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .listrow .li,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .showrow .shico,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .foltab.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pvopt.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .consent,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .valrow .ic,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .checkopt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .reasonopt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.info,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.amber,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.coral,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.green,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .disc,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .visbox,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .onav .omore,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mdcard .mi.done,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .clubrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .notif,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .clubcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fixcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pkg,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rewcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .target,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .seg i.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmgrask{
  background:var(--card)!important;border-color:var(--line)!important;
}
/* Dark-mode surface remap — gap classes from full-app audit (white cards -> theme card) */
body[data-stage="dark"] #mount>.phone :is(.idfield,.stat,.srow,.proof,.reccard,.kycrow,.csentry,.ruletable,.kinput,.kitem,.srccard,.lcard,.lreason,.laopt,.composer,.announce,.csrow,.coinsplit,.recbox,.waitbanner,.lgdcard,.inv.av,.inv.rs,.diffcol.old,.diffcol.new,.lbtn.ghost,.otp i),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) :is(.idfield,.stat,.srow,.proof,.reccard,.kycrow,.csentry,.ruletable,.kinput,.kitem,.srccard,.lcard,.lreason,.laopt,.composer,.announce,.csrow,.coinsplit,.recbox,.waitbanner,.lgdcard,.inv.av,.inv.rs,.diffcol.old,.diffcol.new,.lbtn.ghost,.otp i){
  background:var(--card)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .inp,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .searchbar,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .search{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sub,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lbl,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .listrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .htitle,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fineprint,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .altlink{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .h1,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cname,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .seg i.on{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gclub,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gwchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .setgrp,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cat,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ticket,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tmsg.them,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .skel,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mom,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .explorelink,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .duty,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hchips .hchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .refchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .req,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .use,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .nbtn.no,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fieldwrap,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .idrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pwfield,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .epname,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .evcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .choose .pricetag{
  background:var(--card)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .btn.ghost,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .btn.coral,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .btn.danger{
  background:var(--card)!important;color:var(--t1)!important;border-color:var(--line)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hchips .hchip.on{
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .bar-track,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mg-prog{
  background:var(--raised2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .seg,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .foltabs,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pvswitch{
  background:var(--raised)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .feed-item .fb,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sq .cm,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pkroom .cm{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .foltab,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pvopt{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .folbtn.on{
  background:var(--raised)!important;color:var(--t2)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segopt.on.loan{background:rgba(245,158,11,.12)!important;border-color:var(--amber,#F59E0B)!important}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segopt.on.perm{background:rgba(15,183,83,.12)!important;border-color:var(--green1,#0FB753)!important}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip.on:not(.pkchip){
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.profile .back,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone.profile .ico{
  background:rgba(255,255,255,.16)!important;border-color:rgba(255,255,255,.28)!important;color:#fff!important;box-shadow:none!important;
}
/* ---- light: fix dark-UI screens & ghost controls ---- */
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .field,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .toggle,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modrow,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .idfield{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .btn.ghost{
  box-shadow:var(--shadow-sm)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room):not(.profile) .back,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room):not(.profile) .ico{
  background:#fff!important;border-color:#ECEEF5!important;color:#707786!important;box-shadow:0 4px 14px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.choose .back,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.choose .ico{
  background:#fff!important;border-color:#ECEEF5!important;color:#707786!important;box-shadow:0 4px 14px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.choose .htitle,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone.choose .h1{
  color:var(--t1)!important;
}
/* ---- light: dark-native journeys (J14 Manager, J17 Games, J19 Messaging) ---- */
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .card,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stat,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .settlecard,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .setgrp,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .recruit,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .short,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .scout,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .clubrow,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .reqcard,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .uresult,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .session,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balchip,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .oddr,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .search,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chdr,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sysmsg,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .composer .cin,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .composer .cbtn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .blockedbar,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .giftopt,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .attr,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmrow{
  background:var(--card)!important;border-color:var(--line)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chdr + div div{
  color:#8A5A00!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stat.wallet,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stat.comm{
  background:linear-gradient(155deg,#FFF8E8,#FFFCF5)!important;border-color:rgba(255,194,61,.32)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .target{
  background:linear-gradient(160deg,#EAF9EF,#F4FBF6)!important;border-color:rgba(15,183,83,.28)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .target .prog{
  background:rgba(20,30,60,.08)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balchip.ticket{
  background:linear-gradient(150deg,#EAF9EF,#F4FBF6)!important;border-color:rgba(15,183,83,.28)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .reqcard .rmsg{
  background:var(--raised2)!important;color:var(--t2)!important;border-color:var(--line)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .bubble.recv{
  background:var(--raised2)!important;color:var(--t1)!important;border:1px solid var(--line)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .bubble.sent,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .bubble.sent *,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tmsg.you,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tmsg.you *{
  color:#fff!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sentwrap .bmeta{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sentwrap .bmeta .tick{
  color:var(--blue,#2F7FD1)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .oddr.total{
  background:var(--raised2)!important;color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sw{
  background:var(--raised2)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sw.on{
  background:var(--volt,#C9FF3D)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .crow .cn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .uresult .un,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .reqcard .rn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chdr .cn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .callrow .cn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .setrow,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .giftopt .gn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .short .sl,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balchip .bv,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .session .sv,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .oddr .c1,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tl .tt,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hrow .hn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet-title,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .h1,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .htitle,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fanrow .fn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .scout .sn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmrow .cmn{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .crow .cp,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .crow .ct,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sub,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .altlink,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .setrow .sv{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .btn.ghost{
  background:var(--card)!important;color:var(--t1)!important;border-color:var(--line2)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hero .btn.ghost,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hero .fanview{
  background:rgba(255,255,255,.16)!important;color:#fff!important;border-color:rgba(255,255,255,.28)!important;box-shadow:none!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip.on,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hfilt.on{
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip.on:not(.pkchip){
  box-shadow:0 2px 8px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hstat.rej{
  background:var(--raised2)!important;color:var(--t3)!important;
}
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .htitle,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .cname,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .fanview,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .back{
  color:#fff!important;
}
/* ---- light: Manager HQ command center (J14 · #j13) — themed game dashboard ---- */
body[data-stage="light"] #j13>.phone:not(.splash):not(.welcome):not(.room){
  background:#F0F2F7!important;
}
body[data-stage="light"] #j13 .hero{
  background:linear-gradient(180deg,#FFF5F4 0%,#F8F9FC 42%,#F0F2F7 100%)!important;
  border-bottom:3px solid #E4362B!important;
  box-shadow:0 8px 24px rgba(228,54,43,.08)!important;
}
body[data-stage="light"] #j13 .hero::before{
  background:radial-gradient(58% 80% at 88% 8%,rgba(228,54,43,.14),transparent 62%)!important;
}
body[data-stage="light"] #j13 .hero::after{
  background-image:linear-gradient(90deg,rgba(228,54,43,.06) 1px,transparent 1px),linear-gradient(rgba(20,30,60,.05) 1px,transparent 1px)!important;
  opacity:.28!important;
}
body[data-stage="light"] #j13 .hero .cname,
body[data-stage="light"] #j13 .hero .htitle,
body[data-stage="light"] #j13 .hero .back{
  color:#14161C!important;
}
body[data-stage="light"] #j13 .hero .hq{
  color:#6B9E12!important;
  text-shadow:none!important;
}
body[data-stage="light"] #j13 .hero .back,
body[data-stage="light"] #j13 .hero .hicon{
  background-color:rgba(255,255,255,.92)!important;
  border-color:rgba(228,54,43,.18)!important;
  color:#3D4859!important;
  box-shadow:0 4px 14px rgba(228,54,43,.10)!important;
}
body[data-stage="light"] #j13 .hero .hicon .dot{
  border-color:#fff!important;
}
body[data-stage="light"] #j13 .hero .fanview{
  background:rgba(255,255,255,.88)!important;
  color:#14161C!important;
  border-color:rgba(228,54,43,.22)!important;
  box-shadow:0 2px 10px rgba(228,54,43,.08)!important;
}
body[data-stage="light"] #j13 .stat{
  box-shadow:0 4px 16px rgba(24,40,80,0)!important;
}
/* unified, professional stat cards (consistent white, subtle semantic icon accents) */
body[data-stage="light"] #j13 .stat.wallet,
body[data-stage="light"] #j13 .stat.comm,
body[data-stage="light"] #j13 .stat.fans,
body[data-stage="light"] #j13 .stat.pos{
  background:#fff!important;border:1px solid #E7EBF2!important;border-radius:16px!important;box-shadow:0 6px 18px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #j13 .stat .v{color:#14161C!important}
body[data-stage="light"] #j13 .stat .ico{border-radius:10px!important}
body[data-stage="light"] #j13 .stat.wallet .ico{background:rgba(255,194,61,.16)!important;color:#B8860B!important}
body[data-stage="light"] #j13 .stat.comm .ico{background:rgba(255,158,27,.16)!important;color:#C47A00!important}
body[data-stage="light"] #j13 .stat.fans .ico{background:rgba(15,183,83,.14)!important;color:#0A8F40!important}
body[data-stage="light"] #j13 .stat.pos .ico{background:rgba(47,127,209,.14)!important;color:#2F7FD1!important}
body[data-stage="light"] #j13 .target{
  background:linear-gradient(160deg,#0F4528 0%,#0A2818 55%,#101820 100%)!important;
  border-color:rgba(201,255,61,.32)!important;
  box-shadow:0 8px 28px rgba(15,70,40,.28)!important;
}
body[data-stage="light"] #j13 .target::after{
  opacity:.45!important;
  background-image:linear-gradient(rgba(201,255,61,.08) 1px,transparent 1px),linear-gradient(90deg,rgba(201,255,61,.08) 1px,transparent 1px)!important;
}
body[data-stage="light"] #j13 .target .tt,
body[data-stage="light"] #j13 .target .big{color:#F2F5FA!important}
body[data-stage="light"] #j13 .target .big small{color:#9AA3B2!important}
body[data-stage="light"] #j13 .target .tpct{color:#C9FF3D!important}
body[data-stage="light"] #j13 .target .tmeta{color:#9AA3B2!important}
body[data-stage="light"] #j13 .target .tmeta a{color:#C9FF3D!important}
body[data-stage="light"] #j13 .target .prog{background:rgba(255,255,255,.14)!important;box-shadow:inset 0 1px 3px rgba(0,0,0,.2)!important}
body[data-stage="light"] #j13 .target .prog i{box-shadow:0 0 12px rgba(201,255,61,.55)!important}
body[data-stage="light"] #j13 .recruit{
  background:linear-gradient(155deg,#F2FAEB 0%,#E8F5DC 100%)!important;
  border-color:rgba(15,183,83,.28)!important;
  box-shadow:0 4px 16px rgba(15,183,83,.10)!important;
}
body[data-stage="light"] #j13 .recruit .rh{color:#3D4859!important}
body[data-stage="light"] #j13 .recruit .rc{color:#14161C!important}
body[data-stage="light"] #j13 .recruit .rc small{color:#707786!important}
body[data-stage="light"] #j13 .recruit .prog{background:rgba(15,183,83,.15)!important}
body[data-stage="light"] #j13 .recruit .prog i{box-shadow:0 0 10px rgba(201,255,61,.45)!important}
body[data-stage="light"] #j13 .body{background:#F0F2F7!important}
body[data-stage="light"] #j13 .lbl{color:#5C6472!important}
body[data-stage="light"] #j13 .short{
  background:#FFFFFF!important;
  border-color:#E2E6F0!important;
  box-shadow:0 3px 12px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #j13 .short .sl{color:#14161C!important}
body[data-stage="light"] #j13 .short .si{
  background:linear-gradient(145deg,#F1F8F2,#E6F3E9)!important;
  border:1px solid rgba(15,183,83,.16)!important;
}
body[data-stage="light"] #j13 .short .badge{
  background:#E4362B!important;
  box-shadow:0 2px 8px rgba(228,54,43,.35)!important;
}
body[data-stage="light"] #j13 .ticket{
  background:linear-gradient(150deg,#FFF5F4 0%,#FFFFFF 55%,#F8F9FC 100%)!important;
  border-color:rgba(228,54,43,.32)!important;
  box-shadow:0 6px 22px rgba(228,54,43,.12)!important;
}
body[data-stage="light"] #j13 .ticket::before{
  display:block!important;
  background:radial-gradient(55% 75% at 88% 10%,rgba(228,54,43,.18),transparent 62%)!important;
}
body[data-stage="light"] #j13 .ticket .tlbl{color:#B4241B!important}
body[data-stage="light"] #j13 .ticket .tclub{color:#14161C!important}
body[data-stage="light"] #j13 .rewcard.claim{
  background:linear-gradient(150deg,#F2FAEB 0%,#E8F5DC 100%)!important;
  border-color:rgba(15,183,83,.30)!important;
  box-shadow:0 4px 16px rgba(15,183,83,.10)!important;
}
/* ---- light: Mini-Games wheel arena (J17 · #j16) ---- */
body[data-stage="light"] #j16 .wheelarena{
  background:
    radial-gradient(80% 42% at 50% 18%,rgba(201,255,61,.10),transparent 62%),
    linear-gradient(#FAFBFE,#F4F6FB 58%)!important;
}
body[data-stage="light"] #j16 .wheelwrap::before{
  background:repeating-linear-gradient(90deg,rgba(18,178,74,.14) 0 14px,rgba(10,125,52,.08) 14px 28px)!important;
}
body[data-stage="light"] #j16 .wheeldisc svg{
  filter:drop-shadow(0 12px 26px rgba(24,40,80,0))!important;
}
body[data-stage="light"] #j16 .wprompt{
  color:var(--t1)!important;
  text-shadow:none!important;
}
body[data-stage="light"] #j16 .wforce .wl{
  color:#4A7A12!important;
}
body[data-stage="light"] #j16 .wforce .wl:last-child{
  color:#B45309!important;
}
body[data-stage="light"] #j16 .wforce-rail{
  border-color:var(--line2)!important;
  background-color:#F0F2F7!important;
}
body[data-stage="light"] #j16 .wforce-rail b{
  background:#14161C!important;
  box-shadow:0 0 8px rgba(20,22,28,.25)!important;
}
body[data-stage="light"] #j16 .wforce.lock b{
  background:var(--volt,#C9FF3D)!important;
  box-shadow:0 0 14px rgba(201,255,61,.45)!important;
}
body[data-stage="light"] #j16 .wchip.on{
  box-shadow:0 0 0 2px #14161C,0 0 14px rgba(201,255,61,.35)!important;
}
body[data-stage="light"] #j16 .wnote{
  color:var(--t2)!important;
}
body[data-stage="light"] #j16 .pt{
  background:var(--card)!important;
  border-color:var(--line)!important;
  color:var(--t1)!important;
  box-shadow:var(--shadow-sm)!important;
}
body[data-stage="light"] #j16 .tile.wheel{
  background:linear-gradient(150deg,#F8F5FF 0%,#F0EBFF 38%,#FAFAFE 100%)!important;
  border-color:rgba(138,92,246,.22)!important;
  box-shadow:0 0 28px rgba(138,92,246,.14),inset 0 1px 0 rgba(255,255,255,.95)!important;
}
body[data-stage="light"] #j16 .tile.wheel::before{
  background:radial-gradient(ellipse 75% 55% at 88% 32%,rgba(138,92,246,.14),transparent 58%)!important;
}
body[data-stage="light"] #j16 .tile.wheel::after{
  border-color:rgba(138,92,246,.18)!important;
  box-shadow:inset 0 0 16px rgba(138,92,246,.06)!important;
}
body[data-stage="light"] #j16 .tile.wheel .tn{
  color:var(--t1)!important;
}
body[data-stage="light"] #j16 .tile.wheel .tp{
  color:#6A3CD6!important;
}
body[data-stage="light"] #j16 .tile.wheel .tclass{
  background:rgba(255,255,255,.78)!important;
  border-color:rgba(138,92,246,.18)!important;
  color:var(--t1)!important;
  backdrop-filter:blur(6px)!important;
}
body[data-stage="light"] #j16 .tile.wheel .tplay{
  background:linear-gradient(140deg,#9B6FFF 0%,#8A5CF6 45%,#6A3CD6 100%)!important;
  color:#fff!important;
  box-shadow:0 8px 20px rgba(138,92,246,.32),0 0 16px rgba(138,92,246,.18)!important;
  border:1px solid rgba(255,255,255,.35)!important;
}
body[data-stage="light"] #j16 .tile.wheel .miniwheel{
  opacity:1!important;
  border-color:rgba(138,92,246,.35)!important;
  box-shadow:0 0 20px rgba(138,92,246,.28),0 4px 16px rgba(24,40,80,0)!important;
  animation:spin 12s linear infinite!important;
}
body[data-stage="light"] #j16 .tile.wheel .miniwheel::after{
  background:radial-gradient(circle,#F8F5FF 0%,#EDE8FF 100%)!important;
  border-color:rgba(138,92,246,.22)!important;
  box-shadow:0 0 6px rgba(138,92,246,.18)!important;
}
/* ---- Discovery / Live Now (E1 · #j20) ---- */
body[data-stage="light"] #j20>.phone,
body[data-stage="light"] #mount#j20>.phone{
  background:linear-gradient(180deg,#0B0D13 0%,#12161F 52%,#090B10 100%)!important;
  color:#F2F5FA!important;border-color:rgba(255,255,255,.08)!important;
}
body[data-stage="dark"] #j20>.phone,
body[data-stage="dark"] #mount#j20>.phone{
  background:linear-gradient(180deg,#07090D 0%,#0C1018 50%,#080A10 100%)!important;
  color:#F2F5FA!important;border-color:rgba(255,255,255,.08)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04)!important;
}
body[data-stage="light"] #j20 .appbar,
body[data-stage="light"] #mount#j20 .appbar,
body[data-stage="dark"] #j20 .appbar,
body[data-stage="dark"] #mount#j20 .appbar{
  background:linear-gradient(180deg,rgba(16,20,28,.94),rgba(7,9,13,.62))!important;
  border-bottom-color:rgba(255,255,255,.07)!important;
}
body[data-stage="light"] #j20 .logo b,
body[data-stage="light"] #j20 .bigtitle,
body[data-stage="light"] #mount#j20 .logo b,
body[data-stage="light"] #mount#j20 .bigtitle,
body[data-stage="dark"] #j20 .logo b,
body[data-stage="dark"] #j20 .bigtitle,
body[data-stage="dark"] #mount#j20 .logo b,
body[data-stage="dark"] #mount#j20 .bigtitle{
  color:#F2F5FA!important;
}
body[data-stage="light"] #j20 .hbtn,
body[data-stage="light"] #mount#j20 .hbtn,
body[data-stage="dark"] #j20 .hbtn,
body[data-stage="dark"] #mount#j20 .hbtn{
  background:rgba(255,255,255,.07)!important;
  border:1px solid rgba(255,255,255,.11)!important;
  color:#F2F5FA!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.06),0 4px 12px rgba(0,0,0,.28)!important;
}
body[data-stage="light"] #j20 .fchip:not(.on),
body[data-stage="light"] #mount#j20 .fchip:not(.on),
body[data-stage="dark"] #j20 .fchip:not(.on),
body[data-stage="dark"] #mount#j20 .fchip:not(.on){
  background:rgba(23,29,39,.9)!important;
  color:#8A939F!important;
  border:1px solid rgba(255,255,255,.08)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04)!important;
  animation:none!important;
}
body[data-stage="light"] #j20 .fchip.on:not(.pkchip),
body[data-stage="light"] #mount#j20 .fchip.on:not(.pkchip),
body[data-stage="dark"] #j20 .fchip.on:not(.pkchip),
body[data-stage="dark"] #mount#j20 .fchip.on:not(.pkchip){
  background:linear-gradient(135deg,#DEFF7A,#C9FF3D)!important;
  color:#0A0C10!important;
  border-color:rgba(201,255,61,.85)!important;
  box-shadow:0 0 0 1px rgba(201,255,61,.35),0 4px 16px rgba(201,255,61,.32)!important;
  animation:none!important;
}
body[data-stage="light"] #j20 .fchip.pkchip:not(.on),
body[data-stage="light"] #mount#j20 .fchip.pkchip:not(.on),
body[data-stage="dark"] #j20 .fchip.pkchip:not(.on),
body[data-stage="dark"] #mount#j20 .fchip.pkchip:not(.on){
  background:rgba(23,29,39,.9)!important;
  color:#98A2B3!important;
  border:1px solid rgba(255,255,255,.08)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04)!important;
  animation:none!important;
}
body[data-stage="light"] #j20 .fchip.pkchip.on,
body[data-stage="light"] #mount#j20 .fchip.pkchip.on,
body[data-stage="dark"] #j20 .fchip.pkchip.on,
body[data-stage="dark"] #mount#j20 .fchip.pkchip.on{
  background:linear-gradient(135deg,#FF3B5C,#7A2BFF)!important;
  color:#fff!important;
  border:none!important;
  box-shadow:0 0 0 1px rgba(255,59,92,.35),0 4px 16px rgba(122,43,255,.4)!important;
  animation:none!important;
}
body[data-stage="light"] #j20 .hero,
body[data-stage="light"] #mount#j20 .hero,
body[data-stage="dark"] #j20 .hero,
body[data-stage="dark"] #mount#j20 .hero{
  border:1px solid rgba(201,255,61,.14)!important;
  box-shadow:0 24px 56px rgba(0,0,0,.58),0 0 0 1px rgba(255,255,255,.04),inset 0 0 80px rgba(0,0,0,.22)!important;
}
body[data-stage="light"] #j20 .hero .headline,
body[data-stage="light"] #j20 .hero .hn,
body[data-stage="light"] #j20 .hero .sc,
body[data-stage="light"] #j20 .hero .tm,
body[data-stage="light"] #j20 .hero .viewers,
body[data-stage="light"] #mount#j20 .hero .headline,
body[data-stage="light"] #mount#j20 .hero .hn,
body[data-stage="light"] #mount#j20 .hero .sc,
body[data-stage="light"] #mount#j20 .hero .tm,
body[data-stage="light"] #mount#j20 .hero .viewers,
body[data-stage="dark"] #j20 .hero .headline,
body[data-stage="dark"] #j20 .hero .hn,
body[data-stage="dark"] #j20 .hero .sc,
body[data-stage="dark"] #j20 .hero .tm,
body[data-stage="dark"] #j20 .hero .viewers,
body[data-stage="dark"] #mount#j20 .hero .headline,
body[data-stage="dark"] #mount#j20 .hero .hn,
body[data-stage="dark"] #mount#j20 .hero .sc,
body[data-stage="dark"] #mount#j20 .hero .tm,
body[data-stage="dark"] #mount#j20 .hero .viewers{
  color:#fff!important;
}
body[data-stage="light"] #j20 .hero .hc,
body[data-stage="light"] #mount#j20 .hero .hc,
body[data-stage="dark"] #j20 .hero .hc,
body[data-stage="dark"] #mount#j20 .hero .hc{
  color:rgba(255,255,255,.72)!important;
}
body[data-stage="light"] #j20 .badge-live,
body[data-stage="light"] #mount#j20 .badge-live,
body[data-stage="dark"] #j20 .badge-live,
body[data-stage="dark"] #mount#j20 .badge-live{
  background:linear-gradient(135deg,#FF4A6A,#FF3B5F)!important;
  color:#fff!important;
  box-shadow:0 6px 18px rgba(255,59,95,.48),0 0 20px rgba(255,59,95,.22)!important;
}
body[data-stage="light"] #j20 .joinbtn,
body[data-stage="light"] #mount#j20 .joinbtn,
body[data-stage="dark"] #j20 .joinbtn,
body[data-stage="dark"] #mount#j20 .joinbtn{
  background:linear-gradient(135deg,#DEFF7A,#C9FF3D)!important;
  color:#0A0C10!important;
  border:1px solid rgba(255,255,255,.28)!important;
  box-shadow:0 8px 22px rgba(201,255,61,.45)!important;
}
body[data-stage="light"] #j20 .golive,
body[data-stage="light"] #mount#j20 .golive,
body[data-stage="dark"] #j20 .golive,
body[data-stage="dark"] #mount#j20 .golive{
  z-index:30!important;
  background:linear-gradient(135deg,#EEFF8A 0%,#C9FF3D 48%,#A8E820 100%)!important;
  color:#0A0C10!important;
  border:1px solid rgba(255,255,255,.35)!important;
  box-shadow:0 20px 44px rgba(201,255,61,.65),0 0 0 5px #07090D,0 0 36px rgba(201,255,61,.32)!important;
}
body[data-stage="light"] #j20 .rowhead .t,
body[data-stage="light"] #mount#j20 .rowhead .t,
body[data-stage="dark"] #j20 .rowhead .t,
body[data-stage="dark"] #mount#j20 .rowhead .t{
  color:#F2F5FA!important;
}
body[data-stage="light"] #j20 .rowhead .a,
body[data-stage="light"] #mount#j20 .rowhead .a,
body[data-stage="dark"] #j20 .rowhead .a,
body[data-stage="dark"] #mount#j20 .rowhead .a{
  color:#C9FF3D!important;
}
body[data-stage="light"] #j20 .rcard,
body[data-stage="light"] #mount#j20 .rcard,
body[data-stage="dark"] #j20 .rcard,
body[data-stage="dark"] #mount#j20 .rcard{
  background:#10141C!important;
  border:1px solid rgba(255,255,255,.08)!important;
  box-shadow:0 14px 32px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.05)!important;
}
body[data-stage="light"] #j20 .rcard .rt,
body[data-stage="light"] #j20 .rcard .rhn,
body[data-stage="light"] #mount#j20 .rcard .rt,
body[data-stage="light"] #mount#j20 .rcard .rhn,
body[data-stage="dark"] #j20 .rcard .rt,
body[data-stage="dark"] #j20 .rcard .rhn,
body[data-stage="dark"] #mount#j20 .rcard .rt,
body[data-stage="dark"] #mount#j20 .rcard .rhn{
  color:#fff!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hqbtn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .guestbanner,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .obanner,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .levelcard,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mod{
  background:var(--card)!important;color:var(--t1)!important;border-color:var(--line)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .logo b,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mod .mt{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.amber,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dnote.amber,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dnote.gold{
  color:#8A5A00!important;
}
/* ---- light: J19 call screens — voice/video (#j18) ---- */
body[data-stage="light"] #mount>.phone:has(.callbg),
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:has(.callbg){
  background:linear-gradient(180deg,#F4F6FB 0%,#E8EDF6 100%)!important;
}
body[data-stage="light"] #mount>.phone:has(.videofull),
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:has(.videofull){
  background:#E8EDF6!important;
}
/* video call: full-bleed, transparent white status bar (any stage) */
#mount>.phone:has(.videofull),[id^="j"]:not(.sflgiftwrap)>.phone:has(.videofull){padding-top:0!important}
#mount>.phone:has(.videofull)>.sfl-statusbar,[id^="j"]:not(.sflgiftwrap)>.phone:has(.videofull)>.sfl-statusbar{background:transparent!important;color:#F4F6FA!important}
body[data-stage="light"] #mount .callbg,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callbg{
  filter:blur(28px) brightness(1.12) saturate(1.05)!important;
  opacity:.34!important;
}
body[data-stage="light"] #mount .callbg::after,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callbg::after{
  background:linear-gradient(to bottom,rgba(244,246,251,.84),rgba(232,237,246,.96))!important;
}
body[data-stage="light"] #mount .callstate,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callstate{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount .callstate[style*="color:var(--green)"],
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callstate[style*="color:var(--green)"]{
  color:var(--green)!important;
}
body[data-stage="light"] #mount .callname,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callname{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount .callsub,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callsub{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount .callsub.num,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callsub.num{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount .netq,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .netq{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount .callava,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callava{
  border-color:rgba(20,30,60,.14)!important;
  box-shadow:0 8px 28px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #mount .callava .pulse,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callava .pulse{
  border-color:rgba(47,203,110,.42)!important;
}
body[data-stage="light"] #mount .callinner .dnote.info,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callinner .dnote.info{
  background:var(--raised2)!important;border-color:var(--line2)!important;color:var(--t2)!important;
}
body[data-stage="light"] #mount .callinner>div[style*="color:rgba(255,255,255"],
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .callinner>div[style*="color:rgba(255,255,255"]{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount .cc .b:not(.end):not(.accept),
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .cc .b:not(.end):not(.accept){
  background:var(--raised2)!important;border-color:var(--line2)!important;color:var(--t1)!important;backdrop-filter:none!important;
}
body[data-stage="light"] #mount .cc .b.on,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .cc .b.on{
  background:#fff!important;color:var(--t1)!important;border-color:var(--line2)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="light"] #mount .cc .b.end,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .cc .b.end{
  background:var(--live)!important;color:#fff!important;border:none!important;
}
body[data-stage="light"] #mount .cc .b.accept,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .cc .b.accept{
  background:var(--green)!important;color:#fff!important;border:none!important;
}
body[data-stage="light"] #mount .cc .l,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .cc .l{
  color:var(--t2)!important;
}
body[data-stage="light"] #mount .videofull::after,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .videofull::after{
  background:linear-gradient(to bottom,rgba(244,246,251,.62),transparent 24%,transparent 66%,rgba(232,237,246,.78))!important;
}
body[data-stage="light"] #mount .vname,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .vname{
  color:var(--t1)!important;text-shadow:0 1px 8px rgba(255,255,255,.75)!important;
}
body[data-stage="light"] #mount .vdur,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .vdur{
  color:var(--t2)!important;text-shadow:0 1px 6px rgba(255,255,255,.65)!important;
}
body[data-stage="light"] #mount .selfview,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .selfview{
  border-color:rgba(255,255,255,.82)!important;box-shadow:0 8px 20px rgba(24,40,80,0)!important;
}
body[data-stage="light"] #j18 .celebrate>div[style*="color:#fff"],
body[data-stage="light"] #mount .celebrate>div[style*="color:#fff"],
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .celebrate>div[style*="color:#fff"]{
  color:var(--t1)!important;
}
/* ---- theme-aware JS overlays / sheets ---- */
.sflsheetwrap{position:absolute;inset:0;z-index:748;display:flex;align-items:flex-end;background:rgba(4,6,10,.52)}
.sflsheet-panel{width:100%;background:var(--card);border-top-left-radius:22px;border-top-right-radius:22px;padding:14px 16px 24px;box-shadow:0 -20px 50px rgba(0,0,0,.35);font-family:Manrope,-apple-system,sans-serif;color:var(--t1)}
body[data-stage="light"] .sflsheet-panel{box-shadow:0 -20px 50px rgba(24,40,80,0)}
.sflsheet-grab{width:38px;height:4px;border-radius:2px;background:var(--line2);margin:0 auto 14px}
.sflsheet-title{font-size:15px;font-weight:800;color:var(--t1);margin-bottom:10px}
.sflsheet-sub{font-size:12.5px;font-weight:700;color:var(--t2);margin-bottom:14px}
.sflsheet-row,.lang-opt,.pp-cam,.pp-gal{display:flex;align-items:center;padding:12px 8px;border-bottom:1px solid var(--line);font-weight:750;font-size:14px;color:var(--t1);cursor:pointer;gap:12px}
.sflsheet-cancel,.sh-cancel{text-align:center;margin-top:12px;padding:12px;background:var(--raised2);border-radius:12px;font-weight:800;color:var(--t1);cursor:pointer}
.sflsheet-danger{text-align:center;padding:13px;background:var(--coral,#E4362B);color:#fff;border-radius:12px;font-weight:800;cursor:pointer}
.sflguestwrap{position:absolute;inset:0;z-index:760;display:flex;align-items:flex-end;background:rgba(4,6,10,.45)}
.sflguest-panel{width:100%;background:#fff;border-radius:22px 22px 0 0;padding:10px 0 18px;box-shadow:0 -16px 40px rgba(0,0,0,.28);color:#14161C;font-family:Manrope,-apple-system,sans-serif}
.sflguest-head{display:flex;align-items:center;gap:10px;padding:6px 16px 12px}
.sflguest-av{width:42px;height:42px;border-radius:50%;background-size:cover;background-position:center;background-color:#DCE2EC;flex:none}
.sflguest-name{flex:1;font-size:16px;font-weight:800;letter-spacing:-.2px;display:flex;align-items:center;gap:6px;cursor:pointer}
.sflguest-name .chev{color:#9AA2B1;font-weight:700}
.sflguest-mention{height:32px;padding:0 12px;border-radius:999px;background:#2F7FD1;color:#fff;font-size:12.5px;font-weight:800;display:flex;align-items:center;cursor:pointer}
.sflguest-gift{width:34px;height:34px;border-radius:50%;background:linear-gradient(140deg,#FFD54F,#FF9E00);display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;flex:none}
.sflguest-row{display:flex;align-items:center;gap:14px;padding:14px 20px;font-size:16px;font-weight:650;color:#1A1D24;border-top:1px solid #EEEFF3;cursor:pointer}
.sflguest-row .gic{width:26px;height:26px;display:flex;align-items:center;justify-content:center;flex:none;color:#3A4050}
.sflguest-row .gic svg{width:22px;height:22px;display:block}
.sflguest-row.danger{color:#E4362B}
.sflguest-row.danger .gic{color:#E4362B}
.sflguest-cancel{text-align:center;padding:16px;font-size:16px;font-weight:650;color:#8B93A3;cursor:pointer}
.ds-club{display:flex;align-items:center;gap:12px;padding:13px;border:1px solid var(--line);border-radius:14px;margin-top:9px;cursor:pointer;background:var(--card)}
.ds-club .ds-name{font-size:15px;font-weight:800;color:var(--t1)}
.ds-club .ds-meta{font-size:11.5px;font-weight:700;color:var(--t2);margin-top:2px}
.tm-opt{display:flex;align-items:center;justify-content:space-between;padding:13px;border:1.5px solid var(--line);border-radius:13px;margin-top:9px;font-size:14px;font-weight:750;color:var(--t1);cursor:pointer;background:var(--card)}
.tm-opt.on{border-color:var(--blue,#2F7FD1);background:rgba(47,127,209,.12)}
.es-field{height:46px;border-radius:12px;background:var(--raised2);display:flex;align-items:center;padding:0 14px;font-size:14px;font-weight:700;color:var(--t1);outline:none;border:1px solid var(--line)}
.sflgalwrap{background:var(--bg)!important;color:var(--t1)!important}
.sflgalwrap .gal-hdr{display:flex;align-items:center;gap:12px;padding:16px;color:var(--t1)}
.sflgalwrap .gal-close{width:34px;height:34px;border-radius:50%;background:var(--raised);display:flex;align-items:center;justify-content:center;font-size:16px;cursor:pointer;color:var(--t1)}
/* ---- dark: extended surface remap ---- */
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .valchart,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .summary,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .wdl,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .method,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modecard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .roomcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .permcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .smcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .formcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgtable,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ttable,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gtarget,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .spr,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mbox,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .actrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .endstat,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sumbox,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chartcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sbox,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .valblock,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutybar,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .heldcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .psummary,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .prow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .actopt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .durchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .infopanel,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cand,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .award,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .statbox,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ptable,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .recip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .miniorder,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .plsearch,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rulestrip .r,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutyp,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .vcard .info,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fixcard .info,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gfix,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .notif,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .msgrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgtab,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .kcat,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mgcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gamecard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .use,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .refchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .req,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tabs i.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segtabs i.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cc .b.on{
  background:var(--card)!important;border-color:var(--line)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tab.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgtab.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .kcat.on{
  background:var(--raised2)!important;color:var(--t1)!important;border-color:var(--line2)!important;
}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tab.on,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg.on,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab.on,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cc .b.on{
  background:var(--t1)!important;color:var(--card)!important;border-color:var(--t1)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .qt.tasks{background:linear-gradient(145deg,rgba(15,183,83,.2),rgba(15,183,83,.08))!important;color:#6EE7A0!important;border:1px solid rgba(15,183,83,.28)!important}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .qt.rewards{background:linear-gradient(145deg,rgba(255,179,0,.18),rgba(255,179,0,.08))!important;color:#FFD56A!important;border:1px solid rgba(255,179,0,.28)!important}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .qt.pred{background:linear-gradient(145deg,rgba(47,127,209,.2),rgba(47,127,209,.08))!important;color:#8FC0F0!important;border:1px solid rgba(47,127,209,.28)!important}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .qt.players{background:linear-gradient(145deg,rgba(228,54,43,.2),rgba(228,54,43,.08))!important;color:#FF9A8F!important;border:1px solid rgba(228,54,43,.28)!important}
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .target .tt,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .target .big,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rewcard .rt,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ticket .tclub,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stat.fans .v,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stat.pos .v,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmrow .cmn,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mg-title,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mg-name,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .msg-name,
body[data-stage="light"] #mount>.phone,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .thread-name{
  color:var(--t1)!important;
}
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .htitle,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .cname,
body[data-stage="light"] #mount .hero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .hero .fanview,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .htitle,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .pn,
body[data-stage="light"] #mount .phero,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phero .pid{
  color:#fff!important;
}
body[data-stage="dark"] .mm-lbl{color:#8892A4}
body[data-stage="light"] .mm-lbl{color:#707786}
/* ---- dark: semantic notes (after generic card remap) ---- */
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.info{
  background:rgba(47,127,209,.12)!important;border-color:rgba(47,127,209,.28)!important;color:#8FC0F0!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.amber,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dnote.amber,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dnote.gold{
  background:rgba(255,179,0,.12)!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.coral{
  background:rgba(255,59,95,.12)!important;border-color:rgba(255,59,95,.28)!important;color:#FF9AB0!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .note.green{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
/* ---- dark: extra surfaces + hardcoded light leaks ---- */
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .opt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .choose .opt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hubcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hubcard.tour,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .docframe,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sbadge,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tab,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segtabs,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tabs,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .setrow,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .field,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .toggle,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tipnote,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .warn,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .warn.y,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .checkrow .ck,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stage .sd.now,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .home .fc,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .waurl,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .waapp,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .wasearch,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .wafield,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .reqno,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .guestgate .gb .signin,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet-panel,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .nbtn.no,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .durchip,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rulestrip .r,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chartcard,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sbox,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .actopt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutyp,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .optrow.danger .oi{
  background:var(--card)!important;border-color:var(--line)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .choose .opt.rec{
  background:linear-gradient(115deg,rgba(15,183,83,.14),var(--card))!important;border-color:rgba(15,183,83,.28)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .choose .opt:not(.rec){
  border-color:rgba(255,179,0,.24)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .guestwhy{
  background:linear-gradient(135deg,rgba(124,77,255,.14),rgba(47,127,209,.10))!important;border-color:rgba(124,77,255,.22)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gfx-cta{
  background:rgba(255,179,0,.12)!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .collsum{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmgrpend{
  background:rgba(255,179,0,.12)!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmgrask{
  background:linear-gradient(155deg,#1A1E28,#141922)!important;border-color:rgba(255,194,61,.22)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmgrask>div:first-child{
  box-shadow:0 0 0 1.5px rgba(255,194,61,.32)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .cmgrask>div[style*="flex:1"]>div:last-child{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sic.g{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sic.r{
  background:rgba(228,54,43,.12)!important;border-color:rgba(228,54,43,.28)!important;color:#FF9A8F!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sic.gold,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .checkrow .ck.seed{
  background:rgba(255,179,0,.12)!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sic.grey{
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sic.y,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .warn.y,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .durchip.on{
  background:rgba(255,179,0,.12)!important;border-color:rgba(245,158,11,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .checkrow .ck.no{
  background:rgba(228,54,43,.12)!important;border-color:rgba(228,54,43,.28)!important;color:#FF9A8F!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sk{
  background:linear-gradient(90deg,var(--raised) 25%,var(--raised2) 50%,var(--raised) 75%)!important;background-size:600px 100%!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .steps i{
  background:var(--raised2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .steps i.on{
  background:linear-gradient(90deg,var(--green1,#0FB753),var(--green2,#7CD843))!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hicon .dot{
  border-color:var(--card)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sw{
  background:var(--raised2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sw.on{
  background:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sw i{
  background:#fff!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .radio{
  border-color:var(--line2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .radio.on{
  border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hchip.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hfilt.on,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .home .fc.on{
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fchip.on:not(.pkchip){
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hqbtn,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .guestbanner,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .obanner,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .levelcard{
  background:linear-gradient(140deg,#171A22,#252A35)!important;color:#F2F5FA!important;border-color:var(--line)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .kv .v,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .idfield,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .logo b,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mod .mt,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .feed-item .fb,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .golivecard .gbtn{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .inp .ph,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .inp .eye{
  color:var(--t3)!important;
}
/* ---- dark: preserve dark-native journey accents ---- */
body[data-stage="dark"] #j13 .target{
  background:linear-gradient(160deg,#0d1a10,#0b0e14)!important;border-color:rgba(201,255,61,.2)!important;
}
body[data-stage="dark"] #j13 .stat.wallet,
body[data-stage="dark"] #j13 .stat.comm{
  background:linear-gradient(155deg,#241A05,#14100a)!important;border-color:rgba(255,194,61,.25)!important;
}
body[data-stage="dark"] #j13 .ticket{
  background:linear-gradient(150deg,#2A0C0A,#160708)!important;border-color:rgba(228,54,43,.4)!important;
}
body[data-stage="dark"] #j13 .rewcard.claim{
  background:linear-gradient(150deg,#0f1c0e,#0c1010)!important;border-color:rgba(201,255,61,.3)!important;
}
body[data-stage="dark"] #j13 .hero{
  background:linear-gradient(160deg,#2A0C0A,#120608 70%)!important;border-bottom-color:rgba(255,255,255,.06)!important;
}
/* ---- dark: Buy Coins (J3 · #j2) ---- */
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .exch{
  background:linear-gradient(120deg,rgba(255,179,0,.10),var(--raised))!important;
  border-color:rgba(255,179,0,.28)!important;box-shadow:var(--shadow-sm)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .exch .r{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .exch .r b{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .exchnote{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balhero{
  background:linear-gradient(135deg,#120D03,#2A1F08 55%,#3D2E10)!important;
  box-shadow:0 14px 34px rgba(0,0,0,.42),inset 0 1px 0 rgba(255,215,106,.08)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balhero .who{
  background:rgba(0,0,0,.10)!important;border-top-color:rgba(255,215,106,.12)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balhero .lab,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balhero .amt small{
  color:#E6C87A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balhero .who .id{
  color:#C9B071!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .csbanner{
  background:linear-gradient(135deg,rgba(255,179,0,.08),var(--raised))!important;
  border-color:rgba(255,179,0,.28)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .csbanner .csa{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .prow.total{
  background:linear-gradient(120deg,rgba(255,179,0,.08),var(--card))!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rcard .rtop{
  background:linear-gradient(120deg,rgba(15,183,83,.08),var(--card))!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ticket .thead{
  background:linear-gradient(120deg,rgba(15,183,83,.10),var(--card))!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .privacy,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .optnote{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pkg .usd,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .balr.new .v,
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .rcard .ramt .c{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .pkg.on{
  border-color:var(--green1,#0FB753)!important;
  box-shadow:0 0 0 3px rgba(15,183,83,.18),0 8px 22px rgba(255,179,0,.12)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .warn.b{
  background:rgba(47,127,209,.12)!important;border-color:rgba(47,127,209,.28)!important;color:#8FC0F0!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .taskinfo{
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .liveearn-snack{
  background:linear-gradient(120deg,rgba(255,194,61,.18),rgba(255,158,27,.1))!important;border-color:rgba(255,194,61,.28)!important;color:#FFE1A0!important;box-shadow:0 4px 14px rgba(255,179,0,.12)!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .liveearn-snack b{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sic:not(.g):not(.r):not(.y):not(.gold){
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t2)!important;
}
body[data-stage="dark"] #j16 .tile.wheel{
  background:linear-gradient(150deg,#2E1A52 0%,#241546 42%,#141922 100%)!important;
  border-color:rgba(138,92,246,.38)!important;
  box-shadow:0 14px 40px rgba(0,0,0,.45),0 0 40px rgba(138,92,246,.24),inset 0 1px 0 rgba(138,92,246,.10)!important;
}
body[data-stage="dark"] #j16 .tile.wheel::before{
  background:radial-gradient(ellipse 80% 60% at 85% 35%,rgba(138,92,246,.28),transparent 55%)!important;
}
body[data-stage="dark"] #j16 .tile.wheel::after{
  border-color:rgba(138,92,246,.22)!important;
  box-shadow:inset 0 0 20px rgba(138,92,246,.08)!important;
}
body[data-stage="dark"] #j16 .tile.wheel .tp{color:#C9B6FF!important}
body[data-stage="dark"] #j16 .tile.wheel .tclass{background:rgba(0,0,0,.55)!important;border-color:rgba(138,92,246,.28)!important}
body[data-stage="dark"] #j16 .tile.wheel .tplay{
  background:linear-gradient(140deg,#9B6FFF 0%,#8A5CF6 45%,#6A3CD6 100%)!important;
  box-shadow:0 8px 22px rgba(138,92,246,.42),0 0 18px rgba(138,92,246,.28)!important;
  border:1px solid rgba(255,255,255,.18)!important;
}
body[data-stage="dark"] #j16 .tile.wheel .miniwheel{
  border-color:rgba(138,92,246,.45)!important;
  box-shadow:0 0 24px rgba(138,92,246,.45),0 0 48px rgba(138,92,246,.18),inset 0 0 12px rgba(0,0,0,.25)!important;
  animation:spin 12s linear infinite!important;
}
body[data-stage="dark"] #j16 .balchip.ticket{
  background:linear-gradient(150deg,#122015,#0d1119)!important;border-color:rgba(201,255,61,.28)!important;
}
body[data-stage="dark"] #j16 .pt{
  background:linear-gradient(145deg,rgba(255,255,255,.10),rgba(255,255,255,.02))!important;border-color:rgba(255,255,255,.14)!important;color:#EDEAF3!important;
}
body[data-stage="dark"] #j16 .wforce-rail{
  background-color:#0a0e12!important;border-color:rgba(255,255,255,.28)!important;
}
body[data-stage="dark"] #j18 .giftcard{
  background:linear-gradient(150deg,#241A05,#141922)!important;border-color:rgba(255,194,61,.35)!important;
}
body[data-stage="dark"] #j18 .bubble.recv{
  background:var(--raised2)!important;color:var(--t1)!important;border:1px solid var(--line)!important;
}
body[data-stage="dark"] #j18 .composer .cin,
body[data-stage="dark"] #j18 .composer .cbtn{
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #j18 .fchip.on{
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #j18 .cc .b.on{
  background:var(--raised2)!important;color:var(--t1)!important;border-color:var(--line2)!important;
}
/* ---- dark: global-shell navpill + J6 transfer market accents ---- */
body[data-stage="dark"] #mount>.phone .navpill,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone .navpill{
  background:rgba(18,22,30,.92)!important;border-color:rgba(255,255,255,.1)!important;box-shadow:0 14px 40px rgba(0,0,0,.55)!important;
}
body[data-stage="dark"] #mount>.phone .navpill .navc,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone .navpill .navc{
  border-color:#12151C!important;
}
body[data-stage="dark"] #mount>.phone .navpill .nav:not(.on),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone .navpill .nav:not(.on){
  color:var(--t3)!important;
}
body[data-stage="dark"] #mount>.phone .hbar .av.ha,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone .hbar .av.ha{
  background-color:var(--raised)!important;
  background-size:cover!important;
  background-position:center!important;
  border:2px solid rgba(201,255,61,.42)!important;
  box-shadow:0 0 0 1px rgba(255,255,255,.06),0 0 14px rgba(201,255,61,.14)!important;
  outline:none!important;
}
body[data-stage="dark"] #mount>.phone .selavatar,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone .selavatar{
  border-color:rgba(201,255,61,.42)!important;
  box-shadow:0 0 12px rgba(201,255,61,.14)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .valblock,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .valblock,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .dutybar,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutybar,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .heldcard,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .heldcard{
  background:linear-gradient(120deg,rgba(255,179,0,.14),rgba(255,179,0,.06))!important;border-color:rgba(255,179,0,.28)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .valblock .vl,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .valblock .vl,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .dutybar .dh,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutybar .dh,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .heldcard .ha,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .heldcard .ha{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .valblock .vv,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .valblock .vv,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .dutybar .dd,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutybar .dd,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .heldcard .hs,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .heldcard .hs{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .psummary,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .psummary{
  background:var(--raised)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .psummary .pp,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .psummary .pp{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .prow .pi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .prow .pi,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .psummary .pi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .psummary .pi{
  border-color:var(--line2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .tabs i:not(.on),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tabs i:not(.on){
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .escrow-note,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .escrow-note{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .dutyp.ok,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutyp.ok{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .dutyp.ok .n,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .dutyp.ok .n{
  color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .prow .listed,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .prow .listed{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .prow .listed.loan,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .prow .listed.loan{
  background:rgba(255,179,0,.12)!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .tipnote,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tipnote{
  background:rgba(255,179,0,.10)!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .vbadge,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .vbadge{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .mv.up,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mv.up{
  background:rgba(15,183,83,.12)!important;color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .mv.flat,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mv.flat{
  background:var(--raised)!important;color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .mv.down,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mv.down{
  background:rgba(255,59,95,.12)!important;color:#FF9AB0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .stage .sd.now,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stage .sd.now{
  border-color:var(--gold1)!important;color:var(--gold1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .stage .sd.wait,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .stage .sd.wait{
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t3)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .actopt .ai,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .actopt .ai{
  background:var(--raised)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .grab,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .grab{
  background:var(--line2)!important;
}
/* ---- dark: seg/mode tabs — volt active pill ---- */
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .modeseg,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .chtabs,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .segtabs,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segtabs,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .seg,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .seg{
  background:var(--raised)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg.on,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg.on,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab.on,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab.on,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .segtabs i.on,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segtabs i.on,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .segopt.on:not(.loan):not(.perm),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segopt.on:not(.loan):not(.perm){
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;box-shadow:0 4px 14px rgba(201,255,61,.22)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg:not(.on),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .modeseg .mseg:not(.on),
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab:not(.on),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .chtabs .tab:not(.on),
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .segtabs i:not(.on),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segtabs i:not(.on),
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .segopt:not(.on),
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .segopt:not(.on){
  color:var(--t2)!important;
}
/* ---- dark: room permissions setup (j7 · GL-01B) ---- */
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .permcard .pi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .permcard .pi{
  background:var(--raised)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .permcard .later,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .permcard .later{
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .permcard .done,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .permcard .done{
  color:#7CD843!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .permdots i,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .permdots i{
  background:rgba(255,255,255,.14)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .permdots i.on,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .permdots i.on{
  background:linear-gradient(140deg,var(--green1,#0FB753),var(--green2,#7CD843))!important;
}
/* ---- dark: formation cards — game surface ---- */
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .formcard,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .formcard{
  background:linear-gradient(155deg,#1A1E28,#141922)!important;border-color:rgba(255,255,255,.08)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .formcard.on,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .formcard.on{
  border-color:rgba(15,183,83,.45)!important;box-shadow:0 0 0 3px rgba(15,183,83,.14)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .formcard .fn,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .formcard .fn{
  color:var(--t1)!important;
}
/* ---- dark: league / tournament / grade cards (j12) ---- */
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgtable,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgtable,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .ttable,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ttable,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .gtarget,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gtarget,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .spr,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .spr,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .mbox,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .mbox,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .actrow,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .actrow,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .tourcard,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .tourcard,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .countrypill,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .countrypill,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .fixcard2,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .fixcard2,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .squadrow,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .squadrow,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet{
  background:linear-gradient(155deg,#1A1E28,#141922)!important;border-color:rgba(255,255,255,.08)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .thd,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .thd{
  background:var(--raised)!important;color:var(--t3)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgr,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgr,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .ttr,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ttr{
  color:var(--t1)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgr .cf,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgr .cf,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgr .rk,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgr .rk,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .ttr .col,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ttr .col{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgr .cn,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgr .cn,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgr .pts,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgr .pts,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .ttr .tn,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ttr .tn,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .ttr .col.pts,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .ttr .col.pts{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgr.you,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgr.you{
  background:linear-gradient(90deg,rgba(228,54,43,.14),transparent)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgtab.on,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgtab.on{
  background:var(--volt,#C9FF3D)!important;color:#0A1400!important;border-color:var(--volt,#C9FF3D)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gt2,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gt2,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gu,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gu{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gt2 span,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gt2 span{
  color:#6EE7A0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gbar,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .gtarget .gbar{
  background:var(--raised2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .prizeline,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .prizeline{
  background:repeating-linear-gradient(90deg,rgba(255,179,0,.12) 0 8px,transparent 8px 14px)!important;color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lgcount,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lgcount{
  background:rgba(228,54,43,.12)!important;border-color:rgba(228,54,43,.28)!important;color:#FF9A8F!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .lrow.cur,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .lrow.cur{
  background:rgba(228,54,43,.10)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .hubcard.grade,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hubcard.grade{
  background:linear-gradient(140deg,rgba(15,183,83,.14),var(--card))!important;border-color:rgba(15,183,83,.28)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .hubcard.grade .hv,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .hubcard.grade .hv{
  color:#6EE7A0!important;
}
/* ---- dark: Club Grade screen (#j11 · PR-04) ---- */
body[data-stage="dark"] #j11 .gradehero{
  background:radial-gradient(90% 70% at 50% -10%,rgba(255,179,0,.18),transparent 55%),radial-gradient(80% 60% at 50% 100%,rgba(228,54,43,.22),transparent 50%),linear-gradient(180deg,#1A1210 0%,#0E1016 55%,#080A10 100%)!important;
  border-color:rgba(255,179,0,.15)!important;
  box-shadow:0 16px 40px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.05)!important;
}
body[data-stage="dark"] #j11 .gtarget{
  background:linear-gradient(155deg,#152018 0%,#101820 55%,#141922 100%)!important;
  border-color:rgba(15,183,83,.28)!important;
  border-top-color:var(--green1)!important;
  box-shadow:0 8px 24px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.04)!important;
}
body[data-stage="dark"] #j11 .gtarget .gbar{
  background:rgba(255,255,255,.08)!important;
  box-shadow:inset 0 1px 3px rgba(0,0,0,.25)!important;
}
body[data-stage="dark"] #j11 .gtarget .gbar i{
  box-shadow:0 0 14px rgba(110,231,160,.45),0 0 4px rgba(15,183,83,.35)!important;
}
body[data-stage="dark"] #j11 .gradestatus{
  background:linear-gradient(155deg,#141922,#1A1E28)!important;
  border-color:rgba(47,127,209,.22)!important;
}
body[data-stage="dark"] #j11 .gradestatus .gsicon{
  background:linear-gradient(140deg,rgba(47,127,209,.22),rgba(47,127,209,.08))!important;
  border-color:rgba(47,127,209,.28)!important;
}
body[data-stage="dark"] #j11 .gradestatus .gstxt{color:var(--t2)!important}
body[data-stage="dark"] #j11 .gradestatus .gstxt b{color:#6EE7A0!important}
body[data-stage="dark"] #j11 .gradecta .btn.ghost{
  background:linear-gradient(180deg,#1E2430,#161B26)!important;
  border-color:rgba(255,255,255,.12)!important;
  box-shadow:0 4px 14px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.06)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .spr .cn,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .spr .cn{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .spr .amt .v,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .spr .amt .v{
  color:#FFD56A!important;
}
/* ---- dark: end live sheet + summary (j7) ---- */
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .endstat,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .endstat{
  background:var(--raised)!important;border:1px solid var(--line)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .endstat .ev,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .endstat .ev{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .endstat .ev.gold,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .endstat .ev.gold,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sumbox .sv.gold,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sumbox .sv.gold{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .endstat .el,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .endstat .el,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sumbox .sl,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sumbox .sl{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sumbox .sv,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sumbox .sv{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .btn.danger,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .btn.danger{
  background:transparent!important;color:var(--red,#E4362B)!important;border:1.5px solid rgba(228,54,43,.35)!important;box-shadow:none!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .taskdone,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .taskdone,
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .celebrate .sic,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .celebrate .sic{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
/* ---- dark: live engagement light sheets (j8) ---- */
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .expl.gold,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .expl.gold{
  background:linear-gradient(135deg,rgba(255,179,0,.16),rgba(255,179,0,.06))!important;border-color:rgba(255,179,0,.28)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .expl.split,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .expl.split{
  background:linear-gradient(100deg,rgba(47,127,209,.14),rgba(228,54,43,.10))!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .keynote,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .keynote{
  background:rgba(47,127,209,.12)!important;border-color:rgba(47,127,209,.28)!important;color:#8FC0F0!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .formula,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .formula{
  background:var(--raised)!important;border-color:var(--line)!important;color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .drow .k,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .drow .k{
  color:var(--t2)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .drow .v,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .drow .v{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="background:#fff"],
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="background:#fff"],
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="background: #fff"],
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="background: #fff"]{
  background:var(--raised)!important;border-color:var(--line)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="background:linear-gradient(120deg,#FFF7E4"],
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="background:linear-gradient(120deg,#FFF7E4"]{
  background:linear-gradient(120deg,rgba(255,179,0,.16),rgba(255,179,0,.08))!important;border-color:rgba(255,179,0,.28)!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="color:var(--goldDeep)"],
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="color:var(--goldDeep)"],
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet .drow .v.gold,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet .drow .v.gold{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="color:#8A6410"],
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap)>.phone:not(.splash):not(.welcome):not(.room) .sheet div[style*="color:#8A6410"]{
  color:var(--t2)!important;
}
body[data-stage="dark"] #j5 .body>div[style*="F2FBF5"],
body[data-stage="dark"] #mount .body>div[style*="F2FBF5"]{
  background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;
}
.sflclubopt{display:flex;align-items:center;gap:12px;padding:13px 10px;border-bottom:1px solid var(--line);cursor:pointer}
.sflclubopt:last-of-type{border-bottom:none}
.sflclubopt.dis{opacity:.52;cursor:default}
.sflclubopt .coi{width:38px;height:38px;border-radius:11px;background:var(--raised2);display:flex;align-items:center;justify-content:center;font-size:17px;flex:none}
.sflclubopt .coi.danger{background:rgba(228,54,43,.12)}
.sflclubopt .coi.gold{background:rgba(255,194,61,.16)}
.sflclubopt .cot{font-size:14px;font-weight:800;color:var(--t1)}
.sflclubopt .cos{font-size:11px;font-weight:700;color:var(--t2);margin-top:2px}
.sflclubopt-sub{font-size:12px;font-weight:700;color:var(--t2);margin-bottom:10px}
body[data-stage="dark"] .sflclubopt .coi.danger{background:rgba(228,54,43,.18)}
body[data-stage="dark"] .sflclubopt .coi.gold{background:rgba(255,194,61,.14)}
.sflsheet-linkrow{display:flex;align-items:center;gap:8px;background:var(--raised2);border:1px solid var(--line);border-radius:12px;padding:11px 13px;margin-bottom:16px}
.sflsheet-qrwrap{display:inline-block;background:var(--card);padding:9px;border-radius:14px;box-shadow:var(--shadow-sm);border:1px solid var(--line)}
.shch-lbl{font-size:10px;font-weight:750;color:var(--t1);white-space:nowrap}
.sflcoin{background:transparent!important;background-image:none!important;border:none!important;box-shadow:none!important;color:transparent!important;overflow:visible!important;padding:0!important;display:inline-flex!important;align-items:center;justify-content:center;line-height:0;font-size:0!important}
.sflcoin svg{width:100%;height:100%;display:block}
.sflemoji{display:inline-flex;width:1.15em;height:1.15em;vertical-align:-.2em;flex:none}
.sflemoji svg{width:100%;height:100%;display:block}
/* ---- header menu + modal ---- */
.hdrscreen{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;padding:0 8px;line-height:1.25;text-align:center}
.hdrscreen .sc{max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px;font-weight:800;color:#EAEEF5;letter-spacing:-.2px}
body[data-stage="light"] .hdrscreen .sc{color:#14161C}
.hdrcount{font-size:11px;font-weight:700;opacity:.6;font-variant-numeric:tabular-nums;color:#EAEEF5}
body[data-stage="light"] .hdrcount{color:#14161C}
.hdrnav{display:flex;align-items:center;gap:6px;flex:none;margin-left:auto}
.ppchev{font-size:22px;line-height:1;font-weight:600;padding:0;letter-spacing:0}
.ppchev.off,.ppchev:disabled{opacity:.32;cursor:default;pointer-events:none}
.ppchev.off:hover,.ppchev:disabled:hover{border-color:rgba(255,255,255,.14)}
body[data-stage="light"] .ppchev.off:hover,body[data-stage="light"] .ppchev:disabled:hover{border-color:#DCE2EC}
.mm-theme{display:flex;align-items:center;gap:10px;width:100%;padding:12px 14px;border-radius:12px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);font-family:inherit;font-size:14px;font-weight:800;color:inherit;cursor:pointer;text-align:left}
body[data-stage="light"] .mm-theme{background:#F7F8FC;border-color:#DCE2EC;color:#14161C}
body[data-stage="dark"] .mm-theme{color:#EAEEF5}
.mm-theme:hover{border-color:#C9FF3D}
.mm-theme-ic{font-size:18px;line-height:1;flex:none}
.mm-theme-lbl{flex:1}
.sflmodal{position:fixed;inset:0;z-index:1000;background:rgba(4,6,10,.62);-webkit-backdrop-filter:blur(5px);backdrop-filter:blur(5px);display:none;align-items:center;justify-content:center;padding:16px;overflow-y:auto}
.sflmodal.open{display:flex}
.sflmodal-card{background:#12151d;border:1px solid rgba(255,255,255,.12);border-radius:18px;padding:16px;width:min(430px,94vw);max-height:calc(100vh - 32px);display:flex;flex-direction:column;box-shadow:0 30px 80px rgba(0,0,0,.6);overflow:hidden}
body[data-stage="light"] .sflmodal-card{background:#fff;border-color:#DCE2EC;color:#14161C}
body[data-stage="dark"] .sflmodal-card .brand{color:#EAEEF5}
body[data-stage="light"] .sflmodal-card .brand{color:#14161C}
.mm-top{display:flex;align-items:center;margin-bottom:12px;flex:none}
.mm-top .brand{margin-right:auto}
.mm-lbl{font-size:11px;font-weight:800;letter-spacing:.5px;text-transform:uppercase;color:#8892A4;margin-bottom:8px;flex:none}
.mm-scroll{flex:1;min-height:0;overflow-y:auto;-webkit-overflow-scrolling:touch;padding-right:2px}
.mm-foot{flex:none;margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,.08)}
body[data-stage="light"] .mm-foot{border-top-color:#DCE2EC}
.mm-nav{display:flex;align-items:center;gap:12px;margin-top:12px}
.mm-nav .ppnavbtn{flex:1}
.mm-nav .ppcount{margin:0;min-width:auto}
/* ---- J2-16 Club Home — Member (#j1 · .clubhome) ---- */
body[data-stage="light"] #mount .phone.clubhome,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome{
  background:linear-gradient(180deg,#F4F6FB 0%,color-mix(in srgb,var(--ck) 4%,#F4F6FB) 100%)!important;
}
body[data-stage="light"] #mount .phone.clubhome .hero::before,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .hero::before{
  background:radial-gradient(120% 90% at 50% 110%,rgba(0,0,0,.48),transparent 58%),radial-gradient(80% 60% at 0% 0%,color-mix(in srgb,var(--ck) 32%,transparent),transparent 50%),radial-gradient(70% 50% at 100% 20%,rgba(8,10,16,.28),transparent 55%)!important;
}
body[data-stage="light"] #mount .phone.clubhome .sp-member,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .sp-member{
  background:linear-gradient(135deg,#0FB753,#7CD843)!important;color:#fff!important;
  border-color:rgba(255,255,255,.35)!important;box-shadow:0 4px 16px rgba(15,183,83,.34),inset 0 1px 0 rgba(255,255,255,.35)!important;
}
body[data-stage="light"] #mount .phone.clubhome .detailbody>.card,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .detailbody>.card{
  background:linear-gradient(145deg,#FFF8E8,#FFFCF4 45%,#fff)!important;
  border-color:color-mix(in srgb,var(--gold1) 44%,#fff)!important;
  box-shadow:0 8px 24px rgba(176,137,0,.11),inset 0 1px 0 rgba(255,255,255,.9)!important;
}
body[data-stage="light"] #mount .phone.clubhome .cmgrask,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmgrask{
  background:linear-gradient(145deg,#FFF6DC,#FFFCF2 55%,#fff)!important;
  border-color:color-mix(in srgb,var(--gold1) 40%,#fff)!important;
  box-shadow:0 8px 22px rgba(176,137,0,.10)!important;
}
body[data-stage="light"] #mount .phone.clubhome .cmgrask>div:first-child,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmgrask>div:first-child{
  box-shadow:0 0 0 1.5px color-mix(in srgb,var(--gold1) 42%,#fff),0 6px 16px rgba(255,158,11,.26)!important;
}
body[data-stage="light"] #mount .phone.clubhome .qa,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa{
  background:linear-gradient(180deg,#fff,#F7F8FC)!important;border-color:#ECEEF5!important;
}
body[data-stage="light"] #mount .phone.clubhome .onlinebar,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .onlinebar,
body[data-stage="light"] #mount .phone.clubhome .chatprev,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .chatprev,
body[data-stage="light"] #mount .phone.clubhome .giftlead,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .giftlead{
  background:linear-gradient(180deg,#fff,#F7F8FC)!important;border-color:#ECEEF5!important;
}
body[data-stage="light"] #mount .phone.clubhome .onav .omore,
body[data-stage="light"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .onav .omore{
  background:linear-gradient(155deg,var(--ck2),var(--ck))!important;color:#fff!important;border-color:#fff!important;
}
body[data-stage="dark"] #mount .phone.clubhome,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome{
  background:linear-gradient(180deg,#080A10 0%,color-mix(in srgb,var(--ck) 8%,#080A10) 100%)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .hero::before,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .hero::before{
  background:radial-gradient(120% 90% at 50% 110%,rgba(0,0,0,.72),transparent 58%),radial-gradient(80% 60% at 0% 0%,color-mix(in srgb,var(--ck) 22%,transparent),transparent 50%),radial-gradient(70% 50% at 100% 20%,rgba(0,0,0,.45),transparent 55%)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .hero::after,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .hero::after{
  background:linear-gradient(180deg,color-mix(in srgb,var(--ck) 42%,transparent) 0%,rgba(8,10,16,.12) 26%,rgba(8,10,16,.72) 68%,#080A10 100%)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .hero .hbadge,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .hero .hbadge{
  border-color:#080A10!important;box-shadow:inset 0 2px 6px rgba(255,255,255,.22),0 10px 28px color-mix(in srgb,var(--ck) 55%,transparent),0 0 20px color-mix(in srgb,var(--ck) 35%,transparent)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .sp-member,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .sp-member{
  background:linear-gradient(135deg,#0FB753,#C9FF3D)!important;color:#0A1400!important;
  border-color:rgba(201,255,61,.35)!important;box-shadow:0 0 18px rgba(201,255,61,.32),0 4px 14px rgba(15,183,83,.28),inset 0 1px 0 rgba(255,255,255,.22)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .detailbody>.card,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .detailbody>.card{
  background:linear-gradient(155deg,#1A1608,#141922 55%,#12161E)!important;
  border-color:rgba(255,194,61,.28)!important;box-shadow:0 10px 28px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,215,106,.08)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .detailbody>.card::before,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .detailbody>.card::before{
  opacity:.9!important;
}
body[data-stage="dark"] #mount .phone.clubhome .detailbody>.card [style*="B08900"],
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .detailbody>.card [style*="B08900"]{
  color:#FFD56A!important;
}
body[data-stage="dark"] #mount .phone.clubhome .detailbody>.card .bar-track,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .detailbody>.card .bar-track{
  background:rgba(255,255,255,.08)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .detailbody>.card .bar-fill.gold,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .detailbody>.card .bar-fill.gold{
  box-shadow:0 0 14px rgba(255,194,61,.45)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .cmgrask,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmgrask{
  background:linear-gradient(155deg,#1A1608,#141922)!important;
  border-color:rgba(255,194,61,.30)!important;box-shadow:0 10px 26px rgba(0,0,0,.30),inset 0 1px 0 rgba(255,215,106,.06)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .cmgrask>div:first-child,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmgrask>div:first-child{
  box-shadow:0 0 0 1.5px rgba(255,194,61,.38),0 0 16px rgba(255,194,61,.22)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .cmgrask>div[style*="flex:1"]>div:first-child,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmgrask>div[style*="flex:1"]>div:first-child{
  color:var(--t1)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .btn.club,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .btn.club{
  background:linear-gradient(145deg,var(--ck2),var(--ck) 52%,var(--ckd))!important;
  box-shadow:0 14px 34px color-mix(in srgb,var(--ck) 55%,transparent),0 0 24px color-mix(in srgb,var(--ck) 28%,transparent),inset 0 1px 0 rgba(255,255,255,.18)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .qa,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa{
  background:linear-gradient(180deg,#171D27,#141922)!important;border-color:rgba(255,255,255,.09)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .qa .qi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa .qi{
  border-color:rgba(255,255,255,.08)!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .qa:nth-child(1) .qi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa:nth-child(1) .qi{
  background:linear-gradient(155deg,rgba(15,183,83,.22),rgba(15,183,83,.10))!important;border-color:rgba(15,183,83,.28)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .qa:nth-child(2) .qi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa:nth-child(2) .qi{
  background:linear-gradient(155deg,rgba(31,168,255,.20),rgba(31,168,255,.08))!important;border-color:rgba(31,168,255,.26)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .qa:nth-child(3) .qi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa:nth-child(3) .qi{
  background:linear-gradient(155deg,rgba(255,179,0,.20),rgba(255,179,0,.08))!important;border-color:rgba(255,179,0,.28)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .qa:nth-child(4) .qi,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .qa:nth-child(4) .qi{
  background:linear-gradient(155deg,rgba(124,77,255,.20),rgba(124,77,255,.08))!important;border-color:rgba(124,77,255,.26)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .lvcard,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .lvcard{
  border-color:rgba(255,255,255,.10)!important;box-shadow:0 12px 28px rgba(0,0,0,.42)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .lvcard .lvb,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .lvcard .lvb{
  box-shadow:0 0 16px rgba(255,65,108,.62)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .onlinebar,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .onlinebar,
body[data-stage="dark"] #mount .phone.clubhome .chatprev,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .chatprev,
body[data-stage="dark"] #mount .phone.clubhome .giftlead,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .giftlead,
body[data-stage="dark"] #mount .phone.clubhome .feed-item,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .feed-item{
  background:linear-gradient(180deg,#171D27,#141922)!important;border-color:rgba(255,255,255,.09)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .onav .oav,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .onav .oav{
  border-color:#141922!important;box-shadow:0 2px 10px rgba(0,0,0,.35)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .onav .omore,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .onav .omore{
  background:linear-gradient(155deg,var(--ck2),var(--ck))!important;color:#fff!important;border-color:#141922!important;
}
body[data-stage="dark"] #mount .phone.clubhome .sechd .sa,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .sechd .sa{
  background:rgba(228,54,43,.12)!important;border-color:rgba(228,54,43,.24)!important;color:#FF9A8F!important;
}
body[data-stage="dark"] #mount .phone.clubhome .cmsg,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmsg{
  color:var(--t2)!important;border-bottom-color:rgba(255,255,255,.08)!important;
}
body[data-stage="dark"] #mount .phone.clubhome .cmsg b,
body[data-stage="dark"] [id^="j"]:not(.sflgiftwrap) .phone.clubhome .cmsg b{
  color:var(--t1)!important;
}
/* ---- UI polish: Games hub (J17 · #j16) ---- */
body[data-stage="light"] #j16 .balchip:first-child{background:linear-gradient(145deg,#FFF8E8,#FFFCF4)!important;border-color:#FFE199!important;box-shadow:0 4px 14px rgba(255,179,0,.12)!important}
body[data-stage="light"] #j16 .balchip:first-child .bv{color:var(--goldDeep)!important}
body[data-stage="light"] #j16 .balchip:nth-child(2){background:linear-gradient(145deg,#EAFBF9,#F4FFFE)!important;border-color:rgba(18,181,168,.28)!important;box-shadow:0 4px 14px rgba(18,181,168,.10)!important}
body[data-stage="light"] #j16 .balchip:nth-child(2) .bv{color:#0A6E66!important}
body[data-stage="light"] #j16 .balchip.ticket{background:linear-gradient(150deg,#F2FAEB,#E8F5DC)!important;border-color:rgba(201,255,61,.35)!important;box-shadow:0 4px 16px rgba(201,255,61,.14)!important}
body[data-stage="light"] #j16 .balchip.ticket .bv{color:#4A7A12!important;text-shadow:none!important}
body[data-stage="light"] #j16 .tile.penalty{border-color:rgba(18,178,74,.22)!important;box-shadow:0 0 24px rgba(18,178,74,.14)!important}
body[data-stage="light"] #j16 .tile.penalty .tn{color:#fff!important}
body[data-stage="light"] #j16 .session{background:linear-gradient(180deg,#fff,#F7F8FC)!important;border-color:var(--line)!important;box-shadow:var(--shadow-sm)!important}
body[data-stage="light"] #j16 .session::before{background:linear-gradient(90deg,transparent,rgba(201,255,61,.35),transparent)!important}
body[data-stage="light"] #j16 .session .sv{color:var(--t1)!important}
body[data-stage="light"] #j16 .session .sc:last-child{background:rgba(201,255,61,.06)!important}
body[data-stage="light"] #j16 .note.bonus{background:linear-gradient(135deg,#EAFBF9,#F4FFFE)!important;border-color:rgba(18,181,168,.28)!important;color:#0A6E66!important;box-shadow:0 4px 14px rgba(18,181,168,.08)!important}
body[data-stage="dark"] #j16 .balchip:first-child{border-color:rgba(255,179,0,.28)!important;box-shadow:0 4px 18px rgba(255,179,0,.12),inset 0 1px 0 rgba(255,255,255,.05)!important}
body[data-stage="dark"] #j16 .balchip:nth-child(2){border-color:rgba(56,224,208,.26)!important;box-shadow:0 4px 18px rgba(56,224,208,.10)!important}
body[data-stage="dark"] #j16 .tile.penalty{box-shadow:0 14px 40px rgba(0,0,0,.48),0 0 36px rgba(18,178,74,.16)!important}
body[data-stage="dark"] #j16 .session{box-shadow:0 8px 24px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.05)!important}
body[data-stage="dark"] #j16 .session .sv.net{text-shadow:0 0 16px rgba(201,255,61,.45)!important}
body[data-stage="dark"] #j16 .note.bonus{box-shadow:0 4px 18px rgba(56,224,208,.10)!important}
/* ---- UI polish: Messages inbox (J19 · #j18) ---- */
body[data-stage="light"] #j18 .search{background:#fff!important;border-color:var(--line2)!important;box-shadow:inset 0 1px 3px rgba(24,40,80,0)!important;color:var(--t2)!important}
body[data-stage="light"] #j18 .fchip.on{box-shadow:0 0 0 1px rgba(201,255,61,.3),0 4px 12px rgba(201,255,61,.22)!important}
body[data-stage="light"] #j18 .crow .cn{color:var(--t1)!important}
body[data-stage="light"] #j18 .crow:has(.unread){background:rgba(255,45,110,.04)!important}
body[data-stage="light"] #j18 .crow .cav .dot{border-color:#fff!important}
body[data-stage="dark"] #j18 .search{box-shadow:inset 0 1px 4px rgba(0,0,0,.22)!important}
body[data-stage="dark"] #j18 .fchip.on{box-shadow:0 0 0 1px rgba(201,255,61,.35),0 4px 16px rgba(201,255,61,.28)!important}
body[data-stage="dark"] #j18 .crow:has(.unread){background:rgba(255,45,110,.06)!important;border-radius:14px!important}
body[data-stage="dark"] #j18 .crow .unread{box-shadow:0 3px 12px rgba(255,45,110,.48)!important}
body[data-stage="dark"] #j18 .crow .rolechip.mgr{border-color:rgba(255,194,61,.32)!important}
body[data-stage="dark"] #j18 .crow .rolechip.club{border-color:rgba(228,54,43,.32)!important}
body[data-stage="dark"] #j18 .crow .cav .dot{box-shadow:0 0 0 2px rgba(47,203,110,.3),0 0 10px rgba(47,203,110,.6)!important;border-color:var(--arena)!important}
/* ---- UI polish: Transfer + My Players (J6 · #j5) ---- */
body[data-stage="dark"] #j5 .sbox:first-child{background:linear-gradient(145deg,rgba(255,179,0,.16),rgba(255,179,0,.06))!important;border-color:rgba(255,179,0,.28)!important;box-shadow:0 6px 22px rgba(255,179,0,.12)!important}
body[data-stage="dark"] #j5 .sbox:last-child{background:linear-gradient(145deg,rgba(15,183,83,.14),rgba(15,183,83,.06))!important;border-color:rgba(15,183,83,.28)!important;box-shadow:0 6px 22px rgba(15,183,83,.10)!important}
body[data-stage="dark"] #j5 .sbox .sv.gold{color:#FFD56A!important}
body[data-stage="dark"] #j5 .sbox .sv.up{color:#6EE7A0!important}
body[data-stage="dark"] #j5 .dutybar{background:linear-gradient(135deg,rgba(255,179,0,.14),rgba(255,179,0,.06))!important;border-color:rgba(255,179,0,.28)!important;box-shadow:0 8px 24px rgba(255,179,0,.10)!important}
body[data-stage="dark"] #j5 .dutybar::before{background:linear-gradient(90deg,transparent,rgba(255,179,0,.45),transparent)!important}
body[data-stage="dark"] #j5 .tabs{background:var(--raised)!important;box-shadow:inset 0 1px 3px rgba(0,0,0,.18)!important}
body[data-stage="dark"] #j5 .tabs i.on{background:var(--raised2)!important;box-shadow:0 3px 12px rgba(0,0,0,.28)!important;color:var(--t1)!important}
body[data-stage="dark"] #j5 .prow{background:var(--card)!important;border-color:var(--line)!important;box-shadow:0 4px 16px rgba(0,0,0,.22)!important}
body[data-stage="dark"] #j5 .prow .pi{box-shadow:0 0 0 1.5px var(--line2),0 4px 14px rgba(0,0,0,.32)!important}
body[data-stage="dark"] #j5 .celebrate::before{background:radial-gradient(circle,rgba(255,179,0,.18),transparent 68%)!important}
body[data-stage="dark"] #j5 .revealcard{border-color:rgba(255,179,0,.55)!important;box-shadow:0 22px 52px rgba(255,179,0,.22),0 10px 28px rgba(0,0,0,.42)!important}
body[data-stage="dark"] #j5 .revealcard::after{box-shadow:0 0 32px rgba(255,179,0,.28)!important}
body[data-stage="dark"] #j5 .balrows.card{background:linear-gradient(180deg,var(--card),var(--raised))!important;box-shadow:0 12px 32px rgba(0,0,0,.32)!important}
body[data-stage="dark"] #j5 .celebrate .btn{box-shadow:0 14px 36px rgba(15,183,83,.28)!important}
/* ---- UI polish: Profile G-05 (Global Shell · #j19) ---- */
body[data-stage="light"] #j19 .phero{box-shadow:inset 0 -1px 0 rgba(255,255,255,.12)!important}
body[data-stage="light"] #j19 .followbar{background:rgba(255,255,255,.18)!important;border-color:rgba(255,255,255,.28)!important}
body[data-stage="light"] #j19 .stat{background:#F6F8FC!important;border:1px solid var(--line)!important}
body[data-stage="dark"] #j19 .phero{background:radial-gradient(80% 70% at 92% -8%,rgba(255,255,255,.14),transparent 52%),radial-gradient(60% 50% at 8% 100%,rgba(0,0,0,.38),transparent 55%),linear-gradient(165deg,#E83830 0%,#C01812 38%,#8E0E0C 58%,#5A0806 100%)!important;box-shadow:inset 0 -1px 0 rgba(255,255,255,.06)!important}
body[data-stage="dark"] #j19 .followbar{background:rgba(255,255,255,.10)!important;border-color:rgba(255,255,255,.16)!important;box-shadow:0 8px 28px rgba(0,0,0,.32),inset 0 1px 0 rgba(255,255,255,.10)!important}
body[data-stage="dark"] #j19 .levelcard{border-color:rgba(255,255,255,.10)!important;box-shadow:0 12px 32px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.05)!important}
body[data-stage="dark"] #j19 .levelcard .lbar i{box-shadow:0 0 16px rgba(228,54,43,.55),0 0 8px rgba(243,204,85,.35)!important}
body[data-stage="dark"] #j19 .stat{background:rgba(255,255,255,.05)!important;border:1px solid rgba(255,255,255,.08)!important}
body[data-stage="dark"] #j19 .showrow .shico{background:var(--raised)!important;border-color:var(--line)!important;box-shadow:0 2px 8px rgba(0,0,0,.18)!important}
body[data-stage="dark"] #j19 .showrow .shico.badge{background:linear-gradient(150deg,rgba(47,127,209,.18),rgba(47,127,209,.08))!important;border-color:rgba(47,127,209,.28)!important}
body[data-stage="dark"] #j19 .listrow .li{background:var(--raised)!important;border-color:var(--line)!important;box-shadow:none!important}
body[data-stage="dark"] #j19 .acclist .listrow .li{background:var(--raised)!important;border-color:var(--line)!important;box-shadow:0 2px 8px rgba(0,0,0,.18)!important}
body[data-stage="light"] #j19 .acclist .listrow .li{box-shadow:0 2px 8px rgba(24,40,80,0)!important}
body[data-stage="dark"] #j19 .phone.profile .body{box-shadow:0 -10px 28px rgba(0,0,0,.28)!important}
/* ---- UI polish: Predict & Vote (J5 · #j4) ---- */
body[data-stage="light"] #j4 .body:has(.candgrid)>div:nth-child(3){background:linear-gradient(135deg,#F2FBF5,#E9F9EF)!important;border-color:#BFE9CE!important;color:#187A42!important}
body[data-stage="dark"] #j4 .tabs{background:var(--raised)!important;box-shadow:inset 0 1px 3px rgba(0,0,0,.18)!important}
body[data-stage="dark"] #j4 .tabs i.on{background:var(--raised2)!important;color:var(--t1)!important;box-shadow:0 3px 12px rgba(0,0,0,.28)!important}
body[data-stage="dark"] #j4 .coinbal{background:linear-gradient(120deg,rgba(255,179,0,.18),rgba(255,179,0,.08))!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;box-shadow:0 4px 16px rgba(255,179,0,.12)!important}
body[data-stage="dark"] #j4 .goldchip{background:linear-gradient(120deg,rgba(255,179,0,.16),rgba(255,179,0,.08))!important;border-color:rgba(255,179,0,.28)!important;color:#FFD56A!important;box-shadow:0 3px 12px rgba(255,179,0,.12)!important}
body[data-stage="dark"] #j4 .cand.on{border-color:var(--green1,#0FB753)!important;box-shadow:0 0 0 3px rgba(15,183,83,.22),0 0 28px rgba(15,183,83,.28)!important}
body[data-stage="dark"] #j4 .cand.on .sel{box-shadow:0 4px 16px rgba(15,183,83,.45),0 0 14px rgba(15,183,83,.35)!important}
body[data-stage="dark"] #j4 .body:has(.candgrid)>div:nth-child(3){background:rgba(15,183,83,.12)!important;border-color:rgba(15,183,83,.28)!important;color:#6EE7A0!important;box-shadow:0 4px 16px rgba(15,183,83,.10)!important}
/* ---- responsive: same page works on phone ---- */
html,body{height:100%}
@media (max-width:600px){
  header{padding:8px 12px;gap:10px}
  .hdrscreen .sc{font-size:12px}
  .ppbtn.sm{width:34px;height:34px;font-size:15px}
  .ppchev{font-size:20px}
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
    var light=document.body.getAttribute('data-stage')==='light';
    var isCall=!!(phone.querySelector&&phone.querySelector(':scope > .videofull'));
    var bleed=phone.classList.contains('bleed')||isCall;
    var keepLite=bleed||/splash|welcome|room/.test(phone.className);
    var dark=keepLite||(!light)||lum(getComputedStyle(phone).backgroundColor)<0.5;
    if(!bleed) phone.style.paddingTop='50px';
    var sb=document.createElement('div');sb.className='sfl-statusbar';
    sb.style.cssText='position:absolute;top:0;left:0;right:0;z-index:600;height:50px;display:flex;align-items:center;justify-content:space-between;padding:2px 40px 0 42px;box-sizing:border-box;background:'+(bleed?'transparent':(light?'#F4F6FB':'#080A10'))+';font-family:Manrope,sans-serif;font-size:15px;font-weight:800;letter-spacing:-.3px;color:'+(bleed||dark?'#F4F6FA':'#0E1016');
    sb.innerHTML='<span style="position:relative;z-index:2">9:41</span><div style="position:absolute;left:50%;top:9px;transform:translateX(-50%);width:116px;height:30px;background:#04060A;border-radius:16px"></div><span style="position:relative;z-index:2;display:flex;align-items:center;gap:7px">'+SIG+WIFI+BAT+'</span>';
    phone.insertBefore(sb,phone.firstChild);
    injectNav(phone,!light);
  }

  var NAVCSS=false;
  function ensureNavCss(){ if(NAVCSS)return; NAVCSS=true; var st=document.createElement('style'); st.textContent=
   '.sfl-nav{position:absolute;left:14px;right:14px;bottom:14px;height:62px;border-radius:24px;display:flex;align-items:center;justify-content:space-around;padding:0 6px;z-index:590;font-family:Manrope,-apple-system,sans-serif;background:rgba(255,255,255,.94);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,.75);box-shadow:0 14px 38px rgba(20,30,60,.22)}'
   +'.sfl-nav.dark{background:rgba(18,22,30,.92);border-color:rgba(255,255,255,.1);box-shadow:0 14px 38px rgba(0,0,0,.55)}'
   +'.sfl-nav .nit{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:9.5px;font-weight:800;color:#9AA2B1;letter-spacing:.2px;transition:color .2s;cursor:pointer}'
   +'.sfl-nav.dark .nit{color:#6A7383}'
   +'.sfl-nav .nit .ic{width:42px;height:33px;border-radius:13px;display:flex;align-items:center;justify-content:center;opacity:.62;transition:transform .28s cubic-bezier(.34,1.56,.64,1),background .2s,box-shadow .2s,opacity .2s}.sfl-nav .nit .ic svg{width:22px;height:22px;display:block}'
   +'.sfl-nav .nit.home:not(.on) .ic{color:#E4362B}.sfl-nav .nit.market:not(.on) .ic{color:#2266C9}.sfl-nav .nit.games:not(.on) .ic{color:#7C3AED}.sfl-nav .nit.chats:not(.on) .ic{color:#0EA47D}'
   +'.sfl-nav .nit:active .ic{transform:scale(.9)}'
   +'.sfl-nav .nit.on{color:var(--accent,#E4362B)}'
   +'.sfl-nav .nit.on .ic{opacity:1;color:#fff;transform:translateY(-4px);background:var(--grad,linear-gradient(150deg,#FF6E3D,#E4362B));box-shadow:0 9px 18px var(--glow,rgba(228,54,43,.5)),inset 0 1px 0 rgba(255,255,255,.4);animation:navpop .44s ease}'
   +'.sfl-nav .nit.on .ic svg{color:#fff}'
   +'.sfl-nav .nit.home{--accent:#E4362B;--grad:linear-gradient(150deg,#FF6E3D,#E4362B);--glow:rgba(228,54,43,.5)}'
   +'.sfl-nav .nit.market{--accent:#2266C9;--grad:linear-gradient(150deg,#4AA0F5,#2266C9);--glow:rgba(47,127,209,.5)}'
   +'.sfl-nav .nit.games{--accent:#7C3AED;--grad:linear-gradient(150deg,#A78BFA,#7C3AED);--glow:rgba(124,58,237,.5)}'
   +'.sfl-nav .nit.chats{--accent:#0EA47D;--grad:linear-gradient(150deg,#2DD4A7,#0EA47D);--glow:rgba(14,164,125,.5)}'
   +'@keyframes navpop{0%{transform:translateY(0) scale(.85)}55%{transform:translateY(-7px) scale(1.16)}100%{transform:translateY(-4px) scale(1)}}'
   +'.sfl-nav .nc{position:relative;width:56px;height:56px;border-radius:50%;background:radial-gradient(circle at 35% 28%,#FF7A5C,#FF4A3D 45%,#B4241B);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;margin-top:-26px;box-shadow:0 10px 24px rgba(228,54,43,.55),inset 0 2px 0 rgba(255,255,255,.4);border:3px solid #F4F6FB;animation:navcfloat 2.8s ease-in-out infinite;cursor:pointer}'
   +'.sfl-nav.dark .nc{border-color:#12151C}'
   +'.sfl-nav .nc::after{content:"";position:absolute;inset:-5px;border-radius:50%;border:2px solid rgba(228,54,43,.4);animation:navcring 2.2s ease-out infinite;pointer-events:none}'
   +'.sfl-nav .nc .ic{height:25px;display:flex;align-items:center;justify-content:center}.sfl-nav .nc .ic svg{width:25px;height:25px;display:block}.sfl-nav .nc .nl{font-size:7.5px;font-weight:800;margin-top:2px;letter-spacing:.3px}'
   +'@keyframes navcfloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}@keyframes navcring{0%{transform:scale(.8);opacity:.7}100%{transform:scale(1.35);opacity:0}}';
   document.head.appendChild(st); }
  function injectNav(phone,dark){ var tab=phone.getAttribute&&phone.getAttribute('data-nav'); if(!tab)return; if(phone.querySelector(':scope > .sfl-nav'))return; ensureNavCss();
   var NAVIC={home:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11.5 12 5l8 6.5"/><path d="M6 10.2V19h12v-8.8"/><path d="M10 19v-5h4v5"/></svg>',
     market:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8.5h13l-3.3-3.3M20 15.5H7l3.3 3.3"/></svg>',
     stadium:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9.5c0-2 4-3.6 9-3.6s9 1.6 9 3.6-4 3.6-9 3.6-9-1.6-9-3.6Z"/><path d="M3 9.5V14c0 2 4 3.6 9 3.6s9-1.6 9-3.6V9.5"/><path d="M8 12.4v3.1M16 12.4v3.1M12 13v3.3"/></svg>',
     games:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="10.5" rx="5.25"/><path d="M6.5 11v2.2M5.4 12.1h2.2"/><circle cx="15.6" cy="11.4" r="1.05" fill="currentColor" stroke="none"/><circle cx="18.2" cy="13.6" r="1.05" fill="currentColor" stroke="none"/></svg>',
     chats:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 11.5a8 8 0 0 1-11.6 7.1L4 20l1.4-4.7A8 8 0 1 1 20.5 11.5Z"/></svg>'};
   function it(id,l){return '<div class="nit '+id+(tab===id?' on':'')+'"><span class="ic">'+NAVIC[id]+'</span>'+l+'</div>';}
   var nav=document.createElement('div'); nav.className='sfl-nav'+(dark?' dark':'');
   nav.innerHTML=it('home','Home')+it('market','Market')+'<div class="nc'+((tab==='stadium'||tab==='live')?' on':'')+'"><span class="ic">'+NAVIC.stadium+'</span><span class="nl">Stadium</span></div>'+it('games','Games')+it('chats','Chats');
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
  var flowsel=document.getElementById('flowsel'), scap=document.getElementById('scap'), ct=document.getElementById('counter');
  var og1='<optgroup label="\\u2605 Prototyped flows">', og2='<optgroup label="All journeys">';
  VIEWS.forEach(function(v,i){var o='<option value="'+i+'">'+v.label+'</option>'; if(i<FLOWN)og1+=o; else og2+=o;});
  flowsel.innerHTML=og1+'</optgroup>'+og2+'</optgroup>';
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
  function roomCommentBox(){ var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return null; return phone.querySelector('.rchat')||phone.querySelector('.pkchat'); }
  function pushComment(html,cls){ var box=roomCommentBox(); if(!box)return; var d=document.createElement('div'); d.className='cm'+(cls?(' '+cls):''); d.innerHTML=html; box.appendChild(d); while(box.children.length>50)box.removeChild(box.firstChild); box.scrollTop=box.scrollHeight; }
  function giftHosts(scope){ return [].slice.call(scope.querySelectorAll('.ghost.on')).map(function(h){return (h.getAttribute('data-host')||((h.querySelector('.ghn')||{}).textContent)||'Host').trim();}); }
  function giftQty(scope){ var q=scope.querySelector('.qval'); return q?Math.max(1,parseInt(q.textContent,10)||1):1; }
  function giftRecalc(scope){
    var tile=scope.querySelector('.gtile.on'); var cnt=scope.querySelector('.gselcount'); var btn=scope.querySelector('.gsend');
    var hosts=giftHosts(scope); var n=Math.max(1,hosts.length); var qty=giftQty(scope);
    if(cnt)cnt.textContent=n+' host'+(n!==1?'s':'')+' selected';
    if(tile&&btn){ var nm=((tile.querySelector('.gn')||{}).textContent||'Gift').trim(); var unit=parseInt(((tile.querySelector('.gp')||{}).textContent||'0').replace(/[^0-9]/g,''),10)||0; var total=unit*qty*n; btn.innerHTML='Send '+nm+(qty>1?(' ×'+qty):'')+(n>1?(' · '+n+' hosts'):'')+' · <span class="num" style="margin-left:4px">'+total+'</span>'; }
    var all=scope.querySelectorAll('.ghost').length, sel=scope.querySelectorAll('.ghost.on').length; var sa=scope.querySelector('.gselall'); if(sa)sa.textContent=(sel>=all&&all>0?'Unselect all':'Select all');
  }
  function giftTier(unit){ return unit>=600?4:unit>=200?3:unit>=90?2:unit>=30?1:0; }
  function fxPhone(){ var s=document.getElementById('scaler'); if(!s||!s.firstElementChild)return null; return s.firstElementChild.querySelector('.phone'); }
  function fxReduce(){ return !!(window.matchMedia&&window.matchMedia('(prefers-reduced-motion:reduce)').matches); }
  /* ===== Scalable animated-gift FX registry =====
     Each gift maps to a visual personality: palette [core,deep,light], a particle
     skin, and (optionally) full:true for a full-screen legendary reaction. To add a
     new animated gift later, add ONE line here keyed by lowercase name — any gift not
     listed still auto-themes from its Coin tier, so the system never breaks. Coin
     values / rarity / Possession maths are untouched: FX is purely visual. */
  var GIFT_FX={
    'rose':{glyph:'🌹',pal:['#ff5d8f','#c9184a','#ffd6e4'],particle:'petals',m:'bloom'},
    'football':{glyph:'⚽',pal:['#8bd450','#2f9e44','#f1fbe6'],particle:'sparkle',m:'kick'},
    'match ball':{glyph:'⚽',pal:['#8bd450','#2f9e44','#f1fbe6'],particle:'sparkle',m:'kick'},
    'chant':{glyph:'📣',pal:['#4dabf7','#1c7ed6','#d0ebff'],particle:'bubbles',m:'chant'},
    'scarf':{glyph:'🧣',pal:['#ff6b6b','#e03131','#ffe3e3'],particle:'confetti',m:'wave'},
    'goal celebration':{glyph:'🔥',pal:['#ffa94d','#e8590c','#fff0e0'],particle:'embers',m:'flare'},
    'fireworks':{glyph:'🎆',pal:['#b197fc','#7048e8','#f3f0ff'],particle:'confetti',full:true,m:'fireworks'},
    'lucky clover':{glyph:'🍀',pal:['#69db7c','#2f9e44','#ebfbee'],particle:'sparkle',m:'spinlucky'},
    'dice roll':{glyph:'🎲',pal:['#ff8787','#e03131','#fff5f5'],particle:'confetti',m:'roll'},
    'fortune wheel':{glyph:'🎡',pal:['#ffd43b','#f08c00','#fff9db'],particle:'stars',m:'spinwheel'},
    'lucky envelope':{glyph:'🧧',pal:['#ff6b6b','#c92a2a','#ffe3e3'],particle:'coins',m:'open'},
    'lucky 777':{glyph:'🎰',pal:['#ffd43b','#e67700','#fff9db'],particle:'coins',m:'slot'},
    'jackpot':{glyph:'💰',pal:['#ffd43b','#e67700','#fff9db'],particle:'coins',full:true,m:'coinrain'},
    'home shirt':{glyph:'👕',pal:['#4dabf7','#1971c2','#e7f5ff'],particle:'confetti',m:'unfurl'},
    'keeper gloves':{glyph:'🧤',pal:['#63e6be','#0ca678','#e6fcf5'],particle:'sparkle',m:'save'},
    'golden glove':{glyph:'🧤',pal:['#ffe066','#f08c00','#fff9db'],particle:'sparkle',m:'save'},
    'boots':{glyph:'👟',pal:['#ffd43b','#f08c00','#fff9db'],particle:'sparkle',m:'strike'},
    'captain armband':{glyph:'🎽',pal:['#ffd43b','#e67700','#fff9db'],particle:'sparkle',m:'salute'},
    'trophy':{glyph:'🏆',pal:['#ffe066','#f08c00','#fff9db'],particle:'sparkle',m:'raise'},
    'champions cup':{glyph:'🥇',pal:['#ffe066','#e67700','#fff9db'],particle:'stars',full:true,m:'raise'},
    'golden boot':{glyph:'🥇',pal:['#ffe066','#e67700','#fff9db'],particle:'sparkle',m:'strike'},
    'bouncy ball':{glyph:'🏀',pal:['#ffa94d','#e8590c','#fff0e0'],particle:'bubbles',m:'bounce'},
    'rocket':{glyph:'🚀',pal:['#74c0fc','#1971c2','#e7f5ff'],particle:'streaks',m:'launch'},
    'boom':{glyph:'💣',pal:['#ff922b','#d9480f','#fff0e0'],particle:'embers',m:'explode'},
    'race car':{glyph:'🏎️',pal:['#ff6b6b','#c92a2a','#ffe3e3'],particle:'streaks',m:'drive'},
    'dragon':{glyph:'🐉',pal:['#51cf66','#2b8a3e','#ebfbee'],particle:'embers',full:true,m:'dragonfly'},
    'goat':{glyph:'🐐',pal:['#ffe066','#e67700','#fff9db'],particle:'stars',full:true,m:'legend'},
    'legend crown':{glyph:'👑',pal:['#ffe066','#e67700','#fff9db'],particle:'stars',full:true,m:'descend'},
    'club kit':{glyph:'🎽',pal:['#b197fc','#7048e8','#f3f0ff'],particle:'confetti',m:'unfurl'}
  };
  var GIFT_TIERPAL=[['#cfd6e6','#8b93a7','#ffffff'],['#74c0fc','#1971c2','#e7f5ff'],['#b197fc','#7048e8','#f3f0ff'],['#ffe066','#e67700','#fff9db'],['#ffd43b','#e8590c','#fff9db']];
  var GIFT_TIERPART=['sparkle','sparkle','confetti','stars','stars'];
  function giftSpec(nm,unit){
    var tier=giftTier(unit||0); var key=(nm||'').toLowerCase().trim(); var s=GIFT_FX[key];
    if(!s)s={glyph:'🎁',pal:GIFT_TIERPAL[tier],particle:GIFT_TIERPART[tier],m:'pop'};
    return {glyph:s.glyph,pal:s.pal||GIFT_TIERPAL[tier],particle:s.particle||GIFT_TIERPART[tier],motion:s.m||'pop',tier:tier,full:(s.full===true)||tier>=3,name:nm||'Gift'};
  }
  /* Lightweight canvas particle system — one GPU-composited canvas per send, capped
     count, rAF loop that self-terminates and removes the node. Skinned per gift. */
  function giftParticles(phone,spec){
    if(fxReduce())return {stop:function(){}};
    var W=phone.offsetWidth||390, H=phone.offsetHeight||844, dpr=Math.min(2,window.devicePixelRatio||1);
    var cv=document.createElement('canvas'); cv.className='sflfx-cv'; cv.width=Math.round(W*dpr); cv.height=Math.round(H*dpr);
    cv.style.cssText='position:absolute;inset:0;width:100%;height:100%;z-index:731;pointer-events:none';
    phone.appendChild(cv); var ctx=cv.getContext('2d'); ctx.scale(dpr,dpr);
    var skin=spec.particle, pal=spec.pal, tier=spec.tier;
    var cap=[26,42,64,92,130][tier]||42, parts=[], running=true, t0=null, life=2500+tier*260, spawnEnd=life-700;
    function rnd(a,b){return a+Math.random()*(b-a);}
    function pick(){return pal[Math.floor(Math.random()*pal.length)];}
    function spawn(){
      var p={x:rnd(0.08,0.92)*W,c:pick(),r:rnd(3,7),a:1,rot:rnd(0,6.28),vr:rnd(-0.12,0.12),skin:skin,tw:rnd(0,6.28)};
      if(skin==='petals'||skin==='confetti'){p.y=-20;p.vy=rnd(0.8,2);p.vx=rnd(-0.5,0.5);p.sway=rnd(0.5,1.6);p.r=rnd(5,10);}
      else if(skin==='coins'){p.y=-20;p.vy=rnd(1.4,2.8);p.vx=rnd(-0.4,0.4);p.r=rnd(7,12);}
      else if(skin==='bubbles'){p.y=H+20;p.vy=-rnd(0.9,1.9);p.vx=rnd(-0.4,0.4);p.r=rnd(5,12);}
      else if(skin==='streaks'){p.y=H+20;p.x=rnd(0.15,0.85)*W;p.vy=-rnd(4.5,7.5);p.vx=rnd(-0.3,0.3);p.len=rnd(26,58);p.r=rnd(2,4);}
      else if(skin==='embers'){p.y=H*0.6;p.x=rnd(0.3,0.7)*W;p.vy=-rnd(1,2.6);p.vx=rnd(-0.9,0.9);p.r=rnd(2,5);}
      else {p.y=rnd(0.18,0.82)*H;p.x=rnd(0.1,0.9)*W;p.vy=-rnd(0.2,1);p.vx=rnd(-0.4,0.4);p.r=rnd(2,5);}
      parts.push(p);
    }
    function star(x,y,r,rot){ ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.beginPath();for(var i=0;i<10;i++){var rr=(i%2)?r*0.45:r;var a=Math.PI*i/5-Math.PI/2;ctx.lineTo(Math.cos(a)*rr,Math.sin(a)*rr);}ctx.closePath();ctx.fill();ctx.restore(); }
    function draw(p,el){
      if(p.skin==='confetti'){ ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.fillRect(-p.r/2,-p.r/3,p.r,p.r*0.66);ctx.restore(); return; }
      if(p.skin==='streaks'){ ctx.strokeStyle=p.c;ctx.lineWidth=p.r;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x,p.y+(p.len||30));ctx.stroke(); return; }
      if(p.skin==='petals'){ ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot);ctx.beginPath();ctx.ellipse(0,0,p.r,p.r*0.55,0,0,6.28);ctx.fill();ctx.restore(); return; }
      if(p.skin==='coins'){ ctx.save();ctx.translate(p.x,p.y);ctx.beginPath();ctx.ellipse(0,0,p.r*Math.abs(Math.cos(p.rot))+1.2,p.r,0,0,6.28);ctx.fill();ctx.restore(); return; }
      if(p.skin==='stars'){ star(p.x,p.y,p.r*1.5,p.rot); return; }
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,6.28);ctx.fill();
    }
    function frame(ts){
      if(!running)return; if(t0===null)t0=ts; var el=ts-t0;
      ctx.clearRect(0,0,W,H);
      var glow=(skin==='embers'||skin==='sparkle'||skin==='stars'); ctx.globalCompositeOperation=glow?'lighter':'source-over';
      if(el<spawnEnd){ var need=Math.min(cap,Math.round(cap*(el<300?el/300:1))), rate=Math.ceil(cap/22); for(var s=0;s<rate&&parts.length<need;s++)spawn(); }
      for(var i=parts.length-1;i>=0;i--){ var p=parts[i];
        p.x+=p.vx||0; p.y+=p.vy||0; p.rot+=p.vr||0; if(p.sway)p.x+=Math.sin(p.y*0.03)*p.sway*0.3;
        if(p.y<-40||p.y>H+50){parts.splice(i,1);continue;}
        if(el>spawnEnd)p.a-=0.02; if(p.a<=0){parts.splice(i,1);continue;}
        var a=Math.max(0,Math.min(1,p.a)); if(p.skin==='sparkle'||p.skin==='stars')a*=0.5+0.5*Math.abs(Math.sin(el*0.008+p.tw));
        ctx.globalAlpha=a; ctx.fillStyle=p.c; draw(p,el);
      }
      ctx.globalAlpha=1; ctx.globalCompositeOperation='source-over';
      if((el>life&&parts.length===0)||el>life+1000){ running=false; if(cv.parentNode)cv.parentNode.removeChild(cv); return; }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
    return {stop:function(){running=false; if(cv.parentNode)cv.parentNode.removeChild(cv);}};
  }
  /* Cinematic overlay: fly-in 3D medallion + shockwave + particles + attribution.
     Non-blocking (pointer-events:none) so the timer / totals / controls stay usable. */
  /* Per-gift signature accessories injected into the stage for the marquee motions. */
  function giftAccessory(motion,spec){
    if(motion==='chant')return '<div class="sflm-wave"></div><div class="sflm-wave w2"></div><div class="sflm-wave w3"></div><div class="sflm-notes"><i>♪</i><i>♫</i><i>♩</i><i>♫</i></div>';
    if(motion==='launch')return '<div class="sflm-flame"></div>';
    if(motion==='drive')return '<div class="sflm-speed"></div><div class="sflm-speed s2"></div><div class="sflm-speed s3"></div>';
    if(motion==='explode')return '<div class="sflm-boom"></div>';
    if(motion==='fireworks')return '<div class="sflm-fw a"></div><div class="sflm-fw b"></div><div class="sflm-fw c"></div><div class="sflm-fw d"></div>';
    if(motion==='slot')return '<div class="sflm-slot"><span>7</span><span>7</span><span>7</span></div>';
    if(motion==='spinwheel')return '<div class="sflm-pointer"></div>';
    if(motion==='roll')return '<div class="sflm-die2">'+spec.glyph+'</div>';
    if(motion==='dragonfly')return '<div class="sflm-trail"></div>';
    return '';
  }
  function playGiftFx(spec,meta){
    var phone=fxPhone(); if(!phone)return; ensureFlyCss(); ensureGiftMotionCss();
    var reduce=fxReduce(), pal=spec.pal, tier=spec.tier, full=spec.full, motion=spec.motion||'pop';
    var qty=meta.qty||1, total=meta.total||0, hosts=meta.hosts||[], sender=meta.sender||'You';
    var to=(hosts.length>1)?(hosts.length+' hosts'):(hosts.length===1?hosts[0]:'Host');
    var big=(tier>=2)||full;
    var rings=full?'<div class="sflfx-ring"></div><div class="sflfx-ring r2"></div>':'<div class="sflfx-ring"></div>';
    var beams=(big&&!reduce)?'<div class="sflfx-beams"></div>':'';
    var flash=reduce?'':'<div class="sflfx-flash"></div>';
    var title=big?'<div class="sflfx-title">'+spec.name+'</div>':'';
    var cine='';
    var acc=reduce?'':giftAccessory(motion,spec);
    var wrap=document.createElement('div'); wrap.className='sflfx'+(reduce?' rm':(' m-'+motion))+(full?' full':'')+(big?' big':'');
    wrap.style.setProperty('--c0',pal[0]); wrap.style.setProperty('--c1',pal[1]); wrap.style.setProperty('--c2',pal[2]||'#fff');
    wrap.innerHTML=
      '<div class="sflfx-flood"></div>'+cine+flash+
      '<div class="sflfx-stage">'+beams+rings+acc+
        '<div class="sflfx-hero"><div class="sflfx-disc"><span class="sflfx-shine"></span><span class="sflfx-glyph">'+spec.glyph+'</span></div>'+
        (qty>1?'<div class="sflfx-combo">×<b>1</b></div>':'')+'</div>'+
        title+
      '</div>'+
      '<div class="sflfx-band"><div class="sflfx-bemo">'+spec.glyph+'</div>'+
        '<div class="sflfx-btx"><div class="sflfx-btag">Gift sent</div><div class="sflfx-bn"><b>'+sender+'</b> → <b>'+to+'</b></div>'+
        '<div class="sflfx-bc"><b class="sflfx-bnm">'+spec.name+(qty>1?(' ×'+qty):'')+'</b><span class="sflfx-coin"></span>'+total+'</div></div></div>';
    phone.appendChild(wrap);
    var shakeMotions={explode:1,legend:1,drive:1};
    if((full||shakeMotions[motion])&&!reduce){ phone.classList.add('sflshake'); setTimeout(function(){phone.classList.remove('sflshake');},680); }
    var pc=giftParticles(phone,spec);
    if(qty>1){ var cb=wrap.querySelector('.sflfx-combo b'), cvv=1; var it=setInterval(function(){ cvv++; if(cvv>=qty){cvv=qty;clearInterval(it);} if(cb)cb.textContent=cvv; },80); }
    var life=reduce?1400:(2700+tier*300);
    setTimeout(function(){ wrap.classList.add('out'); },life-380);
    setTimeout(function(){ if(pc)pc.stop(); if(wrap.parentNode)wrap.parentNode.removeChild(wrap); },life+80);
  }
  function sendGift(em,nm,n,unit,hosts,qty){
    qty=Math.max(1,qty||1); n=Math.max(1,n||1); var total=(unit||0)*qty*n;
    var spec=giftSpec(nm,unit); if(em&&em.length<=4)spec.glyph=em;
    playGiftFx(spec,{qty:qty,total:total,hosts:(hosts&&hosts.length)?hosts:['Host'],sender:'You'});
    var who=(hosts&&hosts.length)?hosts:['Host'];
    pushComment('<b style="color:#DCFF8A">You</b> sent '+spec.glyph+' <b style="color:#FFE1A0">'+nm+' ×'+qty+'</b>'+(who.length>1?(' to '+who.length+' hosts'):(' to '+who[0])), 'giftmsg');
  }
  function SFLgiftInteract(scope,tgt,onClose){
    if(tgt.classList&&(tgt.classList.contains('sheet-scrim')||tgt.classList.contains('sflgiftoverlay'))){ if(onClose)onClose(); return true; }
    var gh=tgt.closest('.ghost'); if(gh){ gh.classList.toggle('on'); if(!scope.querySelector('.ghost.on'))gh.classList.add('on'); giftRecalc(scope); return true; }
    if(tgt.closest('.gselall')){ var hs=scope.querySelectorAll('.ghost'); var sel=scope.querySelectorAll('.ghost.on').length; var turnOn=sel<hs.length; [].forEach.call(hs,function(h,i){ if(turnOn)h.classList.add('on'); else h.classList.toggle('on', i===0); }); giftRecalc(scope); return true; }
    if(tgt.closest('.qminus')){ var q=scope.querySelector('.qval'); if(q){var v=Math.max(1,(parseInt(q.textContent,10)||1)-1); q.textContent=v; giftRecalc(scope);} return true; }
    if(tgt.closest('.qplus')){ var q2=scope.querySelector('.qval'); if(q2){var v2=Math.min(99,(parseInt(q2.textContent,10)||1)+1); q2.textContent=v2; giftRecalc(scope);} return true; }
    var gc=tgt.closest('.gcat'); if(gc&&gc.parentElement){ [].forEach.call(gc.parentElement.children,function(c){c.classList&&c.classList.remove('on');}); gc.classList.add('on'); var key=gc.getAttribute('data-k')||'popular'; var first=null; [].forEach.call(scope.querySelectorAll('.gtile'),function(tl){var m=((tl.getAttribute('data-cat')||'').split(' ').indexOf(key)>=0); tl.style.display=m?'':'none'; tl.classList.remove('on'); if(m&&!first)first=tl;}); if(first)first.classList.add('on'); giftRecalc(scope); return true; }
    var gt=tgt.closest('.gtile'); if(gt){ [].forEach.call(scope.querySelectorAll('.gtile'),function(c){c.classList.remove('on');}); gt.classList.add('on'); giftRecalc(scope); return true; }
    if(tgt.closest('.gsend,.btn,.gbtn')){ var t2=scope.querySelector('.gtile.on'); var hosts=giftHosts(scope); var n=Math.max(1,hosts.length); var qty=giftQty(scope); var nm=t2?((t2.querySelector('.gn')||{}).textContent||'Gift').trim():'Gift'; var em=t2?((t2.querySelector('.ge')||{}).textContent||'🎁').trim():'🎁'; var unit=t2?(parseInt(((t2.querySelector('.gp')||{}).textContent||'0').replace(/[^0-9]/g,''),10)||0):0; if(onClose)onClose(); sendGift(em,nm,n,unit,hosts,qty); return true; }
    return false;
  }
  function openGiftSheet(){
    if(SFLguest){goTo('gate');return;}
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflgiftoverlay'))return;
    var ov=document.createElement('div'); ov.className='sflgiftoverlay'; ov.style.cssText='position:absolute;inset:0;z-index:700'; ov.innerHTML=GIFTSHEET;
    phone.appendChild(ov); SFLcoinify(ov); SFLcrest(ov); giftRecalc(ov);
    ov.addEventListener('click',function(e){ e.stopPropagation(); SFLgiftInteract(ov,e.target,function(){ov.remove();}); });
  }
  function guestIcon(kind){
    if(kind==='info') return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="3.2"/><path d="M5.8 19.2c.7-3.2 3.2-5 6.2-5s5.5 1.8 6.2 5"/><circle cx="12" cy="12" r="9.2"/></svg>';
    if(kind==='mgr') return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="10" cy="8" r="3.1"/><path d="M3.8 19.2c.7-3.1 3-4.9 6.2-4.9 1.2 0 2.3.3 3.2.8"/><path d="M17.2 10.2v6.2M14.1 13.3h6.2"/></svg>';
    if(kind==='remove') return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 14.5c0-2.4 3.2-3.6 7-3.6s7 1.2 7 3.6"/><path d="M5 14.5v4.2c0 .6.5 1.1 1.1 1.1h11.8c.6 0 1.1-.5 1.1-1.1V14.5"/><path d="M8.2 10.8c.6-1.5 2-2.5 3.8-2.5s3.2 1 3.8 2.5"/></svg>';
    if(kind==='mute') return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="9" y="3.5" width="6" height="10" rx="3"/><path d="M6.8 11.2a5.2 5.2 0 0 0 10.4 0M12 16.4V20"/><path d="M4.5 5.2l15 14.2"/></svg>';
    if(kind==='ask') return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.5 11.5a8 8 0 0 1-11.6 7.1L4 20l1.4-4.7A8 8 0 1 1 20.5 11.5Z"/><path d="M9.7 9.4a2.3 2.3 0 0 1 4.4.8c0 1.6-2.2 1.9-2.2 3.4"/><path d="M12 16.2h.01"/></svg>';
    if(kind==='pk') return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14.5 14.5 20 20l1-1-4.8-6.2M4 4l6.2 6.2M9.5 14.5 4 20l-1-1 4.8-6.2M20 4l-6.2 6.2"/><path d="M4 4l2.5.6.6 2.5M20 4l-2.5.6-.6 2.5"/></svg>';
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="10" cy="8" r="3.1"/><path d="M3.8 19.2c.7-3.1 3-4.9 6.2-4.9 1.1 0 2.1.2 3 .7"/><path d="M15.4 10.4l6 6M21.4 10.4l-6 6"/></svg>';
  }
  function showGuestSheet(seat){
    if(!seat||seat.classList.contains('open'))return false;
    var staff=(typeof isLiveStaff==='function'&&isLiveStaff());
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return false;
    var nm=((seat.querySelector('.nm')||{}).textContent||'').trim(); if(!nm||nm==='Open')return false;
    if(phone.querySelector('.sflguestwrap')||phone.querySelector('.sflseatwrap'))return true;
    var av=seat.querySelector('.av'); var bg=(av&&(av.style.backgroundImage||(window.getComputedStyle&&getComputedStyle(av).backgroundImage)))||'';
    var isYou=/^you$/i.test(nm)||seat.classList.contains('you');
    var isHostSeat=seat.classList.contains('host');
    var isCo=!!(typeof SFLcoHosts!=='undefined'&&SFLcoHosts[chKey(nm)]);
    var canPk=!isYou&&!isHostSeat;
    function row(act,kind,label,danger){
      return '<div class="sflguest-row'+(danger?' danger':'')+'" data-gact="'+act+'"><div class="gic">'+guestIcon(kind)+'</div>'+label+'</div>';
    }
    var wrap=document.createElement('div'); wrap.className='sflguestwrap';
    wrap.innerHTML='<div class="sflguest-panel">'
      +'<div class="sflguest-head"><div class="sflguest-av" style="background-image:'+bg+'"></div>'
      +'<div class="sflguest-name ssc-profile">'+nm+' <span class="chev">›</span></div>'
      +'<div class="sflguest-mention">@Mention</div><div class="sflguest-gift">🎁</div></div>'
      +row('info','info','Information',false)
      +(canPk?row('ask','ask','Ask a Question',false):'')
      +(canPk?row('pk','pk','Start PK Battle',false):'')
      +(staff?row('mgr','mgr',isCo?'Remove manager':'Set as manager',false):'')
      +(staff?row('remove','remove','Remove guest',false):'')
      +(staff?row('mute','mute','No mic allowed within 30 minutes',true):'')
      +(staff?row('kick','kick','Kick out within 3 hours',true):'')
      +'<div class="sflguest-cancel">Cancel</div></div>';
    phone.appendChild(wrap);
    var gav=wrap.querySelector('.sflguest-av'); if(gav&&bg&&bg!=='none') gav.style.backgroundImage=bg;
    wrap.addEventListener('click',function(e){
      e.stopPropagation();
      if(e.target===wrap||e.target.closest('.sflguest-cancel')){ wrap.remove(); return; }
      if(e.target.closest('.sflguest-mention')){ wrap.remove(); if(typeof pushComment==='function') pushComment('<b style="color:#DCFF8A">You</b> @'+nm+' '); sflToast('@'+nm); return; }
      if(e.target.closest('.sflguest-gift')){ wrap.remove(); openGiftSheet(); return; }
      if(e.target.closest('.sflguest-name')){ wrap.remove(); showSeatCard(seat); return; }
      var rowEl=e.target.closest('.sflguest-row'); if(!rowEl) return;
      var act=rowEl.getAttribute('data-gact');
      if(act==='info'){ wrap.remove(); showSeatCard(seat); return; }
      if(act==='ask'){ wrap.remove(); if(typeof showAskCompose==='function') showAskCompose(nm); return; }
      if(act==='pk'){ wrap.remove(); sflToast('⚔️ PK request sent to '+nm+' — waiting for them to accept'); if(typeof pushComment==='function') pushComment('<b style="color:#DCFF8A">You</b> challenged <b style="color:#FFE1A0">'+nm+'</b> to a PK Battle ⚔️','askmsg'); return; }
      if(act==='mgr'){ wrap.remove(); if(typeof chToggle==='function') chToggle(nm); return; }
      if(act==='remove'){
        wrap.remove();
        if(isYou||isHostSeat){ sflToast(isYou?"That's your seat":'Cannot remove the host'); return; }
        kickFromSeat(seat,nm); SFLkicked=true; sflToast(nm+' removed · notified · can\\'t rejoin'); return;
      }
      if(act==='mute'){
        var mi=seat.querySelector('.micind');
        if(mi){ mi.classList.add('muted'); mi.textContent='🔇'; }
        wrap.remove(); sflToast('No mic for '+nm+' · 30 minutes'); return;
      }
      if(act==='kick'){
        wrap.remove();
        if(isYou||isHostSeat){ sflToast(isYou?"That's your seat":'Cannot kick the host'); return; }
        kickFromSeat(seat,nm); SFLkicked=true; sflToast(nm+' kicked out · notified · blocked 3 hours'); return;
      }
    });
    return true;
  }
  function showSeatCard(seat){
    if(!seat||seat.classList.contains('open'))return false;
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return false;
    var nm=((seat.querySelector('.nm')||{}).textContent||'').trim(); if(!nm||nm==='Open')return false;
    if(phone.querySelector('.sflseatwrap'))return true;
    var av=seat.querySelector('.av'); var bg=(av&&av.style.backgroundImage)||''; var pos=((seat.querySelector('.pos')||{}).textContent||'').trim();
    var isYou=/^you$/i.test(nm); var _fn=((VIEWS[curJ].screens[curS]||{}).fnum)||''; var isHostView=(_fn==='GL-03H'||_fn==='GL-WA-H'); var isStaffView=isHostView||_fn==='GL-CH-C'; var isCo=!!(typeof SFLcoHosts!=='undefined'&&SFLcoHosts[String(nm).toLowerCase().replace(/\s+/g,'')]);
    var h=0; for(var i=0;i<nm.length;i++)h=(h*31+nm.charCodeAt(i))>>>0;
    var lvl=8+(h%13), fp=(2+(h%9))+'.'+(h%10)+'k', gifts=40+(h%210), streak=3+(h%22);
    var stat=function(v,l){return '<div style="flex:1"><div style="font-size:15px;font-weight:800;color:#fff">'+v+'</div><div style="font-size:9.5px;font-weight:800;letter-spacing:.3px;color:#8892A4;margin-top:2px;text-transform:uppercase">'+l+'</div></div>';};
    var wrap=document.createElement('div'); wrap.className='sflseatwrap';
    wrap.style.cssText='position:absolute;inset:0;z-index:720;display:flex;align-items:center;justify-content:center;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px)';
    wrap.innerHTML='<div style="position:relative;width:272px;background:linear-gradient(180deg,#1b2030,#12151d);border:1px solid rgba(255,255,255,.14);border-radius:22px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.65);color:#EAEEF5;font-family:Manrope,-apple-system,sans-serif">'
      +'<div class="ssc-close" style="position:absolute;top:11px;right:11px;width:26px;height:26px;border-radius:50%;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:#fff;cursor:pointer;z-index:3">✕</div>'
      +'<div style="height:66px;background:linear-gradient(135deg,#E4362B,#8E1912)"></div>'
      +'<div style="padding:0 18px 18px;margin-top:-40px;text-align:center">'
      +'<div class="ssc-av" style="width:80px;height:80px;border-radius:50%;margin:0 auto;background-color:#222;background-size:cover;background-position:center top;border:3px solid #12151d;box-shadow:0 8px 20px rgba(0,0,0,.5)"></div>'
      +'<div style="font-size:18px;font-weight:800;margin-top:9px">'+nm+' <span style="color:#3FA9F5;font-size:14px">✓</span></div>'
      +'<div style="display:flex;gap:6px;align-items:center;justify-content:center;font-size:12px;font-weight:750;color:#B7C0CE;margin-top:3px"><span style="display:inline-flex;width:16px;height:18px;background:linear-gradient(150deg,#E4362B,#8E1912);border-radius:3px;align-items:center;justify-content:center;font-size:8px;font-weight:800;color:#fff">RD</span> Red District FC'+(pos?(' · '+pos):'')+'</div>'
      +'<div style="display:flex;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.06);border-radius:14px;padding:11px 4px;margin-top:14px">'+stat('Lv '+lvl,'Level')+'<div style="width:1px;background:rgba(255,255,255,.09)"></div>'+stat(fp,'Possession')+'<div style="width:1px;background:rgba(255,255,255,.09)"></div>'+stat(gifts,'Gifts')+'</div>'
      +'<div style="display:flex;gap:6px;justify-content:center;margin-top:11px"><span style="font-size:10px;font-weight:800;background:rgba(201,255,61,.16);color:#C9FF3D;padding:5px 10px;border-radius:8px">🔥 '+streak+'-day streak</span><span style="font-size:10px;font-weight:800;background:rgba(255,255,255,.08);padding:5px 10px;border-radius:8px">'+(isYou?'That\\'s you':'Supporter')+'</span></div>'
      +(isYou
        ? '<div class="ssc-profile" style="margin-top:14px;display:flex;align-items:center;justify-content:center;gap:7px;background:rgba(255,255,255,.08);font-weight:800;font-size:13px;padding:12px;border-radius:12px;cursor:pointer">👤 View Profile</div>'
        : '<div style="display:flex;gap:8px;margin-top:14px"><div class="ssc-msg" style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(255,255,255,.08);font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">💬 Message</div><div class="ssc-profile" style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(255,255,255,.08);font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">👤 Profile</div></div>'
          +'<div class="ssc-gift" style="margin-top:9px;background:linear-gradient(140deg,#F3CC55,#B0800A);color:#3A2400;font-weight:800;font-size:13.5px;padding:12px;border-radius:13px;cursor:pointer">🎁 Send '+nm+' a Gift</div>'
          +(isStaffView?'<div style="display:flex;gap:8px;margin-top:9px"><div class="ssc-mute" style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(228,54,43,.16);border:1px solid rgba(228,54,43,.35);color:#FF9F98;font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">🔇 Mute</div>'+(isStaffView&&!isYou?'<div class="ssc-kick" style="flex:1;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(228,54,43,.16);border:1px solid rgba(228,54,43,.35);color:#FF9F98;font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">🚪 Remove</div>':'')+'</div>'+(isHostView&&!isYou?'<div class="ssc-mgr" style="margin-top:8px;display:flex;align-items:center;justify-content:center;gap:6px;background:rgba(255,214,120,.16);border:1px solid rgba(255,214,120,.38);color:#FFE27A;font-weight:800;font-size:12.5px;padding:11px;border-radius:12px;cursor:pointer">'+(isCo?'Remove Manager':'Make Manager')+'</div>':'') :''))
      +'</div></div>';
    phone.appendChild(wrap);
    var _sca=wrap.querySelector('.ssc-av'); if(_sca&&bg&&bg!=='none') _sca.style.backgroundImage=bg;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.ssc-close')){wrap.remove();return;} if(e.target.closest('.ssc-gift')){wrap.remove(); openGiftSheet(); return;} if(e.target.closest('.ssc-msg')){wrap.remove(); goTo('chatthread'); return;} if(e.target.closest('.ssc-profile')){wrap.remove(); goTo('userprofile'); return;}
      if(e.target.closest('.ssc-mute')){ var mi=seat.querySelector('.micind'); var md=true; if(mi){md=mi.classList.toggle('muted'); mi.textContent=md?'🔇':'🎤';} wrap.remove(); sflToast((md?'🔇 Muted ':'🎤 Unmuted ')+nm); return; }
      if(e.target.closest('.ssc-kick')){ wrap.remove(); kickFromSeat(seat, nm); return; }
      if(e.target.closest('.ssc-mgr')){ wrap.remove(); if(typeof chToggle==='function') chToggle(nm); return; } });
    return true;
  }
  var _FLYCSS=false;
  function ensureFlyCss(){ if(_FLYCSS)return; _FLYCSS=true; var st=document.createElement('style'); st.textContent=
    '@keyframes sflflyup{0%{transform:translateY(0) scale(.5);opacity:0}12%{opacity:1;transform:translateY(-16px) scale(1)}75%{opacity:1}100%{transform:translateY(-340px) scale(1.15);opacity:0}}'
    +'.sflfly{position:absolute;bottom:96px;z-index:735;pointer-events:none;animation:sflflyup 1.9s cubic-bezier(.25,.7,.4,1) forwards;filter:drop-shadow(0 4px 10px rgba(0,0,0,.5))}'
    /* ===== Premium animated-gift overlay (Bigo/Niki style) ===== */
    +'.sflfx{position:absolute;inset:0;z-index:720;pointer-events:none;overflow:hidden;font-family:Manrope,-apple-system,sans-serif}'
    +'.sflfx.out{transition:opacity .34s ease;opacity:0}'
    +'@keyframes sflxflood{0%{opacity:0}100%{opacity:.32}}'
    +'.sflfx-flood{position:absolute;inset:0;background:radial-gradient(60% 46% at 50% 34%,var(--c2),var(--c0) 44%,transparent 74%);opacity:0;animation:sflxflood .5s ease forwards}'
    +'.sflfx.full .sflfx-flood{animation:sflxflood .5s ease forwards, sflxpulse 1.8s ease-in-out .5s infinite}'
    +'@keyframes sflxpulse{0%,100%{opacity:.34}50%{opacity:.5}}'
    +'.sflfx-stage{position:absolute;inset:0}'
    /* cinematic layers: god-ray beams, impact flash, title reveal, vignette, letterbox, camera shake */
    +'@keyframes sflxrot{to{transform:rotate(360deg)}}'
    +'@keyframes sflxbeamin{to{opacity:.5}}'
    +'.sflfx-beams{position:absolute;left:50%;top:33%;width:560px;height:560px;margin:-280px 0 0 -280px;background:conic-gradient(from 0deg,rgba(255,255,255,.16) 0 9deg,transparent 9deg 30deg);opacity:0;mix-blend-mode:screen;animation:sflxrot 10s linear infinite, sflxbeamin .6s ease .1s forwards}'
    +'@keyframes sflxflash{0%{opacity:0}16%{opacity:.92}100%{opacity:0}}'
    +'.sflfx-flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 33%,rgba(255,255,255,.95),var(--c2) 34%,transparent 68%);opacity:0;animation:sflxflash .7s ease-out .16s forwards}'
    +'@keyframes sflxtitle{0%{opacity:0;transform:translateY(14px) scale(.86);filter:blur(6px)}16%{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}82%{opacity:1}100%{opacity:0}}'
    +'.sflfx-title{position:absolute;left:0;right:0;top:55%;text-align:center;z-index:3;font-weight:800;font-size:25px;letter-spacing:3px;text-transform:uppercase;color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.7),0 0 30px var(--c0);opacity:0;animation:sflxtitle 2.6s ease .28s forwards}'
    +'.sflfx.full .sflfx-title{font-size:32px}'
    +'.sflfx.rm .sflfx-title{animation:none;opacity:1;transform:none;filter:none}'
    +'@keyframes sflxvig{to{opacity:.85}}'
    +'.sflfx-vig{position:absolute;inset:0;box-shadow:inset 0 0 160px 44px rgba(0,0,0,.72);opacity:0;animation:sflxvig .5s ease forwards}'
    +'@keyframes sflxlb{to{transform:scaleY(1)}}'
    +'.sflfx-lb{position:absolute;left:0;right:0;height:9%;background:#000;z-index:4;transform:scaleY(0);animation:sflxlb .5s cubic-bezier(.2,.8,.2,1) forwards}'
    +'.sflfx-lb.top{top:0;transform-origin:top}'
    +'.sflfx-lb.bot{bottom:0;transform-origin:bottom}'
    +'@keyframes sflxshake{0%,100%{transform:translate(0,0)}20%{transform:translate(-3px,2px)}40%{transform:translate(3px,-2px)}60%{transform:translate(-2px,-2px)}80%{transform:translate(2px,2px)}}'
    +'.phone.sflshake{animation:sflxshake .42s ease-in-out .16s}'
    +'@keyframes sflxin{0%{transform:translate(-50%,60px) scale(.2) rotate(-16deg);opacity:0}60%{opacity:1}80%{transform:translate(-50%,-56%) scale(1.12) rotate(4deg)}100%{transform:translate(-50%,-50%) scale(1) rotate(0)}}'
    +'@keyframes sflxbob{0%,100%{translate:0 0}50%{translate:0 -9px}}'
    +'.sflfx-hero{position:absolute;left:50%;top:33%;transform:translate(-50%,-50%);will-change:transform;animation:sflxin .6s cubic-bezier(.2,.9,.3,1.3) both, sflxbob 2.4s ease-in-out .6s infinite}'
    +'.sflfx.rm .sflfx-hero{animation:none}'
    +'.sflfx-disc{position:relative;width:150px;height:150px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 34% 27%,var(--c2),var(--c0) 47%,var(--c1) 100%);box-shadow:0 18px 44px rgba(0,0,0,.5),0 0 60px var(--c0),inset 0 6px 14px rgba(255,255,255,.55),inset 0 -14px 26px rgba(0,0,0,.32);border:2px solid rgba(255,255,255,.42)}'
    +'.sflfx.full .sflfx-disc{width:184px;height:184px}'
    +'@keyframes sflxglyph{0%,100%{transform:rotate(-4deg) scale(1)}50%{transform:rotate(4deg) scale(1.05)}}'
    +'.sflfx-glyph{font-size:78px;line-height:1;filter:drop-shadow(0 6px 14px rgba(0,0,0,.45));animation:sflxglyph 2.6s ease-in-out infinite}'
    +'.sflfx.full .sflfx-glyph{font-size:98px}'
    +'.sflfx.rm .sflfx-glyph{animation:none}'
    +'.sflfx-shine{position:absolute;inset:0;border-radius:50%;overflow:hidden}'
    +'@keyframes sflxsweep{0%{left:-70%}55%,100%{left:130%}}'
    +'.sflfx-shine::before{content:"";position:absolute;top:-40%;left:-70%;width:55%;height:180%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.7),transparent);transform:rotate(18deg);animation:sflxsweep 1.9s ease-in-out .4s infinite}'
    +'@keyframes sflxring{0%{transform:scale(.3);opacity:.85}100%{transform:scale(2.9);opacity:0}}'
    +'.sflfx-ring{position:absolute;left:50%;top:33%;width:150px;height:150px;margin:-75px 0 0 -75px;border-radius:50%;border:3px solid var(--c2);box-shadow:0 0 30px var(--c0);opacity:0;animation:sflxring 1s ease-out .1s forwards}'
    +'.sflfx-ring.r2{border-color:var(--c0);animation-delay:.34s}'
    +'.sflfx-combo{margin-top:14px;text-align:center;font-size:28px;font-weight:800;color:var(--c2);text-shadow:0 2px 10px var(--c1),0 0 22px var(--c0);font-variant-numeric:tabular-nums}'
    +'.sflfx-combo b{font-size:46px;vertical-align:-4px}'
    +'@keyframes sflxband{0%{transform:translateX(-24px);opacity:0}100%{transform:translateX(0);opacity:1}}'
    +'.sflfx-band{position:absolute;left:14px;bottom:150px;z-index:742;display:flex;align-items:center;gap:11px;max-width:80%;padding:9px 16px 9px 9px;border-radius:16px;background:linear-gradient(120deg,rgba(22,17,32,.94),rgba(13,10,18,.94));border:1.5px solid var(--c0);box-shadow:0 14px 34px rgba(0,0,0,.55),0 0 22px var(--c0);animation:sflxband .4s ease both}'
    +'.sflfx-bemo{font-size:26px;width:46px;height:46px;flex:none;border-radius:13px;display:flex;align-items:center;justify-content:center;background:radial-gradient(circle at 40% 30%,var(--c1),var(--c0));box-shadow:inset 0 1px 0 rgba(255,255,255,.35),0 4px 10px rgba(0,0,0,.4);filter:drop-shadow(0 2px 4px rgba(0,0,0,.4))}'
    +'.sflfx-btag{font-size:8.5px;font-weight:800;letter-spacing:.7px;text-transform:uppercase;color:var(--c2)}'
    +'.sflfx-bn{font-size:12px;font-weight:700;color:#C9D0DC;margin-top:1px}'
    +'.sflfx-bn b{color:#fff;font-weight:800}'
    +'.sflfx-bc{margin-top:3px;font-size:11px;font-weight:800;color:#FFE1A0;display:flex;align-items:center;gap:5px}'
    +'.sflfx-bnm{color:#fff}'
    +'.sflfx-bc .sflfx-coin{width:13px;height:13px;border-radius:50%;background:radial-gradient(circle at 35% 28%,#FFE7A8,#C88A00);margin-left:2px}'
    +'.sflfx-coin{width:12px;height:12px;border-radius:50%;background:radial-gradient(circle at 35% 28%,#FFE7A8,#C88A00)}'
    +'.cm.giftmsg{background:linear-gradient(90deg,rgba(255,179,0,.18),transparent);border-left:2px solid rgba(255,200,90,.7);padding-left:6px;border-radius:4px}'
    +'.cm.joinmsg{color:#8FE5FF}'
    +'.cm.askmsg{background:linear-gradient(90deg,rgba(201,255,61,.16),transparent);border-left:2px solid rgba(201,255,61,.7);padding-left:6px;border-radius:4px}'
    +'.qa-ce:empty:before{content:attr(data-ph);color:rgba(255,255,255,.4);pointer-events:none}'
    ; document.head.appendChild(st); }
  var _GMCSS=false;
  /* Per-gift signature motion CSS — each gift key (m-<motion>) drives its own hero path,
     glyph behaviour and accessory props so every gift animates uniquely on send. */
  function ensureGiftMotionCss(){ if(_GMCSS)return; _GMCSS=true; var st=document.createElement('style'); st.textContent=
    /* ROSE — bloom */
    '@keyframes gm-bloom{0%{transform:scale(0) rotate(-120deg)}55%{transform:scale(1.2) rotate(12deg)}100%{transform:scale(1) rotate(0)}}'
    +'.sflfx.m-bloom .sflfx-glyph{animation:gm-bloom 1s cubic-bezier(.2,.9,.3,1.3) both, sflxglyph 2.6s ease-in-out 1s infinite}'
    /* FOOTBALL — arc kick + spin */
    +'@keyframes gm-arc{0%{transform:translate(-260%,120px) scale(.4);opacity:0}22%{opacity:1}55%{transform:translate(-50%,-60%) scale(1.12)}72%{transform:translate(-50%,-44%)}86%{transform:translate(-50%,-52%)}100%{transform:translate(-50%,-50%) scale(1)}}'
    +'@keyframes gm-spin{from{transform:rotate(0)}to{transform:rotate(720deg)}}'
    +'.sflfx.m-kick .sflfx-hero{animation:gm-arc 1s cubic-bezier(.2,.8,.3,1) both, sflxbob 2.6s ease-in-out 1s infinite}'
    +'.sflfx.m-kick .sflfx-glyph{animation:gm-spin 1.1s cubic-bezier(.1,.7,.2,1) both}'
    /* CHANT — shout + sound waves + notes */
    +'@keyframes gm-shout{0%,100%{transform:rotate(-18deg) scale(1)}50%{transform:rotate(-4deg) scale(1.14)}}'
    +'.sflfx.m-chant .sflfx-glyph{animation:gm-shout .5s ease-in-out infinite}'
    +'@keyframes gm-wave{0%{transform:scale(.4);opacity:.7}100%{transform:scale(2.5);opacity:0}}'
    +'.sflm-wave{position:absolute;left:50%;top:33%;width:120px;height:120px;margin:-60px 0 0 -60px;border-radius:50%;border:3px solid var(--c2);opacity:0;animation:gm-wave 1.1s ease-out infinite}'
    +'.sflm-wave.w2{animation-delay:.36s}.sflm-wave.w3{animation-delay:.72s}'
    +'@keyframes gm-note{0%{transform:translateY(0) scale(.6);opacity:0}20%{opacity:1}100%{transform:translateY(-130px) scale(1.1);opacity:0}}'
    +'.sflm-notes{position:absolute;left:50%;top:30%}'
    +'.sflm-notes i{position:absolute;font-size:22px;font-style:normal;color:var(--c2);text-shadow:0 2px 8px rgba(0,0,0,.5);animation:gm-note 1.8s ease-in infinite}'
    +'.sflm-notes i:nth-child(1){left:-64px;animation-delay:0s}.sflm-notes i:nth-child(2){left:-20px;animation-delay:.45s}.sflm-notes i:nth-child(3){left:24px;animation-delay:.9s}.sflm-notes i:nth-child(4){left:60px;animation-delay:1.3s}'
    /* SCARF — wave */
    +'@keyframes gm-scarf{0%,100%{transform:skewX(-16deg) rotate(-6deg)}50%{transform:skewX(16deg) rotate(6deg)}}'
    +'.sflfx.m-wave .sflfx-glyph{animation:gm-scarf 1s ease-in-out infinite}'
    /* GOAL CELEBRATION — flare */
    +'@keyframes gm-flare{0%,100%{transform:scale(1) rotate(-3deg)}30%{transform:scale(1.24) rotate(3deg)}60%{transform:scale(.94)}}'
    +'.sflfx.m-flare .sflfx-glyph{animation:gm-flare .6s ease-in-out infinite}'
    /* FIREWORKS — multi-burst */
    +'@keyframes gm-fw{0%{transform:scale(.3);opacity:1;box-shadow:0 0 0 0 var(--c2)}70%{opacity:.9}100%{transform:scale(1);opacity:0;box-shadow:0 0 2px 42px transparent}}'
    +'.sflm-fw{position:absolute;width:10px;height:10px;border-radius:50%;background:radial-gradient(circle,#fff,var(--c0));opacity:0;animation:gm-fw 1.4s ease-out infinite}'
    +'.sflm-fw.a{left:24%;top:24%}.sflm-fw.b{left:74%;top:30%;animation-delay:.4s}.sflm-fw.c{left:34%;top:60%;animation-delay:.8s}.sflm-fw.d{left:66%;top:56%;animation-delay:1.1s}'
    /* LUCKY CLOVER — spin */
    +'.sflfx.m-spinlucky .sflfx-glyph{animation:gm-spin 2.4s linear infinite}'
    /* DICE ROLL — tumble in + twin die */
    +'@keyframes gm-roll{0%{transform:translate(-280%,30px) rotate(0) scale(.7);opacity:0}12%{opacity:1}60%{transform:translate(-50%,-50%) rotate(900deg) scale(1)}72%{transform:translate(-50%,-40%) rotate(900deg)}84%{transform:translate(-50%,-52%) rotate(900deg)}100%{transform:translate(-50%,-50%) rotate(900deg) scale(1)}}'
    +'.sflfx.m-roll .sflfx-hero{animation:gm-roll 1.2s cubic-bezier(.2,.7,.3,1) both, sflxbob 2.6s ease-in-out 1.2s infinite}'
    +'@keyframes gm-roll2{0%{transform:translate(-360%,60px) rotate(0) scale(.6);opacity:0}12%{opacity:1}60%{transform:translate(-118%,-40%) rotate(-720deg) scale(.9)}100%{transform:translate(-118%,-40%) rotate(-720deg) scale(.9);opacity:.92}}'
    +'.sflm-die2{position:absolute;left:50%;top:33%;font-size:52px;filter:drop-shadow(0 6px 12px rgba(0,0,0,.5));animation:gm-roll2 1.2s cubic-bezier(.2,.7,.3,1) both}'
    /* FORTUNE WHEEL — spin-to-stop + pointer */
    +'@keyframes gm-wheel{0%{transform:rotate(0)}80%{transform:rotate(1440deg)}100%{transform:rotate(1530deg)}}'
    +'.sflfx.m-spinwheel .sflfx-glyph{animation:gm-wheel 2.2s cubic-bezier(.15,.85,.2,1) both}'
    +'@keyframes gm-tick{0%,100%{transform:rotate(0)}50%{transform:rotate(-18deg)}}'
    +'.sflm-pointer{position:absolute;left:50%;top:33%;margin:-96px 0 0 -9px;width:0;height:0;border-left:9px solid transparent;border-right:9px solid transparent;border-top:16px solid var(--c2);transform-origin:50% 0;filter:drop-shadow(0 2px 4px rgba(0,0,0,.5));animation:gm-tick .13s ease-in-out 7}'
    /* LUCKY ENVELOPE — shake open */
    +'@keyframes gm-open{0%,8%{transform:rotate(0)}2%{transform:rotate(-10deg)}4%{transform:rotate(10deg)}6%{transform:rotate(-8deg)}30%{transform:scale(1.25)}45%{transform:scale(.96)}100%{transform:scale(1)}}'
    +'.sflfx.m-open .sflfx-glyph{animation:gm-open 1.1s ease both, sflxglyph 2.6s ease-in-out 1.1s infinite}'
    /* LUCKY 777 — slot reels */
    +'@keyframes gm-reel{0%{transform:translateY(-42px) scaleY(.4);opacity:0;filter:blur(3px)}60%{opacity:1}100%{transform:translateY(0) scaleY(1);opacity:1;filter:blur(0)}}'
    +'.sflm-slot{position:absolute;left:50%;top:33%;transform:translate(-50%,-50%);display:flex;gap:6px;z-index:3}'
    +'.sflm-slot span{width:34px;height:46px;border-radius:8px;background:linear-gradient(#fff,#e9edf5);color:#c92a2a;font-weight:800;font-size:30px;display:flex;align-items:center;justify-content:center;box-shadow:inset 0 2px 4px rgba(0,0,0,.2),0 6px 14px rgba(0,0,0,.4);animation:gm-reel 1.1s cubic-bezier(.2,.8,.2,1) both}'
    +'.sflm-slot span:nth-child(2){animation-delay:.18s}.sflm-slot span:nth-child(3){animation-delay:.36s}'
    /* JACKPOT — pop + coin rain */
    +'@keyframes gm-pop{0%{transform:translate(-50%,40px) scale(.2);opacity:0}55%{opacity:1;transform:translate(-50%,-56%) scale(1.2)}100%{transform:translate(-50%,-50%) scale(1)}}'
    +'.sflfx.m-coinrain .sflfx-hero{animation:gm-pop 1s cubic-bezier(.2,.9,.3,1.3) both, sflxbob 2.6s ease-in-out 1s infinite}'
    /* HOME SHIRT / CLUB KIT — unfurl flip */
    +'@keyframes gm-unfurl{0%{transform:perspective(400px) rotateX(-95deg);opacity:0}50%{opacity:1}70%{transform:perspective(400px) rotateX(16deg)}100%{transform:perspective(400px) rotateX(0)}}'
    +'.sflfx.m-unfurl .sflfx-glyph{transform-origin:top;animation:gm-unfurl 1s ease both, sflxglyph 2.6s ease-in-out 1s infinite}'
    /* KEEPER GLOVES — dive save */
    +'@keyframes gm-save{0%{transform:translate(80%,-30%) rotate(40deg) scale(.6);opacity:0}30%{opacity:1}62%{transform:translate(-50%,-54%) rotate(-12deg) scale(1.12)}100%{transform:translate(-50%,-50%) rotate(0) scale(1)}}'
    +'.sflfx.m-save .sflfx-hero{animation:gm-save 1s cubic-bezier(.2,.8,.3,1) both, sflxbob 2.6s ease-in-out 1s infinite}'
    /* BOOTS / GOLDEN BOOT — strike swing */
    +'@keyframes gm-strike{0%{transform:rotate(-70deg) scale(.8)}45%{transform:rotate(24deg) scale(1.12)}62%{transform:rotate(-8deg)}100%{transform:rotate(0) scale(1)}}'
    +'.sflfx.m-strike .sflfx-glyph{transform-origin:70% 80%;animation:gm-strike 1s cubic-bezier(.2,.8,.2,1) both, sflxglyph 2.6s ease-in-out 1s infinite}'
    /* CAPTAIN ARMBAND — proud rise */
    +'@keyframes gm-rise{0%{transform:translate(-50%,30px) scale(.6);opacity:0}60%{opacity:1;transform:translate(-50%,-56%) scale(1.1)}100%{transform:translate(-50%,-50%) scale(1)}}'
    +'.sflfx.m-salute .sflfx-hero{animation:gm-rise 1s cubic-bezier(.2,.9,.3,1.2) both, sflxbob 2.6s ease-in-out 1s infinite}'
    /* TROPHY / CHAMPIONS CUP — raise aloft */
    +'@keyframes gm-raise{0%{transform:translate(-50%,50px) scale(.4);opacity:0}55%{opacity:1;transform:translate(-50%,-60%) scale(1.18)}100%{transform:translate(-50%,-54%) scale(1)}}'
    +'@keyframes gm-raisebob{0%,100%{translate:0 0}50%{translate:0 -6px}}'
    +'.sflfx.m-raise .sflfx-hero{animation:gm-raise 1.1s cubic-bezier(.2,.9,.3,1.2) both, gm-raisebob 2.4s ease-in-out 1.1s infinite}'
    /* BOUNCY BALL — bounce */
    +'@keyframes gm-bounce{0%{transform:translate(-50%,-160%) scale(.6);opacity:0}15%{opacity:1}35%{transform:translate(-50%,-50%)}50%{transform:translate(-50%,-78%)}65%{transform:translate(-50%,-50%)}78%{transform:translate(-50%,-64%)}100%{transform:translate(-50%,-52%)}}'
    +'.sflfx.m-bounce .sflfx-hero{animation:gm-bounce 1.3s cubic-bezier(.3,.7,.4,1) both, sflxbob 2.4s ease-in-out 1.3s infinite}'
    +'.sflfx.m-bounce .sflfx-glyph{animation:gm-spin 1.3s ease-out both}'
    /* ROCKET — launch + flame */
    +'@keyframes gm-launch{0%{transform:translate(-50%,80px) scale(.4) rotate(-8deg);opacity:0}18%{opacity:1;transform:translate(-50%,-50%) scale(1) rotate(-4deg)}40%{transform:translate(-50%,-50%) scale(1) rotate(-4deg)}100%{transform:translate(-50%,-380px) scale(.7) rotate(-6deg);opacity:0}}'
    +'.sflfx.m-launch .sflfx-hero{animation:gm-launch 1.9s cubic-bezier(.4,.2,.7,1) both}'
    +'@keyframes gm-flame{0%{opacity:0;transform:scaleY(.2)}20%{opacity:1}40%{opacity:1;transform:translateY(0) scaleY(1)}100%{opacity:0;transform:translateY(-330px) scaleY(1.5)}}'
    +'.sflm-flame{position:absolute;left:50%;top:33%;margin:44px 0 0 -14px;width:28px;height:60px;border-radius:0 0 50% 50%/0 0 70% 70%;background:linear-gradient(#ffec99,#ff922b 60%,#e8590c);filter:blur(2px);transform-origin:top;opacity:0;animation:gm-flame 1.9s ease both}'
    /* BOOM — drop + explode */
    +'@keyframes gm-drop{0%{transform:translate(-50%,-170%) scale(.7) rotate(0);opacity:0}30%{opacity:1;transform:translate(-50%,-50%) rotate(6deg)}52%{transform:translate(-50%,-50%) rotate(-6deg)}64%{transform:translate(-50%,-50%) scale(1.3)}70%{transform:translate(-50%,-50%) scale(0);opacity:0}100%{opacity:0}}'
    +'.sflfx.m-explode .sflfx-hero{animation:gm-drop 1.1s ease both}'
    +'@keyframes gm-explode{0%{transform:scale(.3);opacity:1}100%{transform:scale(9);opacity:0}}'
    +'.sflm-boom{position:absolute;left:50%;top:33%;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;background:radial-gradient(circle,#fff,#ffec99 30%,#ff922b 55%,transparent 72%);opacity:0;animation:gm-explode .7s ease-out .62s forwards}'
    /* RACE CAR — drive across + speed lines */
    +'@keyframes gm-drive{0%{transform:translate(-320%,-50%) scale(.7);opacity:0}18%{opacity:1}42%{transform:translate(-50%,-50%) scale(1)}64%{transform:translate(-50%,-50%) scale(1)}100%{transform:translate(300%,-50%) scale(.8);opacity:0}}'
    +'.sflfx.m-drive .sflfx-hero{animation:gm-drive 2s cubic-bezier(.3,.6,.5,1) both}'
    +'@keyframes gm-speed{0%,20%{opacity:0;transform:translateX(-160px)}40%{opacity:.9}100%{opacity:0;transform:translateX(440px)}}'
    +'.sflm-speed{position:absolute;left:50%;top:33%;margin-left:-60px;height:4px;width:120px;border-radius:2px;background:linear-gradient(90deg,transparent,var(--c2));opacity:0;animation:gm-speed 2s linear both}'
    +'.sflm-speed.s2{top:36%;animation-delay:.15s}.sflm-speed.s3{top:30%;animation-delay:.3s}'
    /* DRAGON — fly-across arc + ember trail */
    +'@keyframes gm-fly{0%{transform:translate(-320%,10%) rotate(-10deg) scale(.5);opacity:0}25%{opacity:1}55%{transform:translate(-50%,-58%) rotate(6deg) scale(1.12)}100%{transform:translate(-50%,-50%) rotate(0) scale(1)}}'
    +'.sflfx.m-dragonfly .sflfx-hero{animation:gm-fly 1.6s cubic-bezier(.2,.7,.4,1) both, sflxbob 2.6s ease-in-out 1.6s infinite}'
    +'@keyframes gm-trail{0%{opacity:0;transform:translateX(-190px) scale(.4)}30%{opacity:.8}100%{opacity:0;transform:translate(0) scale(1.5)}}'
    +'.sflm-trail{position:absolute;left:50%;top:40%;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;background:radial-gradient(circle,rgba(255,150,60,.7),transparent 70%);opacity:0;animation:gm-trail 1.6s ease both}'
    /* LEGEND CROWN — descend from above */
    +'@keyframes gm-descend{0%{transform:translate(-50%,-240%) scale(.7) rotate(-8deg);opacity:0}35%{opacity:1}72%{transform:translate(-50%,-46%) scale(1.12) rotate(4deg)}100%{transform:translate(-50%,-50%) scale(1) rotate(0)}}'
    +'.sflfx.m-descend .sflfx-hero{animation:gm-descend 1.2s cubic-bezier(.2,.8,.3,1.1) both, sflxbob 2.6s ease-in-out 1.2s infinite}'
    /* GOAT — legendary zoom */
    +'@keyframes gm-legend{0%{transform:translate(-50%,-50%) scale(0) rotate(-24deg);opacity:0}45%{opacity:1;transform:translate(-50%,-50%) scale(1.35) rotate(10deg)}72%{transform:translate(-50%,-50%) scale(.94)}100%{transform:translate(-50%,-50%) scale(1.06)}}'
    +'.sflfx.m-legend .sflfx-hero{animation:gm-legend 1.2s cubic-bezier(.2,.9,.3,1.3) both, sflxbob 2.6s ease-in-out 1.2s infinite}'
    ; document.head.appendChild(st); }
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
    var rows=clubs.map(function(c){return '<div class="ds-club" data-cn="'+c[1]+'" data-cm="'+c[2]+'" data-cr="'+c[0]+'" data-cc="'+c[3]+'"><div style="width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:800;color:#fff;font-size:18px;background:'+(c[3]==='blue'?'linear-gradient(150deg,#2F7FD1,#1E5E9E)':c[3]==='green'?'linear-gradient(150deg,#0FB753,#0a8f40)':'linear-gradient(150deg,#E4362B,#B4241B)')+'">'+c[0]+'</div><div style="flex:1"><div class="ds-name">'+c[1]+'</div><div class="ds-meta">'+c[2]+'</div></div></div>';}).join('');
    var wrap=document.createElement('div'); wrap.className='sfldestwrap sflsheetwrap';
    wrap.innerHTML='<div class="sflsheet-panel"><div class="sflsheet-grab"></div><div class="sflsheet-title">Choose destination club</div><div class="sflsheet-sub">Only clubs accepting moves are shown</div>'+rows+'<div class="ds-cancel sflsheet-cancel">Cancel</div></div>';
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
    var opts=m[1].map(function(o){var on=(o.indexOf(cur)>=0||cur.indexOf(o)>=0); return '<div class="tm-opt'+(on?' on':'')+'" data-v="'+o+'">'+o+(on?'<span style="color:#2F7FD1;font-weight:800">✓</span>':'')+'</div>';}).join('');
    var wrap=document.createElement('div'); wrap.className='sfltermwrap sflsheetwrap';
    wrap.innerHTML='<div class="sflsheet-panel"><div class="sflsheet-grab"></div><div class="sflsheet-title">'+m[0]+'</div><div class="sflsheet-sub">Set the term for this offer</div>'+opts+'<div class="tm-cancel sflsheet-cancel">Cancel</div></div>';
    phone.appendChild(wrap);
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.tm-cancel')){wrap.remove();return;} var op=e.target.closest('.tm-opt'); if(op){var v=op.getAttribute('data-v'); var vel=row.querySelector('.v'); if(vel)vel.textContent=v; wrap.remove(); sflToast('Updated · '+v);} });
  }
  function setEditPhoto(url){ var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return; var av=phone.querySelector('.epavatar'); if(av){ av.style.backgroundImage=url||'none'; av.style.backgroundColor=url?'':'#DCE2EC'; } }
  function showPhotoSheet(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflphotowrap'))return;
    var wrap=document.createElement('div'); wrap.className='sflphotowrap sflsheetwrap';
    wrap.innerHTML='<div class="sflsheet-panel"><div class="sflsheet-grab"></div><div class="sflsheet-title">Change display picture</div>'
      +'<div class="pp-cam">📷 Take a photo</div>'
      +'<div class="pp-gal">🖼️ Choose from gallery</div>'
      +'<div class="pp-rm sflsheet-row" style="color:var(--coral,#E4362B);border-bottom:none">🗑️ Remove current photo</div>'
      +'<div class="pp-cancel sflsheet-cancel">Cancel</div></div>';
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
  function sflSheet(title, inner){ var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone||phone.querySelector('.sflsheetwrap'))return null; var wrap=document.createElement('div'); wrap.className='sflsheetwrap'; wrap.innerHTML='<div class="sflsheet-panel"><div class="sflsheet-grab"></div><div class="sflsheet-title">'+title+'</div>'+inner+'</div>'; phone.appendChild(wrap); return wrap; }
  function showLanguageSheet(){
    var langs=['English','Español','Français','Deutsch','العربية','हिन्दी','Português']; var rows='';
    for(var i=0;i<langs.length;i++){rows+='<div class="lang-opt" data-l="'+langs[i]+'">'+langs[i]+(i===0?'<span style="margin-left:auto;color:#0FA04C">✓</span>':'')+'</div>';}
    var wrap=sflSheet('Language', rows+'<div class="sh-cancel sflsheet-cancel">Cancel</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} var lo=e.target.closest('.lang-opt'); if(lo){var l=lo.getAttribute('data-l'); var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); [].forEach.call(phone.querySelectorAll('.listrow'),function(r){if(/language/i.test(r.textContent)){var a=r.querySelector('.arr'); if(a)a.textContent=l+' ›';}}); wrap.remove(); sflToast('Language set to '+l); return;} });
  }
  var SFLtaken={ada:1,reds:1,jay:1,priya:1,marco:1,lena:1,diego:1,mikael:1,goal:1,fury:1,captain:1,king:1,legend:1,nadia:1,omar:1};
  function nameTaken(v){ return !!SFLtaken[(v||'').trim().toLowerCase()]; }
  function nameSuggest(v){ var b=((v||'').trim().replace(/[0-9]+$/,''))||'Fan'; var opts=[b+'02',b+'123',b+'2026',b+'_SFL']; for(var i=0;i<opts.length;i++){ if(!nameTaken(opts[i])) return opts[i]; } return b+Math.floor(Math.random()*900+100); }
  function showNameErr(field){ if(!field) return false; var v=(field.textContent||'').trim(); var err=field.nextElementSibling; if(!err||!err.classList||!err.classList.contains('dnerr')){ err=document.createElement('div'); err.className='dnerr'; err.style.cssText='margin-top:8px;font-size:12px;font-weight:750;line-height:1.5'; field.insertAdjacentElement('afterend',err); }
    if(v && nameTaken(v)){ var sug=nameSuggest(v); field.style.borderColor='#E4362B'; err.style.display='block'; err.innerHTML='<span style="color:#E4362B">⚠ This display name is already taken. Please choose another one.</span><br><span class="dnsug" data-s="'+sug+'" style="display:inline-block;margin-top:7px;background:#EEF6FF;color:#2266C9;border:1px solid #CFE3FA;border-radius:999px;padding:4px 12px;font-weight:800;cursor:pointer">Try “'+sug+'” ›</span>'; return true; }
    field.style.borderColor=''; err.style.display='none'; err.innerHTML=''; return false; }
  function applyMgrGate(root){
    var bal=root.querySelector('.mg-bal'), badge=root.querySelector('.mg-badge'), prog=root.querySelector('.mg-prog i'), togo=root.querySelector('.mg-togo'), buy=root.querySelector('.ccbuy'), go=root.querySelector('.ccgo');
    if(SFLmgrEligible){
      if(bal)bal.innerHTML='5,000 <span style="font-size:12px;font-weight:700;color:var(--t3)">/ 5,000 Coins</span>';
      if(badge){badge.textContent='Unlocked ✓'; badge.style.color='#0A8F40'; badge.style.background='#EAF9F0'; badge.style.borderColor='#BFE9CE';}
      if(prog)prog.style.width='100%';
      if(togo)togo.textContent='You meet the 5,000-Coin requirement — create your club.';
      if(buy)buy.style.display='none';
      if(go){go.innerHTML='Continue · Pick your club ›'; go.className='btn ccgo'; go.style.opacity='1'; go.style.marginTop='0';}
    } else {
      if(buy)buy.style.display='';
      if(go){go.innerHTML='🔒 Reach 5,000 Coins to continue'; go.className='btn dark ccgo'; go.style.opacity='.5'; go.style.marginTop='9px';}
    }
  }
  function showClubOptsSheet(){
    if(!SFLmember){ sflToast('You are not in a club'); return; }
    var leaveDis=SFLleaveAsk==='pending';
    var mgrLocked=!!(SFLmgrMode||SFLcmgrAsk==='accepted'||SFLcmgrInvite==='accepted');
    var mgrPend=SFLcmgrAsk==='pending';
    var leaveRow=leaveDis
      ? '<div class="sflclubopt dis" data-co="leave-pend"><div class="coi">⏳</div><div><div class="cot">Leave request pending</div><div class="cos">Tap to view status · waiting on manager</div></div></div>'
      : '<div class="sflclubopt leave" data-co="leave"><div class="coi danger">🚪</div><div><div class="cot">Leave this club</div><div class="cos">Review consequences · manager approves</div></div></div>';
    var mgrRow;
    if(mgrLocked){
      mgrRow='<div class="sflclubopt dis" data-co="mgr-yes"><div class="coi">🛡️</div><div><div class="cot">You are a manager</div><div class="cos">Manager HQ is on your profile</div></div></div>';
    } else if(mgrPend){
      mgrRow='<div class="sflclubopt mgr pend" data-co="mgr-pend"><div class="coi">🕐</div><div><div class="cot">Manager request pending</div><div class="cos">Tap to view · waiting for Jay Malik</div></div></div>';
    } else {
      mgrRow='<div class="sflclubopt mgr" data-co="mgr"><div class="coi gold">🛡️</div><div><div class="cot">Request to become manager</div><div class="cos">Ask the current manager · you accept nothing yet</div></div></div>';
    }
    var inner='<div class="sflclubopt-sub">Red District FC · member options</div>'+mgrRow+leaveRow+'<div class="sh-cancel sflsheet-cancel">Cancel</div>';
    var wrap=sflSheet('Club options', inner); if(!wrap)return;
    wrap.addEventListener('click',function(e){
      e.stopPropagation();
      if(e.target===wrap||e.target.closest('.sh-cancel')){ wrap.remove(); return; }
      var row=e.target.closest('.sflclubopt'); if(!row)return;
      var co=row.getAttribute('data-co')||'';
      if(co==='leave'){ wrap.remove(); goTo('clubleave'); return; }
      if(co==='leave-pend'){ wrap.remove(); goTo('leavepending'); return; }
      if(co==='mgr'){ wrap.remove(); goTo('cmgrask'); return; }
      if(co==='mgr-pend'){ wrap.remove(); goTo('cmgrsent'); return; }
      if(co==='mgr-yes'){ sflToast('You are already a manager'); return; }
    });
  }
  function showWithdrawSheet(){
    var wrap=sflSheet('Withdraw application?', '<div class="sflsheet-sub">Your application to Red District FC will be removed. You can re-apply anytime.</div><div class="wd-yes sflsheet-danger">Withdraw application</div><div class="sh-cancel sflsheet-cancel">Keep it</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} if(e.target.closest('.wd-yes')){ wrap.remove(); var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); var body=phone&&phone.querySelector('.body'); if(body){ body.innerHTML='<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 24px"><div style="width:80px;height:80px;border-radius:50%;background:#F0F2F7;display:flex;align-items:center;justify-content:center;font-size:34px">📭</div><div style="font-size:20px;font-weight:800;color:#14161C;margin-top:16px">No applications</div><div style="font-size:13px;font-weight:650;color:#707786;margin-top:8px;max-width:250px">You withdrew your application. Discover clubs and apply anytime.</div><div class="wd-discover" style="margin-top:20px;padding:14px 22px;background:#E4362B;color:#fff;border-radius:14px;font-weight:800;cursor:pointer">Discover Clubs</div></div>'; } sflToast('Application withdrawn'); return;} });
  }
  function showLogoutSheet(){
    var wrap=sflSheet('Log out of SFL?', '<div class="sflsheet-sub">You can sign back in anytime. Your account and progress stay safe.</div><div class="lo-yes sflsheet-danger">Log out</div><div class="sh-cancel sflsheet-cancel">Cancel</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} if(e.target.closest('.lo-yes')){wrap.remove(); hist.length=0; goTo('signin'); return;} });
  }
  function showClubChatMenu(){
    var wrap=sflSheet('Red Fury · Club Chat', '<div class="ccm-members sflsheet-row">👥 View members</div><div class="ccm-mute sflsheet-row">🔕 Mute notifications</div><div class="ccm-leave sflsheet-danger">🚪 Leave group chat</div><div class="sh-cancel sflsheet-cancel">Cancel</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap||e.target.closest('.sh-cancel')){wrap.remove();return;} if(e.target.closest('.ccm-members')){wrap.remove(); goTo('clubmembers'); return;} if(e.target.closest('.ccm-mute')){wrap.remove(); sflToast('🔕 Club chat muted'); return;} if(e.target.closest('.ccm-leave')){wrap.remove(); SFLleftClub=true; goTo('inbox'); sflToast('You left Red Fury · Club Chat'); return;} });
  }
  function showShareSheet(){
    var link='sfl.app/join/red-fury-12345';
    var chans=[
      {k:'WhatsApp',e:'💚',c:'#25D366'},{k:'Instagram',e:'📸',c:'linear-gradient(135deg,#F58529,#DD2A7B,#8134AF)'},
      {k:'Facebook',e:'👍',c:'#1877F2'},{k:'Messenger',e:'💬',c:'linear-gradient(135deg,#00B2FF,#006AFF)'},
      {k:'TikTok',e:'🎵',c:'#111'},{k:'X',e:'✖',c:'#111'},
      {k:'Telegram',e:'✈️',c:'#26A5E4'},{k:'Snapchat',e:'👻',c:'#FFC800'},
      {k:'SMS',e:'💬',c:'#34C759'},{k:'Email',e:'✉️',c:'#EA4335'},
      {k:'QR code',e:'🔳',c:'#3A3F4B'},{k:'Copy link',e:'🔗',c:'#707786'}
    ];
    var tiles=chans.map(function(ch){return '<div class="shch" data-k="'+ch.k+'" style="display:flex;flex-direction:column;align-items:center;gap:7px;cursor:pointer"><div style="width:54px;height:54px;border-radius:17px;display:flex;align-items:center;justify-content:center;font-size:25px;box-shadow:var(--shadow-sm);background:'+ch.c+'">'+ch.e+'</div><div class="shch-lbl">'+ch.k+'</div></div>';}).join('');
    var qr='<svg viewBox="0 0 100 100" shape-rendering="crispEdges" style="width:118px;height:118px;display:block"><rect width="100" height="100" fill="#fff"/><g fill="#07090D"><rect x="6" y="6" width="22" height="22"/><rect x="10" y="10" width="14" height="14" fill="#fff"/><rect x="13" y="13" width="8" height="8"/><rect x="72" y="6" width="22" height="22"/><rect x="76" y="10" width="14" height="14" fill="#fff"/><rect x="79" y="13" width="8" height="8"/><rect x="6" y="72" width="22" height="22"/><rect x="10" y="76" width="14" height="14" fill="#fff"/><rect x="13" y="79" width="8" height="8"/><rect x="34" y="8" width="4" height="4"/><rect x="42" y="8" width="4" height="4"/><rect x="34" y="16" width="8" height="4"/><rect x="50" y="12" width="4" height="8"/><rect x="60" y="8" width="4" height="12"/><rect x="34" y="34" width="4" height="4"/><rect x="42" y="38" width="8" height="4"/><rect x="54" y="34" width="4" height="8"/><rect x="64" y="40" width="8" height="4"/><rect x="74" y="34" width="4" height="8"/><rect x="84" y="38" width="6" height="6"/><rect x="8" y="34" width="4" height="8"/><rect x="16" y="42" width="6" height="4"/><rect x="8" y="52" width="8" height="4"/><rect x="20" y="54" width="4" height="8"/><rect x="34" y="52" width="6" height="6"/><rect x="46" y="54" width="4" height="10"/><rect x="56" y="52" width="10" height="4"/><rect x="70" y="56" width="6" height="6"/><rect x="82" y="52" width="8" height="8"/><rect x="34" y="70" width="4" height="8"/><rect x="44" y="72" width="8" height="4"/><rect x="54" y="78" width="4" height="8"/><rect x="66" y="72" width="6" height="6"/><rect x="78" y="70" width="4" height="10"/><rect x="86" y="80" width="6" height="6"/><rect x="40" y="86" width="10" height="4"/><rect x="62" y="86" width="8" height="6"/></g></svg>';
    var inner='<div class="sflsheet-sub">Invite people from your contacts &amp; socials to apply to <b>Red Fury</b>. They always choose to accept — no one is auto-added.</div>'
      +'<div style="text-align:center;margin-bottom:14px"><div class="sflsheet-qrwrap">'+qr+'</div><div style="font-size:10.5px;font-weight:750;color:var(--t2);margin-top:7px">Scan to apply to Red Fury</div></div>'
      +'<div class="sflsheet-linkrow"><span style="flex:1;font-size:12.5px;font-weight:700;color:var(--t1);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+link+'</span><span class="shcopy" style="font-size:12px;font-weight:800;color:var(--red,#E4362B);cursor:pointer">Copy</span></div>'
      +'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:17px 4px">'+tiles+'</div>';
    var wrap=sflSheet('Share club invitation', inner); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap){wrap.remove();return;}
      if(e.target.closest('.shcopy')){ sflToast('🔗 Invite link copied'); return; }
      var ch=e.target.closest('.shch'); if(ch){ var k=ch.getAttribute('data-k'); wrap.remove(); if(/qr/i.test(k)){goTo('mgrshare');return;} if(/copy/i.test(k)){sflToast('🔗 Invite link copied');return;} sflToast('✅ Invitation shared to '+k+' · fans can now apply'); return; } });
  }
  function showEditSheet(title, val, msg){
    var wrap=sflSheet(title, '<div contenteditable="true" class="es-field">'+val+'</div><div class="sflsheet-sub" style="margin-top:8px;margin-bottom:0">'+(msg||'')+'</div><div class="es-save" style="text-align:center;margin-top:14px;padding:13px;background:#C9FF3D;color:#0A1400;border-radius:12px;font-weight:800;cursor:pointer">Save</div>'); if(!wrap)return;
    wrap.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===wrap){wrap.remove();return;} if(e.target.closest('.es-field')){return;} if(e.target.closest('.es-save')){wrap.remove();sflToast(title+' updated · verification sent');return;} });
  }
  function SFLchat(root){
    function sendFrom(e){ var ph=e.getAttribute('data-ph')||''; var txt=(e.textContent||'').trim(); if(!txt||txt===ph)return; var clean=txt.replace(/[<>&]/g,''); var box=root.querySelector('.rchat')||root.querySelector('.msgs')||root.querySelector('.chatwrap')||root.querySelector('.chatprev'); if(box){var isMsg=box.classList.contains('msgs')||box.classList.contains('chatwrap'); var d=document.createElement('div'); d.className=isMsg?'msg out':'cm'; d.innerHTML=isMsg?clean:'<b style="color:#DCFF8A">You</b> '+clean; box.appendChild(d); box.scrollTop=box.scrollHeight;} e.textContent=''; }
    function attachChip(kind){
      var map={photo:['🖼','Photo'],video:['🎬','Video'],doc:['📄','Document'],shot:['📱','Screenshot']};
      var m=map[kind]||['📎','File'];
      var box=root.querySelector('.msgs');
      if(box){
        var wrap=document.createElement('div'); wrap.className='sentwrap';
        wrap.innerHTML='<div class="bubble sent att"><span class="attic">'+m[0]+'</span><span>'+m[1]+' attached</span></div><div class="bmeta"><span>Now</span><span class="tick">✓ Sent</span></div>';
        box.appendChild(wrap); box.scrollTop=box.scrollHeight;
      }
      sflToast(m[1]+' attached');
    }
    root.querySelectorAll('.rsay,.cin,.chatin,.msgin,.rsayb').forEach(function(e){
      if(e.getAttribute('data-chat'))return; if(/speaking on/i.test(e.textContent||''))return;
      e.setAttribute('data-chat','1'); e.setAttribute('contenteditable','true'); e.style.outline='none'; e.style.cursor='text';
      var ph=(e.textContent||'').trim(); e.setAttribute('data-ph',ph);
      e.addEventListener('focus',function(){ if((e.textContent||'').trim()===ph){e.textContent='';} });
      e.addEventListener('blur',function(){ if(!(e.textContent||'').trim()){e.textContent=ph;} });
      e.addEventListener('keydown',function(ev){ ev.stopPropagation(); if(ev.key==='Enter'){ ev.preventDefault(); sendFrom(e); } });
    });
    root.querySelectorAll('.cbtn.send').forEach(function(b){ if(b.getAttribute('data-send'))return; b.setAttribute('data-send','1'); b.addEventListener('click',function(ev){ ev.stopPropagation(); var inp=b.parentElement.querySelector('.cin'); if(inp)sendFrom(inp); }); });
    root.querySelectorAll('.cbtn.attach').forEach(function(b){ if(b.getAttribute('data-att'))return; b.setAttribute('data-att','1'); b.addEventListener('click',function(ev){ ev.stopPropagation(); var tray=root.querySelector('.atttray'); if(tray) tray.classList.toggle('on'); }); });
    root.querySelectorAll('.atchip').forEach(function(ch){ if(ch.getAttribute('data-wired'))return; ch.setAttribute('data-wired','1'); ch.addEventListener('click',function(ev){ ev.stopPropagation(); [].forEach.call(ch.parentElement.children,function(c){c.classList&&c.classList.remove('on');}); ch.classList.add('on'); attachChip(ch.getAttribute('data-att')||'photo'); }); });
  }
  function applyMoveType(root){
    if(!root)return;
    var perm=SFLmoveType==='perm';
    var lbl=root.querySelector('.termslbl'); if(lbl)lbl.textContent=perm?'Transfer terms':'Loan terms';
    [].forEach.call(root.querySelectorAll('.loanonly'),function(r){r.style.display=perm?'none':'';});
    [].forEach.call(root.querySelectorAll('.permonly'),function(r){r.style.display=perm?'':'none';});
  }
  function moveSplitToast(){ return SFLmoveType==='perm'?' · 1,000 coins · Manager 600 / Fan 400':''; }
  function pkWhistle(){
    try{
      var AC=window.AudioContext||window.webkitAudioContext; if(!AC)return;
      if(!window._sflac)window._sflac=new AC();
      var ac=window._sflac; if(ac.state==='suspended'){try{ac.resume();}catch(e){}}
      var t0=ac.currentTime;
      var o=ac.createOscillator(), g=ac.createGain(), lfo=ac.createOscillator(), lg=ac.createGain();
      o.type='sine'; o.frequency.value=2150;
      lfo.type='sine'; lfo.frequency.value=19; lg.gain.value=150;
      lfo.connect(lg); lg.connect(o.frequency);
      g.gain.setValueAtTime(0,t0);
      g.gain.linearRampToValueAtTime(0.22,t0+0.02);
      g.gain.setValueAtTime(0.22,t0+0.48);
      g.gain.linearRampToValueAtTime(0.0001,t0+0.62);
      o.connect(g); g.connect(ac.destination);
      o.start(t0); lfo.start(t0); o.stop(t0+0.64); lfo.stop(t0+0.64);
    }catch(e){}
  }
  function pkFinale(m){
    if(window._sflpkfin){clearInterval(window._sflpkfin);window._sflpkfin=null;}
    if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='PK-03')return;
    var phone=m.querySelector('.phone'); if(!phone)return;
    var ov=phone.querySelector('.pkstrike');
    if(!ov){ ov=document.createElement('div'); ov.className='pkstrike'; ov.innerHTML='<div class="pkst-word">STRIKE</div><div class="pkst-n">10</div><div class="pkst-cap">FINAL SECONDS</div>'; phone.appendChild(ov); }
    var nn=ov.querySelector('.pkst-n'); var n=10; if(nn)nn.textContent=n;
    var clk=m.querySelector('.pktimer .mclock'); if(clk){clk.setAttribute('data-sec','10'); var _mm=clk.querySelector('.mm'),_ss=clk.querySelector('.ss'); if(_mm)_mm.textContent='00'; if(_ss)_ss.textContent='10';}
    window._sflpkfin=setInterval(function(){
      if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='PK-03'){clearInterval(window._sflpkfin);window._sflpkfin=null;return;}
      n--; if(nn)nn.textContent=(n<0?0:n); ov.classList.toggle('hot',n<=3);
      if(n<=0){ clearInterval(window._sflpkfin); window._sflpkfin=null; pkWhistle(); var w=ov.querySelector('.pkst-word'); if(w)w.textContent='FULL TIME'; var c2=ov.querySelector('.pkst-cap'); if(c2)c2.textContent='Battle over'; setTimeout(function(){ if(((VIEWS[curJ].screens[curS]||{}).fnum)==='PK-03')goTo('pkfinalizing'); },1000); }
    },1000);
  }
  function startTimers(m){
    if(window._sfltmr){clearInterval(window._sfltmr);window._sfltmr=null;}
    var pad=function(n){return(n<10?'0':'')+n;};
    var C=2*Math.PI*28;
    var setRing=function(r,v,from){var fg=r.querySelector('.cdfg'); if(fg){fg.style.strokeDasharray=C.toFixed(1); fg.style.strokeDashoffset=(C*(1-v/from)).toFixed(1);} var n=r.querySelector('.cdn'); if(n)n.textContent=v; r.classList.toggle('low',v<=3);};
    [].forEach.call(m.querySelectorAll('.cdring'),function(r){var from=+(r.getAttribute('data-from')||10); if(r._v==null)r._v=from; setRing(r,r._v,from);});
    if(!m.querySelector('.mclock')&&!m.querySelector('.cdring'))return;
    window._sfltmr=setInterval(function(){
      [].forEach.call(m.querySelectorAll('.mclock'),function(c){var s=+(c.getAttribute('data-sec')||0); if(s>0)s--; c.setAttribute('data-sec',s); var mm=c.querySelector('.mm'),ss=c.querySelector('.ss'); if(mm)mm.textContent=pad(Math.floor(s/60)); if(ss)ss.textContent=pad(s%60); c.classList.toggle('low',s<=30&&s>0);});
      [].forEach.call(m.querySelectorAll('.cdring'),function(r){var from=+(r.getAttribute('data-from')||10); r._v=(r._v<=0?from:r._v-1); setRing(r,r._v,from);});
    },1000);
  }
  var _LIVENAMES=['Ada','SamRed','PitchZed','Marta','Kojo_9','Nadia','BlueMoon','TifoKing','GloveBoy','RedFury','Zico','LaraW','Deni','MoSalah7'];
  var _LIVESAY=['come on reds 🔴','what a save! 🧤','GOAL incoming ⚽','turn up the mics 🎙️','let\\'s go 🔥','who scored?','best room today','pass it wide!','🔥🔥🔥','defense please 😅','big match energy','love this club ❤️'];
  function startLiveFeed(m){
    if(window._sflfeed){clearInterval(window._sflfeed);window._sflfeed=null;}
    var box=m.querySelector('.rchat')||m.querySelector('.pkchat'); if(!box)return;
    var seed=_LIVENAMES[(curS+curJ)%_LIVENAMES.length];
    setTimeout(function(){ var b2=m.querySelector('.rchat')||m.querySelector('.pkchat'); if(b2!==box||!document.body.contains(box))return; pushComment('<b>'+seed+'</b> joined the live','joinmsg'); },500);
    var i=0;
    window._sflfeed=setInterval(function(){
      if(!document.body.contains(box)){clearInterval(window._sflfeed);window._sflfeed=null;return;}
      i++; var nm=_LIVENAMES[(i*5+3)%_LIVENAMES.length];
      if(i%3===0){ pushComment('<b>'+nm+'</b> joined the live','joinmsg'); }
      else { var col=['#8FE5FF','#DCFF8A','#FF9FB0','#FFD54F'][i%4]; pushComment('<b style="color:'+col+'">'+nm+'</b> '+_LIVESAY[(i*7)%_LIVESAY.length]); }
    },2900);
  }
  var SFLPOLICIES={
    tos:{t:'Terms of Service',ic:'📄',ac:'#2F7FD1',upd:'Last updated 12 Aug 2026',s:[
      {h:'Your account',p:'By using Soccer Fan Live (SFL) you agree to keep your login secure and to be at least the minimum age required in your region. One person, one account.'},
      {h:'Coins &amp; Gold',p:'Coins are a prepaid entertainment credit. Gold reflects verified activity and club standing. Neither is legal tender, and purchased Coins never move your Level.'},
      {h:'Fair play',p:'No bots, and no manipulation of Possession, gifts or PK results. Host earnings and commissions follow the published rates in your region.'},
      {h:'Your content',p:'You own what you post; you grant SFL a licence to display it inside live rooms and feeds. Illegal or abusive content is removed.'}]},
    privacy:{t:'Privacy Policy',ic:'🔒',ac:'#0FB753',upd:'Last updated 12 Aug 2026',s:[
      {h:'What we collect',p:'Your display name, User ID, club and activity needed to run live rooms, gifting and progression. We never sell your personal data.'},
      {h:'What stays private',p:'Phone numbers and email are never shown to other fans — invites and calls only reveal what is needed to connect you.'},
      {h:'Your controls',p:'You choose who can message or call you, and can toggle read receipts and online status any time in Privacy settings.'}]},
    community:{t:'Community Guidelines',ic:'📣',ac:'#FF3B5F',upd:'Play like a fan, not a troll',s:[
      {h:'Respect the room',p:'No harassment, hate speech or spam in live chat, PK battles or DMs. Hosts and managers can mute or remove disruptive fans.'},
      {h:'Keep it football',p:'Celebrate your club, back your side and keep rivalries friendly. Safety &amp; transaction messages can never be muted.'},
      {h:'Reporting',p:'Use the report control on any profile, room or message. Repeat violations lead to suspension.'}]},
    responsible:{t:'Responsible Play',ic:'🎮',ac:'#7C4DFF',upd:'Entertainment — never a way to earn',s:[
      {h:'Spend limits',p:'Mini-games use Coins or a free daily ticket, and winnings land in a separate non-withdrawable Bonus bucket. A daily play limit applies.'},
      {h:'No casino mechanics',p:'Odds are disclosed, outcomes are server-decided before any animation, and we never show fake “almost won” messages or auto-repeat.'},
      {h:'Need a break?',p:'You can set reminders or self-exclude from mini-games in Settings at any time.'}]},
    licenses:{t:'Licenses',ic:'⚖️',ac:'#B08900',upd:'Open-source &amp; third-party notices',s:[
      {h:'Fonts',p:'Manrope — SIL Open Font License 1.1.'},
      {h:'Libraries',p:'This prototype uses standard web technologies. Club names, crests and player likenesses shown are illustrative placeholders for demo purposes only.'},
      {h:'Contact',p:'legal@soccerfanlive.example'}]}
  };
  function applyLegalDoc(m){
    var p=SFLPOLICIES[SFLpolicy]||SFLPOLICIES.tos;
    var t=m.querySelector('.legaltitle'); if(t)t.textContent=p.t;
    var b=m.querySelector('.legalbody'); if(!b)return;
    var h='<div class="lgdhero" style="--ac:'+p.ac+'"><div class="lgdic">'+p.ic+'</div><div class="lgdt">'+p.t+'</div><div class="lgdu">🕒 '+p.upd+'</div></div>';
    for(var i=0;i<p.s.length;i++){ h+='<div class="lgdcard" style="--ac:'+p.ac+'"><div class="lgdnum">'+(i+1)+'</div><div><div class="lgdh">'+p.s[i].h+'</div><div class="lgdp">'+p.s[i].p+'</div></div></div>'; }
    h+='<div class="lgdfoot">SFL v1.0.0 · © 2026 Soccer Fan Live</div>';
    b.innerHTML=h;
  }
  function applyFollowTab(m){
    [].forEach.call(m.querySelectorAll('.foltab'),function(t){t.classList.toggle('on',t.getAttribute('data-tab')===SFLfollowTab);});
    [].forEach.call(m.querySelectorAll('.follist'),function(l){l.style.display=(l.getAttribute('data-list')===SFLfollowTab)?'':'none';});
  }
  function peerFromRow(row){
    var name='Fan', avbg='', role='', id='', club='Red Fury';
    var cn=row.querySelector('.cn,.un,.foln,.memn'); if(cn){var c=cn.cloneNode(true); [].forEach.call(c.querySelectorAll('.rolechip,.tick,span[style]'),function(x){x.remove();}); name=(c.textContent||'').replace(/[✓✔●]/g,'').trim();}
    var avEl=row.querySelector('.av,.cav .av,.folav,.memav'); if(avEl){avbg=avEl.style.backgroundImage||''; if(!avbg){var _cs=getComputedStyle(avEl); if(_cs&&_cs.backgroundImage&&_cs.backgroundImage!=='none')avbg=_cs.backgroundImage;}}
    var rc=row.querySelector('.rolechip'); if(rc)role=(rc.textContent||'').trim();
    if(row.getAttribute('data-id'))id=row.getAttribute('data-id');
    if(row.getAttribute('data-club'))club=row.getAttribute('data-club');
    return {name:name,avbg:avbg,role:role,id:id,club:club,on:!!row.querySelector('.dot')};
  }
  function applyChatPeer(m){
    var p=SFLchatPeer||{name:'Olivia S.',avbg:'',on:true}; var h=m.querySelector('.chdr'); if(!h)return;
    var hn=h.querySelector('.cn'); if(hn)hn.textContent=p.name;
    var ha=h.querySelector('.av'); if(ha&&p.avbg)ha.style.backgroundImage=p.avbg;
    var hs=h.querySelector('.cs'); if(hs)hs.innerHTML=p.on?'● Online':'Offline';
  }
  function applyProfilePeer(m){
    if(!SFLprofilePeer)return; var p=SFLprofilePeer;
    var pn=m.querySelector('.pn'); if(pn)pn.innerHTML=p.name+' <span style="color:#8FD0FF">✓</span>';
    var pav=m.querySelector('.pav'); if(pav&&p.avbg)pav.style.backgroundImage=p.avbg;
    var pid=m.querySelector('.pid'); if(pid&&p.id)pid.textContent='User ID '+p.id;
  }
  var SFL_SEAT_MAP={
    4:[[{p:'LW'},{p:'ST'},{p:'RW'}],[{p:'GK',gk:1}]],
    6:[[{p:'LW'},{p:'ST'},{p:'RW'}],[{p:'CM'},{p:'CM'}],[{p:'GK',gk:1}]],
    9:[[{p:'LW'},{p:'ST'},{p:'RW'}],[{p:'CM'},{p:'CM'}],[{p:'LB'},{p:'CB'},{p:'RB'}],[{p:'GK',gk:1}]],
    11:[[{p:'LW'},{p:'ST'},{p:'RW'}],[{p:'CM'},{p:'CM'},{p:'CM'}],[{p:'LB'},{p:'CB'},{p:'CB'},{p:'RB'}],[{p:'GK',gk:1}]],
    13:[[{p:'LW'},{p:'ST'},{p:'RW'}],[{p:'CM'},{p:'CM'},{p:'CM'}],[{p:'LB'},{p:'CB'},{p:'CB'},{p:'RB'}],[{p:'SUB'},{p:'GK',gk:1},{p:'SUB'}]]
  };
  var SFL_SEAT_PEOPLE=[
    {p:'LW',n:'Lucia',a:'pa_h_01.png',spk:1},{p:'ST',n:'Omar',a:'pa_h_03.png'},{p:'RW',n:'Open'},
    {p:'CM',n:'JJ',a:'pa_h_04.png'},{p:'CM',n:'Nadia',a:'pa_h_05.png',spk:1},{p:'CM',n:'Teo',a:'pa_h_06.png'},
    {p:'LB',n:'Kojo',a:'pa_h_01.png'},{p:'CB',n:'Sara',a:'pa_h_05.png'},{p:'CB',n:'Open'},{p:'RB',n:'Mik',a:'pa_h_03.png'},
    {p:'GK',n:'GloveBoy',a:'pa_h_04.png',gk:1},{p:'SUB',n:'Open'},{p:'SUB',n:'Open'}
  ];
  var SFL_SEAT_DOTS={
    4:[{l:22,t:22},{l:50,t:16},{l:78,t:22},{l:50,t:88,gk:1}],
    6:[{l:22,t:18},{l:50,t:14},{l:78,t:18},{l:35,t:48},{l:65,t:48},{l:50,t:88,gk:1}],
    9:[{l:22,t:16},{l:50,t:12},{l:78,t:16},{l:35,t:44},{l:65,t:44},{l:22,t:70},{l:50,t:74},{l:78,t:70},{l:50,t:90,gk:1}],
    11:[{l:22,t:16},{l:50,t:12},{l:78,t:16},{l:28,t:42},{l:50,t:46},{l:72,t:42},{l:18,t:70},{l:39,t:74},{l:61,t:74},{l:82,t:70},{l:50,t:90,gk:1}],
    13:[{l:22,t:16},{l:50,t:12},{l:78,t:16},{l:28,t:42},{l:50,t:46},{l:72,t:42},{l:18,t:68},{l:39,t:72},{l:61,t:72},{l:82,t:68},{l:28,t:88},{l:50,t:90,gk:1},{l:72,t:88}]
  };
  function seatCountN(){ var n=+SFLseatCount||11; return SFL_SEAT_MAP[n]?n:11; }
  function applyFormMode(m){
    var n=seatCountN();
    var seg=m.querySelector('.modeseg'); if(seg){ [].forEach.call(seg.querySelectorAll('.mseg'),function(s){ s.classList.toggle('on', s.getAttribute('data-mode')===SFLseatMode); }); }
    var pv=m.querySelector('.posview'), nv=m.querySelector('.numview'); if(pv)pv.style.display=(SFLseatMode==='num')?'none':''; if(nv)nv.style.display=(SFLseatMode==='num')?'':'none';
    var np=m.querySelector('.numpitch'); if(np){ np.style.gridTemplateColumns=n<=6?'repeat(3,1fr)':'repeat(4,1fr)'; var html=''; for(var i=1;i<=n;i++){ html+='<div class="numslot'+(i===1?' host':'')+'">'+i+(i===1?'<span class="sl">Host</span>':'')+'</div>'; } np.innerHTML=html; }
    var note=m.querySelector('.numnote'); if(note)note.innerHTML='Guests join by number (2–'+n+'). You\\'re always <b>#1</b> as host — you don\\'t pick a position.';
    var grid=m.querySelector('.formgrid'); if(grid) grid.style.display=(SFLseatMode==='pos'&&n>=11)?'':'none';
    var bp=m.querySelector('.bigpitch');
    if(bp&&SFLseatMode==='pos'){
      var dots=SFL_SEAT_DOTS[n]||SFL_SEAT_DOTS[11];
      var keep=bp.querySelectorAll('.mln,.mcirc');
      var marks=''; [].forEach.call(keep,function(el){ marks+=el.outerHTML; });
      bp.innerHTML=marks+dots.map(function(d){ return '<span class="pn'+(d.gk?' gk':'')+'" style="left:'+d.l+'%;top:'+d.t+'%"></span>'; }).join('');
    }
    if(n<11) SFLformation=n+'-seat';
    var cta=m.querySelector('.cta .btn'); if(cta)cta.textContent='Preview & Go Live · '+(SFLseatMode==='num'?('Numbers 1–'+n):(n>=11?SFLformation:(n+' seats')));
  }
  function applyLiveSeats(root){
    if(!root) return;
    var n=seatCountN();
    var phone=root.querySelector('.phone.room');
    if(phone) phone.setAttribute('data-seats',String(n));
    var ff=root.querySelector('.formfield'); if(!ff) return;
    var wa=ff.querySelector('.wavid'); var waHTML=wa?wa.outerHTML:'';
    var fn=((VIEWS[curJ].screens[curS]||{}).fnum)||'';
    var allOpen=fn==='GL-02A';
    var youOn=fn==='GL-05B'||fn==='GL-CH-C';
    var used={}; var youPlaced=false;
    function take(p){
      if(allOpen) return {p:p,n:'Open'};
      var i; for(i=0;i<SFL_SEAT_PEOPLE.length;i++){ if(SFL_SEAT_PEOPLE[i].p===p&&!used[i]){ used[i]=1; return SFL_SEAT_PEOPLE[i]; } }
      return {p:p,n:'Open'};
    }
    var hostYou=fn==='GL-03H'||fn==='GL-WA-H'||fn==='GL-02A';
    var hostNm=hostYou?'You':'RobbieOnAir';
    var html='<div class="frow hostrow"><div class="seat host'+(hostYou?' you':'')+'"><div class="av" style="background-image:url(\\\'assets/pa_h_02.png\\\')"></div><div class="hl"><i></i>'+(fn==='GL-02A'?'PREVIEW':'LIVE')+'</div><div class="pos">HOST</div><div class="nm">'+hostNm+'</div></div></div>';
    var lines=({4:['fwd','gk'],6:['fwd','mid','gk'],9:['fwd','mid','def','gk'],11:['fwd','mid','def','gk'],13:['fwd','mid','def','gk']})[n]||['fwd','mid','def','gk'];
    (SFL_SEAT_MAP[n]||SFL_SEAT_MAP[11]).forEach(function(row,ri){
      html+='<div class="frow '+(lines[ri]||'')+'">';
      row.forEach(function(slot){
        var fan=take(slot.p); var open=/^open$/i.test(fan.n||'');
        if(youOn&&open&&!youPlaced){ fan={p:slot.p,n:'You',a:'pa_h_06.png',you:1}; youPlaced=true; open=false; }
        var cls='seat'+(open?' open':'')+(fan.spk?' spk':'')+(fan.you?' you':'');
        var avSt=(!open&&fan.a)?' style="background-image:url(\\\'assets/'+fan.a+'\\\')"':'';
        var posSt=(slot.gk||fan.gk)?' style="background:var(--gold1);color:#5A3E00"':'';
        var nmSt=fan.you?' style="color:var(--gold2)"':'';
        html+='<div class="'+cls+'"><div class="av"'+avSt+'>'+(open?'＋':'')+'</div><div class="pos"'+posSt+'>'+slot.p+'</div><div class="nm"'+nmSt+'>'+(open?'Open':fan.n)+'</div></div>';
      });
      html+='</div>';
      if(waHTML&&ri===0) html+=waHTML;
    });
    ff.innerHTML=html;
    var filled=ff.querySelectorAll('.seat:not(.open)').length;
    var meta=root.querySelector('.rt2 .rmeta');
    if(meta){ var tx=meta.textContent||''; if(/\d+\s*\/\s*\d+/.test(tx)) meta.textContent=tx.replace(/\d+\s*\/\s*\d+(\s*filled)?/, filled+'/'+n+(/\s*filled/i.test(tx)?' filled':'')); }
  }
  function applyPosSheet(m){
    var list=m.querySelector('.poslist'); if(!list) return;
    var n=seatCountN();
    var sh=m.querySelector('.sh2'); if(sh) sh.innerHTML=(n>=11?SFLformation:(n+'-seat'))+' · <b style="color:#0FA04C">open seats</b> · '+n+' total';
    var used={};
    function take(p){ var i; for(i=0;i<SFL_SEAT_PEOPLE.length;i++){ if(SFL_SEAT_PEOPLE[i].p===p&&!used[i]){ used[i]=1; return SFL_SEAT_PEOPLE[i]; } } return {p:p,n:'Open'}; }
    var slots=[]; (SFL_SEAT_MAP[n]||SFL_SEAT_MAP[11]).forEach(function(r){ r.forEach(function(s){ slots.push(s); }); });
    list.innerHTML=slots.map(function(s){
      var fan=take(s.p); var open=/^open$/i.test(fan.n||'');
      var names={LW:'Left Wing',ST:'Striker',RW:'Right Wing',CM:'Centre Mid',LB:'Left Back',CB:'Centre Back',RB:'Right Back',GK:'Goalkeeper',SUB:'Substitute'};
      if(open) return '<div class="posrow"><div class="pb open">'+s.p+'</div><div><div class="pn2">'+(names[s.p]||s.p)+'</div><div class="ps">Open</div></div><div class="opentag">Take it</div></div>';
      return '<div class="posrow"><div class="pb taken">'+s.p+'</div><div><div class="pn2">'+(names[s.p]||s.p)+'</div><div class="ps">'+fan.n+'</div></div><div class="av" style="background-image:url(\\\'assets/'+(fan.a||'up_10.png')+'\\\')"></div></div>';
    }).join('');
  }
  function applyPermissions(m){
    if(!m)return;
    function setAct(row, cls, txt){ var act=row.querySelector('[data-perm-act]'); if(!act)return; act.className=cls; act.textContent=txt; }
    var cam=m.querySelector('.permcard[data-perm="camera"]'); if(cam){ setAct(cam, SFLperm.camera?'done':'allow', SFLperm.camera?'✓ Allowed':'Allow'); }
    var mic=m.querySelector('.permcard[data-perm="mic"]'); if(mic){ setAct(mic, SFLperm.mic?'done':'allow', SFLperm.mic?'✓ Allowed':'Allow'); }
    var notif=m.querySelector('.permcard[data-perm="notif"]'); if(notif){
      if(SFLperm.notif==='allowed') setAct(notif,'done','✓ Allowed');
      else if(SFLperm.notif==='later') setAct(notif,'deferred','Skipped');
      else setAct(notif,'later','Later');
    }
    var ready=!!(SFLperm.camera&&SFLperm.mic);
    var btn=m.querySelector('.permsetup .cta .btn')||m.querySelector('.cta .btn');
    if(btn){ btn.classList.toggle('disabled',!ready); btn.textContent=ready?'Continue':'Allow camera & mic to continue'; }
    var prev=m.querySelector('.campreview'); if(prev) prev.style.opacity=SFLperm.camera?'1':'.72';
  }
  function applySeatNumbers(m){
    var ht=m.querySelector('.seat.host')||m.querySelector('.hosttile'); if(ht){ var hn=ht.querySelector('.hostnum'); if(SFLseatMode==='num'){ if(!hn){hn=document.createElement('div');hn.className='hostnum';ht.appendChild(hn);} hn.textContent='1'; } else if(hn){ hn.remove(); } }
    if(SFLseatMode!=='num')return;
    var seats=m.querySelectorAll('.formfield .seat'); if(!seats.length)return;
    var n=2;
    [].forEach.call(seats,function(s){ if(s.classList.contains('host'))return; var pos=s.querySelector('.pos'); if(!pos)return; pos.textContent='#'+n; n++; });
  }
  function decorateSeatMics(m){
    var seats=m.querySelectorAll('.formfield .seat'); if(!seats.length)return;
    [].forEach.call(seats,function(s,idx){ if(s.classList.contains('open'))return; if(s.querySelector('.micind'))return;
      var old=s.querySelector('.mut'); if(old)old.remove();
      var muted=(idx%5===2);
      var mi=document.createElement('div'); mi.className='micind'+(muted?' muted':''); mi.textContent=muted?'🔇':'🎤';
      s.appendChild(mi);
    });
  }
  function initMgPenalty(root){
    var field=root.querySelector('#mgpk')||root.querySelector('.mgpk'); if(!field) return;
    var keeper=root.querySelector('#mgpk-keeper'), ball=root.querySelector('#mgpk-ball');
    var ret=root.querySelector('#mgpk-ret'), trail=root.querySelector('#mgpk-trail');
    var pwr=root.querySelector('#mgpk-pwr'), needle=root.querySelector('#mgpk-needle');
    var ang=root.querySelector('#mgpk-ang'), prompt=root.querySelector('#mgpk-prompt');
    var flash=root.querySelector('#mgpk-flash'), goal=root.querySelector('.mgpk-goal');
    var G={phase:'aim',ax:0.5,ay:0.42,power:0.5,moved:0,drag:0,t0:0};
    function clamp(v,a,b){ return v<a?a:v>b?b:v; }
    function goalM(){ if(!goal) return {gl:45,gt:22,gw:292,gh:142}; var pr=field.getBoundingClientRect(),gr=goal.getBoundingClientRect(); return {gl:gr.left-pr.left,gt:gr.top-pr.top,gw:gr.width,gh:gr.height}; }
    function setPrompt(t,big){ if(!prompt)return; prompt.textContent=t||''; prompt.className='mgpk-prompt'+(big?' big':''); }
    function layout(){
      var m=goalM();
      if(keeper){ keeper.classList.remove('dive'); keeper.style.left=(m.gl+m.gw/2-20)+'px'; keeper.style.top=(m.gt+m.gh*0.38)+'px'; keeper.style.transform=''; }
      if(ball){ ball.className='mgpk-ball idle'; ball.style.left=(field.clientWidth/2-14)+'px'; ball.style.top=(field.clientHeight-54)+'px'; ball.style.opacity='1'; ball.style.transform=''; ball.style.setProperty('--sc','1'); }
      if(ret) ret.classList.remove('on'); if(trail) trail.innerHTML=''; if(pwr) pwr.classList.remove('on'); if(ang) ang.classList.remove('on');
      field.classList.remove('bulge','shake');
    }
    function placeAim(x,y){
      G.ax=x; G.ay=y; var m=goalM();
      var px=m.gl+clamp(x,-0.12,1.12)*m.gw, py=m.gt+clamp(y,-0.12,1.12)*m.gh;
      if(ret){ ret.style.left=px+'px'; ret.style.top=py+'px'; ret.classList.add('on'); }
      if(trail&&ball){
        var sx=parseFloat(ball.style.left)+14, sy=parseFloat(ball.style.top)+14, h='';
        for(var i=1;i<=7;i++){ var p=i/8; h+='<b style="left:'+(sx+(px-sx)*p)+'px;top:'+(sy+(py-sy)*p-46*Math.sin(Math.PI*p))+'px"></b>'; }
        trail.innerHTML=h;
      }
      if(ang){
        var bx=field.clientWidth/2, by=field.clientHeight-40;
        var sweep=Math.round(90+Math.atan2(px-bx, by-py)*180/Math.PI);
        sweep=clamp(sweep,0,180);
        var side=sweep<35?'Far left':sweep<70?'Left':sweep>145?'Far right':sweep>110?'Right':'Centre';
        var height=y<0.28?'top':y>0.72?'low':'mid';
        ang.textContent='ANGLE · '+side+' '+height+' · '+sweep+'°'; ang.classList.add('on');
      }
    }
    function aimFrom(e){
      var m=goalM(), fr=field.getBoundingClientRect();
      var x=(e.clientX-fr.left-m.gl)/m.gw, y=(e.clientY-fr.top-m.gt)/m.gh;
      return {x:clamp(x,-0.12,1.12), y:clamp(y,-0.12,1.12)};
    }
    function bouncePower(){
      if(G.phase!=='power') return;
      var t=(performance.now()-G.t0)/1000, cyc=(t*1.45)%2, p=cyc<1?cyc:2-cyc;
      G.power=0.10+p*0.90;
      if(needle) needle.style.bottom=(G.power*100)+'%';
      window._sflmgpkraf=requestAnimationFrame(bouncePower);
    }
    function fire(){
      if(G.phase!=='power') return;
      G.phase='fire'; if(window._sflmgpkraf){cancelAnimationFrame(window._sflmgpkraf);window._sflmgpkraf=0;}
      if(pwr) pwr.classList.remove('on'); if(ret) ret.classList.remove('on'); if(trail) trail.innerHTML='';
      setPrompt('');
      var scatter=(G.power>0.86?0.18:0.06)+(G.power<0.22?0.10:0);
      var fx=clamp(G.ax+(Math.random()-0.5)*scatter*2,-0.08,1.08);
      var fy=clamp(G.ay+(Math.random()-0.5)*scatter*1.4,-0.12,1.08);
      var over=fy<-0.03||(G.power>0.93&&fy<0.16&&Math.random()<0.62);
      var wide=fx<-0.02||fx>1.02;
      var kx,ky;
      if(Math.random()<0.46){ kx=G.ax<0.5?0.64+Math.random()*0.24:0.08+Math.random()*0.24; ky=0.28+Math.random()*0.46; }
      else { kx=clamp(G.ax+(Math.random()-0.5)*0.16,0.06,0.94); ky=clamp(G.ay+(Math.random()-0.5)*0.16,0.08,0.92); }
      var corner=Math.min(Math.min(fx,1-fx),Math.min(fy,1-fy));
      var reach=0.20-G.power*0.05-(0.12-Math.min(0.12,corner))*1.05;
      var dx=fx-kx, dy=(fy-ky)*0.72, dist=Math.sqrt(dx*dx+dy*dy);
      var out;
      if(over) out={r:'miss',label:'Over the bar'};
      else if(wide) out={r:'miss',label:'Wide'};
      else if(dist<reach) out={r:'save',label:'Saved!'};
      else if(corner<0.11&&G.power>0.5) out={r:'goal',label:'Top corner!'};
      else out={r:'goal',label:'GOAL!'};
      var m=goalM();
      if(ball){ ball.className='mgpk-ball spin'; }
      if(keeper){ keeper.classList.add('dive'); keeper.style.left=(m.gl+kx*m.gw-18)+'px'; keeper.style.top=(m.gt+ky*m.gh-6)+'px'; keeper.style.transform='rotate('+(kx<0.5?-32:32)+'deg)'; }
      var sx=parseFloat(ball.style.left), sy=parseFloat(ball.style.top);
      var tx=over?sx:(wide?(fx<0.5?m.gl-30:m.gl+m.gw+6):m.gl+fx*m.gw-13);
      var ty=over?(m.gt-46):(m.gt+fy*m.gh-13);
      var dur=560+G.power*120, arc=70+G.power*42, t0=null;
      function fly(ts){
        if(!t0)t0=ts; var t=clamp((ts-t0)/dur,0,1);
        var sc=1-0.42*t;
        ball.style.left=(sx+(tx-sx)*t)+'px'; ball.style.top=(sy+(ty-sy)*t-arc*Math.sin(Math.PI*t))+'px';
        ball.style.setProperty('--sc',sc); ball.style.transform='scale('+sc+')';
        if(t<1) window._sflmgpkraf=requestAnimationFrame(fly);
        else finish(out);
      }
      window._sflmgpkraf=requestAnimationFrame(fly);
    }
    function finish(out){
      field.classList.add('shake');
      if(out.r==='goal'){ field.classList.add('bulge'); if(flash){flash.classList.add('on');} if(ball) ball.style.opacity='0'; }
      else if(out.r==='save'&&ball){ ball.style.transition='left .28s, top .28s'; ball.style.left=(parseFloat(ball.style.left)-30+Math.random()*60)+'px'; ball.style.top=(parseFloat(ball.style.top)+32)+'px'; }
      else if(ball){ ball.style.opacity='0'; }
      setPrompt(out.label,true);
      window._sflmgpkto=setTimeout(function(){ goTo(out.r==='goal'?'penaltygoal':'penaltysaved'); },1280);
    }
    layout(); placeAim(0.5,0.42); setPrompt('1/2 · DRAG anywhere — 0° left · 90° centre · 180° right');
    field.addEventListener('pointerdown',function(e){
      e.preventDefault(); try{field.setPointerCapture(e.pointerId);}catch(err){}
      if(G.phase==='aim'){ G.drag=1; G.moved=0; var a=aimFrom(e); placeAim(a.x,a.y); }
      else if(G.phase==='power'){ fire(); }
    });
    field.addEventListener('pointermove',function(e){
      if(G.phase!=='aim'||!G.drag) return;
      if(e.pointerType==='mouse'&&!(e.buttons&1)) return;
      var a=aimFrom(e); G.moved++; placeAim(a.x,a.y);
    });
    function endAim(){
      if(G.phase!=='aim'||!G.drag) return;
      G.drag=0;
      if(G.moved<2){ setPrompt('1/2 · DRAG left to right — every angle is live'); return; }
      G.phase='power'; G.t0=performance.now();
      if(pwr) pwr.classList.add('on');
      setPrompt('2/2 · TAP to lock POWER — mind the red');
      bouncePower();
    }
    field.addEventListener('pointerup',endAim);
    field.addEventListener('pointercancel',endAim);
  }
  function initMgWheel(root){
    var disc=root.querySelector('#mgwh-disc')||root.querySelector('.wheeldisc');
    var needle=root.querySelector('#mgwh-needle');
    var prompt=root.querySelector('#mgwh-prompt');
    var ptr=root.querySelector('#mgwh-ptr')||root.querySelector('.wheelptr');
    var btn=root.querySelector('#mgwh-spin')||root.querySelector('.btn.purple');
    var forceEl=root.querySelector('#mgwh-force')||root.querySelector('.wforce');
    if(!disc) return;
    var W={phase:'ready',rot:0,power:0.5,t0:performance.now(),busy:0};
    var SEGS=[
      {key:'50',kind:'coin'},{key:'free',kind:'free'},{key:'100',kind:'coin'},{key:'gift',kind:'gift'},
      {key:'30',kind:'coin'},{key:'jackpot',kind:'gift'},{key:'10',kind:'coin'},{key:'miss',kind:'miss'}
    ];
    function setPrompt(t){ if(prompt) prompt.textContent=t||''; }
    function segAt(rot){ var a=((-rot)%360+360)%360; return Math.floor(a/45)%8; }
    function markSeg(idx){
      [].forEach.call(root.querySelectorAll('.wchip'),function(c){ c.classList.toggle('on', +c.getAttribute('data-seg')===idx); });
    }
    function bounce(){
      if(W.phase!=='ready') return;
      var t=(performance.now()-W.t0)/1000, cyc=(t*1.35)%2, p=cyc<1?cyc:2-cyc;
      W.power=0.12+p*0.88;
      if(needle) needle.style.left=(W.power*100)+'%';
      window._sflmgwhraf=requestAnimationFrame(bounce);
    }
    function resetReady(label, btnTxt){
      W.busy=0; W.phase='ready'; W.t0=performance.now();
      if(forceEl) forceEl.classList.remove('lock');
      if(btn){ btn.textContent=btnTxt; btn.classList.remove('dis'); }
      setPrompt(label); markSeg(-1); bounce();
    }
    function launch(){
      if(W.busy||W.phase!=='ready') return;
      W.busy=1; W.phase='accel';
      if(window._sflmgwhraf){cancelAnimationFrame(window._sflmgwhraf);window._sflmgwhraf=0;}
      disc.style.transition='none';
      var force=W.power;
      var peak=18+force*36;
      var accelMs=160+force*260;
      var drag=0.988-(1-force)*0.008;
      var last=performance.now(), lastSeg=segAt(W.rot), vel=0, t0=last;
      if(forceEl) forceEl.classList.add('lock');
      setPrompt(force>0.82?'MAX FORCE — winding up…':force<0.28?'Soft flick — winding up…':'Locked — winding up, then friction takes it…');
      if(btn){ btn.textContent='Spinning…'; btn.classList.add('dis'); }
      function frame(ts){
        var dt=Math.min((ts-last)/16.67, 2.4); last=ts;
        if(W.phase==='accel'){
          var u=Math.min(1,(ts-t0)/accelMs);
          vel=peak*u*u*(3-2*u);
          if(u>=1){ vel=peak; W.phase='coast'; setPrompt(force>0.82?'MAX FORCE — letting it run down…':force<0.28?'Soft flick — watching it die…':'Spinning — friction is eating the speed…'); }
        } else {
          vel*=Math.pow(drag, dt);
          if(Math.abs(vel)<7) vel*=Math.pow(0.94, dt);
        }
        W.rot+=vel*dt;
        disc.style.transform='rotate('+W.rot+'deg)';
        var s=segAt(W.rot);
        if(s!==lastSeg){ lastSeg=s; markSeg(s); if(ptr){ ptr.classList.remove('tick'); void ptr.offsetWidth; ptr.classList.add('tick'); } }
        if(W.phase==='coast'&&Math.abs(vel)<=0.28) settle();
        else window._sflmgwhraf=requestAnimationFrame(frame);
      }
      window._sflmgwhraf=requestAnimationFrame(frame);
    }
    function settle(){
      var idx=segAt(W.rot);
      var want=-(idx*45+22.5);
      var k=Math.round((W.rot-want)/360);
      var fin=want+k*360;
      disc.style.transition='transform .42s cubic-bezier(.18,.78,.22,1)';
      disc.style.transform='rotate('+fin+'deg)';
      W.rot=fin; markSeg(idx);
      var out=SEGS[idx];
      setPrompt(out.kind==='gift'?'Gift landed!':out.kind==='free'?'Extra spin!':out.kind==='miss'?'No prize this time':'+'+out.key+' Bonus');
      window._sflmgwhto=setTimeout(function(){
        disc.style.transition='none';
        if(out.kind==='gift'){ if(!goTo('giftresult')) goTo('wheelresult'); }
        else if(out.kind==='free') resetReady('Free spin unlocked — TAP to lock FORCE again','Free Spin');
        else if(out.kind==='miss') resetReady('TAP Spin to lock FORCE again','Spin Again · 20 Coins');
        else goTo('wheelresult');
      }, 720);
    }
    bounce();
    function go(){ launch(); }
    if(btn) btn.addEventListener('click',function(e){ e.stopPropagation(); go(); });
    disc.addEventListener('click',function(e){ e.stopPropagation(); go(); });
  }
  function csMoney(n){ return '$'+(Math.round(n*100)/100).toFixed(2); }
  function applyCsDetail(root){
    var usd=(SFLcs.amt||5000)/(SFLcs.rate||104);
    var custom=root.querySelector('#cs-custom'); if(custom) custom.textContent=String(SFLcs.amt);
    [].forEach.call(root.querySelectorAll('.cs-usd,.cs-usd2'),function(el){ el.textContent=csMoney(usd); });
    var rate=root.querySelector('.cs-rate'); if(rate) rate.textContent=(SFLcs.rate||104)+' Coins / $1';
    var name=root.querySelector('.cs-name'); if(name) name.innerHTML=(SFLcs.name||'Maya Chen')+' <span class="vbadge">✓ Verified</span>';
    var btn=root.querySelector('.cta .btn'); if(btn&&/purchase request/i.test(btn.textContent||'')) btn.textContent='Create purchase request';
  }
  function applyCsWallet(root){
    var b=root.querySelector('#cs-trade-bucket');
    if(!b) return;
    if(SFLcs.status==='approved'){ b.style.display=''; var av=root.querySelector('#cs-w-av'); var rs=root.querySelector('#cs-w-rs'); if(av)av.textContent=SFLcs.tradeAvail.toLocaleString('en-US'); if(rs)rs.textContent=SFLcs.tradeReserved.toLocaleString('en-US'); }
    else { b.style.display='none'; }
  }
  function applyCsScreen(root,fnum){
    if(fnum==='CS-02') applyCsDetail(root);
    if(fnum==='CS-04'){ SFLcs.proof=0; }
    if(fnum==='CS-03') playCsBuyer(root,'pending');
    if(fnum==='CS-05') playCsBuyer(root,'wait');
    if(fnum==='CS-06') playCsBuyer(root,'xfer');
    if(fnum==='CS-30'){
      var av=root.querySelector('#cs-desk-av'), rs=root.querySelector('#cs-desk-rs'), tot=root.querySelector('#cs-desk-total');
      if(av) av.textContent=SFLcs.tradeAvail.toLocaleString('en-US');
      if(rs) rs.textContent=SFLcs.tradeReserved.toLocaleString('en-US');
      if(tot) tot.textContent=(SFLcs.tradeAvail+SFLcs.tradeReserved).toLocaleString('en-US');
    }
    if(fnum==='CS-23') SFLcs.status='approved';
    if(fnum==='CS-25') SFLcs.status='suspended';
  }
  function csStill(fn){ return ((VIEWS[curJ].screens[curS]||{}).fnum)===fn && ((VIEWS[curJ].screens[curS]||{}).srcJ===25); }
  function csMarkStage(st, kind, title, sub){
    if(!st) return;
    var sd=st.querySelector('.sd'), t=st.querySelector('.st'), s=st.querySelector('.ss');
    st.classList.remove('wait');
    if(kind==='done'){ if(sd){sd.className='sd done';sd.textContent='✓';} }
    else if(kind==='now'){ if(sd){sd.className='sd now';sd.textContent='';} }
    else { st.classList.add('wait'); if(sd){sd.className='sd wait';sd.textContent='◦';} }
    if(title&&t) t.textContent=title;
    if(sub&&s) s.textContent=sub;
  }
  function playCsBuyer(root,kind){
    var stages=root.querySelectorAll('.stage');
    var live=root.querySelector('.cs-live');
    if(window._sflcsto){clearTimeout(window._sflcsto);window._sflcsto=null;}
    if(kind==='pending'){
      window._sflcsto=setTimeout(function(){
        if(!csStill('CS-03')) return;
        csMarkStage(stages[1],'done','Maya accepted','500 Coins stay reserved until you pay');
        csMarkStage(stages[2],'now','Pay by bank transfer','Open your bank app · use ORD-2901');
        if(live) live.textContent='Maya accepted your request. You can pay now.';
        sflToast('Seller accepted your request');
        window._sflcsto=setTimeout(function(){ if(csStill('CS-03')) goTo('cspay'); }, 900);
      }, 1400);
    }
    if(kind==='wait'){
      window._sflcsto=setTimeout(function(){
        if(!csStill('CS-05')) return;
        csMarkStage(stages[2],'done','Maya confirmed payment','Screenshot matched ORD-2901');
        csMarkStage(stages[3],'now','Coins releasing','Reserved → your wallet');
        if(live) live.textContent='Payment confirmed. Coins are on the way.';
        sflToast('Payment confirmed · coins incoming');
        window._sflcsto=setTimeout(function(){ if(csStill('CS-05')) goTo('cstransfer'); }, 900);
      }, 1600);
    }
    if(kind==='xfer'){
      window._sflcsto=setTimeout(function(){
        if(!csStill('CS-06')) return;
        csMarkStage(stages[1],'done','Unlocking reserved Coins','500 trading → your balance');
        csMarkStage(stages[2],'now','Order complete','Crediting your wallet');
        window._sflcsto=setTimeout(function(){ if(csStill('CS-06')) goTo('csdone'); }, 800);
      }, 1200);
    }
  }
  function attachCsProof(root){
    var box=root.querySelector('#cs-proof');
    var btn=root.querySelector('#cs-send');
    if(!box||box.classList.contains('on')) return;
    SFLcs.proof=1;
    box.classList.add('on');
    box.innerHTML='<div class="proofshot"><div class="pk">Metro Commercial · Sent</div><div class="pv num">$48.08</div><div class="pr"><span>To M. Chen</span><span class="num">ORD-2901</span></div></div><div class="prooffoot">✓ Screenshot attached · ready to submit</div>';
    if(btn){ btn.classList.remove('dis'); btn.textContent='Submit proof & mark sent'; btn.setAttribute('data-csact','sent'); }
    sflToast('Screenshot attached');
  }
  // ---- Per-card neon energy image backgrounds (arcade / PS / Tekken vibe) ----
  // Distinct neon artwork behind each avatar. Order maps to the 6 Stadium cards.
  var EIMG=['b_c1','b_c3','b_c4','b_c2','b_c3','b_c5'];
  var SFLpip=null;
  function injectLivePip(){
    var sc=document.getElementById('scaler'); if(!sc||!sc.firstElementChild)return; var phone=sc.firstElementChild.querySelector('.phone')||sc.firstElementChild;
    var fn=((VIEWS[curJ].screens[curS]||{}).fnum)||'';
    var inLive=(fn==='GL-03V'||fn==='GL-03H'||fn==='GL-WA-V'||fn==='GL-WA-H');
    var ex=phone.querySelector('.sflpip');
    if(!SFLpip||inLive){ if(ex)ex.remove(); return; }
    if(ex)return;
    var pip=document.createElement('div'); pip.className='sflpip';
    pip.style.cssText='position:absolute;right:12px;bottom:96px;width:120px;height:82px;z-index:560;border-radius:12px;overflow:hidden;box-shadow:0 10px 26px rgba(0,0,0,.55);border:1.5px solid rgba(201,255,61,.6);cursor:pointer;background:#0b140c;font-family:Manrope,-apple-system,sans-serif';
    pip.innerHTML='<div style="position:absolute;inset:0;background:url(\\\'assets/pa_h_02.png\\\') center top/cover"></div><div style="position:absolute;top:5px;left:5px;background:#FF3B5C;color:#fff;font-size:8px;font-weight:800;padding:2px 6px;border-radius:5px">● LIVE</div><div class="pip-x" style="position:absolute;top:4px;right:4px;width:18px;height:18px;border-radius:50%;background:rgba(0,0,0,.55);color:#fff;font-size:10px;display:flex;align-items:center;justify-content:center">✕</div><div style="position:absolute;left:0;right:0;bottom:0;padding:4px 7px;font-size:8.5px;font-weight:800;color:#fff;background:linear-gradient(180deg,transparent,rgba(0,0,0,.85))">Matchday Warm-Up · tap to return</div>';
    phone.appendChild(pip);
    pip.addEventListener('click',function(e){ e.stopPropagation(); if(e.target.closest('.pip-x')){ SFLpip=null; pip.remove(); sflToast('Live closed'); return; } var r=SFLpip; SFLpip=null; goTo(r==='host'?'liveroomhost':'liveroom'); });
  }
  function showLeaveConfirm(){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return; var old=phone.querySelector('.sflleave'); if(old)old.remove();
    var w=document.createElement('div'); w.className='sflleave';
    w.style.cssText='position:absolute;inset:0;z-index:90;display:flex;align-items:center;justify-content:center;background:rgba(4,6,10,.7);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);font-family:Manrope,-apple-system,sans-serif';
    w.innerHTML='<div style="width:80%;max-width:290px;text-align:center;background:linear-gradient(180deg,#1b2233,#12151d);border:1px solid rgba(255,255,255,.14);border-radius:20px;padding:22px 20px">'
      +'<div style="font-size:17px;font-weight:800;color:#fff">Leave live room?</div>'
      +'<div style="font-size:13px;font-weight:600;color:#8892A4;margin-top:8px;line-height:1.5">Are you sure you want to leave? You can rejoin anytime while the host is live.</div>'
      +'<div style="display:flex;gap:9px;margin-top:18px"><div class="lv-stay" style="flex:1;padding:12px;border-radius:12px;background:rgba(255,255,255,.08);color:#C9D0DC;font-weight:800;font-size:13.5px;cursor:pointer">Stay</div><div class="lv-go" style="flex:1;padding:12px;border-radius:12px;background:rgba(228,54,43,.92);color:#fff;font-weight:800;font-size:13.5px;cursor:pointer">Leave room</div></div></div>';
    phone.appendChild(w);
    w.addEventListener('click',function(e){ e.stopPropagation(); if(e.target===w||e.target.closest('.lv-stay')){ w.remove(); return; } if(e.target.closest('.lv-go')){ w.remove(); SFLpip=null; sflToast('You left the live room'); goTo('live'); return; } });
  }
  function injectRoomBg(mount){ if(!mount)return; var cards=mount.querySelectorAll('.stadhome .roomcard .rc'); for(var i=0;i<cards.length;i++){ var rc=cards[i]; if(rc.querySelector('.rcbg'))continue; var b=document.createElement('div'); b.className='rcbg '+(EIMG[i%EIMG.length]); rc.insertBefore(b, rc.firstChild); } }
  function render(){
    var v=VIEWS[curJ]; if(!v||!v.screens.length)return;
    if(curS>=v.screens.length)curS=v.screens.length-1;
    var scr=v.screens[curS];
    mount.id='j'+scr.srcJ; mount.innerHTML=scr.html;
    var _ph=mount.querySelector('.phone'); if(_ph&&_ph.classList.contains('light')) _ph.setAttribute('data-sfl-light','1');
    if(window._sflpkto){clearTimeout(window._sflpkto);window._sflpkto=null;} if(window._sflpkfin){clearInterval(window._sflpkfin);window._sflpkfin=null;}
    if(window._sflmgpkraf){cancelAnimationFrame(window._sflmgpkraf);window._sflmgpkraf=0;} if(window._sflmgpkto){clearTimeout(window._sflmgpkto);window._sflmgpkto=null;}
    if(window._sflmgwhraf){cancelAnimationFrame(window._sflmgwhraf);window._sflmgwhraf=0;} if(window._sflmgwhto){clearTimeout(window._sflmgwhto);window._sflmgwhto=null;}
    if(window._sflcsto){clearTimeout(window._sflcsto);window._sflcsto=null;}
    if(window._sflwabar){clearInterval(window._sflwabar);window._sflwabar=null;}
    if(window._sflchto){clearTimeout(window._sflchto);window._sflchto=null;}
    if(window._sflcmto){clearTimeout(window._sflcmto);window._sflcmto=null;}
    injectBar(mount.querySelector('.phone'));
    applyStageChrome();
    SFLcoinify(mount); SFLcrest(mount); SFLchat(mount);
    if(/^ML-/.test(scr.fnum)||scr.fnum==='MC-07D') applyMoveType(mount);
    if(scr.fnum==='FT-01'||scr.fnum==='FT-02'){applyTaskDone(mount);}
    if(scr.fnum==='PV-04'){SFLpred={match:SFLpredMatch,score:SFLpredScore};}
    if(scr.fnum==='PV-05'){applyVoteDone(mount,'motm');}
    if(scr.fnum==='PV-09'){applyVoteDone(mount,'award');}
    if(scr.fnum==='GK-01E'){setTimeout(function(){flyGift('🥇');},180);}
    if(scr.fnum==='J2-21'&&SFLfvActive){var _j21b=mount.querySelector('.btn'); if(_j21b)_j21b.textContent='✓ Fan Value Active';}
    if(scr.fnum==='FV-00'&&SFLfvActive){var _fv0b=mount.querySelector('.btn'); if(_fv0b)_fv0b.textContent='✓ Already Active';}
    if((scr.fnum==='MSG-04'||scr.fnum==='MSG-05')&&SFLchatGift){ var _cg=SFLchatGift; SFLchatGift=null; var _mb=mount.querySelector('.msgs'); if(_mb){ var _gcard=document.createElement('div'); _gcard.className='giftcard'; _gcard.innerHTML='<div class="gi">'+_cg.em+'</div><div class="gt">You sent a '+_cg.gn+'</div><div class="gs">Sent via Gifts · '+_cg.gp+' Coins</div>'; _mb.appendChild(_gcard); _mb.scrollTop=_mb.scrollHeight; } setTimeout(function(){flyGift(_cg.em);},160); }
    if(scr.fnum==='PK-00'){SFLpkViewer=false;}
    if(scr.fnum==='G-02G'){SFLguest=true;}
    if(scr.fnum==='G-02'||scr.fnum==='G-02M'){SFLguest=false;}
    if(scr.fnum==='PK-03'){ var _pgb=mount.querySelector('.giftbtns'); if(_pgb)_pgb.style.display=SFLpkViewer?'':'none'; if(!SFLpkViewer){setTimeout(function(){flyGift('🎁');},500);setTimeout(function(){flyGift('🥇');},1300);} var _pck=mount.querySelector('.pktimer .mclock'); if(_pck){var _ps=(SFLpkMin||5)*60; _pck.setAttribute('data-sec',_ps); _pck.setAttribute('data-init',_ps); var _pmm=_pck.querySelector('.mm'),_pss=_pck.querySelector('.ss'); if(_pmm)_pmm.textContent=(SFLpkMin<10?'0':'')+(SFLpkMin||5); if(_pss)_pss.textContent='00';} pkWhistle(); window._sflpkto=setTimeout(function(){ pkFinale(mount); },4500); }
    if((scr.fnum==='PK-04A'||scr.fnum==='PK-04C')&&SFLpkViewer){var _reb=mount.querySelector('.winbtns .re'); if(_reb)_reb.style.display='none'; var _exb=mount.querySelector('.winbtns .ex'); if(_exb)_exb.style.flex='1';}
    if(scr.fnum==='PV-01'){applyPredDone(mount);}
    if(scr.fnum==='G-05'){ var _pf=mount.querySelector('.pv-fan'),_pm=mount.querySelector('.pv-mgr'); if(_pf)_pf.style.display=SFLmgrMode?'none':''; if(_pm)_pm.style.display=SFLmgrMode?'block':'none'; var _rm=mount.querySelector('.rolemgr'); if(_rm)_rm.style.display=SFLmgrMode?'':'none'; applyCmgrMember(mount); }
    if(scr.fnum==='CC-00'){ applyMgrGate(mount); }
    if(scr.fnum==='J2-20'){ SFLmember=false; }
    if(scr.fnum==='J2-01'){ SFLmember=false; SFLleaveAsk='none'; }
    if(scr.fnum==='J2-08'){ setTimeout(function(){ if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='J2-08')return; var m=mount; var _c=m.querySelector('.tl .dot.cur'); if(_c){_c.className='dot done';_c.textContent='✓';} var _pd=m.querySelector('.tl.pending'); if(_pd){_pd.classList.remove('pending'); var _dd=_pd.querySelector('.dot'); if(_dd){_dd.className='dot cur';_dd.textContent='◔';} var _t2=_pd.querySelector('.td'); if(_t2)_t2.textContent='Reviewing your application…';} },800);
      setTimeout(function(){ if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='J2-08')return; var m=mount; var _pl=m.querySelector('.sp-pending'); if(_pl){_pl.textContent='✓ Approved'; _pl.style.cssText='font-size:9px;font-weight:800;color:#0A8F40;background:#EAF9F0;border:1px solid #BFE9CE;padding:2px 8px;border-radius:999px';} var _c2=m.querySelector('.tl .dot.cur'); if(_c2){_c2.className='dot done';_c2.textContent='✓';} var _tls=m.querySelectorAll('.tl'); if(_tls.length){var _L=_tls[_tls.length-1]; var _tt=_L.querySelector('.tt'); if(_tt)_tt.textContent='Decision · Approved'; var _td=_L.querySelector('.td'); if(_td)_td.textContent='Welcome to Red District FC!';} var _b=m.querySelector('.btn.danger'); if(_b){_b.textContent='Enter Club'; _b.className='btn';} sflToast('✅ Application approved · Welcome to Red District FC'); },1600); }
    if(scr.fnum==='MG-03A'){ setTimeout(function(){ if(((VIEWS[curJ].screens[curS]||{}).fnum)==='MG-03A'){goTo('wheelresult');} },2900); }
    if(scr.fnum==='PL-04'){ var _plchk=function(){return ((VIEWS[curJ].screens[curS]||{}).fnum)==='PL-04';};
      setTimeout(function(){ if(!_plchk())return; var st=mount.querySelectorAll('.stage'); if(st[1]){var d=st[1].querySelector('.sd'); if(d){d.className='sd done';d.textContent='✓';}} if(st[2]){st[2].classList.remove('wait'); var d2=st[2].querySelector('.sd'); if(d2){d2.className='sd now';d2.textContent='';}} },1000);
      setTimeout(function(){ if(!_plchk())return; var st=mount.querySelectorAll('.stage'); if(st[2]){var d=st[2].querySelector('.sd'); if(d){d.className='sd done';d.textContent='✓';}} if(st[3]){st[3].classList.remove('wait'); var d3=st[3].querySelector('.sd'); if(d3){d3.className='sd now';d3.textContent='';}} },1800);
      setTimeout(function(){ if(!_plchk())return; [].forEach.call(mount.querySelectorAll('.stage'),function(s){s.classList.remove('wait'); var d=s.querySelector('.sd'); if(d){d.className='sd done';d.textContent='✓';}}); var _h1=mount.querySelector('.h1'); if(_h1)_h1.textContent='Transfer complete'; sflToast('✅ Transfer complete · view details to finish'); },2500); }
    if(scr.fnum==='PL-09'){ var _pl9=function(){return ((VIEWS[curJ].screens[curS]||{}).fnum)==='PL-09';};
      setTimeout(function(){ if(!_pl9())return; var st=mount.querySelectorAll('.stage'); if(st[1]){var d=st[1].querySelector('.sd'); if(d){d.className='sd done';d.textContent='✓';}} if(st[2]){st[2].classList.remove('wait'); var d2=st[2].querySelector('.sd'); if(d2){d2.className='sd now';d2.textContent=''; var ss=st[2].querySelector('.ss'); if(ss)ss.textContent='Releasing to your wallet';}} },1100);
      setTimeout(function(){ if(!_pl9())return; [].forEach.call(mount.querySelectorAll('.stage'),function(s){s.classList.remove('wait'); var d=s.querySelector('.sd'); if(d){d.className='sd done';d.textContent='✓';}}); var _h1=mount.querySelector('.h1'); if(_h1)_h1.textContent='Sale complete'; sflToast('Coins released to your wallet'); },1900);
      setTimeout(function(){ if(_pl9()) goTo('plsold'); }, 2600); }
    if(scr.fnum==='J2-LV'){ setTimeout(function(){ if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='J2-LV')return; var m=mount; var _h=m.querySelector('.ch1'); if(_h)_h.textContent='Leave approved ✓'; var _cm=m.querySelector('.cmedal'); if(_cm)_cm.innerHTML='✅<div class="halo2"></div>'; var _s=m.querySelector('.csub'); if(_s)_s.textContent='A club manager approved your request. You can complete leaving now.'; var _bt=m.querySelector('.cbtns'); if(_bt)_bt.innerHTML='<div class="btn lvcomplete">Complete Leaving</div>'; sflToast('✅ Leave request approved by your manager'); },1500); }
    if(scr.fnum==='G-02'||scr.fnum==='J2-16'||scr.fnum==='J2-10'||scr.fnum==='J2-15'){SFLmember=true;}
    if(/^[1-9]$|^1[0-6]$|^[1-9][a-z]$/.test(scr.fnum)||scr.fnum==='G-02G'){SFLmember=false;}
    scap.textContent=(scr.cap||'').slice(0,46);
    ct.textContent=(curS+1)+' / '+v.screens.length;
    var c2=document.getElementById('counter2');if(c2)c2.textContent=ct.textContent;
    var canBack=curJ>0||curS>0||hist.length>0;
    var canFwd=curJ<VIEWS.length-1||curS<v.screens.length-1;
    var bp2=document.getElementById('bprev2'),bn2=document.getElementById('bnext2');
    if(bp2){bp2.disabled=!canBack;bp2.classList.toggle('off',!canBack);}
    if(bn2){bn2.disabled=!canFwd;bn2.classList.toggle('off',!canFwd);}
    flowsel.value=curJ;
    if(scr.fnum==='GL-01'){ [].forEach.call(mount.querySelectorAll('.smcard'),function(c){ var v=parseInt(c.getAttribute('data-seats')||'0',10); c.classList.toggle('on', v===seatCountN()); }); }
    if(scr.fnum==='GL-02'){ applyFormMode(mount); }
    if(scr.fnum==='GL-01B'){ applyPermissions(mount); }
    if(scr.fnum==='G-05F'){ applyFollowTab(mount); }
    if(scr.fnum==='MSG-04'){ applyChatPeer(mount); }
    if(scr.fnum==='G-05U'){ applyProfilePeer(mount); }
    if(scr.fnum==='G-05TD'){ applyLegalDoc(mount); }
    if(scr.fnum==='MSG-01'&&SFLleftClub){ var _ccx=[].slice.call(mount.querySelectorAll('.crow')).filter(function(r){return r.querySelector('.rolechip.club');})[0]; if(_ccx)_ccx.style.display='none'; }
    if(scr.fnum==='GL-02A'){ var _gm=mount.querySelector('.rt2 .rmeta'); if(_gm){ _gm.textContent='Red District FC · '+(SFLseatMode==='num'?('Numbers 1–'+seatCountN()):((seatCountN()>=11?SFLformation:(seatCountN()+' seats'))+' · '+seatCountN()+' positions')); } }
    [].forEach.call(mount.querySelectorAll('.sflguest-static'),function(el){ el.remove(); });
    if(/^GL-02A$|^GL-03|^GL-05B$|^GL-CH-C$|^GL-WA-[HV]$/.test(scr.fnum)) applyLiveSeats(mount);
    if(scr.fnum==='GL-05') applyPosSheet(mount);
    startTimers(mount);
    startLiveFeed(mount);
    applySeatNumbers(mount);
    decorateSeatMics(mount);
    if(scr.fnum==='GL-00') injectRoomBg(mount);
    injectLivePip();
    if(scr.fnum==='CS-07'&&SFLmgrBuying){ var _ccb=mount.querySelector('[data-csgo="coinstore"]'); if(_ccb)_ccb.textContent='Continue · Create Club'; var _rlb=mount.querySelector('[data-csact="rate"],[data-csgo="csrate"]'); }
    if(scr.fnum==='GL-WA-H'||scr.fnum==='GL-WA-V'){applyWaClip(mount);applyWaSize(mount);}
    if(scr.fnum==='GL-WA-L'||scr.fnum==='GL-WA-P'){applyWaApp(mount);}
    if(scr.fnum==='GL-03H'||scr.fnum==='GL-WA-H'||scr.fnum==='GL-04'||scr.fnum==='GL-04A'){ if(SFLliveRole!=='cohost'&&SFLliveRole!=='manager') SFLliveRole='host'; }
    if(scr.fnum==='GL-CH-C'){ SFLliveRole='manager'; SFLcoHosts.you=1; }
    if(scr.fnum==='GL-03V'||scr.fnum==='GL-WA-V'){ if(SFLliveRole==='host') SFLliveRole=SFLcoHosts.you?'manager':'viewer'; }
    if(scr.fnum==='GL-05B'||scr.fnum==='GL-05OK'||scr.fnum==='GL-CH-C') SFLseated=true;
    if(scr.fnum==='GL-03V'||scr.fnum==='GL-00'||scr.fnum==='GL-03Vg') SFLseated=false;
    if(/^GL-03|^GL-04|^GL-05|^GL-CH|^GL-WA-/.test(scr.fnum)){applyLiveStaff(mount);}
    if(scr.fnum==='GL-05W'){
      window._sflchto=setTimeout(function(){
        if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='GL-05W')return;
        chDrop('join-you');
        sflToast('RobbieOnAir accepted your RW request');
        goTo('joinaccepted');
      },1400);
    }
    if(/^PL-0[2-5]/.test(scr.fnum)||scr.fnum==='PL-06A'||scr.fnum==='PL-07'||scr.fnum==='PL-07L'||scr.fnum==='PL-08'||scr.fnum==='PL-08L'||scr.fnum==='PL-09'||scr.fnum==='PL-10'){applyPlayer(mount);}
    if(scr.fnum==='PL-01'){applyPlMarket(mount);}
    if(scr.fnum==='PL-06'){applyPlSquad(mount);}
    if(scr.fnum==='PL-06A'){applyPlAction(mount);}
    if(scr.fnum==='PL-07L'||scr.fnum==='PL-08L'){applyPlLoan(mount);}
    if(scr.fnum==='PL-08'){applyPlListLive(mount);}
    if(scr.fnum==='PL-01W'){applyPlWeeklyBuys(mount);}
    if(scr.fnum==='PL-05'){applyPlPurchaseDuty(mount);}
    if(scr.fnum==='G-02'||scr.fnum==='G-02M'){applyHomePlayersDuty(mount);}
    if(scr.fnum==='FT-02'){applyFtPlayerDuty(mount);}
    if(scr.fnum==='FT-03P'){applyFtBuySellDetail(mount);}
    if(scr.fnum==='G-03'){applyPlNotifs(mount);applyCmgrNotifs(mount);applyTourn(mount);}
    if(scr.fnum==='J2-16'){applyCmgrMember(mount);}
    if(scr.fnum==='J2-05'){applyClubDetailMember(mount);}
    if(scr.fnum==='MC-01'){applyCmgrHqBadge(mount);}
    if(scr.fnum==='MC-04'||scr.fnum==='MC-04A'||scr.fnum==='MC-CM-01'||scr.fnum==='MC-CM-02'||scr.fnum==='MC-CM-03'){applyCmgrPick(mount);}
    if(scr.fnum==='MC-CM-02'){
      window._sflcmto=setTimeout(function(){
        if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='MC-CM-02')return;
        var _p=SFLcmgrPick||{}; var _id=_p.id||'priya';
        var _inv=cmgrFind('inv-'+_id); if(_inv)_inv.status='accepted';
        SFLcmgrInvite='accepted';
        SFLcmgrStaff[_id]=true; cmgrMark({name:_p.name||'Olivia M.'});
        sflToast((_p.name||'Olivia M.')+' accepted · they are now a manager');
        goTo('cmgrfanok');
      },1400);
    }
    if(scr.fnum==='MC-CM-Q'){applyCmgrQueue(mount);}
    if(scr.fnum==='MC-CM-F3'){
      window._sflcmto=setTimeout(function(){
        if(((VIEWS[curJ].screens[curS]||{}).fnum)!=='MC-CM-F3')return;
        var _aq=cmgrFind('ask-you'); if(_aq)_aq.status='accepted';
        cmgrGrant('you');
        sflToast('Jay Malik accepted · you are now a manager');
        goTo('cmgryes');
      },1400);
    }
    if(scr.fnum==='MC-CM-F5'){ var _rj=mount.querySelector('.cm-rej'); if(_rj)_rj.textContent=SFLcmgrAsk==='rejected'?'The manager declined your request. You stay a Fan of Red Fury. Nothing else changes.':'The manager invite was declined. You stay a Fan of Red Fury. Nothing else changes.'; }
    if(scr.fnum==='MG-02'){initMgPenalty(mount);}
    if(scr.fnum==='MG-03'){initMgWheel(mount);}
    if(scr.fnum==='WA-01'){applyCsWallet(mount);}
    if(scr.srcJ===25){applyCsScreen(mount,scr.fnum);}
    if(/^TR-/.test(scr.fnum)||scr.fnum==='PR-00'){applyTourn(mount);}
    if(scr.fnum==='10'){applySigninTab(mount);}
    fit();
  }
  var WACLIPS={goals:{title:'Every Goal · MD5',file:'fb_stadium.jpg'},derby:{title:'Derby Highlights',file:'fb_crowd.jpg'},skills:{title:'Skills of the Week',file:'fb_host.jpg'}};
  var WAAPPS={
    yt:{name:'YouTube',title:'Sign in',lib:'YouTube',badge:'YT',brand:'▶',email:'Email or phone',pass:'Password',btn:'Sign in',search:'Search YouTube',sub:'Sign in to pick a video for the pitch.',vids:[
      {title:'United vs City · Highlights',file:'fb_stadium.jpg',meta:'12:41 · 2.1M views'},
      {title:'Derby night · Best bits',file:'fb_crowd.jpg',meta:'8:02 · 890K views'},
      {title:'Skills of the week',file:'fb_host.jpg',meta:'6:18 · 410K views'}
    ]},
    fb:{name:'Facebook',title:'Facebook',lib:'Watch',badge:'FB',brand:'f',email:'Mobile number or email',pass:'Password',btn:'Log in',search:'Search Watch',sub:'Log in to stream a Facebook Watch video.',vids:[
      {title:'Matchday Warm-Up · Live replay',file:'fb_host.jpg',meta:'Watch · 18 min'},
      {title:'North Stand after the winner',file:'fb_crowd.jpg',meta:'Watch · 6 min'},
      {title:'Every goal · this weekend',file:'fb_stadium.jpg',meta:'Watch · 9 min'}
    ]},
    ig:{name:'Instagram',title:'Instagram',lib:'Reels',badge:'IG',brand:'◎',email:'Phone, username or email',pass:'Password',btn:'Log in',search:'Search',sub:'Log in to pick a Reel for Watch-Along.',vids:[
      {title:'Tunnel walk · Reels',file:'fb_host.jpg',meta:'0:47'},
      {title:'Crowd surge after the 2nd',file:'fb_crowd.jpg',meta:'0:28'},
      {title:'Top bins compilation',file:'fb_stadium.jpg',meta:'0:54'}
    ]},
    tw:{name:'Twitch',title:'Log in to Twitch',lib:'Channel VODs',badge:'TW',brand:'tw',email:'Username',pass:'Password',btn:'Log In',search:'Search',sub:'Log in to pick a VOD or clip for the pitch.',vids:[
      {title:'Co-stream · Derby night',file:'fb_crowd.jpg',meta:'VOD · 1h 12m'},
      {title:'Tactics desk · half-time',file:'fb_host.jpg',meta:'VOD · 24m'},
      {title:'Stadium cam · goals only',file:'fb_stadium.jpg',meta:'VOD · 11m'}
    ]}
  };
  function waParseUrl(u){
    var s=String(u||'').trim(), host=s;
    if(host.indexOf('https://')===0) host=host.slice(8);
    else if(host.indexOf('http://')===0) host=host.slice(7);
    host=host.split('/')[0]||'Video';
    if(host.indexOf('www.')===0) host=host.slice(4);
    var file=/youtu|youtube/i.test(s)?'fb_stadium.jpg':/twitch/i.test(s)?'fb_crowd.jpg':'fb_host.jpg';
    var badge=/youtu|youtube/i.test(s)?'YT':/faceb|fb\.com/i.test(s)?'FB':/insta/i.test(s)?'IG':/twitch/i.test(s)?'TW':'URL';
    return {title:host+' · Watch-Along',file:file,badge:badge,url:s};
  }
  function waStart(src){
    SFLwaSrc=src||SFLwaSrc||{title:'Watch-Along',file:'fb_stadium.jpg',badge:'WATCH'};
    cleanTo('watchlive', /^GL-WA-/);
    sflToast('▶ Watch-Along started · synced');
  }
  function applyWaApp(root){
    var app=WAAPPS[SFLwaApp]||WAAPPS.yt;
    var isLib=!!root.querySelector('#wa-lib');
    [].forEach.call(root.querySelectorAll('.waapp'),function(el){ el.className='waapp '+SFLwaApp; });
    var t=root.querySelector('.watit'); if(t) t.textContent=isLib?app.lib:app.title;
    var sub=root.querySelector('.wa-sub'); if(sub) sub.textContent=app.sub;
    var br=root.querySelector('.wabrand'); if(br) br.textContent=app.brand;
    var elab=root.querySelector('.wa-email-lab'); if(elab) elab.textContent=app.email;
    var plab=root.querySelector('.wa-pass-lab'); if(plab) plab.textContent=app.pass;
    var btn=root.querySelector('[data-wa="signin"]'); if(btn) btn.textContent=app.btn;
    var host=root.querySelector('#wa-vids');
    if(host){
      host.innerHTML='<div class="wasearch">'+app.search+'</div>'+app.vids.map(function(v,i){
        return '<div class="wavrow" data-wavid="'+i+'"><div class="wavth"></div><div><div class="wavn">'+v.title+'</div><div class="wavm">'+v.meta+'</div></div></div>';
      }).join('');
      [].forEach.call(host.querySelectorAll('.wavrow'),function(row,i){
        var vid=app.vids[i], th=row.querySelector('.wavth');
        if(vid&&th) th.style.backgroundImage='url("assets/'+vid.file+'")';
      });
    }
  }
  function applyWaClip(m){
    var c=SFLwaSrc||WACLIPS[SFLwaClip]||WACLIPS.goals;
    var v=m.querySelector('.wavid'); if(!v)return;
    var vn='--img-'+(c.file||'fb_stadium.jpg').replace(/[^a-zA-Z0-9]/g,'_');
    v.style.backgroundImage='var('+vn+'), url("assets/'+(c.file||'fb_stadium.jpg')+'")';
    var t=v.querySelector('.watitle'); if(t)t.textContent=c.title||'Watch-Along';
    var b=v.querySelector('.wabadge'); if(b) b.textContent=c.badge||'WATCH';
    if(!v.querySelector('.waplay')){ var p=document.createElement('div'); p.className='waplay'; p.textContent='▶'; v.appendChild(p); }
    var bar=v.querySelector('.wabar i');
    if(bar){ bar.style.width='8%'; var n=8; if(window._sflwabar)clearInterval(window._sflwabar); window._sflwabar=setInterval(function(){ n=Math.min(92,n+1.2); bar.style.width=n+'%'; if(n>=92){clearInterval(window._sflwabar);window._sflwabar=null;} }, 220); }
  }
  function applyWaSize(m){
    var v=m.querySelector('.wavid'); if(!v)return;
    v.classList.remove('sm','full');
    if(SFLwaSize==='sm')v.classList.add('sm');
    if(SFLwaSize==='full')v.classList.add('full');
    [].forEach.call(v.querySelectorAll('.wasz'),function(b){ b.classList.toggle('on',b.getAttribute('data-sz')===SFLwaSize); });
  }
  function chKey(n){ return String(n||'').toLowerCase().replace(/\s+/g,''); }
  function isRoomMgr(){ return SFLliveRole==='manager'||SFLliveRole==='cohost'||!!(SFLcoHosts&&SFLcoHosts.you); }
  function isLiveHost(){ return SFLliveRole==='host'; }
  function isLiveStaff(){ return isLiveHost()||isRoomMgr(); }
  function mgrCount(){ return Object.keys(SFLcoHosts||{}).length; }
  function chIsMgrKind(k){ return k==='cohost'||k==='manager'; }
  function sflLeaveLive(){ SFLseated=false; goTo('live'); }
  function takeSeatSkip(){ SFLseated=true; goTo(isRoomMgr()?'cohostroom':'fanseated'); }
  function showQuestionTimer(nm){
    var phone=document.getElementById('scaler').firstElementChild.querySelector('.phone'); if(!phone)return;
    var old=phone.querySelector('.qztimer'); if(old){ if(old._iv)clearInterval(old._iv); old.remove(); }
    var w=document.createElement('div'); w.className='qztimer'; w._sec=30;
    w.style.cssText='position:absolute;right:14px;top:104px;z-index:60;width:66px;text-align:center;cursor:pointer;font-family:Manrope,-apple-system,sans-serif';
    w.innerHTML='<div class="qzr" style="width:56px;height:56px;border-radius:50%;margin:0 auto;background:rgba(6,14,9,.85);border:2px solid #C9FF3D;box-shadow:0 0 14px rgba(201,255,61,.45),0 6px 14px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center"><span class="qzt" style="font-size:15px;font-weight:900;color:#C9FF3D;font-variant-numeric:tabular-nums">0:30</span></div><div style="font-size:8px;font-weight:800;color:rgba(255,255,255,.72);text-transform:uppercase;margin-top:3px;letter-spacing:.3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+(nm.split(" ")[0])+' · tap +</div>';
    phone.appendChild(w);
    function fmt(s){ return Math.floor(s/60)+':'+((s%60)<10?'0':'')+(s%60); }
    function rn(){ var t=w.querySelector('.qzt'); var r=w.querySelector('.qzr'); var c=(w._sec<=5)?'#FF3B5F':'#C9FF3D'; if(t){ t.textContent=fmt(w._sec); t.style.color=c; } if(r){ r.style.borderColor=c; } }
    w.addEventListener('click',function(e){ e.stopPropagation(); w._sec+=15; rn(); if(typeof sflToast==='function')sflToast('+15s · '+fmt(w._sec)); });
    w._iv=setInterval(function(){ w._sec--; if(w._sec<=0){ clearInterval(w._iv); w.remove(); if(typeof sflToast==='function')sflToast('Time up'); return; } rn(); },1000);
  }
  function _qaPhone(){ return document.getElementById('scaler').firstElementChild.querySelector('.phone'); }
  function showAskCompose(nm){
    var phone=_qaPhone(); if(!phone)return; var old=phone.querySelector('.sflask'); if(old){if(old._iv)clearInterval(old._iv);old.remove();}
    if(!document.getElementById('sflqa-css')){ var _st=document.createElement('style'); _st.id='sflqa-css'; _st.textContent='@keyframes sflqawob{0%,100%{transform:rotate(-9deg)}50%{transform:rotate(9deg)}}@keyframes sflqapulse{0%,100%{box-shadow:0 10px 24px rgba(143,212,0,.5)}50%{box-shadow:0 10px 30px rgba(201,255,61,.85)}}.sflqa-fab .sflqa-fab-btn{animation:sflqawob .5s ease-in-out infinite,sflqapulse 1s ease-in-out infinite;transform-origin:50% 60%}'; document.head.appendChild(_st); }
    var w=document.createElement('div'); w.className='sflask';
    w.style.cssText='position:absolute;inset:0;z-index:80;display:flex;align-items:center;justify-content:center;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);font-family:Manrope,-apple-system,sans-serif';
    var card=document.createElement('div'); card.className='sflask-card';
    card.style.cssText='width:84%;max-width:308px;background:linear-gradient(180deg,#1b2233,#12151d);border:1.5px solid rgba(201,255,61,.4);border-radius:20px;padding:18px;box-shadow:0 30px 70px rgba(0,0,0,.6)';
    w.appendChild(card); phone.appendChild(w);
    function fmt(s){ return Math.floor(s/60)+':'+((s%60)<10?'0':'')+(s%60); }
    function head(sub){ return '<div style="display:flex;align-items:center;gap:10px;margin-bottom:13px"><div style="width:36px;height:36px;border-radius:11px;flex:none;background:radial-gradient(circle at 40% 30%,#DCFF8A,#7BC900);display:flex;align-items:center;justify-content:center;font-size:18px">❓</div><div style="flex:1;min-width:0"><div style="font-size:15px;font-weight:800;color:#fff">'+nm+'</div><div style="font-size:11px;font-weight:650;color:#8892A4">'+sub+'</div></div><span class="qa-tmr" style="font-size:16px;font-weight:900;color:#C9FF3D;font-variant-numeric:tabular-nums;display:none"></span></div>'; }
    // STATE 1 — compose
    card.innerHTML=head('Ask a question · everyone sees it')
      +'<div class="sflask-in qa-ce" contenteditable="true" data-ph="Type your question…" style="min-height:60px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:13px;padding:11px 13px;font-size:14px;font-weight:600;color:#fff;outline:none"></div>'
      +'<div style="display:flex;gap:9px;margin-top:14px"><div class="sflask-cancel" style="flex:1;text-align:center;padding:12px;border-radius:12px;background:rgba(255,255,255,.08);color:#C9D0DC;font-weight:800;font-size:13.5px;cursor:pointer">Cancel</div><div class="sflask-send" style="flex:1.5;text-align:center;padding:12px;border-radius:12px;background:linear-gradient(140deg,#C9FF3D,#8FD400);color:#10140A;font-weight:800;font-size:13.5px;cursor:pointer">Send Question</div></div>';
    setTimeout(function(){try{card.querySelector('.sflask-in').focus();}catch(e){}},60);
    // STATE 2 — same card shows question + answer field
    function toQA(q){
      if(typeof pushComment==='function') pushComment('❓ <b style="color:#DCFF8A">You</b> asked <b style="color:#FFE1A0">'+nm+'</b>: '+q,'askmsg');
      w._qa=true;
      card.innerHTML=head('is answering… 30s')
        +'<div style="font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:#C9FF3D;margin-bottom:5px">Question</div>'
        +'<div style="font-size:14px;font-weight:750;color:#EAEEF5;line-height:1.4;margin-bottom:13px">'+q+'</div>'
        +'<div class="sflqa-ansrow" style="display:flex;gap:8px;align-items:center"><div class="sflqa-in qa-ce" contenteditable="true" data-ph="'+nm+', type your answer…" style="flex:1;min-height:20px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:11px;padding:10px 12px;font-size:13px;font-weight:600;color:#fff;outline:none"></div><div class="sflqa-send" style="width:42px;height:42px;flex:none;border-radius:11px;background:linear-gradient(140deg,#C9FF3D,#8FD400);color:#10140A;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;cursor:pointer">➤</div></div>'
        +'<div class="sflqa-hint" style="font-size:10px;font-weight:700;color:#8892A4;text-align:center;margin-top:11px">Tap outside to minimise · answer later</div>';
      var tmr=card.querySelector('.qa-tmr'); if(tmr)tmr.style.display='';
      var inp=card.querySelector('.sflqa-in'); setTimeout(function(){try{inp.focus();}catch(e){}},70);
      w._sec=30; function rt(){ if(tmr){ tmr.textContent=fmt(w._sec); tmr.style.color=w._sec<=5?'#FF3B5F':'#C9FF3D'; } if(w._fab){ var ft=w._fab.querySelector('.sflqa-fabtmr'); if(ft){ ft.textContent=fmt(w._sec); ft.style.color=w._sec<=5?'#FF3B5F':'#10140A'; } } } rt();
      function restore(){ if(w._fab){ w._fab.remove(); w._fab=null; } card.style.display=''; w.style.background='rgba(4,6,10,.55)'; w.style.backdropFilter='blur(3px)'; w.style.webkitBackdropFilter='blur(3px)'; w.style.pointerEvents=''; }
      function minimize(){ if(w._fab)return; card.style.display='none'; w.style.background='transparent'; w.style.backdropFilter='none'; w.style.webkitBackdropFilter='none'; w.style.pointerEvents='none';
        var fab=document.createElement('div'); fab.className='sflqa-fab'; fab.style.cssText='position:absolute;right:12px;top:42%;z-index:82;pointer-events:auto;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:6px';
        fab.innerHTML='<div class="sflqa-fab-btn" style="position:relative;width:56px;height:56px;border-radius:17px;background:linear-gradient(140deg,#C9FF3D,#8FD400);display:flex;align-items:center;justify-content:center;font-size:26px">❓<span class="sflqa-fabtmr" style="position:absolute;bottom:-7px;right:-7px;background:#10140A;color:#C9FF3D;font-size:9px;font-weight:900;padding:2px 5px;border-radius:8px;font-variant-numeric:tabular-nums">'+fmt(w._sec)+'</span></div><div style="font-size:9.5px;font-weight:800;color:#10140A;background:#C9FF3D;padding:3px 9px;border-radius:9px;white-space:nowrap;box-shadow:0 5px 14px rgba(0,0,0,.35)">Answer a question</div>';
        fab.addEventListener('click',function(e){ e.stopPropagation(); restore(); });
        w.appendChild(fab); w._fab=fab; }
      w._min=minimize;
      function ans(a){ if(w._iv)clearInterval(w._iv); restore(); w._qa=false; if(typeof pushComment==='function') pushComment('💬 <b style="color:#FFE1A0">'+nm+'</b> answered: '+a,'askmsg');
        card.innerHTML=head('answered')+'<div style="font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:#C9FF3D;margin-bottom:5px">Question</div><div style="font-size:13.5px;font-weight:700;color:#EAEEF5;margin-bottom:12px">'+q+'</div><div style="font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;color:#8FD400;margin-bottom:5px">Answer</div><div style="font-size:14px;font-weight:750;color:#DCFF8A">'+a+'</div>';
        setTimeout(function(){ if(w.parentNode)w.remove(); },2600); }
      inp.addEventListener('keydown',function(e){ if(e.key==='Enter'){ e.preventDefault(); var a=(inp.textContent||'').trim(); if(a)ans(a); } });
      card.querySelector('.sflqa-send').addEventListener('click',function(e){ e.stopPropagation(); var a=(inp.textContent||'').trim()||'Reds all the way! 🔴'; ans(a); });
      w._iv=setInterval(function(){ w._sec--; rt(); if(w._sec<=0){ clearInterval(w._iv); ans('(no answer — time up)'); } },1000);
    }
    w.addEventListener('click',function(e){ e.stopPropagation();
      if(e.target.closest('.sflqa-fab')) return;
      if(e.target.closest('.sflask-cancel')){ w.remove(); return; }
      if(e.target.closest('.sflask-send')){ var q=(card.querySelector('.sflask-in').textContent||'').trim()||"What's your call this half?"; toQA(q); return; }
      if(w._qa && w._min && !e.target.closest('.sflask-card')){ w._min(); return; } });
  }
  var SFLkicked=false;
  function showKickedNotice(){
    var phone=_qaPhone(); if(!phone)return; var old=phone.querySelector('.sflkick'); if(old)old.remove();
    var w=document.createElement('div'); w.className='sflkick';
    w.style.cssText='position:absolute;inset:0;z-index:90;display:flex;align-items:center;justify-content:center;background:rgba(4,6,10,.82);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);font-family:Manrope,-apple-system,sans-serif';
    w.innerHTML='<div style="width:82%;max-width:300px;text-align:center;background:linear-gradient(180deg,#241016,#160a0d);border:1px solid rgba(228,54,43,.5);border-radius:20px;padding:24px 20px;box-shadow:0 30px 70px rgba(0,0,0,.6)">'
      +'<div style="width:58px;height:58px;border-radius:50%;margin:0 auto 14px;background:rgba(228,54,43,.16);border:1px solid rgba(228,54,43,.5);display:flex;align-items:center;justify-content:center;font-size:28px">🚫</div>'
      +'<div style="font-size:18px;font-weight:800;color:#fff">You have been removed</div>'
      +'<div style="font-size:13px;font-weight:600;color:#C9A0A6;margin-top:8px;line-height:1.5">The host removed you from <b style="color:#fff">Matchday Warm-Up</b>. You cannot rejoin this live session.</div>'
      +'<div class="sflkick-ok" style="margin-top:18px;padding:13px;border-radius:13px;background:linear-gradient(140deg,#C9FF3D,#8FD400);color:#10140A;font-weight:800;font-size:14px;cursor:pointer">Back to Stadium</div></div>';
    phone.appendChild(w);
    w.addEventListener('click',function(e){ e.stopPropagation(); if(e.target.closest('.sflkick-ok')||e.target===w){ w.remove(); goTo('live'); } });
  }
  function showInviteSheet(pos){
    var phone=_qaPhone(); if(!phone)return; var old=phone.querySelector('.sflinvwrap'); if(old)old.remove();
    var w=document.createElement('div'); w.className='sflinvwrap';
    w.style.cssText='position:absolute;inset:0;z-index:80;display:flex;align-items:flex-end;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);font-family:Manrope,-apple-system,sans-serif';
    w.innerHTML='<div style="width:100%;background:linear-gradient(180deg,#1b2233,#12151d);border-top-left-radius:22px;border-top-right-radius:22px;padding:16px 18px 26px;box-shadow:0 -20px 50px rgba(0,0,0,.5)">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:rgba(255,255,255,.2);margin:0 auto 14px"></div>'
      +'<div style="font-size:17px;font-weight:800;color:#fff">Invite a fan to '+pos+'</div>'
      +'<div style="font-size:12px;font-weight:650;color:#8892A4;margin-top:3px">Send an invite — the fan accepts to take '+pos+'. You stay Host (#1).</div>'
      +'<div class="inv-opt" data-inv="link" style="display:flex;align-items:center;gap:12px;margin-top:14px;padding:13px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);cursor:pointer"><div style="font-size:20px">🔗</div><div style="flex:1"><div style="font-size:14px;font-weight:800;color:#fff">Share invite link</div><div style="font-size:11px;color:#8892A4">Share to WhatsApp, Instagram, Facebook…</div></div></div>'
      +'<div class="inv-opt" data-inv="fans" style="display:flex;align-items:center;gap:12px;margin-top:9px;padding:13px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);cursor:pointer"><div style="font-size:20px">👥</div><div style="flex:1"><div style="font-size:14px;font-weight:800;color:#fff">Invite your club fans</div><div style="font-size:11px;color:#8892A4">Copy link & post in your club chat</div></div></div>'
      +'<div class="inv-cancel" style="text-align:center;margin-top:16px;font-size:13px;font-weight:800;color:#8892A4;cursor:pointer">Cancel</div></div>';
    phone.appendChild(w);
    w.addEventListener('click',function(e){ e.stopPropagation();
      if(e.target===w||e.target.closest('.inv-cancel')){ w.remove(); return; }
      var _io=e.target.closest('.inv-opt'); if(_io){ var _k=_io.getAttribute('data-inv'); w.remove(); if(_k==='fans'){ sflToast('🔗 Invite link copied — post it in your club chat'); goTo('clubchat'); } else { showShareSheet(pos); } return; } });
  }
  function showShareSheet(pos){
    var phone=_qaPhone(); if(!phone)return; var old=phone.querySelector('.sflshare'); if(old)old.remove();
    var w=document.createElement('div'); w.className='sflshare';
    w.style.cssText='position:absolute;inset:0;z-index:82;display:flex;align-items:flex-end;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);font-family:Manrope,-apple-system,sans-serif';
    function app(k,ic,c){ return '<div class="sh-app" data-app="'+k+'" style="flex:1;text-align:center;cursor:pointer"><div style="width:54px;height:54px;margin:0 auto;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:26px;background:'+c+'">'+ic+'</div><div style="font-size:10px;font-weight:750;color:#C9D0DC;margin-top:6px">'+k+'</div></div>'; }
    w.innerHTML='<div style="width:100%;background:linear-gradient(180deg,#1b2233,#12151d);border-top-left-radius:22px;border-top-right-radius:22px;padding:16px 18px 26px;box-shadow:0 -20px 50px rgba(0,0,0,.5)">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:rgba(255,255,255,.2);margin:0 auto 14px"></div>'
      +'<div style="font-size:16px;font-weight:800;color:#fff">Share invite link · '+pos+'</div>'
      +'<div style="font-size:12px;font-weight:650;color:#8892A4;margin-top:3px">sfl.live/join/redfury-'+pos.toLowerCase()+'</div>'
      +'<div style="display:flex;gap:8px;margin-top:16px">'+app('WhatsApp','💬','#1FAF54')+app('Instagram','📸','linear-gradient(140deg,#F58529,#DD2A7B,#8134AF)')+app('Facebook','f','#1877F2')+app('Copy','🔗','rgba(255,255,255,.1)')+'</div>'
      +'<div class="sh-done" style="text-align:center;margin-top:18px;padding:12px;border-radius:12px;background:linear-gradient(140deg,#C9FF3D,#8FD400);color:#10140A;font-weight:800;font-size:14px;cursor:pointer">Done · continue live</div></div>';
    phone.appendChild(w);
    w.addEventListener('click',function(e){ e.stopPropagation();
      if(e.target===w||e.target.closest('.sh-done')){ w.remove(); sflToast('✓ Invite shared — back to your live'); return; }
      var a=e.target.closest('.sh-app'); if(a){ var k=a.getAttribute('data-app'); w.remove(); sflToast(k==='Copy'?'🔗 Link copied':('✓ Invite shared via '+k)); return; } });
  }
  function showAudienceSheet(){
    var phone=_qaPhone(); if(!phone)return; var old=phone.querySelector('.sflaud'); if(old)old.remove();
    var AUD=[['TifoKing','pa_h_01'],['Deni','pa_h_03'],['MartaSilva','pa_h_05'],['Zico','pa_h_06'],['PitchZed','pa_h_04'],['SamRed','pa_h_02'],['GoalHawk','pa_h_01']];
    var CLUB=[['Lucia','pa_h_01'],['Kojo','pa_h_03'],['Sara','pa_h_05'],['GloveBoy','pa_h_04'],['Nadia','pa_h_06']];
    function rows(arr,tag){ return arr.map(function(p){ return '<div style="display:flex;align-items:center;gap:11px;padding:10px 2px;border-bottom:1px solid rgba(255,255,255,.06)"><div style="width:38px;height:38px;border-radius:50%;flex:none;background:url(\\\'assets/'+p[1]+'.png\\\') center/cover"></div><div style="flex:1"><div style="font-size:13.5px;font-weight:800;color:#fff">'+p[0]+'</div><div style="font-size:11px;color:#8892A4">'+tag+'</div></div><div class="aud-msg" style="font-size:11px;font-weight:800;color:#C9FF3D;cursor:pointer">Message</div></div>'; }).join(''); }
    function tab(k,l,on){ return '<div class="aud-tab" data-tab="'+k+'" style="flex:1;text-align:center;padding:9px;border-radius:11px;font-size:12.5px;font-weight:800;cursor:pointer;background:'+(on?'#C9FF3D':'rgba(255,255,255,.08)')+';color:'+(on?'#10140A':'#C9D0DC')+'">'+l+'</div>'; }
    var w=document.createElement('div'); w.className='sflaud';
    w.style.cssText='position:absolute;inset:0;z-index:82;display:flex;align-items:flex-end;background:rgba(4,6,10,.55);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);font-family:Manrope,-apple-system,sans-serif';
    w.innerHTML='<div style="width:100%;max-height:74%;display:flex;flex-direction:column;background:linear-gradient(180deg,#1b2233,#12151d);border-top-left-radius:22px;border-top-right-radius:22px;padding:16px 18px 22px;box-shadow:0 -20px 50px rgba(0,0,0,.5)">'
      +'<div style="width:38px;height:4px;border-radius:2px;background:rgba(255,255,255,.2);margin:0 auto 12px;flex:none"></div>'
      +'<div style="font-size:16px;font-weight:800;color:#fff;margin-bottom:12px;flex:none">In this live · '+(AUD.length+CLUB.length)+'</div>'
      +'<div style="display:flex;gap:8px;margin-bottom:6px;flex:none">'+tab('aud','Audience · '+AUD.length,true)+tab('club','Club members · '+CLUB.length,false)+'</div>'
      +'<div class="aud-list" style="flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch">'+rows(AUD,'Viewer')+'</div>'
      +'</div>';
    phone.appendChild(w);
    w.addEventListener('click',function(e){ e.stopPropagation();
      if(e.target===w){ w.remove(); return; }
      var tb=e.target.closest('.aud-tab'); if(tb){ [].forEach.call(w.querySelectorAll('.aud-tab'),function(x){x.style.background='rgba(255,255,255,.08)';x.style.color='#C9D0DC';}); tb.style.background='#C9FF3D'; tb.style.color='#10140A'; var k=tb.getAttribute('data-tab'); w.querySelector('.aud-list').innerHTML=(k==='club')?rows(CLUB,'Red Fury FC'):rows(AUD,'Viewer'); return; }
      if(e.target.closest('.aud-msg')){ w.remove(); goTo('chatthread'); return; } });
  }
  function takeSeatHere(seat){ if(!seat)return; var pos=((seat.querySelector('.pos')||{}).textContent||'').trim(); seat.classList.remove('open','pulse'); seat.classList.add('you','spk'); var av=seat.querySelector('.av'); if(av){ av.textContent=''; av.style.backgroundImage="url('assets/pa_h_06.png')"; } var nm=seat.querySelector('.nm'); if(nm){ nm.textContent='You'; nm.style.color='var(--gold2)'; } var p=seat.querySelector('.pos'); if(p){ p.style.background='var(--gold1)'; p.style.color='#5A3E00'; } seat.style.opacity=''; SFLseated=true; if(typeof pushComment==='function') pushComment('✓ <b style="color:#DCFF8A">You</b> took '+pos+' — request accepted ⚡','join'); sflToast('✓ Host accepted — you are on '+pos); }
  function requestSeat(seat){ if(!seat||!seat.classList.contains('open'))return; var pos=((seat.querySelector('.pos')||{}).textContent||'').trim(); var av=seat.querySelector('.av'); if(av)av.textContent='⏳'; seat.style.opacity='.65'; sflToast('⏳ Request sent to host — '+pos); if(typeof pushComment==='function') pushComment('<b style="color:#DCFF8A">You</b> requested '+pos+' · waiting for host ✋','join'); setTimeout(function(){ if(!seat.parentNode)return; sflToast('The host is reviewing your request…'); },900); setTimeout(function(){ if(!seat.parentNode)return; if(av)av.textContent=''; takeSeatHere(seat); },2000); }
  function chatInviteName(el){
    if(!el) return '';
    var b=el.querySelector('b'); if(b) return (b.textContent||'').trim();
    var tx=(el.textContent||'').replace(/^\s*[⚡👑👔▶]+/,'').trim();
    var m=tx.match(/^([A-Za-z][A-Za-z0-9._ ]{1,24}?)(?:\s+joined|\s+took|\s+is\b)/);
    return m?m[1].trim():'';
  }
  function inviteOntoSeat(name, av){
    name=(name||'').trim(); if(!name||/^you$/i.test(name)) { sflToast('Pick a commenter to invite'); return; }
    var root=document.getElementById('scaler').firstElementChild; if(!root) return;
    var open=root.querySelector('.formfield .seat.open');
    if(!open){ sflToast('No open seats to invite onto'); return; }
    var pos=((open.querySelector('.pos')||{}).textContent||'RW').trim();
    open.classList.remove('open','pulse');
    var avEl=open.querySelector('.av'); if(avEl){ avEl.textContent=''; avEl.style.backgroundImage='url("assets/'+(av||'up_12.png')+'")'; }
    var nm=open.querySelector('.nm'); if(nm) nm.textContent=name;
    if(typeof decorateSeatMics==='function') decorateSeatMics(root);
    if(typeof applyLiveStaff==='function') applyLiveStaff(root);
    if(typeof pushComment==='function') pushComment('⚡ '+name+' took '+pos+' · invited','join');
    sflToast(name+' invited onto '+pos);
  }
  function kickFromSeat(seat, name){
    if(!seat||seat.classList.contains('open')||seat.classList.contains('you')) return;
    seat.classList.add('open'); seat.classList.remove('spk');
    var av=seat.querySelector('.av'); if(av){ av.textContent='＋'; av.style.backgroundImage=''; }
    var nm=seat.querySelector('.nm'); if(nm) nm.textContent='Open';
    var mi=seat.querySelector('.micind'); if(mi) mi.remove();
    var bd=seat.querySelector('.chbadge'); if(bd) bd.remove();
    sflToast((name||'Guest')+' removed from the pitch');
  }
  function chLiveRoom(){ return isRoomMgr()?'cohostroom':(SFLseated?'fanseated':'liveroom'); }
  function chQueue(item){
    item.id=item.id||(item.kind+'-'+chKey(item.name)+'-'+(item.pos||''));
    if(SFLjoinQ.some(function(q){ return q.id===item.id; })) return;
    SFLjoinQ.push(item);
  }
  function chDrop(id){ SFLjoinQ=SFLjoinQ.filter(function(q){ return q.id!==id; }); }
  function chToggle(name){
    var k=chKey(name); if(!k||(k==='you'&&SFLliveRole==='host')) return;
    if(!isLiveHost()){ sflToast('Only the host can appoint managers'); return; }
    if(SFLcoHosts[k]){ delete SFLcoHosts[k]; if(k==='you') SFLliveRole='viewer'; sflToast(name+' is no longer a room manager'); }
    else {
      if(mgrCount()>=4){ sflToast('Max 4 managers on this live'); return; }
      SFLcoHosts[k]=1; sflToast(name+' is now a room manager · this live only');
    }
    var m=document.getElementById('scaler').firstElementChild; if(m) applyLiveStaff(m);
  }
  function chDecide(id, ok){
    var q=null; for(var i=0;i<SFLjoinQ.length;i++) if(SFLjoinQ[i].id===id) q=SFLjoinQ[i];
    if(!q) return;
    var _fn=((VIEWS[curJ].screens[curS]||{}).fnum)||'';
    if(chIsMgrKind(q.kind)&&(isRoomMgr()||_fn==='GL-CH-C')&&!isLiveHost()){ sflToast('Only the host can appoint a manager'); return; }
    chDrop(id);
    var you=/^you/i.test(q.name);
    if(chIsMgrKind(q.kind)){
      if(ok){
        if(mgrCount()>=4 && !SFLcoHosts[chKey(q.name)]){ sflToast('Max 4 managers on this live'); return; }
        SFLcoHosts[chKey(q.name)]=1;
        if(you){ SFLchAsk='accepted'; SFLliveRole='manager'; sflToast('You are now a room manager'); goTo('cohostroom'); return; }
        sflToast(q.name+' is now a room manager');
      } else { if(you) SFLchAsk='denied'; sflToast(q.name+' manager request declined'); }
    } else {
      if(ok){ if(you){ sflToast('RW approved — you are on the pitch'); goTo('fanseated'); return; } sflToast(q.name+' approved · '+q.pos); }
      else { sflToast(q.name+' join declined'); }
    }
    var m=document.getElementById('scaler').firstElementChild; if(m) applyLiveStaff(m);
  }
  function applyLiveStaff(root){
    if(!root) return;
    var n=SFLjoinQ.length;
    [].forEach.call(root.querySelectorAll('.nbadge'),function(b){ b.textContent=String(n); b.classList.toggle('on',n>0); });
    var _fnStaff0=((VIEWS[curJ].screens[curS]||{}).fnum)||'';
    var showCo=_fnStaff0==='GL-03H'||_fnStaff0==='GL-WA-H'||_fnStaff0==='GL-CH-C'||_fnStaff0==='GL-05B'||_fnStaff0==='GL-03V'||_fnStaff0==='GL-WA-V';
    [].forEach.call(root.querySelectorAll('.formfield .seat'),function(seat){
      var nm=((seat.querySelector('.nm')||{}).textContent||'').trim();
      var on=showCo&&!!SFLcoHosts[chKey(nm)];
      var badge=seat.querySelector('.chbadge');
      if(on&&!badge){ badge=document.createElement('div'); badge.className='chbadge'; badge.textContent='MGR'; seat.appendChild(badge); }
      if(on&&badge) badge.textContent='MGR';
      if(!on&&badge) badge.remove();
    });
    var _fnStaff=((VIEWS[curJ].screens[curS]||{}).fnum)||'';
    var names=Object.keys(SFLcoHosts);
    var rtop=root.querySelector('.rtop');
    var exist=root.querySelector('#co-tile');
    var staffRoom=_fnStaff==='GL-03H'||_fnStaff==='GL-WA-H'||_fnStaff==='GL-CH-C';
    var ht=rtop&&rtop.querySelector('.hosttile');
    if(rtop&&ht&&names.length&&!exist&&staffRoom){
      var tile=document.createElement('div'); tile.id='co-tile'; tile.className='cotile';
      tile.style.backgroundImage='url("assets/up_07.png")';
      tile.innerHTML='<div class="cl">MGR</div>';
      ht.parentNode.insertBefore(tile, ht.nextSibling);
    }
    if(exist){
      if(!names.length||!staffRoom) exist.remove();
      else { var cl=exist.querySelector('.cl'); if(cl) cl.textContent='MGR'; }
    }
    var chip=root.querySelector('.rtop .rolechip');
    if(chip && (_fnStaff==='GL-03V'||_fnStaff==='GL-WA-V'||_fnStaff==='GL-05B'||_fnStaff==='GL-CH-C')){
      if(isRoomMgr()){ chip.className='rolechip manager'; chip.textContent='Manager'; }
    }
    var hintMeta=root.querySelector('.rt2 > .rmeta');
    if(hintMeta && /appoint you as a (room )?manager|mute\s*·\s*reset\s*·\s*remove/i.test(hintMeta.textContent||'')) hintMeta.remove();
    [].forEach.call(root.querySelectorAll('.chactlab'),function(lab){
      var who=lab.getAttribute('data-chname')||((root.querySelector('.seathead .nm')||{}).textContent||'Teo').split('·')[0].trim();
      lab.textContent=SFLcoHosts[chKey(who)]?'Remove Manager':'Make Manager';
    });
    var tab=SFLchTab||'join';
    [].forEach.call(root.querySelectorAll('[data-chtab]'),function(el){
      var k=el.getAttribute('data-chtab');
      el.classList.toggle('on', tab===k);
      var c=SFLjoinQ.filter(function(q){ return k==='cohost'?chIsMgrKind(q.kind):q.kind==='join'; }).length;
      el.textContent=(k==='cohost'?('Managers · '+mgrCount()+'/4'):'Waiting list')+(c?(' · '+c):'');
    });
    var hint=root.querySelector('#ch-hint');
    if(hint) hint.textContent=tab==='cohost'?'Host-only. Appoint up to 4 room managers for this live — not a club role. Managers skip seat approval later.':'People waiting to enter the pitch. Host or a room manager can accept or decline.';
    var list=root.querySelector('#ch-list');
    if(list){
      var hostDecides=isRoomMgr()||_fnStaff==='GL-CH-C';
      var rows=SFLjoinQ.filter(function(q){ return tab==='cohost'?chIsMgrKind(q.kind):q.kind==='join'; });
      if(!rows.length){ list.innerHTML='<div style="padding:22px 8px;text-align:center;font-size:13px;font-weight:700;color:#707786">'+(tab==='cohost'?'No manager requests':'No one waiting to join')+'</div>'; }
      else {
        list.innerHTML=rows.map(function(q){
          var kind=chIsMgrKind(q.kind)?'co':'join';
          var meta=chIsMgrKind(q.kind)?'Wants to be a room manager':'Wants '+q.pos+' on the pitch';
          var acts=(chIsMgrKind(q.kind)&&hostDecides&&!isLiveHost())
            ? '<div class="reqm">Host appoints managers</div>'
            : '<div class="reqok" data-chdec="ok">Accept</div><div class="reqno" data-chdec="no">Decline</div>';
          return '<div class="reqrow" data-chid="'+q.id+'"><div class="reqav" data-av="'+q.av+'"></div><div style="flex:1"><div class="reqn">'+q.name+' <span class="chkind '+kind+'">'+(chIsMgrKind(q.kind)?'Manager':'Join')+'</span></div><div class="reqm">'+meta+'</div></div><div class="reqacts">'+acts+'</div></div>';
        }).join('');
        [].forEach.call(list.querySelectorAll('.reqav[data-av]'),function(av){ av.style.backgroundImage='url("assets/'+av.getAttribute('data-av')+'")'; });
      }
    }
  }
  var SFLPLAYERS={
    rivera:{name:'A. Rivera',pos:'ST',club:'Northbridge FC',seller:'Blue Wolves FC',cr:'cr-blue',crL:'BW',val:420,move:'up',moveTxt:'▲ +30',trend:'▲ Rising',av:'pl_nobg_rivera.png',fig:'pl_nobg_rivera.png',next:'Sat · vs Coast City',listed:'2h ago · Blue Wolves FC',wdl:['w','d','w','l','w','w'],line:'15,70 62,66 110,50 158,52 205,34 253,20'},
    bello:{name:'T. Bello',pos:'CM',club:'Southgate United',seller:'Red District FC',cr:'cr-red',crL:'RD',val:310,move:'flat',moveTxt:'0',trend:'● Stable',av:'pl_nobg_bello.png',fig:'pl_nobg_bello.png',next:'Sun · vs Royal Athletic',listed:'5h ago · Red District FC',wdl:['d','w','l','d','w','d'],line:'15,48 62,52 110,58 158,50 205,46 253,50'},
    mensah:{name:'K. Mensah',pos:'LW',club:'Coast City',seller:'Greenfield FC',cr:'cr-green',crL:'GF',val:560,move:'up',moveTxt:'▲ +10',trend:'▲ Rising',av:'pl_nobg_mensah.png',fig:'pl_nobg_mensah.png',next:'Sat · vs Northbridge FC',listed:'1d ago · Greenfield FC',wdl:['w','w','d','w','l','w'],line:'15,62 62,54 110,50 158,44 205,48 253,36'},
    silva:{name:'M. Silva',pos:'GK',club:'Royal Athletic',seller:'Royal Lions FC',cr:'cr-gold',crL:'RL',val:340,move:'flat',moveTxt:'0',trend:'● Stable',av:'pl_nobg_silva.png',fig:'pl_nobg_silva.png',next:'Tue · vs Iron Valley',listed:'3h ago · Royal Lions FC',wdl:['l','w','d','w','d','d'],line:'15,56 62,60 110,52 158,54 205,50 253,52'}
  };
  function plExtra(name,pos,club,val,av,move){
    return {name:name,pos:pos,club:club,seller:'Red District FC',cr:'cr-red',crL:'RD',val:val,move:move||'flat',moveTxt:move==='up'?'▲ +30':move==='down'?'▼ −20':'0',trend:move==='up'?'▲ Rising':move==='down'?'▼ Falling':'● Stable',av:av,fig:av,next:'Sat · vs Coast City',listed:'In your squad',wdl:['w','d','w','l','w','d'],line:'15,56 62,52 110,50 158,48 205,46 253,44'};
  }
  SFLPLAYERS.okonkwo=plExtra('D. Okonkwo','CB','Iron Valley',410,'av_02.png','up');
  SFLPLAYERS.fernandez=plExtra('L. Fernández','CM','Coast City',440,'av_05.png','down');
  SFLPLAYERS.park=plExtra('J. Park','RW','Northbridge FC',560,'av_07.png','up');
  SFLPLAYERS.almeida=plExtra('T. Almeida','RB','Royal Athletic',280,'av_01.png','up');
  SFLPLAYERS.berg=plExtra('S. Berg','ST','Coast City',700,'av_09.png','up');
  SFLPLAYERS.costa=plExtra('R. Costa','LB','Iron Valley',300,'av_04.png');
  SFLPLAYERS.diallo=plExtra('N. Diallo','CDM','Northbridge FC',450,'av_06.png','up');
  SFLPLAYERS.obello=plExtra('O. Bello','CB','Coast City',330,'av_08.png','down');
  SFLPLAYERS.vlasic=plExtra('E. Vlašić','CF','Royal Athletic',620,'av_03.png','up');
  SFLPLAYERS.sanchez=plExtra('P. Sánchez','CAM','Iron Valley',540,'av_11.png','up');
  SFLPLAYERS.rossi=plExtra('G. Rossi','GK','Northbridge FC',240,'av_02.png');
  SFLPLAYERS.kante=plExtra('H. Kanté','CM','Coast City',470,'av_05.png','up');
  SFLPLAYERS.mendy=plExtra('F. Mendy','RM','Royal Athletic',390,'av_07.png','up');
  SFLPLAYERS.ibrahim=plExtra('Z. Ibrahim','LM','Iron Valley',300,'av_09.png','down');
  SFLPLAYERS.nkunku=plExtra('C. Nkunku','CF','Northbridge FC',660,'av_06.png','up');
  SFLPLAYERS.okoro=plExtra('Y. Okoro','CM','Harbor FC',450,'av_03.png','up');
  SFLPLAYERS.okoro.seller='Harbor City FC'; SFLPLAYERS.okoro.cr='cr-blue'; SFLPLAYERS.okoro.crL='HC';
  SFLPLAYERS.moretti=plExtra('L. Moretti','RW','Royal Athletic',560,'av_11.png','up');
  SFLPLAYERS.hassan=plExtra('A. Hassan','CB','Iron Valley',410,'av_08.png','flat');
  SFLPLAYERS.ike=plExtra('K. Ike','ST','Coast City',700,'av_09.png','up');
  SFLPLAYERS.nunez=plExtra('M. Núñez','GK','Southgate United',240,'av_02.png');
  var SFL_REC_POOL=['okoro','bello','moretti','hassan','ike','nunez'];
  function plFromEl(el){
    if(!el)return SFLpl||'rivera';
    var id=el.getAttribute('data-pl'); if(id&&SFLPLAYERS[id])return id;
    var tx=(el.textContent||'').toLowerCase();
    for(var k in SFLPLAYERS){ if(tx.indexOf((SFLPLAYERS[k].name||'').toLowerCase())>=0) return k; }
    return SFLpl||'rivera';
  }
  function plLoanFee(p){ return Math.max(20, Math.round(((p&&p.val)||400)*0.15/10)*10); }
  function plDutyCounts(){
    var sell=0,loan=0,buy=0,k;
    for(k in SFLplList){ if(SFLplList[k]==='loan')loan++; else if(SFLplList[k]==='transfer')sell++; }
    for(k in SFLplBought){ if(SFLplBought[k]) buy++; }
    return {sell:sell,buy:buy,t:sell,l:loan};
  }
  function plListedSellIds(){ var out=[],k; for(k in SFLplList){ if(SFLplList[k]==='transfer') out.push(k); } return out; }
  function plMatchRecs(){
    var listed=plListedSellIds(), pool=SFL_REC_POOL.slice(), recs=[];
    function pickFor(val){
      var best=null,bestD=1e9,bi=-1,i,p,d;
      for(i=0;i<pool.length;i++){
        p=SFLPLAYERS[pool[i]]; if(!p) continue;
        d=Math.abs((p.val||0)-val);
        if(d<bestD){bestD=d;best=pool[i];bi=i;}
      }
      if(bi>=0) pool.splice(bi,1);
      return best;
    }
    if(!listed.length) return ['okoro','bello'];
    listed.forEach(function(id){ var r=pickFor((SFLPLAYERS[id]||{}).val||400); if(r) recs.push(r); });
    while(recs.length<2){ var extra=pickFor(400); if(!extra) break; recs.push(extra); }
    return recs.slice(0,2);
  }
  function plMarkBuySellDuty(){
    var d=plDutyCounts();
    if(d.sell>=2&&d.buy>=2){ SFLdone['Buy & sell players']=1; sflToast('Weekly task complete · 2 listed + 2 buys'); return true; }
    return false;
  }
  function plRecordList(kind){
    var id=SFLpl||'rivera';
    if(SFLplList[id]&&SFLplList[id]!==kind){ sflToast('Unlist first to change type'); return false; }
    SFLplList[id]=kind;
    var d=plDutyCounts();
    if(kind==='transfer'){
      if(!plMarkBuySellDuty()){
        if(d.sell>=2) sflToast('2 listed · buy the 2 players to finish');
        else sflToast('Listed · sell '+Math.min(2,d.sell)+'/2 · you pick who to sell');
      }
    } else sflToast('Loan listed');
    if(window._sflploffer){clearTimeout(window._sflploffer);window._sflploffer=null;}
    window._sflploffer=setTimeout(function(){
      plQueueOffer(id,kind);
      if(((VIEWS[curJ].screens[curS]||{}).fnum)==='G-03') applyPlNotifs(mount);
      if(((VIEWS[curJ].screens[curS]||{}).fnum)==='G-03') applyTourn(mount);
    },1600);
    return true;
  }
  function plRecordBuy(id){
    id=id||SFLpl||'bello';
    SFLplBought[id]=1;
    if(!plMarkBuySellDuty()){
      var d=plDutyCounts();
      sflToast('Bought · buy '+Math.min(2,d.buy)+'/2');
    }
  }
  function plRecRowHtml(id, listedId){
    var p=SFLPLAYERS[id]||SFLPLAYERS.bello, src=SFLPLAYERS[listedId], bought=!!SFLplBought[id];
    var match=src?('Matched to '+src.name+' · '+p.val+' vs '+src.val):('Buy · '+p.val+' Coins');
    return '<div class="recrow" data-pl="'+id+'" data-plrec="'+id+'"><div class="pi" style="background-image:'+sflImg(p.av)+'"></div><div><div class="pn">'+p.name+'</div><div class="pp">'+p.pos+' · '+p.club+'</div><div class="rmatch">'+match+'</div></div><div class="side">'+(bought?'<div class="bought">✓ Bought</div>':'<div class="cv" style="display:flex;align-items:center;gap:4px;font-size:13px;font-weight:800;color:var(--goldDeep)"><div class="coin" style="width:15px;height:15px;font-size:8px">C</div>'+p.val+'</div>')+'</div></div>';
  }
  function plUnlist(){ var id=SFLpl||'rivera'; delete SFLplList[id]; sflToast('Player unlisted'); }
  function plQueueOffer(id,kind){
    id=id||SFLpl||'rivera'; kind=kind||'transfer';
    var i; for(i=0;i<SFLplOffers.length;i++){ if(SFLplOffers[i].id===id&&SFLplOffers[i].status==='pending') return; }
    var p=SFLPLAYERS[id]||SFLPLAYERS.rivera;
    SFLplOffers.unshift({id:id,kind:kind,buyer:kind==='loan'?'Luis Ortega':'Olivia S.',status:'pending'});
    sflToast((kind==='loan'?'Luis':'Olivia')+' wants your '+p.name+' · check Notifications');
  }
  function cmgrKey(n){ return String(n||'').toLowerCase().replace(/\s+/g,''); }
  function cmgrFind(id){ var i; for(i=0;i<SFLcmgrQ.length;i++){ if(SFLcmgrQ[i].id===id) return SFLcmgrQ[i]; } return null; }
  function cmgrUpsert(row){
    var e=cmgrFind(row.id);
    if(e){ e.kind=row.kind||e.kind; e.name=row.name||e.name; e.av=row.av||e.av; e.status=row.status||e.status; return e; }
    SFLcmgrQ.unshift({id:row.id,kind:row.kind||'ask',name:row.name||'Fan',av:row.av||'up_12.png',status:row.status||'pending'});
    return SFLcmgrQ[0];
  }
  function cmgrPending(kind){ var n=0,i; for(i=0;i<SFLcmgrQ.length;i++){ if(SFLcmgrQ[i].status==='pending'&&(!kind||SFLcmgrQ[i].kind===kind)) n++; } return n; }
  function cmgrMark(q){
    if(!q) return;
    SFLcmgrStaff[cmgrKey(q.name)]=true;
    if(/diego/i.test(q.name)) SFLcmgrStaff.diego=true;
    if(/priya/i.test(q.name)) SFLcmgrStaff.priya=true;
    if(/marco/i.test(q.name)) SFLcmgrStaff.marco=true;
    if(/lena/i.test(q.name)) SFLcmgrStaff.lena=true;
    if(/tom/i.test(q.name)) SFLcmgrStaff.tom=true;
  }
  function cmgrGrant(who){
    SFLmgrMode=true; SFLmember=true; SFLcmgrInvite='accepted'; SFLcmgrAsk='accepted';
    if(who) SFLcmgrStaff[who]=true;
    SFLcmgrStaff.you=true;
  }
  function applyCmgrPick(root){
    var p=SFLcmgrPick||{};
    var av=p.av||'up_11.png';
    [].forEach.call(root.querySelectorAll('#cm-av,.cm-av'),function(el){ el.style.backgroundImage='url("assets/'+av+'")'; });
    [].forEach.call(root.querySelectorAll('.cm-name'),function(el){ el.textContent=p.name||'Olivia M.'; });
    [].forEach.call(root.querySelectorAll('.cm-fid'),function(el){
      var fid=p.fid||'67890';
      el.textContent=/joined/i.test(el.textContent||'')?('ID '+fid+' · joined 12 Jul'):('ID '+fid+(p.lv?(' · Lv '+p.lv):''));
    });
    var lv=root.querySelector('.cm-lv'); if(lv) lv.textContent='Lv '+(p.lv||'9');
    var fv=root.querySelector('.cm-fv'); if(fv) fv.textContent='Fan Value '+(p.fv||'1,510');
    var nm=p.name||'Olivia M.';
    var sub=root.querySelector('.cm-sub'); if(sub) sub.textContent='Invite sent to '+nm+'. Stay here — you will see their decision on this screen.';
    var okt=root.querySelector('.cm-oktitle'); if(okt) okt.textContent=nm+' is now a manager';
    var oks=root.querySelector('.cm-oksub'); if(oks) oks.textContent='They accepted your invite. Fan stays permanent — Manager HQ is now on their profile too.';
    var title=root.querySelector('.sheet-title');
    if(title&&/Invite /.test(title.textContent||'')) title.textContent='Invite '+nm+' to manage Red Fury too?';
    var make=root.querySelector('[data-cmact="make"]');
    if(make){
      var id=p.id||'priya';
      if(SFLcmgrStaff[id]){ make.textContent='Already a manager'; make.classList.add('dis'); }
      else if(cmgrFind('inv-'+id)&&cmgrFind('inv-'+id).status==='pending'){ make.textContent='Invite pending'; make.classList.add('dis'); }
      else { make.textContent='Make Manager'; make.classList.remove('dis'); }
    }
    [].forEach.call(root.querySelectorAll('.fanrow'),function(r){
      var fid=r.getAttribute('data-fan'); if(!fid) return;
      var hold=r.querySelector('.fn')&&r.querySelector('.fn').parentElement;
      if(!hold) return;
      var pill=hold.querySelector('.mgrpill');
      if(SFLcmgrStaff[fid]){ if(!pill){ pill=document.createElement('span'); pill.className='mgrpill'; pill.textContent='MGR'; hold.appendChild(pill); } }
      else if(pill) pill.remove();
    });
  }
  function applyCmgrMember(root){
    var ask=root.querySelector('.cmgrask'), pend=root.querySelector('.cmgrpend');
    var locked=!!(SFLmgrMode||SFLcmgrAsk==='accepted'||SFLcmgrInvite==='accepted');
    var waiting=SFLcmgrAsk==='pending'||SFLcmgrInvite==='pending';
    if(ask) ask.style.display=(locked||waiting)?'none':'';
    if(pend){ pend.style.display=waiting?'':'none'; if(waiting) pend.textContent=SFLcmgrInvite==='pending'?'🕐 Manager invite waiting · accept it from Notifications':'🕐 Manager request pending · you will be notified'; }
  }
  function applyClubDetailMember(root){
    var hnav=root.querySelector('.hnav'); if(!hnav) return;
    var more=hnav.querySelector('.clubmore'), pill=hnav.querySelector('.sp-member-detail');
    if(SFLmember){
      if(!pill){
        pill=document.createElement('span');
        pill.className='pill sp-member sp-member-detail';
        pill.style.cssText='margin-left:auto;align-self:center';
        pill.textContent='✓ Member';
        if(more) hnav.insertBefore(pill, more);
        else hnav.appendChild(pill);
      }
      var apply=root.querySelector('.cta .btn.club');
      if(apply) apply.textContent='Enter Club Home';
    } else {
      if(pill) pill.remove();
      var apply2=root.querySelector('.cta .btn.club');
      if(apply2) apply2.textContent='Apply to Join';
    }
  }
  function applyCmgrQueue(root){
    var list=root.querySelector('#cm-list'); if(!list) return;
    var tab=SFLcmgrTab||'ask';
    [].forEach.call(root.querySelectorAll('[data-cmtab]'),function(el){ el.classList.toggle('on', el.getAttribute('data-cmtab')===tab); });
    var askn=root.querySelector('#cm-askn'), invn=root.querySelector('#cm-invn');
    if(askn) askn.textContent=String(cmgrPending('ask'));
    if(invn) invn.textContent=String(cmgrPending('invite'));
    var hint=root.querySelector('#cm-hint');
    if(hint) hint.textContent=tab==='invite'?'Invites you sent. The fan must accept before HQ unlocks.':'Fans who asked to become a manager. Accept or reject — they are notified either way.';
    var rows=SFLcmgrQ.filter(function(q){ return tab==='invite'?(q.kind==='invite'):(q.kind==='ask'); });
    if(!rows.length){ list.innerHTML='<div class="note info" style="margin-top:8px">Nothing in this list right now.</div>'; return; }
    list.innerHTML=rows.map(function(q){
      var acts=q.status==='pending'
        ? '<div class="cmacts"><div class="btn ghost sm" data-cmdec="reject">Decline</div><div class="btn sm" data-cmdec="accept">Accept</div></div>'
        : '<div class="cmkind '+(q.status==='accepted'?'invite':'ask')+'">'+(q.status==='accepted'?'Accepted':'Declined')+'</div>';
      var meta=q.kind==='invite'?'Invite sent · waiting on fan':'Asked to become a manager';
      if(q.status!=='pending') meta=(q.status==='accepted'?'Accepted · HQ unlocked':'Declined · fan notified');
      return '<div class="cmrow" data-cmid="'+q.id+'"><div class="cmav" data-av="'+q.av+'"></div><div style="flex:1"><div class="cmn">'+q.name+' <span class="cmkind '+q.kind+'">'+(q.kind==='invite'?'Invite':'Request')+'</span></div><div class="cmm">'+meta+'</div></div>'+acts+'</div>';
    }).join('');
    [].forEach.call(list.querySelectorAll('.cmav[data-av]'),function(el){ el.style.backgroundImage='url("assets/'+el.getAttribute('data-av')+'")'; });
  }
  function applyCmgrHqBadge(root){
    var b=root.querySelector('#cmgr-badge'); if(!b) return;
    var n=cmgrPending(); b.textContent=String(n||0); b.style.display=n?'':'none';
  }
  function applyCmgrNotifs(root){
    var host=root.querySelector('#n-today'); if(!host) return;
    [].forEach.call(root.querySelectorAll('[data-cmgr][data-dyn="1"]'),function(row){ row.remove(); });
    var row=root.querySelector('#n-cmgr-invite');
    if(!row){
      row=document.createElement('div');
      row.className='nrow'; row.id='n-cmgr-invite'; row.setAttribute('data-cmgr','invite');
      host.insertBefore(row, host.firstChild);
    } else if(row.parentNode===host){ host.insertBefore(row, host.firstChild); }
    var st=SFLcmgrInvite||'none';
    var body='', unread=true;
    if(st==='accepted'||SFLcmgrAsk==='accepted'){
      row.setAttribute('data-cmgr','yes');
      body='<div class="ni club">🛡️</div><div style="flex:1"><div class="nt">You are now a manager of Red Fury</div><div class="nsupport">You accepted · Manager HQ is on your profile</div><div class="nstatus ok">Accepted</div><div class="ntime">Just now</div></div>';
    } else if(st==='rejected'){
      row.setAttribute('data-cmgr','no');
      unread=false;
      body='<div class="ni live">✕</div><div style="flex:1"><div class="nt">You declined the manager invite</div><div class="nsupport">You stay a Fan of Red Fury</div><div class="nstatus no">Rejected</div><div class="ntime">Just now</div></div>';
    } else {
      row.setAttribute('data-cmgr','invite');
      body='<div class="ni club">🛡️</div><div style="flex:1"><div class="nt">Manager asked you to become a manager</div><div class="nsupport">Jay Malik · Red Fury · accept or reject</div><div class="nacts"><div class="nbtn ok" data-cmdec="accept">Accept</div><div class="nbtn no" data-cmdec="reject">Reject</div></div><div class="ntime">Just now</div></div>'+(unread?'<div class="unread"></div>':'');
    }
    row.innerHTML=body;
    function add(kind, icon, cls, title, sub, acts, un){
      var el=document.createElement('div');
      el.className='nrow'; el.setAttribute('data-cmgr',kind); el.setAttribute('data-dyn','1');
      el.innerHTML='<div class="ni '+cls+'">'+icon+'</div><div style="flex:1"><div class="nt">'+title+'</div><div class="nsupport">'+sub+'</div>'+(acts||'')+'<div class="ntime">Just now</div></div>'+(un?'<div class="unread"></div>':'');
      host.insertBefore(el, host.firstChild.nextSibling);
    }
    if(!SFLmgrMode && SFLcmgrAsk==='rejected' && st!=='rejected'){
      add('no','✕','live','Manager declined your request','You stay a Fan · you can ask again later','',true);
    }
    if(!SFLmgrMode && SFLcmgrAsk==='pending'){
      add('sent','🕐','acct','Manager request sent','Waiting for Jay Malik to accept or reject','',false);
    }
    if(SFLmgrMode && cmgrPending('ask')){
      add('inbox','🛡️','acct','A fan asked to become a manager','Open Co-managers to accept or reject','',true);
    }
  }
  function applyPlNotifs(root){
    var host=root.querySelector('#n-today'); if(!host)return;
    [].forEach.call(root.querySelectorAll('[data-ploffer]'),function(row){
      var id=row.getAttribute('data-ploffer'), o=null, i;
      for(i=0;i<SFLplOffers.length;i++){ if(SFLplOffers[i].id===id){o=SFLplOffers[i];break;} }
      if(!o||o.status==='pending')return;
      var acts=row.querySelector('.nacts'), unread=row.querySelector('.unread');
      if(acts) acts.innerHTML='<div class="nstatus '+(o.status==='approved'?'ok':'no')+'">'+(o.status==='approved'?'Approved':'Rejected · listing still live')+'</div>';
      if(unread) unread.remove();
    });
    SFLplOffers.forEach(function(o){
      if(root.querySelector('[data-ploffer="'+o.id+'"]')) return;
      var p=SFLPLAYERS[o.id]; if(!p)return;
      var fee=o.kind==='loan'?plLoanFee(p):p.val;
      var row=document.createElement('div');
      row.className='nrow'; row.setAttribute('data-ploffer',o.id); row.setAttribute('data-kind',o.kind); row.setAttribute('data-dyn','1');
      var acts=o.status==='pending'
        ?'<div class="nacts"><div class="nbtn ok" data-pldec="approve">Approve</div><div class="nbtn no" data-pldec="reject">Reject</div></div>'
        :'<div class="nacts"><div class="nstatus '+(o.status==='approved'?'ok':'no')+'">'+(o.status==='approved'?'Approved':'Rejected · listing still live')+'</div></div>';
      row.innerHTML='<div class="ni money">'+(o.kind==='loan'?'🕐':'⚽')+'</div><div style="flex:1"><div class="nt">'+o.buyer+' wants '+p.name+(o.kind==='loan'?' on loan':'')+'</div><div class="nsupport">'+(o.kind==='loan'?'Loan · '+fee+' Coins fee · '+SFLplLoan:'Transfer · '+fee+' Coins in escrow')+' · approve to complete</div>'+acts+'<div class="ntime">Just now</div></div>'+(o.status==='pending'?'<div class="unread"></div>':'');
      host.insertBefore(row,host.firstChild);
    });
  }
  function applyPlSquad(root){
    var d=plDutyCounts();
    var dt=root.querySelector('#pl-duty-t'), db=root.querySelector('#pl-duty-b');
    if(dt){ var n=dt.querySelector('.n'); if(n)n.textContent=Math.min(2,d.sell)+'/2'; dt.classList.toggle('ok',d.sell>=2); }
    if(db){ var n2=db.querySelector('.n'); if(n2)n2.textContent=Math.min(2,d.buy)+'/2'; db.classList.toggle('ok',d.buy>=2); }
    applyPlRecsBox(root);
    [].forEach.call(root.querySelectorAll('.prow'),function(r){
      var id=r.getAttribute('data-pl'), kind=id&&SFLplList[id], box=r.children[1], badge=r.querySelector('.listed');
      if(kind){ if(!badge&&box){ badge=document.createElement('span'); box.appendChild(badge); } if(badge){ badge.className='listed'+(kind==='loan'?' loan':''); badge.textContent=kind==='loan'?'● LOAN':'● TRANSFER'; } }
      else if(badge) badge.remove();
    });
    var tab=root.querySelector('.tabs i.on'); var mode=tab?(tab.getAttribute('data-pltab')||'all'):'all';
    [].forEach.call(root.querySelectorAll('.prow'),function(r){
      var kind=SFLplList[r.getAttribute('data-pl')||''];
      var show=mode==='avail'?!kind:mode==='listed'?!!kind:mode==='pending'?false:true;
      r.style.display=show?'':'none';
    });
  }
  function applyPlAction(root){
    var id=SFLpl||'rivera', kind=SFLplList[id], tip=root.querySelector('.tipnote');
    if(!kind) return;
    [].forEach.call(root.querySelectorAll('.actopt'),function(o){ o.style.display='none'; });
    var host=root.querySelector('.sheet');
    if(host&&!host.querySelector('[data-plact="unlist"]')){
      var u=document.createElement('div'); u.className='actopt'; u.setAttribute('data-plact','unlist');
      u.innerHTML='<div class="ai" style="background:#FFF5F4;color:#E4362B">✕</div><div><div class="at">Unlist this '+(kind==='loan'?'loan':'transfer')+'</div><div class="ad">Remove from the Transfer Market</div></div><div class="chev">›</div>';
      var cta=host.querySelector('.cta'); if(cta) host.insertBefore(u,cta); else host.appendChild(u);
    }
    if(tip) tip.textContent='Already listed for '+(kind==='loan'?'loan':'transfer')+'. Unlist first if you want the other type.';
  }
  function applyPlLoan(root){
    var p=SFLPLAYERS[SFLpl]||SFLPLAYERS.rivera, fee=plLoanFee(p);
    setBalKey(root,'loan fee',fee+' Coins');
    setBalKey(root,'term',SFLplLoan+(SFLplLoan==='1 week'?' · returns 27 Aug':SFLplLoan==='1 season'?' · until 31 May':' · next fixture'));
    [].forEach.call(root.querySelectorAll('.durchip'),function(c){ c.classList.toggle('on',(c.getAttribute('data-loan')||'')===SFLplLoan); });
    [].forEach.call(root.querySelectorAll('.btn'),function(b){ if(/list loan/i.test(b.textContent||'')) b.textContent='List loan · '+fee+' Coins'; });
    [].forEach.call(root.querySelectorAll('.revealcard .rn .t'),function(el){ el.textContent=fee+' Coins · '+SFLplLoan; });
  }
  function applyPlMarket(root){
    var grid=root.querySelector('.pgrid'); if(!grid)return;
    [].forEach.call(grid.querySelectorAll('.pcard[data-mine]'),function(c){ c.remove(); });
    for(var id in SFLplList){
      var p=SFLPLAYERS[id]; if(!p)continue;
      var kind=SFLplList[id], fee=kind==='loan'?plLoanFee(p):p.val;
      var card=document.createElement('div');
      card.className='pcard'; card.setAttribute('data-pl',id); card.setAttribute('data-kind',kind); card.setAttribute('data-mine','1');
      card.setAttribute('data-pos',/ST|LW|RW|CF/.test(p.pos)?'fwd':/CM|CAM|CDM|RM|LM/.test(p.pos)?'mid':'def');
      card.innerHTML='<div class="ph" style="background:linear-gradient(165deg,#1b2233,#10141d)">'+(kind==='loan'?'<span class="lbadge">LOAN · YOURS</span>':'<span class="lbadge" style="background:linear-gradient(140deg,#7CD843,#0FB753);color:#fff">TRANSFER · YOURS</span>')+'<span class="pos">'+p.pos+'</span><div class="pav" style="background-image:'+sflImg(p.av)+'"></div><div class="pn"><div class="n">'+p.name+'</div><div class="t">'+p.club+'</div></div></div><div class="meta"><span class="valchip"><div class="coin">C</div>'+fee+'</span><span class="mv '+(kind==='loan'?'flat':'up')+'">'+(kind==='loan'?SFLplLoan:'Listed')+'</span></div><div class="seller">'+(kind==='loan'?'Your loan listing':'Your transfer listing')+'</div>';
      grid.insertBefore(card,grid.firstChild);
    }
  }
  function applyHomePlayersDuty(root){
    var q=root.querySelector('.qt.players .qs'); if(!q)return;
    var d=plDutyCounts(), n=Math.min(2,d.sell)+Math.min(2,d.buy);
    q.textContent=n>=4?'Duty complete · sold 2 + bought 2':'Duty · sell '+d.sell+'/2 you pick · buy '+d.buy+'/2';
    var bar=root.querySelector('.qt.players .qbar i'); if(bar) bar.style.width=Math.round((n/4)*100)+'%';
  }
  function applyFtPlayerDuty(root){
    [].forEach.call(root.querySelectorAll('.trow'),function(r){
      var tt=r.querySelector('.tt'); if(!tt||!/buy|sell|player|transfer|loan/i.test(tt.textContent||''))return;
      var d=plDutyCounts();
      var req=r.querySelector('.req'); if(req) req.textContent='Sell '+Math.min(2,d.sell)+'/2 · Buy '+Math.min(2,d.buy)+'/2 · you pick sells · buys are matched';
      var bar=r.querySelector('.pbar i'); if(bar) bar.style.width=Math.round(((Math.min(2,d.sell)+Math.min(2,d.buy))/4)*100)+'%';
      if(d.sell>=2&&d.buy>=2){ r.classList.add('complete'); var side=r.querySelector('.side'); if(side) side.innerHTML='<div class="done">✓</div>'; }
    });
  }
  function applyFtBuySellDetail(root){
    var d=plDutyCounts(), n=Math.min(2,d.sell)+Math.min(2,d.buy);
    var prog=root.querySelector('#ft-buysell-prog'); if(prog) prog.textContent='Sell '+Math.min(2,d.sell)+'/2 · Buy '+Math.min(2,d.buy)+'/2';
    var dp=root.querySelector('.dp'); if(dp) dp.innerHTML=n+'<small> / 4</small>';
    var buyBtn=root.querySelector('[data-ftact="buyrecs"]');
    if(buyBtn) buyBtn.textContent='Buy the 2 players';
  }
  function applyPlRecsBox(root){
    var copy=root.querySelector('#pl-recs-copy'), rows=root.querySelector('#pl-recs-rows'), cta=root.querySelector('#pl-recs-cta');
    if(!copy&&!rows) return;
    var listed=plListedSellIds(), recs=plMatchRecs(), d=plDutyCounts();
    if(copy){
      if(!listed.length) copy.textContent='List 2 players first. SFL will then show two recommended buys matched to those listing values — you don’t browse-pick them.';
      else copy.textContent='You pick the sells. These buys are matched to your listing values.';
    }
    if(rows){
      if(!listed.length) rows.innerHTML='';
      else rows.innerHTML=recs.map(function(id,i){ return plRecRowHtml(id, listed[i]||listed[0]); }).join('');
    }
    if(cta) cta.style.display=listed.length>=2?'':'none';
  }
  function applyPlWeeklyBuys(root){
    var d=plDutyCounts(), listed=plListedSellIds(), recs=plMatchRecs();
    var ds=root.querySelector('#pl-w-sell'), db=root.querySelector('#pl-w-buy');
    if(ds){ var n=ds.querySelector('.n'); if(n)n.textContent=Math.min(2,d.sell)+'/2'; ds.classList.toggle('ok',d.sell>=2); }
    if(db){ var n2=db.querySelector('.n'); if(n2)n2.textContent=Math.min(2,d.buy)+'/2'; db.classList.toggle('ok',d.buy>=2); }
    var copy=root.querySelector('#pl-w-copy');
    if(copy){
      if(!listed.length) copy.textContent='Default pair until you list: Y. Okoro (450) matches A. Rivera (420–450) · T. Bello (310) matches M. Silva (300–340).';
      else copy.textContent=recs.map(function(id,i){ var p=SFLPLAYERS[id], s=SFLPLAYERS[listed[i]||listed[0]]; return p.name+' ('+p.val+') matches '+(s?s.name+' ('+s.val+')':'your listing'); }).join(' · ');
    }
    var rows=root.querySelector('#pl-w-rows');
    if(rows) rows.innerHTML=recs.map(function(id,i){ return plRecRowHtml(id, listed[i]||listed[0]); }).join('');
  }
  function applyPlListLive(root){
    var d=plDutyCounts(), btn=root.querySelector('[data-plact="afterlist"], .cta .btn');
    if(btn) btn.textContent=d.sell>=2?'Buy the 2 players':'List another player';
  }
  function applyPlPurchaseDuty(root){
    if(SFLplWeeklyBuy || (SFL_REC_POOL.indexOf(SFLpl)>=0)){
      if(!SFLplBought[SFLpl]) plRecordBuy(SFLpl);
      SFLplWeeklyBuy=false;
      var d=plDutyCounts(), btn=root.querySelector('.cta .btn');
      if(btn) btn.textContent=d.buy>=2?'Back to weekly tasks':'Buy the other pick';
    }
  }
  function sflImg(fn){ return 'var(--img-'+fn.replace(/[^a-zA-Z0-9]/g,'_')+'), url("assets/'+fn+'")'; }
  function setBalKey(root,key,val){
    [].forEach.call(root.querySelectorAll('.balr'),function(r){
      var k=r.querySelector('.k'); if(!k||k.textContent.toLowerCase().indexOf(key)<0)return;
      var v=r.querySelector('.v'); if(v)v.textContent=val;
    });
  }
  function applyTourn(root){
    if(!root)return;
    var bal=SFLtournCoins, fee=500, after=Math.max(0,bal-fee), elig=SFLtournEligible, payout=100*elig;
    var balS=bal.toLocaleString('en-US'), afterS=after.toLocaleString('en-US'), feeS=fee.toLocaleString('en-US'), payS=payout.toLocaleString('en-US');
    [].forEach.call(root.querySelectorAll('[data-tbal]'),function(e){e.textContent=balS;});
    [].forEach.call(root.querySelectorAll('[data-tafter]'),function(e){e.textContent=afterS;});
    [].forEach.call(root.querySelectorAll('[data-tfee]'),function(e){e.textContent=feeS;});
    [].forEach.call(root.querySelectorAll('[data-tcountry]'),function(e){e.textContent=SFLtournCountry+' '+SFLtournFlag;});
    [].forEach.call(root.querySelectorAll('[data-tname]'),function(e){e.textContent=SFLtournName;});
    [].forEach.call(root.querySelectorAll('[data-telig]'),function(e){e.textContent=String(elig);});
    [].forEach.call(root.querySelectorAll('[data-tpayout]'),function(e){e.textContent=payS;});
    var _tc=root.querySelector('.hubcard.tour .hv'); if(_tc)_tc.textContent=SFLtournReg?(SFLtournName+' · Group C'):('Register · '+SFLtournName);
    var _ta=root.querySelector('.tourcard.reg .tact'); if(_ta)_ta.textContent=SFLtournReg?'Open dashboard':'Register';
    var _tn=root.querySelector('#n-tourn-afcon'); if(_tn){ _tn.style.display=SFLtournReg?'none':''; }
  }
  function applyPlayer(root){
    var p=SFLPLAYERS[SFLpl]||SFLPLAYERS.rivera;
    var after=1240-p.val;
    var hero=root.querySelector('.dhero');
    if(hero){
      hero.setAttribute('data-art',SFLpl||'rivera');
      var fig=hero.querySelector('.dfull');
      if(fig) fig.style.backgroundImage=sflImg(p.fig);
      var dn=hero.querySelector('.dn'); if(dn)dn.textContent=p.name;
      var dt=hero.querySelector('.dt'); if(dt)dt.innerHTML=p.pos+' · '+p.club+' <span class="crest '+p.cr+'">'+p.crL+'</span> '+p.seller;
      var tr=hero.querySelector('.trend'); if(tr){ tr.className='mv trend '+p.move; tr.textContent=p.trend; }
    }
    var vv=root.querySelector('.valblock .vv'); if(vv)vv.textContent=p.val+' Coins';
    var vm=root.querySelector('.valblock .mv'); if(vm){ vm.className='mv '+p.move; vm.textContent=p.moveTxt; }
    var pr=root.querySelector('.cta .price'); if(pr)pr.textContent=p.val+' Coins';
    var fx=root.querySelectorAll('.dbody .card .balr .v');
    if(fx[0])fx[0].textContent=p.next; if(fx[1])fx[1].textContent=p.listed;
    var poly=root.querySelector('.chartcard polyline'); var gon=root.querySelector('.chartcard polygon');
    if(poly)poly.setAttribute('points',p.line);
    if(gon)gon.setAttribute('points',p.line+' 253,90 15,90');
    var pts=p.line.split(' ');
    [].forEach.call(root.querySelectorAll('.chartcard circle'),function(c,i){
      if(!pts[i])return; var xy=pts[i].split(','); c.setAttribute('cx',xy[0]); c.setAttribute('cy',xy[1]);
    });
    [].forEach.call(root.querySelectorAll('.wdl b'),function(b,i){ if(!p.wdl[i])return; b.className=p.wdl[i]; b.textContent=p.wdl[i].toUpperCase(); });
    [].forEach.call(root.querySelectorAll('.h1'),function(h){ if(/A\\. Rivera|T\\. Bello|K\\. Mensah|M\\. Silva/.test(h.textContent)) h.textContent=p.name; });
    [].forEach.call(root.querySelectorAll('.psummary .pn, .revealcard .rn .n'),function(n){ n.textContent=p.name; });
    [].forEach.call(root.querySelectorAll('.psummary .pp, .revealcard .rn .t'),function(t){ if(/Coins/.test(t.textContent)) t.textContent=p.val+' Coins'; else t.textContent=p.pos+' · '+p.club; });
    [].forEach.call(root.querySelectorAll('.psummary .pi'),function(im){ im.style.backgroundImage=sflImg(p.av); });
    [].forEach.call(root.querySelectorAll('.revealcard .rp'),function(im){ im.style.backgroundImage=sflImg(p.fig); });
    var pv=root.querySelector('.psummary .pv'); if(pv){ var c=pv.querySelector('.coin'); pv.innerHTML=''; if(c)pv.appendChild(c); pv.appendChild(document.createTextNode(String(p.val))); }
    setBalKey(root,'player price',p.val+' Coins');
    setBalKey(root,'held in escrow',p.val+' Coins');
    setBalKey(root,'spendable after hold',after+' Coins');
    setBalKey(root,'price paid',p.val+' Coins');
    setBalKey(root,'your value baseline',p.val+' Coins');
    setBalKey(root,'acquisition baseline',p.val+' Coins');
    setBalKey(root,'completed sale price',(p.val+(p.move==='up'?30:0))+' Coins');
    setBalKey(root,'listing price',p.val+' Coins');
    setBalKey(root,'current app value',p.val+' Coins');
    setBalKey(root,'loan fee',plLoanFee(p)+' Coins');
    var held=root.querySelector('.heldcard .ha'); if(held)held.textContent=p.val+' Coins held';
    [].forEach.call(root.querySelectorAll('.ss'),function(s){ if(/Rivera|Bello|Mensah|Silva/.test(s.textContent)) s.textContent=s.textContent.replace(/A\\. Rivera|T\\. Bello|K\\. Mensah|M\\. Silva/g,p.name); });
    [].forEach.call(root.querySelectorAll('.sub'),function(s){
      var tx=s.textContent;
      if(/from /.test(tx)||/Joined your squad|Transfer complete/.test((root.querySelector('.h1')||{}).textContent||'')) s.textContent=p.name+' · from '+p.seller;
      else if(/ to /.test(tx)) s.textContent=p.name+' · to Red District FC';
      else if(/costs \\d+/.test(tx)) s.textContent=tx.replace(/costs \\d+ Coins/,'costs '+p.val+' Coins');
    });
    [].forEach.call(root.querySelectorAll('.btn'),function(b){ b.innerHTML=b.innerHTML.replace(/\\b\\d{3}\\b Coins/g,p.val+' Coins'); });
  }
  function next(){var v=VIEWS[curJ]; if(curS<v.screens.length-1){curS++;} else if(curJ<VIEWS.length-1){curJ++;curS=0;} render();}
  function prev(){if(curS>0){curS--;} else if(curJ>0){curJ--;curS=VIEWS[curJ].screens.length-1;} render();}
  document.getElementById('bnext2').onclick=next; document.getElementById('bprev2').onclick=goBack;
  document.getElementById('bnext').onclick=next; document.getElementById('bprev').onclick=goBack;
  flowsel.onchange=function(){curJ=+flowsel.value;curS=0;render();};
  document.addEventListener('keydown',function(e){ var _ae=document.activeElement; if(_ae&&(_ae.tagName==='INPUT'||_ae.tagName==='TEXTAREA'||_ae.isContentEditable))return; if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();next();}else if(e.key==='ArrowLeft'){goBack();}});
  var tx=0,ty=0,swipeLock=null; var stage=document.getElementById('stage');
  var SWIPE_MIN=window.matchMedia('(pointer: coarse)').matches?96:72;
  var SWIPE_RATIO=window.matchMedia('(pointer: coarse)').matches?2.2:1.75;
  function swipeScrollTarget(t){return t&&t.closest&&t.closest('.scrollarea,.scroll,.lscroll,.hscroll,.feed,.list,.dbody,.lbody,.body,.rchat,.pkchat');}
  stage.addEventListener('touchstart',function(e){
    if(e.touches.length!==1)return;
    tx=e.touches[0].clientX; ty=e.touches[0].clientY; swipeLock=swipeScrollTarget(e.target)?'v':null;
  },{passive:true});
  stage.addEventListener('touchmove',function(e){
    if(e.touches.length!==1||swipeLock==='v')return;
    var dx=e.touches[0].clientX-tx, dy=e.touches[0].clientY-ty;
    if(Math.abs(dy)>Math.abs(dx)&&Math.abs(dy)>14) swipeLock='v';
    else if(Math.abs(dx)>Math.abs(dy)&&Math.abs(dx)>28) swipeLock='h';
  },{passive:true});
  stage.addEventListener('touchend',function(e){
    if(e.changedTouches.length!==1){swipeLock=null;return;}
    if(swipeLock==='v'){swipeLock=null;return;}
    var t=e.changedTouches[0], dx=t.clientX-tx, dy=t.clientY-ty;
    swipeLock=null;
    if(Math.abs(dx)<SWIPE_MIN||Math.abs(dx)<Math.abs(dy)*SWIPE_RATIO)return;
    dx<0?next():prev();
  },{passive:true});
  var MULTI='.tchip,.chip', SINGLE='.fchip,.lchip,.tab,.dtab,.segopt,.reasonopt,.srcopt,.laopt,.opt,.giftopt,.pt,.sw,.em,.teamrow,.lgchip,.formcard', SEG='.seg,.tabs,.dtabs';
  function singleSel(el,grp){[].forEach.call(grp.children,function(c){if(c.classList)c.classList.remove('on');});el.classList.add('on');}
  var hist=[]; var SFLdone={}; var SFLpred=null; var SFLpredMatch='Red Devils'; var SFLpredScore='2–1'; var SFLvote={motm:null,award:null}; var SFLmember=false; var SFLpkViewer=false; var SFLchatGift=null; var SFLchatOrigin='chatthread'; var SFLpickOrigin='vote'; var SFLfvActive=false; var SFLguest=false; var SFLmoveType='loan'; var SFLmgrMode=false; var SFLmgrEligible=false; var SFLmgrBuying=false; var SFLpkMin=5; var SFLseatCount=11; var SFLseatMode='pos'; var SFLformation='4-3-3'; var SFLfollowTab='followers'; var SFLchatPeer=null; var SFLprofilePeer=null; var SFLleftClub=false; var SFLpolicy='tos'; var SFLwaClip='goals'; var SFLwaSrc=null; var SFLwaApp='yt'; var SFLwaSize='md'; var SFLcoHosts={}; var SFLchAsk='none'; var SFLliveRole='viewer'; var SFLseated=false; var SFLchTab='join'; var SFLjoinQ=[{id:'join-priya',kind:'join',name:'Olivia S.',pos:'RW',av:'up_12.png'},{id:'join-kai',kind:'join',name:'Kai M.',pos:'CM',av:'up_02.png'},{id:'ch-maya',kind:'cohost',name:'Maya Chen',pos:'Viewer',av:'up_11.png'}]; var SFLpl='rivera'; var SFLplList={}; var SFLplBought={}; var SFLplWeeklyBuy=false; var SFLplKind='transfer'; var SFLperm={camera:true,mic:false,notif:null}; var SFLplLoan='1 week'; var SFLsigninTab='email'; var SFLsigninOtpSent=false; var SFLplOffers=[{id:'rivera',kind:'transfer',buyer:'Olivia S.',status:'pending'},{id:'mensah',kind:'loan',buyer:'Luis Ortega',status:'pending'}]; var SFLcs={status:'none',amt:5000,seller:'maya',rate:104,name:'Maya Chen',tradeAvail:8400,tradeReserved:5000,proof:0}; var SFLcmgrPick={id:'priya',name:'Olivia M.',fid:'67890',av:'up_11.png',lv:'9',fv:'1,510'}; var SFLcmgrStaff={}; var SFLcmgrAsk='none'; var SFLcmgrInvite='none'; var SFLcmgrTab='ask'; var SFLleaveAsk='none'; var SFLtournReg=false; var SFLtournCountry='Nigeria'; var SFLtournFlag='🇳🇬'; var SFLtournCoins=1240; var SFLtournEligible=7; var SFLtournName='AFCON 2026'; var SFLcmgrQ=[{id:'ask-diego',kind:'ask',name:'Diego S.',av:'up_10.png',status:'pending'}]; var ANCH={"watchpick":[6,"GL-WA-01"],"walogin":[6,"GL-WA-L"],"wapickvid":[6,"GL-WA-P"],"watchlive":[6,"GL-WA-H"],"watchlivev":[6,"GL-WA-V"],"watchend":[6,"GL-WA-E"],"chrequest":[6,"GL-CH-01"],"chsent":[6,"GL-CH-02"],"chinbox":[6,"GL-CH-H"],"cohostroom":[6,"GL-CH-C"],"joinwait":[6,"GL-05W"],"joinaccepted":[6,"GL-05OK"],"home": [19, "G-02"], "profile": [19, "G-05"], "userprofile": [19, "G-05U"], "followlist": [19, "G-05F"], "giftshowcase": [19, "G-05GW"], "badgewall": [19, "G-05BW"], "settings": [19, "G-05B"], "security": [19, "G-05C"], "deleteacct": [19, "G-05E"], "editprofile": [19, "G-05ED"], "changepw": [19, "G-05P"], "blockedusers": [19, "G-05BL"], "legal": [19, "G-05T"], "legaldoc": [19, "G-05TD"], "notifications": [19, "G-03"], "kyc": [19, "G-06A"], "kycverified": [19, "G-06H"], "support": [19, "G-07A"], "market": [5, "PL-01"], "myplayers":[5,"PL-06"], "plweeklybuys":[5,"PL-01W"], "plbuy":[5,"PL-03"], "plescrow":[5,"PL-04"], "plcomplete":[5,"PL-05"], "pllist":[5,"PL-07"], "plactions":[5,"PL-06A"], "plloan":[5,"PL-07L"], "plloanlive":[5,"PL-08L"], "pllistlive":[5,"PL-08"], "plsale":[5,"PL-09"], "plsold":[5,"PL-10"], "plfilters":[5,"PL-01A"], "games": [16, 0], "gameshub": [16, "MG-01"], "gamerules": [16, "MG-01R"], "gamehistory": [16, "MG-05"], "penalty": [16, "MG-02"], "penaltygoal": [16, "MG-02G"], "penaltysaved": [16, "MG-02S"], "wheel": [16, "MG-03"], "wheelspin": [16, "MG-03A"], "wheelresult": [16, "MG-04C"], "giftresult": [16, "MG-04G"], "csellers":[25,"CS-01"],"csloading":[25,"CS-01L"],"csempty":[25,"CS-01E"],"cserror":[25,"CS-01X"],"cseller":[25,"CS-02"],"csconfirm":[25,"CS-02C"],"cspending":[25,"CS-03"],"cspay":[25,"CS-04"],"cssent":[25,"CS-04S"],"cswait":[25,"CS-05"],"cstransfer":[25,"CS-06"],"csdone":[25,"CS-07"],"csrate":[25,"CS-08"],"cscancelled":[25,"CS-09"],"csexpired":[25,"CS-10"],"csreject":[25,"CS-11"],"cshistory":[25,"CS-12"],"csfailed":[25,"CS-13"],"csbecome":[25,"CS-20"],"csapply":[25,"CS-21"],"csapppend":[25,"CS-22"],"csapproved":[25,"CS-23"],"csappreject":[25,"CS-24"],"cssuspended":[25,"CS-25"],"csdesk":[25,"CS-30"],"csrequests":[25,"CS-31"],"csreq":[25,"CS-32"],"csconfirm-pay":[25,"CS-33"],"cstx":[25,"CS-34"],"cscust":[25,"CS-35"],"csnotes":[25,"CS-36"],"cssell":[25,"CS-40"],"csverify":[25,"CS-41"],"csnotfound":[25,"CS-41X"],"csamount":[25,"CS-42"],"cssellconfirm":[25,"CS-43"],"csselldone":[25,"CS-44"],"csinv":[25,"CS-50"],"csinvpay":[25,"CS-51"],"csinvdone":[25,"CS-52"], "wallet": [12, 0], "coinstore": [2, "J3-02"], "selectrecipient": [2, "J3-03"], "reviewpurchase": [2, "J3-05"], "coinrecipientconfirm":[2,"J3-04"], "coinpayment":[2,"J3-06"], "coinprocessing":[2,"J3-07"], "coinsuccess":[2,"J3-08"], "coinreceipt":[2,"J3-09"], "coinboost":[2,"J3-10"], "club": [1, "J2-16"], "tasks": [3, "FT-01"], "taskdetail":[3,"FT-03"], "taskbuysell":[3,"FT-03P"], "taskwatch":[3,"FT-03W"], "clubevents":[19,"EV-01"],"fvunlocked":[10,"FV-00"],"fvexplain":[10,"FV-01"],"fvconfirm":[10,"FV-02"],"fvprocessing":[10,"FV-03"],"fvsuccess":[10,"FV-04"],"fvdashboard":[10,"FV-05"],"fvhistory":[10,"FV-06"],"fvalready":[10,"FV-10"], "tasklocked":[3,"FT-04"], "taskverify":[3,"FT-05"], "taskcomplete":[3,"FT-06"], "taskclaim":[3,"FT-08"], "taskclaimed":[3,"FT-10"], "mystats":[3,"FT-11"], "predictions": [4, "PV-01"], "rewards": [15, 0], "managerhq": [13, "MC-01"], "mgrclubs":[13,"MC-00"], "mgrcommission":[13,"MC-01A"], "mgrfandetail":[13,"MC-04A"], "mgrremovefan":[13,"MC-04B"], "cmgrmake":[13,"MC-CM-01"], "cmgrinvsent":[13,"MC-CM-02"], "cmgrfanok":[13,"MC-CM-03"], "cmgrqueue":[13,"MC-CM-Q"], "cmgrinvite":[13,"MC-CM-F1"], "cmgrask":[13,"MC-CM-F2"], "cmgrsent":[13,"MC-CM-F3"], "cmgryes":[13,"MC-CM-F4"], "cmgrno":[13,"MC-CM-F5"], "inbox": [18, 0], "newmessage": [18, "MSG-02"], "msgrequests": [18, "MSG-03"], "kitbag": [9, 0], "progression": [11, 0], "live": [6, "GL-00"],"convert":[12,"WA-02"],"gtransfer":[12,"WA-03"],"withdraw":[12,"WA-04A"],"wallethist":[12,"WA-05"],"walletrules":[12,"WA-01A"],"convertconfirm":[12,"WA-02B"],"convertdone":[12,"WA-02D"],"transferamount":[12,"WA-03A"],"transferconfirm":[12,"WA-03B"],"kycverify":[12,"KYC-01"],"kycpersonal":[12,"KYC-01A"],"kycdoc":[12,"KYC-02"],"kycselfie":[12,"KYC-03"],"kycreview":[12,"KYC-04"],"withdrawconfirm":[12,"WA-04C"],"withdrawproc":[12,"WA-04D"],"txdetail":[12,"WA-05A"],"move":[14,0],"movereq":[14,"ML-00"],"createoffer":[14,"ML-01"],"reviewoffer":[14,"ML-01A"],"offersent":[14,"ML-01S"],"fanconsentloan":[14,"ML-02"],"fanconsentperm":[14,"ML-02P"],"acceptconfirm":[14,"ML-02A"],"moveoffer":[14,"ML-02"],"moveproc":[14,"ML-03"],"transfercomplete":[14,"ML-03A"],"loanactive":[14,"ML-03B"],"loanreturn":[14,"ML-03C"],"termschanged":[14,"ML-X1"],"offerexpired":[14,"ML-X2"],"offerdeclined":[14,"ML-X3"],"tasksdaily":[3,"FT-01"],"tasksweekly":[3,"FT-02"],"tasksdone":[3,"FT-07"],"tasksweeklydone":[3,"FT-07W"],"watch":[17,0],"golive":[6,"GL-01A"],"stadiumhub":[6,"GL-00"],"eligibility":[6,"GL-01A"],"permissions":[6,"GL-01B"],"golivesetup":[6,"GL-01"],"formation":[6,"GL-02"],"prelive":[6,"GL-02A"],"manageseats":[6,"GL-04"],"manageparticipant":[6,"GL-04A"],"endlive":[6,"GL-06"],"livesummary":[6,"GL-07"],"pk":[8,"PK-00"],"pkmatch":[8,"PK-01"],"pkincoming":[8,"PK-01C"],"pkmatchup":[8,"PK-01E"],"pkside":[8,"PK-03A"],"pkleadchange":[8,"PK-03B"],"pkfinalizing":[8,"PK-03D"],"pkwin":[8,"PK-04A"],"pkdraw":[8,"PK-04C"],"register":[0,"3"],"signin":[0,"10"],"forgotpw":[0,"12"],"resetverify":[0,"13"],"newpassword":[0,"14"],"passwordupdated":[0,"14b"],"clubs":[1,"J2-02"],"guesthome":[19,"G-02G"],"guestregister":[1,"J2-22"],"guestlive":[6,"GL-03Vg"],"gate":[19,"GATE-01"],"clubsearch":[1,"J2-03"],"clubapplications":[1,"J2-08"],"clubinvite":[1,"J2-13"],"clubdecline":[1,"J2-14"],"clubinviteaccepted":[1,"J2-15"],"clubleave":[1,"J2-18"],"clubleaveconfirm":[1,"J2-19"],"leavepending":[1,"J2-LV"],"clubleft":[1,"J2-20"],"league":[11,"PR-02"],"prohub":[11,"PR-00"],"fanlevel":[11,"PR-01"],"tournament":[11,"PR-03"],"clubgrade":[11,"PR-04"],"prizeeligibility":[11,"PR-04B"],"howtoearn":[11,"PR-01A"],"levelroadmap":[11,"PR-01B"],"clubdetail":[1,"J2-05"],"clubapply":[1,"J2-06"],"vote":[4,"PV-05"],"awards":[4,"PV-08"],"predictscore":[4,"PV-02"],"predictconfirm":[4,"PV-03"],"predictdone":[4,"PV-04"],"picksubmitted":[4,"PV-07"],"awardcandidates":[4,"PV-09"],"matchlive":[4,"PV-11"],"predictwin":[4,"PV-12"],"predictclose":[4,"PV-12b"],"playerdetail":[5,"PL-02"],"chatthread":[18,"MSG-04"],"rewarddetail":[15,"RW-01A"],"rewardclaim":[15,"RW-01B"],"rewardsuccess":[15,"RW-01C"],"rewardreview":[15,"RW-01E"],"rewardinprog":[15,"RW-01D"],"rewardhistory":[15,"RW-01F"],"clubblocked":[1,"J2-13b"],"noclub":[1,"J2-01"],"clubsubmitted":[1,"J2-07"],"clubconfirmed":[1,"J2-10"],"createclub":[24,"CC-00"],"mgrupgrade":[24,"CC-00"],"ccstart":[24,"CC-01T"],"ccbasics":[24,"CC-01"],"ccidentity":[24,"CC-02"],"cctype":[24,"CC-03"],"ccagree":[24,"CC-04"],"ccreview":[24,"CC-05"],"cccreated":[24,"CC-06"],"mgrapplications":[13,"MC-05"],"mgrapprovals":[13,"MC-07"],"mgrapprovaldetail":[13,"MC-07D"],"clubchat":[18,"MSG-05"],"clubmembers":[18,"MSG-05M"],"watchcomplete":[17,"CS-01C"],"choosestart":[0,"9"],"mgrfanlist":[13,"MC-04"],"mgrrecruit":[13,"MC-02"],"mgrshare":[13,"MC-02A"],"mgrinvitesent":[13,"MC-06R"],"mgrhistory":[13,"MC-02H"],"mgraddid":[13,"MC-06"],"mgrrewards":[13,"MC-03"],"mgrbreakdown":[13,"MC-01B"],"liveroom":[6,"GL-03V"],"squadroom":[6,"GL-05"],"giftmenu":[9,"GK-01"],"giftdetailq":[9,"GK-01A"],"giftconfirm":[9,"GK-01B"],"giftsending":[9,"GK-01D"],"giftsent":[9,"GK-01E"],"confirmseat":[6,"GL-05A"],"fanseated":[6,"GL-05B"],"seattaken":[6,"GL-05C"],"guestgate":[6,"GL-03Vg"],"chatgift":[18,"MSG-06"],"pkrandom":[8,"PK-01A"],"pkinvite":[8,"PK-01B"],"pkcountdown":[8,"PK-02A"],"pkbattle":[8,"PK-03"],"pkrematch":[8,"PK-04D"],"liveroomhost":[6,"GL-03H"],"callvoice":[18,"CALL-01"],"callvideo":[18,"CALL-04"],"callsettings":[18,"MSG-08"],"callperm":[18,"CALL-P"],"callactivevoice":[18,"CALL-03"],"callmissed":[18,"CALL-05"],"callhistory":[18,"CALL-06"],"leaguespend":[11,"PR-02C"],"leagueprev":[11,"PR-02D"],"tournhub":[11,"TR-01"],"tournnotify":[11,"TR-02"],"tournconfirm":[11,"TR-03"],"tournpay":[11,"TR-04"],"tournsuccess":[11,"TR-05"],"tourndash":[11,"TR-06"],"tournpayout":[11,"TR-07"],"tournteam":[11,"TR-08"],"tournrules":[11,"TR-09"]};
  function idxOfFnum(j,fn){var a=(JOUR[j]&&JOUR[j].screens)||[];for(var i=0;i<a.length;i++)if(a[i].fnum===fn)return i;return 0;}
  var GUESTOK={guesthome:1,gate:1,clubs:1,clubdetail:1,clubsearch:1,guestlive:1,live:1,register:1,signin:1,notifications:1,guestregister:1,market:1,playerdetail:1,plfilters:1,liveroom:1,pkbattle:1,stadiumhub:1,userprofile:1,squadroom:1,confirmseat:1,fanseated:1,pkfinalizing:1,pkwin:1,pkdraw:1,pkleadchange:1,pkcountdown:1,pkmatchup:1,watchlivev:1,legal:1,legaldoc:1};
  function goTo(a){
    if(a==='register'||a==='signin'){SFLguest=false;}
    if(a==='managerhq'||a==='mgrclubs'||a==='cccreated'||a.indexOf('mgr')===0){SFLmgrMode=true;SFLmember=true;}
    else if(a==='cmgrinvite'||a==='cmgrask'||a==='cmgrsent'||a==='cmgrno'){ if(SFLcmgrInvite!=='accepted'&&SFLcmgrAsk!=='accepted') SFLmgrMode=false; }
    else if(a==='guesthome'||a==='clubconfirmed'||a==='clubinviteaccepted'){SFLmgrMode=false;}
    if(a==='club'&&!SFLmember){a='noclub';}
    if(SFLguest){ if(a==='home'){a='guesthome';} else if(!GUESTOK[a]){a='gate';} }
    var d=ANCH[a]; if(!d)return false; hist.push({j:curJ,s:curS,html:mount.innerHTML}); curJ=FLOWN+d[0]; curS=(typeof d[1]==='number')?d[1]:idxOfFnum(d[0],d[1]); render(); return true;}
    function goBack(){ if(hist.length){var h=hist.pop(); curJ=h.j; curS=h.s; render(); if(h.html){mount.innerHTML=h.html;} var sc=VIEWS[curJ].screens[curS]||{}; SFLcoinify(mount); SFLcrest(mount); SFLchat(mount); if(/^ML-/.test(sc.fnum)||sc.fnum==='MC-07D') applyMoveType(mount); if(sc.fnum==='FT-01'||sc.fnum==='FT-02'){applyTaskDone(mount);} if(sc.fnum==='PV-01'){applyPredDone(mount);} if(sc.fnum==='PV-05'){applyVoteDone(mount,'motm');} if(sc.fnum==='PV-09'){applyVoteDone(mount,'award');} if(sc.fnum==='10'){applySigninTab(mount);} } else prev(); }
  function endCall(){ while(hist.length){ var _t=hist[hist.length-1]; var _f=((VIEWS[_t.j]&&VIEWS[_t.j].screens[_t.s])||{}).fnum||''; if(_f.indexOf('CALL')===0){hist.pop();} else break; } if(hist.length){goBack();} else {goTo('chatthread');} }
  function cleanTo(anchor, re){ while(hist.length){var _ch=hist[hist.length-1];var _cff=((VIEWS[_ch.j]&&VIEWS[_ch.j].screens[_ch.s])||{}).fnum||'';if(re.test(_cff)){hist.pop();}else break;} var _cd=ANCH[anchor]; if(!_cd)return; curJ=FLOWN+_cd[0]; curS=(typeof _cd[1]==='number')?_cd[1]:idxOfFnum(_cd[0],_cd[1]); render(); }
  function jumpTab(anchor){ var _jd=ANCH[anchor]; if(!_jd)return; curJ=FLOWN+_jd[0]; curS=(typeof _jd[1]==='number')?_jd[1]:idxOfFnum(_jd[0],_jd[1]); render(); }
  function returnTo(fnum, anchor){ while(hist.length){ var _rt=hist[hist.length-1]; var _rf=((VIEWS[_rt.j]&&VIEWS[_rt.j].screens[_rt.s])||{}).fnum||''; if(_rf===fnum){ goBack(); return; } hist.pop(); } if(anchor)goTo(anchor); }
  function enterAfterJoin(a){ SFLmember=true; hist.length=0; jumpTab('home'); goTo(a); }
  function goSectionFromClub(sec){ if(goTo(sec)&&hist.length){ var hc=ANCH['home']; hist[hist.length-1]={ j:FLOWN+hc[0], s:(typeof hc[1]==='number')?hc[1]:idxOfFnum(hc[0],hc[1]) }; } }
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
  function applySigninTab(root){
    if(!root.querySelector('.signin-panel'))return;
    var isPhone=SFLsigninTab==='phone';
    var seg=root.querySelector('.signin-seg')||root.querySelector('.seg');
    if(seg){
      [].forEach.call(seg.children,function(c){
        var tab=c.getAttribute('data-tab')||'';
        if(!tab)tab=/phone/i.test(c.textContent||'')?'phone':'email';
        c.classList.toggle('on',isPhone?(tab==='phone'):(tab==='email'));
      });
    }
    var em=root.querySelector('.signin-email'), ph=root.querySelector('.signin-phone');
    if(em)em.style.display=isPhone?'none':'';
    if(ph){
      ph.style.display=isPhone?'':'none';
      var send=ph.querySelector('.signin-phone-send'), verify=ph.querySelector('.signin-phone-verify');
      if(send)send.style.display=SFLsigninOtpSent?'none':'';
      if(verify)verify.style.display=SFLsigninOtpSent?'':'none';
    }
  }
  function destOf(t){
    if(t.closest('.coinpill'))return 'coinstore';
    if(t.closest('.hqbtn'))return 'managerhq';
    var nav=t.closest('.sfl-nav .nit,.sfl-nav .nc,.navpill .nav,.navpill .navc'); if(nav){var n=nav.textContent.toLowerCase(); if(n.indexOf('home')>=0)return 'home'; if(n.indexOf('market')>=0)return 'market'; if(n.indexOf('stadium')>=0||n.indexOf('live')>=0)return 'live'; if(n.indexOf('games')>=0)return 'games'; if(n.indexOf('chat')>=0)return 'inbox'; if(n.indexOf('wallet')>=0)return 'wallet'; return null;}
    var hic=t.closest('.hicon'); if(hic){var e=hic.textContent; if(e.indexOf('🔔')>=0)return 'notifications'; if(e.indexOf('💬')>=0)return 'inbox';}
    if(t.closest('.ha')||t.closest('.selavatar'))return 'profile';
    var lab=t.closest('.btn,.dbtn,.lbtn,.short,.mod,.tile,.tplay,.listrow,.rolerow,.pjoin,.ab,.mgo,.cgo,.gj,.rw,.cat,.reccard,.mbanner,.clubcard,.hqbtn,.nrow,.txrow,.hrow,.crow,.callrow,.qt,.mom,.hjoin,.nextfix,.hfol,.livecard,.act,.explorelink,a'); var x=(lab?lab.textContent:'').toLowerCase();
    var K=[['ask to become a manager','cmgrask'],['manager asked you','cmgrinvite'],['selected you to become','cmgrinvite'],['make manager','cmgrmake'],['co-managers','cmgrqueue'],['you are now a manager','cmgryes'],['is now a manager','cmgrfanok'],['request to become a room manager','chrequest'],['request room manager','chrequest'],['request to become co-host','chrequest'],['request co-host','chrequest'],['waiting list','chinbox'],['join & managers','chinbox'],['join & co-host','chinbox'],['buy from a coin seller','csellers'],['buy from coin seller','csellers'],['coin seller desk','csdesk'],['open desk','csdesk'],['go live','golive'],['start watch','watchlive'],['end watch-along','watchend'],['end watch','watchend'],['watch along','watchpick'],['▶ watch','watchpick'],['join a pk','pk'],['pk battle','pk'],['start a pk','pk'],['matchday','live'],['watchalong','live'],['join live','live'],['north stand','live'],['watch sfl','watch'],['watch','watch'],['make a prediction','predictions'],['predict','predictions'],['transfer gold','gtransfer'],['send gold','gtransfer'],['gold transfer','gtransfer'],['convert','convert'],['withdraw','withdraw'],['buy coins','coinstore'],['coin store','coinstore'],['top up','coinstore'],['manager hq','managerhq'],['manager dashboard','managerhq'],['open hq','managerhq'],['enter hq','managerhq'],['kit bag','kitbag'],['reward ready','rewards'],['ready to claim','rewards'],['see winners','rewards'],['monthly winners','rewards'],['claim','rewards'],['rewards','rewards'],['you won','rewards'],['invited you','clubinvite'],['invitation','clubinvite'],['application','clubapplications'],['open club','club'],['club home','club'],['view club','club'],['other clubs','clubs'],['explore other','clubs'],['browse clubs','clubs'],['discover clubs','clubs'],['explore clubs','clubs'],['find a club','clubs'],['join a fan club','clubs'],['join a club','clubs'],['join club','clubs'],['gold received','wallethist'],['sent you','wallethist'],['refund','wallethist'],['transaction','wallethist'],['loan offer','moveoffer'],['transfer offer','moveoffer'],['loan/transfer','move'],['awaiting fan consent','moveproc'],['move status','moveproc'],['loan activated','loanactive'],['loan completed','loanreturn'],['leave request approved','clubleft'],['leave request declined','club'],['seat request approved','fanseated'],['position approved','fanseated'],['seat request declined','live'],['join live','live'],['watchalong','live'],['matchday','live'],['north stand','live'],['pk battle','live'],['go live','live'],['watch party','live'],['stadium','live'],['live room','live'],['notification','notifications'],['messages','inbox'],['message','inbox'],['chat','inbox'],['prediction','predictions'],['tasks','tasks'],['duties','tasks'],['progression','progression'],['fan level','progression'],['verify identity','kyc'],['kyc','kyc'],['withdrawals unlocked','kyc'],['contact support','support'],['get support','support'],['report a problem','support'],['raise dispute','support'],['buy the 2 recommended','plweeklybuys'],['buy the 2 players','plweeklybuys'],['buy 2 players','plweeklybuys'],['list 2 players','myplayers'],['my players','myplayers'],['player market','market'],['escrow','market'],['market','market'],['edit profile','profile'],['my stats','profile'],['wallet','wallet'],['games','games'],['afcon 2026','tournnotify'],['register your country','tournnotify'],['tournament coin','tournhub'],['tournament registration','tournnotify']];
    for(var i=0;i<K.length;i++){if(x.indexOf(K[i][0])>=0)return K[i][1];}
    return null;
  }
  stage.addEventListener('input',function(e){ var f=e.target; if(f&&f.classList&&(f.classList.contains('dname')||f.classList.contains('epname'))){ showNameErr(f); } });
  // Stadium card avatar parallax tilt (pointer-follow, transform-only)
  var _tiltRAF=null,_tiltCard=null,_tiltPX=0,_tiltPY=0;
  function _applyTilt(){ _tiltRAF=null; if(!_tiltCard)return; var av=_tiltCard.querySelector('.rcav'); if(!av)return; av.style.setProperty('--ry',(_tiltPX*11).toFixed(2)+'deg'); av.style.setProperty('--rx',(-_tiltPY*8).toFixed(2)+'deg'); }
  function _resetTilt(card){ if(!card)return; var av=card.querySelector('.rcav'); if(av){av.style.setProperty('--rx','0deg');av.style.setProperty('--ry','0deg');} }
  stage.addEventListener('pointermove',function(e){ if(e.pointerType==='touch')return; var card=e.target.closest&&e.target.closest('.roomcard'); if(!card||!card.closest('.stadhome')){ if(_tiltCard){_resetTilt(_tiltCard);_tiltCard=null;} return; } var rc=card.querySelector('.rc')||card; var r=rc.getBoundingClientRect(); _tiltPX=(e.clientX-r.left)/r.width-0.5; _tiltPY=(e.clientY-r.top)/r.height-0.5; _tiltCard=card; if(!_tiltRAF)_tiltRAF=requestAnimationFrame(_applyTilt); });
  stage.addEventListener('pointerout',function(e){ var card=e.target.closest&&e.target.closest('.roomcard'); if(card&&(!e.relatedTarget||!card.contains(e.relatedTarget))){ _resetTilt(card); if(_tiltCard===card)_tiltCard=null; } });
  stage.addEventListener('click',function(e){
    var mEl=document.getElementById('scaler').firstElementChild; if(!mEl||!mEl.contains(e.target))return;
    var t=e.target;
    if(t.closest('.sfl-statusbar'))return;
    if(t.classList&&t.classList.contains('sheet-scrim')&&!t.closest('.sheet')){ goBack(); return; }
    var _navEl=t.closest('.sfl-nav .nit,.sfl-nav .nc,.navpill .nav,.navpill .navc'); if(_navEl){var _n=(_navEl.textContent||'').toLowerCase(); if(_n.indexOf('home')>=0){goTo(SFLguest?'guesthome':'home');} else if(_n.indexOf('market')>=0){goTo('market');} else if(_n.indexOf('stadium')>=0||_n.indexOf('live')>=0){goTo('live');} else if(_n.indexOf('games')>=0){goTo(SFLguest?'gate':'games');} else if(_n.indexOf('chat')>=0){goTo(SFLguest?'gate':'inbox');} else if(_n.indexOf('wallet')>=0){goTo('wallet');} return;}
    if(t.closest('.coinbal')){goTo('wallet');return;}
    if(t.closest('.statgrid')){return;}
    var _cf=(VIEWS[curJ].screens[curS]||{}).fnum||'';
    var _mck=t.closest('.mcchip'); if(_mck){ var _mcl=mEl.querySelector('.mclock'); var _mn=+_mck.getAttribute('data-min'); singleSel(_mck,_mck.parentElement); if(_mcl){ _mcl.setAttribute('data-sec',_mn*60); _mcl.setAttribute('data-init',_mn*60); var _cm=_mcl.querySelector('.mm'),_cs=_mcl.querySelector('.ss'); if(_cm)_cm.textContent=(_mn<10?'0':'')+_mn; if(_cs)_cs.textContent='00'; _mcl.classList.remove('low'); startTimers(mEl);} sflToast('⏱ Match time set to '+_mn+' min'); return; }
    if(t.closest('.mcreset')){ var _mcl2=mEl.querySelector('.mclock'); if(_mcl2){ var _in=+(_mcl2.getAttribute('data-init')||2700); _mcl2.setAttribute('data-sec',_in); var _im=Math.floor(_in/60); var _rm=_mcl2.querySelector('.mm'),_rs=_mcl2.querySelector('.ss'); if(_rm)_rm.textContent=(_im<10?'0':'')+_im; if(_rs)_rs.textContent='00'; _mcl2.classList.remove('low'); startTimers(mEl);} sflToast('↺ Clock reset'); return; }
    var _pkl=t.closest('.pklen'); if(_pkl){ singleSel(_pkl,_pkl.parentElement); SFLpkMin=+_pkl.getAttribute('data-min'); sflToast('⚔️ Battle length · '+SFLpkMin+' min'); return; }
    var _mic=t.closest('.micind'); if(_mic){ var _mst=_mic.closest('.seat'); var _isHost=(_cf==='GL-03H'||_cf==='GL-CH-C'||_cf==='GL-WA-H'); var _mnm=(((_mst&&_mst.querySelector('.nm'))||{}).textContent||'this seat').trim(); var _isYou=_mst&&(_mst.classList.contains('you')||/^you$/i.test(_mnm)); if(_isHost||_isYou||isRoomMgr()){ var _md=_mic.classList.toggle('muted'); _mic.textContent=_md?'🔇':'🎤'; sflToast((_md?'🔇 Muted ':'🎤 Unmuted ')+(_isYou?'your mic':_mnm)); } else { sflToast('🔒 Only the host or a room manager can mute other seats'); } return; }
    if(t.closest('.rback')){ var _rbf=((VIEWS[curJ].screens[curS]||{}).fnum)||''; SFLpip=(_rbf==='GL-03H'||_rbf==='GL-WA-H')?'host':'viewer'; goTo('live'); return; }
    if(t.closest('.rleave')){ showLeaveConfirm(); return; }
    var _sug=t.closest('.dnsug'); if(_sug){ var _de=_sug.closest('.dnerr'); var _df=_de&&_de.previousElementSibling; if(_df){ _df.textContent=_sug.getAttribute('data-s'); showNameErr(_df); } return; }
    if(_cf==='7'&&t.closest('.btn')){ var _f7=mEl.querySelector('.dname'); if(_f7&&showNameErr(_f7)){return;} next(); return; }
    if(_cf==='10'&&mEl.querySelector('.signin-panel')){
      var _sg10=t.closest('.seg i'); if(_sg10){
        var _tab10=_sg10.getAttribute('data-tab')||(/phone/i.test(_sg10.textContent||'')?'phone':'email');
        SFLsigninTab=_tab10; if(_tab10==='email')SFLsigninOtpSent=false;
        singleSel(_sg10,_sg10.parentElement); applySigninTab(mEl); return;
      }
      if(t.closest('.resend .b')){ SFLsigninOtpSent=false; applySigninTab(mEl); return; }
      var _sb10=t.closest('.btn'); if(_sb10){
        var _sbt=(_sb10.textContent||'').trim();
        if(/send code/i.test(_sbt)&&SFLsigninTab==='phone'&&!SFLsigninOtpSent){ SFLsigninOtpSent=true; applySigninTab(mEl); sflToast('Code sent · check your messages'); return; }
      }
      if(t.closest('.forgot')){ SFLsigninTab='email'; SFLsigninOtpSent=false; goTo('forgotpw'); return; }
    }
    if(_cf==='3b'){
      var _b3b=t.closest('.btn'); if(_b3b){
        if(/sign in/i.test(_b3b.textContent)){ SFLsigninTab='email'; SFLsigninOtpSent=false; goTo('signin'); return; }
        if(/recover/i.test(_b3b.textContent)){ goTo('forgotpw'); return; }
      }
      if(t.closest('.top .back')){ goBack(); return; }
      return;
    }
    if(_cf==='12'){
      if(t.closest('.top .back')){ if(hist.length){goBack();}else{SFLsigninTab='email';SFLsigninOtpSent=false;goTo('signin');} return; }
      if(t.closest('.btn')){ goTo('resetverify'); sflToast('Verification code sent'); return; }
      return;
    }
    if(_cf==='13'){
      if(t.closest('.top .back')){ goBack(); return; }
      if(t.closest('.resend .b')){ sflToast(/phone/i.test((t.closest('.resend .b').textContent||''))?'Code sent to your phone':'Code resent'); return; }
      if(t.closest('.btn')){ goTo('newpassword'); return; }
      return;
    }
    if(_cf==='14'){
      if(t.closest('.top .back')){ goBack(); return; }
      if(t.closest('.btn')){ goTo('passwordupdated'); return; }
      return;
    }
    if(_cf==='14b'){
      if(t.closest('.btn')){ goTo('signin'); return; }
      return;
    }
    if(_cf==='1'){ if(!t.closest('.btn,.altlink,a')){next();return;} }
    if(_cf==='G-03'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.ico')){[].forEach.call(mEl.querySelectorAll('.unread'),function(u){u.style.display='none';}); sflToast('All notifications marked read'); return;} var _nfc=t.closest('.fchip'); if(_nfc){singleSel(_nfc,_nfc.parentElement);return;}
      var _off=t.closest('[data-ploffer]');
      if(_off){
        var _pid=_off.getAttribute('data-ploffer')||'rivera', _kind=_off.getAttribute('data-kind')||'transfer', _dec=(t.closest('[data-pldec]')||{}).getAttribute&&t.closest('[data-pldec]').getAttribute('data-pldec');
        SFLpl=_pid;
        var _oi=-1, _i; for(_i=0;_i<SFLplOffers.length;_i++){ if(SFLplOffers[_i].id===_pid){ _oi=_i; break; } }
        if(_oi<0){ SFLplOffers.unshift({id:_pid,kind:_kind,buyer:_kind==='loan'?'Luis Ortega':'Olivia S.',status:'pending'}); _oi=0; }
        if(_dec==='approve'){
          SFLplOffers[_oi].status='approved'; delete SFLplList[_pid];
          if(_kind==='loan'){ sflToast('Loan approved · '+SFLplOffers[_oi].buyer+' has them for '+SFLplLoan); cleanTo('myplayers',/^G-03$/); }
          else { sflToast('Transfer approved · escrow completing'); goTo('plsale'); }
          return;
        }
        if(_dec==='reject'){
          SFLplOffers[_oi].status='rejected';
          sflToast('Offer rejected · listing stays on the market');
          applyPlNotifs(mEl);
          return;
        }
        sflToast('Approve or reject this offer');
        return;
      }
      var _cmn=t.closest('[data-cmgr]');
      if(_cmn){
        var _cmk=_cmn.getAttribute('data-cmgr');
        var _cmd=(t.closest('[data-cmdec]')||{}).getAttribute&&t.closest('[data-cmdec]').getAttribute('data-cmdec');
        if(_cmk==='invite'){
          if(_cmd==='accept'){ cmgrGrant(SFLcmgrPick.id); var _ia=cmgrFind('inv-'+(SFLcmgrPick.id||'priya')); if(_ia)_ia.status='accepted'; sflToast('You are now a manager'); goTo('cmgryes'); return; }
          if(_cmd==='reject'){ SFLcmgrInvite='rejected'; var _ir=cmgrFind('inv-'+(SFLcmgrPick.id||'priya')); if(_ir)_ir.status='rejected'; goTo('cmgrno'); return; }
          goTo('cmgrinvite'); return;
        }
        if(_cmk==='yes'){ goTo('managerhq'); return; }
        if(_cmk==='inbox'){ goTo('cmgrqueue'); return; }
        return;
      }
      var _tno=t.closest('[data-tourn]');
      if(_tno){ var _un=_tno.querySelector('.unread'); if(_un)_un.style.display='none'; goTo(SFLtournReg?'tourndash':'tournnotify'); return; }
      var _nrow=t.closest('.nrow'); if(_nrow&&!_nrow.getAttribute('data-ploffer')&&!_nrow.getAttribute('data-cmgr')&&!_nrow.getAttribute('data-tourn')){
        var _ntx=(_nrow.textContent||'').toLowerCase();
        if(/afcon|register your country|tournament coin/.test(_ntx)){ goTo(SFLtournReg?'tourndash':'tournnotify'); return; }
      }
      return;
    }
    if(_cf==='MSG-01'){var _rq=t.closest('.fchip'); if(_rq){ var _rt=(_rq.textContent||'').toLowerCase(); if(/request/i.test(_rt)){goTo('msgrequests');return;} singleSel(_rq,_rq.parentElement); [].forEach.call(mEl.querySelectorAll('.crow'),function(r){ var show=true; if(/unread/.test(_rt)){show=!!r.querySelector('.unread');} else if(/club/.test(_rt)){show=!!r.querySelector('.rolechip.club');} else if(/manager/.test(_rt)){show=!!r.querySelector('.rolechip.mgr');} r.style.display=show?'':'none'; }); return;} }
    if(t.closest('.pkcard')){SFLpkViewer=true;goTo('pkbattle');return;}
    var _dvc=t.closest('.filters .fchip'); if(_dvc&&mEl.querySelector('.pkcard')){ singleSel(_dvc,_dvc.parentElement); var _pk=/pk/i.test(_dvc.textContent); var _dh=mEl.querySelector('.hero'); if(_dh)_dh.style.display=_pk?'none':''; [].forEach.call(mEl.querySelectorAll('.rcard'),function(r){var _isp=r.classList.contains('pkcard'); r.style.display=(_pk?_isp:!_isp)?'':'none';}); var _car=mEl.querySelector('.carousel'); if(_car){_car.classList.toggle('pkmode',_pk);} var _rh=mEl.querySelector('.rowhead .t'); if(_rh)_rh.textContent=_pk?'Live PK battles':'Rooms heating up'; return; }
    if(_cf==='CC-01T'){var lgc=t.closest('.lgchip'); if(lgc){var grp=lgc.parentElement; [].forEach.call(grp.children,function(c){c.classList&&c.classList.remove('on');}); lgc.classList.add('on'); var key=lgc.getAttribute('data-league')||''; [].forEach.call(mEl.querySelectorAll('.lgroup'),function(g){g.style.display=(!key||g.getAttribute('data-league')===key)?'':'none';}); return;}}
    var ffc=t.closest('.filters .fchip'); if(ffc){var fgrp=ffc.parentElement;[].forEach.call(fgrp.children,function(c){c.classList&&c.classList.remove('on');});ffc.classList.add('on');var fl=(ffc.textContent||'').toLowerCase();var fk=/follow/.test(fl)?'following':/premier/.test(fl)?'prem':/champion/.test(fl)?'champions':'';var rc=mEl.querySelectorAll('.carousel .rcard, .rcard');[].forEach.call(rc,function(r){var cats=(r.getAttribute('data-cat')||'');r.style.display=(!fk||cats.indexOf(fk)>=0)?'':'none';});return;}
    if(_cf==='RW-01'){var bchip=t.closest('.chip'); if(bchip&&bchip.querySelector('.cv')){goTo('wallet');return;}}
    if(_cf.indexOf('J3-')===0){
      var _j3bk=t.closest('.top .back'); if(_j3bk){var _j3t=(_j3bk.textContent||'').trim(); if(/🧾/.test(_j3t)){goTo('coinreceipt');return;} if(/↗/.test(_j3t)){sflToast('Sharing receipt…');return;} goBack(); return;}
      if(_cf==='J3-01'){ if(t.closest('.btn')){goTo('register');return;} return; }
      if(_cf==='J3-02'){ if(t.closest('.ch')){goTo('selectrecipient');return;} var _pk=t.closest('.pkg'); if(_pk){[].forEach.call(_pk.parentElement.children,function(c){c.classList&&c.classList.remove('on');});_pk.classList.add('on');return;} if(t.closest('.btn')){goTo('reviewpurchase');return;} return; }
      if(_cf==='J3-03'){ var _sg=t.closest('.segtabs i'); if(_sg){singleSel(_sg,_sg.parentElement);return;} if(t.closest('.btn')){goTo('coinrecipientconfirm');return;} return; }
      if(_cf==='J3-04'){ var _b4=t.closest('.btn'); if(_b4){ if(/search again/i.test(_b4.textContent)){goBack();return;} goTo('reviewpurchase');return;} return; }
      if(_cf==='J3-05'){ if(t.closest('.confirm')){t.closest('.confirm').classList.toggle('on');return;} var _pm=t.closest('.method'); if(_pm){ [].forEach.call(mEl.querySelectorAll('.method'),function(x){x.classList.remove('on');}); _pm.classList.add('on'); if(_pm.getAttribute('data-pay')==='seller'){goTo('csellers');return;} return;} if(t.closest('.btn')){ var _sell=mEl.querySelector('.method.on[data-pay="seller"]'); if(_sell){goTo('csellers');return;} goTo('coinpayment');return;} return; }
      if(_cf==='J3-06'){ if(t.closest('.btn')){goTo('coinprocessing');return;} return; }
      if(_cf==='J3-07'){ goTo('coinsuccess'); return; }
      if(_cf==='J3-08'){ var _b8=t.closest('.btn'); if(_b8){ if(/receipt/i.test(_b8.textContent)){goTo('coinreceipt');return;} if(SFLmgrBuying){ SFLmgrBuying=false; SFLmgrEligible=true; while(hist.length){var _hm=hist[hist.length-1];var _fm=((VIEWS[_hm.j]&&VIEWS[_hm.j].screens[_hm.s])||{}).fnum||'';if(/^J3-/.test(_fm)||_fm==='CC-00'){hist.pop();}else break;} var _dcs=ANCH['ccstart']; curJ=FLOWN+_dcs[0]; curS=idxOfFnum(_dcs[0],_dcs[1]); render(); sflToast('5,000 Coins added · Manager unlocked'); return; } while(hist.length){var _j8=hist[hist.length-1];var _j8f=((VIEWS[_j8.j]&&VIEWS[_j8.j].screens[_j8.s])||{}).fnum||'';if(/^J3-/.test(_j8f)){hist.pop();}else break;} goBack(); return;} return; }
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
    if(_cf.indexOf('CS-')===0 && ((VIEWS[curJ].screens[curS]||{}).srcJ===25)){
      var _csbk=t.closest('.top .back');
      if(_csbk){ if(/🔔/.test(_csbk.textContent||'')){goTo('csnotes');return;} if(/🧾/.test(_csbk.textContent||'')){goTo('cshistory');return;} if(_cf==='CS-30'){goTo('profile');return;} goBack(); return; }
      var _sl=t.closest('[data-seller]');
      if(_sl){
        if(_sl.classList.contains('off')){ sflToast('Seller is offline'); return; }
        var _sid=_sl.getAttribute('data-seller');
        var _S={maya:{name:'Maya Chen',rate:104,avail:12400},luis:{name:'Luis Ortega',rate:102,avail:3200},kenji:{name:'Kenji Sato',rate:100,avail:900},nia:{name:'Nia Okonkwo',rate:101,avail:8000}}[_sid]||{name:'Maya Chen',rate:104};
        SFLcs.seller=_sid; SFLcs.name=_S.name; SFLcs.rate=_S.rate; goTo('cseller'); return;
      }
      var _am=t.closest('[data-amt]');
      if(_am){ [].forEach.call(mEl.querySelectorAll('[data-amt]'),function(x){x.classList.remove('on');}); _am.classList.add('on'); SFLcs.amt=+(_am.getAttribute('data-amt')||500); applyCsDetail(mEl); return; }
      var _st=t.closest('.star');
      if(_st){ var _stars=_st.parentElement.querySelectorAll('.star'); var _si=[].indexOf.call(_stars,_st); [].forEach.call(_stars,function(s,i){s.classList.toggle('on',i<=_si);}); return; }
      var _fc=t.closest('.fchip');
      if(_fc && _fc.hasAttribute('data-csfilter')){ singleSel(_fc,_fc.parentElement); var _f=_fc.getAttribute('data-csfilter'); if(_cf==='CS-01'){ [].forEach.call(mEl.querySelectorAll('.srow[data-seller]'),function(r){ var off=r.classList.contains('off'); r.style.display=(_f==='online'&&off)?'none':''; }); if(_f==='online'&&!mEl.querySelector('.srow[data-seller]:not(.off)')){ goTo('csempty'); } } return; }
      var _inv=t.closest('[data-inv]');
      if(_inv){ [].forEach.call(mEl.querySelectorAll('[data-inv]'),function(x){x.classList.remove('on');}); _inv.classList.add('on'); var _iv=+_inv.getAttribute('data-inv'); SFLcs.buyAmt=_iv; var _btn=mEl.querySelector('.cta .btn'); if(_btn)_btn.textContent='Buy '+_iv.toLocaleString('en-US')+' trading · $'+(_iv/10); return; }
      var _act=(t.closest('[data-csact]')||{}).getAttribute&&t.closest('[data-csact]').getAttribute('data-csact');
      if(_act==='copy'){ sflToast('Copied'); return; }
      if(_act==='create'){ sflToast('New purchase request · 5,000 Coins reserved on Maya’s desk'); goTo('cspending'); return; }
      if(_act==='cancel'){ if(window._sflcsto){clearTimeout(window._sflcsto);window._sflcsto=null;} sflToast('Order cancelled · reserved coins released'); goTo('cscancelled'); return; }
      if(_act==='needproof'){ sflToast('Attach a payment screenshot first'); return; }
      if(_act==='attach'){ attachCsProof(mEl); return; }
      if(_act==='sent'){ if(!SFLcs.proof){ sflToast('Attach a payment screenshot first'); return; } sflToast('Proof submitted · waiting for Maya'); goTo('cswait'); return; }
      if(_act==='rated'){ sflToast('Thanks · Maya is now 4.98'); if(SFLmgrBuying){ SFLmgrEligible=true; SFLmgrBuying=false; sflToast('✓ 5,000 Coins ready — continue creating your club'); cleanTo('createclub', /^CS-|^J3-/); return; } cleanTo('coinstore', /^CS-/); return; }
      if(_act==='apply'){ SFLcs.status='pending'; sflToast('Application submitted'); goTo('csapppend'); return; }
      if(_act==='accept'){ SFLcs.tradeAvail=Math.max(0,SFLcs.tradeAvail-5000); SFLcs.tradeReserved+=5000; sflToast('Accepted · 5,000 reserved — waiting for buyer’s transfer'); goTo('csconfirm-pay'); return; }
      if(_act==='confirm-pay'){ SFLcs.tradeReserved=Math.max(0,SFLcs.tradeReserved-5000); sflToast('✓ Payment confirmed · 5,000 Coins released to Alex'); goTo('csdesk'); return; }
      if(_act==='sell'){ SFLcs.tradeAvail=Math.max(0,SFLcs.tradeAvail-5000); sflToast('Coins received · Olivia +5,000'); goTo('csselldone'); return; }
      if(_act==='buystock'){ var _ba=SFLcs.buyAmt||20000; SFLcs.tradeAvail+=_ba; if(SFLcs.status!=='approved'){ SFLcs.status='approved'; sflToast('✓ Inventory funded · you’re now a Coin Seller'); goTo('csapproved'); return; } sflToast('Trading inventory +'+_ba.toLocaleString('en-US')); goTo('csinvdone'); return; }
      var _csg=t.closest('[data-csgo]');
      if(_csg){
        var _cka=_csg.getAttribute('data-csgo');
        if(_cka==='csapproved'){ SFLcs.status='approved'; sflToast('Seller approved · your desk is live'); }
        if(_cka==='csappreject'){ SFLcs.status='rejected'; }
        if(_cka==='home'){ goTo('home'); return; }
        if(_cka==='support'){ goTo('support'); return; }
        if(_cka==='coinstore'){ if(SFLmgrBuying){ SFLmgrEligible=true; SFLmgrBuying=false; sflToast('✓ 5,000 Coins ready — continue creating your club'); cleanTo('createclub', /^CS-|^J3-/); return; } cleanTo('coinstore', /^CS-/); return; }
        if(!goTo(_cka)) sflToast('Coming next');
        return;
      }
      return;
    }
    if(_cf==='MSG-01'){ if(t.closest('.search')){goTo('newmessage');return;} var msgico=t.closest('.ico'); if(msgico){ if(/✎/.test(msgico.textContent)){goTo('newmessage');return;} if(/⚙/.test(msgico.textContent)){goTo('callsettings');return;} }}
    if(_cf==='MSG-06'){ if(t.closest('.btn')){ var _ge=mEl.querySelector('.giftopt.on .ge'),_gnn=mEl.querySelector('.giftopt.on .gn'),_gcc=mEl.querySelector('.giftopt.on .gc'); SFLchatGift={em:(_ge?_ge.textContent:'🎁').trim(),gn:(_gnn?_gnn.textContent:'Gift').trim(),gp:(_gcc?_gcc.textContent:'').replace(/[^0-9]/g,'')}; while(hist.length){var _h=hist[hist.length-1];var _hf=((VIEWS[_h.j]&&VIEWS[_h.j].screens[_h.s])||{}).fnum||'';if(_hf==='MSG-06'||_hf==='MSG-04'||_hf==='MSG-05'){hist.pop();}else break;} var _dc=ANCH[SFLchatOrigin]||ANCH['chatthread']; curJ=FLOWN+_dc[0]; curS=idxOfFnum(_dc[0],_dc[1]); render(); return;} }
    if(_cf==='G-05U'){ var _ub=t.closest('.back'); if(_ub){ if(/‹|←/.test(_ub.textContent)){goBack();} return; } if(t.closest('.umsg')){goTo('chatthread');return;} if(t.closest('.ugift')){goTo('giftmenu');return;} var _uf=t.closest('.ufollow'); if(_uf){ if(SFLguest){goTo('gate');return;} var _un=((mEl.querySelector('.pn')||{}).textContent||'this fan').replace(/[✓✔]/g,'').trim(); var _on=/following/i.test(_uf.textContent); _uf.textContent=_on?'Follow':'Following'; _uf.style.background=_on?'#C9FF3D':'rgba(255,255,255,.18)'; _uf.style.color=_on?'#0A1400':'#fff'; sflToast(_on?('Unfollowed '+_un):('Following '+_un)); return;} var _fcu=t.closest('.fcount'); if(_fcu){SFLfollowTab=_fcu.getAttribute('data-tab')||'followers'; goTo('followlist'); return;} var _sru=t.closest('.showrow'); if(_sru){goTo(/badge/i.test(_sru.textContent)?'badgewall':'giftshowcase');return;} if(t.closest('.listrow')){return;} }
    if(_cf==='G-05GW'||_cf==='G-05BW'){ if(t.closest('.top .back')){goBack();return;} return; }
    if(_cf==='G-05F'){ if(t.closest('.top .back')){goBack();return;} var _ft=t.closest('.foltab'); if(_ft){SFLfollowTab=_ft.getAttribute('data-tab')||'followers'; applyFollowTab(mEl); return;} var _fbn=t.closest('.folbtn'); if(_fbn){var _fon=_fbn.classList.toggle('on'); _fbn.textContent=_fon?'Following':'Follow'; return;} if(t.closest('.folrow')){goTo('userprofile');return;} return; }
    if(_cf==='GATE-01'){ if(t.closest('.top .back')||t.closest('.altlink')){goBack();return;} var _gt=t.closest('.btn'); if(_gt){ if(/sign in/i.test(_gt.textContent)){goTo('signin');return;} goTo('register');return;} return; }
    if(_cf==='G-05ED'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.epphoto')){showPhotoSheet();return;} if(t.closest('.epname')){return;} if(t.closest('.btn')){ var _fe=mEl.querySelector('.epname'); if(_fe&&showNameErr(_fe)){return;} goBack();sflToast('Profile updated');return;} return; }
    if(_cf==='G-05'){ if(t.closest('.pback')){goTo('home');return;} if(t.closest('.pt .back')){goTo('editprofile');return;} if(t.closest('.cmgrask')){goTo('cmgrask');return;} if(t.closest('.mgrupg')){goTo('mgrupgrade');return;} if(t.closest('.mgo')){goTo('managerhq');return;} if(t.closest('.rgo')){goTo('managerhq');return;} var _ml=t.closest('.mgrlink'); if(_ml){goTo(_ml.getAttribute('data-go'));return;} if(t.closest('.rolerow')){return;} if(t.closest('.levelcard')){goTo('fanlevel');return;} var _fc5=t.closest('.fcount'); if(_fc5){SFLfollowTab=_fc5.getAttribute('data-tab')||'followers'; goTo('followlist'); return;} var _sr5=t.closest('.showrow'); if(_sr5){goTo(/badge/i.test(_sr5.textContent)?'badgewall':'giftshowcase');return;} var _p5=t.closest('.listrow'); if(_p5){var _p5t=(_p5.textContent||'').toLowerCase(); if(/wallet/.test(_p5t)){goTo('wallet');return;} if(/coin seller/.test(_p5t)){goTo(SFLcs.status==='approved'?'csdesk':'csbecome');return;} if(/kit bag/.test(_p5t)){goTo('kitbag');return;} if(/kyc/.test(_p5t)){goTo('kyc');return;} if(/settings/.test(_p5t)){goTo('settings');return;} return;} return; }
    if(_cf==='G-05B'){ if(t.closest('.top .back')){goBack();return;} var _sw=t.closest('.sw'); if(_sw){_sw.classList.toggle('on');return;} var _sl=t.closest('.listrow'); if(_sl){var _st=(_sl.textContent||'').toLowerCase(); if(/email/.test(_st)){showEditSheet('Email','z•••@gmail.com','We\\'ll send a verification link to confirm.');return;} if(/phone/.test(_st)){showEditSheet('Phone','+44 •••• ••• 021','We\\'ll text a verification code.');return;} if(/change password/.test(_st)){goTo('changepw');return;} if(/active devices/.test(_st)){goTo('security');return;} if(/blocked/.test(_st)){goTo('blockedusers');return;} if(/language/.test(_st)){showLanguageSheet();return;} if(/delete account/.test(_st)){goTo('deleteacct');return;} if(/log out/.test(_st)){showLogoutSheet();return;} if(/terms|privacy|guidelines/.test(_st)){goTo('legal');return;} return;} return; }
    if(_cf==='G-05P'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.pwfield')){return;} if(t.closest('.btn')){goBack();sflToast('Password updated');return;} return; }
    if(_cf==='G-05BL'){ if(t.closest('.top .back')){goBack();return;} var _bl=t.closest('.blbtn'); if(_bl){var _row=t.closest('.blrow'); var _nm=((_row.querySelector('div')||{}).textContent||'User'); if(_row)_row.remove(); sflToast('Unblocked'); return;} return; }
    if(_cf==='MSG-08'){ if(t.closest('.top .back')){goBack();return;} var _msr=t.closest('.setrow'); if(_msr){ var _mrd=_msr.querySelector('.radio'); if(_mrd){ var _mgrp=_msr.closest('.setgrp'); if(_mgrp){[].forEach.call(_mgrp.querySelectorAll('.radio'),function(r){r.classList.remove('on');});} _mrd.classList.add('on'); return; } var _msw=_msr.querySelector('.sw'); if(_msw){_msw.classList.toggle('on'); return;} } return; }
    if(_cf==='G-05T'){ if(t.closest('.top .back')){goBack();return;} var _lgr=t.closest('.listrow'); if(_lgr){var _lg=(_lgr.textContent||'').toLowerCase(); SFLpolicy=/privacy/.test(_lg)?'privacy':/community|guideline/.test(_lg)?'community':/responsible/.test(_lg)?'responsible':/licen/.test(_lg)?'licenses':'tos'; goTo('legaldoc'); return;} return; }
    if(_cf==='G-05TD'){ if(t.closest('.top .back')){goBack();return;} return; }
    if(_cf==='G-06A'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){goTo('kycpersonal');return;} if(t.closest('.altlink')){goTo('wallet');return;} return; }
    if(_cf==='G-06H'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){cleanTo('withdraw',/^(KYC-|G-06)/);return;} if(t.closest('.altlink')){cleanTo('wallet',/^(KYC-|G-06)/);return;} return; }
    if(_cf==='G-05C'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){sflToast('Account secured');return;} if(t.closest('.listrow')){return;} return; }
    if(_cf==='G-05E'){ if(t.closest('.top .back')){goBack();return;} var _de=t.closest('.btn,.altlink'); if(_de){ if(/resolve/i.test(_de.textContent)){goBack();return;} sflToast('Deletion request submitted');return;} return; }
    if(_cf==='MSG-02'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.search')){return;} if(t.closest('.uresult')||t.closest('.act')){goTo('chatthread');return;} return; }
    if(_cf==='MSG-03'){ var _rc=t.closest('.reqcard'); if(_rc&&(t.closest('.btn')||/block\s*&?\s*report/i.test(t.textContent||''))){ _rc.remove(); var _left=mEl.querySelectorAll('.reqcard').length; if(!_left){var _sc=mEl.querySelector('.scroll'); if(_sc)_sc.innerHTML='<div class="dnote info" style="margin-top:20px">No pending requests. You\\'re all caught up.</div>';} return; } }
    if(_cf==='MSG-04'||_cf==='MSG-05'||_cf==='MSG-04B'){ if(t.closest('.chdr .back')){goBack();return;} var _clb=t.closest('.callbtn'); if(_clb){ if(_cf==='MSG-05'){ showClubChatMenu(); return; } if(_cf==='MSG-04'){var _ct=(_clb.textContent||''); if(/📹/.test(_ct)){goTo('callvideo');return;} if(/📞/.test(_ct)){goTo('callvoice');return;}} return; } if(t.closest('.chdr')){ if(_cf==='MSG-05'){goTo('clubmembers');return;} if(_cf==='MSG-04'){ var _pp=SFLchatPeer||{name:'Olivia S.',avbg:''}; SFLprofilePeer={name:_pp.name,avbg:_pp.avbg,id:_pp.id||'67890',club:_pp.club||'Red Fury'}; goTo('userprofile'); return;} return; } if(t.closest('.msgs')||t.closest('.cbtn.attach')||t.closest('.atchip')||t.closest('.atttray')){return;} }
    if(_cf==='MSG-05M'){ if(t.closest('.top .back')||t.closest('.chdr .back')){goBack();return;} var _mm=t.closest('.memrow'); if(_mm){ SFLprofilePeer=peerFromRow(_mm); goTo('userprofile'); return;} if(t.closest('.search')){return;} return; }
    if(_cf.indexOf('MG-')===0){
      var MGRESULT={'MG-02G':1,'MG-02S':1,'MG-04C':1,'MG-04G':1,'MG-01X':1,'MG-REC':1,'MG-REF':1,'MG-LIM':1};
      var mgbk=t.closest('.top .back'); if(mgbk){var mb=(mgbk.textContent||'').trim(); if(/📜/.test(mb)){goTo('gamehistory');return;} if(mb==='?'){goTo('gamerules');return;} if(/[‹←]/.test(mb)){ if(MGRESULT[_cf]){goTo('gameshub');} else {goBack();} return; }}
      if(_cf==='MG-01'){ var bchip=t.closest('.balchip'); if(bchip){ if(bchip.querySelector('.gc')){goTo('wallet');} return; } if(t.closest('.tile.penalty')){goTo('penalty');return;} if(t.closest('.tile.wheel')){goTo('wheel');return;} return; }
      if(_cf==='MG-01R'){ if(t.closest('.btn')){goBack();return;} return; }
      if(_cf==='MG-05'){ var _hf=t.closest('.fchip'); if(_hf){ singleSel(_hf,_hf.parentElement); var _ht=(_hf.textContent||'').toLowerCase(); [].forEach.call(mEl.querySelectorAll('.hrow'),function(r){ var _hn=((r.querySelector('.hn')||{}).textContent||'').toLowerCase(); var show=true; if(/penalty/.test(_ht)){show=/penalty/.test(_hn);} else if(/wheel/.test(_ht)){show=/wheel/.test(_hn);} else if(/won/.test(_ht)){show=!!r.querySelector('.ha.plus');} else if(/refund/.test(_ht)){show=!!r.querySelector('.ha.ref');} r.style.display=show?'':'none'; }); return;} return; }
      if(_cf==='MG-01X'){ var xb=t.closest('.btn'); if(xb){ if(/buy coins/i.test(xb.textContent)){goTo('coinstore');return;} goTo('penalty');return; } }
      if(_cf==='MG-02'){
        if(t.closest('.altlink')){goTo('gamerules');return;}
        if(t.closest('.mgpk')||t.closest('[data-pk]')) return;
        return;
      }
      if(_cf==='MG-02G'){ if(t.closest('.btn')){goTo('penalty');return;} if(t.closest('.altlink')){goTo('gameshub');return;} }
      if(_cf==='MG-02S'){ if(t.closest('.btn')){goTo('penalty');return;} if(t.closest('.altlink')){goTo('gameshub');return;} }
      if(_cf==='MG-03'){ if(t.closest('.altlink')){goTo('gamerules');return;} if(t.closest('.btn')||t.closest('.wheeldisc')||t.closest('[data-wh]')) return; return; }
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
    var _seatEl=t.closest('.formfield .seat'); if(_seatEl&&!_seatEl.classList.contains('open')){ if(showGuestSheet(_seatEl))return; }
    if(_cf==='GL-03V'||_cf==='GL-05B'){ if(t.closest('.chreq')){ if(SFLguest){goTo('gate');return;} if(isRoomMgr()){goTo('cohostroom');return;} if(SFLchAsk==='pending'){goTo('chsent');return;} goTo('chrequest');return;} if(_cf==='GL-05B'){ if(t.closest('.rrb.gift')){openGiftSheet();return;} var _lv=t.closest('.rrb'); if(_lv){ if(/🚪|leave|end/i.test(_lv.textContent)){sflLeaveLive();return;} _lv.classList.toggle('on'); return; } if(t.closest('.rsay')||t.closest('.cin')||t.closest('.rchat')){return;} return; } if(t.closest('.rrb.join')){ if(isRoomMgr()){ takeSeatSkip(); return; } goTo('squadroom');return;} if(t.closest('.rrb.gift')){openGiftSheet();return;} if(t.closest('.seat.open')){ if(isRoomMgr()){ takeSeatSkip(); return; } requestSeat(t.closest('.seat.open')); return;} if(t.closest('.htool')){goTo('squadroom');return;} if(t.closest('.rsay')||t.closest('.cin')||t.closest('.rchat')){return;} return; }
    if(_cf==='GL-05'){ if(t.closest('.sheetx')||t.classList.contains('sheet-scrim')){ goBack(); return; } var _pr=t.closest('.posrow'); if(_pr){ if(_pr.querySelector('.pb.open')||_pr.querySelector('.opentag')){goTo('confirmseat');} return; } return; }
    if(_cf==='GL-05A'){ if(t.closest('.sheetx')||t.classList.contains('sheet-scrim')){ goTo(chLiveRoom()); return; } if(t.closest('.btn')){ if(isRoomMgr()){ sflToast('Manager seat — no host approval'); takeSeatSkip(); return; } chQueue({id:'join-you',kind:'join',name:'You',pos:'RW',av:'up_12.png'}); sflToast('Request sent to host and managers'); goTo('joinwait'); return;} if(t.closest('.altlink')){goTo('squadroom');return;} return; }
    if(_cf==='GL-05W'){ if(t.closest('[data-ch="canceljoin"]')){ if(window._sflchto){clearTimeout(window._sflchto);window._sflchto=null;} chDrop('join-you'); sflToast('Join request cancelled'); goTo('liveroom'); return;} if(t.closest('[data-ch="backlive"]')||t.closest('.btn')||t.closest('.altlink')||t.classList.contains('sheet-scrim')){goTo('liveroom');return;} return; }
    if(_cf==='GL-05OK'){ if(t.closest('[data-ch="enterpitch"]')||t.closest('.btn')){SFLseated=true;goTo('fanseated');return;} return; }
    if(_cf==='GL-05C'){ if(t.closest('.btn')){goTo('squadroom');return;} if(t.closest('.altlink')){goTo('liveroom');return;} return; }
    if(_cf==='GL-03Vg'){ var _gb=t.closest('.b'); if(_gb){ if(/create/i.test(_gb.textContent)){goTo('register');return;} if(/sign in/i.test(_gb.textContent)){goTo('signin');return;} } if(t.closest('.altlink')){return;} return; }
    if(_cf==='GL-00'){ if(t.closest('.ss-x')){var _sx=mEl.querySelector('.stadsearch'); if(_sx)_sx.classList.remove('on'); return;} if(t.closest('.stadsearch')){return;} if(t.closest('.hbtn')){var _sb=mEl.querySelector('.stadsearch'); if(_sb){_sb.classList.toggle('on');} return;} if(t.closest('.golivecard')){goTo(SFLguest?'gate':'eligibility');return;} if(t.closest('.pkbcard')){ if(SFLguest){goTo('gate');return;} SFLpkViewer=true; goTo('pkbattle');return;} if(t.closest('.wacard')){goTo(SFLguest?'gate':'watchlivev');return;} if(t.closest('.roomcard')){ if(SFLkicked){ showKickedNotice(); return; } goTo('liveroom');return;} var _t0=t.closest('.tab'); if(_t0){singleSel(_t0,_t0.parentElement); var _vw=_t0.getAttribute('data-view'); if(_vw){ [].forEach.call(mEl.querySelectorAll('.scrollarea > [data-view]'),function(s){ s.style.display=(s.getAttribute('data-view')===_vw)?'':'none'; }); } return;} return; }
    if(_cf==='GL-01A'){ if(t.closest('.back')){goBack();return;} if(t.closest('.btn')){goTo('permissions');return;} }
    if(_cf==='GL-01B'){
      if(t.closest('.back')){goBack();return;}
      var _pr=t.closest('.permcard');
      if(_pr){
        var _pk=_pr.getAttribute('data-perm');
        if(!t.closest('[data-perm-act]'))return;
        if(_pk==='camera'&&!SFLperm.camera){ SFLperm.camera=true; applyPermissions(mEl); sflToast('Camera allowed'); return; }
        if(_pk==='mic'&&!SFLperm.mic){ SFLperm.mic=true; applyPermissions(mEl); sflToast('Microphone allowed'); return; }
        if(_pk==='notif'&&SFLperm.notif!=='later'&&SFLperm.notif!=='allowed'){
          SFLperm.notif='later'; applyPermissions(mEl); sflToast('Notifications skipped — enable anytime in Settings'); return;
        }
        return;
      }
      var _pb=t.closest('.btn');
      if(_pb){
        if(_pb.classList.contains('disabled')){ sflToast('Allow camera and microphone to continue'); return; }
        goTo('golivesetup'); return;
      }
      return;
    }
    if(_cf==='GL-01'){ if(t.closest('.btn')){goTo('formation');return;} var _sm=t.closest('.smcard'); if(_sm){singleSel(_sm,_sm.parentElement); var _sc=parseInt(_sm.getAttribute('data-seats')||(_sm.textContent||'').replace(/[^0-9]/g,''),10); if(_sc)SFLseatCount=_sc; return;} }
    if(_cf==='GL-02'){ var _ms=t.closest('.mseg'); if(_ms){ SFLseatMode=_ms.getAttribute('data-mode')||'pos'; applyFormMode(mEl); return; } var _fcc=t.closest('.formcard'); if(_fcc){ var _fnt=((_fcc.querySelector('.fn')||{}).textContent||'').trim(); if(/^\d/.test(_fnt)){ SFLformation=_fnt; SFLseatMode='pos'; singleSel(_fcc,_fcc.parentElement); applyFormMode(mEl); } else { sflToast('More formations coming soon'); } return; } if(t.closest('.btn')){goTo('prelive');return;} }
    if(_cf==='GL-02A'){ if(t.closest('.btn')){goTo('liveroomhost');return;} if(t.closest('.seat.host')||t.closest('.seat.you')){ sflToast("You're the host — always position #1"); return; } var _iseat=t.closest('.seat'); if(_iseat){ var _ip=_iseat.querySelector('.pos'); showInviteSheet(_ip?(_ip.textContent||'').trim():'this position'); return; } if(t.closest('.rrb')){goTo('liveroomhost');return;} }
    if(_cf==='GL-03H'){ if(t.closest('.audstack')){showAudienceSheet();return;} if(t.closest('.chinbox')){goTo('chinbox');return;} var _hr=t.closest('.rrb'); if(_hr){var _ht=_hr.textContent||''; if(_hr.classList.contains('wa')||/▶\s*watch|watch along/i.test(_ht)){goTo('watchpick');return;} if(/manage/i.test(_ht)||/⚙/.test(_ht)){goTo('manageseats');return;} if(_hr.classList.contains('pk')||/⚔/.test(_ht)){goTo('pk');return;} if(_hr.classList.contains('gift')||/🎁/.test(_ht)){openGiftSheet();return;} if(/⏹|end|stop/i.test(_ht)){goTo('endlive');return;} return;} if(t.closest('.htool')){goTo('manageseats');return;} if(t.closest('.seat.open')){goTo('manageseats');return;} var _hcm=t.closest('.rchat .cm'); if(_hcm){ inviteOntoSeat(chatInviteName(_hcm)); return; } return; }
    if(_cf==='GL-WA-01'){
      var _app=t.closest('[data-waapp]'); if(_app){ SFLwaApp=_app.getAttribute('data-waapp')||'yt'; goTo('walogin'); return; }
      var _samp=t.closest('.wasample');
      if(_samp){ var _ue=mEl.querySelector('#wa-url'); if(_ue){ _ue.value=_samp.getAttribute('data-waurl')||'https://youtu.be/sfl-derby-2026'; _ue.classList.add('on'); _ue.focus(); } return; }
      if(t.closest('#wa-url')||t.closest('.waurl')) return;
      if(t.closest('.wastart')||(t.closest('.btn')&&!t.closest('[data-waapp]'))){
        var _uin=mEl.querySelector('#wa-url');
        var _ut=((_uin&&_uin.value)||(_uin&&_uin.textContent)||'').trim();
        if(!_ut||/paste a video/i.test(_ut)){ sflToast('Paste a video URL or pick a platform'); return; }
        waStart(waParseUrl(_ut)); return;
      }
      if(t.closest('.altlink')||t.classList.contains('sheet-scrim')){goBack();return;}
      return;
    }
    if(_cf==='GL-WA-L'){ if(t.closest('[data-wa="signin"]')||t.closest('.wabtn')){ sflToast('Signed in · pick a video'); goTo('wapickvid'); return; } if(t.closest('.waback')||t.closest('[data-wa="cancel"]')||t.closest('.altlink')){goBack();return;} return; }
    if(_cf==='GL-WA-P'){ var _wv=t.closest('[data-wavid]'); if(_wv){ var _app2=WAAPPS[SFLwaApp]||WAAPPS.yt; var _vid=_app2.vids[+_wv.getAttribute('data-wavid')]||_app2.vids[0]; SFLwaSrc={title:_vid.title,file:_vid.file,badge:_app2.badge}; waStart(SFLwaSrc); return; } if(t.closest('.waback')){goBack();return;} return; }
    if(_cf==='GL-WA-H'||_cf==='GL-WA-V'){ var _wsz=t.closest('.wasz'); if(_wsz){ SFLwaSize=_wsz.getAttribute('data-sz')||'md'; applyWaSize(mEl); sflToast(SFLwaSize==='full'?'Player · Full width':(SFLwaSize==='sm'?'Player · Small':'Player · Fit')); return; } }
    if(_cf==='GL-WA-H'){ if(t.closest('.chinbox')){goTo('chinbox');return;} var _wh=t.closest('.rrb'); if(_wh){var _wt=_wh.textContent||''; if(_wh.classList.contains('waend')||/end watch/i.test(_wt)){goTo('watchend');return;} if(/manage/i.test(_wt)||/⚙/.test(_wt)){goTo('manageseats');return;} if(_wh.classList.contains('gift')||/🎁/.test(_wt)){openGiftSheet();return;} if(/⏹/.test(_wt)){goTo('endlive');return;} return;} if(t.closest('.htool')){goTo('manageseats');return;} if(t.closest('.seat.open')){goTo('manageseats');return;} var _wcm=t.closest('.rchat .cm'); if(_wcm){ inviteOntoSeat(chatInviteName(_wcm)); return; } if(t.closest('.rchat')||t.closest('.rsay')||t.closest('.cin')){return;} return; }
    if(_cf==='GL-WA-V'){ if(t.closest('.chreq')){ if(SFLguest){goTo('gate');return;} if(isRoomMgr()){goTo('cohostroom');return;} if(SFLchAsk==='pending'){goTo('chsent');return;} goTo('chrequest');return;} if(t.closest('.rrb.join')||t.closest('.htool')){ if(isRoomMgr()){ takeSeatSkip(); return; } goTo('squadroom');return;} if(t.closest('.rrb.gift')){openGiftSheet();return;} if(t.closest('.seat.open')){ if(isRoomMgr()){ takeSeatSkip(); return; } goTo('confirmseat');return;} if(t.closest('.rsay')||t.closest('.cin')||t.closest('.rchat')){return;} return; }
    if(_cf==='GL-WA-E'){ if(t.closest('.waendyes')||(t.closest('.btn.danger'))){goTo('liveroomhost');sflToast('Watch-Along ended · back on the pitch');return;} if(t.closest('.btn')||t.closest('.altlink')||t.classList.contains('sheet-scrim')){goTo('watchlive');return;} return; }
    if(_cf==='GL-CH-01'){ if(t.closest('[data-ch="send"]')||t.closest('.btn')){ SFLchAsk='pending'; chQueue({id:'ch-you',kind:'cohost',name:'You',pos:'Viewer',av:'up_12.png'}); sflToast('Manager request sent to the host'); goTo('chsent'); return;} if(t.closest('.altlink')||t.classList.contains('sheet-scrim')){goTo(chLiveRoom());return;} return; }
    if(_cf==='GL-CH-02'){ if(t.closest('[data-ch="cancel"]')){ SFLchAsk='none'; chDrop('ch-you'); sflToast('Manager request cancelled'); goTo(chLiveRoom()); return;} if(t.closest('[data-ch="backlive"]')||t.closest('.btn')||t.closest('.altlink')||t.classList.contains('sheet-scrim')){goTo(chLiveRoom());return;} return; }
    if(_cf==='GL-CH-H'){ var _tab=t.closest('[data-chtab]'); if(_tab){ SFLchTab=_tab.getAttribute('data-chtab')||'join'; applyLiveStaff(mEl); return; } var _dec=t.closest('[data-chdec]'); if(_dec){ var _row=_dec.closest('[data-chid]'); chDecide(_row&&_row.getAttribute('data-chid'), _dec.getAttribute('data-chdec')==='ok'); return;} if(t.closest('.top .back')){goBack();return;} if(t.closest('[data-ch="backlive"]')||t.closest('.btn')){ goTo(isRoomMgr()?'cohostroom':'liveroomhost'); return;} return; }
    if(_cf==='GL-CH-C'){ if(t.closest('.chinbox')){goTo('chinbox');return;} if(t.closest('.rrb.gift')){openGiftSheet();return;} if(t.closest('.htool')){goTo('chinbox');return;} var _mcm=t.closest('.rchat .cm'); if(_mcm){ inviteOntoSeat(chatInviteName(_mcm)); return; } if(t.closest('.rchat')||t.closest('.rsay')||t.closest('.cin')){return;} return; }
    if(_cf==='GL-04'){ if(t.closest('.chinbox-banner')){goTo('chinbox');return;} if(t.closest('.btn')){goTo('endlive');return;} var _orow=t.closest('.optrow'); if(_orow){ if(_orow.getAttribute('data-chact')==='toggle'){ chToggle(_orow.getAttribute('data-chname')||'Olivia S.'); return; } if(/·\s*open|close/i.test(_orow.textContent)){return;} goTo('manageparticipant');return;} var _t4=t.closest('.tab,.fillbadge'); if(_t4){singleSel(_t4,_t4.parentElement);return;} }
    if(_cf==='GL-04A'){ var _or=t.closest('.optrow'); if(_or){ var _ot=(_or.textContent||'').toLowerCase(); var _pn=_or.getAttribute('data-chname')||((mEl.querySelector('.seathead .nm')||{}).textContent||'this fan').split('·')[0].trim();
      if(_or.getAttribute('data-chact')==='toggle'||/make manager|remove manager|make co-host|remove co-host/.test(_ot)){ chToggle(_pn); return; }
      if(/block/.test(_ot)){goBack();sflToast(_pn+' removed & blocked');return;}
      if(/remove/.test(_ot)){goBack();sflToast(_pn+' removed from position');return;}
      if(/unmute/.test(_ot)){goBack();sflToast('Unmute requested from '+_pn);return;}
      if(/move/.test(_ot)){showMoveSheet(_pn);return;}
      if(/mute/.test(_ot)){goBack();sflToast(_pn+' muted');return;}
      goBack();return; } return; }
    if(_cf==='GL-06'){ var _eb=t.closest('.btn'); if(_eb){ if(/end/i.test(_eb.textContent)){goTo('livesummary');return;} goBack();return; } }
    if(_cf==='GL-07'){ if(t.closest('.altlink')){goTo('live');return;} if(t.closest('.btn')){sflToast('Highlights shared to your feed 🎬');return;} return; }
    if(_cf.indexOf('PK-')===0){
      var _pbk=t.closest('.top .back'); if(_pbk){goBack();return;}
      if(_cf==='PK-00'){ if(t.closest('.btn')){goTo('pkmatch');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PK-01'){ var _mc=t.closest('.modecard'); if(_mc){var _mct=(_mc.textContent||'').toLowerCase(); if(/quick/.test(_mct)){goTo('pkrandom');return;} if(/id/.test(_mct)){goTo('pkinvite');return;} goTo('live');return;} return; }
      if(_cf==='PK-01B'){ if(t.closest('.btn')){goTo('pkmatchup');return;} return; }
      if(_cf==='PK-01A'){ if(t.closest('.btn')){goTo('pkinvite');return;} if(/cancel search/i.test(t.textContent||'')){goTo('pkmatch');return;} goTo('pkmatchup'); return; }
      if(_cf==='PK-01C'){ var _ca=t.closest('.a'); if(_ca){ if(_ca.classList.contains('acc')||/accept/i.test(_ca.textContent)){goTo('pkbattle');return;} goTo('live');return;} return; }
      if(_cf==='PK-01E'){ if(t.closest('.pkback')){goBack();return;} var _rb=t.closest('.b'); if(_rb){ if(_rb.classList.contains('ready')||/ready/i.test(_rb.textContent)){goTo('pkbattle');return;} goTo('pkrandom');return;} return; }
      if(_cf==='PK-02A'){ goTo('pkbattle'); return; }
      if(_cf==='PK-03'){ if(t.closest('.pkend')){ if(window._sflpkto)clearTimeout(window._sflpkto); if(window._sflpkfin){clearInterval(window._sflpkfin);window._sflpkfin=null;} var _pkw=mEl.querySelector('.pkstwrap'); if(_pkw)_pkw.remove(); sflToast('PK Battle ended · your live continues'); goTo(SFLpkViewer?'liveroom':'liveroomhost'); return; } if(t.closest('.gbtn')){goTo('pkside');return;} if(t.closest('.pktimer')||t.closest('.vid')||t.closest('.scrim')){goTo('pkfinalizing');return;} return; }
      if(_cf==='PK-03A'){ if(t.closest('.btn')){goTo('pkleadchange');return;} if(t.closest('.altlink')){goTo('coinstore');return;} var _gi=t.closest('.gi'); if(_gi){singleSel(_gi,_gi.parentElement);return;} return; }
      if(_cf==='PK-03B'){ goTo('pkfinalizing'); return; }
      if(_cf==='PK-03D'){ goTo('pkwin'); return; }
      if(_cf==='PK-04A'||_cf==='PK-04C'){ var _wb=t.closest('.b'); if(_wb){ if((_wb.classList.contains('re')||/rematch/i.test(_wb.textContent))&&!SFLpkViewer){goTo('pkrematch');return;} if(window._sflpkto)clearTimeout(window._sflpkto); if(window._sflpkfin){clearInterval(window._sflpkfin);window._sflpkfin=null;} goTo(SFLpkViewer?'liveroom':'liveroomhost');return;} return; }
      if(_cf==='PK-04D'){ if(t.closest('.btn')){goTo('pkbattle');return;} if(t.closest('.altlink')){goTo('live');return;} return; }
    }
    if(_cf.indexOf('PL-')===0){
      var _plbk=t.closest('.top .back, .dnav .back'); if(_plbk){goBack();return;}
      if(_cf==='PL-00'){ if(t.closest('.btn')){goTo('market');return;} return; }
      if(_cf==='PL-01'){ if(t.closest('.plsearch')){goTo('plfilters');return;} var _pc=t.closest('.pcard'); if(_pc){SFLpl=plFromEl(_pc); if(_pc.getAttribute('data-mine')){sflToast('Your listing · other fans can take this player');return;} goTo('playerdetail');return;} var _pfc=t.closest('.fchip'); if(_pfc){ singleSel(_pfc,_pfc.parentElement); var _pf=_pfc.getAttribute('data-plfilter')||''; [].forEach.call(mEl.querySelectorAll('.pcard'),function(c){ var k=c.getAttribute('data-kind')||'transfer', pos=c.getAttribute('data-pos')||'', show=true; if(_pf==='transfer')show=k==='transfer'; else if(_pf==='loan')show=k==='loan'; else if(_pf==='fwd')show=pos==='fwd'; else if(_pf==='mid')show=pos==='mid'; c.style.display=show?'':'none'; }); return;} return; }
      if(_cf==='PL-01A'){ if(t.closest('.btn')){goBack();return;} var _pf2=t.closest('.fchip'); if(_pf2){singleSel(_pf2,_pf2.parentElement);return;} return; }
      if(_cf==='PL-02'){ if(t.closest('.btn')){goTo(SFLguest?'gate':'plbuy');return;} return; }
      if(_cf==='PL-02A'){ if(t.closest('.btn')){goTo('plbuy');return;} if(t.closest('.altlink')){goTo('market');return;} return; }
      if(_cf==='PL-03'){ if(t.closest('.btn')){goTo('plescrow');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PL-03A'){ var _b3=t.closest('.btn,.link'); if(_b3){ if(/buy coins/i.test(_b3.textContent)){goTo('coinstore');return;} goTo('market');return;} return; }
      if(_cf==='PL-04'){ if(t.closest('.link')){goTo('support');return;} if(t.closest('.plcont')){goTo('plcomplete');return;} if(t.closest('.btn')){goTo('plcomplete');return;} return; }
      if(_cf==='PL-04A'){ var _b4=t.closest('.btn,.link'); if(_b4){ if(/wallet/i.test(_b4.textContent)){goTo('wallet');return;} goTo('market');return;} return; }
      if(_cf==='PL-05'){ if(t.closest('.btn')){ var _pd=plDutyCounts(); if(/weekly|other pick/i.test((t.closest('.btn').textContent||''))){ if(_pd.buy>=2){cleanTo('tasksweekly', /^PL-0[1-5W]/);return;} goTo('plweeklybuys'); return; } cleanTo('myplayers', /^PL-0[2-5]/);return;} if(t.closest('.link')){cleanTo('market', /^PL-0[1-5]$/);return;} return; }
      if(_cf==='PL-06'){ var _rec=t.closest('[data-plrec]'); if(_rec){ SFLpl=_rec.getAttribute('data-plrec')||plFromEl(_rec); SFLplWeeklyBuy=true; goTo('playerdetail'); return; } if(t.closest('[data-plact="weeklybuys"]')){ goTo('plweeklybuys'); return; } var _pr=t.closest('.prow'); if(_pr){SFLpl=plFromEl(_pr);goTo('plactions');return;} var _ptb=t.closest('.tabs i'); if(_ptb){singleSel(_ptb,_ptb.parentElement); applyPlSquad(mEl); return;} return; }
      if(_cf==='PL-06A'){ if(t.closest('.altlink')){goBack();return;} var _pa=t.closest('[data-plact]'); if(_pa){ var _act=_pa.getAttribute('data-plact'); if(_act==='transfer'){SFLplKind='transfer';goTo('pllist');return;} if(_act==='loan'){SFLplKind='loan';goTo('plloan');return;} if(_act==='unlist'){plUnlist();cleanTo('myplayers',/^PL-06A$/);return;} } return; }
      if(_cf==='PL-07'){ if(t.closest('.btn')){ if(!plRecordList('transfer'))return; goTo('pllistlive');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PL-07L'){ var _ld=t.closest('.durchip'); if(_ld){ singleSel(_ld,_ld.parentElement); SFLplLoan=_ld.getAttribute('data-loan')||'1 week'; applyPlLoan(mEl); return; } if(t.closest('.btn')){ if(!plRecordList('loan'))return; goTo('plloanlive');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='PL-01W'){ var _wr=t.closest('[data-plrec],.recrow'); if(_wr){ SFLpl=_wr.getAttribute('data-plrec')||plFromEl(_wr); SFLplWeeklyBuy=true; goTo('playerdetail'); return; } if(t.closest('[data-plact="buyfirst"]')||t.closest('.btn')){ var _recs=plMatchRecs(), _ri=0; while(_ri<_recs.length&&SFLplBought[_recs[_ri]])_ri++; SFLpl=_recs[_ri]||_recs[0]||'okoro'; SFLplWeeklyBuy=true; goTo('plbuy'); return; } if(t.closest('[data-plact="backsell"]')||t.closest('.link')){ cleanTo('myplayers',/^PL-01W$/); return; } return; }
      if(_cf==='PL-08'||_cf==='PL-08L'){ if(t.closest('[data-plact="unlist"]')||/unlist/i.test((t.closest('.link')||{}).textContent||'')){ plUnlist(); cleanTo('myplayers',/^PL-06|^PL-07|^PL-08/); return; } if(t.closest('.btn')){ if(_cf==='PL-08'&&plDutyCounts().sell>=2){ goTo('plweeklybuys'); return; } if(_cf==='PL-08'){ cleanTo('myplayers',/^PL-06|^PL-07|^PL-08/); return; } cleanTo('market',/^PL-06|^PL-07|^PL-08/); return; } return; }
      if(_cf==='PL-09'){ goTo('plsold'); return; }
      if(_cf==='PL-10'){ var _b10=t.closest('.btn,.link'); if(_b10){ var _pldone=/^PL-0[6-9]|^PL-10$|^PL-07L$|^PL-08L$|^G-03$/; if(/wallet/i.test(_b10.textContent)){cleanTo('wallet',_pldone);return;} cleanTo('market',_pldone);return;} return; }
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
          if(/buy|sell|player|transfer|loan/.test(_tt)){goTo('taskbuysell');return;}
          if(/active day/.test(_tt)){goTo('progression');return;}
          if(/support/.test(_tt)){goTo('clubchat');return;}
          if(/event/.test(_tt)){goTo('clubevents');return;}
          if(/watch/.test(_tt)){goTo('taskdetail');return;}
          goTo('taskdetail'); return; }
        if(t.closest('.btn')){goTo(_cf==='FT-02'?'tasksweeklydone':'tasksdone');return;}
        if(t.closest('.ringhero')){return;}
      }
      if(_cf==='FT-03P'){ var _fta=(t.closest('[data-ftact]')||{}).getAttribute&&t.closest('[data-ftact]').getAttribute('data-ftact'); var _ftbtn=t.closest('.btn'); var _ftbuy=_fta==='buyrecs'||/buy the 2|buy 2 player|recommend/i.test((_ftbtn||{}).textContent||''); if(_ftbuy){ if(plDutyCounts().sell<2) sflToast('List 2 players first · you pick the sells'); goTo('plweeklybuys'); return; } if(_ftbtn||_fta==='list2'){ goTo('myplayers'); return; } return; }
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
    if(_cf.indexOf('PR-')===0||_cf.indexOf('TR-')===0){
      var _prbk=t.closest('.top .back'); if(_prbk){goBack();return;}
      if(_cf.indexOf('TR-')===0){
        if(t.closest('.ttable')||t.closest('.ttr')||t.closest('.thd')||t.closest('.squadrow')||t.closest('.grouppill')||t.closest('.countrypill')){return;}
        if(_cf==='TR-01'){ var _tc1=t.closest('.tourcard'); if(_tc1){ if(_tc1.classList.contains('soon')){sflToast('Registration opens soon');return;} if(SFLtournReg){goTo('tourndash');return;} goTo('tournnotify');return;} return; }
        if(_cf==='TR-02'){ if(t.closest('.btn')){goTo('tournconfirm');return;} if(t.closest('.ruleslink')){goTo('tournrules');return;} return; }
        if(_cf==='TR-03'){ if(t.closest('.btn')){goTo('tournpay');return;} if(t.closest('.ruleslink')){goTo('tournrules');return;} return; }
        if(_cf==='TR-04'){ if(t.closest('.btn')){ if(SFLtournCoins<500){sflToast('Not enough Coins · need 500');return;} SFLtournReg=true; SFLtournCoins-=500; sflToast('500 Coins deducted · you\\'re registered!'); goTo('tournsuccess'); return;} if(t.closest('.altlink')){goBack();return;} return; }
        if(_cf==='TR-05'){ if(t.closest('.btn')){goTo('tourndash');return;} return; }
        if(_cf==='TR-06'){ if(t.closest('.btn')){goTo('tournpayout');return;} if(t.closest('.ruleslink')){goTo('tournrules');return;} if(t.closest('.altlink')){goTo('tournteam');return;} return; }
        if(_cf==='TR-07'){ if(t.closest('.btn')){goTo('tourndash');return;} if(t.closest('.altlink')){goTo('tournteam');return;} return; }
        if(_cf==='TR-08'){ if(t.closest('.ruleslink')){goTo('tournrules');return;} return; }
        if(_cf==='TR-09'){ if(t.target.closest('.sheet-scrim')===t||t.closest('.grab')||t.closest('.btn')){goBack();return;} return; }
      }
      if(_cf==='PR-02C'&&t.closest('.spr')){goTo('clubdetail');return;}
      if(t.closest('.lgr')||t.closest('.pod')||t.closest('.podium')||t.closest('.lgtable')||t.closest('.ttr')||t.closest('.ttable')||t.closest('.thd')||t.closest('.lgcount')||t.closest('.spendhero')||t.closest('.grouplabel')){return;}
      var _lgt2=t.closest('.lgtab'); if(_lgt2){var _lx2=_lgt2.textContent.toLowerCase(); if(/spend/.test(_lx2)){goTo('leaguespend');return;} if(/previous|prev/.test(_lx2)){goTo('leagueprev');return;} singleSel(_lgt2,_lgt2.parentElement); return;}
      var _ttb=t.closest('.ttab'); if(_ttb){singleSel(_ttb,_ttb.parentElement);return;}
      if(_cf==='PR-00'){ var _hc=t.closest('.hubcard'); if(_hc){ if(_hc.classList.contains('lvl')){goTo('fanlevel');return;} if(_hc.classList.contains('league')){goTo('league');return;} if(_hc.classList.contains('tour')){goTo(SFLtournReg?'tourndash':'tournhub');return;} if(_hc.classList.contains('grade')){goTo('clubgrade');return;} } return; }
      if(_cf==='PR-01'){ if(t.closest('.btn')){goTo('howtoearn');return;} if(t.closest('.altlink')){goTo('levelroadmap');return;} return; }
      if(_cf==='PR-01A'){ if(t.closest('.top .back')){goBack();return;} var _ar=t.closest('.actrow'); if(_ar&&_ar.getAttribute('data-go')){goTo(_ar.getAttribute('data-go'));return;} return; }
      if(_cf==='PR-04'){ if(t.closest('.btn,.altlink')){goTo('prizeeligibility');return;} return; }
      if(_cf==='PR-04B'){ if(t.closest('.btn')){goTo('rewards');return;} return; }
      if(_cf==='PR-02D'){ if(t.closest('.btn')){goBack();return;} return; }
      if(_cf==='PR-01C'){ var _c1c=t.closest('.btn,.altlink'); if(_c1c){ if(/benefit/i.test(_c1c.textContent)){goTo('levelroadmap');return;} goBack();return;} return; }
    }
    if(_cf.indexOf('WA-')===0||_cf.indexOf('KYC-')===0){
      var _wbk=t.closest('.top .back'); if(_wbk){ if(/🧾/.test(_wbk.textContent)){goTo('wallethist');return;} goBack(); return; }
      if(_cf==='WA-01'){ if(t.closest('.csentry')||t.closest('[data-go="csellers"]')){goTo('csellers');return;} if(t.closest('[data-go="csdesk"]')){goTo('csdesk');return;} if(t.closest('[data-go="csinv"]')){goTo('csinv');return;} var _ab=t.closest('.ab'); if(_ab){var _at=_ab.textContent.toLowerCase(); if(/buy coins/.test(_at)){goTo('coinstore');return;} if(/convert/.test(_at)){goTo('convert');return;} if(/transfer/.test(_at)){goTo('gtransfer');return;} if(/withdraw/.test(_at)){goTo('withdraw');return;}} if(t.closest('.kycrow')){goTo('kycverify');return;} return; }
      if(_cf==='WA-01A'){ if(t.closest('.btn')){goBack();return;} return; }
      if(_cf==='WA-02'){ if(t.closest('.swapbtn')){return;} if(t.closest('.btn')){goTo('convertconfirm');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-02B'){ if(t.closest('.btn')){goTo('convertdone');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-02D'){ if(t.closest('.btn')){returnTo('WA-01','wallet');return;} if(t.closest('.altlink')){goTo('convert');return;} return; }
      if(_cf==='WA-03'){ if(t.closest('.btn')){goTo('transferamount');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-03A'){ if(t.closest('.btn')){goTo('transferconfirm');return;} return; }
      if(_cf==='WA-03B'){ if(t.closest('.btn')){returnTo('WA-01','wallet'); sflToast('200 Gold sent to Mikael K.'); return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-03F'){ var _f3=t.closest('.btn'); if(_f3){ if(/withdraw/i.test(_f3.textContent)){goTo('withdraw');return;} goTo('gtransfer');return;} return; }
      if(_cf==='KYC-01'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){goTo('kycpersonal');return;} if(t.closest('.altlink')){goTo('profile');return;} return; }
      if(_cf==='KYC-01A'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){goTo('kycdoc');return;} return; }
      if(_cf==='KYC-02'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){goTo('kycselfie');return;} return; }
      if(_cf==='KYC-03'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.btn')){goTo('kycreview');return;} if(t.closest('.altlink')){sflToast('Payout method is set during withdrawal');return;} return; }
      if(_cf==='KYC-04'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.kedit')){goBack();return;} if(t.closest('.btn')){cleanTo('kycverified',/^(KYC-|G-06A)/);return;} return; }
      if(_cf==='WA-04A'){ var _so=t.closest('.srcopt'); if(_so){singleSel(_so,_so.parentElement);return;} if(t.closest('.btn')){goTo('withdrawconfirm');return;} return; }
      if(_cf==='WA-04C'){ if(t.closest('.btn')){goTo('withdrawproc');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='WA-04D'){ if(t.closest('.btn')){ goTo('wallet'); if(hist.length){var _whp=ANCH['profile']; hist[hist.length-1]={j:FLOWN+_whp[0], s:(typeof _whp[1]==='number')?_whp[1]:idxOfFnum(_whp[0],_whp[1])};} return;} return; }
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
      if(_cf==='CC-00'){ if(t.closest('.top .back')){goBack();return;} if(t.closest('.ccbuy')){SFLmgrBuying=true;goTo('coinstore');return;} if(t.closest('.ccgo')){ if(SFLmgrEligible){goTo('ccstart');return;} sflToast('You need 5,000+ Coins first — tap “Get 5,000 Coins”.'); return;} return; }
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
      if(t.closest('.clubmore')){ showClubOptsSheet(); return; }
      var _j16bk=t.closest('.hnav .back'); if(_j16bk){ if(/‹|←/.test(_j16bk.textContent||'')){goBack();} return; }
      if(t.closest('.cmgrask')){goTo('cmgrask');return;}
      if(t.closest('.sbtn')){goTo('clubchat');return;}
      var _q16=t.closest('.qa'); if(_q16){var _qq=(_q16.textContent||'').toLowerCase(); if(/task/.test(_qq)){goSectionFromClub('tasks');return;} if(/live/.test(_qq)){goSectionFromClub('live');return;} if(/reward/.test(_qq)){goSectionFromClub('rewards');return;} if(/league/.test(_qq)){goSectionFromClub('league');return;} return;}
      var _lv16=t.closest('.lvcard'); if(_lv16){var _lvb2=_lv16.querySelector('.lvb'); if(_lvb2&&/pk/i.test(_lvb2.textContent)){SFLpkViewer=true;goTo('pkbattle');return;} goTo('liveroom');return;}
      if(t.closest('.btn.club')){goTo('squadroom');return;}
      return;
    }
    if(_cf==='J2-21'){ if(t.closest('.btn')){goTo(SFLfvActive?'fvalready':'fvconfirm');return;} if(t.closest('.link')){goTo('fvexplain');return;} return; }
    if(_cf.indexOf('J2-')===0){
      if(t.closest('.clubmore')){ showClubOptsSheet(); return; }
      var _j2bk=t.closest('.top .back, .hnav .back:not(.clubmore)'); if(_j2bk){ if(/‹|←/.test(_j2bk.textContent||'')){goBack();} return; }
      if(_cf==='J2-01'){ var _b1=t.closest('.btn'); if(_b1){ if(/recruit/i.test(_b1.textContent)){goTo('clubdetail');return;} goTo('clubs');return;} return; }
      if(_cf==='J2-02'){ var _ct=t.closest('.ctab'); if(_ct){var _cx=_ct.textContent.toLowerCase(); if(/my club/.test(_cx)){goTo('club');return;} if(/league/.test(_cx)){goTo('league');return;} jumpTab('clubs'); return;} var _ico=t.closest('.ico'); if(_ico){ if(/🔍/.test(_ico.textContent)){goTo('clubsearch');return;} if(/🔔/.test(_ico.textContent)){goTo('notifications');return;} return;} if(t.closest('.vcard')||t.closest('.apply')){goTo('clubdetail');return;} return; }
      if(_cf==='J2-03'){ if(t.closest('.searchbar')){return;} var _f3=t.closest('.fchip'); if(_f3){singleSel(_f3,_f3.parentElement);return;} if(t.closest('.vcard')||t.closest('.recent')){goTo('clubdetail');return;} return; }
      if(_cf==='J2-04'){ goTo('clubdetail'); return; }
      if(_cf==='J2-05'){ if(t.closest('.roomtile')){goTo('liveroom');return;} var _b5=t.closest('.btn'); if(_b5){ if(/preview/i.test(_b5.textContent)){goTo(SFLguest?'gate':'club');return;} if(SFLmember&&/enter club/i.test(_b5.textContent)){goTo('club');return;} goTo(SFLguest?'gate':(SFLmember?'clubblocked':'clubapply'));return;} return; }
      if(_cf==='J2-06'){ if(t.closest('.btn')){goTo('clubsubmitted');return;} if(t.closest('.altlink')){goBack();return;} return; }
      if(_cf==='J2-07'){ var _b7=t.closest('.btn'); if(_b7){ var _t7=_b7.textContent.toLowerCase(); if(/application/.test(_t7)){cleanTo('clubapplications',/^J2-0[456]$/);return;} if(/live/.test(_t7)){cleanTo('live',/^J2-0/);return;} cleanTo('clubs',/^J2-0/);return;} return; }
      if(_cf==='J2-08'){ if(t.closest('.wd-discover')){cleanTo('clubs',/^J2-0/);return;} var _b8=t.closest('.btn'); if(_b8){ if(/enter club/i.test(_b8.textContent)){goTo('clubconfirmed');return;} if(/withdraw/i.test(_b8.textContent)){showWithdrawSheet();return;} } return; }
      if(_cf==='J2-10'){ var _b10=t.closest('.btn'); if(_b10){ if(/task/i.test(_b10.textContent)){enterAfterJoin('tasks');return;} enterAfterJoin('club');return;} return; }
      if(_cf==='J2-11'){ if(t.closest('.btn')){goTo('clubs');return;} return; }
      if(_cf==='J2-12'){ if(t.closest('.btn')){goTo('clubinvite');return;} return; }
      if(_cf==='J2-13'){ var _b13=t.closest('.btn'); if(_b13){ if(/decline/i.test(_b13.textContent)){goTo('clubdecline');return;} goTo(SFLmember?'clubblocked':'clubinviteaccepted');return;} return; }
      if(_cf==='J2-14'){ var _r14=t.closest('.radio'); if(_r14){singleSel(_r14,_r14.parentElement);return;} var _b14=t.closest('.btn'); if(_b14){ if(/keep/i.test(_b14.textContent)){goBack();return;} goTo('clubs');return;} return; }
      if(_cf==='J2-15'){ var _b15=t.closest('.btn'); if(_b15){ if(/task/i.test(_b15.textContent)){enterAfterJoin('tasks');return;} enterAfterJoin('club');return;} return; }
      if(_cf==='J2-18'){ var _b18=t.closest('.btn,.link'); if(_b18){ if(/continue leaving/i.test(_b18.textContent)){goTo('clubleaveconfirm');return;} goBack();return;} return; }
      if(_cf==='J2-19'){ var _b19=t.closest('.btn'); if(_b19){ if(/leave club/i.test(_b19.textContent)){ SFLleaveAsk='pending'; goTo('leavepending'); return;} goBack();return;} return; }
      if(_cf==='J2-LV'){ var _blv=t.closest('.btn'); if(_blv){ var _lvt=_blv.textContent.toLowerCase(); function _lvpop(){ while(hist.length){var _hl=hist[hist.length-1];var _fl=((VIEWS[_hl.j]&&VIEWS[_hl.j].screens[_hl.s])||{}).fnum||'';if(/^J2-(18|19|LV)$/.test(_fl)){hist.pop();}else break;} } if(/complete leaving/.test(_lvt)){ _lvpop(); SFLmember=false; SFLleaveAsk='none'; hist.length=0; goTo('noclub'); sflToast('You left Red District FC'); return;} if(/withdraw/.test(_lvt)){ _lvpop(); SFLleaveAsk='none'; goTo('club'); sflToast('Leave request withdrawn'); return;} _lvpop(); goTo('club'); return;} return; }
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
    if(_cf==='MC-02'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.cp')||t.closest('.linkbox')){sflToast('🔗 Invite link copied');return;} if(t.closest('.byidbtn')){goTo('mgraddid');return;} if(t.closest('.row2')){showShareSheet();return;} if(t.closest('.btn')){goTo('mgrhistory');return;} return; }
    if(_cf==='MC-02H'){ if(t.closest('.htop .back')){goBack();return;} var _hf=t.closest('.hfilt'); if(_hf){singleSel(_hf,_hf.parentElement);return;} return; }
    if(_cf==='MC-02A'){ if(t.closest('.htop .back')){goBack();return;} var _msb=t.closest('.btn'); if(_msb){ if(/sfl chat/i.test(_msb.textContent)){goTo('clubchat');return;} sflToast('🔗 Invite link copied');return;} if(t.closest('.altlink')){showShareSheet();return;} return; }
    if(_cf==='MC-05'){ if(t.closest('.htop .back')){goBack();return;} var _sc=t.closest('.scout'); if(_sc){var _sb=t.closest('.btn'); if(_sb){var _acc=/accept/i.test(_sb.textContent); var _snm=((_sc.querySelector('.sn')||{}).textContent||'Fan').trim(); _sc.remove(); sflToast(_acc?(_snm+' accepted into the club'):(_snm+' rejected')); if(!mEl.querySelectorAll('.scout').length){var _scr=mEl.querySelector('.scroll'); if(_scr)_scr.innerHTML='<div class="note info" style="margin-top:20px">No pending applications right now.</div>';} return;} } return; }
    if(_cf==='MC-06'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.btn')){goTo('mgrinvitesent');return;} return; }
    if(_cf==='MC-06R'){ if(t.closest('.htop .back')){cleanTo('managerhq', /^MC-0[26]/);return;} var _r6=t.closest('.btn,.altlink'); if(_r6){ if(/another/i.test(_r6.textContent)){goTo('mgraddid');return;} goTo('mgrapplications');return;} return; }
    if(_cf==='MC-07'){ if(t.closest('.htop .back')){goBack();return;}
      var _mtab=t.closest('.tabs .tab'); if(_mtab){singleSel(_mtab,_mtab.parentElement);return;}
      var _tf=t.closest('.transfer'); if(_tf){ var _ab=t.closest('.btn'); if(_ab){ if(_ab.classList.contains('dis')){return;} var _appr=/approve/i.test(_ab.textContent); var _tnm=((_tf.querySelector('.fnm')||{}).textContent||'Request').trim(); _tf.remove(); sflToast(_appr?(_tnm+' — transfer approved'):(_tnm+' — rejected')); return;} goTo('mgrapprovaldetail'); return; }
      return; }
    if(_cf==='MC-07D'){ if(t.closest('.htop .back')||t.closest('.top .back')){goBack();return;} var _b7d=t.closest('.btn'); if(_b7d){ if(/reject/i.test(_b7d.textContent)){goBack();sflToast('Move rejected · fan notified');return;} if(/chat/i.test(_b7d.textContent)){goTo('chatthread');return;} goBack();sflToast('Move approved · membership updating'+moveSplitToast());return;} return; }
    if(_cf==='MC-00'){ if(t.closest('.htop .back')){goBack();return;} var _cr0=t.closest('.clubrow'); if(_cr0){ if(_cr0.classList.contains('susp')){sflToast('This club is suspended · review pending');return;} [].forEach.call(mEl.querySelectorAll('.clubrow'),function(c){c.classList.remove('sel');}); _cr0.classList.add('sel'); goTo('managerhq'); return;} var _mb0=t.closest('.btn'); if(_mb0){ if(/create/i.test(_mb0.textContent)){goTo('createclub');return;} goTo('managerhq');return;} return; }
    if(_cf==='MC-01'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.fanview')){goTo('club');return;} var _mhi=t.closest('.hicon'); if(_mhi){ if(/🔔/.test(_mhi.textContent)){goTo('notifications');return;} goTo('profile');return;} if(t.closest('[data-cmgo="queue"]')){goTo('cmgrqueue');return;} var _msh=t.closest('.short'); if(_msh){var _mst=(_msh.textContent||'').toLowerCase(); if(/fan list/.test(_mst)){goTo('mgrfanlist');return;} if(/application/.test(_mst)){goTo('mgrapplications');return;} if(/add by id/.test(_mst)){goTo('mgraddid');return;} if(/recruit/.test(_mst)){goTo('mgrrecruit');return;} if(/reward/.test(_mst)){goTo('mgrrewards');return;} if(/approval/.test(_mst)){goTo('mgrapprovals');return;} if(/co-manager/.test(_mst)){goTo('cmgrqueue');return;} return;} if(t.closest('.recruit')){goTo('mgrrecruit');return;} if(t.closest('.target')){goTo('mgrbreakdown');return;} var _mst2=t.closest('.stat'); if(_mst2){var _msx=(_mst2.textContent||'').toLowerCase(); if(/wallet/.test(_msx)){goTo('wallet');return;} if(/tier|commission/.test(_msx)){goTo('mgrcommission');return;} if(/league|grade/.test(_msx)){goTo('league');return;} goTo('mgrfanlist');return;} return; }
    if(_cf==='MC-01A'){ if(t.closest('.htop .back')){goBack();return;} return; }
    if(_cf==='MC-01B'){ if(t.closest('.htop .back')){goBack();return;} return; }
    if(_cf==='MC-03'){ if(t.closest('.htop .back')){goBack();return;} var _r3=t.closest('.tabs .tab'); if(_r3){singleSel(_r3,_r3.parentElement);return;} if(t.closest('.btn')){sflToast('350 Coins claimed to Club Wallet');return;} return; }
    if(_cf==='MC-04'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('.search')){return;} var _f4=t.closest('.fchip'); if(_f4){ singleSel(_f4,_f4.parentElement); var _fk=(_f4.textContent||'').toLowerCase(); var _fcard=mEl.querySelector('.scroll .card'); if(_fcard){ var _frows=[].slice.call(_fcard.querySelectorAll('.fanrow')); var _pv=function(el,re){var st=el.querySelector('.stats'); var m=st?(st.textContent||'').match(re):null; return m?parseFloat(m[1]):0;}; var _val=function(r){var b=r.querySelector('.fvbadge'); var m=b?(b.textContent||'').match(/([\\d,]+)/):null; return m?parseFloat(m[1].replace(/,/g,'')):0;}; _frows.sort(function(a,b){ if(/active/.test(_fk))return _pv(b,/(\\d+)d/)-_pv(a,/(\\d+)d/); if(/live/.test(_fk))return _pv(b,/([\\d.]+)h/)-_pv(a,/([\\d.]+)h/); if(/newest/.test(_fk))return _pv(a,/(\\d+)d/)-_pv(b,/(\\d+)d/); return _val(b)-_val(a); }); _frows.forEach(function(r){_fcard.appendChild(r);}); } return; } var _fr4=t.closest('.fanrow'); if(_fr4){ SFLcmgrPick={id:_fr4.getAttribute('data-fan')||'priya',name:_fr4.getAttribute('data-fname')||'Olivia M.',fid:_fr4.getAttribute('data-fid')||'',av:_fr4.getAttribute('data-av')||'up_11.png',lv:_fr4.getAttribute('data-lv')||'',fv:_fr4.getAttribute('data-fv')||''}; goTo('mgrfandetail');return;} return; }
    if(_cf==='MC-04A'){ if(t.closest('.htop .back')){goBack();return;} var _b4a=t.closest('.btn,.altlink'); if(_b4a){ if(_b4a.getAttribute('data-cmact')==='make'||/make manager|already a manager|invite pending/i.test(_b4a.textContent||'')){ if(_b4a.classList.contains('dis')){ sflToast(SFLcmgrStaff[(SFLcmgrPick&&SFLcmgrPick.id)||'priya']?'Already a manager of this club':'Invite already pending'); return; } goTo('cmgrmake'); return; } if(/remove/i.test(_b4a.textContent)){goTo('mgrremovefan');return;} if(/chat/i.test(_b4a.textContent)){goTo('chatthread');return;} if(/move/i.test(_b4a.textContent)){goTo('createoffer');return;} } return; }
    if(_cf==='MC-CM-01'){ if(t.closest('.htop .back')||t.closest('.altlink')){goBack();return;} if(t.closest('[data-cmact="send"]')||t.closest('.btn')){ var _cp=SFLcmgrPick||{}; var _cid=_cp.id||'priya'; cmgrUpsert({id:'inv-'+_cid,kind:'invite',name:_cp.name||'Olivia M.',av:_cp.av||'up_11.png',status:'pending'}); SFLcmgrInvite='pending'; sflToast('Manager invite sent · fan notified'); goTo('cmgrinvsent'); return; } return; }
    if(_cf==='MC-CM-02'){ if(t.closest('.htop .back')){goTo('mgrfanlist');return;} return; }
    if(_cf==='MC-CM-03'){ if(t.closest('.htop .back')){goTo('managerhq');return;} if(t.closest('[data-cmact="hq"]')||t.closest('.btn')){goTo('managerhq');return;} if(t.closest('.altlink')){goTo('mgrfanlist');return;} return; }
    if(_cf==='MC-CM-Q'){ if(t.closest('.htop .back')){goBack();return;} var _cmt=t.closest('[data-cmtab]'); if(_cmt){ SFLcmgrTab=_cmt.getAttribute('data-cmtab')||'ask'; applyCmgrQueue(mEl); return; } var _cmr=t.closest('[data-cmid]'); if(_cmr){ var _qid=_cmr.getAttribute('data-cmid'); var _qdec=(t.closest('[data-cmdec]')||{}).getAttribute&&t.closest('[data-cmdec]').getAttribute('data-cmdec'); if(!_qdec) return; var _qq=cmgrFind(_qid); if(!_qq||_qq.status!=='pending') return; if(_qdec==='accept'){ _qq.status='accepted'; cmgrMark(_qq); if(_qid==='ask-you'||_qid.indexOf('inv-')===0){ cmgrGrant(_qid==='ask-you'?'you':(_qid.slice(4)||SFLcmgrPick.id)); sflToast('You are now a manager'); goTo('cmgryes'); return; } sflToast(_qq.name+' is now a manager · they were notified'); applyCmgrQueue(mEl); applyCmgrHqBadge(mEl); return; } _qq.status='rejected'; if(_qid==='ask-you'){ SFLcmgrAsk='rejected'; goTo('cmgrno'); return; } if(_qid.indexOf('inv-')===0){ SFLcmgrInvite='rejected'; goTo('cmgrno'); return; } sflToast(_qq.name+' was declined · they were notified'); applyCmgrQueue(mEl); applyCmgrHqBadge(mEl); return; } return; }
    if(_cf==='MC-CM-F1'){ if(t.closest('.htop .back')){goBack();return;} if(t.closest('[data-cmact="accept"]')){ cmgrGrant(SFLcmgrPick.id); var _iacc=cmgrFind('inv-'+(SFLcmgrPick.id||'priya')); if(_iacc)_iacc.status='accepted'; sflToast('You are now a manager'); goTo('cmgryes'); return; } if(t.closest('[data-cmact="reject"]')){ SFLcmgrInvite='rejected'; var _irej=cmgrFind('inv-'+(SFLcmgrPick.id||'priya')); if(_irej)_irej.status='rejected'; goTo('cmgrno'); return; } return; }
    if(_cf==='MC-CM-F2'){ if(t.closest('.htop .back')||t.closest('.altlink')){goBack();return;} if(t.closest('[data-cmact="ask"]')||t.closest('.btn')){ SFLcmgrAsk='pending'; cmgrUpsert({id:'ask-you',kind:'ask',name:'You',av:'up_12.png',status:'pending'}); sflToast('Request sent to the manager'); goTo('cmgrsent'); return; } return; }
    if(_cf==='MC-CM-F3'){ if(t.closest('.htop .back')){goTo('club');return;} return; }
    if(_cf==='MC-CM-F4'){ if(t.closest('.htop .back')){goTo('profile');return;} if(t.closest('[data-cmact="hq"]')||t.closest('.btn')){goTo('managerhq');return;} if(t.closest('.altlink')){goTo('profile');return;} return; }
    if(_cf==='MC-CM-F5'){ if(t.closest('.htop .back')||t.closest('.btn')||t.closest('.altlink')){goTo('club');return;} return; }
    if(_cf==='MC-04B'){ if(t.closest('.htop .back')){goBack();return;} var _ro=t.closest('.reasonopt'); if(_ro){singleSel(_ro,_ro.parentElement);return;} var _b4b=t.closest('.btn,.altlink'); if(_b4b){ if(/confirm/i.test(_b4b.textContent)){goBack();sflToast('Fan removed from club');return;} goBack();return;} return; }
    if(_cf.indexOf('ML-')===0){
      if(t.closest('.top .back')){goBack();return;}
      var _seg=t.closest('.seg .segopt'); if(_seg){ [].forEach.call(_seg.parentElement.children,function(c){c.classList&&c.classList.remove('on');}); _seg.classList.add('on'); SFLmoveType=_seg.classList.contains('perm')?'perm':'loan'; applyMoveType(mEl); return; }
      if(_cf==='ML-00'){ var _b0=t.closest('.btn,.altlink'); if(_b0){ if(/cancel/i.test(_b0.textContent)){goBack();return;} hist.length=0; SFLmgrMode=false; jumpTab('home'); sflToast('Move request sent to your Manager'+moveSplitToast());return;} return; }
      if(_cf==='ML-01'){ if(t.closest('.clubprev')){showDestSheet();return;} var _er=t.closest('.editrow'); if(_er){showTermSheet(_er);return;} var _b1=t.closest('.btn,.altlink'); if(_b1){ if(/save draft|cancel/i.test(_b1.textContent)){goBack();return;} goTo('reviewoffer');return;} return; }
      if(_cf==='ML-01A'){ var _b1a=t.closest('.btn,.altlink'); if(_b1a){ if(/edit/i.test(_b1a.textContent)){goBack();return;} sflToast('Offer sent · awaiting fan consent'+moveSplitToast()); goTo('offersent');return;} return; }
      if(_cf==='ML-01S'){ var _b1s=t.closest('.btn,.altlink'); if(_b1s){ if(/pending offers/i.test(_b1s.textContent)){cleanTo('mgrapprovals',/^ML-/);return;} returnTo('MC-04','mgrfanlist');return;} return; }
      if(_cf==='ML-02'||_cf==='ML-02P'){ var _b2=t.closest('.btn'); if(_b2){ if(/decline/i.test(_b2.textContent)){cleanTo('club',/^ML-/);sflToast('Offer declined · your membership is unchanged');return;} if(/ask manager/i.test(_b2.textContent)){goTo('chatthread');return;} goTo('acceptconfirm');return;} return; }
      if(_cf==='ML-02A'){ var _b2a=t.closest('.btn,.altlink'); if(_b2a){ if(/go back/i.test(_b2a.textContent)){goBack();return;} if(SFLmoveType==='perm'){ sflToast('Transfer complete · Manager 600 / Fan 400'); goTo('transfercomplete'); } else { goTo('loanactive'); } return;} return; }
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
      var seg=t.closest(SEG); if(seg){var kid=[].filter.call(seg.children,function(c){return c.contains(t);})[0]; if(kid){var kt=kid.textContent.toLowerCase(); var cf0=(VIEWS[curJ].screens[curS]||{}).fnum||''; if(cf0==='10'&&mEl.querySelector('.signin-panel')){return;} if(cf0.indexOf('PV')===0){ if(/vote/.test(kt)){goTo('vote');return;} if(/award/.test(kt)){goTo('awards');return;} if(/predict/.test(kt)){if(cf0!=='PV-01')goTo('predictions');else singleSel(kid,seg);return;} } if(cf0==='RW-01'){ if(/progress/.test(kt)){goTo('rewardinprog');return;} if(/history/.test(kt)){goTo('rewardhistory');return;} if(/claim/.test(kt)){singleSel(kid,seg);return;} } if(kt.indexOf('weekly')>=0){goTo('tasksweekly');return;} if(kt.indexOf('daily')>=0){goTo('tasksdaily');return;} singleSel(kid,seg);} return;}
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
    if(/(sign in|log in)/i.test(lbl)){goTo(cf==='10'?'live':'signin');return;}
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
    var _pc2=t.closest('.pcard'); if(_pc2){SFLpl=plFromEl(_pc2);goTo('playerdetail');return;}
    var _crow=t.closest('.crow'); if(_crow){ var _cg=_crow.getAttribute('data-goto')||''; if(!ANCH[_cg]){ _cg=(_crow.querySelector('.rolechip.club')||/club chat/i.test(_crow.textContent||''))?'clubchat':'chatthread'; } if(_cg==='chatthread'){ SFLchatPeer=peerFromRow(_crow); } SFLchatOrigin=_cg; goTo(_cg); return; }
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
      if(/i'?m ready|start|accept/.test(pkt)){goTo('pkbattle');return;}
      if(/find another/.test(pkt)){goTo('pkrandom');return;}
      if(/rematch/.test(pkt)){goTo('pkrematch');return;}
      if(/exit|stadium|leave|done|home/.test(pkt)){goTo('live');return;}
    }
    if(/^GL-0/.test(cf)){ if(/choose formation|preview/i.test(lbl)){next();return;} if(/go live now|start.*live|start broadcast|start room/i.test(lbl)){goTo('liveroomhost');return;} }
    var giftel=t.closest('.rrb.gift,.rb.gift,.cbtn.gift,.giftbtn,.pkgift'); if(!giftel){var gbt=t.closest('.gbtn'); if(gbt&&/gift/i.test(gbt.textContent))giftel=gbt;} if(giftel){ if(/^MSG/.test(cf)){SFLchatOrigin=(cf==='MSG-05')?'clubchat':'chatthread';goTo('chatgift');} else {openGiftSheet();} return; }
    var rrb=t.closest('.rrb'); if(rrb){var rrt=rrb.textContent||''; if(/🎁/.test(rrt)){goTo('giftmenu');return;} if(/🚪|🔴|leave|end/i.test(rrt)){sflLeaveLive();return;} return;}
    if(t.closest('.rmeta')||t.closest('.ractbar')||t.closest('.coincap')||t.closest('.rchat')||t.closest('.rsay')||t.closest('.composer')||t.closest('.cin')){return;}
    if(t.closest('.seat.open')||t.closest('.posrow')||t.closest('.opentag')){ if(isRoomMgr()){ takeSeatSkip(); return; } goTo('confirmseat');return;}
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
    var qae=t.closest('.qa'); if(qae){var q=(qae.textContent||'').toLowerCase(); if(/task/.test(q)){goSectionFromClub('tasks');return;} if(/live/.test(q)){goSectionFromClub('live');return;} if(/reward/.test(q)){goSectionFromClub('rewards');return;} if(/league/.test(q)){goSectionFromClub('league');return;}}
    var dutye=t.closest('.duty'); if(dutye){var dz=(dutye.textContent||'').toLowerCase(); if(/application/.test(dz)){goTo('mgrapplications');return;} if(/transfer|approve|loan/.test(dz)){goTo('mgrapprovals');return;} if(/live/.test(dz)){goTo('live');return;} if(/chat|announcement/.test(dz)){goTo('clubchat');return;} goTo('managerhq');return;}
    var modt=t.closest('.mod'); if(modt){var mt=(modt.textContent||'').toLowerCase(); if(/application/.test(mt)){goTo('mgrapplications');return;} if(/approval/.test(mt)){goTo('mgrapprovals');return;} if(/task/.test(mt)){goTo('tasks');return;} if(/reward/.test(mt)){goTo('rewards');return;} goTo('managerhq');return;}
    var sal=t.closest('.sa'); if(sal){var stx=(sal.textContent||'').toLowerCase(); if(/explore/.test(stx)){goTo('clubs');return;} if(/reward/.test(stx)){goTo('rewards');return;} if(/member/.test(stx)){goTo('clubchat');return;} if(/home/.test(stx)){goTo('home');return;} goTo('live');return;}

    if(t.closest('.fanview')){goTo('club');return;}
    if(cf==='MC-01'){
      if(/view breakdown/i.test(lbl)){goTo('mgrbreakdown');return;}
      if(t.closest('.recruit')){goTo('mgrrecruit');return;}
      var msh=t.closest('.short'); if(msh){var mst=(msh.textContent||'').toLowerCase(); if(/fan list/.test(mst)){goTo('mgrfanlist');return;} if(/application/.test(mst)){goTo('mgrapplications');return;} if(/add by id/.test(mst)){goTo('mgraddid');return;} if(/recruit/.test(mst)){goTo('mgrrecruit');return;} if(/reward/.test(mst)){goTo('mgrrewards');return;} if(/approval/.test(mst)){goTo('mgrapprovals');return;} if(/co-manager/.test(mst)){goTo('cmgrqueue');return;} goTo('managerhq');return;}
      var mstt=t.closest('.stat'); if(mstt){var msx=(mstt.textContent||'').toLowerCase(); if(/wallet/.test(msx)){goTo('wallet');return;} if(/league/.test(msx)){goTo('league');return;} if(/week|fans|\bfan\b/.test(msx)){goTo('mgrfanlist');return;} goTo('mgrbreakdown');return;}
    }
    var d=destOf(t); if(d&&goTo(d))return;
    if(t.closest('.sfl-nav')||t.closest('.navpill')||t.closest('.tabbar'))return;
    if(t.closest('.searchbar'))return;
    if(t.matches&&t.matches('.phone,.body,.dbody,.lbody,.scroll,.scrollarea,.feed,.list,.hscroll,.lscroll,.msgs,.chatwrap,.frames,.top,.dtop,.hbar,.hero,.phero,.lhero,.chdr,#mount'))return;
    if(/^CC-/.test(cf)&&!t.closest('.btn')){return;}
    if(!t.closest('.btn,.altlink,a,.opt,.method,.srcopt,.tab,.dtab,.seg,.segopt,.chip,.fchip,.card,.listrow,.crow,.actrow,.reasonopt,.laopt,.giftopt,.modecard,.formcard,.roomcard,.golivecard,.fixcard,.predict,.hubcard,.evcard')&&(mEl.querySelector('.cta .btn')||mEl.querySelector('.lbody>.btn')||mEl.querySelector('.btn.club'))){return;}
    next();
  });
  function updateStageToggleLabel(){
    var lbl=document.getElementById('stageToggleLbl');
    if(!lbl)return;
    lbl.textContent=document.body.getAttribute('data-stage')==='light'?'Dark mode':'Light mode';
  }
  function applyStageChrome(){
    var light=document.body.getAttribute('data-stage')==='light';
    try{localStorage.setItem('sfl-stage',light?'light':'dark');}catch(e){}
    updateStageToggleLabel();
    var phone=mount?mount.querySelector('.phone'):null; if(!phone)return;
    var keepLite=phone.classList.contains('bleed')||/splash|welcome|room/.test(phone.className);
    if(phone.classList.contains('light')) phone.setAttribute('data-sfl-light','1');
    if(phone.getAttribute('data-sfl-light')==='1') phone.classList.toggle('light', light&&!keepLite);
    var sb=phone.querySelector(':scope > .sfl-statusbar');
    if(sb){
      sb.style.color=(keepLite||!light)?'#F4F6FA':'#0E1016';
      if(!phone.classList.contains('bleed')) sb.style.background=light?'#F4F6FB':'#080A10';
    }
    var nav=phone.querySelector(':scope > .sfl-nav');
    if(nav) nav.classList.toggle('dark', !light);
  }
  try{var _st=localStorage.getItem('sfl-stage'); if(_st==='dark'||_st==='light') document.body.setAttribute('data-stage',_st);}catch(e){}
  updateStageToggleLabel();
  document.getElementById('stageToggle').onclick=function(){
    document.body.setAttribute('data-stage', document.body.getAttribute('data-stage')==='light'?'dark':'light');
    applyStageChrome();
  };
  var _mm=document.getElementById('menuModal');
  document.getElementById('menuBtn').onclick=function(){_mm.classList.add('open');};
  document.getElementById('menuClose').onclick=function(){_mm.classList.remove('open');};
  _mm.onclick=function(e){if(e.target===_mm)_mm.classList.remove('open');};
  flowsel.addEventListener('change',function(){_mm.classList.remove('open');});
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
 {"name":"2 · Returning user (Sign in)","refs":[[0,"1"],[0,"2"],[0,"10"],[6,"GL-00"]]},
 {"name":"3 · Forgot password","refs":[[0,"10"],[0,"12"],[0,"13"],[0,"14"],[0,"14b"],[0,"10"]]},
 {"name":"4 · Daily tasks (do & claim)","refs":[[3,"FT-01"],[17,"CS-01"],[3,"FT-06"],[3,"FT-01"],[4,"PV-01"],[3,"FT-06"],[3,"FT-01"],[3,"FT-07"],[3,"FT-08"],[3,"FT-10"]]},
 {"name":"⭐ Watch-Along (in live)","refs":[[6,"GL-03H"],[6,"GL-WA-01"],[6,"GL-WA-L"],[6,"GL-WA-P"],[6,"GL-WA-H"],[6,"GL-WA-V"],[6,"GL-WA-E"],[6,"GL-03H"]]},
 {"name":"⭐ Room managers & join requests","refs":[[6,"GL-03H"],[6,"GL-CH-H"],[6,"GL-03V"],[6,"GL-05"],[6,"GL-05A"],[6,"GL-05W"],[6,"GL-05OK"],[6,"GL-05B"],[6,"GL-CH-01"],[6,"GL-CH-02"],[6,"GL-CH-C"]]},
 {"name":"⭐ Coin Seller (P2P top-up)","refs":[[2,"J3-02"],[2,"J3-05"],[25,"CS-01"],[25,"CS-02"],[25,"CS-03"],[25,"CS-04"],[25,"CS-05"],[25,"CS-07"]]},
 {"name":"⭐ Weekly buy & sell players","refs":[[3,"FT-02"],[3,"FT-03P"],[5,"PL-06"],[5,"PL-06A"],[5,"PL-07"],[5,"PL-08"],[5,"PL-01W"],[5,"PL-02"],[5,"PL-03"],[5,"PL-05"]]},
 {"name":"⭐ Co-manager of a club","refs":[[13,"MC-01"],[13,"MC-04"],[13,"MC-04A"],[13,"MC-CM-01"],[13,"MC-CM-02"],[13,"MC-CM-03"],[13,"MC-01"],[19,"G-05"],[1,"J2-16"],[13,"MC-CM-F2"],[13,"MC-CM-F3"],[13,"MC-CM-F4"]]},
]
JLABELS=[ ('Global Shell' if num=='G' else ('Extra · '+title if num.startswith('E') else 'J'+num+' · '+title)) for (fn,num,title) in ALL]
PLAYER_JS=PLAYER_JS.replace('%SB%',SB_INJECT).replace('%META%',json.dumps([m for _,_,m in ALL])).replace('%FLOWS%',json.dumps(FLOWS)).replace('%JLABELS%',json.dumps(JLABELS)).replace('%GIFTSHEET%',json.dumps(GIFTSHEET_HTML))

page=('<!DOCTYPE html>\n<html lang="en"><head><meta charset="UTF-8">'
 '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">'
 '<title>SFL — Flow Prototype</title>\n<style>\n'+font_css+'\n'+root_vars+'\n'+CHROME_CSS+PPNAV_CSS+'\n'+'\n'.join(styleblocks)+'\n</style></head>'
 '<body data-stage="light">'
 '<header>'
 '<button class="ppbtn sm" id="menuBtn" title="Menu">☰</button>'
 '<div class="hdrscreen"><span class="sc" id="scap"></span><span class="ppcount hdrcount" id="counter2"></span></div>'
 '<div class="hdrnav">'
 '<button class="ppbtn sm ppchev" id="bprev2" title="Previous screen" aria-label="Previous">‹</button>'
 '<button class="ppbtn sm ppchev" id="bnext2" title="Next screen" aria-label="Next">›</button>'
 '</div>'
 '</header>'
 '<div class="sflmodal" id="menuModal"><div class="sflmodal-card">'
 '<div class="mm-top"><div class="brand"><div class="bc">SFL</div>Flow Prototype</div><button class="ppbtn sm" id="menuClose">✕</button></div>'
 '<div class="mm-lbl">Jump to a flow or journey</div>'
 '<div class="mm-scroll"><select id="flowsel"></select></div>'
 '<div class="mm-foot"><button class="mm-theme" id="stageToggle" type="button" title="Toggle theme"><span class="mm-theme-ic">◐</span><span class="mm-theme-lbl" id="stageToggleLbl">Dark mode</span></button>'
 '<div class="mm-nav"><button class="ppnavbtn" id="bprev">‹ Prev</button><span class="ppcount" id="counter"></span><button class="ppnavbtn" id="bnext">Next ›</button></div></div>'
 '</div></div>'
 '<div class="ppstage" id="stage">'
 '<div class="scaler" id="scaler"><div id="mount"></div></div>'
 '</div>'
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
    out=inline_img_src(out)
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
    inlined=inline_assets(src)
    open(os.path.join(SITE,'journeys',outname),'w',encoding='utf-8').write(inlined)
    # Keep screens/*.html (the open-on-its-own gallery) in lockstep with *.dev.html
    open(fn.replace('.dev.html','.html'),'w',encoding='utf-8').write(inlined)
    entries.append((code,label,slug,'journeys/'+outname,nscr,'reference' if code in REF else 'journey'))

# copy the interactive prototype into the site as prototype.html
shutil.copyfile('sfl-prototype.html', os.path.join(SITE,'prototype.html'))

# copy the raw assets folder so runtime-generated markup (JS-built url('assets/..') for
# live-room avatars, camera, gallery, dynamic data-av) resolves on the deployed site.
# The inlined pages don't need it, but the interactive prototype builds these paths at runtime.
if os.path.isdir('assets'):
    shutil.copytree('assets', os.path.join(SITE,'assets'), dirs_exist_ok=True)
    print('copied assets/ ->', os.path.join(SITE,'assets'))

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

# screens/ hub — same cards, local paths (serve from screens/)
def cards_local(kind):
    out=''
    for fn,code,label in ALL:
        nscr=allsrc[fn].count('class="fnum"')
        k='reference' if code in REF else 'journey'
        if k!=kind: continue
        href=fn.replace('.dev.html','.html')
        out+=('<a class="jcard" href="'+href+'">'
              '<div class="jcode">'+code+'</div>'
              '<div class="jmeta"><div class="jname">'+label+'</div>'
              '<div class="jscr">'+str(nscr)+' screens</div></div>'
              '<div class="jarrow">→</div></a>')
    return out
hub_scr=hub.replace('href="prototype.html"','href="sfl-prototype.html"').replace(
    '<div class="grid">'+cards('journey')+'</div>',
    '<div class="grid">'+cards_local('journey')+'</div>').replace(
    '<div class="grid">'+cards('reference')+'</div>',
    '<div class="grid">'+cards_local('reference')+'</div>')
open('index.html','w',encoding='utf-8').write(hub_scr)
# Former concatenated dump — keep the filename, point at current per-journey pages
open('sfl-all-journeys.html','w',encoding='utf-8').write(hub_scr)
print('wrote screens/index.html + screens/sfl-all-journeys.html (hubs -> current journey pages)')
