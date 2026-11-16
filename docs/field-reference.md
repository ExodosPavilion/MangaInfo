# Field reference (version 1.0.0)

This document describes every field of the two files of the format. The terms are defined in [`GLOSSARY.md`](../GLOSSARY.md).

| | MangaInfo file | Series file |
|---|---|---|
| File name | `MangaInfo.xml` | `MangaSeries.json` |
| Location | Root of the archive | Series folder, beside the archives of the series |
| Describes | One unit | One series |
| Schema | [`schema/1/MangaInfo.xsd`](../schema/1/MangaInfo.xsd) | [`schema/1/MangaSeries.schema.json`](../schema/1/MangaSeries.schema.json) |
| Identifier | Namespace `https://exodospavilion.github.io/MangaInfo/1` | `$id` `https://exodospavilion.github.io/MangaInfo/1/MangaSeries.schema.json` |

File names are exact and case-sensitive. A series folder holds one series.

Both files use the same name for the same concept. The MangaInfo file writes element names in PascalCase (`OriginalLanguage`) and attribute names in camelCase (`language`). The series file writes keys in camelCase (`originalLanguage`).

Both schemas reject a field that they do not know. Tool data goes in the [extensions](#extensions) container.

## Rules that the schemas do not enforce

A validator cannot check these rules. A tool that writes files must obey them.

1. **Primary title.** Each title list has exactly one primary title. The XML schema enforces "at most one" only. The JSON schema enforces the full rule.
2. **Day needs month.** A date with a day must also have a month. The JSON schema enforces this rule. The XML schema does not.
3. **Standalone units.** A unit of type `oneShot` or `gallery` has a `Description` and no series file. A unit of type `volume`, `chapter` or `chapterRange` has a `Series` element. The XML schema requires one of the two elements, but it does not connect the choice to the unit type.
4. **Series file wins.** If the series identity in a MangaInfo file is different from the series file, the series file is correct.
5. **Overrides.** `ContentRating`, `ReadingMode` and `CensorshipState` inside `Unit` replace the series value for that unit only.
6. **Unknown means absent.** No field has a value for "unknown", except `publicationStatus`. Omit a field that you do not know.

## Version

| File | Field | Rule |
|---|---|---|
| MangaInfo file | `version` attribute on `MangaInfo` | Mandatory. Format `1.x.y`. |
| Series file | `version` | Mandatory. Format `1.x.y`. |

The value is the schema version that the file obeys. A change that breaks old files increases the first number, and also changes the namespace and the `$id`.

## MangaInfo file

The root element `MangaInfo` has three children, in this order:

| Element | Mandatory | Contents |
|---|---|---|
| `Unit` | Yes | The facts about this unit. |
| `Series` or `Description` | Yes, one of them | `Series` is the series identity. `Description` is the full description of a standalone unit. |
| `Extensions` | No | Tool data. |

The children of `Unit`, `Series` and `Description` can be in any order.

### Unit

| Field | Type | Notes |
|---|---|---|
| `type` (attribute) | Unit type | Mandatory. See [unit type](#unit-type). |
| `Volume` | String | The volume number. A string, so `3.5` is possible. |
| `FirstChapter` | String | The first chapter in the unit. For a single chapter, give this field only. |
| `LastChapter` | String | The last chapter in the unit. |
| `Title` | String | The title of this unit, in the language of the unit. |
| `ReleaseDate` | [Date](#date) | The release date of this edition of the unit. |
| `Language` | Language tag | The language of the pages in the archive. |
| `Isbn` | String | ISBN-10 or ISBN-13, with or without hyphens. |
| `PageCount` | Positive integer | |
| `Publisher` | `Name`, optional `Imprint` | The publisher of this edition. |
| `ScanlationGroups` | List of `ScanlationGroup` strings | |
| `Creators` | List of [creators](#creator) | Creators of this unit only, such as its translator. |
| `ContentRating` | [Content rating](#content-rating) | Override. |
| `ReadingMode` | [Reading mode](#reading-mode) | Override. |
| `CensorshipState` | [Censorship state](#censorship-state) | Override. |
| `Pages` | List of `Page` | See below. |

A `Page` has attributes only:

| Attribute | Type | Notes |
|---|---|---|
| `index` | Integer from 0 | Mandatory. The position of the page in the archive. Each index occurs one time only. |
| `type` | [Page type](#page-type) | Default `story`. |
| `doublePage` | Boolean | Default `false`. |

List only the pages that are not a normal single story page.

### Series (series identity)

| Field | Type | Notes |
|---|---|---|
| `Titles` | List of [titles](#title) | Mandatory. Only the primary title is necessary. |
| `ExternalIds` | List of [external IDs](#external-id) | |
| `Format` | [Format](#format) | |
| `OriginalLanguage` | Language tag | |
| `ReadingMode` | [Reading mode](#reading-mode) | |
| `ContentRating` | [Content rating](#content-rating) | |

### Description (standalone unit)

`Description` has the fields of the [description](#description-fields) table below, with PascalCase names. Each list has a container element and one child element for each entry, for example `Genres` with `Genre` children.

## Series file

The series file is one JSON object. It has the [description fields](#description-fields) and the [series-only fields](#series-only-fields) at the top level. It can also have a `$schema` key.

## Description fields

These fields are in the series file and in the `Description` of a standalone unit.

| Series file key | MangaInfo element | Type | Notes |
|---|---|---|---|
| `titles` | `Titles` / `Title` | List of [titles](#title) | Mandatory. |
| `creators` | `Creators` / `Creator` | List of [creators](#creator) | |
| `summaries` | `Summaries` / `Summary` | List of text with a mandatory `language` | One entry for each language. |
| `genres` | `Genres` / `Genre` | List of strings | Broad categories. |
| `tags` | `Tags` / `Tag` | List of [tags](#tag) | Specific labels. |
| `characters` | `Characters` / `Character` | List of strings | Names only. |
| `externalIds` | `ExternalIds` / `ExternalId` | List of [external IDs](#external-id) | |
| `links` | `Links` / `Link` | List of [links](#link) | |
| `covers` | `Covers` / `Cover` | List of [covers](#cover) | |
| `format` | `Format` | [Format](#format) | |
| `publicationType` | `PublicationType` | [Publication type](#publication-type) | |
| `demographic` | `Demographic` | [Demographic](#demographic) | Omit when none applies. |
| `contentRating` | `ContentRating` | [Content rating](#content-rating) | |
| `readingMode` | `ReadingMode` | [Reading mode](#reading-mode) | |
| `censorshipState` | `CensorshipState` | [Censorship state](#censorship-state) | |
| `originCountry` | `OriginCountry` | ISO 3166-1 two-letter code, uppercase | For example `JP`, `KR`, `TW`. |
| `originalLanguage` | `OriginalLanguage` | Language tag | For example `ja`, `ko`, `zh-Hant`. |
| `parodies` | `Parodies` / `Parody` | List of name with optional external IDs | The works that a derivative work is based on. |
| `circles` | `Circles` / `Circle` | List of name with optional external IDs | |
| `event` | `Event` | `name` with optional `date` | For example "Comiket 103". |

## Series-only fields

These fields are in the series file only.

| Key | Type | Notes |
|---|---|---|
| `publicationStatus` | [Publication status](#publication-status) | |
| `startDate`, `endDate` | [Date](#date) | The first and last publication dates of the original. |
| `totalVolumes`, `totalChapters` | Integer from 1 | Omit when unknown. |
| `publishers` | List of `name`, optional `language`, optional `imprint` | One entry for each edition. |
| `magazines` | List of `name`, optional `startDate`, optional `endDate` | The magazines where the chapters first appeared. |
| `licensedLanguages` | List of language tags | Languages that have an official licensed edition. |
| `relations` | List of [relations](#relation) | |
| `extensions` | Object | See [extensions](#extensions). |

## Shapes

### Title

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Text | `text` | Element text | Mandatory. |
| Language | `language` | `language` attribute | Language tag. A romanized title uses a script subtag: `ja-Latn`, `ko-Latn`, `zh-Latn`. |
| Kind | `kind` | `kind` attribute | `official` (default), `alternative` or `abbreviated`. |
| Primary | `primary: true` | `primary="true"` | Only on the primary title. The value `false` is not permitted; omit the field. |

### Creator

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Name | `name` | `Name` | Mandatory. |
| Role | `role` | `role` attribute | Mandatory. See [role](#role). |
| Note | `note` | `Note` | Free text, for example "Volumes 1 to 41". |
| External IDs | `externalIds` | `ExternalIds` | The creator at a provider. |

A creator with two roles has two entries.

### Tag

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Name | `name` | Element text | Mandatory. |
| Namespace | `namespace` | `namespace` attribute | States who or what the tag applies to, for example `female` or `male`. |
| Spoiler | `spoiler` | `spoiler` attribute | Boolean. Default `false`. |

### External ID

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Provider | `provider` | `provider` attribute | Mandatory. A lowercase key: letters, digits and hyphens. |
| ID | `id` | Element text | Mandatory. Always a string. |

Recommended provider keys. A key that is not in this table is valid.

| Key | Provider | Key | Provider |
|---|---|---|---|
| `anilist` | AniList | `hikka` | Hikka |
| `mal` | MyAnimeList | `comick` | Comick |
| `mangabaka` | MangaBaka | `mangadex` | MangaDex |
| `mangaupdates` | MangaUpdates | `nhentai` | nhentai |
| `kitsu` | Kitsu | `ehentai` | E-Hentai |
| `shikimori` | Shikimori | `anime-planet` | Anime-Planet |
| `bangumi` | Bangumi | | |

### Link

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Address | `url` | Element text | Mandatory. Starts with `http://` or `https://`. |
| Kind | `kind` | `kind` attribute | `official`, `retailer`, `info`, `social` or `other`. |
| Language | `language` | `language` attribute | The language of the page. |

### Cover

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Address | `url` | Element text | Mandatory. |
| Volume | `volume` | `volume` attribute | The volume that the cover belongs to. Omit for series art. |
| Language | `language` | `language` attribute | The language of the edition. |

A reader takes the cover of an archive from the page list first.

### Date

| Part | Series file | MangaInfo file | Notes |
|---|---|---|---|
| Year | `year` | `year` attribute | Mandatory. |
| Month | `month` | `month` attribute | 1 to 12. |
| Day | `day` | `day` attribute | 1 to 31. Needs a month. |

### Relation

| Part | Key | Notes |
|---|---|---|
| Type | `type` | Mandatory. See [relation type](#relation-type). |
| Title | `title` | The primary title of the other series. |
| External IDs | `externalIds` | The other series at a provider. |

A relation needs a title, or external IDs, or both.

### Extensions

A tool keeps its own data below its own name. The schemas do not examine the contents.

```json
"extensions": {
  "example-sync-tool": { "lastSync": "2026-11-16" }
}
```

```xml
<Extensions>
  <Extension tool="example-sync-tool">
    <LastSync>2026-11-16</LastSync>
  </Extension>
</Extensions>
```

In the series file, the value for each tool is an object. In the MangaInfo file, each tool has one `Extension` element.

## Value lists

### Unit type

| Value | The archive contains |
|---|---|
| `volume` | One collected book from the publisher. |
| `chapter` | One chapter. |
| `chapterRange` | Several consecutive chapters that are not an official volume. |
| `oneShot` | A complete work that has no series. |
| `gallery` | A standalone unit that has no series, typical for doujinshi. |

### Page type

`cover`, `backCover`, `story`, `contents`, `credits`, `advertisement`, `other`.

### Role

| Value | Meaning |
|---|---|
| `story` | Wrote the story. |
| `art` | Drew the art. |
| `storyAndArt` | Did both. |
| `originalCreator` | Created the work that this work adapts. |
| `characterDesign` | Designed the characters. |
| `translator` | Translated an edition. |
| `letterer` | Lettered an edition. |
| `editor` | Edited the work or an edition. |
| `assistant` | Assisted the artist. |
| `other` | A different role. Describe it in the note. |

### Format

| Value | Meaning |
|---|---|
| `manga` | A work in the Japanese tradition. |
| `manhwa` | A work in the Korean tradition. |
| `manhua` | A work in the Chinese tradition. |
| `oel` | An original English-language work in the manga style. |
| `other` | A work from a different tradition. |

Format does not state how the work was published or how long it is. See publication type and unit type.

### Publication type

| Value | Meaning |
|---|---|
| `commercial` | A publisher released the work. |
| `doujinshi` | The creators published the work themselves. |
| `webcomic` | The work was first published on the web. |

### Publication status

`upcoming`, `ongoing`, `hiatus`, `completed`, `cancelled`, `unknown`. The status is that of the original publication, not of a translation.

### Demographic

`shounen`, `shoujo`, `seinen`, `josei`, `kids`.

### Content rating

| Value | Meaning |
|---|---|
| `safe` | No sexual content. |
| `suggestive` | Sexual themes, without explicit imagery. |
| `erotica` | Explicit nudity or sexual content that is not the main purpose of the work. |
| `pornographic` | Explicit sexual content that is the main purpose of the work. |

The value is the highest level of sexual content in the series or unit. Violence and other warnings are tags.

### Reading mode

| Value | Meaning |
|---|---|
| `rightToLeft` | Pages, read from right to left. |
| `leftToRight` | Pages, read from left to right. |
| `vertical` | Pages, read from top to bottom, one page at a time. |
| `longStrip` | One continuous vertical scroll. |

No provider supplies a reading mode. A tool can set a default from the format: `manga` gives `rightToLeft`, and a `webcomic` in the `manhwa` or `manhua` format usually gives `longStrip`.

### Censorship state

| Value | Meaning |
|---|---|
| `uncensored` | The official release has no censorship. |
| `decensored` | Fans removed the censorship from an official release. |
| `mosaic` | Mosaic censorship. |
| `bars` | Bar censorship. |
| `other` | A different type of censorship. |

### Relation type

The type states what the other series is to this series.

| Value | The other series is |
|---|---|
| `prequel` | Earlier in the story. |
| `sequel` | Later in the story. |
| `parentStory` | The main story that this series comes from. |
| `sideStory` | A story beside the main story of this series. |
| `spinOff` | A separate story that comes from this series. |
| `alternativeVersion` | A different telling of the same story, such as a remake. |
| `adaptation` | An adaptation of this series, or the work that this series adapts. |
| `sharedUniverse` | In the same world, with a separate story. |
| `other` | Related in a different way. |

## Not in version 1

Scores, ranks and other volatile data. Anime adaptation details. Adaptation source. Character roles. Tag relevance. Audience-style age ratings. Novels.

## Examples

| Example | Files |
|---|---|
| A volume of a manga | [`examples/manga-volume/`](../examples/manga-volume/) |
| A fan-translated chapter of a manhwa | [`examples/manhwa-chapter/`](../examples/manhwa-chapter/) |
| A doujinshi gallery (standalone, so it has no series file) | [`examples/doujinshi-gallery/`](../examples/doujinshi-gallery/) |

The works, people and IDs in the examples are invented.
