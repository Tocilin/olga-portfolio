# Olga Tochilin — portfolio (olgatochilin.com)

Static site: plain HTML, one stylesheet (`assets/style.css`) and one small script
(`assets/site.js`). No build step, no dependencies.

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
  outdoorsy, jpmorgan-chase)
- `assets/` — `style.css`, `site.js`, `fonts/`, `img/`, and the résumé PDF

The header and footer markup is duplicated in every page, so a change to the
nav or footer must be made in all six HTML files.

## Hosting

- Vercel project `olga-portfolio`, Production Branch = `main`.
- Domain `olgatochilin.com` (registered at DreamHost, nameservers pointed at
  Vercel DNS); `olgatochilin.com` redirects to `www.olgatochilin.com`.
