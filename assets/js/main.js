(() => {
  const root = document.documentElement;
  const theme = document.querySelector('#theme-toggle');
  const menu = document.querySelector('#menu-toggle');
  const nav = document.querySelector('#nav-links');
  const system = matchMedia('(prefers-color-scheme: dark)');
  let selected;
  try { selected = localStorage.getItem('htm-theme'); } catch {}
  function setTheme(value) {
    root.dataset.theme = value;
    theme.setAttribute('aria-pressed', String(value === 'dark'));
    theme.textContent = value === 'dark' ? '☀' : '☾';
    document.querySelector('meta[name="theme-color"]').content = value === 'dark' ? '#201929' : '#24559a';
  }
  setTheme(selected || (system.matches ? 'dark' : 'light'));
  system.addEventListener('change', e => { if (!selected) setTheme(e.matches ? 'dark' : 'light'); });
  theme.addEventListener('click', () => {
    selected = root.dataset.theme === 'dark' ? 'light' : 'dark';
    setTheme(selected);
    try { localStorage.setItem('htm-theme', selected); } catch {}
  });
  function setMenu(open) {
    nav.classList.toggle('open', open);
    menu.setAttribute('aria-expanded', String(open));
  }
  menu.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && nav.classList.contains('open')) {
      setMenu(false);
      menu.focus();
    }
  });
  const backTop = document.querySelector('.back-top');
  function updateBackTop() {
    backTop.hidden = window.scrollY < window.innerHeight * 0.75;
  }
  window.addEventListener('scroll', updateBackTop, { passive: true });
  window.addEventListener('resize', updateBackTop);
  updateBackTop();

  const overflowObserver = new ResizeObserver(entries => {
    for (const entry of entries) entry.target.dispatchEvent(new Event('check-overflow'));
  });
  for (const region of document.querySelectorAll('.table-scroll, .code-sample')) {
    const slider = document.createElement('input');
    const name = region.getAttribute('aria-label') ||
      region.closest('.code-wrap').querySelector('.code-label').textContent;
    slider.type = 'range';
    slider.className = 'horizontal-slider';
    slider.min = '0';
    slider.setAttribute('aria-label', 'Scroll horizontally: ' + name);
    region.after(slider);

    function syncSlider() {
      const max = region.scrollWidth - region.clientWidth;
      slider.max = String(max);
      slider.value = String(Math.round(region.scrollLeft));
      slider.hidden = max <= 0;
    }
    slider.addEventListener('input', () => { region.scrollLeft = slider.valueAsNumber; });
    region.addEventListener('scroll', syncSlider, { passive: true });
    region.addEventListener('check-overflow', syncSlider);
    overflowObserver.observe(region);
    syncSlider();
  }

  const box = document.querySelector('dialog');
  const full = box.querySelector('img');
  const title = box.querySelector('#image-title');
  const position = box.querySelector('#image-position');
  const original = box.querySelector('#image-original');
  const previous = box.querySelector('#previous-image');
  const next = box.querySelector('#next-image');
  const controls = document.querySelector('#gallery-controls');
  const search = document.querySelector('#gallery-search');
  const filters = [...controls.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('.site-gallery figure')];
  const links = [...document.querySelectorAll('.site-gallery a')];
  let opener;
  let visible = links;
  let category = 'all';
  let current = 0;

  function filterGallery() {
    const terms = search.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    visible = [];
    for (const card of cards) {
      const topic = card.dataset.category;
      const text = (topic + ' ' + card.textContent).toLowerCase();
      card.hidden = (category !== 'all' && category !== topic) ||
        !terms.every(term => text.includes(term));
      if (!card.hidden) visible.push(card.querySelector('a'));
    }
    document.querySelector('#gallery-count').textContent = visible.length
      ? `${visible.length} of ${links.length} screenshots`
      : 'No screenshots match your search.';
  }

  controls.hidden = false;
  search.addEventListener('input', filterGallery);
  for (const button of filters) {
    button.addEventListener('click', () => {
      category = button.dataset.filter;
      for (const filter of filters) filter.setAttribute('aria-pressed', String(filter === button));
      filterGallery();
    });
  }
  filterGallery();

  function showImage(index) {
    current = (index + visible.length) % visible.length;
    const link = visible[current];
    full.src = link.href;
    full.alt = link.querySelector('img').alt;
    title.textContent = link.dataset.title;
    original.href = link.href;
    position.textContent = `${current + 1} of ${visible.length}`;
    previous.disabled = next.disabled = visible.length < 2;
  }

  for (const link of links) {
    link.addEventListener('click', e => {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || !box.showModal) return;
      e.preventDefault();
      opener = link;
      showImage(visible.indexOf(link));
      box.showModal();
    });
  }
  previous.addEventListener('click', () => showImage(current - 1));
  next.addEventListener('click', () => showImage(current + 1));
  box.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    showImage(current + (event.key === 'ArrowLeft' ? -1 : 1));
  });
  box.addEventListener('click', e => { if (e.target === box) box.close(); });
  box.addEventListener('close', () => opener?.focus());

  if (navigator.clipboard?.writeText) {
    for (const button of document.querySelectorAll('.code-bar .copy')) {
      let reset;
      button.hidden = false;
      button.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(button.closest('.code-wrap').querySelector('code').textContent);
          button.textContent = 'Copied';
        } catch {
          button.textContent = 'Copy unavailable';
        }
        clearTimeout(reset);
        reset = setTimeout(() => { button.textContent = 'Copy'; }, 1800);
      });
    }
  }
})();
