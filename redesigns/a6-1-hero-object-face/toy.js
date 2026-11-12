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
