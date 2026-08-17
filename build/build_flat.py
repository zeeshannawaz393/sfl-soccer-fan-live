import re, base64, os

SCR='/Users/shahnawaz/Documents/sfl-niki/screens'; os.chdir(SCR)

CORE=[
 ('onboarding.dev.html','1','Onboarding & Sign-in'),
 ('journey2.dev.html','2','Join a Fan Club'),
 ('journey3.dev.html','3','Buy Coins'),
 ('journey4.dev.html','4','Fan Tasks & Duties'),
 ('journey5.dev.html','5','Predictions & Voting'),
 ('journey6.dev.html','6','Player Transfer Market'),
 ('journey7.dev.html','7','Formation Live Rooms'),
 ('journey8.dev.html','8','Live Engagement'),
 ('journey9.dev.html','9','PK Battle'),
 ('journey10.dev.html','10','Gifts & Kit Bag'),
 ('journey11.dev.html','11','Fan Value Activation'),
 ('journey12.dev.html','12','Progression & Leagues'),
 ('journey13.dev.html','13','Wallet'),
 ('journey14.dev.html','14','Manager Console'),
 ('journey15.dev.html','15','Fan Transfer & Loan'),
 ('journey16.dev.html','16','Rewards & Monthly Winners'),
 ('journey17.dev.html','17','Mini-Games'),
 ('journey18.dev.html','18','Content & Social'),
 ('journey19.dev.html','19','Messaging & Calls'),
 ('global-shell.dev.html','G','Global Shell'),
]
EXTRAS=[
 ('discovery-live.dev.html','E1','Discovery / Live'),
 ('missions.dev.html','E2','Fan Missions'),
 ('room-templates.dev.html','E3','Room Templates'),
 ('light-mode.dev.html','E4','Light Mode Set'),
 ('create-club.dev.html','E5','Create a Club'),
]
ALL=CORE+EXTRAS

allsrc={fn:open(fn).read() for fn,_,_ in ALL}

# unique images -> :root vars
img_map={}
def vn(fn): return '--img-'+re.sub(r'[^a-zA-Z0-9]','_',fn)
for s in allsrc.values():
    for m in re.finditer(r"url\(['\"]?assets/([\w.\-]+)['\"]?\)", s):
        a=m.group(1)
        if a.endswith('.woff2'): continue
        img_map.setdefault(a,vn(a))
def datauri(path):
    mime='image/jpeg' if path.lower().endswith(('.jpg','.jpeg')) else ('image/png' if path.lower().endswith('.png') else 'application/octet-stream')
    with open('assets/'+path,'rb') as f: b=base64.b64encode(f.read()).decode()
    return f'data:{mime};base64,{b}'
root_vars=':root{\n'+'\n'.join(f'  {v}: url("{datauri(a)}");' for a,v in sorted(img_map.items()))+'\n}'
with open('assets/manrope.woff2','rb') as f: font_b64=base64.b64encode(f.read()).decode()
font_css=("@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;"
          f"src:url('data:font/woff2;base64,{font_b64}') format('woff2')}}")

# ---------- CSS scoping ----------
def split_commas(sel):
    out=[]; d=0; cur=''
    for ch in sel:
        if ch in '([': d+=1
        elif ch in ')]': d-=1
        if ch==',' and d==0: out.append(cur); cur=''
        else: cur+=ch
    if cur.strip(): out.append(cur)
    return out
def scope_sels(prelude, scope):
    res=[]
    for s in split_commas(prelude):
        s=s.strip()
        if not s: continue
        if s=='*': continue  # global reset handles this  # reset inside journey
        elif s.startswith(':root'): res.append(s.replace(':root',scope,1))
        elif re.match(r'^(html|body)\b', s): res.append(re.sub(r'^(html|body)', scope, s))
        else: res.append(scope+' '+s)
    return ', '.join(res)
def scope_css(css, scope):
    res=''; i=0; n=len(css)
    while i<n:
        b=css.find('{', i)
        if b==-1: res+=css[i:]; break
        prelude=css[i:b].strip()
        d=1; j=b+1
        while j<n and d>0:
            if css[j]=='{': d+=1
            elif css[j]=='}': d-=1
            j+=1
        body=css[b+1:j-1]
        low=prelude.lower()
        if prelude.startswith('@'):
            at=low.split()[0] if low.split() else ''
            if at in ('@media','@supports','@document'):
                res+=prelude+'{'+scope_css(body,scope)+'}'
            else:  # keyframes / font-face -> keep global
                res+=prelude+'{'+body+'}'
        else:
            res+=scope_sels(prelude,scope)+'{'+body+'}'
        i=j
    return res

def imgvar(txt):
    def rep(m):
        a=m.group(1)
        if a.endswith('.woff2'): return m.group(0)
        return f'var({img_map[a]})'
    return re.sub(r"url\(['\"]?assets/([\w.\-]+)['\"]?\)", rep, txt)

sections=[]; styleblocks=[]; navlinks=[]
for idx,(fn,num,title) in enumerate(ALL):
    sid='j'+str(idx)
    s=allsrc[fn]
    css=re.search(r'<style>(.*?)</style>', s, re.S).group(1)
    css=re.sub(r'@font-face\{[^}]*\}','',css)
    css=imgvar(css)
    css=scope_css(css, '#'+sid)
    styleblocks.append(f'/* ===== {title} ===== */\n'+css)
    # body content: page-head + frames (exclude sfl-chrome)
    pi=s.find('<div class="page-head">')
    fi=s.find('<div class="frames">')
    end=s.find('<style id="sfl-chrome"');  end=end if end>0 else s.rfind('</body>')
    body=s[pi:end].rstrip()
    body=imgvar(body)
    label = ('Global Shell' if num=='G' else ('Exploration '+num[1:] if num.startswith('E') else 'Journey '+num))
    sections.append(f'<section id="{sid}" class="jsec" data-journey="{label}">\n{body}\n</section>')
    navlinks.append(f'<a href="#{sid}">{num}</a>')

SB_CSS = """
.sfl-statusbar{position:absolute;top:0;left:0;right:0;z-index:600;height:50px;display:flex;align-items:center;justify-content:space-between;padding:2px 40px 0 42px;background:inherit;font-family:'Manrope',-apple-system,'Segoe UI',sans-serif;font-size:15px;font-weight:800;letter-spacing:-.3px;font-variant-numeric:tabular-nums}
.sfl-statusbar .sfl-sys{display:flex;align-items:center;gap:7px}
.sfl-notch{position:absolute;left:50%;top:9px;transform:translateX(-50%);width:116px;height:30px;background:#04060A;border-radius:16px}
.sfl-notch::after{content:"";position:absolute;right:16px;top:50%;transform:translateY(-50%);width:8px;height:8px;border-radius:50%;background:#1b222c}
"""
SHELL_CSS = """
/*GLOBAL_RESET_ADDED*/
*{margin:0;padding:0;box-sizing:border-box;-webkit-font-smoothing:antialiased}
html{scroll-behavior:smooth}
body.flatbody{margin:0;background:#0B0E14;font-family:'Manrope',-apple-system,'Segoe UI',sans-serif}
.jsec{position:relative;border-bottom:2px solid rgba(255,255,255,.06)}
.flatnav{position:fixed;top:14px;right:14px;z-index:99999;display:flex;flex-wrap:wrap;gap:5px;max-width:150px;justify-content:flex-end;background:rgba(10,12,18,.82);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:8px}
.flatnav a{width:26px;height:24px;display:flex;align-items:center;justify-content:center;font:800 11px 'Manrope',sans-serif;color:#C9D2E0;text-decoration:none;background:rgba(255,255,255,.06);border-radius:7px}
.flatnav a:hover{background:#C9FF3D;color:#0A1400}
.flathint{position:fixed;top:14px;left:14px;z-index:99999;background:rgba(10,12,18,.82);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.12);border-radius:12px;padding:8px 13px;font:800 11px 'Manrope',sans-serif;color:#C9D2E0}
"""
INJECTOR = r"""
<script>
(function(){
  var SIG='<svg width="18" height="13" viewBox="0 0 18 13" fill="currentColor"><rect x="0" y="9" width="3" height="4" rx="1"/><rect x="5" y="6.5" width="3" height="6.5" rx="1"/><rect x="10" y="3.5" width="3" height="9.5" rx="1"/><rect x="15" y="0" width="3" height="13" rx="1"/></svg>';
  var WIFI='<svg width="17" height="13" viewBox="0 0 17 13" fill="currentColor"><path d="M8.5 2.2C5.6 2.2 2.9 3.3 1 5.2l1.5 1.5C4 5.2 6.2 4.2 8.5 4.2s4.5 1 6 2.5L16 5.2c-1.9-1.9-4.6-3-7.5-3z"/><path d="M8.5 6.6c-1.7 0-3.3.7-4.5 1.9l1.6 1.6c.8-.7 1.8-1.2 2.9-1.2s2.1.5 2.9 1.2l1.6-1.6C11.8 7.3 10.2 6.6 8.5 6.6z"/><circle cx="8.5" cy="11.6" r="1.4"/></svg>';
  var BAT='<svg width="27" height="13" viewBox="0 0 27 13" fill="none"><rect x="0.6" y="0.6" width="22.8" height="11.8" rx="3.4" stroke="currentColor" stroke-opacity="0.45"/><rect x="2.1" y="2.1" width="15" height="8.8" rx="1.8" fill="currentColor"/><path d="M25 4.6c1 .5 1 3.3 0 3.8z" fill="currentColor" fill-opacity="0.6"/></svg>';
  function lum(c){var m=(c||'').match(/[\d.]+/g);if(!m)return 1;return 0.2126*m[0]/255+0.7152*m[1]/255+0.0722*m[2]/255;}

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
   var body=phone.querySelector('.body,.dbody,.lbody,.hscroll'); if(body) body.style.paddingBottom='78px'; }

  document.querySelectorAll('.phone').forEach(function(p){
    if(p.querySelector(':scope > .sfl-statusbar'))return;
    var dark=lum(getComputedStyle(p).backgroundColor)<0.5;
    p.style.paddingTop='46px';
    var sb=document.createElement('div');sb.className='sfl-statusbar';sb.style.cssText='padding:2px 40px 0 42px;box-sizing:border-box;color:'+(dark?'#F4F6FA':'#0E1016')+';';
    sb.innerHTML='<span class="sfl-time">9:41</span><div class="sfl-notch"></div><span class="sfl-sys">'+SIG+WIFI+BAT+'</span>';
    p.insertBefore(sb,p.firstChild);
    injectNav(p,dark);
  });

  var COIN='<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11.2" fill="#C9820C"/><circle cx="12" cy="12" r="9.6" fill="#F4C23A"/><path d="M6 8.5a9 9 0 0 1 12 0" stroke="#FCE7A6" stroke-width="1.1" fill="none" opacity=".7"/><circle cx="12" cy="12" r="4.7" fill="#fff"/><path d="M12 8.1l2.6 1.9-1 3.1h-3.2l-1-3.1z" fill="#22252B"/><circle cx="12" cy="7.4" r=".7" fill="#22252B"/><circle cx="16.2" cy="10.6" r=".7" fill="#22252B"/><circle cx="14.6" cy="15.5" r=".7" fill="#22252B"/><circle cx="9.4" cy="15.5" r=".7" fill="#22252B"/><circle cx="7.8" cy="10.6" r=".7" fill="#22252B"/></svg>';
  var GOLD='<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="11.2" fill="#8A5606"/><circle cx="12" cy="12" r="9.6" fill="#E7A62A"/><path d="M6 8.5a9 9 0 0 1 12 0" stroke="#FFDE9B" stroke-width="1.1" fill="none" opacity=".65"/><path d="M12 6.6l1.7 3.7 4 .4-3 2.6.9 3.9-3.6-2.1-3.6 2.1.9-3.9-3-2.6 4-.4z" fill="#7A4B00"/></svg>';
  var icst=document.createElement('style'); icst.textContent='.sflcoin{background:transparent!important;background-image:none!important;border:none!important;box-shadow:none!important;color:transparent!important;overflow:visible!important;padding:0!important;display:inline-flex!important;align-items:center;justify-content:center;line-height:0;font-size:0!important}.sflcoin svg{width:100%;height:100%;display:block}.sflemoji{display:inline-flex;width:1.15em;height:1.15em;vertical-align:-.2em;flex:none}.sflemoji svg{width:100%;height:100%;display:block}.phone .scrollarea>*,.phone .scroll>*,.phone .lbody>*,.phone .dbody>*{flex-shrink:0}'; document.head.appendChild(icst);
  document.querySelectorAll('.coin,.gc,.gg,.g-coin,.g-gold,.g-tgold').forEach(function(e){
    if(e.getAttribute('data-ic'))return; var cn=e.className||'', tx=(e.textContent||'').trim();
    if(tx.length>1)return;
    var gold=/(^|\s)gg(\s|$)|g-gold|g-tgold/.test(cn)||tx==='G'||tx==='g';
    e.setAttribute('data-ic','1'); e.classList.add('sflcoin'); if(gold)e.classList.add('isgold'); e.innerHTML=gold?GOLD:COIN;
  });
  document.querySelectorAll('.coinpill,.coinbal').forEach(function(e){ if(e.innerHTML.indexOf('🪙')>=0){e.innerHTML=e.innerHTML.replace(/🪙/g,'<span class="sflemoji">'+COIN+'</span>');}});

  var COLMAP={red:['#F0564A','#A81C12'],blue:['#5AA0E6','#1B569B'],gold:['#F3CC55','#B0800A'],green:['#5FC27E','#1C8348'],purple:['#B07CF0','#6A34B8'],teal:['#43C4C9','#157B7F']};
  var INITCOL={RD:'red',RF:'red',BV:'blue',BW:'blue',BL:'blue',CF:'blue',RL:'gold',NS:'gold',NSH:'green',MTL:'green',SFL:'red'};
  var PALK=['red','blue','gold','green','purple','teal'];
  function crestCols(cn,tx){ if(/(^|\s)(cr-red|red)(\s|$)/.test(cn))return COLMAP.red; if(/(^|\s)(cr-blue|blue)(\s|$)/.test(cn))return COLMAP.blue; if(/(^|\s)(cr-gold|gold)(\s|$)/.test(cn))return COLMAP.gold; if(/(^|\s)(cr-green|green)(\s|$)/.test(cn))return COLMAP.green; if(INITCOL[tx])return COLMAP[INITCOL[tx]]; var h=0;for(var i=0;i<tx.length;i++)h=(h*31+tx.charCodeAt(i))>>>0;return COLMAP[PALK[h%PALK.length]];}
  function shield(c1,c2){return 'data:image/svg+xml;utf8,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 46"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+c1+'"/><stop offset="1" stop-color="'+c2+'"/></linearGradient></defs><path d="M20 2 L37 6.8 V21 C37 32.5 29.5 40 20 43.6 C10.5 40 3 32.5 3 21 V6.8 Z" fill="url(#g)" stroke="#ffffff" stroke-width="2"/><path d="M20 5 L34 8.8 V20 C34 24 31 27 20 22 C9 27 6 24 6 20 V8.8 Z" fill="#ffffff" opacity="0.12"/></svg>');}
  document.querySelectorAll('.crest,.ccrest,.crestbig,.cbadge').forEach(function(e){
    if(e.getAttribute('data-cr'))return; var tx=(e.textContent||'').trim(); if(tx.length>4)return;
    var cols=crestCols(e.className||'',tx); e.setAttribute('data-cr','1'); e.classList.add('sflcrest');
    e.style.backgroundImage='url("'+shield(cols[0],cols[1])+'")'; e.style.backgroundColor='transparent'; e.style.backgroundSize='contain'; e.style.backgroundRepeat='no-repeat'; e.style.backgroundPosition='center'; e.style.borderRadius='0'; e.style.boxShadow='none'; e.style.border='none'; e.style.color='#fff'; e.style.textShadow='0 1px 2px rgba(0,0,0,.4)'; e.style.fontWeight='800';
  });
  document.addEventListener('click',function(e){var lgc=e.target.closest&&e.target.closest('.lgchip'); if(!lgc)return; var grp=lgc.parentElement; [].forEach.call(grp.children,function(c){c.classList&&c.classList.remove('on');}); lgc.classList.add('on'); var key=lgc.getAttribute('data-league')||''; var phone=lgc.closest('.phone'); if(!phone)return; [].forEach.call(phone.querySelectorAll('.lgroup'),function(g){g.style.display=(!key||g.getAttribute('data-league')===key)?'':'none';});});
})();
</script>
"""

page = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n'
 '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
 '<title>Soccer Fan Live — All Screens (flat, for Figma import)</title>\n<style>\n'
 + font_css + '\n' + root_vars + '\n' + SB_CSS + '\n' + SHELL_CSS + '\n'
 + '\n'.join(styleblocks) + '\n</style>\n</head>\n<body class="flatbody">\n'
 + '<div class="flathint">SFL · all screens</div>\n'
 + '<nav class="flatnav">' + ''.join(navlinks) + '</nav>\n'
 + '\n'.join(sections) + '\n'
 + INJECTOR + '\n</body>\n</html>')

open('sfl-all-screens-flat.html','w').write(page)
print('wrote sfl-all-screens-flat.html', round(len(page)/1048576,2),'MB · sections:',len(ALL),'· images:',len(img_map))
