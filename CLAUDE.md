# CLAUDE.md

Portfolio and client pages for **Noor Creative Marketing** (نور للتسويق الإبداعي), a social-media marketing studio in Amman. Hosted on GitHub Pages from `main`:
https://alhodanoor52-tech.github.io/noor-creative-marketing/

## Build, run, test

There is no build step, package manager, framework or test suite. Every page is a single hand-written HTML file with its CSS in `<style>` and its JS in `<script>`. Keep it that way: do not add npm, bundlers, frameworks or a CSS library.

- **Preview locally:** `python3 -m http.server 8000` from the repo root, then open `http://localhost:8000/`. Use a server, not `file://`, because paths are relative and some pages load each other's images.
- **Check before committing** (this stands in for tests):
  - Open each page you changed at phone width (about 375px) and at desktop width. Check both RTL Arabic and, on the home page, English (the `EN` toggle).
  - Make sure no image, video or audio path is broken. This one-liner lists missing local assets:
    ```sh
    for d in . awj awj/links links invitation; do grep -oh '\(src\|href\|poster\|data-full\)="[^"#:]*\.\(jpg\|png\|mp4\|mp3\)"' $d/index.html | sed 's/.*="//;s/"//' | sort -u | while read p; do [ -e "$d/$p" ] || echo "MISSING $d -> $p"; done; done
    ```
    `images/branding.jpg` and `images/marah-birds.jpg` are expected to be missing: they are optional placeholders with `onerror="this.remove()"`.
  - Playwright and Chromium come pre-installed in cloud sessions if you want screenshots.
- **Deploy:** merging or pushing to `main` publishes through GitHub Pages. There is no CI.

## Layout

| Path | What it is |
|---|---|
| `index.html` | Main bilingual (AR/EN) site: hero, services, work/case studies, process, contact |
| `links/index.html` | Link-in-bio page for Noor (`/links/`) |
| `awj/index.html` | Hosted website for client **Awj / AWG uniforms** (أوج للألبسة المهنية). It has its own brand, not Noor's |
| `awj/links/index.html` | Link-in-bio page for Awj |
| `invitation/index.html` | Wedding invitation demo, with `music.mp3` |
| `images/` | All shared images. Client folders: `awj/` (with `awj/chef/`), `sns/` (Stop & Shop), `ameed/` (Al Ameed Coffee), `shahwan/` (Shahwan Furniture). Reels are `reel.mp4` + `reel-poster.jpg` |

Each page is self-contained: CSS is copied per page, not shared. When you change a design token, update it in every page that uses it.

## Code style

- **Arabic first, RTL.** Every page starts with `<html lang="ar" dir="rtl">`. Write natural Jordanian/Levantine-friendly Modern Standard Arabic copy, not machine-translated text.
- **Bilingual text on `index.html`:** put both languages side by side as `<span class="ar">…</span><span class="en">…</span>`; CSS hides the inactive one. Any new visible text on the home page needs both. The language toggle stores the choice in `localStorage` (wrapped in try/catch). The other pages are Arabic only.
- **Noor brand tokens** (in `:root` on `index.html` and `links/`): `--white`, `--mist #F3F6EE`, `--sage #8A9C67`, `--moss #3E4A2E`, `--ink #2B2723`, `--ink-soft`, `--rule`, `--lav #8B78C2` (use lavender sparingly), `--lav-tint`. Use the variables, not raw hex.
- **Fonts:** Google Fonts only. Arabic: Noto Kufi Arabic (display) + IBM Plex Sans Arabic (body). English: Cormorant Garamond (display) + IBM Plex Sans (body). The Awj pages use Cairo with their own red/grey palette (`--red #af2e33`).
- Use logical CSS properties (`margin-inline`, `inset-inline-end`, `padding-inline-start`) so layouts work in RTL and LTR.
- Compact CSS: one rule per line, no extra whitespace, matching the existing files.
- Vanilla JS only, small and inline, at the end of `<body>`. Icons are inline SVG `<symbol>`s used with `<use href="#…">`.
- Every external link gets `target="_blank" rel="noopener"`. Show Latin handles and phone numbers inside `dir="ltr"`.
- Show client work uncropped (phone frame or `object-fit:contain`) unless asked otherwise. Images go in `images/<client>/` as compressed `.jpg`. Keep files small; the repo is already about 14 MB.

## Contacts and links (don't ask, use these)

- **Noor WhatsApp:** `962788218638`. On `index.html` it is set once in the config block at the top of the `<script>` (`WHATSAPP`, `FACEBOOK_*`) and applied to every `.wa` link. Change it there, not in each link.
- **Awj WhatsApp:** `962788119852` (Awj pages and the links pages).
- Noor Instagram: `https://www.instagram.com/noor.creative.marketing/`
- Awj Instagram: `@uniform_awg_uniform`; Awj Facebook: `facebook.com/awguniform`; Awj LinkedIn: `linkedin.com/company/awg-for-trading-uniform/`
- Clients in the portfolio: Awj (uniforms), Stop & Shop, Marah Birds (مرح العصافير), Al Ameed Coffee, Shahwan Furniture, plus the wedding invitation demo.

## Git

- Commit messages are short and in English, prefixed with the page or client when it helps: `Awj page: add links section and nav item`, `Work: add Al Ameed Coffee AI concept ad reel`, `Links page: add Awj WhatsApp`.
- `main` is live. Work on a branch unless told to push directly.

## Notes

- `images/README.md` (in Arabic) is an older upload guide. Some of the filenames it lists no longer match what the pages use. Trust the HTML.
- Reel videos autoplay `muted loop playsinline`; the invitation music only starts after a tap. The reel sound buttons on `index.html` mute every other reel when one is unmuted. Keep that behaviour when you add reels.
