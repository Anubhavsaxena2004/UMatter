# UMatter Frontend (templates & static)

Folder layout created in the project root:

- `templates/` - Django templates (base.html, home.html, trauma_assessment.html, selfcare_tips.html, progress_tracker.html, account.html)
- `static/css/styles.css` - global styles
- `static/js/main.js` - simple JS helpers
- `static/images/` - place your UI images here (see `static/images/README.md`)

Integration notes:
1. `UMatter/UMatter/settings.py` already updated to include `BASE_DIR / 'templates'` in `TEMPLATES[0]['DIRS']` and `STATICFILES_DIRS = [BASE_DIR / 'static']`.
2. During development Django serves static files automatically with `DEBUG=True`.
3. For each page, create a Django view that renders the template:
   - Example: `return render(request, 'home.html')` for the home view.
4. Use the static files using `{% load static %}` and the provided references in `base.html`.

Quick test:

- Start the Django dev server: `python manage.py runserver`
- Open a browser and visit: `http://127.0.0.1:8000/` (home), `http://127.0.0.1:8000/trauma-assessment/`, `http://127.0.0.1:8000/selfcare/`, `http://127.0.0.1:8000/progress/`, `http://127.0.0.1:8000/account/`

Note: I added quick TemplateView-based URL patterns in `UMatter/urls.py` to render these templates immediately for development and testing. When you connect real backend views, replace those TemplateView entries with your view functions or include URLs from your apps.

If you'd like, I can also add example view functions and wire them to an app (e.g. `accounts` or a new `frontend` app) — tell me which you prefer and I will add them.