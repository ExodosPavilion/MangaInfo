# The series file is our own schema, not Mylar's series.json

Series-level facts live in `MangaSeries.json`, with a schema of our own. Mylar's `series.json` is the only existing series-level file that readers import, but it is built around ComicVine and has no titles list, creators, genres, origin or demographic; Komga also rejects a `series.json` that lacks Mylar's mandatory fields. We do not extend it and do not aim for Komga compatibility; a separate plugin system will connect readers to the format.

## Considered options

- **Extend Mylar's `series.json`**: Komga could read part of it, but the file would have to carry Mylar's mandatory ComicVine fields.
- **Our own schema in a file named `series.json`**: Mylar writes a file of that name into the same folder, so the two tools would overwrite each other.
- **Our own schema in `MangaSeries.json`** (chosen).

## Consequences

- No reader imports the series file without a plugin.
- The series file is JSON and the MangaInfo file is XML. The two share field names, in camelCase and PascalCase.
