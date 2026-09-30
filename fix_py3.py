#!/usr/bin/env python3
"""Patch PRET for Python 3 compatibility"""

def patch(filename, replacements):
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    original = content
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"  fixed: {repr(old)[:60]}")
        else:
            print(f"  MISS:  {repr(old)[:60]}")
    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {filename} patched\n")
    else:
        print(f"  {filename} unchanged\n")

# ── pret.py ──────────────────────────────────────────────────────
patch('pret.py', [
    ('/_____\\||-.', '/_____\\\\||-.'),
])

# ── helper.py ────────────────────────────────────────────────────
patch('helper.py', [
    # regex escape sequences
    ("'Errno -?\\d+\\] (.*)'",        "r'Errno -?\\d+\\] (.*)'"),
    ("'%%\\[ (.*)\\]%%'",              "r'%%\\[ (.*)\\]%%'"),
    ("'%%\\[ Error: (.*)\\]%%'",       "r'%%\\[ Error: (.*)\\]%%'"),
    ("'%%\\[ Flushing: (.*)\\]%%'",    "r'%%\\[ Flushing: (.*)\\]%%'"),
    # USB recv: handle non-UTF-8 binary responses
    ('os.read(self._file, bytes).decode()',
     "os.read(self._file, bytes).decode('latin-1')"),
])

# ── postscript.py ────────────────────────────────────────────────
patch('postscript.py', [
    # line 159: non-regex escape in .replace()
    (".replace('(', '\\(').replace(')', '\\)')",
     ".replace('(', '\\\\(').replace(')', '\\\\)')"),
    # line 942: non-regex escape in PS string literal
    ("ifelse} loop } def\\n'",         "ifelse} loop } def\\n'"),  # context check
    ("{(\\\\\\) search",               "{(\\\\\\\\) search"),
    # regex strings
    ('re.split("\\s+", arg, 1)',       're.split(r"\\s+", arg, 1)'),
    ('re.split("\\s+", arg)',          're.split(r"\\s+", arg)'),
    ('re.sub(",[ \\t\\r\\n]+\\]"',     're.sub(r",[ \\t\\r\\n]+\\]"'),
    # ord() on bytes fix (line ~250)
    ("data = ''.join"
     "(['\\\\{:03o}'.format(ord(char)) for char in data])",
     "if isinstance(data, bytes): data = data.decode('latin-1')\n"
     "    data = ''.join"
     "(['\\\\{:03o}'.format(ord(char)) for char in data])"),
])

# ── printer.py ───────────────────────────────────────────────────
patch('printer.py', [
    ('re.split("\\s+", arg)',          're.split(r"\\s+", arg)'),
    ('re.split("\\s+", arg, 1)',       're.split(r"\\s+", arg, 1)'),
    ('"^[\\.' ,                        'r"^[\\.'),
])

# ── pjl.py ───────────────────────────────────────────────────────
patch('pjl.py', [
    ('"(@PJL ECHO\\s+)?"',             'r"(@PJL ECHO\\s+)?"'),
    ('"CODE(\\d+)?\\s*=\\s*(\\d+)"',   'r"CODE(\\d+)?\\s*=\\s*(\\d+)"'),
    ("'DISPLAY(\\d+)?\\s*=\\s*\"(.*)\"'",
     "r'DISPLAY(\\d+)?\\s*=\\s*\"(.*)\"'"),
    ('"FILEERROR\\s*=\\s*(\\d+)"',     'r"FILEERROR\\s*=\\s*(\\d+)"'),
    ('"TYPE\\s*=\\s*FILE\\s+SIZE\\s*=\\s*(\\d*)"',
     'r"TYPE\\s*=\\s*FILE\\s+SIZE\\s*=\\s*(\\d*)"'),
    ('re.split("\\s+", line, 1)',      're.split(r"\\s+", line, 1)'),
    ('"^(.*)\\s+TYPE\\s*=\\s*DIR$"',   'r"^(.*)\\s+TYPE\\s*=\\s*DIR$"'),
    ('"^(.*)\\s+TYPE\\s*=\\s*FILE"',   'r"^(.*)\\s+TYPE\\s*=\\s*FILE"'),
    ('"FILE\\s+SIZE\\s*=\\s*(\\d*)"',  'r"FILE\\s+SIZE\\s*=\\s*(\\d*)"'),
    ('".*\\s+\\["',                    'r".*\\s+\\["'),
    ('"=(.*) \\s+\\["',                'r"=(.*)\\s+\\["'),
    ('re.split("\\s+", arg, 1)',       're.split(r"\\s+", arg, 1)'),
    ('re.split("\\s+", arg, 2)',       're.split(r"\\s+", arg, 2)'),
    ('"ADDRESS\\s*=\\s*(\\d+)"',       'r"ADDRESS\\s*=\\s*(\\d+)"'),
    ('"DATA\\s*=\\s*(\\d+)"',          'r"DATA\\s*=\\s*(\\d+)"'),
    ('"FILEERROR\\s*=\\s*(\\d+)"',     'r"FILEERROR\\s*=\\s*(\\d+)"'),
    ('"\\s+\\["',                      'r"\\s+\\["'),
    ('if len(re.split("\\s+", arg, 1))',
     'if len(re.split(r"\\s+", arg, 1))'),
])

# ── pcl.py ───────────────────────────────────────────────────────
patch('pcl.py', [
    ('"ECHO (\\d+)"',                  'r"ECHO (\\d+)"'),
])

print("Done. Re-run: python3 -m py_compile pret.py helper.py postscript.py printer.py pjl.py pcl.py")
