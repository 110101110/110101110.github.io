# BadSeed

Portfolio at https://thebadseed.fr, by naozhong, XX & TT.

## Development

Install Ruby and Bundler, then run:

```sh
bundle install
bundle exec jekyll serve
```

Run `bundle exec jekyll build` before publishing. GitHub Pages can build the committed Jekyll source and optimized images.

## Structure

- `index.html`: responsive homepage.
- `_posts/`: project text and image includes. Filenames determine the existing project URLs; post layout is configured once in `_config.yml`.
- `_layouts/`: shared page frame, project layout, and generic page layout.
- `_includes/`: head metadata, menu, email icon, and responsive image helpers.
- `_data/navigation.yml`: menu links; site title, author, and email live in `_config.yml`.
- `assets/css/main.css`: all styles, with no Sass compilation.
- `assets/js/menu.js`: menu toggle, backdrop dismissal, and Escape handling.

SEO, sitemap, Atom feed, and the legacy RSS endpoint are retained. The unused theme category, pagination, comment, sharing, related-post, code-highlighting, and theme-packaging features have been removed.

## Image optimization

Browser images use committed variants under `assets/img/optimized/`; original uploads remain unchanged. `_data/images.json` supplies intrinsic dimensions and responsive sources. Animated GIFs retain their original animation.

To regenerate after adding images, install Python Pillow with WebP support and `heif-convert` (libheif, needed for legacy HEIC uploads), then run:

```sh
python3 scripts/optimize_images.py
```

Use `{% include image.html file="filename.jpg" alt="Description" %}` for post images. Below-the-fold images default to lazy loading. The post cover and homepage are eager and high priority. Pixel-art variants use nearest-neighbor resizing and lossless WebP; photographic variants use quality 85. Commit generated assets and metadata together with the content changes.
