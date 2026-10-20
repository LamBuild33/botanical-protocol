# Botanical Protocol

By Alfred Ceballos

A weight-based guide to a daily herbal and spice protocol. Enter your body weight and the page shows suggested daily amounts, the maximum for each ingredient that has an official safety limit, a shopping list, how to make it, cautions, and the research behind each ingredient (97 sources).

This is general information, not medical advice. Read "Before you start" on the page first.

## Open it

- **Regular version:** `index.html`
- **Large-text version** (bigger text and buttons, easier to read on a phone): `large-text.html`

Each page is one self-contained file (the photo is built in), so it also works if you download it and open it in any browser.

## Folder layout

| Path | What it is |
|---|---|
| `index.html`, `large-text.html` | The finished pages people open |
| `src/protocol.html` | The main page content: edit this to change wording, amounts, or sources |
| `src/large-text.css` | Extra styles that make the large-text version |
| `scripts/` | Steps that rebuild both pages from `src/` |
| `img/main.jpg` | The ingredients photo (location and camera data removed) |

## Making changes

1. Edit `src/protocol.html` (or `src/large-text.css` for large-text styling).
2. Run `scripts/build.sh`. It needs Python 3, Node, and Playwright.
3. Both `index.html` and `large-text.html` update together, so they always match.

## License and credit

© 2026 Alfred Ceballos. Licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) (Creative Commons Attribution-NonCommercial-NoDerivatives). You may share this work as long as you credit Alfred Ceballos. You may not use it to make money, and you may not share changed versions. Full terms are in `LICENSE`.
