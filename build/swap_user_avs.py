"""One-off: map circular user avatars onto up_01..up_16. Full-bleed / player art left alone."""
import os, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'screens')

NAME_MAP = [
    ('gloveboy', 10), ('glove', 10),
    ('lucia', 7), ('omar', 3),
    ('jordan', 1), ('jj okafor', 1), ('jj_reds', 1), ('jj</', 1), ('>jj<', 1),
    ('nadia', 4), ('teo', 6), ('kojo', 5),
    ('sara', 9),
    ('mikael', 8), ('mikkel', 8), ('mikael', 8), (' mik', 8),
    ('priya', 11), ('mo a', 13),
    ('lena', 14), ('diego', 10),
    ('marco', 1), ('tom h', 6),
    ('danny', 6), ('matty', 13), ('maria', 2),
    ('jay m', 1), ('robbie', 8),
    ('zeeshan', 12), ('alex morgan', 12), ('alex r', 12),
    ('welcome back', 12),
]

FILE_MAP = {
    'lucia_t.jpg': 7, 'omar_t.jpg': 3, 'kojo_t.jpg': 5, 'sara_t.jpg': 9,
    'nadia_t.jpg': 4, 'q1_t.jpg': 12, 'q2_t.jpg': 15, 'q3_t.jpg': 2, 'q4_t.jpg': 16,
    'dk_t.jpg': 6, 'mb_t.jpg': 13, 'jj_t.jpg': 1, 'teo_t.jpg': 6,
    'mikkel_t.jpg': 8, 'glove_t.jpg': 10, 'rb_t.jpg': 8, 'cc_t.jpg': 2,
    'rs1_t.jpg': 14, 'rs2_t.jpg': 4, 'rs3_t.jpg': 11,
    'ss1_t.jpg': 7, 'ss2_t.jpg': 9, 'ss3_t.jpg': 15,
    'fb_f1.jpg': 14, 'fb_f2.jpg': 7, 'fb_f3.jpg': 11,
    'fb_m1.jpg': 1, 'fb_m2.jpg': 10, 'fb_m3.jpg': 6, 'fb_m4.jpg': 8,
    'fb_host.jpg': 12,
}

USER_FILES = set(FILE_MAP) | {
    'fb_f1.jpg','fb_f2.jpg','fb_f3.jpg','fb_m1.jpg','fb_m2.jpg','fb_m3.jpg','fb_m4.jpg','fb_host.jpg'
}

SKIP_CLASS = {
    'hosttile','campreview','wavid','waclip','wath','callbg','videofull','selfview',
    'livecard','pthumb','cover','coverthumb','hero','vid','player','pimg','th',
    'cand','pcard','rc','waclip','callava'
}
HIT_CLASS = {
    'av','avatar','ha','fav','folav','hav','cav','aav','sav','ha2','selavatar',
    'epavatar','tav','simg','pav','oav','gav','rav'
}

TAG_RE = re.compile(r'<([a-zA-Z0-9]+)([^>]*?)>', re.S)
URL_RE = re.compile(r"""url\(['"]?assets/([\w.\-]+)['"]?\)""")
CLASS_RE = re.compile(r"""class=['"]([^'"]+)['"]""")

def classes(attrs):
    m = CLASS_RE.search(attrs)
    return set((m.group(1) if m else '').split())

def pick(fn, nearby):
    low = nearby.lower()
    for name, n in NAME_MAP:
        if name in low:
            return n
    return FILE_MAP.get(fn, 12)

def should_swap(cls, attrs, fn):
    if fn not in USER_FILES:
        return False
    if cls & SKIP_CLASS:
        return False
    if 'ph' in cls and 'avatar' not in cls and 'av' not in cls:
        return False
    if cls & HIT_CLASS:
        return True
    if 'border-radius:50%' in attrs.replace(' ', '') or 'border-radius: 50%' in attrs:
        return True
    return False

def patch(html):
    n = 0
    def repl(m):
        nonlocal n
        tag, attrs = m.group(1), m.group(2)
        um = URL_RE.search(attrs)
        if not um:
            return m.group(0)
        fn = um.group(1)
        cls = classes(attrs)
        if not should_swap(cls, attrs, fn):
            return m.group(0)
        end = m.end()
        nearby = html[m.start():min(len(html), end+220)]
        idx = pick(fn, nearby)
        new = f'up_{idx:02d}.png'
        if new == fn:
            return m.group(0)
        n += 1
        new_attrs = URL_RE.sub(lambda x: x.group(0).replace(fn, new) if x.group(1)==fn else x.group(0), attrs, count=1)
        return f'<{tag}{new_attrs}>'
    return TAG_RE.sub(repl, html), n

total = 0
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith('.dev.html'):
            continue
        path = os.path.join(dirpath, fn)
        raw = open(path, encoding='utf-8').read()
        out, n = patch(raw)
        if n:
            open(path, 'w', encoding='utf-8').write(out)
            print(f'{n:3d}  {fn}')
            total += n
print('total', total)
