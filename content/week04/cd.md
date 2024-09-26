# Continuous Deployment

Example job:

```yaml
name: CD

on:
  workflow_dispatch:
  release:
    types:
      - published

jobs:
  dist:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build SDist and wheel
        run: pipx run build

      - uses: actions/upload-artifact@v3
        with:
          path: dist/*

  publish:
    needs: [dist]
    runs-on: ubuntu-latest
    if: github.event_name == 'release' && github.event.action == 'published'

    steps:
      - uses: actions/download-artifact@v3
        with:
          name: artifact
          path: dist

      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository_url: https://test.pypi.org/legacy/
```

This workflow is triggerable manually (by clicking in the web interface), as
well as on any "GitHub Release" (which uses or creates a Git tag, too).

This workflow has two jobs. One builds the artifacts (an SDist and a wheel), and
the other takes those artifacts and pushes them to PyPI (test PyPI in this case,
just in case!) The second job only runs if the first succeeds. It also only runs
if this is a release; otherwise, if you triggered it manually, you can manually
download the files from the first job.

This does not have to be in two jobs, but this does scale a bit better if you
need to do something more complex, like build binaries.

If you aren't setting up Trusted Publishing on the PyPI/TestPyPI sites, then
`password: ${{ secrets.pypi_password }}` can be used to pass in a token.
