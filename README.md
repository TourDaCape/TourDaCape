# Tour Da Cape Website

A luxury tour operator website based in Cape Town, South Africa.

## Large Files Strategy

Original images live in `actual-images/` and are excluded from Git by `.gitignore`. The site uses optimized assets from `optimized-images/` (WebP + JPEG fallbacks), keeping the repository small and avoiding upload limits.

If you must version large originals, consider Git LFS, but for static hosting (GitHub Pages) optimized assets are preferred.

## Image Optimization

Generate optimized WebP + JPEG fallbacks:

```
python compress_images.py
```

Output goes to `optimized-images/`. All HTML pages use `<picture>` tags to serve WebP with JPEG fallback.

Manual tools (optional):
- TinyPNG https://tinypng.com/
- ImageOptim
- Squoosh

## Project Structure
- HTML pages for all website sections
- CSS styling with custom color scheme
- JavaScript for interactive elements
- Original images in `actual-images/` (ignored by Git)
- Optimized images in `optimized-images/` (tracked)

## Deployment

### A) GitHub Pages (automated)
This repo includes `.github/workflows/pages.yml` to deploy from the `main` branch.

Steps:
- Create a new GitHub repository named `TourDaCape` under the `tourdacape` account.
- Push the project:
  - `git init`
  - `git add optimized-images *.html style.css script.js compress_images.py .gitignore README.md robots.txt sitemap.xml favicon.* assets images data`
  - If originals were staged: `git rm -r --cached actual-images hero-images`
  - `git commit -m "Initial site with optimized assets"`
  - `git branch -M main`
  - `git remote add origin https://github.com/<your-username>/<your-repo>.git`
  - `git push -u origin main`
- In GitHub → Settings → Pages, set Source to “GitHub Actions”. After the first workflow run, Pages will publish your site at:
  - `https://tourdacape.github.io/TourDaCape/`

### B) GitHub Web Upload (no Git required)
Use the helper script to package files excluding large originals:

```
./prepare_upload_folder.ps1
```

Then drag the CONTENTS of `uploadable/` into GitHub’s web upload UI.

## Google Search (Indexing)

1) Get your site URL
- GitHub Pages URL is `https://tourdacape.github.io/TourDaCape/`.
- Update `sitemap.xml` and `robots.txt` to use your URL.

2) Verify site ownership in Google Search Console
- Go to https://search.google.com/search-console
- Add property using your Pages URL.
- Verify via DNS, HTML file upload, or a meta tag. Meta tag example (put in `<head>` of all pages):
  - `<meta name="google-site-verification" content="YOUR_TOKEN_HERE">`

3) Submit your sitemap
- Ensure `sitemap.xml` points to your Pages URL.
- In Search Console, submit `https://tourdacape.github.io/TourDaCape/sitemap.xml`.

4) Request indexing
- Use “URL Inspection” to submit key pages (home, tours, about).

## Notes
- `.gitignore` excludes `actual-images/` and `hero-images/` to prevent large files from being uploaded.
- Use `prepare_upload.ps1` to create a zip for web upload if needed.
- No server is required; GitHub Pages serves static HTML, CSS, and JS.