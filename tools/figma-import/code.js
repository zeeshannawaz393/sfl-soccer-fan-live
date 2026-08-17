/* code.js — rebuilds a captured DOM snapshot into native Figma layers */
figma.showUI(__html__, { width: 340, height: 260 });

const WEIGHTS = [
  { w: 800, s: 'ExtraBold' }, { w: 700, s: 'Bold' }, { w: 600, s: 'SemiBold' },
  { w: 500, s: 'Medium' }, { w: 400, s: 'Regular' }, { w: 300, s: 'Light' },
];

async function resolveFonts(root) {
  // Collect (family, weight) pairs used in the snapshot
  const families = new Set();
  (function walk(n) {
    if (n.tag === '#text' || (n.font && n.text !== undefined)) families.add(n.font.family);
    else if (n.font) families.add(n.font.family);
    (n.children || []).forEach(walk);
  })(root);

  const loaded = {}; // family -> { styleName: true }
  async function tryLoad(family) {
    if (loaded[family]) return loaded[family];
    const map = {};
    for (const { s } of WEIGHTS) {
      try { await figma.loadFontAsync({ family, style: s }); map[s] = true; } catch (e) {}
    }
    if (Object.keys(map).length === 0) {
      // fallback family
      for (const { s } of WEIGHTS) {
        try { await figma.loadFontAsync({ family: 'Inter', style: s }); map[s] = true; } catch (e) {}
      }
      loaded[family] = { __fallback: 'Inter', ...map };
    } else {
      loaded[family] = map;
    }
    return loaded[family];
  }
  for (const f of families) await tryLoad(f);
  return loaded;
}

function pickStyle(map, weight) {
  for (const { w, s } of WEIGHTS) if (weight >= w && map[s]) return s;
  return map.Regular ? 'Regular' : Object.keys(map).filter((k) => k !== '__fallback')[0];
}

function gradientPaint(g) {
  // angle in CSS degrees (0 = up). Build a rough linear gradient transform.
  const rad = ((g.angle - 90) * Math.PI) / 180;
  const c = Math.cos(rad), s = Math.sin(rad);
  return {
    type: 'GRADIENT_LINEAR',
    gradientTransform: [[c, s, (1 - c - s) / 2], [-s, c, (1 + s - c) / 2]],
    gradientStops: g.stops.map((st) => ({ position: st.position, color: st.color })),
  };
}

async function build(node, parent, offX, offY, fonts) {
  if (node.tag === '#text') {
    const t = figma.createText();
    const map = fonts[node.font.family] || {};
    const fam = map.__fallback || node.font.family;
    const style = pickStyle(map, node.font.weight) || 'Regular';
    try { t.fontName = { family: fam, style }; } catch (e) { t.fontName = { family: 'Inter', style: 'Regular' }; }
    t.characters = node.text;
    t.fontSize = Math.max(1, node.font.size);
    if (node.font.color) t.fills = [{ type: 'SOLID', color: rgb(node.font.color), opacity: node.font.color.a }];
    t.textAlignHorizontal = (node.font.align || 'left').toUpperCase().includes('CENTER') ? 'CENTER'
      : node.font.align === 'right' ? 'RIGHT' : 'LEFT';
    if (node.font.letterSpacing) t.letterSpacing = { unit: 'PIXELS', value: node.font.letterSpacing };
    if (node.font.lineHeight) t.lineHeight = { unit: 'PIXELS', value: node.font.lineHeight };
    t.textAutoResize = 'HEIGHT';
    t.resize(Math.max(node.w, 4), t.height);
    t.x = node.x - offX; t.y = node.y - offY;
    parent.appendChild(t);
    return;
  }

  const f = figma.createFrame();
  f.name = node.tag;
  f.resize(Math.max(node.w, 0.01), Math.max(node.h, 0.01));
  f.x = node.x - offX; f.y = node.y - offY;
  f.clipsContent = false;

  const fills = [];
  if (node.gradient) fills.push(gradientPaint(node.gradient));
  else if (node.bg) fills.push({ type: 'SOLID', color: rgb(node.bg), opacity: node.bg.a });
  f.fills = fills;

  if (node.radius) {
    const [tl, tr, br, bl] = node.radius;
    f.topLeftRadius = tl; f.topRightRadius = tr; f.bottomRightRadius = br; f.bottomLeftRadius = bl;
  }
  if (node.border && node.border.color) {
    f.strokes = [{ type: 'SOLID', color: rgb(node.border.color), opacity: node.border.color.a }];
    f.strokeWeight = node.border.w;
  }
  if (typeof node.opacity === 'number' && node.opacity < 1) f.opacity = node.opacity;
  const shadow = parseShadow(node.shadow);
  if (shadow) f.effects = [shadow];
  parent.appendChild(f);

  for (const c of node.children) await build(c, f, node.x, node.y, fonts);
}

function rgb(c) { return { r: c.r, g: c.g, b: c.b }; }

function parseShadow(str) {
  if (!str || str === 'none') return null;
  // take the first shadow if comma-separated (respect commas inside rgba())
  let depth = 0, first = '';
  for (const ch of str) {
    if (ch === '(') depth++;
    if (ch === ')') depth--;
    if (ch === ',' && depth === 0) break;
    first += ch;
  }
  const inset = /\binset\b/.test(first);
  const cm = first.match(/rgba?\(([^)]+)\)/);
  let color = { r: 0, g: 0, b: 0, a: 0.15 };
  if (cm) {
    const p = cm[1].split(',').map((s) => parseFloat(s.trim()));
    color = { r: p[0] / 255, g: p[1] / 255, b: p[2] / 255, a: p.length > 3 ? p[3] : 1 };
  }
  const nums = (first.replace(/rgba?\([^)]+\)/, '').match(/-?\d*\.?\d+px/g) || []).map((n) => parseFloat(n));
  if (nums.length < 2) return null;
  const [x = 0, y = 0, blur = 0, spread = 0] = nums;
  return {
    type: inset ? 'INNER_SHADOW' : 'DROP_SHADOW',
    color: { r: color.r, g: color.g, b: color.b, a: color.a },
    offset: { x, y }, radius: blur, spread, visible: true, blendMode: 'NORMAL',
  };
}

figma.ui.onmessage = async (msg) => {
  if (msg.type !== 'import') return;
  let payload;
  try { payload = JSON.parse(msg.json); } catch (e) { figma.ui.postMessage({ type: 'error', message: 'Invalid JSON' }); return; }
  const root = payload.root;
  if (!root) { figma.ui.postMessage({ type: 'error', message: 'No root node in payload' }); return; }

  figma.ui.postMessage({ type: 'status', message: 'Loading fonts…' });
  const fonts = await resolveFonts(root);

  // place at a clear spot right of existing content
  let maxX = 0;
  for (const c of figma.currentPage.children) maxX = Math.max(maxX, c.x + c.width);
  const startX = maxX ? maxX + 80 : 0;

  figma.ui.postMessage({ type: 'status', message: 'Building layers…' });
  const container = figma.createFrame();
  container.name = 'Imported: ' + (payload.source || 'page').split('/').pop();
  container.resize(Math.max(root.w, 1), Math.max(root.h, 1));
  container.x = startX; container.y = 0;
  container.fills = root.bg ? [{ type: 'SOLID', color: rgb(root.bg), opacity: root.bg.a }] : [];
  figma.currentPage.appendChild(container);

  for (const c of root.children) await build(c, container, root.x, root.y, fonts);

  figma.currentPage.selection = [container];
  figma.viewport.scrollAndZoomIntoView([container]);
  figma.ui.postMessage({ type: 'done', message: 'Imported ✓' });
};
