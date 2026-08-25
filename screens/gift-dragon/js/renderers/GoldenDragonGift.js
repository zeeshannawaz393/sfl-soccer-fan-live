// GoldenDragonGift — premium full-screen gift renderer.
//
// A procedural Chinese/eastern golden dragon drawn on a single <canvas>:
//   • Head leads along a Catmull-Rom flight path; the serpentine body is produced by
//     sampling that same path at increasing time-lag, so the body flows and follows
//     the head with delay (no per-frame history, so it is frame-rate independent).
//   • Golden metallic shading, glowing edges, horns, whiskers, mane, four clawed
//     limbs, dorsal ridge and a long tapering tail.
//   • Cinematic phases: atmosphere → entrance → flight → circle → hero → finale → exit.
//
// The renderer is deliberately self-contained. GiftAnimationManager only calls
// play() / setCombo() / destroy(), so this class can later be replaced by an
// alpha-video / SVGA element without changing the manager.

import { ParticleSystem } from '../fx/ParticleSystem.js';
import { QUALITY } from '../config/gifts.js';
import { dragonHeadSVG, dragonHeadFrontSVG, HEAD_VB, FRONT_VB } from '../assets/dragonHead.js';

const HEAD_SCALE = 7.6;   // profile head height ≈ HEAD_SCALE × base body radius
const FRONT_SCALE = 9.0;  // front head is a touch larger for the hero turn

const PHASE = { atmos: [0, 0.15], entrance: [0.10, 0.28], flight: [0.28, 0.44],
  circle: [0.44, 0.62], hero: [0.62, 0.80], finale: [0.78, 0.92], exit: [0.90, 1] };

// Flight waypoints in normalised screen coords (0..1). Sequential — the body
// follows this exact curve. Off-screen entries/exits keep the reveal clean.
const WP = [
  { x: -0.28, y: 1.25 }, // 0 off-screen bottom-left
  { x: 0.20, y: 0.74 },  // 1 rise into lower-left
  { x: 0.88, y: 0.50 },  // 2 sweep to the right
  { x: 0.26, y: 0.60 },  // 3 curve back (circle begins)
  { x: 0.52, y: 0.80 },  // 4 circle — bottom
  { x: 0.82, y: 0.52 },  // 5 circle — right
  { x: 0.50, y: 0.30 },  // 6 circle — top (framing the streamer)
  { x: 0.50, y: 0.24 },  // 7 hero — upper middle
  { x: 0.58, y: -0.40 }, // 8 exit — up and out
];
// Per-leg timing [t0, t1, fromIdx]. Legs are sequential fromIdx -> fromIdx+1.
const LEGS = [
  [0.00, 0.15, 0], [0.15, 0.33, 1], [0.33, 0.45, 2], [0.45, 0.56, 3],
  [0.56, 0.66, 4], [0.66, 0.74, 5], [0.74, 0.84, 6], [0.84, 1.00, 7],
];

const PALETTES = {
  gold: { dark: '#5a3d05', mid: '#c8890c', lite: '#ffd54a', hi: '#fff4bf',
    edge: 'rgba(255,207,90,0.9)', illum: '#ff9a3c', ember: '#ffcf5a', eye: '#fff6cf' },
  jade: { dark: '#0b3b2e', mid: '#12876a', lite: '#4fe3b0', hi: '#d8fff2',
    edge: 'rgba(120,255,210,0.9)', illum: '#ffd54a', ember: '#8affd8', eye: '#eafff8' },
};

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const smooth = (u) => u * u * (3 - 2 * u);
function catmull(p0, p1, p2, p3, u) {
  const u2 = u * u, u3 = u2 * u;
  return {
    x: 0.5 * ((2 * p1.x) + (-p0.x + p2.x) * u + (2*p0.x - 5*p1.x + 4*p2.x - p3.x) * u2 + (-p0.x + 3*p1.x - 3*p2.x + p3.x) * u3),
    y: 0.5 * ((2 * p1.y) + (-p0.y + p2.y) * u + (2*p0.y - 5*p1.y + 4*p2.y - p3.y) * u2 + (-p0.y + 3*p1.y - 3*p2.y + p3.y) * u3),
  };
}

export class GoldenDragonGift {
  constructor({ root, quality = 'high', config = {}, onDone } = {}) {
    this.root = root;
    this.q = QUALITY[quality] || QUALITY.high;
    this.config = config;
    this.pal = PALETTES[config.variant] || PALETTES.gold;
    this.onDone = onDone || (() => {});
    this.duration = config.duration || 8000;
    this._raf = 0; this._t0 = null; this._alive = false;
    this._combo = 1; this._comboPulse = 0;
    this._onResize = () => this._resize();
  }

  play(sender = {}) {
    this.sender = { name: sender.senderName || 'Guest', avatar: sender.senderAvatar || '', quantity: sender.quantity || 1 };
    this._combo = this.sender.quantity;
    this._buildDom();
    this.ps = new ParticleSystem(this.q.particles * 8);
    this._resize();
    window.addEventListener('resize', this._onResize);
    this._alive = true;
    this._raf = requestAnimationFrame((ts) => this._loop(ts));
  }

  // Bump the combo counter WITHOUT restarting the dragon.
  setCombo(n) {
    this._combo = n; this._comboPulse = 1;
    if (this.comboEl) { this.comboEl.textContent = '×' + n; this.comboEl.classList.remove('pop'); void this.comboEl.offsetWidth; this.comboEl.classList.add('pop'); }
    // little celebratory spark burst at the current head position
    if (this.ps && this._head) this.ps.burst(this._head.x, this._head.y, 14, { speed: 4, life: 0.7, size: 3, color: this.pal.ember, kind: 'spark', jitter: true });
  }

  destroy() {
    this._alive = false;
    cancelAnimationFrame(this._raf);
    window.removeEventListener('resize', this._onResize);
    if (this.layer && this.layer.parentNode) this.layer.parentNode.removeChild(this.layer);
    this.ps && this.ps.clear();
    this.layer = this.canvas = this.ctx = this.ps = null;
  }

  // ---------- DOM scaffold (canvas + glassmorphism banner + combo + title) ----------
  _buildDom() {
    const L = document.createElement('div');
    L.className = 'gd-overlay';
    L.innerHTML =
      '<div class="gd-dim"></div>' +
      '<canvas class="gd-canvas"></canvas>' +
      '<div class="gd-banner"><div class="gd-ava"></div><div class="gd-meta">' +
        '<div class="gd-name"></div><div class="gd-sub">sent <b>' + (this.config.name || 'Golden Dragon') + '</b></div>' +
      '</div><div class="gd-combo">×' + this._combo + '</div></div>' +
      '<div class="gd-title"><div class="gd-title-main">' + (this.config.name || 'GOLDEN DRAGON').toUpperCase() + '</div>' +
        '<div class="gd-title-sub"></div><div class="gd-title-qty"></div></div>';
    this.layer = L;
    this.root.appendChild(L);
    this.canvas = L.querySelector('.gd-canvas');
    this.ctx = this.canvas.getContext('2d');
    // vector head element rides on the canvas body's head point
    this.headEl = document.createElement('div');
    this.headEl.className = 'gd-head';
    this.headEl.innerHTML = dragonHeadSVG(this.pal);
    this.canvas.after(this.headEl);
    // front-facing head, shown only during the hero head-turn
    this.headFrontEl = document.createElement('div');
    this.headFrontEl.className = 'gd-head gd-head-front';
    this.headFrontEl.style.opacity = '0';
    this.headFrontEl.innerHTML = dragonHeadFrontSVG(this.pal);
    this.headEl.after(this.headFrontEl);
    this.bannerEl = L.querySelector('.gd-banner');
    this.comboEl = L.querySelector('.gd-combo');
    this.titleEl = L.querySelector('.gd-title');
    L.querySelector('.gd-name').textContent = this.sender.name;
    L.querySelector('.gd-title-sub').textContent = 'Sent by ' + this.sender.name;
    const ava = L.querySelector('.gd-ava');
    if (this.sender.avatar) ava.style.backgroundImage = 'url("' + this.sender.avatar + '")';
    else ava.textContent = (this.sender.name[0] || '?').toUpperCase();
  }

  _resize() {
    const r = this.root.getBoundingClientRect();
    this.W = r.width || 390; this.H = r.height || 844;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    this.canvas.width = Math.round(this.W * dpr);
    this.canvas.height = Math.round(this.H * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.R = Math.min(this.W, this.H) * 0.05; // base body radius
    // size the vector head relative to the body
    this.headK = (this.R * HEAD_SCALE) / HEAD_VB.h;
    if (this.headEl) {
      this.headEl.style.width = (HEAD_VB.w * this.headK) + 'px';
      this.headEl.style.height = (HEAD_VB.h * this.headK) + 'px';
      this.headEl.style.transformOrigin = (HEAD_VB.anchor.x * this.headK) + 'px ' + (HEAD_VB.anchor.y * this.headK) + 'px';
    }
    this.headKF = (this.R * FRONT_SCALE) / FRONT_VB.h;
    if (this.headFrontEl) {
      this.headFrontEl.style.width = (FRONT_VB.w * this.headKF) + 'px';
      this.headFrontEl.style.height = (FRONT_VB.h * this.headKF) + 'px';
      this.headFrontEl.style.transformOrigin = (FRONT_VB.anchor.x * this.headKF) + 'px ' + (FRONT_VB.anchor.y * this.headKF) + 'px';
    }
  }

  // Place the vector head on the canvas head point, upright and facing travel.
  // At the hero beat the dragon TURNS to face the viewer: the profile head cross-fades
  // to a front-facing head (scaled up), then fades back out as it rises away.
  _placeHead(tf) {
    if (!this.headEl || !this._head) return;
    if (tf < 0.03) { this.headEl.style.opacity = '0'; this.headFrontEl.style.opacity = '0'; return; }
    // front-facing visibility: fade in ~0.60–0.66, hold, fade out on exit
    const inT = clamp((tf - 0.60) / 0.06, 0, 1);
    const outT = tf > 0.90 ? clamp((tf - 0.90) / 0.05, 0, 1) : 0;
    const frontVis = (tf >= 0.60 && tf <= 0.95) ? inT * (1 - outT) : 0;

    const k = this.headK, ax = HEAD_VB.anchor.x * k, ay = HEAD_VB.anchor.y * k;
    const dir = Math.cos(this._angle) < 0 ? -1 : 1;
    const pitch = clamp(Math.atan2(Math.sin(this._angle), Math.abs(Math.cos(this._angle))), -0.5, 0.5);
    const baseOpacity = tf > 0.94 ? clamp((1 - tf) / 0.06, 0, 1) : 1;
    this.headEl.style.opacity = String(baseOpacity * (1 - frontVis));
    this.headEl.style.left = (this._head.x - ax) + 'px';
    this.headEl.style.top = (this._head.y - ay) + 'px';
    this.headEl.style.transform = 'rotate(' + (pitch * dir) + 'rad) scaleX(' + dir + ')';
    this.headEl.classList.toggle('hero', this._inPhase(tf, 'hero') || this._inPhase(tf, 'finale'));

    if (frontVis > 0.001) {
      const kf = this.headKF, axf = FRONT_VB.anchor.x * kf, ayf = FRONT_VB.anchor.y * kf;
      const grow = 0.88 + 0.12 * inT + 0.04 * Math.sin(tf * this.duration / 1000 * 3);
      this.headFrontEl.style.opacity = String(frontVis);
      this.headFrontEl.style.left = (this._head.x - axf) + 'px';
      this.headFrontEl.style.top = (this._head.y - ayf) + 'px';
      this.headFrontEl.style.transform = 'scale(' + grow + ')';
      this.headFrontEl.classList.add('hero');
    } else {
      this.headFrontEl.style.opacity = '0';
    }
  }

  // Head position at normalised timeline `tf` (0..1), in pixels.
  _pathAt(tf) {
    tf = clamp(tf, 0, 1);
    let leg = LEGS[0];
    for (const l of LEGS) { if (tf >= l[0] && tf <= l[1]) { leg = l; break; } if (tf > l[1]) leg = l; }
    const u = smooth(clamp((tf - leg[0]) / (leg[1] - leg[0] || 1), 0, 1));
    const i = leg[2];
    const p0 = WP[Math.max(0, i - 1)], p1 = WP[i], p2 = WP[Math.min(WP.length - 1, i + 1)], p3 = WP[Math.min(WP.length - 1, i + 2)];
    const p = catmull(p0, p1, p2, p3, u);
    return { x: p.x * this.W, y: p.y * this.H };
  }

  _loop(ts) {
    if (!this._alive) return;
    if (this._t0 == null) this._t0 = ts;
    const dt = Math.min(48, ts - (this._last || ts)); this._last = ts;
    const elapsed = ts - this._t0;
    const tf = elapsed / this.duration;
    this._update(tf, dt);
    this._draw(tf);
    if (tf >= 1) { this.destroy(); this.onDone(); return; }
    this._raf = requestAnimationFrame((t) => this._loop(t));
  }

  _inPhase(tf, name) { const p = PHASE[name]; return tf >= p[0] && tf <= p[1]; }

  _update(tf, dt) {
    // reveal DOM cues on schedule
    if (tf >= 0.24 && this.bannerEl && !this.bannerEl.classList.contains('in')) this.bannerEl.classList.add('in');
    if (this._inPhase(tf, 'finale') && this.titleEl && !this.titleEl.classList.contains('in')) {
      this.titleEl.classList.add('in');
      this.layer.querySelector('.gd-title-qty').textContent = '🐉 ×' + this._combo;
    }
    if (tf > 0.9) { this.bannerEl && this.bannerEl.classList.add('out'); }
    if (tf > 0.94 && this.titleEl) this.titleEl.classList.add('out');

    // head + heading
    this._head = this._pathAt(tf);
    const ahead = this._pathAt(tf + 0.006);
    this._angle = Math.atan2(ahead.y - this._head.y, ahead.x - this._head.x);

    // ambient gold motes rising from bottom-left / bottom-center
    const spawnRate = this._inPhase(tf, 'circle') ? 3 : (tf < 0.9 ? 1.5 : 0);
    for (let k = 0; k < spawnRate; k++) {
      if (Math.random() > dt / 22) continue;
      const fromLeft = Math.random() < 0.6;
      this.ps.spawn({
        x: (fromLeft ? 0.05 + Math.random() * 0.35 : 0.35 + Math.random() * 0.4) * this.W,
        y: this.H * (0.9 + Math.random() * 0.15),
        vx: (Math.random() - 0.5) * 0.5, vy: -(0.6 + Math.random() * 1.4),
        g: -0.004, drag: 0.995, life: 1.6 + Math.random() * 1.4,
        size: 1.5 + Math.random() * 3, color: this.pal.ember, kind: 'glow',
      });
    }

    // gold sparks trailing the body
    if (tf > 0.14 && tf < 0.92 && Math.random() < 0.7) {
      const tail = this._pathAt(tf - 0.05 - Math.random() * 0.05);
      this.ps.spawn({ x: tail.x, y: tail.y, vx: (Math.random() - 0.5) * 1.2, vy: (Math.random() - 0.5) * 1.2 - 0.2,
        g: 0.006, drag: 0.96, life: 0.5 + Math.random() * 0.5, size: 1 + Math.random() * 2,
        color: this.pal.ember, kind: 'spark' });
    }

    // hero moment — particles converge toward the head (energy gather)
    if (this._inPhase(tf, 'hero')) {
      for (let k = 0; k < 2; k++) {
        const a = Math.random() * Math.PI * 2, rad = 60 + Math.random() * 90;
        this.ps.spawn({ x: this._head.x + Math.cos(a) * rad, y: this._head.y + Math.sin(a) * rad,
          vx: -Math.cos(a) * 2.4, vy: -Math.sin(a) * 2.4, drag: 0.98, life: 0.6, size: 2 + Math.random() * 2,
          color: this.pal.illum, kind: 'spark' });
      }
    }
    // finale burst — one big radial shower behind the rising dragon
    if (tf >= PHASE.finale[0] && !this._burst) {
      this._burst = true;
      this.ps.burst(this._head.x, this._head.y, this.q.sparks * 3, { speed: 7, lift: 1, life: 1.3, size: 3, color: this.pal.ember, kind: 'spark', jitter: true, g: 0.03 });
      for (let k = 0; k < this.q.sparks; k++) this.ps.spawn({ x: this._head.x, y: this._head.y,
        vx: (Math.random() - 0.5) * 8, vy: -(2 + Math.random() * 7), g: 0.05, drag: 0.98,
        life: 1 + Math.random(), size: 2 + Math.random() * 2, color: '#fff', kind: 'star', spin: 0.2 });
    }

    this.ps.update(dt);
    if (this._comboPulse > 0) this._comboPulse = Math.max(0, this._comboPulse - dt / 300);
  }

  // ---------- drawing ----------
  _draw(tf) {
    const ctx = this.ctx; ctx.clearRect(0, 0, this.W, this.H);

    // subtle dimming (kept low so the streamer stays visible)
    const dim = this._inPhase(tf, 'atmos') ? smooth(clamp(tf / 0.12, 0, 1)) * 0.10
      : (tf > 0.9 ? 0.10 * (1 - clamp((tf - 0.9) / 0.1, 0, 1)) : 0.10);
    if (dim > 0.001) { ctx.fillStyle = `rgba(0,0,0,${dim.toFixed(3)})`; ctx.fillRect(0, 0, this.W, this.H); }

    // radial golden illumination during the circle / hero framing
    if (tf > PHASE.circle[0] && tf < PHASE.exit[0]) {
      const cx = this.W * 0.5, cy = this.H * 0.42, rad = Math.min(this.W, this.H) * 0.7;
      const g = ctx.createRadialGradient(cx, cy, 0, cx, cy, rad);
      const a = 0.16 * smooth(clamp((tf - PHASE.circle[0]) / 0.12, 0, 1));
      g.addColorStop(0, `rgba(255,180,60,${a})`); g.addColorStop(1, 'rgba(255,180,60,0)');
      ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = g; ctx.fillRect(0, 0, this.W, this.H); ctx.restore();
    }

    // trail ribbon (soft, fading) — sampled just behind the head
    this._drawTrail(ctx, tf);

    // the dragon
    if (tf > 0.02) this._drawDragon(ctx, tf);

    // particles on top (additive)
    this.ps.draw(ctx);

    // position the vector head element over the canvas body
    this._placeHead(tf);
  }

  _drawTrail(ctx, tf) {
    const N = this.q.trail; if (N < 2) return;
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round';
    for (let i = 0; i < N; i++) {
      const a = this._pathAt(tf - 0.03 - i * 0.012);
      const b = this._pathAt(tf - 0.03 - (i + 1) * 0.012);
      const alpha = (1 - i / N) * 0.5;
      ctx.strokeStyle = `rgba(255,200,90,${alpha.toFixed(3)})`;
      ctx.lineWidth = this.R * 0.5 * (1 - i / N) + 1;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
    }
    ctx.restore();
  }

  _drawDragon(ctx, tf) {
    const N = this.q.segments;
    const LAG = 0.15 / N; // total tail spans ~0.15 of the timeline behind the head
    const ripple = (tf * this.duration) / 1000 * 5.5;
    const base = [], rad = [];
    for (let i = 0; i < N; i++) {
      base.push(this._pathAt(tf - i * LAG));
      const f = i / (N - 1);
      // radius: thick neck, gentle belly bulge, tapering tail
      rad.push(this.R * (0.30 + 0.70 * Math.pow(1 - f, 0.62)) * (1 + 0.18 * Math.sin(f * Math.PI)));
    }
    const bnrm = base.map((p, i) => {
      const a = base[Math.max(0, i - 1)], b = base[Math.min(base.length - 1, i + 1)];
      const dx = b.x - a.x, dy = b.y - a.y, l = Math.hypot(dx, dy) || 1; return { x: -dy / l, y: dx / l };
    });
    // secondary undulation so the body flexes like a swimming serpent (whips more at the tail)
    const pts = base.map((p, i) => {
      const f = i / (N - 1), amp = this.R * 0.5 * (0.15 + 0.85 * f), off = amp * Math.sin(i * 0.55 - ripple);
      return { x: p.x + bnrm[i].x * off, y: p.y + bnrm[i].y * off };
    });
    const nrm = pts.map((p, i) => {
      const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
      const dx = b.x - a.x, dy = b.y - a.y, l = Math.hypot(dx, dy) || 1; return { x: -dy / l, y: dx / l };
    });

    // soft golden aura / halo behind the whole body
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    ctx.strokeStyle = 'rgba(255,180,60,0.09)'; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < N; i++) ctx.lineTo(pts[i].x, pts[i].y);
    ctx.lineWidth = this.R * 2.8; ctx.stroke(); ctx.restore();

    // body ribbon path (reused for fill + rim)
    const ribbon = () => {
      ctx.beginPath();
      ctx.moveTo(pts[0].x + nrm[0].x * rad[0], pts[0].y + nrm[0].y * rad[0]);
      for (let i = 1; i < N; i++) ctx.lineTo(pts[i].x + nrm[i].x * rad[i], pts[i].y + nrm[i].y * rad[i]);
      for (let i = N - 1; i >= 0; i--) ctx.lineTo(pts[i].x - nrm[i].x * rad[i], pts[i].y - nrm[i].y * rad[i]);
      ctx.closePath();
    };
    ribbon();
    // metallic cross-section gradient: bright highlight band near the top, shadow below
    const grad = ctx.createLinearGradient(pts[0].x, pts[0].y - this.R, pts[0].x, pts[0].y + this.R);
    grad.addColorStop(0, this.pal.hi); grad.addColorStop(0.22, this.pal.lite); grad.addColorStop(0.44, this.pal.lite);
    grad.addColorStop(0.62, this.pal.mid); grad.addColorStop(0.78, this.pal.dark); grad.addColorStop(0.9, this.pal.mid); grad.addColorStop(1, this.pal.dark);
    ctx.save();
    ctx.shadowColor = this.pal.edge; ctx.shadowBlur = this.q.blur ? 20 : 0;
    ctx.fillStyle = grad; ctx.fill();
    ctx.restore();

    // tubular shading: top sheen + belly shadow make the body read as a round metallic tube
    this._shadeTube(ctx, pts, nrm, rad);

    // glowing rim
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.strokeStyle = this.pal.edge; ctx.lineWidth = 1.6;
    ribbon(); ctx.stroke(); ctx.restore();

    // dorsal ridge + scales + limbs
    this._drawRidge(ctx, pts, nrm, rad);
    this._drawScales(ctx, pts, nrm, rad);
    this._drawLimb(ctx, pts, nrm, rad, Math.floor(N * 0.24), tf);
    this._drawLimb(ctx, pts, nrm, rad, Math.floor(N * 0.52), tf, true);

    // the flaming pearl the dragon chases (classic motif; folds into the finale burst)
    if (tf < PHASE.finale[0]) this._drawPearl(ctx, pts[0], this._angle, rad[0], tf);

    // neck glow so the vector head blends into the body
    const hg = ctx.createRadialGradient(pts[0].x, pts[0].y, 0, pts[0].x, pts[0].y, rad[0] * 2.4);
    hg.addColorStop(0, 'rgba(255,200,90,0.5)'); hg.addColorStop(1, 'rgba(255,200,90,0)');
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.fillStyle = hg;
    ctx.beginPath(); ctx.arc(pts[0].x, pts[0].y, rad[0] * 2.4, 0, Math.PI * 2); ctx.fill(); ctx.restore();
    // (the ornate head itself is a vector element, positioned in _placeHead)
  }

  _shadeTube(ctx, pts, nrm, rad) {
    // top highlight sheen
    ctx.save(); ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    ctx.strokeStyle = 'rgba(255,246,200,0.42)';
    ctx.beginPath();
    for (let i = 0; i < pts.length; i++) { const x = pts[i].x + nrm[i].x * rad[i] * 0.42, y = pts[i].y + nrm[i].y * rad[i] * 0.42; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.lineWidth = this.R * 0.4; ctx.stroke(); ctx.restore();
    // belly shadow
    ctx.save(); ctx.lineCap = 'round'; ctx.lineJoin = 'round'; ctx.strokeStyle = 'rgba(50,32,3,0.45)';
    ctx.beginPath();
    for (let i = 0; i < pts.length; i++) { const x = pts[i].x - nrm[i].x * rad[i] * 0.52, y = pts[i].y - nrm[i].y * rad[i] * 0.52; i ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }
    ctx.lineWidth = this.R * 0.5; ctx.stroke(); ctx.restore();
  }

  _drawPearl(ctx, head, angle, r, tf) {
    const dist = r * 3.4, px = head.x + Math.cos(angle) * dist, py = head.y + Math.sin(angle) * dist;
    const pulse = 1 + 0.14 * Math.sin((tf * this.duration) / 1000 * 6);
    const pr = r * 0.8 * pulse;
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    const g = ctx.createRadialGradient(px, py, 0, px, py, pr * 2.4);
    g.addColorStop(0, 'rgba(255,255,255,0.95)'); g.addColorStop(0.28, 'rgba(255,226,150,0.85)');
    g.addColorStop(0.6, 'rgba(255,170,60,0.4)'); g.addColorStop(1, 'rgba(255,170,60,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(px, py, pr * 2.4, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fff8e0'; ctx.beginPath(); ctx.arc(px, py, pr * 0.5, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  _drawRidge(ctx, pts, nrm, rad) {
    ctx.save(); ctx.fillStyle = this.pal.illum;
    for (let i = 2; i < pts.length - 2; i += 2) {
      const spike = rad[i] * 0.75, s = i / pts.length;
      const bx = pts[i].x + nrm[i].x * rad[i], by = pts[i].y + nrm[i].y * rad[i];
      ctx.globalAlpha = 0.55 * (1 - s);
      ctx.beginPath();
      ctx.moveTo(bx, by);
      ctx.lineTo(bx + nrm[i].x * spike - (pts[i + 1].x - pts[i].x) * 0.4, by + nrm[i].y * spike - (pts[i + 1].y - pts[i].y) * 0.4);
      ctx.lineTo(pts[i + 1].x + nrm[i + 1].x * rad[i + 1], pts[i + 1].y + nrm[i + 1].y * rad[i + 1]);
      ctx.closePath(); ctx.fill();
    }
    ctx.restore();
  }

  _drawScales(ctx, pts, nrm, rad) {
    // Realistic reptile scaling: the body surface is tiled with individual overlapping
    // scales in brick-offset rows. Each scale gets cross-section shading (bright on the
    // top of the tube, dark toward the flanks/belly), a bright exposed lip and a dark
    // overlap groove — so the whole body reads as scale-by-scale metallic hide.
    ctx.save();
    const along = this.q.blur ? 1 : 2;      // row spacing along the body (density)
    for (let i = 5; i < pts.length - 2; i += along) {
      const ang = this._angleAt(pts, i);
      const r = rad[i];
      if (r < 4) continue;
      const across = Math.max(2, Math.round(r / 3.8));   // scales per side (finer)
      const brick = (Math.floor(i / along) % 2) ? 0.5 : 0;
      for (let j = -across; j <= across; j++) {
        const u = (j + brick) / (across + 0.4);          // -1..1 across the width
        if (Math.abs(u) > 1) continue;
        const cx = pts[i].x + nrm[i].x * u * r * 0.94;
        const cy = pts[i].y + nrm[i].y * u * r * 0.94;
        const sr = (r / (across + 0.4)) * 1.18;          // scale radius ≈ spacing
        const b = 1 - Math.min(1, Math.abs(u));          // 1 on top of tube, 0 at flank
        // scale body — light overlay only where the tube faces the light, dark on flanks;
        // low opacity so the metallic gradient beneath keeps the cylindrical shading
        if (b > 0.35) {
          ctx.fillStyle = `rgba(255,244,196,${(0.06 + 0.16 * b).toFixed(2)})`;
          ctx.beginPath();
          ctx.arc(cx, cy, sr * 0.78, ang - 2.2, ang - 0.9);
          ctx.arc(cx, cy, sr * 0.42, ang - 0.9, ang - 2.2, true);
          ctx.closePath(); ctx.fill();
        } else {
          ctx.fillStyle = `rgba(40,26,2,${(0.28 * (1 - b)).toFixed(2)})`;
          ctx.beginPath(); ctx.arc(cx, cy, sr * 0.7, ang - 2.2, ang - 0.9);
          ctx.arc(cx, cy, sr * 0.4, ang - 0.9, ang - 2.2, true); ctx.closePath(); ctx.fill();
        }
        // dark overlap groove (defines each scale edge)
        ctx.strokeStyle = 'rgba(40,25,2,0.6)'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(cx, cy, sr, ang - 2.5, ang - 0.6); ctx.stroke();
        // bright exposed lip (only meaningful on the lit top of the tube)
        if (b > 0.25) {
          ctx.strokeStyle = `rgba(255,250,220,${(0.55 * b).toFixed(2)})`; ctx.lineWidth = 1.1;
          ctx.beginPath(); ctx.arc(cx, cy, sr * 0.86, ang - 2.1, ang - 1.0); ctx.stroke();
        }
      }
    }
    ctx.restore();
  }

  _angleAt(pts, i) {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    return Math.atan2(b.y - a.y, b.x - a.x);
  }

  _drawLimb(ctx, pts, nrm, rad, i, tf, back) {
    if (i < 1 || i >= pts.length) return;
    const p = pts[i], n = nrm[i], side = back ? -1 : 1;
    const baseX = p.x + n.x * rad[i] * side, baseY = p.y + n.y * rad[i] * side;
    const swing = Math.sin(tf * 40 + (back ? 1.5 : 0)) * 0.3;
    const dir = this._angleAt(pts, i) + side * (1.1 + swing);
    const len = rad[i] * 2.4;
    const kx = baseX + Math.cos(dir) * len * 0.6, ky = baseY + Math.sin(dir) * len * 0.6;
    const fx = kx + Math.cos(dir + 0.5) * len * 0.5, fy = ky + Math.sin(dir + 0.5) * len * 0.5;
    ctx.save();
    ctx.strokeStyle = this.pal.mid; ctx.lineWidth = rad[i] * 0.7; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(baseX, baseY); ctx.lineTo(kx, ky); ctx.lineTo(fx, fy); ctx.stroke();
    // three claws
    ctx.strokeStyle = this.pal.hi; ctx.lineWidth = 1.4;
    for (let c = -1; c <= 1; c++) {
      ctx.beginPath(); ctx.moveTo(fx, fy);
      ctx.lineTo(fx + Math.cos(dir + c * 0.4) * 7, fy + Math.sin(dir + c * 0.4) * 7); ctx.stroke();
    }
    ctx.restore();
  }

  // (The ornate head is a hand-authored vector element — see assets/dragonHead.js
  //  and _placeHead — so it always reads as deliberate art and stays upright.)
}
