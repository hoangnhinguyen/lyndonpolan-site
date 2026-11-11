#!/usr/bin/env python3
"""Rebuild the site's HTML pages from the files in content/.

    python3 build.py

Edit content/works.json (paintings) or content/site.json (texts, CV, links),
run this script, then commit and push. Standard library only; Pillow is needed
just once per new painting, to measure it and make its thumbnail.

Pages written:
    index.html            Works (thumbnail grid)
    bio/index.html        Bio / CV
    contact/index.html    Contact form
    <id>/index.html       one page per painting
    404.html              "page not found"
"""
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = json.loads((ROOT / "content" / "site.json").read_text(encoding="utf-8"))
WORKS = json.loads((ROOT / "content" / "works.json").read_text(encoding="utf-8"))
THUMB_WIDTH = 560  # pixels; about twice the width a thumbnail is shown at, so it stays sharp


def prepare(work):
    """Fill in what can be worked out: file paths, image size, and a missing thumbnail.

    A new painting only needs "id" and "caption" in works.json plus images/<id>.jpg.
    Measuring the image and making the thumbnail needs Pillow (pip install pillow);
    paintings that already list width/height and have a thumbnail do not need it.
    """
    wid = work["id"]
    work.setdefault("image", f"images/{wid}.jpg")
    work.setdefault("thumb", f"images/mini/{wid}m.jpg")
    image, thumb = ROOT / work["image"], ROOT / work["thumb"]
    if not image.exists():
        raise SystemExit(f"painting {wid}: missing file {work['image']}")
    if "width" in work and "height" in work and thumb.exists():
        return
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit(f"painting {wid}: needs Pillow to measure the image / make its thumbnail.\n"
                         f"  Run: pip install pillow   (or add width, height and {work['thumb']} by hand)")
    with Image.open(image) as im:
        work["width"], work["height"] = im.size
        if not thumb.exists():
            thumb.parent.mkdir(parents=True, exist_ok=True)
            small = im.convert("RGB").resize((THUMB_WIDTH, round(im.height * THUMB_WIDTH / im.width)), Image.LANCZOS)
            small.save(thumb, quality=82, optimize=True, progressive=True)
            print(f"  made thumbnail {work['thumb']}")

FACEBOOK_ICON = "M22.675 0h-21.35c-.732 0-1.325.593-1.325 1.325v21.351c0 .731.593 1.324 1.325 1.324h11.495v-9.294h-3.128v-3.622h3.128v-2.671c0-3.1 1.893-4.788 4.659-4.788 1.325 0 2.463.099 2.795.143v3.24l-1.918.001c-1.504 0-1.795.715-1.795 1.763v2.313h3.587l-.467 3.622h-3.12v9.293h6.116c.73 0 1.323-.593 1.323-1.325v-21.35c0-.732-.593-1.325-1.325-1.325z"
INSTAGRAM_ICON = "M15.233 5.488c-.843-.038-1.097-.046-3.233-.046s-2.389.008-3.232.046c-2.17.099-3.181 1.127-3.279 3.279-.039.844-.048 1.097-.048 3.233s.009 2.389.047 3.233c.099 2.148 1.106 3.18 3.279 3.279.843.038 1.097.047 3.233.047 2.137 0 2.39-.008 3.233-.046 2.17-.099 3.18-1.129 3.279-3.279.038-.844.046-1.097.046-3.233s-.008-2.389-.046-3.232c-.099-2.153-1.111-3.182-3.279-3.281zm-3.233 10.62c-2.269 0-4.108-1.839-4.108-4.108 0-2.269 1.84-4.108 4.108-4.108s4.108 1.839 4.108 4.108c0 2.269-1.839 4.108-4.108 4.108zm4.271-7.418c-.53 0-.96-.43-.96-.96s.43-.96.96-.96.96.43.96.96-.43.96-.96.96zm-1.604 3.31c0 1.473-1.194 2.667-2.667 2.667s-2.667-1.194-2.667-2.667c0-1.473 1.194-2.667 2.667-2.667s2.667 1.194 2.667 2.667zm4.333-12h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm.952 15.298c-.132 2.909-1.751 4.521-4.653 4.654-.854.039-1.126.048-3.299.048s-2.444-.009-3.298-.048c-2.908-.133-4.52-1.748-4.654-4.654-.039-.853-.048-1.125-.048-3.298 0-2.172.009-2.445.048-3.298.134-2.908 1.748-4.521 4.654-4.653.854-.04 1.125-.049 3.298-.049s2.445.009 3.299.048c2.908.133 4.523 1.751 4.653 4.653.039.854.048 1.127.048 3.299 0 2.173-.009 2.445-.048 3.298z"

T = SITE["text"]


def t(key):
    """A text in both languages; CSS shows the one matching <html class>."""
    return (f'<span class="t-en" lang="en">{escape(T["en"][key])}</span>'
            f'<span class="t-fr" lang="fr">{escape(T["fr"][key])}</span>')


def caption_html(work):
    sold = ' <span class="soldLabel">Sold</span>' if work.get("sold") else ""
    return escape(work["caption"]) + sold


def page(root, title, main, current="", description=None, preload=None, head_first=""):
    """Wrap a page's main content in the shared layout. `root` is '' or '../'."""
    home = root or "./"
    desc = description or SITE["description"]
    cur = lambda name: ' aria-current="page"' if current == name else ""
    preload_tag = f'<link rel="preload" as="image" href="{root}{preload}">\n' if preload else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{head_first}<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc, quote=True)}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="{root}favicon.png">
<script>try{{if(localStorage.getItem('lang')==='fr'){{document.documentElement.className='fr';document.documentElement.lang='fr'}}}}catch(e){{}}</script>
<link rel="stylesheet" href="{root}assets/site.css">
{preload_tag}</head>
<body>
<div id="root"><div>
<div class="headerContainer"><div class="menu"><div class="navigation"><div class="artistName"><a class="artistNameA" href="{home}"><img src="{root}images/LyndonGif.gif" class="artistNameA2" alt="{escape(SITE['title'])}" width="600" height="338"></a></div><div class="base"><a href="{home}"{cur('works')}>{t('Works')}</a></div><div class="base"><a href="{root}bio/"{cur('bio')}>Bio / CV</a></div><div class="base"><a href="{root}contact/"{cur('contact')}>Contact</a></div><div class="base"><button type="button" class="langSwitchFr" id="langSwitch" aria-label="Français / English"><span class="t-en">FR</span><span class="t-fr">EN</span></button></div><span><a href="{escape(SITE['social']['facebook'])}" aria-label="Facebook"><svg class="social" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="{FACEBOOK_ICON}"/></svg></a></span><span><a href="{escape(SITE['social']['instagram'])}" aria-label="Instagram"><svg class="social" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="{INSTAGRAM_ICON}"/></svg></a></span></div></div></div>
<div class="mainLayout"><div class="mainLayOutInner">
{main}
</div></div>
</div></div>
<script src="{root}assets/site.js"></script>
</body>
</html>
"""


def works_page():
    by_id = {w["id"]: w for w in WORKS}
    placed = [i for col in SITE["home_columns"] for i in col]
    missing = [w["id"] for w in WORKS if w["id"] not in placed]
    if missing:
        raise SystemExit(f"content/site.json: add painting id(s) {missing} to one of the home_columns")
    cols = []
    for col in SITE["home_columns"]:
        items = []
        for n, wid in enumerate(col):
            w = by_id[wid]
            tw = THUMB_WIDTH
            th = round(w["height"] * tw / w["width"])
            lazy = ' loading="lazy"' if n >= 2 else ""
            items.append(
                f'<a href="{wid}/"><span class="pic1"><img src="{w["thumb"]}" alt="{escape(w["caption"], quote=True)}" '
                f'width="{tw}" height="{th}"{lazy} decoding="async">'
                f'<div class="picText">{caption_html(w)}</div></span></a>')
        cols.append('<div class="column">' + "".join(items) + "</div>")
    main = '<br>\n<div class="row">\n' + "\n".join(cols) + "\n</div>"
    return page("", SITE["title"], main, current="works")


def work_page(index):
    w = WORKS[index]
    prev_id = WORKS[index - 1]["id"] if index > 0 else None
    next_id = WORKS[index + 1]["id"] if index + 1 < len(WORKS) else None
    ratio = round(w["width"] / w["height"], 4)
    arrows = ""
    if prev_id is not None:
        arrows += f'<span class="arrow1"> <a href="../{prev_id}/" rel="prev" aria-label="Previous">&lt;</a> </span>'
    if next_id is not None:
        arrows += f'<span class="arrow2"> <a href="../{next_id}/" rel="next" aria-label="Next">&gt;</a></span>'
    main = (f'<br>\n<div class="imageWraper">'
            f'<img src="../{w["image"]}" class="pic1M" alt="{escape(w["caption"], quote=True)}" '
            f'width="{w["width"]}" height="{w["height"]}" style="--ratio:{ratio}">'
            f'<div class="pic1MDisc"><div>{caption_html(w)}</div></div>'
            f'{arrows}</div>')
    title = w["caption"]
    return page("../", title, main, description=w["caption"], preload=w["image"])


def bio_page():
    cv = SITE["cv"]
    parts = [f"<h4>{t('Bio')}</h4>", f"<div>{t('BioText')}</div>",
             f"<h4>{t('Artist statement')}</h4>", f"<div>{t('ArtistStatementText')}</div>",
             "<h4>CV</h4>", f"<h4>{escape(cv['name'])}</h4>"]
    parts += [f"<div>{escape(line)}</div>" for line in cv["contact"]]
    for section in cv["sections"]:
        parts.append(f"<h4>{escape(section['title'])}</h4>")
        parts += [f"<div>{escape(line)}</div>" for line in section["items"]]
    parts.append("<br><br><br>")
    main = '<div class="bioBlock">\n' + "\n".join(parts) + "\n</div>"
    return page("../", f"Bio / CV - {SITE['title']}", main, current="bio")


def contact_page():
    e = SITE["emailjs"]
    main = f"""<form class="contact-form" id="contactForm" data-service="{escape(e['service_id'])}" data-template="{escape(e['template_id'])}" data-user="{escape(e['user_id'])}" data-fallback="{escape(SITE['contact_fallback_email'])}"><input type="hidden" name="contact_number"><label for="user_name">{t('Name')}</label><input type="text" name="user_name" id="user_name" autocomplete="name"><label for="user_email">Email</label><input type="email" name="user_email" id="user_email" autocomplete="email" required><label for="message">Message</label><textarea name="message" id="message" required></textarea><input type="submit" id="sendButton" value="{escape(T['en']['Send'], quote=True)}" data-en="{escape(T['en']['Send'], quote=True)}" data-fr="{escape(T['fr']['Send'], quote=True)}"><p class="formStatus" id="formStatus" role="status" aria-live="polite"></p></form>"""
    return page("../", f"Contact - {SITE['title']}", main, current="contact")


def not_found_page():
    # GitHub Pages serves this one file for any unknown address, at any depth, so relative
    # links cannot be trusted here. The script below sets the base address first:
    # "/" on a custom domain, "/<repository>/" on a <user>.github.io/<repository>/ demo.
    base = ("<script>(function(){var b='/';if(/\\.github\\.io$/.test(location.hostname)){"
            "var s=location.pathname.split('/')[1];if(s)b='/'+s+'/';}"
            "document.write('<base href=\"'+b+'\">');})();</script>")
    main = '<div class="homePageContainer notFound">404 - <a href="./">Go home</a></div>'
    return page("", f"404 - {SITE['title']}", main, head_first=base)


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def main():
    ids = [w["id"] for w in WORKS]
    if len(set(ids)) != len(ids):
        raise SystemExit("content/works.json: two paintings share the same id")
    for w in WORKS:
        prepare(w)
    # remove pages of paintings that no longer exist
    for d in ROOT.iterdir():
        if d.is_dir() and d.name.isdigit() and int(d.name) not in ids:
            shutil.rmtree(d)
    write("index.html", works_page())
    write("bio/index.html", bio_page())
    write("contact/index.html", contact_page())
    for n in range(len(WORKS)):
        write(f"{WORKS[n]['id']}/index.html", work_page(n))
    write("404.html", not_found_page())
    print(f"Built {len(WORKS) + 4} pages ({len(WORKS)} paintings).")


if __name__ == "__main__":
    main()
