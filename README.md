# Lyndon Polan — portfolio site

Static version of lyndonpolan.com, ready for GitHub Pages. Plain HTML, CSS and a little
JavaScript: nothing to install, nothing to build on GitHub's side. Check the full website here: <https://h-ngnhi.github.io/lyndonpolan-site/>.

## What is in here

| Path | What it is |
| --- | --- |
| `index.html` | Works — the thumbnail grid |
| `bio/`, `contact/` | Bio / CV and the contact form |
| `1/` … `17/` | One page per painting (same addresses as the old site: `/6`, `/bio`, …) |
| `404.html` | Shown for any address that does not exist |
| `images/` | Paintings (`images/6.jpg`), thumbnails (`images/mini/6m.jpg`), animated logo |
| `assets/` | Stylesheet, script, Roboto font files |
| `content/works.json` | The list of paintings and their captions |
| `content/site.json` | Bio and artist statement (EN/FR), CV, social links, grid layout |
| `build.py` | Regenerates every page from the two files in `content/` |

The `.html` pages are generated. Change the files in `content/`, then run `python3 build.py`.

## Look at it on your computer

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. (Opening `index.html` by double-click shows the home page,
but links to the other pages need the small server above.)

## Put it on GitHub Pages

1. Create a new **public** repository on GitHub (for example `lyndonpolan`).
2. Push this folder to it:
   ```bash
   git init -b main
   git add -A
   git commit -m "Portfolio site"
   git remote add origin https://github.com/YOUR-USERNAME/lyndonpolan.git
   git push -u origin main
   ```
   No git? On the new repository's page choose **uploading an existing file** and drag in
   everything *inside* this folder.
3. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch**,
   branch `main`, folder `/ (root)`, **Save**.
4. After a minute the demo is at `https://YOUR-USERNAME.github.io/lyndonpolan/`.

All links are relative, so the same files work at that demo address and later at the real domain.

## Go live on lyndonpolan.com

Do this only when the demo looks right; until then the current site keeps running untouched.

1. Optional: run `bash tools/fetch-originals.sh` and commit, to swap in the byte-identical
   original image files while the old host is still reachable.
2. **Settings → Pages → Custom domain**: enter `lyndonpolan.com` and save (GitHub adds a `CNAME` file).
3. At the domain registrar, point the domain's DNS at GitHub Pages, following
   <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site>.
4. Back in **Settings → Pages**, tick **Enforce HTTPS** once it becomes available.
5. Cancel the old hosting only after the new site has been answering on the domain for a few days.

## Everyday edits

**Add a painting**

1. Save the image as `images/18.jpg` (next free number).
2. Add it to `content/works.json`:
   ```json
   { "id": 18, "caption": "Lyndon Polan, Title, Oil on canvas, 24x36, 2026" }
   ```
   Add `"sold": true` to show the red *Sold* label.
3. Add `18` to one of the four lists in `home_columns` in `content/site.json` — each list is one
   column of the grid, top to bottom.
4. Run `python3 build.py`. It measures the image and makes the thumbnail (this step needs
   `pip install pillow`), then writes the pages. Commit and push.

**Mark a painting sold / change a caption** — edit `content/works.json`, run `python3 build.py`.

**Change the bio, statement or CV** — edit `content/site.json` (`text.en`, `text.fr`, `cv`),
run `python3 build.py`.

**Remove a painting** — delete its entry from `works.json` and its number from `home_columns`,
run `python3 build.py` (its page folder is removed for you).

## Contact form

The form sends through the same EmailJS service, template and key as the old site
(`emailjs` in `content/site.json`), so messages keep arriving in the same inbox. If the EmailJS
account restricts which domains may send, add the `github.io` demo address there to test the
form before going live. If sending fails, the visitor is shown the fallback e-mail address.

## Credits

Roboto font files in `assets/fonts/` are licensed under the SIL Open Font License
(`assets/fonts/LICENSE.txt`). All artwork © Lyndon Polan.
