"""Make the README's relative links absolute so they resolve from this repo.

The source README links images and files by paths relative to the
wasi-master/wmkeyboard root. Shown as this organization's profile, those paths
would resolve against wmkeyboard/.github instead and every image would break.
Images go to raw file URLs, everything else to the blob/tree view.
"""
import re
import sys

REPO = "https://github.com/wasi-master/wmkeyboard"
RAW = f"{REPO}/raw/main/"
BLOB = f"{REPO}/blob/main/"


def relative(url):
    return not re.match(r"^([a-z][a-z0-9+.-]*:|#|/)", url, re.I)


def fix(url, image):
    if not relative(url):
        return url
    return (RAW if image else BLOB) + url.removeprefix("./")


IMAGE_EXT = re.compile(r"\.(png|jpe?g|gif|svg|webp|avif)(\?.*)?$", re.I)

text = open(sys.argv[1], encoding="utf-8").read()
# HTML attributes: src/srcset are always images; href only when it points at one.
text = re.sub(r'\b(src|srcset)="([^"]+)"', lambda m: f'{m[1]}="{fix(m[2], True)}"', text)
text = re.sub(r'\bhref="([^"]+)"', lambda m: f'href="{fix(m[1], bool(IMAGE_EXT.search(m[1])))}"', text)
# Markdown: ![alt](img) and [text](link).
text = re.sub(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)",
              lambda m: f"{m[1]}[{m[2]}]({fix(m[3], m[1] == '!' or bool(IMAGE_EXT.search(m[3])))})", text)
open(sys.argv[2], "w", encoding="utf-8").write(text)
