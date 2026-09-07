from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

sprite_indexes = {
    's1': 0, 's2': 1, 's3': 2, 's4': 3,
    's5': 4, 's6': 5, 'm1': 6, 'm2': 7,
    'm4': 8, 'm9': 9, 'm10': 10, 'm11': 11,
    'm12': 12, 'm13': 13, 'm14': 14, 'v1': 15,
    'e5': 16, 'a2': 17, 'a3': 18, 'a4': 19,
    'd1': 20, 'd3': 21,
}

lines = text.splitlines(keepends=True)
found = set()
out = []
for line in lines:
    for item_id, idx in sprite_indexes.items():
        token = f"id: '{item_id}'"
        if token in line:
            found.add(item_id)
            if 'spriteIndex:' not in line:
                close = line.rfind('}')
                if close < 0:
                    raise RuntimeError(f'Could not patch {item_id}')
                line = line[:close].rstrip() + f", spriteIndex: {idx} " + line[close:]
            break
    out.append(line)
text = ''.join(out)
missing = set(sprite_indexes) - found
if missing:
    raise RuntimeError(f'Menu IDs not found: {sorted(missing)}')

old_visual = '          const visualHtml = `<div class="menu-visual">${placeholderIcon()}</div>`;'
new_visual = '''          const visualHtml = Number.isInteger(item.spriteIndex)
            ? `<div class="menu-visual has-photo"><div class="menu-sprite" style="--sprite-index:${item.spriteIndex}" role="img" aria-label="${itemName}"></div></div>`
            : `<div class="menu-visual">${placeholderIcon()}</div>`;'''
if old_visual in text:
    text = text.replace(old_visual, new_visual, 1)
elif 'class="menu-sprite"' not in text:
    raise RuntimeError('Menu visual render marker not found')

css = '''
    .menu-visual.has-photo { background: #201914; }
    .menu-visual.has-photo::before,
    .menu-visual.has-photo::after { display: none; }
    .menu-sprite {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background-image: url('assets/menu/menu-sprite.webp');
      background-repeat: no-repeat;
      background-size: 400% 600%;
      background-position:
        calc((var(--sprite-index) % 4) * -100%)
        calc((var(--sprite-index) / 4) * -100%);
    }
'''
# CSS calc with modulo/floor is not cross-browser, so generate per-index rules.
rules = []
for idx in range(22):
    col = idx % 4
    row = idx // 4
    x = (col / 3 * 100) if col else 0
    y = (row / 5 * 100) if row else 0
    rules.append(f'    .menu-sprite[style*="--sprite-index:{idx}"] {{ background-position: {x:.6f}% {y:.6f}%; }}')
css = css.replace("      background-position:\n        calc((var(--sprite-index) % 4) * -100%)\n        calc((var(--sprite-index) / 4) * -100%);\n", '') + '\n'.join(rules) + '\n'

if '.menu-sprite {' not in text:
    marker = '</style>'
    if marker not in text:
        raise RuntimeError('Style closing tag not found')
    text = text.replace(marker, css + '  </style>', 1)

if text.count('spriteIndex:') != len(sprite_indexes):
    raise RuntimeError('Unexpected sprite mapping count')
if 'const LIFF_ID = "2010784971-mH3KqiRT"' not in text:
    raise RuntimeError('LIFF guard failed')
if 'function isMondayDate' not in text:
    raise RuntimeError('Monday guard failed')

path.write_text(text, encoding='utf-8')
