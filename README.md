# GitHub Repo Traffic Stats

A simple tool to collect and view GitHub repos traffic history longer than 14 days using GitHub Actions.

[![A screenshot of the website.](dashboard_screenshot.png)](https://piebro.github.io/github-repo-traffic-stats)

## Features

- Collect traffic metrics for all your repos using GitHub Actions
- A simple web interface to view the stats locally or hosted using GitHub Pages
- A demo website is here: [piebro.github.io/github-repo-traffic-stats](https://piebro.github.io/github-repo-traffic-stats)

## How to use

1. Fork the repo
2. Delete the existing data in the `data` and `preview_plots` folders
3. Change the "owner" in `github_username.txt` and change the websites in `index.html`
4. Create a GitHub token to access this API: https://docs.github.com/en/rest/metrics/traffic
5. Add the token as an Action secret to the repo and name it `GH_TOKEN`
6. In the settings, enable the Read and Write Action Permissions (to allow the action to push the data to the repo)

All your public repos should now be queried at 23:30 UTC every day.
The data is stored in the data folder.
You can enable GitHub Pages to host the dashboard or host it locally using `python -m http.server` in the project root folder.

## Contributing

Contributions are welcome. Open an Issue if you want to report a bug, have an idea or want to propose a change.

## Website Statistics

There is lightweight tracking with [Plausible](https://plausible.io/about) for the [website](https://piebro.github.io/github-repo-traffic-stats/) to get info about how many people are visiting. Everyone who is interested can look at these stats here: https://plausible.io/piebro.github.io%2Fgithub-repo-traffic-stats?period=30d. Only users without an AdBlocker are counted, so these statistics are underestimating the actual count of visitors. I would guess that quite a few people (including me) visiting the site have an AdBlocker.

## License

All code in this project is licensed under the MIT License.
