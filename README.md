# fenix-beta-version

This _GitHub Action_ determines the the current Fenix Beta version.

It publishes the major Fenix Beta release number in the `fenix-beta-version` output, which can then be used in other _GitHub Actions_.

Example usage:

```
      - name: "Discover Fenix Beta Version"
        id: fenix-beta-version
        uses: mozilla-mobile/fenix-beta-version@1.0.0

      - name "Print the version number"
        run: "The current Fenix Beta is $${{steps.fenix-beta-version.outputs.fenix-beta-version}}"
```

This _GitHub Action_ is used in in the [github.com/mozilla-mobile/fenix/blob/master/.github/workflows/sync-strings.yml](https://github.com/mozilla-mobile/fenix/blob/master/.github/workflows/sync-strings.yml) workflow.
