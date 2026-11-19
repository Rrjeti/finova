# Finova — website

Static site (HTML + one CSS file + one small JS file, no frameworks).

## Pages
`index.html` · `sherbimet.html` · `rreth-nesh.html` (new) · `kontakt.html` · `privatesia.html` (new) · `404.html`

## Editing
All pages are generated from `tools/build.py` (shared header, footer, SEO tags, structured data).
Edit the text/data there, then run:

```
python3 tools/build.py
```

Styles: `assets/css/style.css` · Animations & interactions: `assets/js/main.js`

### Scroll animations
Add `data-reveal="up|down|left|right|zoom|blur|flip|tilt|mask|wipe"` to any element.
Headings with `data-split` animate word by word. `data-stagger=".1"` on a parent staggers its children.
`data-parallax=".1"` moves an element with scroll; `data-count="320"` counts a number up.

### Before going live — replace placeholders
- `SITE`, `PHONE`, `GEO` (office coordinates) and `SOCIAL` links at the top of `tools/build.py`
- Testimonials on the home page (use real ones, with permission)
- Team names/photos on `rreth-nesh.html`
- Contact form: create a free form at formspree.io and put its URL in `data-endpoint`
  on `#contact-form` (otherwise the form opens the visitor's email app)
- Have the privacy policy reviewed legally
