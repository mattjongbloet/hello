// 1 · Untangle, in 3D. One closed cord: a knot of harmonics far from the cursor, a clean ring up close.
// Idle: it slowly demonstrates itself. Touch: tap to toggle. Reduced motion: it rests as the ring.
(() => {
  const root = document.querySelector('.toy-untangle'); if (!root || !window.THREE) return;
  const stage = root.querySelector('.toy-stage'), hint = root.querySelector('.toy-hint');
  const { scene, ptr, reduce, onTick } = Toy3D.setup(stage, { z: 12 });
  const css = getComputedStyle(document.documentElement);
  const INK = new THREE.Color(css.getPropertyValue('--ink').trim() || '#15171a'), SIGNAL = new THREE.Color(css.getPropertyValue('--signal').trim() || '#ff5a1f');
  const N = 240, TAU = Math.PI * 2, R = 2.7;
  const K = [[1, .26, 0], [2, .21, 1.3], [3, .22, 2.1], [5, .19, .7], [7, .15, 4.2], [11, .11, 5.5], [16, .05, 2.9]];
  const group = new THREE.Group(); scene.add(group);
  const cordMat = new THREE.MeshPhysicalMaterial({ color: INK, roughness: .32, clearcoat: 1, clearcoatRoughness: .18 });
  const cord = new THREE.Mesh(new THREE.BufferGeometry(), cordMat); cord.castShadow = true; cord.receiveShadow = true; group.add(cord);
  const bead = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 24), new THREE.MeshPhysicalMaterial({ color: SIGNAL, roughness: .25, clearcoat: 1 })); bead.castShadow = true; group.add(bead);
  const ease = (v) => v * v * (3 - 2 * v);
  let t = reduce ? 1 : 0, goal = t, tapGoal = null, tapAt = -1e9;

  const build = (time) => {
    const e = ease(Math.max(0, Math.min(1, t))), pts = [];
    for (let i = 0; i < N; i++) {
      const s = (i / N) * TAU; let x = 0, y = 0, z = 0;
      for (const [f, a, p] of K) { x += a * Math.sin(f * s + p + time * .00016 * f); y += a * Math.cos(f * s + p * 1.9 - time * .00013 * f); z += a * Math.sin(f * s * 1.31 + p * .7 + time * .0001 * f); }
      const cx = .62 * Math.cos(s - Math.PI / 2), cy = -.62 * Math.sin(s - Math.PI / 2);
      pts.push(new THREE.Vector3(R * ((1 - e) * x + e * cx), R * ((1 - e) * y + e * cy), R * (1 - e) * z * .55));
    }
    cord.geometry.dispose();
    cord.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 420, .055 + .035 * e, 10, true);
    bead.position.copy(pts[0]); bead.scale.setScalar(.15 + .05 * e);
    const label = e > .93 ? 'Simple' : e < .12 ? 'Complex' : 'Simplifying';
    if (hint.textContent !== label) hint.textContent = label;
  };

  stage.addEventListener('pointerdown', (e) => { if (e.pointerType === 'mouse') return; tapGoal = t > .5 ? 0 : 1; tapAt = performance.now(); });
  onTick((time) => {
    if (reduce) { build(0); return; }
    if (time - tapAt < 6000 && tapGoal !== null) goal = tapGoal;                // touch: tap toggles
    else if (time - ptr.at < 3500 && ptr.px !== undefined) {                     // mouse: closer = simpler
      const r = stage.getBoundingClientRect(), d = Math.hypot(ptr.px - (r.left + r.width / 2), ptr.py - (r.top + r.height / 2));
      goal = 1 - Math.max(0, Math.min(1, (d - r.width * .42) / (r.width * 1.5)));
    } else goal = .5 - .5 * Math.cos(time * .00055);                             // idle: show what it does
    t += (goal - t) * .07;
    group.rotation.y += (ptr.x * .45 - group.rotation.y) * .08; group.rotation.x += (ptr.y * .3 - group.rotation.x) * .08;
    build(time);
  });
})();
