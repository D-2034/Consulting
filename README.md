# Daniel Yorke Consulting — website

Live at <https://d-2034.github.io/Consulting/>

The site is built with [Quarto](https://quarto.org). Each page is a plain-text `.qmd` file written in Markdown. When you push changes to GitHub, the site rebuilds and publishes itself.

## Where things are

| File | What it is |
|---|---|
| `index.qmd` | Home page |
| `services.qmd` | Services (both service lines) |
| `examples.qmd` | "What a project looks like" |
| `about.qmd` | About page and portrait |
| `contact.qmd` | Contact page |
| `blog/` | Notes/blog — built but hidden (see below) |
| `_variables.yml` | Email address, reply-time line, location — change them once here |
| `_quarto.yml` | Site settings: navigation bar, footer, theme |
| `assets/css/custom.scss` | All colours, fonts and styling |
| `assets/img/` | Images |
| `scripts/make_graphics.py` | Draws the dot graphic, favicon and share image |
| `CONTENT-TODO.md` | Content still to be supplied |

## Editing a page

1. Open the `.qmd` file.
2. Edit the text. It's ordinary Markdown: `## Heading`, `**bold**`, `- list item`, `[link text](contact.qmd)`.
3. Leave the block between the `---` lines at the top alone, except `title` and `description` (the description is what search engines show).
4. Lines like `::: {.cards}` and `:::` group content for layout. Keep them in pairs.

**Links between pages** must be relative, e.g. `[About](about.qmd)` — never `/about.html`. The site lives under `/Consulting/`, so a link starting with `/` breaks once it's published, even if it works in preview.

## Previewing on your computer

Install Quarto from <https://quarto.org/docs/get-started/>, then, from this folder:

```sh
quarto preview
```

A browser opens and refreshes as you save. (If `quarto` isn't found, add `%LOCALAPPDATA%\Programs\Quarto\bin` to your PATH, or reinstall Quarto with the "add to PATH" option.)

## Publishing

Commit your changes and push to the `main` branch. That's all — GitHub Actions (`.github/workflows/publish.yml`) builds the site, checks the links, and publishes it within a few minutes. Watch progress in the repository's **Actions** tab. If a run fails, the site stays on the previous version.

Never commit the `_site/` folder; it's generated.

## Changing the colours or fonts

Open `assets/css/custom.scss`. Everything you'd want to change is at the top:

- `$accent` — the one accent colour (buttons, links, rules). Changing this one line re-colours light **and** dark mode.
- `$paper-light`, `$ink-light`, etc. — background and text colours for each mode.
- `$font-heading`, `$font-body` — fonts. The heading font (Fraunces) is loaded from Google Fonts in `_quarto.yml`; change that link too if you switch heading fonts.

Check that text still has enough contrast after a colour change (e.g. <https://webaim.org/resources/contrastchecker/> — aim for at least 4.5:1).

If you change `$accent`, also update `ACCENT` in `scripts/make_graphics.py` and run `python scripts/make_graphics.py` (needs Pillow) to redraw the graphics.

## Adding a blog post

1. Copy one of the files in `blog/posts/`, rename it `YYYY-MM-DD-short-title.qmd`.
2. Change `title`, `date`, `description`, and write the post.
3. Put any images next to the post or in `assets/img/`, and reference them with a relative path.

## Turning on the blog

The blog is built but hidden: not in the navigation, marked `noindex`, and removed from `sitemap.xml`. To launch it:

1. In `_quarto.yml`, un-comment the two `Notes` lines under `navbar: left:`.
2. Delete `blog/_metadata.yml` (removes `noindex`), delete the `post-render:` line in `_quarto.yml` (puts the blog back in the sitemap), and remove the `Disallow: /Consulting/blog/` line from `robots.txt`.

Delete or replace the two sample posts first.

## Changing the email, or adding a phone number

- Email: edit `email` in `_variables.yml`, and the two email lines in the structured data at the bottom of `index.qmd`.
- Phone: un-comment `phone` in `_variables.yml`, then un-comment the phone stub in `contact.qmd`.

## Moving to a custom domain

A domain like `danielyorke.ca` (about $15/year) reads better to clients than a `github.io` address and removes the `/Consulting/` subpath issue. When you have one:

1. Add a DNS record at your registrar per <https://docs.github.com/pages/configuring-a-custom-domain-for-your-github-pages-site>.
2. Enter the domain under **Settings → Pages → Custom domain**, and add a `CNAME` file (containing just the domain) to this folder, listed under `resources:` in `_quarto.yml`.
3. Update `site-url` in `_quarto.yml` and `_variables.yml`, the URLs at the bottom of `index.qmd`, and `robots.txt`.
