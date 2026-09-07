from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

positions = {
    's1': '0% 0%', 's2': '33.333% 0%', 's3': '66.667% 0%', 's4': '100% 0%',
    's5': '0% 20%', 's6': '33.333% 20%', 'm1': '66.667% 20%', 'm2': '100% 20%',
    'm4': '0% 40%', 'm9': '33.333% 40%', 'm10': '66.667% 40%', 'm11': '100% 40%',
    'm12': '0% 60%', 'm13': '33.333% 60%', 'm14': '66.667% 60%', 'v1': '100% 60%',
    'e5': '0% 80%', 'a2': '33.333% 80%', 'a3': '66.667% 80%', 'a4': '100% 80%',
    'd1': '0% 100%', 'd3': '33.333% 100%',
}
assert len(positions) == 22

for item_id in positions:
    if f"id: '{item_id}'" not in text:
        raise RuntimeError(f'Menu item missing: {item_id}')

marker = '    const LIFF_ID = "2010784971-mH3KqiRT";'
if 'const MENU_SPRITE_POSITIONS' not in text:
    if marker not in text:
        raise RuntimeError('LIFF marker not found')
    lines = ['    const MENU_SPRITE_POSITIONS = {']
    lines.extend(f"      '{k}': '{v}'," for k, v in positions.items())
    lines.append('    };')
    text = text.replace(marker, marker + '\n' + '\n'.join(lines), 1)

old_visual = '          const visualHtml = `<div class="menu-visual">${placeholderIcon()}</div>`;'
new_visual = '''          const spritePosition = MENU_SPRITE_POSITIONS[item.id];
          const visualHtml = spritePosition
            ? `<div class="menu-visual has-photo"><div class="menu-photo-sprite" role="img" aria-label="${itemName}" style="background-position:${spritePosition}"></div></div>`
            : `<div class="menu-visual">${placeholderIcon()}</div>`;'''
if old_visual in text:
    text = text.replace(old_visual, new_visual, 1)
elif 'MENU_SPRITE_POSITIONS[item.id]' not in text:
    raise RuntimeError('Menu visual render marker not found')

photo_css = '''
    .menu-visual.has-photo {
      height: 86px;
      min-height: 86px;
      align-self: start;
      background: #201914;
      border-color: rgba(224,189,115,.24);
    }
    .menu-visual.has-photo::before,
    .menu-visual.has-photo::after { display: none; }
    .menu-photo-sprite {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background-image: url('assets/menu/menu-sprite.webp');
      background-size: 400% 600%;
      background-repeat: no-repeat;
      border-radius: inherit;
    }
'''
if '.menu-photo-sprite {' not in text:
    if '</style>' not in text:
        raise RuntimeError('Style closing tag not found')
    text = text.replace('</style>', photo_css + '  </style>', 1)

if text.count('const MENU_SPRITE_POSITIONS') != 1:
    raise RuntimeError('Unexpected sprite mapping count')
if text.count('MENU_SPRITE_POSITIONS[item.id]') != 1:
    raise RuntimeError('Unexpected sprite renderer count')
if 'function isMondayDate' not in text:
    raise RuntimeError('Monday booking guard missing')
if marker not in text:
    raise RuntimeError('LIFF ID missing')

path.write_text(text, encoding='utf-8')
