(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const canvas = document.getElementById('live-chart');
  const ctx = canvas ? canvas.getContext('2d') : null;
  const eventRate = document.getElementById('event-rate');
  const eventChange = document.getElementById('event-change');
  const clock = document.getElementById('clock');
  const pauseButton = document.getElementById('pause-stream');
  let paused = false;
  let intervalId = null;
  let chartValues = [96, 103, 101, 115, 109, 121, 113, 118, 127, 121, 133, 129, 138, 124, 131, 143, 135, 128, 137, 145, 139, 148, 137, 141];
  let currentRate = 128;
  let prevRate = 123;

  function updateClock() {
    if (!clock) return;
    clock.textContent = new Intl.DateTimeFormat(undefined, {hour:'2-digit', minute:'2-digit', second:'2-digit', hour12:false}).format(new Date());
  }

  function drawChart() {
    if (!canvas || !ctx) return;
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    const rect = canvas.getBoundingClientRect();
    if (!rect.width || !rect.height) return;
    canvas.width = Math.round(rect.width * dpr);
    canvas.height = Math.round(rect.height * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const w = rect.width, h = rect.height;
    const pad = {left:4, right:5, top:8, bottom:9};
    const plotW = w - pad.left - pad.right;
    const plotH = h - pad.top - pad.bottom;
    const min = Math.min(...chartValues) - 14;
    const max = Math.max(...chartValues) + 12;
    const points = chartValues.map((v, i) => ({x:pad.left + (i / (chartValues.length - 1)) * plotW, y:pad.top + (1 - ((v - min) / (max - min))) * plotH}));
    ctx.clearRect(0, 0, w, h);
    ctx.save();
    ctx.beginPath();
    points.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, h);
    ctx.lineTo(points[0].x, h);
    ctx.closePath();
    const fill = ctx.createLinearGradient(0, 0, 0, h);
    fill.addColorStop(0, 'rgba(119,224,233,0.19)');
    fill.addColorStop(1, 'rgba(119,224,233,0.00)');
    ctx.fillStyle = fill;
    ctx.fill();
    ctx.restore();
    ctx.beginPath();
    points.forEach((p, i) => i ? ctx.lineTo(p.x, p.y) : ctx.moveTo(p.x, p.y));
    ctx.strokeStyle = '#77e0e9';
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    ctx.shadowColor = 'rgba(119,224,233,.28)';
    ctx.shadowBlur = 8;
    ctx.stroke();
    ctx.shadowBlur = 0;
    const last = points[points.length - 1];
    ctx.beginPath(); ctx.arc(last.x, last.y, 3.4, 0, Math.PI * 2); ctx.fillStyle = '#b8f278'; ctx.fill();
  }

  function tickStream() {
    if (paused) return;
    prevRate = currentRate;
    currentRate = Math.max(88, Math.min(164, currentRate + Math.round(Math.random() * 16 - 7)));
    chartValues.push(currentRate);
    if (chartValues.length > 24) chartValues.shift();
    if (eventRate) eventRate.textContent = currentRate;
    if (eventChange) {
      const pct = prevRate ? ((currentRate - prevRate) / prevRate) * 100 : 0;
      const sign = pct > 0 ? '+' : '';
      eventChange.innerHTML = `${sign}${pct.toFixed(1)}% <i>${pct >= 0 ? '↗' : '↘'}</i>`;
      eventChange.style.color = pct >= 0 ? '#b8f278' : '#ffc27b';
    }
    drawChart();
    updateClock();
  }

  function startStream() {
    if (intervalId) window.clearInterval(intervalId);
    intervalId = window.setInterval(tickStream, 3000);
  }

  if (canvas) {
    window.addEventListener('resize', drawChart, {passive:true});
    if (typeof ResizeObserver !== 'undefined') new ResizeObserver(drawChart).observe(canvas);
    drawChart(); updateClock(); startStream();
  }
  if (pauseButton) {
    pauseButton.addEventListener('click', () => {
      paused = !paused;
      pauseButton.setAttribute('aria-pressed', String(paused));
      pauseButton.textContent = paused ? 'Resume stream' : 'Pause stream';
      const label = document.querySelector('.chart-live-label');
      if (label) label.innerHTML = paused ? 'Ⅱ PAUSED' : '<span class="pulse-dot"></span> STREAMING';
    });
  }
  if (reducedMotion) {
    paused = true;
    if (pauseButton) { pauseButton.textContent = 'Resume stream'; pauseButton.setAttribute('aria-pressed', 'true'); }
  }

  // Accessible, text-aware project filters.
  const filterButtons = Array.from(document.querySelectorAll('.filter-button'));
  const cards = Array.from(document.querySelectorAll('.project-card'));
  const searchInput = document.getElementById('project-search');
  const status = document.getElementById('filter-status');
  const emptyState = document.getElementById('empty-state');
  let activeFilter = 'all';
  function applyFilters() {
    const query = (searchInput?.value || '').trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const matchesCategory = activeFilter === 'all' || card.dataset.category === activeFilter;
      const searchable = `${card.dataset.search || ''} ${card.textContent || ''}`.toLowerCase();
      const matchesText = !query || searchable.includes(query);
      const show = matchesCategory && matchesText;
      card.hidden = !show;
      if (show) visible++;
    });
    if (status) status.textContent = `Showing ${visible} of ${cards.length} projects${query ? ` for “${query}”` : ''}.`;
    if (emptyState) emptyState.hidden = visible !== 0;
  }
  filterButtons.forEach(btn => btn.addEventListener('click', () => {
    activeFilter = btn.dataset.filter || 'all';
    filterButtons.forEach(other => {
      const active = other === btn;
      other.classList.toggle('active', active);
      other.setAttribute('aria-pressed', String(active));
    });
    applyFilters();
  }));
  if (searchInput) searchInput.addEventListener('input', applyFilters);

  // Mobile navigation menu.
  const menuToggle = document.getElementById('menu-toggle');
  const nav = document.getElementById('primary-nav');
  if (menuToggle && nav) {
    menuToggle.addEventListener('click', () => {
      const open = !nav.classList.contains('open');
      nav.classList.toggle('open', open);
      menuToggle.setAttribute('aria-expanded', String(open));
      menuToggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      menuToggle.textContent = open ? '✕' : '☰';
    });
    nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
      nav.classList.remove('open'); menuToggle.setAttribute('aria-expanded','false');
      menuToggle.setAttribute('aria-label','Open navigation'); menuToggle.textContent = '☰';
    }));
  }

  const copyButton = document.getElementById('copy-email');
  const copyStatus = document.getElementById('copy-status');
  if (copyButton) copyButton.addEventListener('click', async () => {
    const email = 'salakooluwaseunayo@gmail.com';
    try {
      await navigator.clipboard.writeText(email);
      copyButton.textContent = 'Copied';
      if (copyStatus) copyStatus.textContent = 'Email address copied to clipboard.';
    } catch (_) {
      window.location.href = `mailto:${email}`;
      if (copyStatus) copyStatus.textContent = 'Opened your email application instead.';
    }
    window.setTimeout(() => { copyButton.textContent = 'Copy email'; }, 1800);
  });

  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
