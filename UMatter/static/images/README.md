Place your UI images in this folder (the template HTML files expect these filenames):

- `hero.jpg` — large hero image (recommended 1200×600)
- `trauma.jpg` — card image for trauma assessment (recommended 800×500)
- `selfcare.jpg` — card image for selfcare tips (recommended 800×500)
- `tracker.jpg` — card image for progress tracker (recommended 800×500)
- `avatar.png` — user avatar placeholder (recommended 200×200)

When you add the images, the templates will load them via `{% static 'images/<name>' %}`.
If you prefer different names, update the `src` attributes in the corresponding templates.