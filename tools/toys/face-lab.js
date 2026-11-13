// Face lab: the 3D face with the vinyl and wheel eyes, and switchable ideas for the nose and mouth.
// Nose: tree (current), cursor (edit mode), pinecone (opens), tent (unzips, lights up), trowel (digs, a sprout grows).
// Mouth: coffee beans (current), bezier curve (drag the handles), hiking trail (a walker crosses), colour swatches (set the accent).
(() => {
  const root = document.querySelector('.lab, .lab-home'); if (!root || !window.THREE) return;
  const HOME = root.classList.contains('lab-home');   // on the home page the caption stays short
  const stage = root.querySelector('.toy-stage'), tip = root.querySelector('.lab-tip'), overlay = root.querySelector('.lab-overlay');
  const { renderer, scene, camera, ptr, reduce, kick, onTick } = Toy3D.setup(stage, { z: 12.5 });
  const { shadow, rod } = Toy3D, V = (x, y, z) => new THREE.Vector3(x, y, z);
  const css = getComputedStyle(document.documentElement), SIGNAL = css.getPropertyValue('--signal').trim() || '#ff5a1f';
  const face = new THREE.Group(); face.position.y = .35; scene.add(face);
  const steel = new THREE.MeshStandardMaterial({ color: 0xd9dce2, metalness: 1, roughness: .22 });
  const alu = new THREE.MeshStandardMaterial({ color: 0xc4c8cf, metalness: 1, roughness: .32 });
  const std = (color, roughness = .7, extra = {}) => new THREE.MeshStandardMaterial({ color, roughness, ...extra });
  const hit = (geo, k) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial()); m.visible = false; m.userData.k = k; return m; };
  const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();
  const lerp = (a, b, k) => a + (b - a) * Math.min(1, k);
/*EYES*/
  // The accent inside the face: the record's label and the wheel's reflector follow the chosen swatch.
  const setAccent = (c) => {
    const S = 512, cv = document.createElement('canvas'); cv.width = cv.height = S; const g = cv.getContext('2d');
    g.fillStyle = c; g.fillRect(0, 0, S, S);
    g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 5; g.beginPath(); g.arc(S / 2, S / 2, S * .44, 0, 7); g.stroke();
    g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = '700 92px system-ui, sans-serif'; g.fillText('MJ', S / 2, S * .36);
    g.font = '600 34px system-ui, sans-serif'; g.fillText('SIDE A · 33⅓', S / 2, S * .76);
    const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    const m = lab.material[1]; if (m.map) m.map.dispose(); m.map = t; m.needsUpdate = true;
    refl.material.color.set(c); kick();
  };

  // ================= NOSES =================
  const noses = {}, NOSE_Y = -1.6;
  // -- tree (current)
  { const g = new THREE.Group(); g.position.set(0, NOSE_Y, .15);
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(.05, .1, .62, 12), std(0x6a4a34, 1)); trunk.position.y = .2; g.add(trunk);
    const crown = new THREE.Group(); crown.position.y = .38; g.add(crown);
    const COUNT = 260, leaves = new THREE.InstancedMesh(new THREE.IcosahedronGeometry(1, 1), std(0xffffff, .85), COUNT), M = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color();
    for (let i = 0; i < COUNT; i++) { const t = Math.pow(rnd(), .8), a = rnd() * 6.283, R = (.5 * Math.pow(1 - t, .85) + .04) * (.55 + .45 * Math.sqrt(rnd())), s = (.075 + .085 * rnd()) * (1 - .45 * t);
      q.setFromEuler(new THREE.Euler(rnd() * 3, rnd() * 3, rnd() * 3)); M.compose(V(Math.cos(a) * R, t * 1.55, Math.sin(a) * R), q, V(s, s * (.75 + .5 * rnd()), s)); leaves.setMatrixAt(i, M);
      col.setHSL(.34 + .05 * (rnd() - .5), .5 + .2 * rnd(), .1 + .1 * rnd() + .05 * t); leaves.setColorAt(i, col); }
    crown.add(leaves); const h = hit(new THREE.PlaneGeometry(1.2, 2.2), 'nose'); h.position.y = 1; g.add(h);
    noses.tree = { g, tip: 'Tree (current): it sways when you hover it.', tick: (t, dt, on) => { g.rotation.z = Math.sin(t * .0017) * .045 * (on ? 1 : .3); } }; }
  // -- cursor arrow: click for edit mode
  let editMode = false;
  { const g = new THREE.Group(); g.position.set(-.3, .05, .15); g.scale.setScalar(.72);   // a little smaller than the first pass
    const s = new THREE.Shape(); [[0, 0], [0, -1.62], [.38, -1.27], [.63, -1.86], [.87, -1.76], [.62, -1.18], [1.12, -1.18]].forEach(([x, y], i) => i ? s.lineTo(x, y) : s.moveTo(x, y)); s.closePath();
    const body = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: .14, bevelEnabled: true, bevelSize: .035, bevelThickness: .035, bevelSegments: 4 }), new THREE.MeshPhysicalMaterial({ color: 0x15171a, roughness: .25, clearcoat: 1 }));
    const rim = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: .06, bevelEnabled: true, bevelSize: .1, bevelThickness: .03, bevelSegments: 3 }), std(0xffffff, .35)); rim.position.z = -.02;
    g.add(rim, body); const h = hit(new THREE.PlaneGeometry(1.5, 2.2), 'nose'); h.position.set(.5, -.9, .2); g.add(h);
    noses.cursor = { g, tip: 'Cursor: click it and the face enters edit mode, with bounding boxes, handles and spacing.', click: () => { editMode = !editMode; }, tick: (t, dt, on) => { g.position.z = lerp(g.position.z, on ? .5 : .15, dt * 8); }, off: () => { editMode = false; } }; }
  // -- pinecone: click and the scales open and close
  { const g = new THREE.Group(); g.position.set(0, .1, .15); const scales = []; let open = 0, target = 0;
    const N = 96, geo = new THREE.SphereGeometry(1, 12, 8);
    for (let i = 0; i < N; i++) { const t = i / (N - 1), r = .08 + .4 * Math.pow(Math.sin(Math.PI * (.1 + .82 * t)), .8), piv = new THREE.Group();
      piv.position.y = -t * 1.55; piv.rotation.y = i * 2.39996;
      const hinge = new THREE.Group(); hinge.position.x = r * .55; piv.add(hinge);
      const m = new THREE.Mesh(geo, std(new THREE.Color().setHSL(.07, .42, .2 + .1 * rnd()), .75)); m.scale.set(.17, .045, .13); m.position.x = .1; hinge.add(m);
      g.add(piv); scales.push(hinge); }
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(.03, .04, .2, 8), std(0x5a3d28, 1)); stem.position.y = .12; g.add(stem);
    const h = hit(new THREE.PlaneGeometry(1.3, 2), 'nose'); h.position.y = -.75; g.add(h);
    noses.pinecone = { g, tip: 'Pinecone: click it and the scales open and close.', click: () => { target = target ? 0 : 1; },
      tick: (t, dt, on) => { open = lerp(open, target, dt * 4); scales.forEach((s, i) => { s.rotation.z = -.95 + open * 1.25 + (on ? Math.sin(t * .004 + i) * .03 : 0); }); g.rotation.y += dt * (on ? .6 : .12); } }; }
  // -- tent: click and it unzips, warm light inside
  { const g = new THREE.Group(); g.position.set(0, -1.5, -.2); let open = 0, target = 0;
    const tri = (w, hgt) => { const s = new THREE.Shape(); s.moveTo(-w, 0); s.lineTo(w, 0); s.lineTo(0, hgt); s.closePath(); return s; };
    const shell = new THREE.Mesh(new THREE.ExtrudeGeometry(tri(.85, 1.55), { depth: 1.1, bevelEnabled: false }), std(0x3f7355, .9)); g.add(shell);
    const glowMat = new THREE.MeshStandardMaterial({ color: 0x1b1410, emissive: 0xffb45a, emissiveIntensity: 0, roughness: 1 });
    const inside = new THREE.Mesh(new THREE.ShapeGeometry(tri(.5, 1.05)), glowMat); inside.position.set(0, .02, 1.105); g.add(inside);
    const flapGeo = (sign) => { const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(sign * .5, 0); s.lineTo(0, 1.05); s.closePath(); return new THREE.ShapeGeometry(s); };
    const flaps = [-1, 1].map((sign) => { const piv = new THREE.Group(); piv.position.set(sign * .5, .02, 1.12); const m = new THREE.Mesh(flapGeo(-sign), std(0x4c8866, .9, { side: THREE.DoubleSide })); piv.add(m); g.add(piv); return { piv, sign }; });
    const zip = new THREE.Mesh(new THREE.BoxGeometry(.02, 1.02, .01), std(0xe9e2c8, .6)); zip.position.set(0, .53, 1.135); g.add(zip);
    const lamp = new THREE.PointLight(0xffb45a, 0, 5); lamp.position.set(0, .5, 1.6); g.add(lamp);
    const h = hit(new THREE.PlaneGeometry(1.8, 1.7), 'nose'); h.position.set(0, .8, 1.2); g.add(h);
    noses.tent = { g, tip: 'Tent: click it and it unzips, with warm light inside.', click: () => { target = target ? 0 : 1; },
      tick: (t, dt) => { open = lerp(open, target, dt * 3.5); flaps.forEach(({ piv, sign }) => { piv.rotation.y = sign * open * 2.2; }); zip.scale.y = Math.max(.001, 1 - open); zip.position.y = .02 + 1.02 * (1 - (1 - open) / 2);
        glowMat.emissiveIntensity = open * (1.5 + Math.sin(t * .006) * .12); lamp.intensity = open * 6; } }; }
  // -- trowel pointing down: click, it digs, a sprout comes up
  { const g = new THREE.Group(); g.position.set(0, .35, .15); const tool = new THREE.Group(); g.add(tool); let dig = -1, grown = 0, target = 0;
    const handle = new THREE.Mesh(new THREE.CylinderGeometry(.085, .07, .62, 20), std(0xb9763f, .6)); handle.position.y = -.31;
    const cap = new THREE.Mesh(new THREE.SphereGeometry(.085, 20, 12), std(0xb9763f, .6));
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(.03, .03, .3, 12), steel); neck.position.y = -.74;
    const s = new THREE.Shape(); s.moveTo(-.2, 0); s.lineTo(.2, 0); s.quadraticCurveTo(.34, -.45, 0, -1); s.quadraticCurveTo(-.34, -.45, -.2, 0);
    const blade = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: .03, bevelEnabled: true, bevelSize: .012, bevelThickness: .012, bevelSegments: 2 }), steel); blade.position.set(0, -.86, -.015);
    tool.add(handle, cap, neck, blade);
    const soil = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 12), std(0x4a3526, 1)); soil.scale.set(.5, .11, .32); soil.position.y = -2.0; g.add(soil);
    const sprout = new THREE.Group(); sprout.position.set(.3, -1.95, .05); sprout.scale.setScalar(.001); g.add(sprout);
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(.018, .022, .34, 8), std(0x4f9a4f, .7)); stem.position.y = .17; sprout.add(stem);
    [-1, 1].forEach((sg) => { const l = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), std(0x58b058, .6)); l.scale.set(.13, .03, .07); l.position.set(sg * .11, .36, 0); l.rotation.z = sg * .5; sprout.add(l); });
    const h = hit(new THREE.PlaneGeometry(1.3, 2.4), 'nose'); h.position.y = -1; g.add(h);
    noses.trowel = { g, tip: 'Trowel: click it and it digs, and a sprout comes up.', click: () => { if (dig < 0) { dig = 0; target = target ? 0 : 1; } },
      tick: (t, dt, on) => { if (dig >= 0) { dig += dt; const k = Math.min(1, dig / .9), e = Math.sin(k * Math.PI); tool.position.y = -e * .32; tool.rotation.z = Math.sin(k * Math.PI * 4) * .12 * e; if (k >= 1) dig = -1; }
        else tool.rotation.z = lerp(tool.rotation.z, on ? .08 : 0, dt * 6);
        grown = lerp(grown, dig < 0 || dig > .5 ? target : grown, dt * 3); sprout.scale.setScalar(Math.max(.001, grown)); } }; }

  // -- framed artwork: click and it opens larger in a lightbox
  { const g = new THREE.Group(); g.position.set(0, -.6, .12); const ART_SRC = '%%ART%%', W = .78, H = W * 1408 / 1010;
    // a moulded frame, a bevel-cut mat board, the print set back behind it, and glass in front
    const rectHole = (w, h, hw, hh) => { const sh = new THREE.Shape(); sh.moveTo(-w / 2, -h / 2); sh.lineTo(w / 2, -h / 2); sh.lineTo(w / 2, h / 2); sh.lineTo(-w / 2, h / 2); sh.closePath();
      const ho = new THREE.Path(); ho.moveTo(-hw / 2, -hh / 2); ho.lineTo(-hw / 2, hh / 2); ho.lineTo(hw / 2, hh / 2); ho.lineTo(hw / 2, -hh / 2); ho.closePath(); sh.holes.push(ho); return sh; };
    const MAT = .1, BAR = .075, iw = W + MAT * 2, ih = H + MAT * 2;
    const frame = new THREE.Mesh(new THREE.ExtrudeGeometry(rectHole(iw + BAR * 2, ih + BAR * 2, iw, ih), { depth: .075, bevelEnabled: true, bevelSize: .022, bevelThickness: .03, bevelSegments: 5 }), new THREE.MeshPhysicalMaterial({ color: 0x121212, roughness: .32, clearcoat: .5, clearcoatRoughness: .35 })); frame.position.z = -.02; g.add(frame);
    const mat = new THREE.Mesh(new THREE.ExtrudeGeometry(rectHole(iw + .02, ih + .02, W, H), { depth: .012, bevelEnabled: true, bevelSize: .012, bevelThickness: .012, bevelSegments: 2 }), new THREE.MeshStandardMaterial({ color: 0xf6f4ee, roughness: .95 })); mat.position.z = .012; g.add(mat);
    const back = new THREE.Mesh(new THREE.BoxGeometry(iw + BAR, ih + BAR, .02), new THREE.MeshStandardMaterial({ color: 0x2a2623, roughness: .9 })); back.position.z = -.03; g.add(back);
    const print = new THREE.Mesh(new THREE.PlaneGeometry(W + .02, H + .02), new THREE.MeshBasicMaterial({ color: 0x111111 })); print.position.z = .006; g.add(print);
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(iw, ih), new THREE.MeshPhysicalMaterial({ color: 0xffffff, transparent: true, opacity: .07, roughness: .02, metalness: 0, clearcoat: 1, depthWrite: false })); glass.position.z = .05; g.add(glass);
    if (ART_SRC) new THREE.TextureLoader().load(ART_SRC, (t) => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; print.material.map = t; print.material.color.set(0xffffff); print.material.needsUpdate = true; kick(); });
    const h = hit(new THREE.PlaneGeometry(W + .45, H + .45), 'nose'); h.position.z = .12; g.add(h);
    let box = null; const close = () => { if (box) { box.remove(); box = null; removeEventListener('keydown', onKey); } }, onKey = (e) => { if (e.key === 'Escape') close(); };
    const openBox = () => { if (box) return; box = document.createElement('div'); box.className = 'art-lightbox'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-modal', 'true'); box.setAttribute('aria-label', 'Artwork by Matt Jongbloet');
      box.innerHTML = '<button type="button" aria-label="Close">Close ✕</button><img src="../assets/art-why.jpg" alt="“Why?”, a dense black and white line illustration by Matt Jongbloet">';
      box.addEventListener('click', close); document.body.appendChild(box); addEventListener('keydown', onKey); box.querySelector('button').focus(); };
    noses.art = { g, tip: 'Framed art: click it and the piece opens larger.', click: openBox, off: close,
      tick: (t, dt, on) => { g.position.z = lerp(g.position.z, on ? .35 : .12, dt * 8); g.rotation.z = lerp(g.rotation.z, on ? -.04 : 0, dt * 8); } }; }

  // ================= MOUTHS =================
  const mouths = {}, MOUTH_Y = -2.35;
  // -- coffee beans (current)
  { const g = new THREE.Group(); g.position.set(0, MOUTH_Y, .1); const beans = [];
    const beanMat = new THREE.MeshPhysicalMaterial({ color: 0x4d2c1a, roughness: .5, clearcoat: .25 }), slitMat = std(0x24120a, .8);
    for (let i = 0; i < 7; i++) { const x = -1.5 + i * .5, y = -.5 + .22 * x * x, b = new THREE.Group();
      const body = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 20), beanMat); body.scale.set(.2, .135, .1);
      const slit = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), slitMat); slit.scale.set(.17, .014, .03); slit.position.z = .085;
      b.add(body, slit); b.position.set(x, y, 0); b.rotation.z = Math.atan(.44 * x); b.userData.y = y; g.add(b); beans.push(b); }
    const h = hit(new THREE.PlaneGeometry(3.6, 1.1), 'mouth'); h.position.y = -.2; g.add(h);
    mouths.beans = { g, tip: 'Coffee beans (current): they hop when you hover them.', tick: (t, dt, on) => beans.forEach((b, i) => { b.position.y = b.userData.y + (on ? Math.max(0, Math.sin(t * .008 - i * .8)) * .16 : 0); }) }; }
  // -- bezier curve with handles: drag them
  let dragging = null;
  { const g = new THREE.Group(); g.position.set(0, MOUTH_Y, .1);
    const A = V(-1.5, 0, 0), B = V(1.5, 0, 0), C = [V(-.75, -1.0, 0), V(.75, -1.0, 0)];
    const cord = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshPhysicalMaterial({ color: 0x15171a, roughness: .3, clearcoat: 1 })); g.add(cord);
    const lineMat = std(0x9a9ea8, .6), lines = new THREE.Group(); g.add(lines);
    const knobs = C.map((c, i) => { const k = new THREE.Mesh(new THREE.SphereGeometry(.13, 24, 16), new THREE.MeshPhysicalMaterial({ color: SIGNAL, roughness: .25, clearcoat: 1 })); k.userData.k = 'mouth'; k.userData.handle = i; g.add(k);
      const hz = hit(new THREE.SphereGeometry(.32, 8, 6), 'mouth'); hz.userData.handle = i; k.add(hz); return k; });
    [A, B].forEach((p) => { const a = new THREE.Mesh(new THREE.BoxGeometry(.16, .16, .16), std(0xffffff, .4)); a.position.copy(p); g.add(a); const e = new THREE.Mesh(new THREE.BoxGeometry(.2, .2, .12), std(0x15171a, .4)); e.position.copy(p).setZ(-.03); g.add(e); });
    const rebuild = () => { cord.geometry.dispose(); cord.geometry = new THREE.TubeGeometry(new THREE.CubicBezierCurve3(A, C[0], C[1], B), 64, .06, 10, false);
      while (lines.children.length) { const c = lines.children.pop(); c.geometry.dispose(); } lines.add(rod(A, C[0], .012, lineMat), rod(B, C[1], .012, lineMat)); knobs.forEach((k, i) => k.position.copy(C[i])); shadow(g); };
    rebuild();
    const mood = () => { const y = (C[0].y + C[1].y) / 2, skew = Math.abs(C[0].y - C[1].y); return skew > .7 ? 'a smirk' : y < -.35 ? 'a smile' : y > .35 ? 'a frown' : 'a straight face'; };
    mouths.bezier = { g, tip: 'Bezier curve: drag the two orange handles to make it smile, smirk or frown.',
      drag: (i, local) => { C[i].set(Math.max(-2.2, Math.min(2.2, local.x)), Math.max(-1.3, Math.min(1.3, local.y - MOUTH_Y)), 0); rebuild(); if (!HOME) tip.textContent = 'Bezier curve: that’s ' + mood() + '.'; }, tick: () => {} }; }
  // -- dotted hiking trail: click and a walker crosses, leaving footprints
  { const g = new THREE.Group(); g.position.set(0, MOUTH_Y, .1); const at = (u) => { const x = -1.6 + 3.2 * u; return V(x, -.55 + .2 * x * x, 0); }; let walk = -1;
    for (let i = 0; i <= 16; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(.045, 12, 8), std(0x8b6b4a, .9)); d.position.copy(at(i / 16)); d.scale.z = .5; g.add(d); }
    const prints = []; for (let i = 0; i < 15; i++) { const f = new THREE.Mesh(new THREE.SphereGeometry(1, 10, 6), std(0x33363c, 1)); const pt = at((i + .5) / 15); f.scale.set(.05, .028, .01); f.position.set(pt.x, pt.y + .12 + (i % 2 ? .05 : -.02), 0); f.visible = false; g.add(f); prints.push(f); }
    const walker = new THREE.Group(); const bodyM = new THREE.Mesh(new THREE.CapsuleGeometry(.055, .12, 6, 12), new THREE.MeshPhysicalMaterial({ color: SIGNAL, roughness: .4 })); bodyM.position.y = .13;
    const head = new THREE.Mesh(new THREE.SphereGeometry(.055, 16, 12), std(0xf1c7a3, .6)); head.position.y = .3;
    const pack = new THREE.Mesh(new THREE.BoxGeometry(.07, .11, .06), std(0x2f55e4, .6)); pack.position.set(-.07, .15, 0);
    walker.add(bodyM, head, pack); walker.position.copy(at(0)); g.add(walker);
    const flagPole = rod(V(1.72, -.02, 0), V(1.72, .42, 0), .012, steel), flag = new THREE.Mesh(new THREE.BoxGeometry(.2, .12, .01), std(0x1a7f45, .6)); flag.position.set(1.83, .35, 0); g.add(flagPole, flag);
    const h = hit(new THREE.PlaneGeometry(3.8, 1.3), 'mouth'); h.position.y = -.15; g.add(h);
    mouths.trail = { g, tip: 'Hiking trail: click it and a tiny walker crosses, leaving footprints.', click: () => { if (walk < 0) { walk = 0; prints.forEach((f) => f.visible = false); } },
      tick: (t, dt) => { if (walk < 0) return; walk += dt / 3.2; const u = Math.min(1, walk), pt = at(u); walker.position.set(pt.x, pt.y + Math.abs(Math.sin(u * 60)) * .035, 0); walker.rotation.z = Math.sin(u * 60) * .08;
        prints.forEach((f, i) => { if ((i + .5) / 15 < u - .03) f.visible = true; }); if (walk > 1.45) { walk = -1; walker.position.copy(at(0)); walker.rotation.z = 0; } } }; }
  // -- fanned colour swatches: click one, the accent colour changes
  { const g = new THREE.Group(); g.position.set(0, -.95, .1); const COLS = ['#ff5a1f', '#2f55e4', '#1a7f45', '#e6a817', '#ef5da8', '#7a4fd6']; const cards = [];
    COLS.forEach((c, i) => { const piv = new THREE.Group(); piv.rotation.z = (-50 + i * 20) * Math.PI / 180; piv.position.z = i * .012;
      const card = new THREE.Group(); card.position.y = -1.55; piv.add(card);
      const paper = new THREE.Mesh(new THREE.BoxGeometry(.5, .86, .02), std(0xffffff, .5)); const chip = new THREE.Mesh(new THREE.BoxGeometry(.42, .56, .012), std(c, .45)); chip.position.set(0, -.1, .012);
      const hz = hit(new THREE.PlaneGeometry(.5, .86), 'mouth'); hz.userData.swatch = c; hz.position.z = .03;
      card.add(paper, chip, hz); g.add(piv); cards.push({ card, c }); });
    const pin = new THREE.Mesh(new THREE.CylinderGeometry(.05, .05, .12, 20), steel); pin.rotation.x = Math.PI / 2; pin.position.z = .06; g.add(pin);
    let picked = null;
    mouths.swatches = { g, tip: 'Colour swatches: click one. The page accent, the record’s label and the wheel’s reflector all change.', click: (obj) => { const c = obj.userData.swatch; if (!c) return; picked = c; document.documentElement.style.setProperty('--signal', c); setAccent(c);
        // Text in the accent (the headline's last line) needs 3:1 on a light page, so pale colours are deepened for text only.
        const col = new THREE.Color(c), lum = (x) => { const f = (v) => v <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); const k = new THREE.Color(x).convertLinearToSRGB(); return .2126 * f(k.r) + .7152 * f(k.g) + .0722 * f(k.b); };
        const light = document.documentElement.dataset.theme !== 'dark'; let text = col.clone(), n = 0;
        while (light && 1.05 / (lum(text) + .05) < 3.2 && n++ < 20) text.multiplyScalar(.93);
        document.documentElement.style.setProperty('--accent-text', '#' + text.getHexString()); if (!HOME) tip.textContent = 'Colour swatches: accent set to ' + c + '.'; },
      tick: (t, dt) => cards.forEach(({ card, c }) => { card.position.y = lerp(card.position.y, c === picked ? -1.72 : -1.55, dt * 8); }) }; }

  // -- half a stroopwafel: each click takes a bite where you clicked; it grows back slowly
  { const g = new THREE.Group(); g.position.set(0, MOUTH_Y - .1, .08); const S = 512, cv = document.createElement('canvas'); cv.width = S; cv.height = S / 2; const c2 = cv.getContext('2d');
    const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace; tex.anisotropy = 8; const bites = [];
    // baked once: golden wafer, darker toward the rim, speckled, with the pressed diamond grid; plus a height map for the relief
    const base = document.createElement('canvas'); base.width = S; base.height = S / 2; const height = document.createElement('canvas'); height.width = S; height.height = S / 2;
    { const b = base.getContext('2d'), hh = height.getContext('2d'); const clip = (c) => { c.beginPath(); c.arc(S / 2, 0, S / 2 - 2, 0, Math.PI); c.closePath(); c.clip(); };
      b.save(); clip(b); const gr = b.createRadialGradient(S / 2, 0, S * .05, S / 2, 0, S / 2); gr.addColorStop(0, '#e2a654'); gr.addColorStop(.7, '#d29245'); gr.addColorStop(1, '#a8672a'); b.fillStyle = gr; b.fillRect(0, 0, S, S / 2);
      for (let i = 0; i < 2600; i++) { b.fillStyle = `rgba(${rnd() > .5 ? '120,66,20' : '255,214,150'},${.05 + rnd() * .12})`; b.beginPath(); b.arc(rnd() * S, rnd() * S / 2, .6 + rnd() * 2.2, 0, 6.283); b.fill(); }
      hh.fillStyle = '#555'; hh.fillRect(0, 0, S, S / 2);
      for (const [cx, w, a, hc] of [[b, 7, 'rgba(150,88,30,.55)', null], [hh, 9, null, '#fff']]) { cx.strokeStyle = a || hc; cx.lineWidth = w; cx.lineCap = 'round';
        for (let i = -S; i < S * 2; i += 26) { cx.beginPath(); cx.moveTo(i, 0); cx.lineTo(i + S / 2, S / 2); cx.stroke(); cx.beginPath(); cx.moveTo(i, 0); cx.lineTo(i - S / 2, S / 2); cx.stroke(); } }
      b.strokeStyle = 'rgba(255,225,170,.35)'; b.lineWidth = 2; for (let i = -S; i < S * 2; i += 26) { b.beginPath(); b.moveTo(i - 3, 0); b.lineTo(i - 3 + S / 2, S / 2); b.stroke(); }
      b.restore(); b.strokeStyle = '#96591f'; b.lineWidth = 10; b.beginPath(); b.arc(S / 2, 0, S / 2 - 7, 0, Math.PI); b.stroke(); b.fillStyle = '#96591f'; b.fillRect(0, 0, S, 5); }
    const bump = new THREE.CanvasTexture(height); bump.anisotropy = 8;
    const paint = (now) => { c2.globalCompositeOperation = 'source-over'; c2.clearRect(0, 0, S, S / 2); c2.drawImage(base, 0, 0);
      c2.globalCompositeOperation = 'destination-out';
      for (const b of bites) { const k = Math.max(0, 1 - Math.max(0, now - b.t - 2500) / 6500), r = b.r * k; if (r < 1) continue;
        for (let j = 0; j < 6; j++) { const a = j / 6 * 6.283 + b.a; c2.beginPath(); c2.arc(b.x + Math.cos(a) * r * .55, b.y + Math.sin(a) * r * .55, r * .58, 0, 6.283); c2.fill(); } }
      tex.needsUpdate = true; };
    paint(0);
    // twelve thin layers give it real thickness: wafer, a glossy caramel middle, wafer. Bites cut through all of them.
    const geo = new THREE.PlaneGeometry(3.1, 1.55), layers = [], LN = 12;
    for (let i = 0; i < LN; i++) { const caramel = i >= 5 && i <= 6, top = i === LN - 1;
      const m = new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ map: tex, color: caramel ? 0x7a3f10 : top ? 0xffffff : 0xb9783a, roughness: caramel ? .18 : .78, clearcoat: caramel ? 1 : 0, alphaTest: .5,
        bumpMap: top ? bump : null, bumpScale: top ? 1.6 : 0 })); m.position.z = i * .0125; if (caramel) m.scale.set(1.012, 1.02, 1);
      m.customDepthMaterial = new THREE.MeshDepthMaterial({ depthPacking: THREE.RGBADepthPacking, map: tex, alphaTest: .5 }); g.add(m); layers.push(m); }
    layers[LN - 1].userData.k = 'mouth';
    const crunch = () => { try { audio(); const src = ac.createBufferSource(), bp = ac.createBiquadFilter(), gn = ac.createGain(), now = ac.currentTime; src.buffer = noise; bp.type = 'bandpass'; bp.frequency.value = 1500; bp.Q.value = .8;
      gn.gain.setValueAtTime(.22, now); gn.gain.exponentialRampToValueAtTime(.0001, now + .09); src.connect(bp).connect(gn).connect(ac.destination); src.start(now); src.stop(now + .03); } catch (e) { /* no audio: bite silently */ } };
    mouths.stroopwafel = { g, tip: 'Stroopwafel: click to take a bite. Eat it all if you like; it grows back.',
      click: (obj, uv) => { if (!uv) return; bites.push({ x: uv.x * S, y: (1 - uv.y) * S / 2, r: 52, a: Math.random() * 6, t: performance.now() }); crunch(); tip.textContent = HOME ? tip.textContent : 'Stroopwafel: ' + bites.length + (bites.length === 1 ? ' bite' : ' bites') + ' taken. It grows back in a few seconds.'; },
      tick: (t) => { if (!bites.length) return; const now = performance.now(); while (bites.length && now - bites[0].t > 9200) bites.shift(); paint(now); } }; }

  Object.values(noses).concat(Object.values(mouths)).forEach((o) => { face.add(o.g); shadow(o.g); o.g.visible = false; });
  let nose = 'tree', mouth = 'beans';
  const choose = (kind, name) => {
    const set = kind === 'nose' ? noses : mouths, prev = kind === 'nose' ? nose : mouth;
    if (set[prev].off) set[prev].off(); set[prev].g.visible = false; set[name].g.visible = true;
    if (kind === 'nose') nose = name; else mouth = name;
    root.querySelectorAll(`[data-kind="${kind}"]`).forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.name === name)));
    if (!HOME) tip.textContent = set[name].tip; kick();
  };
  root.querySelectorAll('.lab-opts button').forEach((b) => b.addEventListener('click', () => choose(b.dataset.kind, b.dataset.name)));
  noses.tree.g.visible = true; mouths.beans.g.visible = true;
  if (HOME) { choose('mouth', 'swatches'); choose('nose', 'cursor'); } else { choose('mouth', 'stroopwafel'); choose('nose', 'art'); }   // home: Matt's pick; lab: what he's trying now

  // ---- sound (Web Audio, nothing to download). Browsers only allow sound after a click, so both start on click.
  let ac = null, stopMusic = null, noise = null, ticks = 0, push = 0;
  const audio = () => { ac = ac || new (window.AudioContext || window.webkitAudioContext)(); if (ac.state === 'suspended') ac.resume();
    if (!noise) { noise = ac.createBuffer(1, ac.sampleRate * .03, ac.sampleRate); const d = noise.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; } return ac; };
  const playMusic = () => {                              // the record: a small lo-fi loop
    audio(); const master = ac.createGain(), lp = ac.createBiquadFilter();
    master.gain.setValueAtTime(.0001, ac.currentTime); master.gain.exponentialRampToValueAtTime(.16, ac.currentTime + .4);
    lp.type = 'lowpass'; lp.frequency.value = 1300; lp.connect(master); master.connect(ac.destination);
    const chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [196, 246.94, 293.66], [164.81, 207.65, 246.94]]; let step = 0; const beat = 1.5;
    const go = () => { const now = ac.currentTime; chords[step++ % 4].forEach((f, i) => { const o = ac.createOscillator(), g = ac.createGain(); o.type = 'triangle'; o.frequency.value = f;
      g.gain.setValueAtTime(.0001, now + i * .09); g.gain.exponentialRampToValueAtTime(.2, now + i * .09 + .06); g.gain.exponentialRampToValueAtTime(.0001, now + beat * .95); o.connect(g).connect(lp); o.start(now + i * .09); o.stop(now + beat); }); };
    go(); const timer = setInterval(go, beat * 1000);
    stopMusic = () => { clearInterval(timer); master.gain.exponentialRampToValueAtTime(.0001, ac.currentTime + .3); setTimeout(() => master.disconnect(), 400); stopMusic = null; };
  };
  const tick = (vol) => {                                // the wheel: one click of the freewheel
    if (!ac || ac.state !== 'running') return; const src = ac.createBufferSource(), bp = ac.createBiquadFilter(), g = ac.createGain(), now = ac.currentTime;
    src.buffer = noise; bp.type = 'bandpass'; bp.frequency.value = 3400; bp.Q.value = 2.2; g.gain.setValueAtTime(vol, now); g.gain.exponentialRampToValueAtTime(.0001, now + .018);
    src.connect(bp).connect(g).connect(ac.destination); src.start(now); src.stop(now + .03);
  };

  // ---- pointer: hover, click, drag
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(); let hover = null;
  const cast = (e) => { const r = stage.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, camera);
    const vis = (o) => { for (let p = o; p; p = p.parent) if (p !== o && p.visible === false) return false; return true; };
    return ray.intersectObjects(face.children, true).find((i) => i.object.userData.k && vis(i.object)); };
  const plane = new THREE.Plane(), pt = new THREE.Vector3();
  stage.addEventListener('pointermove', (e) => {
    if (dragging !== null) { plane.setFromNormalAndCoplanarPoint(V(0, 0, 1).applyQuaternion(face.quaternion), face.localToWorld(V(0, MOUTH_Y, .1))); cast(e); if (ray.ray.intersectPlane(plane, pt)) mouths.bezier.drag(dragging, face.worldToLocal(pt.clone())); kick(); return; }
    if (e.pointerType === 'touch') return; const h = cast(e); hover = h ? h.object.userData.k : null; stage.style.cursor = h ? (h.object.userData.handle !== undefined ? 'grab' : 'pointer') : ''; kick(); });
  stage.addEventListener('pointerdown', (e) => { const h = cast(e); if (h && h.object.userData.handle !== undefined && mouth === 'bezier') { dragging = h.object.userData.handle; stage.setPointerCapture(e.pointerId); stage.style.cursor = 'grabbing'; } });
  const drop = () => { dragging = null; stage.style.cursor = ''; }; stage.addEventListener('pointerup', drop); stage.addEventListener('pointercancel', drop);
  stage.addEventListener('pointerleave', () => { hover = null; });
  stage.addEventListener('click', (e) => { const h = cast(e); if (!h) return; const k = h.object.userData.k;
    if (k === 'music') { if (stopMusic) stopMusic(); else playMusic(); }
    if (k === 'cycle') { audio(); push = 16; }                // a push: it spins up, then coasts and ticks down
    if (k === 'nose' && noses[nose].click) noses[nose].click(h.object); if (k === 'mouth' && mouths[mouth].click) mouths[mouth].click(h.object, h.uv); kick(); });

  // ---- edit mode overlay (cursor nose): bounding boxes, handles, spacing
  const boxEls = ['Eye', 'Eye', 'Nose', 'Mouth'].map((n) => { const d = document.createElement('div'); d.className = 'lab-box'; d.innerHTML = `<i></i><i></i><i></i><i></i><span></span><b>${n}</b>`; overlay.appendChild(d); return d; });
  const gapEl = document.createElement('div'); gapEl.className = 'lab-gap'; gapEl.innerHTML = '<span></span>'; overlay.appendChild(gapEl);
  const box3 = new THREE.Box3(), corner = new THREE.Vector3();
  const screenBox = (o) => { box3.setFromObject(o); const r = stage.getBoundingClientRect(); let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const x of [box3.min.x, box3.max.x]) for (const y of [box3.min.y, box3.max.y]) for (const z of [box3.min.z, box3.max.z]) { corner.set(x, y, z).project(camera); const sx = (corner.x + 1) / 2 * r.width, sy = (1 - corner.y) / 2 * r.height; x0 = Math.min(x0, sx); x1 = Math.max(x1, sx); y0 = Math.min(y0, sy); y1 = Math.max(y1, sy); }
    return [x0, y0, x1, y1]; };

  // ---- motion
  let vSpin = 0, wSpin = 0;
  onTick((time, dt) => {
    const music = hover === 'music' || !!stopMusic; arm.rotation.z = lerp(arm.rotation.z, music ? -.43 : .1, dt * 5); arm.position.z = lerp(arm.position.z, music ? .1 : .2, dt * 5);
    vSpin = lerp(vSpin, music ? 3.49 : 0, dt * (music ? 2.5 : 1.4)); spinner.rotation.z -= vSpin * dt;
    if (push) { wSpin = Math.max(wSpin, push); push = 0; }
    wSpin = lerp(wSpin, hover === 'cycle' ? Math.max(11, wSpin) : 0, dt * (hover === 'cycle' ? 3 : .35)); wspin.rotation.z -= wSpin * dt;
    ticks += wSpin * dt * 24 / 6.283; let nTick = 0; while (ticks >= 1) { ticks -= 1; if (wSpin > .6 && nTick++ < 3) tick(.05 + Math.min(.07, wSpin * .005)); }   // 24 clicks a turn
    noses[nose].tick(time, dt, hover === 'nose'); mouths[mouth].tick(time, dt, hover === 'mouth');
    const still = editMode || dragging !== null || reduce, idle = time - ptr.at > 3000, gx = still ? 0 : idle ? Math.sin(time * .0006) * .25 : ptr.x, gy = still ? 0 : idle ? Math.cos(time * .0008) * .15 : ptr.y;
    face.rotation.y = lerp(face.rotation.y, gx * .42, dt * 4); face.rotation.x = lerp(face.rotation.x, gy * .3, dt * 4);
    overlay.classList.toggle('on', editMode);
    if (editMode) { const bs = [vinyl, wheel, noses[nose].g, mouths[mouth].g].map(screenBox);
      bs.forEach(([x0, y0, x1, y1], i) => { const el = boxEls[i]; el.style.cssText = `left:${x0}px;top:${y0}px;width:${x1 - x0}px;height:${y1 - y0}px`; el.querySelector('span').textContent = `${Math.round(x1 - x0)} × ${Math.round(y1 - y0)}`; });
      const gx0 = bs[0][2], gx1 = bs[1][0], gy0 = (bs[0][1] + bs[0][3]) / 2; gapEl.style.cssText = `left:${gx0}px;top:${gy0}px;width:${Math.max(0, gx1 - gx0)}px`; gapEl.querySelector('span').textContent = Math.round(gx1 - gx0); }
  });
})();
