/*
 * capture.js — "Copy to Figma" snapshotter
 * Run this on any page (DevTools console, or as a bookmarklet).
 * It walks the RENDERED DOM, reads computed styles + positions, and copies
 * a JSON snapshot to your clipboard. Paste that JSON into the companion
 * Figma plugin ("HTML Paste to Figma (local)") to rebuild native layers.
 *
 * Usage in DevTools console:
 *   1. Open the page (e.g. http://localhost:8642/screens/onboarding.html)
 *   2. Paste this whole file and press Enter.
 *   3. Call:  copyToFigma()            // whole <body>
 *      or:    copyToFigma('.frames')   // a CSS selector (recommended)
 *      or:    copyToFigma($0)          // the element selected in Elements panel
 */
(function () {
  const px = (v) => (v && v.endsWith('px') ? parseFloat(v) : parseFloat(v) || 0);

  function parseColor(str) {
    if (!str || str === 'transparent' || str === 'none') return null;
    const m = str.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map((s) => parseFloat(s.trim()));
    const a = p.length > 3 ? p[3] : 1;
    if (a === 0) return null;
    return { r: p[0] / 255, g: p[1] / 255, b: p[2] / 255, a };
  }

  // Very small linear-gradient parser: angle + color stops
  function parseGradient(bg) {
    if (!bg || bg.indexOf('linear-gradient') === -1) return null;
    const inner = bg.slice(bg.indexOf('(') + 1, bg.lastIndexOf(')'));
    // split top-level commas (ignore commas inside rgb())
    const parts = [];
    let depth = 0, cur = '';
    for (const ch of inner) {
      if (ch === '(') depth++;
      if (ch === ')') depth--;
      if (ch === ',' && depth === 0) { parts.push(cur.trim()); cur = ''; }
      else cur += ch;
    }
    if (cur.trim()) parts.push(cur.trim());
    let angle = 180;
    let start = 0;
    if (/deg/.test(parts[0])) { angle = parseFloat(parts[0]); start = 1; }
    else if (/^to\s/.test(parts[0])) { start = 1; } // keep default-ish
    const stops = [];
    const colorStops = parts.slice(start);
    colorStops.forEach((s, i) => {
      const cm = s.match(/(rgba?\([^)]+\)|#[0-9a-fA-F]{3,8})/);
      if (!cm) return;
      const pm = s.match(/(\d+(?:\.\d+)?)%/);
      const pos = pm ? parseFloat(pm[1]) / 100 : i / Math.max(1, colorStops.length - 1);
      let col = parseColor(cm[1]);
      if (!col && cm[1][0] === '#') col = hexToRgb(cm[1]);
      if (col) stops.push({ position: pos, color: col });
    });
    if (stops.length < 2) return null;
    return { angle, stops };
  }

  function hexToRgb(h) {
    h = h.replace('#', '');
    if (h.length === 3) h = h.split('').map((c) => c + c).join('');
    return { r: parseInt(h.slice(0, 2), 16) / 255, g: parseInt(h.slice(2, 4), 16) / 255, b: parseInt(h.slice(4, 6), 16) / 255, a: 1 };
  }

  const SKIP = new Set(['SCRIPT', 'STYLE', 'HEAD', 'META', 'LINK', 'NOSCRIPT', 'BR']);

  function serialize(el, rootRect) {
    if (el.nodeType !== 1) return null;
    if (SKIP.has(el.tagName)) return null;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return null;
    const r = el.getBoundingClientRect();
    if (r.width === 0 && r.height === 0) return null;

    const node = {
      tag: el.tagName.toLowerCase(),
      x: r.left - rootRect.left,
      y: r.top - rootRect.top,
      w: r.width,
      h: r.height,
      radius: [px(cs.borderTopLeftRadius), px(cs.borderTopRightRadius), px(cs.borderBottomRightRadius), px(cs.borderBottomLeftRadius)],
      bg: parseColor(cs.backgroundColor),
      gradient: parseGradient(cs.backgroundImage),
      opacity: parseFloat(cs.opacity),
      border: px(cs.borderTopWidth) > 0 ? { w: px(cs.borderTopWidth), color: parseColor(cs.borderTopColor) } : null,
      shadow: cs.boxShadow && cs.boxShadow !== 'none' ? cs.boxShadow : null,
      font: {
        family: cs.fontFamily.split(',')[0].replace(/['"]/g, '').trim(),
        size: px(cs.fontSize),
        weight: parseInt(cs.fontWeight) || 400,
        color: parseColor(cs.color),
        align: cs.textAlign,
        lineHeight: cs.lineHeight === 'normal' ? null : px(cs.lineHeight),
        letterSpacing: cs.letterSpacing === 'normal' ? 0 : px(cs.letterSpacing),
      },
      children: [],
    };

    // Collect element children + meaningful direct text runs (with real bbox via Range)
    el.childNodes.forEach((cn) => {
      if (cn.nodeType === 1) {
        const c = serialize(cn, rootRect);
        if (c) node.children.push(c);
      } else if (cn.nodeType === 3) {
        const txt = cn.textContent.replace(/\s+/g, ' ').trim();
        if (txt) {
          const range = document.createRange();
          range.selectNodeContents(cn);
          const tr = range.getBoundingClientRect();
          node.children.push({
            tag: '#text',
            text: txt,
            x: tr.left - rootRect.left,
            y: tr.top - rootRect.top,
            w: Math.max(tr.width, 1),
            h: Math.max(tr.height, node.font.size * 1.2),
            font: node.font,
            children: [],
          });
        }
      }
    });
    return node;
  }

  window.copyToFigma = function (target) {
    let root = document.body;
    if (typeof target === 'string') root = document.querySelector(target);
    else if (target && target.nodeType === 1) root = target;
    if (!root) { console.error('copyToFigma: target not found:', target); return; }
    const rootRect = root.getBoundingClientRect();
    const tree = serialize(root, rootRect);
    const payload = { version: 1, source: location.href, root: tree };
    const json = JSON.stringify(payload);
    const done = () => console.log('%c✅ Copied to clipboard — paste into the Figma plugin. Size: ' + (json.length / 1024).toFixed(0) + ' KB', 'color:#0FB753;font-weight:bold');
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(json).then(done).catch(() => { window.__figmaJSON = json; console.warn('Clipboard blocked. JSON is in window.__figmaJSON — copy(window.__figmaJSON)'); });
    } else {
      window.__figmaJSON = json;
      console.warn('Clipboard API unavailable. Run: copy(window.__figmaJSON)');
    }
    return payload;
  };

  // ---- On-page UI: floating buttons so you never touch the console ----
  function toast(msg, ok) {
    let t = document.getElementById('__figmaToast');
    if (!t) {
      t = document.createElement('div'); t.id = '__figmaToast';
      t.style.cssText = 'position:fixed;z-index:2147483647;left:50%;bottom:28px;transform:translateX(-50%);padding:12px 20px;border-radius:12px;font:600 14px -apple-system,Segoe UI,sans-serif;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.25);transition:opacity .3s;pointer-events:none';
      document.body.appendChild(t);
    }
    t.textContent = msg; t.style.background = ok ? '#0FB753' : '#E4362B'; t.style.opacity = '1';
    clearTimeout(t.__h); t.__h = setTimeout(() => { t.style.opacity = '0'; }, 2200);
  }

  function copyEl(el, label) {
    const p = window.copyToFigma(el);
    if (p) toast('✓ ' + (label || 'Copied') + ' → now paste in Figma', true);
    else toast('Copy failed — check console', false);
  }

  function injectUI() {
    if (document.getElementById('__figmaBar')) return; // once
    // main floating button
    const bar = document.createElement('div'); bar.id = '__figmaBar';
    bar.style.cssText = 'position:fixed;z-index:2147483647;top:16px;right:16px;display:flex;gap:8px;align-items:center;font:700 13px -apple-system,Segoe UI,sans-serif';
    const all = document.createElement('button');
    all.textContent = '📋 Copy ALL screens to Figma';
    all.style.cssText = 'cursor:pointer;border:0;border-radius:10px;padding:11px 16px;color:#fff;background:linear-gradient(140deg,#0FB753,#7CD843);box-shadow:0 8px 22px rgba(15,183,83,.4)';
    all.onclick = () => copyEl(document.querySelector('.frames') || document.body, 'All screens');
    bar.appendChild(all);
    document.body.appendChild(bar);

    // per-screen buttons
    const screens = document.querySelectorAll('.fw');
    (screens.length ? screens : document.querySelectorAll('.phone')).forEach((el, i) => {
      el.style.position = el.style.position || 'relative';
      const b = document.createElement('button');
      b.textContent = '📋 Copy';
      b.style.cssText = 'position:absolute;z-index:2147483646;top:-4px;right:-4px;cursor:pointer;border:0;border-radius:8px;padding:6px 10px;font:700 12px -apple-system,sans-serif;color:#fff;background:#14161C;opacity:.85;box-shadow:0 4px 12px rgba(0,0,0,.2)';
      b.onmouseenter = () => (b.style.opacity = '1');
      b.onmouseleave = () => (b.style.opacity = '.85');
      b.onclick = (e) => { e.stopPropagation(); copyEl(el, 'Screen ' + (i + 1)); };
      el.appendChild(b);
    });
    toast('Buttons ready — click any "Copy", then paste in the Figma plugin', true);
  }

  injectUI();
  console.log('%cReady. Use the on-page buttons, or run copyToFigma(".fw").', 'color:#1FA8FF;font-weight:bold');
})();
