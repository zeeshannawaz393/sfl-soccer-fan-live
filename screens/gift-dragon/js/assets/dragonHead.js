// Hand-authored vector dragon heads (side profile + front-facing for the hero turn).
// Tuned visually in head-preview.html, then parameterised by palette here. Drawn as
// SVG so it reads as deliberate art; the renderer rides these on the canvas body's
// head point. Metallic gradients + specular highlights give the polished-gold look.
//
// Side head is authored in a 0..420 space shifted +20,+10 into a 0-based viewBox so
// _placeHead's (anchor × scale) math stays exact.

export const HEAD_VB = { w: 460, h: 330, anchor: { x: 88, y: 182 } };
export const FRONT_VB = { w: 300, h: 340, anchor: { x: 150, y: 145 } };

// Shared metallic gradient/definition block. The repeated mid→dark→mid stops create
// a specular "sheen band" that reads as polished metal rather than flat colour.
function defs(P) {
  return `
    <linearGradient id="dhG" x1="0.12" y1="0" x2="0.5" y2="1">
      <stop offset="0" stop-color="${P.hi}"/><stop offset="0.16" stop-color="${P.lite}"/><stop offset="0.38" stop-color="${P.lite}"/>
      <stop offset="0.57" stop-color="${P.mid}"/><stop offset="0.73" stop-color="${P.dark}"/><stop offset="0.87" stop-color="${P.mid}"/><stop offset="1" stop-color="${P.dark}"/>
    </linearGradient>
    <linearGradient id="dhJ" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="${P.hi}"/><stop offset="0.4" stop-color="${P.lite}"/><stop offset="0.8" stop-color="${P.mid}"/><stop offset="1" stop-color="${P.dark}"/>
    </linearGradient>
    <linearGradient id="dhH" x1="0" y1="1" x2="0.7" y2="0">
      <stop offset="0" stop-color="${P.dark}"/><stop offset="0.35" stop-color="${P.mid}"/><stop offset="0.55" stop-color="${P.lite}"/><stop offset="0.72" stop-color="${P.hi}"/><stop offset="1" stop-color="${P.lite}"/>
    </linearGradient>
    <linearGradient id="dhM" x1="1" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="#fff0a0"/><stop offset="0.35" stop-color="${P.lite}"/><stop offset="0.7" stop-color="${P.illum}"/><stop offset="1" stop-color="${P.illum}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="dhE" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="#ffffff"/><stop offset="0.4" stop-color="${P.eye}"/><stop offset="1" stop-color="${P.illum}" stop-opacity="0"/>
    </radialGradient>`;
}

export function dragonHeadSVG(pal) {
  const P = pal;
  return `
<svg viewBox="0 0 ${HEAD_VB.w} ${HEAD_VB.h}" width="100%" height="100%" style="overflow:visible" xmlns="http://www.w3.org/2000/svg">
  <defs>${defs(P)}</defs>
  <g transform="translate(20,10)">
    <!-- mane -->
    <g fill="url(#dhM)">
      <path d="M120,108 C64,84 30,96 2,80 C34,112 36,132 118,140 Z"/>
      <path d="M110,142 C50,132 20,152 -8,150 C28,172 40,196 122,178 Z"/>
      <path d="M114,178 C56,192 28,220 4,232 C44,226 70,236 128,214 Z"/>
      <path d="M126,208 C80,228 54,252 38,268 C78,258 100,262 138,238 Z"/>
    </g>
    <!-- thick curved horns -->
    <path d="M156,92 C146,60 134,36 112,6 C128,34 158,64 186,90 Z" fill="url(#dhH)" opacity="0.9"/>
    <path d="M132,98 C110,64 84,40 48,10 C74,34 116,66 172,94 Z" fill="url(#dhH)" stroke="${P.hi}" stroke-width="2"/>
    <g stroke="${P.mid}" stroke-width="3" fill="none" opacity="0.5" stroke-linecap="round">
      <path d="M104,66 c10,-7 20,-9 28,-6"/><path d="M84,44 c9,-7 18,-8 26,-5"/><path d="M66,26 c8,-6 14,-7 20,-4"/>
    </g>
    <path d="M52,14 C80,38 118,68 168,92" fill="none" stroke="#fff8e0" stroke-width="2.5" stroke-linecap="round" opacity="0.6"/>
    <!-- lower jaw (open) -->
    <path d="M186,164 C222,184 262,192 300,204 C286,226 252,228 220,226 C176,222 138,208 116,190 C142,178 164,170 186,164 Z" fill="url(#dhJ)" stroke="${P.dark}" stroke-width="2"/>
    <!-- upper head + snout -->
    <path d="M62,184 C48,128 82,94 128,90 C158,86 182,90 200,104 C240,112 282,110 314,108 C338,106 351,113 360,123 C366,131 360,144 344,144 C324,152 302,148 284,152 L214,158 L184,162 C150,164 108,158 90,150 C70,168 62,180 62,184 Z" fill="url(#dhG)" stroke="${P.dark}" stroke-width="2"/>
    <!-- crisp rim highlight along the top edge -->
    <path d="M128,94 C162,86 200,90 240,100 C286,108 324,108 352,117" fill="none" stroke="#fffdf2" stroke-width="2.5" stroke-linecap="round" opacity="0.8"/>
    <!-- dorsal crest -->
    <g fill="${P.mid}">
      <path d="M248,106 l9,-16 l6,15 Z"/><path d="M282,106 l8,-15 l6,14 Z"/><path d="M312,108 l7,-13 l5,12 Z"/>
    </g>
    <!-- metal glints -->
    <g fill="#fffdf2">
      <path d="M302,118 l2,7 l7,2 l-7,2 l-2,7 l-2,-7 l-7,-2 l7,-2 Z" opacity="0.9"/>
      <path d="M214,138 l1.5,5 l5,1.5 l-5,1.5 l-1.5,5 l-1.5,-5 l-5,-1.5 l5,-1.5 Z" opacity="0.75"/>
    </g>
    <!-- mouth interior + tongue -->
    <path d="M184,162 L282,152 L266,200 L196,182 Z" fill="#2a1305"/>
    <path d="M198,180 C238,192 264,190 290,194 C264,208 234,208 200,198 Z" fill="#c23b4b"/>
    <!-- fangs -->
    <g fill="#fffbe8">
      <path d="M274,150 l11,36 l10,-34 Z"/><path d="M240,156 l9,28 l9,-27 Z"/><path d="M208,160 l7,22 l7,-21 Z"/>
      <path d="M208,186 l8,-25 l9,24 Z"/><path d="M246,190 l9,-25 l9,24 Z"/>
    </g>
    <!-- brow -->
    <path d="M120,122 C146,96 180,96 204,118 C180,108 148,110 124,128 Z" fill="url(#dhG)"/>
    <!-- eye -->
    <circle cx="158" cy="138" r="30" fill="url(#dhE)"/>
    <ellipse cx="158" cy="139" rx="18" ry="13" fill="#fff6d8"/>
    <ellipse cx="161" cy="139" rx="5.5" ry="12" fill="#241200"/>
    <circle cx="152" cy="133" r="4" fill="#fff"/>
    <path d="M138,130 C150,120 172,122 180,132" fill="none" stroke="${P.dark}" stroke-width="3" stroke-linecap="round"/>
    <!-- nostril -->
    <ellipse cx="330" cy="128" rx="8" ry="5" fill="${P.dark}" transform="rotate(20 330 128)"/>
    <!-- whiskers -->
    <g fill="none" stroke="${P.edge}" stroke-width="3.5" stroke-linecap="round">
      <path d="M350,126 C392,144 414,116 442,128 C466,138 466,158 486,154"/>
      <path d="M342,150 C380,178 402,168 428,190"/>
    </g>
    <!-- beard tufts -->
    <g fill="${P.illum}" opacity="0.92">
      <path d="M200,210 C192,244 198,266 188,294 C210,272 220,246 222,212 Z"/>
      <path d="M228,216 C222,250 228,272 220,298 C240,274 248,250 248,216 Z"/>
      <path d="M256,214 C252,246 258,268 252,294 C268,272 274,248 272,214 Z"/>
    </g>
  </g>
</svg>`;
}

// Front-facing head shown briefly during the hero head-turn.
export function dragonHeadFrontSVG(pal) {
  const P = pal;
  return `
<svg viewBox="0 0 ${FRONT_VB.w} ${FRONT_VB.h}" width="100%" height="100%" style="overflow:visible" xmlns="http://www.w3.org/2000/svg">
  <defs>${defs(P)}</defs>
  <!-- radiating mane -->
  <g fill="url(#dhM)">
    <path d="M104,98 C66,66 34,66 8,50 C34,94 54,106 116,124 Z"/>
    <path d="M196,98 C234,66 266,66 292,50 C266,94 246,106 184,124 Z"/>
    <path d="M86,150 C44,148 18,166 -8,172 C32,180 58,184 104,170 Z"/>
    <path d="M214,150 C256,148 282,166 308,172 C268,180 242,184 196,170 Z"/>
    <path d="M96,196 C60,214 40,238 22,258 C58,244 82,244 116,222 Z"/>
    <path d="M204,196 C240,214 260,238 278,258 C242,244 218,244 184,222 Z"/>
  </g>
  <!-- horns -->
  <path d="M118,86 C102,54 92,34 68,6 C88,32 116,58 140,84 Z" fill="url(#dhH)" stroke="${P.hi}" stroke-width="2"/>
  <path d="M182,86 C198,54 208,34 232,6 C212,32 184,58 160,84 Z" fill="url(#dhH)" stroke="${P.hi}" stroke-width="2"/>
  <!-- face shield -->
  <path d="M82,116 C82,80 112,60 150,58 C188,60 218,80 218,116 C224,150 216,180 188,200 C172,214 160,220 150,222 C140,220 128,214 112,200 C84,180 76,150 82,116 Z" fill="url(#dhG)" stroke="${P.dark}" stroke-width="2"/>
  <path d="M96,96 C120,82 180,82 204,96" fill="none" stroke="#fffdf2" stroke-width="2.5" stroke-linecap="round" opacity="0.7"/>
  <g fill="rgba(120,80,8,0.2)"><ellipse cx="108" cy="170" rx="18" ry="11"/><ellipse cx="192" cy="170" rx="18" ry="11"/></g>
  <!-- muzzle -->
  <path d="M124,120 C138,108 162,108 176,120 C182,150 176,176 150,190 C124,176 118,150 124,120 Z" fill="url(#dhG)"/>
  <ellipse cx="138" cy="160" rx="6" ry="4.5" fill="${P.dark}"/><ellipse cx="162" cy="160" rx="6" ry="4.5" fill="${P.dark}"/>
  <!-- fierce brows -->
  <path d="M92,118 C110,108 132,112 146,130 C128,120 108,120 90,132 Z" fill="url(#dhG)"/>
  <path d="M208,118 C190,108 168,112 154,130 C172,120 192,120 210,132 Z" fill="url(#dhG)"/>
  <!-- eyes -->
  <circle cx="114" cy="138" r="30" fill="url(#dhE)"/><circle cx="186" cy="138" r="30" fill="url(#dhE)"/>
  <ellipse cx="114" cy="139" rx="17" ry="15" fill="#fff6d8"/><ellipse cx="186" cy="139" rx="17" ry="15" fill="#fff6d8"/>
  <ellipse cx="117" cy="140" rx="6" ry="13" fill="#241200"/><ellipse cx="183" cy="140" rx="6" ry="13" fill="#241200"/>
  <circle cx="110" cy="133" r="4" fill="#fff"/><circle cx="182" cy="133" r="4" fill="#fff"/>
  <!-- roaring mouth -->
  <path d="M112,186 C136,181 164,181 188,186 C180,210 164,226 150,228 C136,226 120,210 112,186 Z" fill="#2a1305"/>
  <path d="M130,204 C140,212 160,212 170,204 C160,216 140,216 130,204 Z" fill="#c23b4b"/>
  <g fill="#fffbe8">
    <path d="M120,187 l-3,18 l11,-13 Z"/><path d="M180,187 l3,18 l-11,-13 Z"/>
    <path d="M140,188 l-3,14 l8,0 Z"/><path d="M160,188 l3,14 l-8,0 Z"/><path d="M150,189 l-3,13 l6,0 Z"/>
    <path d="M136,220 l-2,-14 l8,5 Z"/><path d="M164,220 l2,-14 l-8,5 Z"/>
  </g>
  <!-- whiskers -->
  <g fill="none" stroke="${P.edge}" stroke-width="3.5" stroke-linecap="round">
    <path d="M124,156 C82,154 50,176 18,170 C-4,166 -10,154 -26,156"/>
    <path d="M176,156 C218,154 250,176 282,170 C304,166 310,154 326,156"/>
  </g>
  <!-- beard -->
  <g fill="${P.illum}" opacity="0.9">
    <path d="M136,222 C130,254 136,278 128,306 C150,282 156,254 156,224 Z"/>
    <path d="M164,222 C170,254 164,278 172,306 C150,282 144,254 144,224 Z"/>
    <path d="M150,226 C150,258 150,282 150,310 C158,282 158,256 156,228 Z"/>
  </g>
</svg>`;
}
