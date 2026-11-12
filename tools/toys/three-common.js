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
