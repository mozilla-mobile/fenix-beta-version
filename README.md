# extract-major-beta-version

This _GitHub Action_ determines the current major Beta version.


To do this the *GITHUB_REPOSITORY* this is applied to has to:

- have a [_release_](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases) following the following naming scheme

  ```
  \d+.0.0-beta.\d+
  ```
- have a file named `version.txt` in the project root containing the latest beta version name (following the same naming scheme as above).

<br>

It publishes the last major version of a beta release (like `88`) in the `beta_version` output, which can then be used in other _GitHub Actions_.

Example usage:

```
      - name: "Discover the last beta release major version"
        id: extract-major-beta-version
        uses: mozilla-mobile/extract-major-beta-version@3.0.0

      - name "Print the version number"
        run: "The current _major beta_ number is $${{steps.extract-major-beta-version.outputs.beta_version}}"
```

This _GitHub Action_ is used in in

- the [github.com/mozilla-mobile/fenix/blob/master/.github/workflows/sync-strings.yml](https://github.com/mozilla-mobile/fenix/blob/master/.github/workflows/sync-strings.yml) workflow
- the [github.com/mozilla-mobile/focus-android/blob/master/.github/workflows/sync-strings.yml](https://github.com/mozilla-mobile/focus-android/blob/master/.github/workflows/sync-strings.yml) workflow.


## Bump dependencies

Just run the following command line. You may need to change the python version to follow what is in `Dockerfile`.

```
docker run -t -v "$PWD:/src" -w /src python:3.9 bash -cx "pip install pip-tools && cd /src/ && pip-compile --upgrade --generate-hashes --output-file requirements.txt requirements.in"
```
