# Generates create-club.dev.html with a real leagues/clubs dataset + filterable team picker.
OUT='/Users/shahnawaz/Documents/sfl-niki/screens/create-club.dev.html'

# league key -> (chip label, section label, [ (name, initials, colorClass, city) ])
LEAGUES=[
 ('premier','🏴 Premier League','ENGLAND · PREMIER LEAGUE',[
   ('Arsenal','ARS','cr-red','London'),('Aston Villa','AVL','cr-red','Birmingham'),('Bournemouth','BOU','cr-red','Bournemouth'),
   ('Brentford','BRE','cr-red','London'),('Brighton & Hove Albion','BHA','cr-blue','Brighton'),('Chelsea','CHE','cr-blue','London'),
   ('Crystal Palace','CRY','cr-blue','London'),('Everton','EVE','cr-blue','Liverpool'),('Fulham','FUL','cr-blue','London'),
   ('Ipswich Town','IPS','cr-blue','Ipswich'),('Leicester City','LEI','cr-blue','Leicester'),('Liverpool','LIV','cr-red','Liverpool'),
   ('Manchester City','MCI','cr-blue','Manchester'),('Manchester United','MUN','cr-red','Manchester'),('Newcastle United','NEW','cr-blue','Newcastle'),
   ('Nottingham Forest','NFO','cr-red','Nottingham'),('Southampton','SOU','cr-red','Southampton'),('Tottenham Hotspur','TOT','cr-blue','London'),
   ('West Ham United','WHU','cr-red','London'),('Wolverhampton','WOL','cr-gold','Wolverhampton'),
 ]),
 ('laliga','🇪🇸 La Liga','SPAIN · LA LIGA',[
   ('Real Madrid','RMA','cr-gold','Madrid'),('FC Barcelona','BAR','cr-blue','Barcelona'),('Atlético Madrid','ATM','cr-red','Madrid'),
   ('Athletic Bilbao','ATH','cr-red','Bilbao'),('Real Sociedad','RSO','cr-blue','San Sebastián'),('Real Betis','BET','cr-green','Seville'),
   ('Villarreal','VIL','cr-gold','Villarreal'),('Valencia','VAL','cr-gold','Valencia'),('Sevilla','SEV','cr-red','Seville'),
   ('Girona','GIR','cr-red','Girona'),('Osasuna','OSA','cr-red','Pamplona'),('Celta Vigo','CEL','cr-blue','Vigo'),
   ('Rayo Vallecano','RAY','cr-red','Madrid'),('Mallorca','MLL','cr-red','Palma'),('Getafe','GET','cr-blue','Getafe'),
   ('Las Palmas','LPA','cr-gold','Las Palmas'),('Deportivo Alavés','ALA','cr-blue','Vitoria'),('Espanyol','ESP','cr-blue','Barcelona'),
   ('Leganés','LEG','cr-blue','Madrid'),('Real Valladolid','VLL','cr-purple','Valladolid'),
 ]),
 ('seriea','🇮🇹 Serie A','ITALY · SERIE A',[
   ('Inter Milan','INT','cr-blue','Milan'),('AC Milan','MIL','cr-red','Milan'),('Juventus','JUV','cr-gold','Turin'),
   ('Napoli','NAP','cr-blue','Naples'),('AS Roma','ROM','cr-red','Rome'),('Lazio','LAZ','cr-blue','Rome'),
   ('Atalanta','ATA','cr-blue','Bergamo'),('Fiorentina','FIO','cr-purple','Florence'),('Bologna','BOL','cr-red','Bologna'),
   ('Torino','TOR','cr-red','Turin'),('Udinese','UDI','cr-gold','Udine'),('Genoa','GEN','cr-red','Genoa'),
   ('Monza','MON','cr-red','Monza'),('Hellas Verona','VER','cr-gold','Verona'),('Cagliari','CAG','cr-red','Cagliari'),
   ('Lecce','LEC','cr-gold','Lecce'),('Empoli','EMP','cr-blue','Empoli'),('Parma','PAR','cr-gold','Parma'),
   ('Como','COM','cr-blue','Como'),('Venezia','VEN','cr-green','Venice'),
 ]),
 ('bundesliga','🇩🇪 Bundesliga','GERMANY · BUNDESLIGA',[
   ('Bayern Munich','FCB','cr-red','Munich'),('Borussia Dortmund','BVB','cr-gold','Dortmund'),('RB Leipzig','RBL','cr-red','Leipzig'),
   ('Bayer Leverkusen','B04','cr-red','Leverkusen'),('Eintracht Frankfurt','SGE','cr-red','Frankfurt'),('VfB Stuttgart','VFB','cr-red','Stuttgart'),
   ('VfL Wolfsburg','WOB','cr-green','Wolfsburg'),('SC Freiburg','SCF','cr-red','Freiburg'),('Hoffenheim','TSG','cr-blue','Sinsheim'),
   ('Mainz 05','M05','cr-red','Mainz'),('Werder Bremen','SVW','cr-green','Bremen'),('FC Augsburg','FCA','cr-red','Augsburg'),
   ('Union Berlin','FCU','cr-red','Berlin'),('Borussia M.gladbach','BMG','cr-green','Mönchengladbach'),('VfL Bochum','BOC','cr-blue','Bochum'),
   ('1. FC Heidenheim','HDH','cr-red','Heidenheim'),('FC St. Pauli','STP','cr-gold','Hamburg'),('Holstein Kiel','KSV','cr-blue','Kiel'),
 ]),
 ('ligue1','🇫🇷 Ligue 1','FRANCE · LIGUE 1',[
   ('Paris Saint-Germain','PSG','cr-blue','Paris'),('Marseille','OM','cr-blue','Marseille'),('AS Monaco','ASM','cr-red','Monaco'),
   ('Lyon','OL','cr-blue','Lyon'),('Lille','LOSC','cr-red','Lille'),('Nice','OGCN','cr-red','Nice'),
   ('Rennes','SRFC','cr-red','Rennes'),('Lens','RCL','cr-gold','Lens'),('Strasbourg','RCSA','cr-blue','Strasbourg'),
   ('Nantes','FCN','cr-gold','Nantes'),('Montpellier','MHSC','cr-blue','Montpellier'),('Toulouse','TFC','cr-purple','Toulouse'),
   ('Reims','SR','cr-red','Reims'),('Brest','SB29','cr-red','Brest'),('Le Havre','HAC','cr-blue','Le Havre'),
   ('Auxerre','AJA','cr-blue','Auxerre'),('Angers','SCO','cr-gold','Angers'),('Saint-Étienne','ASSE','cr-green','Saint-Étienne'),
 ]),
 ('primeira','🇵🇹 Primeira','PORTUGAL · PRIMEIRA LIGA',[
   ('Benfica','SLB','cr-red','Lisbon'),('FC Porto','FCP','cr-blue','Porto'),('Sporting CP','SCP','cr-green','Lisbon'),
   ('Braga','SCB','cr-red','Braga'),('Vitória SC','VSC','cr-blue','Guimarães'),
 ]),
 ('eredivisie','🇳🇱 Eredivisie','NETHERLANDS · EREDIVISIE',[
   ('Ajax','AJA','cr-red','Amsterdam'),('PSV Eindhoven','PSV','cr-red','Eindhoven'),('Feyenoord','FEY','cr-red','Rotterdam'),
   ('AZ Alkmaar','AZ','cr-red','Alkmaar'),('FC Twente','TWE','cr-red','Enschede'),
 ]),
]

def teamrow(name,ini,col,city,on=False):
    return (f'      <div class="teamrow{" on" if on else ""}" data-name="{name.lower()}">'
            f'<div class="crest {col}">{ini}</div><div><div class="tn">{name}</div>'
            f'<div class="tc">{city}</div></div><div class="rad"></div></div>')

# chips
chips='<span class="lgchip on" data-league="">All</span>'
for key,label,_,_teams in LEAGUES:
    chips+=f'<span class="lgchip" data-league="{key}">{label}</span>'

# groups
groups=''
first=True
for key,label,seclabel,teams in LEAGUES:
    rows=''
    for i,(name,ini,col,city) in enumerate(teams):
        rows+=teamrow(name,ini,col,city,on=(first and i==0))+'\n'
    groups+=f'    <div class="lgroup" data-league="{key}">\n      <div class="lgsec">{seclabel}</div>\n{rows}    </div>\n'
    first=False

total=sum(len(t) for *_,t in LEAGUES)

HEAD='''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>SFL — Create a Club</title>
<style>
  :root{
    --bg:#F4F6FB;--card:#FFFFFF;--line:#ECEEF5;
    --t1:#14161C;--t2:#707786;--t3:#A6ADBC;
    --green1:#0FB753;--green2:#7CD843;
    --live1:#FF416C;--live2:#FF7A3B;
    --gold1:#FFB300;--gold2:#FFD54F;
    --violet:#7C4DFF;--cyan:#1FA8FF;--red:#E4362B;--sky:#5FA8DE;--amber:#F59E0B;
    --shadow:0 12px 34px rgba(24,40,80,.12);--shadow-sm:0 5px 16px rgba(24,40,80,.09);
  }
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#0d1017;font-family:'Manrope',-apple-system,sans-serif;color:var(--t1);padding:40px}
  .frames{display:flex;gap:52px;flex-wrap:wrap;justify-content:center;max-width:1980px;margin:0 auto}
  .fw{display:flex;flex-direction:column;gap:15px}
  .flabel{display:flex;align-items:center;gap:11px;max-width:390px}
  .fnum{min-width:52px;height:26px;padding:0 8px;border-radius:8px;background:linear-gradient(140deg,var(--green1),var(--green2));color:#fff;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;flex:none}
  .fname{font-size:15px;font-weight:800;color:#EAEEF5}.fname span{display:block;font-size:11px;font-weight:650;color:#8892A4}
  .phone{width:390px;height:844px;flex:none;border-radius:46px;overflow:hidden;position:relative;background:var(--bg);display:flex;flex-direction:column;box-shadow:0 44px 96px rgba(20,30,60,.20);border:1px solid #D7DDEA}
  .top{padding:18px 20px 0;display:flex;align-items:center;gap:12px;z-index:5}
  .htitle{font-size:19px;font-weight:800;letter-spacing:-.4px}
  .back{width:36px;height:36px;border-radius:50%;background:#fff;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:15px;color:var(--t2);box-shadow:var(--shadow-sm);flex:none}
  .stepind{margin-left:auto;font-size:11.5px;font-weight:800;color:var(--t3)}
  .steps{display:flex;gap:5px;padding:14px 20px 4px}
  .steps i{height:5px;flex:1;border-radius:3px;background:var(--line)}
  .steps i.on{background:linear-gradient(90deg,var(--green1),var(--green2))}
  .body{flex:1;padding:8px 20px 0;display:flex;flex-direction:column;overflow:hidden}
  .scrollarea{flex:1;overflow:hidden;display:flex;flex-direction:column;gap:14px;padding-top:8px}
  .h1{font-size:22px;line-height:27px;font-weight:800;letter-spacing:-.5px}
  .sub{font-size:13px;line-height:19px;font-weight:600;color:var(--t2);margin-top:6px}
  .fl{font-size:11.5px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.5px;margin-bottom:7px}
  .input{background:#fff;border:1px solid var(--line);border-radius:13px;padding:14px 15px;font-size:14.5px;font-weight:700;box-shadow:var(--shadow-sm);display:flex;align-items:center;gap:8px}
  .input .ph{color:var(--t3);font-weight:600}.input .pre{color:var(--t3);font-weight:800}
  .avail{margin-left:auto;font-size:11.5px;font-weight:800;color:var(--green1);display:flex;align-items:center;gap:4px}
  .disc{font-size:11px;line-height:16px;font-weight:650;color:var(--t3);background:#FFF8E9;border:1px solid #FDECC2;border-radius:11px;padding:10px 12px}
  .btn{height:52px;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:8px;font-size:15px;font-weight:800;color:#fff;background:linear-gradient(140deg,var(--green1),var(--green2));box-shadow:0 12px 26px rgba(15,183,83,.32)}
  .btn.dark{background:linear-gradient(140deg,#1A1D25,#33384A)}
  .cta{padding:14px 0 18px;margin-top:auto}
  .card{background:#fff;border-radius:18px;border:1px solid var(--line);box-shadow:var(--shadow-sm)}
  .searchbar{display:flex;align-items:center;gap:9px;background:#fff;border:1px solid var(--line);border-radius:13px;padding:13px 15px;font-size:14px;font-weight:650;color:var(--t3);box-shadow:var(--shadow-sm)}
  .lgchips{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
  .lgchips::-webkit-scrollbar{display:none}
  .lgchip{flex:none;padding:8px 13px;border-radius:999px;background:#fff;border:1px solid var(--line);font-size:12px;font-weight:800;color:var(--t2);box-shadow:var(--shadow-sm);white-space:nowrap}
  .lgchip.on{background:var(--t1);color:#fff;border-color:transparent}
  .lgsec{font-size:11.5px;font-weight:800;color:var(--t2);text-transform:uppercase;letter-spacing:.5px;margin:6px 0 2px}
  .lgroup{display:flex;flex-direction:column;gap:10px}
  .teamrow{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:11px 13px;box-shadow:var(--shadow-sm)}
  .teamrow.on{border-color:var(--green1);box-shadow:0 0 0 2px rgba(15,183,83,.25)}
  .teamrow .crest{width:38px;height:38px;border-radius:10px;font-size:11px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;background:linear-gradient(150deg,var(--red),#8F1109);flex:none}
  .teamrow .tn{font-size:14px;font-weight:800}
  .teamrow .tc{font-size:11px;font-weight:650;color:var(--t2);margin-top:1px}
  .teamrow .rad{margin-left:auto;width:20px;height:20px;border-radius:50%;border:2px solid var(--line);flex:none}
  .teamrow.on .rad{border-color:var(--green1);background:radial-gradient(circle,var(--green1) 40%,transparent 46%)}
  .teamsel{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,#fff,#F3F7FD);border:1px solid var(--line);border-radius:15px;padding:13px 14px;box-shadow:var(--shadow-sm)}
  .teamsel .crest{width:44px;height:44px;border-radius:11px;font-size:13px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:800;background:linear-gradient(150deg,var(--red),#8F1109);flex:none}
  .teamsel .tn{font-size:14.5px;font-weight:800}.teamsel .tc{font-size:11.5px;font-weight:650;color:var(--t2);margin-top:1px}
  .teamsel .chg{margin-left:auto;font-size:12px;font-weight:800;color:var(--cyan)}
  .crestbuild{display:flex;flex-direction:column;align-items:center;gap:14px;background:linear-gradient(160deg,#fff,#F4F7FD);border:1px solid var(--line);border-radius:20px;padding:22px 16px;box-shadow:var(--shadow-sm)}
  .crest{width:96px;height:96px;border-radius:16px;background:linear-gradient(150deg,var(--red),#8F1109);display:flex;align-items:center;justify-content:center;font-size:26px;font-weight:800;color:#fff;box-shadow:0 12px 30px rgba(228,54,43,.32)}
  .swatches{display:flex;gap:11px}
  .sw{width:34px;height:34px;border-radius:50%;border:2px solid #fff;box-shadow:0 3px 9px rgba(0,0,0,.15);position:relative}
  .sw.on::after{content:"";position:absolute;inset:-5px;border:2px solid var(--t1);border-radius:50%}
  .emrow{display:flex;gap:9px}
  .em{width:44px;height:44px;border-radius:12px;background:#fff;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-size:19px}
  .em.on{border-color:var(--t1);border-width:2px}
  .seg{display:flex;background:#EBEEF4;border-radius:13px;padding:4px;gap:4px}
  .segopt{flex:1;text-align:center;padding:11px;border-radius:10px;font-size:13px;font-weight:800;color:var(--t2)}
  .segopt.on{background:#fff;color:var(--t1);box-shadow:var(--shadow-sm)}
  .visbox{font-size:12px;line-height:17px;font-weight:650;color:var(--t2);background:#EFF6FF;border:1px solid #DCEAFB;border-radius:12px;padding:11px 13px}
  .visbox b{color:var(--t1)}
  .visbox.inv{background:#F4EEFF;border-color:#E4D8FB}
  .invlink{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:13px;padding:12px 13px;box-shadow:var(--shadow-sm);margin-top:10px}
  .invlink .ilk{font-size:10.5px;font-weight:800;color:var(--t3);text-transform:uppercase;letter-spacing:.5px}
  .invlink .ilv{font-size:13px;font-weight:800;color:var(--t1);margin-top:2px}
  .invlink .ilbtns{margin-left:auto;display:flex;gap:7px}
  .invlink .ilb{font-size:11.5px;font-weight:800;color:var(--cyan);background:#EAF6FF;border-radius:999px;padding:7px 12px}
  .trow{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 15px;box-shadow:var(--shadow-sm)}
  .trow .tt{font-size:13.5px;font-weight:800}.trow .ts{font-size:11.5px;font-weight:650;color:var(--t2);margin-top:2px}
  .tog{margin-left:auto;width:46px;height:28px;border-radius:999px;background:var(--green1);position:relative;flex:none}
  .tog::after{content:"";position:absolute;top:3px;right:3px;width:22px;height:22px;border-radius:50%;background:#fff}
  .tog.off{background:#CDD3DE}.tog.off::after{right:auto;left:3px}
  .chk{width:24px;height:24px;border-radius:7px;background:var(--green1);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;flex:none}
  .chk.off{background:#fff;border:1.5px solid var(--line);color:transparent}
  .summ{display:flex;align-items:center;gap:13px;padding:16px}
  .summ .crest{width:56px;height:56px;font-size:15px}
  .summ .sn{font-size:16px;font-weight:800}.summ .sh{font-size:12px;font-weight:700;color:var(--t2);margin-top:2px}
  .srow{display:flex;align-items:center;padding:12px 16px;border-top:1px solid var(--line);font-size:13px;font-weight:700}
  .srow .k{color:var(--t2)}.srow .v{margin-left:auto;font-weight:800}
  .celebrate{align-items:center;text-align:center;justify-content:center;gap:0}
  .cbadge{width:110px;height:110px;border-radius:20px;background:linear-gradient(150deg,var(--red),#8F1109);display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800;color:#fff;box-shadow:0 20px 44px rgba(228,54,43,.36);margin:0 auto}
  .checklist{display:flex;flex-direction:column;gap:10px;width:100%;margin-top:18px}
  .cli{display:flex;align-items:center;gap:12px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:13px 14px;box-shadow:var(--shadow-sm);text-align:left}
  .cli .ci{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:16px;flex:none}
  .cli .cn{font-size:13px;font-weight:800}.cli .cs{font-size:11px;font-weight:650;color:var(--t2)}
  .cli .arr{margin-left:auto;color:var(--t3);font-weight:800}
</style></head>
<body>
<div class="frames">
'''

CC01T=f'''
  <!-- CC-01T SELECT TEAM -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-01T</div><div class="fname">Select Team — League Picker<span>Search · filter by league · {total} clubs</span></div></div>
  <div class="phone">
    <div class="top"><div class="back">‹</div><div class="htitle">Pick your team</div><div class="stepind">Step 1 of 6</div></div>
    <div class="steps"><i class="on"></i><i></i><i></i><i></i><i></i><i></i></div>
    <div class="body"><div class="scrollarea">
      <div class="searchbar">🔍 Search {total}+ clubs or cities…</div>
      <div class="lgchips">{chips}</div>
{groups}      <div class="disc">⚠️ Real club &amp; league names shown for concept. Official names, badges &amp; data require licensing or an official data provider before launch.</div>
    </div><div class="cta"><div class="btn">Use Arsenal ›</div></div></div>
  </div></div>
'''

REST='''
  <!-- CC-01 BASICS -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-01</div><div class="fname">Create Club — Basics<span>Name · handle · region</span></div></div>
  <div class="phone">
    <div class="top"><div class="back">‹</div><div class="htitle">Club basics</div><div class="stepind">Step 2 of 6</div></div>
    <div class="steps"><i class="on"></i><i class="on"></i><i></i><i></i><i></i><i></i></div>
    <div class="body"><div class="scrollarea">
      <div class="fl">Your team</div>
      <div class="teamsel"><div class="crest cr-red">ARS</div><div style="flex:1"><div class="tn">Arsenal</div><div class="tc">London · Premier League</div></div><div class="chg">Change</div></div>
      <div class="field"><div class="fl">Club name</div><div class="input">Arsenal Fans</div></div>
      <div class="field"><div class="fl">Handle</div><div class="input"><span class="pre">@</span>arsenalfans<span class="avail">✓ Available</span></div></div>
      <div class="field"><div class="fl">City / Region</div><div class="input">London, UK 🇬🇧</div></div>
      <div class="disc">⚠️ SFL clubs are fan communities. Choosing a team does not imply official affiliation, licence or endorsement.</div>
    </div><div class="cta"><div class="btn">Continue</div></div></div>
  </div></div>

  <!-- CC-02 IDENTITY -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-02</div><div class="fname">Identity — Crest &amp; Colours<span>Shield builder</span></div></div>
  <div class="phone">
    <div class="top"><div class="back">‹</div><div class="htitle">Club identity</div><div class="stepind">Step 3 of 6</div></div>
    <div class="steps"><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i><i></i></div>
    <div class="body"><div class="scrollarea">
      <div class="crestbuild">
        <div class="crest cr-red">ARS</div>
        <div class="swatches">
          <div class="sw on" style="background:linear-gradient(150deg,#F0564A,#A81C12)"></div>
          <div class="sw" style="background:linear-gradient(150deg,#5AA0E6,#1B569B)"></div>
          <div class="sw" style="background:linear-gradient(150deg,#F3CC55,#B0800A)"></div>
          <div class="sw" style="background:linear-gradient(150deg,#5FC27E,#1C8348)"></div>
          <div class="sw" style="background:linear-gradient(150deg,#B07CF0,#6A34B8)"></div>
          <div class="sw" style="background:linear-gradient(150deg,#43C4C9,#157B7F)"></div>
        </div>
        <div class="emrow"><div class="em on">🛡️</div><div class="em">⚽</div><div class="em">🦁</div><div class="em">⭐</div><div class="em">🔥</div></div>
      </div>
      <div class="field"><div class="fl">Initials on crest</div><div class="input">ARS</div></div>
      <div class="field"><div class="fl">Club motto <span style="text-transform:none;color:var(--t3)">(optional)</span></div><div class="input">Victoria Concordia Crescit</div></div>
    </div><div class="cta"><div class="btn">Continue</div></div></div>
  </div></div>

  <!-- CC-03 TYPE & RULES -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-03</div><div class="fname">Type &amp; Rules<span>Visibility · approvals</span></div></div>
  <div class="phone">
    <div class="top"><div class="back">‹</div><div class="htitle">How it runs</div><div class="stepind">Step 4 of 6</div></div>
    <div class="steps"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i><i></i></div>
    <div class="body"><div class="scrollarea">
      <div class="field"><div class="fl">Who can find your club</div><div class="seg"><div class="segopt on">Public</div><div class="segopt">Invite-only</div></div></div>
      <div class="visbox pubonly">🌍 <b>Public</b> — your club appears in Discovery, search &amp; league tables. Anyone can apply to join.</div>
      <div class="invonly" style="display:none">
        <div class="visbox inv">🔒 <b>Invite-only</b> — hidden from Discovery. Fans join with your link or code.</div>
        <div class="invlink"><div><div class="ilk">Your invite link</div><div class="ilv num">sfl.live/c/arsenal-x8f2</div></div><div class="ilbtns"><div class="ilb">Copy</div><div class="ilb">Share</div></div></div>
      </div>
      <div class="trow"><div><div class="tt">Approve new fans</div><div class="ts">Review each application before they join</div></div><div class="tog"></div></div>
      <div class="trow"><div><div class="tt">Members can post to club feed</div><div class="ts">Off = only you (Manager) can post</div></div><div class="tog"></div></div>
      <div class="trow"><div><div class="tt">Age-restricted content</div><div class="ts">Keep the club 18+</div></div><div class="tog off"></div></div>
      <div class="field"><div class="fl">Category</div><div class="input">Match-day &amp; watchalongs</div></div>
    </div><div class="cta"><div class="btn">Continue</div></div></div>
  </div></div>

  <!-- CC-04 MANAGER AGREEMENT -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-04</div><div class="fname">Manager Agreement<span>Commission · KYC · conduct</span></div></div>
  <div class="phone">
    <div class="top"><div class="back">‹</div><div class="htitle">Manager terms</div><div class="stepind">Step 5 of 6</div></div>
    <div class="steps"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i></i></div>
    <div class="body"><div class="scrollarea">
      <div class="h1">Before you go live</div>
      <div class="card" style="padding:2px 16px">
        <div class="srow" style="border-top:none"><span class="k">Manager commission</span><span class="v">Additive · from platform</span></div>
        <div class="srow"><span class="k">Payouts</span><span class="v">To verified wallet</span></div>
        <div class="srow"><span class="k">Club wallet</span><span class="v">Held in Gold</span></div>
      </div>
      <div class="disc">🛡️ Identity verification (KYC) is required before your club can receive or pay out money. You'll be prompted when you first withdraw.</div>
      <div class="trow"><div class="chk">✓</div><div><div class="tt">I accept the Manager Code of Conduct</div><div class="ts">No misleading real-team claims · fair play · community rules</div></div></div>
      <div class="trow"><div class="chk">✓</div><div><div class="tt">I'm 18+ and these details are accurate</div></div></div>
    </div><div class="cta"><div class="btn dark">Agree &amp; continue</div></div></div>
  </div></div>

  <!-- CC-05 REVIEW & CREATE -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-05</div><div class="fname">Review &amp; Create<span>Final summary</span></div></div>
  <div class="phone">
    <div class="top"><div class="back">‹</div><div class="htitle">Review</div><div class="stepind">Step 6 of 6</div></div>
    <div class="steps"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></div>
    <div class="body"><div class="scrollarea">
      <div class="card">
        <div class="summ"><div class="crest cr-red">ARS</div><div><div class="sn">Arsenal Fans</div><div class="sh">@arsenalfans · London 🇬🇧</div></div></div>
        <div class="srow"><span class="k">Team</span><span class="v">Arsenal</span></div>
        <div class="srow"><span class="k">Visibility</span><span class="v">Public</span></div>
        <div class="srow"><span class="k">Approve fans</span><span class="v">On</span></div>
        <div class="srow"><span class="k">Your roles</span><span class="v">Manager + Fan</span></div>
      </div>
      <div class="disc">You become Manager and Fan of this club. While you run it you can't join or manage another — but you can always explore others.</div>
    </div><div class="cta"><div class="btn">Create Club 🎉</div></div></div>
  </div></div>

  <!-- CC-06 CLUB CREATED -->
  <div class="fw"><div class="flabel"><div class="fnum">CC-06</div><div class="fname">Club Created — First Steps<span>New-club empty state</span></div></div>
  <div class="phone">
    <div class="top"><div class="back" style="opacity:0">‹</div><div class="htitle"></div></div>
    <div class="body"><div class="scrollarea celebrate">
      <div class="cbadge cr-red">ARS</div>
      <div class="h1" style="margin-top:16px">Arsenal Fans is live! 🎉</div>
      <div class="sub" style="text-align:center;max-width:280px">You're the Manager and first Fan. Here's how to get your club buzzing.</div>
      <div class="checklist">
        <div class="cli"><div class="ci" style="background:#EAF3FF">👥</div><div><div class="cn">Invite your first fans</div><div class="cs">Share your club link</div></div><div class="arr">›</div></div>
        <div class="cli"><div class="ci" style="background:#EAFBEF">✅</div><div><div class="cn">Set the first Fan Task</div><div class="cs">Give fans a reason to return daily</div></div><div class="arr">›</div></div>
        <div class="cli"><div class="ci" style="background:#FFF0E9">📡</div><div><div class="cn">Go live for match-day</div><div class="cs">Host a watchalong</div></div><div class="arr">›</div></div>
        <div class="cli"><div class="ci" style="background:#F3EEFF">🎯</div><div><div class="cn">Open a prediction</div><div class="cs">Next fixture: Arsenal vs Chelsea</div></div><div class="arr">›</div></div>
      </div>
    </div><div class="cta"><div class="btn dark">Go to Manager HQ</div></div></div>
  </div></div>

</div>
</body></html>
'''

open(OUT,'w',encoding='utf-8').write(HEAD+CC01T+REST)
print('wrote create-club.dev.html ·', total, 'clubs across', len(LEAGUES), 'leagues')
