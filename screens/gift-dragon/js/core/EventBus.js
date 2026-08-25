// Minimal event bus that stands in for a real-time gift socket (WebSocket / SSE).
// Swap `emit` for an actual socket message handler in production; subscribers stay the same.

export class EventBus {
  constructor() { this._handlers = new Map(); }

  on(type, fn) {
    if (!this._handlers.has(type)) this._handlers.set(type, new Set());
    this._handlers.get(type).add(fn);
    return () => this.off(type, fn);
  }

  off(type, fn) {
    const set = this._handlers.get(type);
    if (set) set.delete(fn);
  }

  emit(type, payload) {
    const set = this._handlers.get(type);
    if (set) set.forEach((fn) => { try { fn(payload); } catch (e) { console.error(e); } });
  }

  clear() { this._handlers.clear(); }
}

// A mock socket that shapes payloads exactly like the production GIFT_SENT event.
export class MockGiftSocket {
  constructor(bus, roomId = 'ROOM_101') { this.bus = bus; this.roomId = roomId; this._seq = 0; }

  // Simulate a viewer sending a gift. `now` is injected so the module has no hidden clock.
  send({ giftId, giftName, senderId = 'USER_22', senderName = 'Zeeshan', senderAvatar = '', quantity = 1, coins = 0 }, now) {
    const evt = {
      type: 'GIFT_SENT',
      roomId: this.roomId,
      seq: ++this._seq,
      senderId,
      senderName,
      senderAvatar,
      giftId,
      giftName,
      quantity,
      coins,
      timestamp: now,
    };
    this.bus.emit('GIFT_SENT', evt);
    return evt;
  }
}
