// A small shell: type a command (or tap one) and it runs. Navigation commands open the matching page.
(() => {
  const form = document.getElementById('prompt'), input = document.getElementById('cmd'), out = document.getElementById('history');
  if (!form) return;
  const CV = 'https://cdn.prod.website-files.com/63b35214bc1dc0317e22bd99/668ae1b79c5572bfad32e508_Matt_Jongbloet_CV_2024.pdf';
  const go = (href) => () => { location.href = href; return 'Opening ' + href + ' …'; };
  const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
  const cmds = {
    help: () => 'Commands:\n  <span class="k">whoami</span>       who this is\n  <span class="k">ls</span>           list work\n  <span class="k">open pmi</span>     PMI case study (man page)\n  <span class="k">about</span>        my story\n  <span class="k">impact</span>       numbers\n  <span class="k">contact</span>      how to reach me\n  <span class="k">cv</span>           download CV (PDF)\n  <span class="k">home</span>         back to the start\n  <span class="k">clear</span>        clear this session',
    whoami: () => 'Matt Jongbloet — <b>Senior Staff Product Designer</b> @ Hospitable · Amsterdam, NL',
    ls: () => 'pmi/  home-search/  internal-admin/  scaling-research/  home-value-estimates/  digital-health/  location-game/\n<span class="mut">Try: open pmi</span>',
    impact: () => '<span class="k">"pmi_potential_savings_per_month"</span>: <span class="y">"≈$200M"</span>\n<span class="k">"home_search_people_helped"</span>: <span class="y">"≈10M"</span>\n<span class="k">"internal_admin_time_saved"</span>: <span class="y">"≈80%"</span>\n<span class="k">"product_people_empowered"</span>: <span class="y">"30+"</span>',
    contact: () => 'Email: <a href="mailto:matthewjongbloet@gmail.com">matthewjongbloet@gmail.com</a>',
    cv: () => { window.open(CV, '_blank', 'noopener'); return 'CV: <a href="' + CV + '">' + 'Matt_Jongbloet_CV.pdf</a>'; },
    'open pmi': go('case-pmi.html'), 'man pmi': go('case-pmi.html'), pmi: go('case-pmi.html'),
    about: go('about.html'), 'cat about.md': go('about.html'),
    home: go('index.html'), 'cd ~': go('index.html'), cd: go('index.html'),
    sudo: () => 'Nice try. Hiring is the only privilege escalation I accept: <a href="mailto:matthewjongbloet@gmail.com">email me</a>.',
  };
  const ext = { 'open home-search': 'https://www.mjongbloet.com/portfolio/home-search', 'open internal-admin': 'https://www.mjongbloet.com/portfolio/internal-admin' };
  const hist = []; let hi = 0;
  const run = (raw) => {
    const c = raw.trim().replace(/\s+/g, ' ').toLowerCase();
    if (!c) return;
    hist.push(raw); hi = hist.length;
    if (c === 'clear') { out.innerHTML = ''; return; }
    let res;
    if (cmds[c]) res = cmds[c]();
    else if (ext[c]) { location.href = ext[c]; res = 'Opening ' + ext[c] + ' …'; }
    else if (c.startsWith('open ')) res = 'Full write-up lives on <a href="https://www.mjongbloet.com/portfolio">mjongbloet.com/portfolio</a>. Only <span class="k">open pmi</span> is local.';
    else res = 'zsh: command not found: ' + esc(c) + '\n<span class="mut">Type</span> <span class="k">help</span> <span class="mut">for commands.</span>';
    const div = document.createElement('div'); div.className = 'block';
    div.innerHTML = '<p class="cmd"><span class="ps">matt@portfolio<span class="p">:~$</span></span><span>' + esc(raw) + '</span></p><pre class="out">' + res + '</pre>';
    out.appendChild(div);
    form.scrollIntoView({ block: 'end' });
  };
  form.addEventListener('submit', (e) => { e.preventDefault(); run(input.value); input.value = ''; });
  input.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowUp' && hi > 0) { hi--; input.value = hist[hi]; e.preventDefault(); }
    else if (e.key === 'ArrowDown') { hi = Math.min(hist.length, hi + 1); input.value = hist[hi] || ''; e.preventDefault(); }
    else if (e.key === 'Tab') {
      const m = Object.keys(cmds).find((k) => input.value && k.startsWith(input.value.toLowerCase()));
      if (m) { input.value = m; e.preventDefault(); }
    }
  });
  const fine = matchMedia('(pointer: fine)').matches;
  document.querySelectorAll('[data-run]').forEach((b) => b.addEventListener('click', () => { run(b.dataset.run); if (fine) input.focus(); }));
  // Typing anywhere focuses the prompt
  addEventListener('keydown', (e) => {
    if (e.target === input || e.metaKey || e.ctrlKey || e.altKey || e.key.length !== 1 || e.target.closest('input, textarea')) return;
    if (e.key === ' ' && e.target.closest('button, a')) return; // let Space activate the focused control
    input.focus();
  });
})();
