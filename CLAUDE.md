# Olga Tochilin — portfolio (olgatochilin.com)

Static site: plain HTML, one stylesheet (`assets/style.css`) and one small script
(`assets/site.js`). Vercel serves the committed files as they are (no build on deploy).

**The HTML pages are generated** by `python3 tools/build.py` from `tools/build.py` and
`tools/content/*.json` (see `tools/README.md`). Never edit `index.html` or
`portfolio/*/index.html` by hand: change the generator or the content, run the build, and commit
the regenerated HTML with the source change. `assets/style.css` and `assets/site.js` are edited
directly.

## Publishing (standing permission from the owner)

This is a non-sensitive personal portfolio. When the owner asks for a change,
**commit and push straight to `main`** — no pull request and no review needed.
Vercel deploys `main` to production automatically (about a minute), so there is
nothing else to click.

- Check the change locally first (`python3 -m http.server 8080`, then look at the
  desktop and ~390px mobile layouts) before pushing.
- Never force-push. If `main` has moved, fetch and rebase/merge first.
- Keep the working branch and `main` in sync after pushing.
- After pushing, confirm the live site (https://www.olgatochilin.com) shows the change.
- To undo a bad deploy: Vercel → Deployments → older good one → Promote
  (Instant Rollback), or `git revert` and push.

## Structure

- `index.html` — home page
- `portfolio/<project>/index.html` — case studies (patpat, midland, lucid,
  outdoorsy, jpmorgan-chase, franky, mayo). `franky` and `mayo` were moved over
  from olgadesignsystems.com; their cover tiles are `assets/img/franky-featured.webp`
  and `assets/img/mayo-featured.webp`.
- `assets/` — `style.css`, `site.js`, `fonts/`, and `img/`
- `tools/` — the page generator, case-study content and notes (kept out of the public deploy via `.vercelignore`)

The header and footer live in `page()` in `tools/build.py` and are written into every page by the
build, so one edit there updates all pages.

## Search engines: do not index (owner's decision)

The owner does not want the site listed by Google. Every page carries
`<meta name="robots" content="noindex, nofollow">` (from `page()` in `tools/build.py`) and
`vercel.json` sends `X-Robots-Tag: noindex, nofollow` for every file, including images.
Keep both. Do not add a `robots.txt` that disallows crawling: crawlers must be able to read the
noindex signal. Remove both only if the owner asks to be listed.

## Hosting

- Vercel project `olga-portfolio`, Production Branch = `main`.
- Domain `olgatochilin.com` (registered at DreamHost, nameservers pointed at
  Vercel DNS); `olgatochilin.com` redirects to `www.olgatochilin.com`.
