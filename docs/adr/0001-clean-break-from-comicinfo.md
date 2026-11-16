# The MangaInfo file is a clean break from ComicInfo.xml

`MangaInfo.xml` does not extend or stay compatible with `ComicInfo.xml`. ComicInfo holds every multi-valued field as one comma-separated string, has fixed creator roles from US comics, and has no place for origin, publication status, demographic, magazines, typed external IDs or typed titles; a superset would have to keep those shapes. We chose our own structure, with repeated elements and attributes, in its own XML namespace.

## Considered options

- **Superset of ComicInfo** (keep its element names, add ours): existing readers would understand part of the file, but every list would stay a comma-separated string and the US-comics fields would stay.
- **Clean break** (chosen): no existing reader understands the file.

## Consequences

- An archive can hold a `ComicInfo.xml` beside the `MangaInfo.xml` for readers that know only ComicInfo. The format does not define how to keep the two in step.
- Reader support comes from plugins or converters, not from the format.
