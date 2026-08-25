// A convincing-but-lightweight simulated live room. It exists only so the Golden
// Dragon overlay can be judged over a real live-stream layout. The gift overlay is
// appended ABOVE this UI and never replaces it.

const NAMES = ['maria_10', 'kojo', 'sara.b', 'jjfan', 'olivia', 'the_ref', 'nadia', 'omar_7'];
const LINES = ['this stream is 🔥', 'GOAL!!', 'let\'s go reds', 'who\'s winning', 'send the dragon 👀',
  'hi from Lagos', 'best host fr', 'wave to us 👋', 'that save omg', '❤️❤️❤️'];

export class LiveRoom {
  constructor(root) { this.root = root; this._timers = []; }

  mount() {
    this.root.classList.add('live-room');
    this.root.innerHTML = `
      <div class="lr-video"></div>
      <div class="lr-scrim"></div>
      <div class="lr-top">
        <div class="lr-host"><div class="lr-host-av"></div>
          <div><div class="lr-host-name">Golden Arena · Live</div><div class="lr-host-tag">@golden_host</div></div>
          <div class="lr-follow">Follow</div>
        </div>
        <div class="lr-count">👁 <b>4.1K</b></div>
      </div>
      <div class="lr-live"><i></i>LIVE</div>
      <div class="lr-hearts"></div>
      <div class="lr-comments"></div>
      <div class="lr-bar">
        <div class="lr-gift">🎁</div>
        <div class="lr-input">Say something…</div>
        <div class="lr-heart">❤️</div>
      </div>
      <div class="lr-gifts-fx"></div>`;
    this.commentsEl = this.root.querySelector('.lr-comments');
    this.heartsEl = this.root.querySelector('.lr-hearts');
    // fx layer sits above the live UI — the gift manager renders into it
    this.fxLayer = this.root.querySelector('.lr-gifts-fx');

    this._timers.push(setInterval(() => this._comment(), 1600));
    this._timers.push(setInterval(() => this._heart(), 900));
    for (let i = 0; i < 4; i++) this._comment();
    return this;
  }

  _comment() {
    const d = document.createElement('div');
    d.className = 'lr-cm';
    d.innerHTML = `<b>${NAMES[(Math.random() * NAMES.length) | 0]}</b> ${LINES[(Math.random() * LINES.length) | 0]}`;
    this.commentsEl.appendChild(d);
    while (this.commentsEl.children.length > 6) this.commentsEl.removeChild(this.commentsEl.firstChild);
  }

  _heart() {
    const h = document.createElement('div');
    h.className = 'lr-fly-heart';
    h.textContent = ['❤️', '💛', '🧡', '💚'][(Math.random() * 4) | 0];
    h.style.right = (10 + Math.random() * 30) + 'px';
    h.style.setProperty('--x', (Math.random() * 40 - 20) + 'px');
    this.heartsEl.appendChild(h);
    setTimeout(() => h.remove(), 2600);
  }

  destroy() { this._timers.forEach(clearInterval); this._timers = []; }
}
