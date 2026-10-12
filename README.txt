TOUR DA CAPE — FOOTER UPDATE

Included files:
- footer.html: replacement footer markup
- footer.css: responsive styling for the new footer
- tour-da-cape-logo.jpeg: your existing logo image, copied without editing

WHAT THIS CHANGES
- Removes the repeated Home / Tours & Experiences / Transfers / Accommodation / Travel Planning / About / Contact links from the footer.
- Removes the descriptive footer sentence.
- Keeps the logo.
- Shows company registration details and B-BBEE Level 1 Contributor status.
- Does not display the 135% procurement-recognition wording.
- Does not display the SARS TCS PIN or claim that the tax number is a VAT number.

HOW TO APPLY IT IN GITHUB
1. Download and extract the ZIP.
2. In each page's HTML file, find the current <footer>...</footer> block and replace only that block with the contents of footer.html.
3. Add the contents of footer.css to the site's main CSS file, OR add this inside each page's <head>:
   <link rel="stylesheet" href="footer.css">
   If linking the separate CSS file, upload footer.css to the same directory as the HTML pages.
4. Upload tour-da-cape-logo.jpeg to the same directory as the HTML pages. If the image is stored in another folder, update the src path in footer.html.
5. Repeat for all seven pages so the footer is consistent throughout the website.
6. Commit the changes in GitHub and wait for GitHub Pages / hosting to publish them.

IMPORTANT
This package is a footer replacement, not a full copy of the entire website. Replace only the footer section; do not replace the page header or the rest of each page. The company details were taken from the documents provided. Confirm the exact public-facing company name and registration details before publishing.
