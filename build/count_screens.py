import re, glob, os
SCR = os.path.join(os.path.dirname(__file__), '..', 'screens')
total = 0
by_file = {}
for fn in sorted(glob.glob(os.path.join(SCR, '*.dev.html'))):
    s = open(fn, encoding='utf-8').read()
    n = len(re.findall(r'class="fnum"', s))
    if n:
        by_file[os.path.basename(fn)] = n
        total += n
print('total_screens', total)
print('journey_files', len(by_file))
for k, v in by_file.items():
    print(v, k)
