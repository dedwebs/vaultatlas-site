# Vault Atlas site

Static website for Vault Atlas, an unofficial Fallout 76 companion for iOS. This repository is the public landing, support, and privacy pages. The iOS app is not in this tree.

GitHub Pages publishes it at https://dedwebs.github.io/vaultatlas-site/.

## Pages

- `index.html` — short landing page. States that Vault Atlas is an unofficial Fallout 76 companion for iOS, and links to support and privacy.
- `support.html` — support page. Contact is `info@nixonmade.com`, plus App Store Connect / TestFlight feedback. It also has short notes on the Theorycraft Pack (one-time unlock for Weapons Caps-Check and Perk Loadout; Restore Purchases from Builds or More), data accuracy (offline packs and estimates can lag live patches), a link to the privacy policy, and a disclaimer that the app is fan-made and not affiliated with Bethesda Softworks, ZeniMax Media, or Microsoft.
- `privacy.html` — privacy policy, last updated July 30, 2026. It says the app is offline-first and does not require an account for core features; that saved builds, favorites, recent searches, fishing progress markers, and cached wiki lookups are stored on the device; that online lookup requests publicly available wiki or community pages and may cache the result; that Theorycraft Pack purchases are handled by Apple In-App Purchase; and that the current build does not include third-party advertising SDKs or analytics trackers.

Those privacy and support statements describe the app. This repository only hosts the pages.

## Structure

Each page is a single HTML file with inline CSS. There is no JavaScript, shared stylesheet, package manifest, bundler, or build script.

`.nojekyll` is an empty file so GitHub Pages serves the files as-is and does not run Jekyll.

`.github/workflows/pages.yml` is the only deploy configuration in the repo.

## Run locally

No install or build step. Open `index.html` in a browser, or serve this directory with any static file server. The pages link to each other with relative URLs, so either works.

## Deploy

A push to `main` runs `.github/workflows/pages.yml` (`Deploy Pages`). The job checks out the repo, runs `actions/configure-pages`, uploads the repository root (`path: .`) as the Pages artifact, and deploys it with `actions/deploy-pages`. There is no compile step.

Pages for this repo is set to build from that workflow (branch `main`, path `/`). There is no `CNAME` file, and no custom domain is configured.
