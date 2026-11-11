# Olga Tochilin — Portfolio

A simple static portfolio site (plain HTML, CSS and a little JavaScript — no build step).

- `index.html` — home page
- `portfolio/<project>/index.html` — case studies
- `assets/` — styles, scripts, fonts, and images

## Preview locally

```bash
python3 -m http.server 8080
```

Then open http://localhost:8080.

## Deploying

The site is hosted on Vercel. Pushing to `main` publishes to production;
other branches get their own preview deployments.
