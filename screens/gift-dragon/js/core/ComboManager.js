// Tracks combo state per (sender + gift) within a rolling window.
// While a premium gift is on screen and identical gifts keep arriving, we
// increment the visible counter instead of replaying the whole animation.

export class ComboManager {
  constructor() { this._active = new Map(); }

  static key(evt) { return `${evt.senderId}:${evt.giftId}`; }

  // Returns the running quantity for this combo key, opening a window if needed.
  bump(evt, windowMs, now) {
    const key = ComboManager.key(evt);
    const prev = this._active.get(key);
    const qty = (prev && now - prev.last <= windowMs) ? prev.count + (evt.quantity || 1) : (evt.quantity || 1);
    this._active.set(key, { count: qty, last: now, windowMs });
    return qty;
  }

  isOpen(evt, now) {
    const p = this._active.get(ComboManager.key(evt));
    return !!(p && now - p.last <= p.windowMs);
  }

  close(evt) { this._active.delete(ComboManager.key(evt)); }
  clear() { this._active.clear(); }
}
