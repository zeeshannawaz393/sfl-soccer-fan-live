// Gift catalogue + quality configuration.
// Shape mirrors a production gift record so the prototype renderer can later be
// swapped for a Lottie / SVGA / alpha-video asset WITHOUT touching the manager.

export const GIFTS = {
  ROSE: {
    id: 'rose',
    name: 'Rose',
    price: 10,
    animationType: 'custom',   // custom | lottie | svga | alpha-video | webm
    renderer: 'small',         // which renderer class handles it
    duration: 2200,
    fullscreen: false,
    priority: 5,
    comboEnabled: true,
    glyph: '🌹',
  },
  GOLDEN_DRAGON: {
    id: 'golden_dragon',
    name: 'Golden Dragon',
    price: 5000,
    animationType: 'custom',
    // In production this becomes: animationType:'alpha-video',
    // animationUrl:'https://cdn.example.com/gifts/golden-dragon.mp4'
    renderer: 'golden-dragon',
    duration: 8000,
    fullscreen: true,
    priority: 100,
    comboEnabled: true,
    comboWindow: 3000,
    glyph: '🐉',
  },
  DRAGON: {
    id: 'dragon',
    name: 'Dragon',
    price: 3000,
    animationType: 'custom',
    renderer: 'golden-dragon', // reuse renderer with a cooler palette variant
    variant: 'jade',
    duration: 8000,
    fullscreen: true,
    priority: 80,
    comboEnabled: true,
    comboWindow: 3000,
    glyph: '🐲',
  },
};

// Look a gift up by the id sent on a GIFT_SENT event (case-insensitive).
export function giftByEventId(giftId) {
  const key = String(giftId || '').toUpperCase();
  return GIFTS[key] || GIFTS[key.replace(/-/g, '_')] || null;
}

// Performance tiers. `auto` picks based on device hints; callers may force one.
export const QUALITY = {
  high:   { particles: 40, trail: 26, sparks: 18, blur: true,  segments: 52 },
  medium: { particles: 25, trail: 16, sparks: 10, blur: false, segments: 40 },
  low:    { particles: 12, trail: 8,  sparks: 4,  blur: false, segments: 28 },
};

export function detectQuality() {
  const mem = navigator.deviceMemory || 4;
  const cores = navigator.hardwareConcurrency || 4;
  const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  if (reduce || mem <= 2 || cores <= 2) return 'low';
  if (mem <= 4 || cores <= 4) return 'medium';
  return 'high';
}
