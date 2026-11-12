// Shared 3D setup for the hero toys (three.js r160, loaded as a classic script so pages also work from file://).
// Physically based materials, a small generated studio for reflections, one key light with soft shadows on an invisible wall.
window.Toy3D = (() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function studio(renderer) {                       // a tiny light room, baked into an environment map
    const s = new THREE.Scene();
    s.add(new THREE.Mesh(new THREE.BoxGeometry(24, 24, 24), new THREE.MeshBasicMaterial({ color: 0x25262a, side: THREE.BackSide })));
    const panel = (i, x, y, z, w, h, c = 0xffffff) => {
      const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(c).multiplyScalar(i), side: THREE.DoubleSide }));
      m.position.set(x, y, z); m.lookAt(0, 0, 0); s.add(m);
    };
    panel(4.2, 0, 11, 2, 12, 10); panel(2.6, -11, 3, 5, 8, 7); panel(2, 11, 4, 3, 6, 7, 0xffe9d6); panel(1.3, 0, 1, 11.5, 14, 6); panel(.7, 0, -11, 3, 12, 8);
    const pm = new THREE.PMREMGenerator(renderer), tex = pm.fromScene(s, .03).texture; pm.dispose(); return tex;
  }

  function setup(stage, { fov = 30, z = 12 } = {}) {
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1;
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    stage.appendChild(renderer.domElement);
    const scene = new THREE.Scene(); scene.environment = studio(renderer);
    const camera = new THREE.PerspectiveCamera(fov, 1, .1, 100); camera.position.set(0, 0, z);
    const key = new THREE.DirectionalLight(0xffffff, 1.9); key.position.set(-2.4, 4, 10); key.castShadow = true;
    key.shadow.mapSize.set(1024, 1024); key.shadow.bias = -.0005; key.shadow.normalBias = .02;
    Object.assign(key.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 1, far: 30 });
    scene.add(key, new THREE.AmbientLight(0xffffff, .12));
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.ShadowMaterial({ opacity: .11 }));
    wall.position.z = -.55; wall.receiveShadow = true; scene.add(wall);
    const resize = () => { const r = stage.getBoundingClientRect(); renderer.setSize(Math.max(1, r.width), Math.max(1, r.height), false); camera.aspect = r.width / Math.max(1, r.height); camera.updateProjectionMatrix(); };
    resize(); addEventListener('resize', resize);

    // pointer, normalised to -1..1 around the stage centre
    const ptr = { x: 0, y: 0, at: -1e9 };
    addEventListener('pointermove', (e) => {
      if (e.pointerType === 'touch') return;
      const r = stage.getBoundingClientRect();
      ptr.x = Math.max(-1, Math.min(1, (e.clientX - (r.left + r.width / 2)) / (innerWidth * .5)));
      ptr.y = Math.max(-1, Math.min(1, (e.clientY - (r.top + r.height / 2)) / (innerHeight * .5)));
      ptr.px = e.clientX; ptr.py = e.clientY; ptr.at = performance.now();
    }, { passive: true });

    // render loop: only while on screen; one frame at a time when motion is reduced
    let visible = true, raf = null, lastT = 0, tick = () => {};
    const frame = (t) => { raf = null; if (!visible) return; const dt = Math.min(.05, (t - lastT) / 1000 || .016); lastT = t; tick(t, dt); renderer.render(scene, camera); if (!reduce) raf = requestAnimationFrame(frame); };
    const kick = () => { if (!raf && visible) raf = requestAnimationFrame(frame); };
    new IntersectionObserver(([en]) => { visible = en.isIntersecting; kick(); }).observe(stage);
    return { renderer, scene, camera, ptr, reduce, kick, onTick: (f) => { tick = f; kick(); } };
  }

  const shadow = (o) => { o.traverse((m) => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } }); return o; };
  function rod(a, b, r, mat) {                      // a thin cylinder between two points
    const d = new THREE.Vector3().subVectors(b, a), m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, d.length(), 8), mat);
    m.position.copy(a).addScaledVector(d, .5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.clone().normalize()); return m;
  }
  return { setup, shadow, rod, reduce };
})();

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
    g.fillStyle = '#fff'; g.textAlign = 'center'; g.font = '700 92px system-ui, sans-serif'; g.fillText('MJ', S / 2, S * .36);
    g.font = '600 34px system-ui, sans-serif'; g.fillText('SIDE A · 33⅓', S / 2, S * .76);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
  })();
  const spinner = new THREE.Group(); vinyl.add(spinner);
  const blackVinyl = new THREE.MeshPhysicalMaterial({ color: 0x050506, roughness: .42, metalness: .15, anisotropy: 1, anisotropyMap: aniso, normalMap: grooves, normalScale: new THREE.Vector2(.5, .5), envMapIntensity: 1.25 });
  const edge = new THREE.MeshPhysicalMaterial({ color: 0x08080a, roughness: .35 });
  const disc = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, .045, 128), [edge, blackVinyl, edge]); disc.rotation.x = Math.PI / 2; spinner.add(disc);
  const lab = new THREE.Mesh(new THREE.CylinderGeometry(.44, .44, .05, 64), [edge, new THREE.MeshStandardMaterial({ map: label, roughness: .75 }), edge]); lab.rotation.x = Math.PI / 2; lab.position.z = .004; spinner.add(lab);
  const spindle = new THREE.Mesh(new THREE.CylinderGeometry(.035, .035, .16, 24), steel); spindle.rotation.x = Math.PI / 2; spindle.position.z = .06; vinyl.add(spindle);
  const arm = new THREE.Group(); arm.position.set(1.36, 1.12, .2); vinyl.add(arm);          // tonearm, pivoting about z
  const base = new THREE.Mesh(new THREE.CylinderGeometry(.15, .17, .14, 32), alu); base.rotation.x = Math.PI / 2; base.position.z = -.12;
  const weight = new THREE.Mesh(new THREE.CylinderGeometry(.085, .085, .2, 24), new THREE.MeshStandardMaterial({ color: 0x2b2d33, metalness: .9, roughness: .35 })); weight.position.set(0, .26, 0);
  const shell = new THREE.Mesh(new THREE.BoxGeometry(.13, .24, .05), new THREE.MeshStandardMaterial({ color: 0x1c1d21, roughness: .5, metalness: .2 })); shell.position.set(0, -1.3, 0);
  const stylus = new THREE.Mesh(new THREE.ConeGeometry(.02, .07, 12), steel); stylus.rotation.x = -Math.PI / 2; stylus.position.set(0, -1.38, -.05);
  arm.add(rod(V(0, .34, 0), V(0, -1.2, 0), .022, steel), weight, shell, stylus); vinyl.add(base); base.position.add(arm.position).setZ(.06);
  vinyl.add(hit(new THREE.CircleGeometry(1.45, 24), 'music')); shadow(vinyl);

  // ---- Right eye: bicycle wheel ----
  const wheel = new THREE.Group(); wheel.position.set(1.85, .85, 0); wheel.scale.setScalar(.95); wheel.userData.k = 'cycle'; face.add(wheel);
  const wspin = new THREE.Group(); wheel.add(wspin);
  const tyre = new THREE.Mesh(new THREE.TorusGeometry(1.2, .105, 24, 120), new THREE.MeshStandardMaterial({ color: 0x141416, roughness: .92 }));
  const rim = new THREE.Mesh(new THREE.TorusGeometry(1.075, .05, 16, 120), alu); rim.scale.z = 1.9;
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(.075, .075, .44, 24), alu); hub.rotation.x = Math.PI / 2;
  wspin.add(tyre, rim, hub);
  for (const z of [-.16, .16]) { const f = new THREE.Mesh(new THREE.CylinderGeometry(.16, .16, .025, 32), steel); f.rotation.x = Math.PI / 2; f.position.z = z; wspin.add(f); }
  for (let i = 0; i < 28; i++) {                         // spokes, laced alternately to each flange
    const a = i / 28 * Math.PI * 2, side = i % 2 ? 1 : -1, fa = a + side * 1.05 * (i % 4 < 2 ? 1 : -1);
    wspin.add(rod(V(.15 * Math.cos(fa), .15 * Math.sin(fa), side * .16), V(1.04 * Math.cos(a), 1.04 * Math.sin(a), 0), .0085, steel));
  }
  const valve = new THREE.Mesh(new THREE.CylinderGeometry(.018, .018, .16, 10), new THREE.MeshStandardMaterial({ color: 0xb08d57, metalness: 1, roughness: .3 })); valve.position.set(0, .97, 0); wspin.add(valve);
  const refl = new THREE.Mesh(new THREE.BoxGeometry(.2, .08, .03), new THREE.MeshPhysicalMaterial({ color: SIGNAL, roughness: .2, clearcoat: 1 })); refl.position.set(0, -.62, 0); wspin.add(refl);
  wheel.add(hit(new THREE.CircleGeometry(1.4, 24), 'cycle')); shadow(wheel);


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
  choose('mouth', 'swatches'); choose('nose', 'cursor');   // the pair Matt is trying

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
    if (k === 'nose' && noses[nose].click) noses[nose].click(h.object); if (k === 'mouth' && mouths[mouth].click) mouths[mouth].click(h.object); kick(); });

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
