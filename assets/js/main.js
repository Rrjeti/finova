/* Finova — interactions & scroll animations (no dependencies) */
(function () {
  'use strict';
  var d = document, w = window, root = d.documentElement;
  var $ = function (s, c) { return (c || d).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || d).querySelectorAll(s)); };

  /* ---------- split headings into words ---------- */
  $$('[data-split]').forEach(function (el) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(part)); return; }
            var o = d.createElement('span'), inner = d.createElement('span');
            o.className = 'w'; inner.textContent = part; inner.style.setProperty('--i', i++);
            o.appendChild(inner); frag.appendChild(o);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') { walk(n); }
      });
    })(el);
    if (!el.hasAttribute('aria-label')) el.setAttribute('aria-label', el.textContent.replace(/\s+/g, ' ').trim());
  });

  /* ---------- staggered children ---------- */
  $$('[data-stagger]').forEach(function (p) {
    var step = parseFloat(p.getAttribute('data-stagger')) || 0.1;
    $$(':scope > [data-reveal]', p).forEach(function (c, i) { c.style.setProperty('--d', (i * step).toFixed(2) + 's'); });
  });

  /* ---------- reveal on scroll ---------- */
  var revealEls = $$('[data-reveal],[data-split],.ring,[data-count]');
  function reveal(el) {
    el.classList.add('is-in');
    if (el.hasAttribute('data-count')) count(el);
    $$('[data-count]', el).forEach(count);
  }
  /* Position-based check (works even with clip-path masks, where
     IntersectionObserver reports zero visible area). */
  var pending = revealEls.slice();
  function checkReveal() {
    if (!pending.length) return;
    var vh = w.innerHeight;
    pending = pending.filter(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < vh * 0.9 && r.bottom > 0) { reveal(el); return false; }
      if (r.bottom <= 0) { reveal(el); return false; } /* already scrolled past (e.g. anchor jump) */
      return true;
    });
  }
  w.addEventListener('load', checkReveal);

  /* ---------- counters ---------- */
  function fmt(n) { return n.toLocaleString('en-US'); }
  function count(el) {
    if (el._counted) return; el._counted = true;
    var to = +el.getAttribute('data-count'), t0 = performance.now(), dur = 1800;
    (function tick(t) {
      var k = Math.min(1, (t - t0) / dur);
      el.textContent = fmt(Math.round(to * (1 - Math.pow(1 - k, 4))));
      if (k < 1) requestAnimationFrame(tick);
    })(t0);
  }

  /* ---------- header, progress, parallax, scroll-linked ---------- */
  var header = $('.site-header'), bar = $('.progress'), toTop = $('.to-top'), mbar = $('.mbar');
  var parallax = $$('[data-parallax]');
  var tracks = $$('[data-progress]');
  var lastY = w.scrollY, ticking = false;

  function onScroll() {
    var y = w.scrollY, h = root.scrollHeight - w.innerHeight, vh = w.innerHeight;
    if (bar) bar.style.setProperty('--sp', h > 0 ? (y / h).toFixed(4) : 0);
    if (header) {
      header.classList.toggle('scrolled', y > 30);
      header.classList.toggle('hide', y > 500 && y > lastY + 4 && !root.classList.contains('menu-open'));
      if (y < lastY - 4) header.classList.remove('hide');
    }
    if (toTop) toTop.classList.toggle('show', y > vh * 1.2);
    if (mbar) mbar.classList.toggle('show', y > vh * 0.6);
    parallax.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var speed = parseFloat(el.getAttribute('data-parallax')) || 0.15;
      var off = (r.top + r.height / 2 - vh / 2) * -speed;
      el.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
    });
    tracks.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, (vh * 0.75 - r.top) / (r.height || 1)));
      el.style.setProperty('--p', p.toFixed(3));
      var kids = $$('[data-step]', el), n = kids.length;
      kids.forEach(function (k, i) { k.classList.toggle('lit', p >= (n > 1 ? i / (n - 1) : 0) * 0.98 - 0.02 && p > 0.02); });
      if (el.hasAttribute('data-fill')) el.style.setProperty('--fill', Math.round(p * 140) + '%');
    });
    checkReveal();
    lastY = y; ticking = false;
  }
  w.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  w.addEventListener('resize', onScroll);
  onScroll();

  if (toTop) toTop.addEventListener('click', function () { w.scrollTo({ top: 0, behavior: 'smooth' }); });

  /* ---------- mobile menu ---------- */
  var btn = $('.menu-btn'), drawer = $('.drawer');
  function setMenu(open) {
    root.classList.toggle('menu-open', open);
    if (btn) { btn.setAttribute('aria-expanded', open); btn.setAttribute('aria-label', open ? 'Mbyll menunë' : 'Hap menunë'); }
    if (drawer) drawer.setAttribute('aria-hidden', !open);
    if (drawer && 'inert' in drawer) drawer.inert = !open;
  }
  if (btn) {
    setMenu(false);
    btn.addEventListener('click', function () { setMenu(!root.classList.contains('menu-open')); });
    $$('a', drawer).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    w.addEventListener('resize', function () { if (w.innerWidth > 1080) setMenu(false); });
  }

  /* ---------- 3D tilt on pointer devices ---------- */
  if (w.matchMedia('(hover:hover) and (pointer:fine)').matches) {
    $$('[data-tilt]').forEach(function (el) {
      var max = parseFloat(el.getAttribute('data-tilt')) || 8;
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'perspective(900px) rotateY(' + (x * max) + 'deg) rotateX(' + (-y * max) + 'deg)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
    /* hero scene follows the mouse */
    var scene = $('.scene');
    if (scene) {
      var hero = scene.closest('.hero');
      hero.addEventListener('pointermove', function (e) {
        var x = e.clientX / w.innerWidth - 0.5, y = e.clientY / w.innerHeight - 0.5;
        $$('[data-depth]', scene).forEach(function (el) {
          var z = parseFloat(el.getAttribute('data-depth'));
          el.style.transform = 'translate3d(' + (x * z * 40) + 'px,' + (y * z * 40) + 'px,0)';
        });
      });
    }
  }

  /* ---------- tax-deadline countdown ---------- */
  $$('[data-deadline-day]').forEach(function (el) {
    var day = +el.getAttribute('data-deadline-day');
    var now = new Date(), target = new Date(now.getFullYear(), now.getMonth(), day, 23, 59);
    if (target < now) target = new Date(now.getFullYear(), now.getMonth() + 1, day, 23, 59);
    var days = Math.ceil((target - now) / 864e5);
    var out = $('b', el); if (out) out.textContent = days + (days === 1 ? ' ditë' : ' ditë');
    var dt = $('[data-deadline-date]', el);
    if (dt) dt.textContent = String(day).padStart(2, '0') + '.' + String(target.getMonth() + 1).padStart(2, '0');
  });

  /* ---------- opening hours: open now? ---------- */
  var hours = $('[data-hours]');
  if (hours) {
    var now = new Date(), wd = now.getDay(), mins = now.getHours() * 60 + now.getMinutes();
    var sched = { 1: [480, 990], 2: [480, 990], 3: [480, 990], 4: [480, 990], 5: [480, 990], 6: [540, 780] };
    var row = $('[data-day~="' + wd + '"]', hours); if (row) row.classList.add('today');
    var s = sched[wd], open = s && mins >= s[0] && mins < s[1];
    var badge = $('.open-now');
    if (badge) { badge.classList.toggle('closed', !open); $('span', badge).textContent = open ? 'Hapur tani' : 'Mbyllur tani'; }
  }

  /* ---------- click-to-load map (faster + privacy friendly) ---------- */
  $$('.map-cover').forEach(function (b) {
    b.addEventListener('click', function () {
      var f = d.createElement('iframe');
      f.src = b.getAttribute('data-src'); f.title = 'Harta e zyrës Finova'; f.loading = 'lazy';
      f.referrerPolicy = 'no-referrer-when-downgrade'; f.allowFullscreen = true;
      b.replaceWith(f);
    });
  });

  /* ---------- contact form ---------- */
  var form = $('#contact-form');
  if (form) {
    var done = $('#form-done');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      if (form.website && form.website.value) return; // honeypot
      var data = new FormData(form), endpoint = form.getAttribute('data-endpoint');
      var sendBtn = $('button[type=submit]', form);
      var ok = function () { form.hidden = true; done.hidden = false; done.focus(); };
      if (endpoint) {
        sendBtn.disabled = true; sendBtn.firstChild.textContent = 'Duke dërguar… ';
        fetch(endpoint, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) { if (!r.ok) throw 0; ok(); form.reset(); })
          .catch(function () { alert('Mesazhi nuk u dërgua. Ju lutem na shkruani në info@finova-ks.com ose na telefononi.'); })
          .finally(function () { sendBtn.disabled = false; sendBtn.firstChild.textContent = 'Dërgo mesazhin '; });
      } else {
        /* no form service configured yet: open the visitor's email app with the message filled in */
        var topic = data.getAll('topic').join(', ') || 'Pyetje';
        var body = 'Emri: ' + data.get('name') + '\nKompania: ' + (data.get('company') || '-') + '\nEmail: ' + data.get('email') +
          '\nTelefoni: ' + (data.get('phone') || '-') + '\nShërbimi: ' + topic + '\n\n' + data.get('message');
        w.location.href = 'mailto:info@finova-ks.com?subject=' + encodeURIComponent('Kërkesë nga uebfaqja: ' + topic) + '&body=' + encodeURIComponent(body);
        ok();
      }
    });
    var again = $('[data-action=reset]');
    if (again) again.addEventListener('click', function () { done.hidden = true; form.hidden = false; });
  }

  /* ---------- preselect service from ?sherbimi= ---------- */
  var q = (w.location.search.match(/sherbimi=([a-z]+)/) || [])[1];
  var map = { auditim: 'Auditim', kontabilitet: 'Kontabilitet', tatime: 'Tatime', pagat: 'Pagat', keshillim: 'Këshillim' };
  if (q && map[q]) { var cb = $('input[name=topic][value="' + map[q] + '"]'); if (cb) cb.checked = true; }

  /* ---------- footer year ---------- */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
