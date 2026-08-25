// Reusable additive particle system (canvas 2D). Coordinates are in CSS pixels;
// the owning renderer handles canvas sizing / devicePixelRatio scaling.
// Kinds: 'glow' (soft orb), 'spark' (bright dot), 'star' (4-point glint), 'streak'.

export class ParticleSystem {
  constructor(cap = 240) { this.cap = cap; this.list = []; }

  get count() { return this.list.length; }

  spawn(p) {
    if (this.list.length >= this.cap) return;
    this.list.push({
      x: p.x, y: p.y,
      vx: p.vx || 0, vy: p.vy || 0,
      g: p.g || 0, drag: p.drag == null ? 0.99 : p.drag,
      life: p.life || 1, age: 0,
      size: p.size || 3, spin: p.spin || 0, rot: p.rot || 0,
      color: p.color || '#ffd76a', kind: p.kind || 'glow',
      fadeIn: p.fadeIn || 0.12,
    });
  }

  // Radial burst of `n` particles from (x,y).
  burst(x, y, n, opts = {}) {
    for (let i = 0; i < n; i++) {
      const a = (Math.PI * 2 * i) / n + (opts.jitter ? (Math.random() - 0.5) : 0);
      const sp = (opts.speed || 3) * (0.5 + Math.random());
      this.spawn({
        x, y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - (opts.lift || 0),
        g: opts.g || 0.02, drag: opts.drag || 0.965,
        life: (opts.life || 1) * (0.7 + Math.random() * 0.6),
        size: (opts.size || 3) * (0.6 + Math.random()),
        color: opts.color || '#ffd76a', kind: opts.kind || 'spark',
      });
    }
  }

  update(dt) {
    const f = dt / 16.67; // normalize to ~60fps steps
    for (let i = this.list.length - 1; i >= 0; i--) {
      const p = this.list[i];
      p.vy += p.g * f;
      p.vx *= Math.pow(p.drag, f);
      p.vy *= Math.pow(p.drag, f);
      p.x += p.vx * f;
      p.y += p.vy * f;
      p.rot += p.spin * f;
      p.age += dt / 1000;
      if (p.age >= p.life) this.list.splice(i, 1);
    }
  }

  draw(ctx) {
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    for (const p of this.list) {
      const t = p.age / p.life;
      let a = 1 - t;
      if (t < p.fadeIn) a = t / p.fadeIn; // ease in
      ctx.globalAlpha = Math.max(0, Math.min(1, a));
      if (p.kind === 'star') this._star(ctx, p);
      else if (p.kind === 'streak') this._streak(ctx, p);
      else this._orb(ctx, p, p.kind === 'spark');
    }
    ctx.restore();
  }

  _orb(ctx, p, tight) {
    const r = p.size * (tight ? 1 : 2.4);
    const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r);
    g.addColorStop(0, '#fff');
    g.addColorStop(0.35, p.color);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, Math.PI * 2); ctx.fill();
  }

  _star(ctx, p) {
    ctx.save();
    ctx.translate(p.x, p.y); ctx.rotate(p.rot);
    ctx.fillStyle = '#fff';
    const s = p.size * 2.4;
    ctx.beginPath();
    for (let i = 0; i < 8; i++) {
      const rr = i % 2 ? s * 0.32 : s;
      const ang = (Math.PI / 4) * i;
      ctx.lineTo(Math.cos(ang) * rr, Math.sin(ang) * rr);
    }
    ctx.closePath(); ctx.fill();
    ctx.restore();
  }

  _streak(ctx, p) {
    ctx.save();
    ctx.strokeStyle = p.color; ctx.lineWidth = p.size; ctx.lineCap = 'round';
    ctx.beginPath(); ctx.moveTo(p.x, p.y);
    ctx.lineTo(p.x - p.vx * 3, p.y - p.vy * 3); ctx.stroke();
    ctx.restore();
  }

  clear() { this.list.length = 0; }
}
