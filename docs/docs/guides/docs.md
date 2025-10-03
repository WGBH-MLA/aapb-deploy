# Documentation
The `docs/` directory contains all the files for the documentation website, built with [mkdocs](https://www.mkdocs.org/) and hosted on GitHub Pages.



## Local Development
To build and serve the documentation locally, you need to have Python and `uv` installed. 

### 1. Install `uv`

```sh
pip install uv
```

### 2. Clone the repository and navigate to the `docs/` directory:
```sh
git clone https://github.com/WGBH-MLA/aapb-deploy.git
cd aapb-deploy/docs/
```

### 3. Sync the dependencies:

```sh
uv sync
```

### 4. Run the mkdocs server:

```sh
uv run mkdocs serve
```

The documentation can be accessed at [localhost:8000](http://localhost:8000)

Changes to the `docs/` files will be rebuilt automatically and reloaded in the browser.


## Pushing changes
To update the published documentation, commit your changes to the `docs` branch and push them to the remote repository:

This will trigger the `docs.yaml` GitHub Actions workflow to build and deploy the updated documentation to GitHub Pages.

Merging the `docs` branch into the `main` branch will also trigger the workflow to re-deploy the latest version of the documentation.

## Version numbers
Version numbers in the documentation are managed using [mike](https://github.com/jimporter/mike). This allows multiple versions of the documentation to be maintained and accessed independently, e.g. `v0.1`, `v0.2`, etc.


### e.g., Adding a new version

To add a new version (e.g. `v0.2`) and set it as the latest version, run:

```sh
mike deploy -u v0.2 latest
```

This will create a new version of the documentation and update the `latest` alias to point to this new version. These changes will be added to the local `gh-pages` branch of the repository.

### Test new version locally
```sh
mike serve
```
Visit [localhost:8000](http://localhost:8000) and test the new version of the documentation.

### Publishing the new version
To publish the new version to GitHub Pages, push the `gh-pages` branch to the remote repository:

```sh
git push origin gh-pages
```

The `docs.yaml` GitHub Actions workflow will automatically deploy the updated documentation to GitHub Pages.