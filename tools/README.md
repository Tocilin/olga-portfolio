# Site generator

The pages are **generated** by one script, then committed as plain HTML. Vercel just serves the
committed files (no build runs on deploy).

```bash
pip install pillow          # once
python3 tools/build.py      # rewrites index.html and portfolio/<project>/index.html
```

Running it on an unchanged repo changes nothing (the output is reproducible). Never edit the
generated HTML by hand: the next build overwrites it. Change the generator or the content instead.

## What to edit

| To change… | Edit |
|---|---|
| Header, footer, `<head>`, back button | `page()` in `tools/build.py` |
| Hero text, buttons, section order on the homepage | the `home` block in `tools/build.py` |
| "What I Do" cards (titles, descriptions, dot shapes) | `WHAT` |
| Experience list | `EXPERIENCE` |
| Which projects exist and their order | `PROJECTS` (first one is the wide tile on the homepage) |
| Homepage / "More work" captions (title + company) | `WORK_CAPTION` |
| A case study's text and images | `tools/content/<slug>.json` |
| How a content type looks (cards, strips, stats…) | `render_blocks()` + `assets/style.css` |
| Favicon (OT in a dark circle) | `assets/favicon.svg` (source), `assets/favicon-32.png`, `assets/apple-touch-icon.png`, `favicon.ico` at the repo root; linked from `page()` |
| Site-wide look, motion | `assets/style.css`, `assets/site.js` (edited directly, not generated) |

Then run the build, check the result locally (`python3 -m http.server 8080`, desktop and ~390px
mobile), and commit the generated HTML together with the source change.

## Content files (`tools/content/<slug>.json`)

A list of `[kind, value]` blocks, rendered in order. Kinds: `h1` (title; or `h1` + `h2` + `p`
triples for the PatPat stats), `h2` (sub-heading), `h4`, `p` / `li` (HTML allowed: `<a>`,
`<strong>`, `<em>`), `img` (`[ 'img', filename-or-url, section ]`), `strip` (sideways gallery),
`stat` (number cards), `pull` (large pull line), `thanks` (closing line), and an optional first
`meta` block with `lead` (subtitle), `client`, `role`. A few pages have special handling keyed
by slug in `render_blocks()` (PatPat decision cards, Outdoorsy problem cards, image pairs listed
in `ROW_FIRST`, Midland's Key takeaways moved to the end).

## Adding a case study

1. Get the content: save the source page's HTML and run
   `python3 -I tools/extract_case_study.py page.html tools/content/<slug>.json` (or write the
   JSON by hand).
2. Put images in `assets/img/` as `<slug>-<name>.webp` (convert PNG/JPG with Pillow, max ~2000px
   wide, quality ~82; keep SVGs as they are). Reference the file names in the JSON.
3. Make a 1200×509 cover tile `assets/img/<slug>-featured.webp` (light `#f0f4f9` background, big
   serif title on top; the existing ones are the model).
4. Add the project to `PROJECTS` and `WORK_CAPTION` in `tools/build.py`, run the build, check it,
   commit.

Source for Franky and Mayo: https://www.olgadesignsystems.com/portfolio/franky/ and `/mayo/`.
