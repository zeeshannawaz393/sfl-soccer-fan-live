// Bootstraps the demo: builds the live room, wires the mock gift socket to the
// GiftAnimationManager, and hooks up the temporary development controls.

import { LiveRoom } from './liveroom/LiveRoom.js';
import { GiftAnimationManager } from './core/GiftAnimationManager.js';
import { EventBus, MockGiftSocket } from './core/EventBus.js';
import { detectQuality } from './config/gifts.js';

const phone = document.getElementById('phone');
const room = new LiveRoom(phone).mount();

let quality = detectQuality();
const bus = new EventBus();
const socket = new MockGiftSocket(bus, 'ROOM_101');

// The manager renders into the live room's fx layer (above the UI, below nothing).
const manager = new GiftAnimationManager({ root: room.fxLayer, quality });

// Incoming real-time events -> manager. In production this is a WebSocket handler.
bus.on('GIFT_SENT', (evt) => manager.onGiftEvent(evt));

const SENDER = { senderName: 'Zeeshan', senderAvatar: 'https://placehold.co/100x100', senderId: 'USER_22' };
const send = (giftId, giftName, quantity = 1) =>
  socket.send({ ...SENDER, giftId, giftName, quantity, coins: 5000 }, performance.now());

// ---- development controls ----
document.getElementById('btn-rose').onclick = () => send('ROSE', 'Rose', 1);
document.getElementById('btn-dragon').onclick = () => send('GOLDEN_DRAGON', 'Golden Dragon', 1);
document.getElementById('btn-dragon5').onclick = () => send('GOLDEN_DRAGON', 'Golden Dragon', 5);
document.getElementById('btn-multi').onclick = () => {
  // stagger a mixed burst to exercise the queue + combo folding
  const seq = [['ROSE', 'Rose'], ['GOLDEN_DRAGON', 'Golden Dragon'], ['DRAGON', 'Dragon'],
    ['GOLDEN_DRAGON', 'Golden Dragon'], ['ROSE', 'Rose']];
  seq.forEach(([id, name], i) => setTimeout(() => send(id, name, 1), i * 700));
};
document.getElementById('btn-reset').onclick = () => manager.reset();

const qSel = document.getElementById('quality');
qSel.value = quality;
qSel.onchange = () => { quality = qSel.value; manager.setQuality(quality); };

// expose for manual poking from the console / automated checks
window.__giftDemo = { manager, socket, bus, send, room };
