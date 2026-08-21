"""Batch theme token fixes across screens/*.dev.html — colors only."""
import re, glob, os

SCR = os.path.join(os.path.dirname(__file__), '..', 'screens')

# Card / surface patterns (themeable white → token)
SURFACE_REPLACEMENTS = [
    (r'\.card\{([^}]*?)background:#fff\b', r'.card{\1background:var(--card)'),
    (r'\.card\{([^}]*?)background:#FFF\b', r'.card{\1background:var(--card)'),
    (r'\.card\{([^}]*?)background:#FFFFFF\b', r'.card{\1background:var(--card)'),
    (r'\.searchbar\{([^}]*?)background:#fff\b', r'.searchbar{\1background:var(--card)'),
    (r'\.inp\{([^}]*?)background:#fff\b', r'.inp{\1background:var(--card)'),
    (r'\.mod\{([^}]*?)background:#fff\b', r'.mod{\1background:var(--card)'),
    (r'\.mission\{([^}]*?)background:#fff\b', r'.mission{\1background:var(--card)'),
    (r'\.sheet\{([^}]*?)background:#fff\b', r'.sheet{\1background:var(--card)'),
    (r'\.feed-item\{([^}]*?)background:#fff\b', r'.feed-item{\1background:var(--card)'),
    (r'\.coinpill\{([^}]*?)background:#fff\b', r'.coinpill{\1background:var(--card)'),
    (r'\.hicon\{([^}]*?)background:#fff\b', r'.hicon{\1background:var(--card)'),
    (r'\.back,([^}]*?)background:#fff\b', r'.back,\1background:var(--card)'),
    (r'\.back\{([^}]*?)background:#fff\b', r'.back{\1background:var(--card)'),
    (r'\.btn\.ghost\{([^}]*?)background:#fff\b', r'.btn.ghost{\1background:var(--card)'),
    (r'\.seg i\.on\{([^}]*?)background:#fff\b', r'.seg i.on{\1background:var(--card)'),
    (r'\.foltab\.on\{([^}]*?)background:#fff\b', r'.foltab.on{\1background:var(--card)'),
    (r'\.pvopt\.on\{([^}]*?)background:#fff\b', r'.pvopt.on{\1background:var(--card)'),
    (r'\.setgrp\{([^}]*?)background:#fff\b', r'.setgrp{\1background:var(--card)'),
    (r'\.explorelink\{([^}]*?)background:#fff\b', r'.explorelink{\1background:var(--card)'),
    (r'\.duty\{([^}]*?)background:#fff\b', r'.duty{\1background:var(--card)'),
    (r'\.mom\{([^}]*?)background:#fff\b', r'.mom{\1background:var(--card)'),
    (r'\.skel\{([^}]*?)background:#fff\b', r'.skel{\1background:var(--card)'),
    (r'\.ticket\{([^}]*?)background:#fff\b', r'.ticket{\1background:var(--card)'),
    (r'\.gclub\{([^}]*?)background:#fff\b', r'.gclub{\1background:var(--card)'),
    (r'\.gwchip\{([^}]*?)background:#fff\b', r'.gwchip{\1background:var(--card)'),
    (r'\.fchip\{([^}]*?)background:#fff\b', r'.fchip{\1background:var(--card)'),
    (r'\.collitem\{([^}]*?)background:#fff\b', r'.collitem{\1background:var(--card)'),
    (r'\.rolecard\{([^}]*?)background:#fff\b', r'.rolecard{\1background:var(--card)'),
    (r'\.statgrid\{([^}]*?)background:#fff\b', r'.statgrid{\1background:var(--card)'),
    (r'\.valchart\{([^}]*?)background:#fff\b', r'.valchart{\1background:var(--card)'),
    (r'\.summary\{([^}]*?)background:#fff\b', r'.summary{\1background:var(--card)'),
    (r'\.hrow\{([^}]*?)background:#fff\b', r'.hrow{\1background:var(--card)'),
    (r'\.wdl\{([^}]*?)background:#fff\b', r'.wdl{\1background:var(--card)'),
    (r'\.pkg\{([^}]*?)background:#fff\b', r'.pkg{\1background:var(--card)'),
    (r'\.pcard\{([^}]*?)background:#fff\b', r'.pcard{\1background:var(--card)'),
    (r'\.fixcard\{([^}]*?)background:#fff\b', r'.fixcard{\1background:var(--card)'),
    (r'\.clubrow\{([^}]*?)background:#fff\b', r'.clubrow{\1background:var(--card)'),
    (r'\.consent\{([^}]*?)background:#fff\b', r'.consent{\1background:var(--card)'),
    (r'\.checkopt\{([^}]*?)background:#fff\b', r'.checkopt{\1background:var(--card)'),
    (r'\.tmsg\.them\{([^}]*?)background:#fff\b', r'.tmsg.them{\1background:var(--card)'),
    (r'\.cat\{([^}]*?)background:#fff\b', r'.cat{\1background:var(--card)'),
    (r'\.fieldwrap\{([^}]*?)background:#fff\b', r'.fieldwrap{\1background:var(--card)'),
    (r'\.seg\{([^}]*?)background:#E9ECF4\b', r'.seg{\1background:var(--raised2)'),
    (r'\.seg\{([^}]*?)background:#EBEEF4\b', r'.seg{\1background:var(--raised2)'),
    (r'\.foltabs\{([^}]*?)background:#E9ECF4\b', r'.foltabs{\1background:var(--raised2)'),
    (r'\.pvswitch\{([^}]*?)background:#E9ECF4\b', r'.pvswitch{\1background:var(--raised2)'),
]

# Dark-native phone shells → token
PHONE_BG = [
    (r'background:#07090D\b', 'background:var(--bg)'),
    (r'background:#0B0E14\b', 'background:var(--bg)'),
]

# In-phone structural text (not hero/back/button white)
TEXT_FIXES = [
    (r'(\.(?:kv \.v|idfield|target \.tt|target \.big|rewcard \.rt|ticket \.tclub|stat\.(?:fans|pos) \.v|htitle|cname|modrow|field|toggle))\{([^}]*?)color:#fff\b', r'\1{\2color:var(--t1)'),
]

SKIP_FILES = {'light-mode.dev.html', 'room-templates.dev.html', 'discovery-live.dev.html'}

def fix_file(path):
    name = os.path.basename(path)
    if name in SKIP_FILES:
        return 0
    s = open(path, encoding='utf-8').read()
    orig = s
    for pat, rep in SURFACE_REPLACEMENTS:
        s = re.sub(pat, rep, s, flags=re.I)
    if name in ('journey14.dev.html', 'journey17.dev.html', 'journey19.dev.html', 'journey8.dev.html', 'journey9.dev.html', 'journey10.dev.html'):
        for pat, rep in PHONE_BG:
            s = re.sub(pat, rep, s)
    if name in ('journey14.dev.html', 'journey17.dev.html', 'journey19.dev.html'):
        for pat, rep in TEXT_FIXES:
            s = re.sub(pat, rep, s)
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
        return 1
    return 0

changed = 0
for path in glob.glob(os.path.join(SCR, '*.dev.html')):
    changed += fix_file(path)
print('files_changed', changed)
