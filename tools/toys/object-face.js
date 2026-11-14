// 2 · Object face, in 3D. Each object is modelled in code: a grooved record with a tonearm, a laced bicycle wheel,
// a tree, and coffee beans for the smile. Hover wakes a piece, click opens its card; the record plays a generated loop.
(() => {
  const root = document.querySelector('.toy-face'); if (!root || !window.THREE) return;
  const stage = root.querySelector('.toy-stage'), pop = root.querySelector('.face-pop'), chips = [...root.querySelectorAll('.face-chips button')];
  const { renderer, scene, camera, ptr, reduce, kick, onTick } = Toy3D.setup(stage, { z: 12.5 });
  const { shadow, rod } = Toy3D, V = (x, y, z) => new THREE.Vector3(x, y, z);
  const css = getComputedStyle(document.documentElement), SIGNAL = css.getPropertyValue('--signal').trim() || '#ff5a1f';
  const face = new THREE.Group(); face.position.y = .35; scene.add(face);
  const steel = new THREE.MeshStandardMaterial({ color: 0xd9dce2, metalness: 1, roughness: .22 });
  const alu = new THREE.MeshStandardMaterial({ color: 0xc4c8cf, metalness: 1, roughness: .32 });
  const hit = (geo, k) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial()); m.visible = false; m.userData.k = k; return m; };
  const rnd = (() => { let s = 7; return () => (s = (s * 16807) % 2147483647) / 2147483647; })();

  // ---- Left eye: vinyl record ----
  const vinyl = new THREE.Group(); vinyl.position.set(-1.85, .85, 0); vinyl.scale.setScalar(.95); vinyl.userData.k = 'music'; face.add(vinyl);
  // Vinyl's look comes from anisotropy: thousands of circular grooves stretch every highlight into a bright wedge.
  // One texture gives the groove direction (around the centre); a faint normal map adds the track gaps and fine shimmer.
  const [grooves, aniso] = (() => {
    const S = 1024, mk = () => { const c = document.createElement('canvas'); c.width = c.height = S; return c; };
    const cn = mk(), ca = mk(), gn = cn.getContext('2d'), ga = ca.getContext('2d'), n = gn.createImageData(S, S), a = ga.createImageData(S, S), h = S / 2;
    for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
      const dx = (x - h) / h, dy = (h - y) / h, r = Math.hypot(dx, dy) || 1e-6, i = (y * S + x) * 4;
      const inGroove = r > .36 && r < .965, gap = Math.abs(r - .56) < .008 || Math.abs(r - .74) < .008 || Math.abs(r - .87) < .008;
      const k = inGroove ? (gap ? .55 * Math.sin((r % .016) / .016 * Math.PI * 2) : .16 * Math.cos(r * 300)) : 0;
      n.data[i] = (dx / r * k * .5 + .5) * 255; n.data[i + 1] = (dy / r * k * .5 + .5) * 255; n.data[i + 2] = 255; n.data[i + 3] = 255;
      a.data[i] = (-dy / r * .5 + .5) * 255; a.data[i + 1] = (dx / r * .5 + .5) * 255; a.data[i + 2] = inGroove && !gap ? 255 : 40; a.data[i + 3] = 255;
    }
    gn.putImageData(n, 0, 0); ga.putImageData(a, 0, 0);
    return [cn, ca].map((c) => { const t = new THREE.CanvasTexture(c); t.anisotropy = renderer.capabilities.getMaxAnisotropy(); return t; });
  })();
  const label = (() => {
    const S = 512, c = document.createElement('canvas'); c.width = c.height = S; const g = c.getContext('2d');
    g.fillStyle = SIGNAL; g.fillRect(0, 0, S, S);
    g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 5; g.beginPath(); g.arc(S / 2, S / 2, S * .44, 0, 7); g.stroke();
    g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = '700 84px system-ui, sans-serif'; g.fillText('MJ', S / 2, S * .35);
    g.fillText('DNB', S / 2, S * .8);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  })();
  // What makes a real record read as turning: the music itself. Loud and quiet passages cut the grooves differently, so each
  // track has streaks and bands that vary round the disc; the gaps between tracks and the run-out are glassy; and there is
  // always a little dust and a hairline scratch or two. One canvas carries the colour, another how sharp the sheen is.
  const [vinylMap, vinylRough] = (() => {
    const S = 1024, h = S / 2, mk = () => { const c = document.createElement('canvas'); c.width = c.height = S; return c; }, cc = mk(), cr = mk(), c = cc.getContext('2d'), r = cr.getContext('2d');
    c.fillStyle = '#060607'; c.fillRect(0, 0, S, S); r.fillStyle = 'rgb(0,112,0)'; r.fillRect(0, 0, S, S);
    const ring = (ctx, rad, w, style) => { ctx.strokeStyle = style; ctx.lineWidth = w; ctx.beginPath(); ctx.arc(h, h, rad * h, 0, 6.2832); ctx.stroke(); };
    const arc = (ctx, rad, a0, len, w, style) => { ctx.strokeStyle = style; ctx.lineWidth = w; ctx.beginPath(); ctx.arc(h, h, rad * h, a0, a0 + len); ctx.stroke(); };
    const tracks = [[.365, .552], [.568, .732], [.748, .862], [.878, .962]];
    tracks.forEach(([a, b], t) => { ring(c, (a + b) / 2, (b - a) * h, ['#070708', '#09090b', '#060607', '#0a0a0c'][t]); ring(r, (a + b) / 2, (b - a) * h, `rgb(0,${[104, 122, 98, 118][t]},0)`); });   // each track has its own tone
    for (let i = 0; i < 70; i++) { const [a, b] = tracks[i % 4], rad = a + rnd() * (b - a), a0 = rnd() * 6.2832, len = .5 + rnd() * 2.6, w = 5 + rnd() * 16, loud = rnd() > .5;      // loud and quiet passages: broad bands
      arc(c, rad, a0, len, w, loud ? 'rgba(26,26,30,.5)' : 'rgba(0,0,0,.45)'); arc(r, rad, a0, len, w, `rgba(0,${loud ? 170 : 62},0,.5)`); }
    for (let i = 0; i < 1500; i++) { const [a, b] = tracks[i % 4], rad = a + rnd() * (b - a), a0 = rnd() * 6.2832, len = .08 + rnd() * 1.1, w = .7 + rnd() * 2.2, loud = rnd() > .5;   // fine streaks inside them
      arc(c, rad, a0, len, w, loud ? 'rgba(40,40,46,.4)' : 'rgba(0,0,0,.5)'); arc(r, rad, a0, len, w, `rgba(0,${loud ? 190 : 50},0,.4)`); }
    for (const g of [.56, .74, .87]) { ring(c, g, .016 * h, '#020203'); ring(r, g, .016 * h, 'rgb(0,34,0)'); }                                                                     // glassy gaps between tracks
    ring(c, .33, .07 * h, '#030304'); ring(r, .33, .07 * h, 'rgb(0,30,0)'); ring(c, .98, .03 * h, '#040405'); ring(r, .98, .03 * h, 'rgb(0,44,0)');                              // run-out and lead-in: smooth
    for (const ctx of [c, r]) { ctx.strokeStyle = ctx === c ? 'rgba(46,46,52,.8)' : 'rgba(0,150,0,.8)'; ctx.lineWidth = 1.3; ctx.beginPath();                                       // the run-out groove spirals in to a locked ring
      for (let i = 0; i <= 260; i++) { const a = i / 260 * 6.2832 * 1.75, rad = (.362 - i / 260 * .05) * h; ctx[i ? 'lineTo' : 'moveTo'](h + Math.cos(a) * rad, h + Math.sin(a) * rad); } ctx.stroke(); }
    ring(c, .312, 1.3, 'rgba(46,46,52,.8)'); ring(r, .312, 1.3, 'rgba(0,150,0,.8)');
    for (let i = 0; i < 520; i++) { const rad = (.3 + rnd() * .68) * h, a = rnd() * 6.2832, x = h + Math.cos(a) * rad, y = h + Math.sin(a) * rad, sz = .5 + rnd() * 1.2;                // dust
      c.fillStyle = `rgba(170,170,176,${.25 + rnd() * .45})`; c.beginPath(); c.arc(x, y, sz, 0, 6.2832); c.fill(); r.fillStyle = 'rgba(0,230,0,.8)'; r.beginPath(); r.arc(x, y, sz * 1.2, 0, 6.2832); r.fill(); }
    for (let i = 0; i < 7; i++) { const rad = (.42 + rnd() * .5) * h, a = rnd() * 6.2832, x = h + Math.cos(a) * rad, y = h + Math.sin(a) * rad, d = rnd() * 6.2832, L = 30 + rnd() * 110;   // hairline scratches
      for (const ctx of [c, r]) { ctx.strokeStyle = ctx === c ? 'rgba(120,120,128,.22)' : 'rgba(0,220,0,.5)'; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + Math.cos(d) * L, y + Math.sin(d) * L); ctx.stroke(); } }
    const tc = new THREE.CanvasTexture(cc), tr = new THREE.CanvasTexture(cr); tc.colorSpace = THREE.SRGBColorSpace; tc.anisotropy = tr.anisotropy = renderer.capabilities.getMaxAnisotropy(); return [tc, tr];
  })();
  // No pressing is perfectly flat: a slight warp tilts the disc inside the spinner, so its sheen rocks as it turns.
  const spinner = new THREE.Group(); vinyl.add(spinner); const warp = new THREE.Group(); warp.rotation.set(.016, .011, 0); spinner.add(warp);
  const blackVinyl = new THREE.MeshPhysicalMaterial({ color: 0xffffff, map: vinylMap, roughness: 1, roughnessMap: vinylRough, metalness: .15, anisotropy: 1, anisotropyMap: aniso, normalMap: grooves, normalScale: new THREE.Vector2(.5, .5), envMapIntensity: 1.02 });   // roughness comes from the map (green channel): about .2 in the gaps, .4 in the grooves, more on dust
  const edge = new THREE.MeshPhysicalMaterial({ color: 0x08080a, roughness: .35 });
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, .045, 128), [edge, blackVinyl, edge]); disc.rotation.x = Math.PI / 2; warp.add(disc);
  const lab = new THREE.Mesh(new THREE.CylinderGeometry(.44, .44, .05, 64), [edge, new THREE.MeshStandardMaterial({ map: label, roughness: .75 }), edge]); lab.rotation.x = Math.PI / 2; lab.position.z = .004; warp.add(lab);
  const spindle = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, .16, 24), steel); spindle.rotation.x = Math.PI / 2; spindle.position.z = .06; vinyl.add(spindle);
  // Technics SL-1210 style: platter, gimbal base, S-shaped tonearm, angled headshell with finger lift, counterweight.
  const black = new THREE.MeshStandardMaterial({ color: 0x17181b, metalness: .6, roughness: .42 }), chrome = new THREE.MeshStandardMaterial({ color: 0xe8eaee, metalness: 1, roughness: .1 });
  const cylZ = (r, h, mat, seg = 40) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, h, seg), mat); m.rotation.x = Math.PI / 2; return m; };
  const platter = cylZ(1.37, .07, alu, 128); platter.position.z = -.062; vinyl.add(platter);
  const dots = new THREE.InstancedMesh(new THREE.CylinderGeometry(.011, .011, .012, 8), black, 180), DM = new THREE.Matrix4();   // strobe dots on the platter rim
  for (let d = 0; d < 180; d++) { const a = d / 180 * Math.PI * 2; DM.makeRotationX(Math.PI / 2); DM.setPosition(Math.cos(a) * 1.335, Math.sin(a) * 1.335, -.026); dots.setMatrixAt(d, DM); } vinyl.add(dots);
  const baseT = new THREE.Group(); baseT.position.set(1.36, 1.12, 0); vinyl.add(baseT);
  const plinth = cylZ(.3, .07, black, 64); plinth.position.z = -.04;
  const collar = cylZ(.21, .13, alu, 64); collar.position.z = .05;
  const gimbal = new THREE.Mesh(new THREE.TorusGeometry(.155, .024, 14, 64), chrome); gimbal.position.z = .2;
  const dial = cylZ(.09, .1, black); dial.position.set(.33, -.2, .0); const dialCap = cylZ(.062, .02, chrome); dialCap.position.set(.33, -.2, .058);
  const lever = rod(V(.33, -.44, -.02), V(.33, -.44, .1), .022, chrome), leverKnob = new THREE.Mesh(new THREE.SphereGeometry(.04, 16, 12), black); leverKnob.position.set(.33, -.44, .11);
  const restPost = rod(V(.17, -.8, -.04), V(.17, -.8, .13), .025, black), restClip = new THREE.Mesh(new THREE.TorusGeometry(.04, .012, 8, 20, Math.PI), black); restClip.position.set(.17, -.8, .16); restClip.rotation.x = Math.PI / 2;
  baseT.add(plinth, collar, gimbal, dial, dialCap, lever, leverKnob, restPost, restClip);
  const arm = new THREE.Group(); arm.position.set(1.36, 1.12, .2); vinyl.add(arm);          // moving parts, pivoting about z
  const yoke = new THREE.Mesh(new THREE.BoxGeometry(.13, .17, .1), chrome);
  const cw = new THREE.Mesh(new THREE.CylinderGeometry(.118, .118, .3, 48), black); cw.position.y = .5;
  const cwRing = new THREE.Mesh(new THREE.CylinderGeometry(.121, .121, .05, 48), chrome); cwRing.position.y = .335;
  const cwCap = new THREE.Mesh(new THREE.CylinderGeometry(.06, .06, .03, 32), chrome); cwCap.position.y = .665;
  const tube = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([V(0, -.06, 0), V(0, -.36, 0), V(.045, -.62, 0), V(.075, -.85, 0), V(.035, -1.05, 0), V(-.05, -1.2, 0)]), 64, .0215, 14), chrome);
  const head = new THREE.Group(); head.position.set(-.05, -1.2, 0); head.rotation.z = -.42;
  const lock = new THREE.Mesh(new THREE.CylinderGeometry(.031, .031, .075, 24), chrome); lock.position.y = -.025;
  const shell = new THREE.Mesh(new THREE.BoxGeometry(.135, .31, .014), black); shell.position.set(0, -.21, 0);
  const lift = rod(V(.055, -.09, 0), V(.23, -.15, .035), .009, chrome);
  const cart = new THREE.Mesh(new THREE.BoxGeometry(.108, .17, .08), new THREE.MeshStandardMaterial({ color: 0xf1f1ef, roughness: .35 })); cart.position.set(0, -.26, -.047);
  const cartFront = new THREE.Mesh(new THREE.BoxGeometry(.11, .035, .082), black); cartFront.position.set(0, -.345, -.047);
  const stylus = new THREE.Mesh(new THREE.ConeGeometry(.014, .05, 12), chrome); stylus.rotation.x = -Math.PI / 2; stylus.position.set(0, -.33, -.105);
  [-.035, .035].forEach((x) => { const sc = cylZ(.012, .01, chrome, 12); sc.position.set(x, -.2, .011); head.add(sc); });
  head.add(lock, shell, lift, cart, cartFront, stylus);
  arm.add(yoke, rod(V(0, .08, 0), V(0, .68, 0), .028, chrome), cw, cwRing, cwCap, tube, head);
  vinyl.add(hit(new THREE.CircleGeometry(1.45, 24), 'music')); shadow(vinyl);

  // ---- Right eye: bicycle wheel ----
  const wheel = new THREE.Group(); wheel.position.set(1.85, .85, 0); wheel.scale.setScalar(.95); wheel.userData.k = 'cycle'; face.add(wheel);
  const wspin = new THREE.Group(); wheel.add(wspin);
  // DT Swiss GRC 1100 style: deep carbon rim with decals, straight-pull spokes, hub, disc rotor, and a gravel tyre (tan sidewalls, chunky knobs on the outer tread only; the black shoulder is smooth).
  const carbon = new THREE.MeshPhysicalMaterial({ color: 0x0d0d0f, roughness: .4, clearcoat: .4, clearcoatRoughness: .28, side: THREE.DoubleSide });
  const blackMetal = new THREE.MeshStandardMaterial({ color: 0x131315, metalness: .85, roughness: .32 });
  const TR = 1.105, TT = .122, tg = new THREE.TorusGeometry(TR, TT, 32, 160);
  { const pos = tg.attributes.position, col = new Float32Array(pos.count * 3), tan = new THREE.Color(0xb28550), blk = new THREE.Color(0x141416);
    for (let i = 0; i < pos.count; i++) { const rho = Math.hypot(pos.getX(i), pos.getY(i)); (rho > TR + TT * .5 || rho < TR - TT * .8 ? blk : tan).toArray(col, i * 3); }
    tg.setAttribute('color', new THREE.BufferAttribute(col, 3)); }
  const tyre = new THREE.Mesh(tg, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: .92 })); wspin.add(tyre);
  const ROWS = [-17, 0, 17], PER = 60, knobs = new THREE.InstancedMesh(new THREE.BoxGeometry(.056, .064, .034), new THREE.MeshStandardMaterial({ color: 0x121214, roughness: .95 }), ROWS.length * PER);
  { const KM = new THREE.Matrix4(), qz = new THREE.Quaternion(), qy = new THREE.Quaternion(), Z = V(0, 0, 1), Y = V(0, 1, 0), one = V(1, 1, 1); let n = 0;
    ROWS.forEach((deg, row) => { const phi = deg * Math.PI / 180, rr = TR + (TT + .022) * Math.cos(phi), zz = (TT + .022) * Math.sin(phi);
      for (let k = 0; k < PER; k++) { const th = (k + (row % 2 ? .5 : 0)) / PER * Math.PI * 2; qz.setFromAxisAngle(Z, th); qy.setFromAxisAngle(Y, -phi);
        KM.compose(V(rr * Math.cos(th), rr * Math.sin(th), zz), qz.clone().multiply(qy), one); knobs.setMatrixAt(n++, KM); } }); }
  wspin.add(knobs);
  const prof = [[1.03, .094], [1.008, .108], [.97, .104], [.9, .07], [.832, .024], [.818, 0], [.832, -.024], [.9, -.07], [.97, -.104], [1.008, -.108], [1.03, -.094]].map(([r, h]) => new THREE.Vector2(r, h));
  const rim = new THREE.Mesh(new THREE.LatheGeometry(prof, 160), carbon); rim.rotation.x = Math.PI / 2; wspin.add(rim);
  const decalTex = (() => { const c = document.createElement('canvas'); c.width = 4096; c.height = 128; const g = c.getContext('2d'); g.fillStyle = '#fff'; g.textBaseline = 'middle';
    [['DT SWISS', .04, '900 italic 92px Arial, Helvetica, sans-serif'], ['GRC 1100', .2, '700 60px Arial, Helvetica, sans-serif'], ['DT SWISS', .54, '900 italic 92px Arial, Helvetica, sans-serif'], ['GRC 1100', .7, '700 60px Arial, Helvetica, sans-serif']].forEach(([t, x, f]) => { g.font = f; g.fillText(t, x * 4096, 66); });
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; })();
  const decal = new THREE.Mesh(new THREE.LatheGeometry([[.998, .1102], [.97, .107], [.905, .0756]].map(([r, h]) => new THREE.Vector2(r, h)), 160), new THREE.MeshStandardMaterial({ map: decalTex, transparent: true, alphaTest: .35, roughness: .5, side: THREE.DoubleSide })); decal.rotation.x = Math.PI / 2; wspin.add(decal);
  const hubBody = cylZ(.052, .5, blackMetal, 32), axle = cylZ(.03, .6, chrome, 24); wspin.add(hubBody, axle);
  for (const z of [-.14, .14]) { const f = cylZ(.105, .04, blackMetal, 40); f.position.z = z; wspin.add(f); }
  // Spokes get their own material: black in light mode, a little lighter in dark mode so they don't vanish against the dark page.
  const spokeMat = blackMetal.clone(), spokeTheme = () => { spokeMat.color.set(document.documentElement.dataset.theme === 'dark' ? 0x70737a : 0x131315); if (typeof kick === 'function') kick(); };
  spokeTheme(); new MutationObserver(spokeTheme).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  for (let i = 0; i < 24; i++) {                         // 24 straight-pull spokes, crossed, alternating flanges
    const a = i / 24 * Math.PI * 2, side = i % 2 ? 1 : -1, fa = a + (i % 4 < 2 ? .62 : -.62);
    wspin.add(rod(V(.095 * Math.cos(fa), .095 * Math.sin(fa), side * .14), V(.825 * Math.cos(a), .825 * Math.sin(a), 0), .0075, spokeMat));
  }
  const rotorMat = new THREE.MeshStandardMaterial({ color: 0xbfc3c9, metalness: 1, roughness: .28, side: THREE.DoubleSide });
  const rotor = new THREE.Group(); rotor.position.z = -.21; rotor.add(new THREE.Mesh(new THREE.RingGeometry(.31, .4, 72), rotorMat));
  for (let i = 0; i < 6; i++) { const arm2 = new THREE.Mesh(new THREE.BoxGeometry(.035, .25, .008), rotorMat); const a = i / 6 * Math.PI * 2; arm2.position.set(Math.cos(a) * .2, Math.sin(a) * .2, 0); arm2.rotation.z = a + Math.PI / 2 + .35; rotor.add(arm2); }
  rotor.add(new THREE.Mesh(new THREE.RingGeometry(.06, .11, 40), blackMetal)); wspin.add(rotor);
  const refl = new THREE.Mesh(new THREE.TorusGeometry(.056, .016, 14, 48), new THREE.MeshPhysicalMaterial({ color: SIGNAL, roughness: .25, clearcoat: 1 })); wspin.add(refl);   // the accent: a band on the hub and the valve cap
  wspin.add(rod(V(0, .825, 0), V(0, .735, 0), .012, blackMetal)); const cap = new THREE.Mesh(new THREE.CylinderGeometry(.016, .016, .04, 12), refl.material); cap.position.set(0, .725, 0); wspin.add(cap);
  wheel.add(hit(new THREE.CircleGeometry(1.4, 24), 'cycle')); shadow(wheel);

  // ---- Nose: a tree ----
  const tree = new THREE.Group(); tree.position.set(0, -1.6, .15); tree.userData.k = 'woods'; face.add(tree);
  const trunk = new THREE.Mesh(new THREE.CylinderGeometry(.05, .1, .62, 12), new THREE.MeshStandardMaterial({ color: 0x6a4a34, roughness: 1 })); trunk.position.y = .2; tree.add(trunk);
  const crown = new THREE.Group(); crown.position.y = .38; tree.add(crown);
  const leafGeo = new THREE.IcosahedronGeometry(1, 1), leafMat = new THREE.MeshStandardMaterial({ roughness: .85, flatShading: false });
  const COUNT = 260, leaves = new THREE.InstancedMesh(leafGeo, leafMat, COUNT), M = new THREE.Matrix4(), q = new THREE.Quaternion(), col = new THREE.Color();
  for (let i = 0; i < COUNT; i++) {
    const t = Math.pow(rnd(), .8), a = rnd() * Math.PI * 2, R = (.5 * Math.pow(1 - t, .85) + .04) * (.55 + .45 * Math.sqrt(rnd())), s = (.075 + .085 * rnd()) * (1 - .45 * t);
    q.setFromEuler(new THREE.Euler(rnd() * 3, rnd() * 3, rnd() * 3));
    M.compose(V(Math.cos(a) * R, t * 1.55, Math.sin(a) * R), q, V(s, s * (.75 + .5 * rnd()), s)); leaves.setMatrixAt(i, M);
    col.setHSL(.34 + .05 * (rnd() - .5), .5 + .2 * rnd(), .1 + .1 * rnd() + .05 * t); leaves.setColorAt(i, col);
  }
  leaves.instanceMatrix.needsUpdate = true; if (leaves.instanceColor) leaves.instanceColor.needsUpdate = true; crown.add(leaves);
  const th = hit(new THREE.PlaneGeometry(1.2, 2.2), 'woods'); th.position.y = 1.0; tree.add(th); shadow(tree);

  // ---- Smile: coffee beans (a stand-in until Matt picks) ----
  const smile = new THREE.Group(); smile.position.set(0, -2.35, .1); smile.userData.k = 'coffee'; face.add(smile);
  const beanMat = new THREE.MeshPhysicalMaterial({ color: 0x4d2c1a, roughness: .5, clearcoat: .25 }), slitMat = new THREE.MeshStandardMaterial({ color: 0x24120a, roughness: .8 });
  const beans = [];
  for (let i = 0; i < 7; i++) {
    const x = -1.5 + i * .5, y = -.5 + .22 * x * x, b = new THREE.Group();
    const body = new THREE.Mesh(new THREE.SphereGeometry(1, 28, 20), beanMat); body.scale.set(.2, .135, .1);
    const slit = new THREE.Mesh(new THREE.SphereGeometry(1, 16, 10), slitMat); slit.scale.set(.17, .014, .03); slit.position.z = .085;
    b.add(body, slit); b.position.set(x, y, 0); b.rotation.z = Math.atan(.44 * x); b.userData.y = y; smile.add(b); beans.push(b);
  }
  const sh = hit(new THREE.PlaneGeometry(3.6, 1.1), 'coffee'); sh.position.y = -.2; smile.add(sh); shadow(smile);

  // ---- What each piece opens ----
  const CARDS = {
    music: ['Music', 'The needle’s down. This loop is made in your browser; your playlist goes here.'],
    cycle: ['Cycling', 'Amsterdam by bike. A favourite route goes here.'],
    woods: ['The woods', 'I like to get out among the trees and explore.'],
    coffee: ['Coffee', 'The fuel. Your favourite roast goes here.'],
  };
  const show = (k) => { const [title, text] = CARDS[k]; pop.innerHTML = `<div class="face-card"><div><b>${title}</b><span>${text}</span></div></div>`; };

  let ac = null, stopMusic = null;                       // a small lo-fi loop made with Web Audio; starts only on click
  const playMusic = () => {
    ac = ac || new (window.AudioContext || window.webkitAudioContext)();
    const master = ac.createGain(), lp = ac.createBiquadFilter();
    master.gain.setValueAtTime(.0001, ac.currentTime); master.gain.exponentialRampToValueAtTime(.16, ac.currentTime + .4);
    lp.type = 'lowpass'; lp.frequency.value = 1300; lp.connect(master); master.connect(ac.destination);
    const chords = [[220, 261.63, 329.63], [174.61, 220, 261.63], [196, 246.94, 293.66], [164.81, 207.65, 246.94]]; let step = 0; const beat = 1.5;
    const tickA = () => { const now = ac.currentTime; chords[step++ % 4].forEach((f, i) => { const o = ac.createOscillator(), g = ac.createGain(); o.type = 'triangle'; o.frequency.value = f;
      g.gain.setValueAtTime(.0001, now + i * .09); g.gain.exponentialRampToValueAtTime(.2, now + i * .09 + .06); g.gain.exponentialRampToValueAtTime(.0001, now + beat * .95); o.connect(g).connect(lp); o.start(now + i * .09); o.stop(now + beat); }); };
    tickA(); const timer = setInterval(tickA, beat * 1000);
    stopMusic = () => { clearInterval(timer); master.gain.exponentialRampToValueAtTime(.0001, ac.currentTime + .3); setTimeout(() => master.disconnect(), 400); stopMusic = null; };
  };
  const activate = (k) => {
    show(k);
    if (k === 'music') { if (stopMusic) stopMusic(); else playMusic(); chips[0].setAttribute('aria-pressed', String(!!stopMusic)); }
    kick();
  };

  // ---- Pointer: hover by raycast, click to open ----
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(); let hover = null, chipHover = null, tapUntil = 0;
  const pick = (e) => {
    const r = stage.getBoundingClientRect(); ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera); const h = ray.intersectObjects(face.children, true).find((i) => i.object.userData.k); return h ? h.object.userData.k : null;
  };
  stage.addEventListener('pointermove', (e) => { if (e.pointerType === 'touch') return; hover = pick(e); stage.style.cursor = hover ? 'pointer' : ''; kick(); });
  stage.addEventListener('pointerleave', () => { hover = null; kick(); });
  stage.addEventListener('click', (e) => { const k = pick(e); if (!k) return; hover = k; tapUntil = performance.now() + 2500; activate(k); });
  chips.forEach((c) => {
    const k = c.dataset.k;
    c.addEventListener('pointerenter', () => { chipHover = k; kick(); }); c.addEventListener('pointerleave', () => { chipHover = null; kick(); });
    c.addEventListener('focus', () => { chipHover = k; kick(); }); c.addEventListener('blur', () => { chipHover = null; kick(); });
    c.addEventListener('click', () => activate(k));
  });
  if (matchMedia('(hover: none)').matches) pop.querySelector('.toy-hint').textContent = 'Tap the face';

  // ---- Motion ----
  let vSpin = 0, wSpin = 0, time0 = 0;
  const lerp = (a, b, k) => a + (b - a) * Math.min(1, k);
  onTick((time, dt) => {
    const on = (k) => hover === k || chipHover === k, music = on('music') || !!stopMusic, snap = reduce ? 1e9 : 1;
    chips.forEach((c) => c.classList.toggle('on', on(c.dataset.k) || (c.dataset.k === 'music' && !!stopMusic)));
    arm.rotation.z = lerp(arm.rotation.z, music ? -.43 : .1, dt * 5 * snap); arm.position.z = lerp(arm.position.z, music ? .1 : .2, dt * 5 * snap);
    if (!reduce) {
      vSpin = lerp(vSpin, music ? 3.49 : 0, dt * (music ? 2.5 : 1.4)); spinner.rotation.z -= vSpin * dt;      // 33⅓ rpm
      wSpin = lerp(wSpin, on('cycle') ? 11 : 0, dt * (on('cycle') ? 3 : .5)); wspin.rotation.z -= wSpin * dt; // keeps turning: inertia
      const sway = on('woods') ? 1 : .3; tree.rotation.z = Math.sin(time * .0017) * .045 * sway; crown.scale.setScalar(lerp(crown.scale.x, on('woods') ? 1.08 : 1, dt * 6));
      beans.forEach((b, i) => { b.position.y = b.userData.y + (on('coffee') ? Math.max(0, Math.sin(time * .008 - i * .8)) * .16 : 0); });
      const idle = time - ptr.at > 3000, gx = idle ? Math.sin(time * .0006) * .25 : ptr.x, gy = idle ? Math.cos(time * .0008) * .15 : ptr.y;
      face.rotation.y = lerp(face.rotation.y, gx * .42, dt * 4); face.rotation.x = lerp(face.rotation.x, gy * .3, dt * 4);
    }
    if (hover && time > tapUntil && matchMedia('(hover: none)').matches) hover = null;
  });
})();
