// SmallGiftRenderer — cheap, non-blocking gifts (e.g. Rose). These float up a
// few glyphs and a name chip; they may overlap the live UI and each other and do
// NOT enter the premium fullscreen queue.

export class SmallGiftRenderer {
  constructor({ root }) { this.root = root; }

  play(config, evt) {
    const layer = document.createElement('div');
    layer.className = 'sg-layer';
    const n = Math.min(10, 4 + (evt.quantity || 1));
    for (let i = 0; i < n; i++) {
      const g = document.createElement('div');
      g.className = 'sg-fly';
      g.textContent = config.glyph || '🎁';
      g.style.left = (14 + Math.random() * 40) + '%';
      g.style.fontSize = (22 + Math.random() * 18) + 'px';
      g.style.animationDelay = (i * 90) + 'ms';
      layer.appendChild(g);
    }
    const chip = document.createElement('div');
    chip.className = 'sg-chip';
    chip.innerHTML = '<b>' + evt.senderName + '</b> sent ' + (config.glyph || '') + ' ' + config.name +
      (evt.quantity > 1 ? ' ×' + evt.quantity : '');
    layer.appendChild(chip);
    this.root.appendChild(layer);
    setTimeout(() => { if (layer.parentNode) layer.parentNode.removeChild(layer); }, 2600);
  }
}
