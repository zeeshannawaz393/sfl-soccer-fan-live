// GiftAnimationManager — the single entry point between gift events and the
// visual layer. Responsibilities:
//   • Route a GIFT_SENT event to the right renderer (small vs premium fullscreen).
//   • Guarantee only ONE fullscreen premium gift plays at a time (a queue).
//   • Fold rapid identical gifts from the same sender into a live combo instead of
//     replaying the whole animation.
//
// Renderers are looked up by config.renderer, so adding a new premium gift is a
// matter of registering a renderer + a gift config — no manager changes.

import { giftByEventId } from '../config/gifts.js';
import { ComboManager } from './ComboManager.js';
import { GoldenDragonGift } from '../renderers/GoldenDragonGift.js';
import { SmallGiftRenderer } from '../renderers/SmallGiftRenderer.js';

export class GiftAnimationManager {
  constructor({ root, quality = 'high', now = () => performance.now() }) {
    this.root = root;
    this.quality = quality;
    this.now = now;
    this.queue = [];
    this.current = null;         // { renderer, config, evt }
    this.combo = new ComboManager();
    this.small = new SmallGiftRenderer({ root });
    // renderer registry (premium/fullscreen)
    this.renderers = { 'golden-dragon': GoldenDragonGift };
  }

  setQuality(q) { this.quality = q; }

  // Public API used by the event system.
  onGiftEvent(evt) {
    const config = giftByEventId(evt.giftId);
    if (!config) { console.warn('Unknown gift', evt.giftId); return; }

    if (!config.fullscreen) { this.small.play(config, evt); return; }

    // Combo fold: identical premium gift already on screen within its window.
    if (config.comboEnabled && this.current &&
        this.current.config.id === config.id &&
        this.current.evt.senderId === evt.senderId &&
        this.combo.isOpen(evt, this.now())) {
      const total = this.combo.bump(evt, config.comboWindow || 3000, this.now());
      this.current.renderer.setCombo(total);
      return;
    }

    this.combo.bump(evt, config.comboWindow || 3000, this.now());
    this._enqueue(config, evt);
  }

  // Convenience: playGift({ giftId, senderName, ... })
  playGift(opts) {
    this.onGiftEvent({
      type: 'GIFT_SENT', senderId: opts.senderId || 'USER_LOCAL',
      senderName: opts.senderName || 'You', senderAvatar: opts.senderAvatar || '',
      giftId: opts.giftId, giftName: opts.giftName || '', quantity: opts.quantity || 1,
      timestamp: this.now(),
    });
  }

  _enqueue(config, evt) {
    this.queue.push({ config, evt });
    // higher priority first
    this.queue.sort((a, b) => (b.config.priority || 0) - (a.config.priority || 0));
    if (!this.current) this._next();
  }

  _next() {
    const item = this.queue.shift();
    if (!item) { this.current = null; return; }
    const RendererClass = this.renderers[item.config.renderer];
    if (!RendererClass) { console.warn('No renderer for', item.config.renderer); this._next(); return; }
    const renderer = new RendererClass({
      root: this.root, quality: this.quality, config: item.config,
      onDone: () => { this.combo.close(item.evt); this.current = null; this._next(); },
    });
    this.current = { renderer, config: item.config, evt: item.evt };
    renderer.play(item.evt);
  }

  reset() {
    this.queue.length = 0;
    if (this.current && this.current.renderer.destroy) this.current.renderer.destroy();
    this.current = null;
    this.combo.clear();
    // clear any lingering small-gift layers
    this.root.querySelectorAll('.sg-layer, .gd-overlay').forEach((n) => n.remove());
  }

  destroy() { this.reset(); }
}
