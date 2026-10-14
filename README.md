# Precious Salako — Data Analytics Portfolio

A responsive, static portfolio website featuring Power BI, SQL, Excel, Python, exploratory analysis, machine learning, and a Grafana learning roadmap. It uses plain HTML, CSS, and JavaScript—no build step, API key, server, or paid hosting is required.

## Included

- `index.html` — portfolio content and interactive demo dashboard
- `styles.css` — responsive styling and dashboard visuals
- `app.js` — animated demo stream, live clock, accessible project filters and search, mobile navigation, copy-email action
- `favicon.svg` — site icon
- `downloads/` — project artefacts shared with the portfolio: Power BI files, SQL script, and project notes/scripts

## Important data note

The animated event-rate chart in the hero is **simulated in the browser** to demonstrate a real-time dashboard interaction. It is not connected to a production database, actual visitor telemetry, or a live Grafana instance. The climate and FMCG modelling examples use synthetic learning datasets. Insurance-charge figures are descriptive associations in that dataset and not evidence of causation. The systolic blood-pressure prototype is for educational use only, not medical diagnosis.

The Power BI reports are downloadable `.pbix` files; visitors need Power BI Desktop or a compatible Power BI environment to inspect them. The MD Water Services SQL script is a large training dataset dump.

## Preview locally

Open `index.html` in a modern web browser. For a local web server, run this command from this folder:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`.

## Publish free on GitHub Pages (public website)

1. Sign in to GitHub and create a **public** repository named exactly `salako-precious.github.io` under the `salako-precious` account.
2. Upload the contents of this folder into the repository root—not the enclosing `precious_salako_portfolio` folder. Ensure `index.html`, `styles.css`, `app.js`, `favicon.svg` and `downloads/` are visible at the top level.
3. In the repository, open **Settings → Pages**. Choose **Deploy from a branch**, select the `main` branch and `/ (root)`, then save.
4. After GitHub Pages finishes building, the public site should be available at `https://salako-precious.github.io/`. It may take a few minutes for the first build.
5. Test the website in a private/incognito browser window and on a phone. Confirm all download buttons work. All files in a public repository—including items in `downloads/`—can be downloaded by anyone.

GitHub Pages documentation: https://docs.github.com/en/pages/getting-started-with-github-pages

## Updating the site

Edit the copy in `index.html`, adjust styles in `styles.css`, and update behaviours in `app.js`. To add a project card, duplicate an existing `<article class="project-card">` in `index.html`, update the `data-category` and `data-search` values, and adjust the filter-button counts if you change the number of cards.

## Grafana next step

Once you are ready, connect Grafana to a real data source (for example, a local SQL database or a time-series source), build a dashboard panel, and replace the simulated event stream only when a genuine endpoint is available. Avoid placing database credentials, API tokens, or private patient/customer data in the public website repository.
