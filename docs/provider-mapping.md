# Provider mapping (version 1.0.0)

This document states how to convert the data of twelve providers to the fields and values of the format. The terms are defined in [`GLOSSARY.md`](../GLOSSARY.md), and the fields in [`field-reference.md`](field-reference.md).

The provider field names and value lists come from [`metadata-requirements-research.md`](../metadata-requirements-research.md) (research date 2026-11-16). This document adds the conversions. No tool has run these conversions against live provider data.

## How to read the tables

| Mark | Meaning |
|---|---|
| (no mark) | The provider value and our value have the same meaning. |
| **≈** | An approximation. The provider value is wider or narrower than ours. This is a judgement, not a provider statement. |
| **?** | Unknown. The research did not confirm the provider's value list or its meaning. Do not write a conversion until someone confirms it. |
| **—** | The provider has no such data. Omit our field. |
| *out* | The entry is not a comic (a novel, an artbook). The format does not cover it. |

## Providers

| Key | Provider | Research confidence | Limits on use |
|---|---|---|---|
| `mangabaka` | MangaBaka | Specification and live responses read | Own data is CC BY-NC-SA 4.0; credit necessary |
| `mal` | MyAnimeList (official API v2) | Specification only; live calls need a client ID | Commercial use needs approval; agreement read as a summary only |
| `anilist` | AniList | Live schema read | No mass collection; licence necessary above a revenue limit |
| `kitsu` | Kitsu | Live responses and server source read | No terms found |
| `mangaupdates` | MangaUpdates | Specification and live responses read | Credit and caching necessary |
| `shikimori` | Shikimori | Live schema read | 5 requests per second, 90 per minute |
| `bangumi` | Bangumi | Specification and live responses read | No terms found |
| `hikka` | Hikka | Specification and live responses read | No terms found |
| `comick` | Comick (comick.dev) | Detail response is untyped; shape from one live sample | No terms found; relation to the old comick.io is not confirmed |
| `mangadex` | MangaDex | Specification and live responses read | Terms not read |
| `nhentai` | nhentai (API v2) | Specification and live tag calls read | Terms not read |
| `ehentai` | E-Hentai | **Community wiki only**; the API itself was not read | Terms not read |

All E-Hentai rows in this document carry that limit. Treat them as leads.

## Format

Our values: `manga`, `manhwa`, `manhua`, `oel`, `other`. Some providers put publication type and unit type in the same list; the last column shows what to set in addition.

| Provider | Provider field | Provider value | Format | Also set |
|---|---|---|---|---|
| MangaBaka | `type` | `manga`, `manhwa`, `manhua`, `oel`, `other` | Same value | |
| | | `novel` | *out* | |
| MyAnimeList | `media_type` | `manga`, `manhwa`, `manhua`, `oel` | Same value | |
| | | `one_shot` | — | Unit type `oneShot` |
| | | `doujinshi` | — | Publication type `doujinshi` |
| | | `novel` | *out* | |
| | | `unknown` | — | |
| AniList | `format` + `countryOfOrigin` | `MANGA` + `JP` | `manga` | |
| | | `MANGA` + `KR` | `manhwa` | |
| | | `MANGA` + `CN` or `TW` | `manhua` **≈** | |
| | | `MANGA` + other country | `other` **≈** | |
| | | `ONE_SHOT` | By country, as above | Unit type `oneShot` |
| | | `NOVEL` | *out* | |
| Kitsu | `subtype` | `manga`, `manhwa`, `manhua`, `oel` | Same value | |
| | | `oneshot` | — | Unit type `oneShot` |
| | | `doujin` | — | Publication type `doujinshi` |
| | | `novel` | *out* | |
| MangaUpdates | `type` | `Manga`, `Manhwa`, `Manhua`, `OEL` | Same value, lowercase | |
| | | `Doujinshi` | — | Publication type `doujinshi` |
| | | `Filipino`, `Indonesian`, `Thai`, `Vietnamese`, `Malaysian`, `Nordic`, `French`, `Spanish`, `German`, `Russian` | `other` | |
| | | `Artbook`, `Drama CD`, `Novel` | *out* | |
| Shikimori | `kind` | `manga`, `manhwa`, `manhua` | Same value | |
| | | `one_shot` | — | Unit type `oneShot` |
| | | `doujin` | — | Publication type `doujinshi` |
| | | `light_novel`, `novel` | *out* | |
| Bangumi | `type` 1 + category | `1001` (comic) | — | The provider does not state a tradition |
| | | `1002` (novel), `1003` (illustration), `0` | *out* | |
| Hikka | `media_type` | `manga`, `manhwa`, `manhua` | Same value | |
| | | `one_shot` | — | Unit type `oneShot` |
| | | `doujin` | — | Publication type `doujinshi` |
| Comick | `media_type` + `country` | `manga` + `jp` | `manga` | |
| | | `manga` + `kr` | `manhwa` | |
| | | `manga` + `cn` | `manhua` | |
| | | `manga` + other country | `other` **≈** | |
| | | `novel`, `anime` | *out* | |
| MangaDex | `originalLanguage` | `ja` | `manga` **≈** | |
| | | `ko` | `manhwa` **≈** | |
| | | `zh`, `zh-hk` | `manhua` **≈** | |
| | | `en` | `oel` **≈** | |
| | | other | `other` **≈** | |
| | format tag | `Doujinshi`, `Self-Published` | — | Publication type `doujinshi` |
| | | `Web Comic` | — | Publication type `webcomic` |
| | | `Long Strip` | — | Reading mode `longStrip` |
| nhentai | `category` tag | `doujinshi` | — | Publication type `doujinshi`; unit type `gallery` |
| | | `manga` | — | Publication type **?** |
| E-Hentai | `category` | `Doujinshi` | — | Publication type `doujinshi`; unit type `gallery` |
| | | `Manga` | — | Publication type **?** |
| | | `Artist CG`, `Game CG`, `Western`, `Image Set`, `Non-H`, `Cosplay`, `Asian Porn`, `Misc`, `Private` | *out* **≈** | |

Notes:

- A provider row with "—" under Format and a publication type or unit type gives no tradition. Take the format from a different provider, or from the origin country.
- MangaDex has no format field. The conversion from `originalLanguage` is an inference.
- nhentai and E-Hentai give the language of the gallery, not the tradition of the work.

## Publication status

Our values: `upcoming`, `ongoing`, `hiatus`, `completed`, `cancelled`, `unknown`.

| Provider | Provider field | `upcoming` | `ongoing` | `hiatus` | `completed` | `cancelled` | `unknown` |
|---|---|---|---|---|---|---|---|
| MangaBaka | `status` | `upcoming` | `releasing` | `hiatus` | `completed` | `cancelled` | `unknown` |
| MyAnimeList | `status` | `not_yet_published` | `currently_publishing` | — | `finished` | — | — |
| AniList | `status` | `NOT_YET_RELEASED` | `RELEASING` | `HIATUS` | `FINISHED` | `CANCELLED` | — |
| Kitsu | `status` | `tba`, `unreleased`, `upcoming` **≈** | `current` | — | `finished` | — | — |
| MangaUpdates | `completed` + `status` text | — | `completed: false` **≈** | **?** | `completed: true` | **?** | — |
| Shikimori | `status` | `anons` | `ongoing` | `paused` | `released` | `discontinued` | — |
| Bangumi | — | — | — | — | — | — | — |
| Hikka | `status` | `announced` | `ongoing` | `paused` | `finished` | `discontinued` | — |
| Comick | `status` (integer) | — | `1` | `4` | `2` | `3` | — |
| MangaDex | `status` | — | `ongoing` | `hiatus` | `completed` | `cancelled` | — |
| nhentai | — | — | — | — | — | — | — |
| E-Hentai | — | — | — | — | — | — | — |

Notes:

- MyAnimeList and Kitsu have no value for hiatus or cancelled. A series on hiatus shows as ongoing there.
- MangaUpdates `status` is free text, for example "43 Volumes (Ongoing)". The words that it uses for hiatus and cancelled were not confirmed.
- Comick has a separate translation status. Our publication status is that of the original publication only.

## Demographic

Our values: `shounen`, `shoujo`, `seinen`, `josei`, `kids`.

| Provider | Where it is | Conversion |
|---|---|---|
| MangaBaka | `genres` (deprecated) values `shounen`, `shoujo`, `seinen`, `josei`; tag group "Audience Demographics" | Same value. The tag names in the group are **?** |
| MyAnimeList | Entries in `genres` | **?** The official specification does not list the genre names |
| AniList | Tags in category `Demographic`: `Shounen`, `Shoujo`, `Seinen`, `Josei`, `Kids` | Same value, lowercase |
| Kitsu | Genres or categories | **?** |
| MangaUpdates | `genres`: `Shounen`, `Shoujo`, `Seinen`, `Josei` | Same value, lowercase. The other genres that the provider marks as demographic (`Lolicon`, `Shotacon`, `Shoujo Ai`, `Shounen Ai`, `Yaoi`, `Yuri`) become genres or tags |
| Shikimori | Genres with `kind: demographic`: `Shounen`, `Shoujo`, `Seinen`, `Josei`, `Kids` | Same value, lowercase |
| Bangumi | — | — |
| Hikka | Genres with `type: demographic`: `Shounen`, `Shoujo`, `Seinen`, `Josei`, `Kids` | Same value, lowercase |
| Comick | `demographic` (integer) | `1` shounen, `2` shoujo, `3` seinen, `4` josei, `5` omit |
| MangaDex | `publicationDemographic` | `shounen`, `shoujo`, `seinen`, `josei`: same value |
| nhentai, E-Hentai | — | — |

A series with more than one demographic at a provider: use the first, and put the others in tags.

## Content rating

Our values: `safe`, `suggestive`, `erotica`, `pornographic`.

| Provider | Provider field | Provider value | Content rating |
|---|---|---|---|
| MangaBaka | `content_rating` | `safe`, `suggestive`, `erotica`, `pornographic` | Same value |
| Comick | `content_rating` | `safe`, `suggestive`, `erotica`, `pornographic` | Same value |
| MangaDex | `contentRating` | `safe`, `suggestive`, `erotica`, `pornographic` | Same value |
| MyAnimeList | `nsfw` | `white` | `safe` **≈** |
| | | `gray` | `suggestive` **≈** |
| | | `black` | `erotica` or `pornographic`: the provider does not separate them **≈** |
| AniList | `isAdult` + `genres` | `isAdult: true` | `pornographic` **≈** |
| | | `isAdult: false`, genre `Ecchi` | `suggestive` **≈** |
| | | `isAdult: false`, no `Ecchi` | `safe` **≈** |
| Kitsu | `ageRating` | `G`, `PG` | `safe` **≈** |
| | | `R` | `suggestive` **≈** |
| | | `R18` | `erotica` or `pornographic`: the provider does not separate them **≈** |
| MangaUpdates | `genres` | `Hentai` | `pornographic` **≈** |
| | | `Adult`, `Smut` | `erotica` **≈** |
| | | `Ecchi`, `Mature` | `suggestive` **≈** |
| | | none of these | `safe` **≈** |
| Shikimori | `genres` | `Hentai` | `pornographic` **≈** |
| | | `Erotica` | `erotica` |
| | | `Ecchi` | `suggestive` **≈** |
| | | none of these | `safe` **≈** |
| Hikka | `genres` with `type: explicit` | `Hentai` | `pornographic` **≈** |
| | | `Erotica` | `erotica` |
| | | `Ecchi` | `suggestive` **≈** |
| | | none of these | `safe` **≈** |
| Bangumi | `nsfw` | `true` | `erotica` or `pornographic`: the provider does not separate them **≈** |
| | | `false` | `safe` or `suggestive` **≈** |
| nhentai | — | Every gallery | `pornographic` **≈** |
| E-Hentai | `category` | `Non-H` | `safe` or `suggestive` **≈** |
| | | other | `pornographic` **≈** |

Notes:

- Only MangaBaka, Comick and MangaDex use our scale. Prefer them when more than one provider has the series.
- Where a row says "the provider does not separate them", select `erotica`, and let a provider with the full scale replace it.
- Kitsu hides R18 entries from requests that have no account.

## Relation type

Our values: `prequel`, `sequel`, `parentStory`, `sideStory`, `spinOff`, `alternativeVersion`, `adaptation`, `sharedUniverse`, `other`.

| Our value | MangaBaka `relation_type` | MyAnimeList `relation_type` | AniList `relationType` | Kitsu `role` | MangaUpdates `relation_type` | Shikimori `relationKind` |
|---|---|---|---|---|---|---|
| `prequel` | `prequel` | `prequel` | `PREQUEL` | `prequel` | `Prequel` | `prequel` |
| `sequel` | `sequel` | `sequel` | `SEQUEL` | `sequel` | `Sequel` | `sequel` |
| `parentStory` | `parent`, `main` **≈** | `parent_story`, `full_story` **≈** | `PARENT` | `parent_story`, `full_story` **≈** | `Main Story` | `parent_story`, `full_story` **≈** |
| `sideStory` | `side_story` | `side_story` | `SIDE_STORY` | `side_story` | `Side Story` | `side_story` |
| `spinOff` | `spin_off` | — | `SPIN_OFF` | `spinoff` | `Spin-Off` | `spin_off` |
| `alternativeVersion` | `alternative`, `remake`, `reboot` **≈** | `alternative_version`, `alternative_setting` **≈** | `ALTERNATIVE` | `alternative_version`, `alternative_setting` **≈** | `Alternate Version` | `alternative_version`, `alternative_setting` **≈** |
| `adaptation` | `adaptation`, `source` | — | `ADAPTATION`, `SOURCE` | `adaptation` | `Adapted From` | `adaptation` |
| `sharedUniverse` | `series` **?** | — | `SAME_UNIVERSE` | — | — | — |
| `other` | `cameo`, `character_focus`, `compilation`, `contains`, `crossover`, `expansion`, `other`, `parody`, `summary`, `uncollected` **≈** | `summary` | `CHARACTER`, `SUMMARY`, `COMPILATION`, `CONTAINS`, `OTHER` | `summary`, `character`, `other` | `Part of Anthology`, `Full Anthology`, `Other` | `summary`, `character`, `other` |

Providers that are not in the table:

| Provider | State |
|---|---|
| Bangumi | The relation is free text. One value was seen: `系列` (a volume to its series). **?** |
| Hikka | — (a "has franchise" flag only) |
| Comick | **?** One value was seen: `Sequel`. The value list is not documented |
| MangaDex | **?** The research did not read its relation list |
| nhentai, E-Hentai | — (a `parody` tag gives the parody, not a relation) |

Notes:

- The provider type states what the other entry is to this one, as ours does. `SOURCE` and `Adapted From` are the reverse direction of `ADAPTATION`; both become `adaptation`, which does not record a direction.
- A relation to an entry that is not a comic (an anime, a novel) is outside the format. Drop it.
- The meaning of MangaBaka `series` is not confirmed.

## Field sources

Each table shows the provider field that fills each of our fields. A field that is not in a table has no source at that provider. No provider supplies reading mode, event or censorship state as a field; see the notes for each provider.

### MangaBaka

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `titles[]` (`language`, `traits`, `title`, `is_primary`) | `traits` `official` and `native` give kind `official`; `alternative` gives `alternative`. `is_primary` gives the primary title |
| Creators | `authors[]`, `artists[]` | Names only. `authors` gives role `story`, `artists` gives `art`; a name in both gives `storyAndArt` **≈** |
| Summaries | `description` | Language not stated; English **≈** |
| Genres, tags | `tags_v2[]` | `is_genre: true` gives a genre, otherwise a tag. `is_spoiler` gives the spoiler flag. Drop `weight` |
| External IDs | `id`; `source{}` | Keys: `anilist`, `anime_planet`, `kitsu`, `manga_updates`, `my_anime_list`, `shikimori` convert to our recommended keys |
| Links | `links_v2[]` (`url`, `type`, `language`) | `publisher` gives `official`; `retailer`, `info`, `social` same; `webplatform`, `news`, `other` give `other`; drop `piracy` |
| Covers | `cover.raw.url`; `/v1/series/{id}/images` | Images of type `volume` give covers with a volume |
| Format | `type` | See Format |
| Publication status | `status` | See Publication status |
| Content rating | `content_rating` | Same value |
| Original language | `original_language` | BCP 47 already |
| Start and end date | `published.start_date`, `published.end_date` | Full dates. Drop the day and month when `*_is_estimated` is true **≈** |
| Total volumes, chapters | `final_volume`, `total_chapters` | Strings in v1, numbers in v2 |
| Publishers | `publishers[]` (`name`, `language`) | One entry for each language |
| Licensed languages | `is_licensed` | `true` gives `en` |
| Relations | `relationships_v2[]` | See Relation type |

### MyAnimeList (official API v2)

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title`; `alternative_titles` (`en`, `ja`, `synonyms[]`) | `title` is primary, usually romanized (`ja-Latn` **≈**). `synonyms` give kind `alternative` |
| Creators | `authors[]` (`node`, `role`) | Role value list **?** |
| Summaries | `synopsis` | English |
| Genres | `genres[]` | Demographic entries are in the same list; names **?** |
| External IDs | `id` | Key `mal` |
| Covers | `main_picture.large` | |
| Format | `media_type` | See Format |
| Publication status | `status` | See Publication status |
| Content rating | `nsfw` | See Content rating |
| Start and end date | `start_date`, `end_date` | `YYYY`, `YYYY-MM` or `YYYY-MM-DD`: split into year, month, day |
| Total volumes, chapters | `num_volumes`, `num_chapters` | `0` means unknown: omit |
| Magazines | `serialization[]` | |
| Relations | `related_manga[]` | See Relation type |

### AniList

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title.romaji`, `title.english`, `title.native`; `synonyms[]` | `romaji` has a `-Latn` tag for the origin country. `synonyms` give kind `alternative`; their language is not stated |
| Creators | `staff.edges[]` (`role`, `node.name`) | Role is free text with a scope, for example "Story & Art (vols 1-41)". Convert the first part to our role **≈**; put the text in the note |
| Summaries | `description` | English |
| Genres | `genres[]` | |
| Tags | `tags[]` | `isMediaSpoiler` or `isGeneralSpoiler` gives the spoiler flag. Drop `rank` |
| Characters | `characters` | Names only |
| External IDs | `id`; `idMal` | Keys `anilist`, `mal` |
| Links | `externalLinks[]` (`url`, `type`, `language`) | `INFO` gives `info`, `SOCIAL` gives `social`, `STREAMING` gives `other` **≈** |
| Covers | `coverImage.extraLarge` | |
| Format | `format` + `countryOfOrigin` | See Format |
| Origin country | `countryOfOrigin` | ISO 3166-1 already |
| Publication status | `status` | See Publication status |
| Demographic | Tags in category `Demographic` | See Demographic |
| Content rating | `isAdult` | See Content rating |
| Start and end date | `startDate`, `endDate` | Year, month, day; each can be null |
| Total volumes, chapters | `volumes`, `chapters` | Null means unknown: omit |
| Licensed languages | `isLicensed` | `true` gives `en` **≈** |
| Relations | `relations` | See Relation type |
| Reading mode | Tag `Long Strip` | Gives `longStrip` **≈** |

### Kitsu

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `canonicalTitle`; `titles{}`; `abbreviatedTitles[]` | Keys of `titles` are locales: `en_jp` gives `ja-Latn`, `en_us` gives `en`. `abbreviatedTitles` give kind `abbreviated` |
| Creators | `staff` (`role`) | Role is free text |
| Summaries | `synopsis` | English |
| Genres | `genres` | |
| Tags | `categories` | |
| Characters | `characters` | Names only |
| External IDs | `id`; `mappings` (`externalSite`, `externalId`) | `myanimelist/manga` gives `mal`; `anilist/manga` gives `anilist` |
| Covers | `posterImage.original` | |
| Format | `subtype` | See Format |
| Publication status | `status` | See Publication status |
| Content rating | `ageRating` | See Content rating |
| Start and end date | `startDate`, `endDate` | |
| Total volumes, chapters | `volumeCount`, `chapterCount` | |
| Magazines | `serialization` | One string |
| Relations | `mediaRelationships` | See Relation type |

### MangaUpdates

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title`; `associated[].title` | Language not stated. `associated` give kind `alternative` |
| Creators | `authors[]` (`name`, `type`, `author_id`) | `Author` gives `story`, `Artist` gives `art`; a name with both gives `storyAndArt` |
| Summaries | `description` | English |
| Genres | `genres[]` | The demographic and content values move out; see Demographic and Content rating |
| Tags | `categories[]` | Drop the votes |
| External IDs | `series_id` | Key `mangaupdates` |
| Covers | `image.url.original` | |
| Format | `type` | See Format |
| Publication status | `completed`, `status` | See Publication status |
| Start date | `year` | Year only |
| Publishers | `publishers[]` (`publisher_name`, `type`) | `type` is a language name (`English`, `Japanese`); convert to a language tag. `Original` is the original language |
| Magazines | `publications[]` (`publication_name`) | |
| Licensed languages | `licensed` | `true` gives `en` |
| Relations | `related_series[]` | See Relation type |

### Shikimori

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `name`; `russian`; `english[]`; `japanese[]`; `synonyms[]` | `name` is romanized. `synonyms` give kind `alternative` |
| Creators | `personRoles` (`rolesEn[]`, `person`) | Role is free text |
| Summaries | `description` | Russian |
| Genres | Genres with `kind: genre` | |
| Tags | Genres with `kind: theme` | |
| Characters | `characterRoles` | Names only |
| External IDs | `id`; `malId` | Keys `shikimori`, `mal` (the two IDs are the same number) |
| Links | `externalLinks` (`kind`, `url`) | `official_site` gives `official`; `wikipedia`, `anime_news_network`, `myanimelist` and similar give `info`; `twitter` gives `social`; the others give `other` **≈** |
| Covers | `poster` | |
| Format | `kind` | See Format |
| Publication status | `status` | See Publication status |
| Demographic | Genres with `kind: demographic` | See Demographic |
| Content rating | Genres | See Content rating |
| Start and end date | `airedOn`, `releasedOn` | Year, month, day; each can be null |
| Total volumes, chapters | `volumes`, `chapters` | |
| Magazines | `publishers[]` | The provider calls magazines "publishers" |
| Licensed languages | `licensors[]` | A value gives `ru` **≈** |
| Relations | `related` | See Relation type |

### Bangumi

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `name`; `name_cn`; alias entries in `infobox` | `name` is the original title; `name_cn` is `zh-Hans` **≈** |
| Creators | `/persons` (`relation`, `career[]`) | `relation` is free Chinese text. `career` `mangaka` gives `storyAndArt` **≈**, `writer` gives `story`, `artist` and `illustrator` give `art` **≈** |
| Summaries | `summary` | Chinese **≈** |
| Tags | `tags[].name`; `meta_tags[]` | Drop the counts |
| Characters | `/characters` | Names only |
| External IDs | `id` | Key `bangumi` |
| Covers | `images.large` | |
| Format | category | See Format; no tradition |
| Content rating | `nsfw` | See Content rating |
| Start date | `date` | Full date |
| Total volumes | `volumes` | |
| Publishers | `infobox` key `出版社` | Seen on one volume only **?** |

Each volume is a separate entry at this provider. The release date, ISBN and page count of a unit come from the `infobox` of the volume entry (keys `发售日`, `ISBN`, `页数`); these keys were seen on one sample only.

### Hikka

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title_original`; `title_native`; `title_en`; `title_ua`; `synonyms[]` | `title_ua` is `uk`. `synonyms` give kind `alternative` |
| Creators | `authors[]` (`person`, `roles[]`) | Role names have English and Ukrainian forms; value list **?** |
| Summaries | `synopsis_en`; `synopsis_ua` | `en` and `uk` |
| Genres | Genres with `type: genre` | |
| Tags | Genres with `type: theme` | |
| Characters | `/manga/{slug}/characters` | Names only |
| External IDs | `slug`; `mal_id` | Keys `hikka`, `mal` |
| Links | `external[]` (`url`, `type`) | `general` gives `info` **≈**; `read` gives `other` **≈** |
| Covers | `image` | |
| Format | `media_type` | See Format |
| Publication status | `status` | See Publication status |
| Demographic | Genres with `type: demographic` | See Demographic |
| Content rating | Genres with `type: explicit`; `nsfw` | See Content rating |
| Start and end date | `start_date`, `end_date` | Seconds since 1970; gives a full date only |
| Total volumes, chapters | `volumes`, `chapters` | |
| Magazines | `magazines[]` | |
| Licensed languages | `translated_ua` | A fan translation, not a licence: do not use |

### Comick

The shape comes from one live response. Confirm each row before use.

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `comic.title`; `comic.md_titles[]` (`title`, `lang`, `is_default`) | `is_default` gives the primary title **?** |
| Creators | `authors[]`, `artists[]` | Names only; as for MangaBaka |
| Summaries | `comic.desc` | English |
| Genres | `comic.md_comic_md_genres[]` | `group` separates genre, theme and format entries |
| Tags | `comic.mu_comic_categories[]` | Drop the votes |
| External IDs | `comic.hid` or `slug`; `comic.links{}` | `al` gives `anilist`, `mal` gives `mal`, `kt` gives `kitsu`, `mu` gives `mangaupdates` **≈**; `ap` and `mb` are **?** |
| Covers | `comic.md_covers[]` (`vol`) | |
| Format | `media_type` + `country` | See Format |
| Origin country | `comic.country` | Lowercase: convert to uppercase |
| Original language | `comic.iso639_1` | |
| Publication status | `comic.status` | See Publication status |
| Demographic | `comic.demographic` | See Demographic |
| Content rating | `comic.content_rating` | Same value |
| Start and end date | `comic.year`, `comic.to_year` | Year only |
| Total volumes, chapters | `comic.final_volume`, `comic.final_chapter` | |
| Publishers | `comic.publishers[]`; `comic.mu_comics.mu_comic_publishers[]` | |
| Licensed languages | `comic.mu_comics.licensed_in_english` | `true` gives `en` |
| Relations | `comic.relate_from[]` | Value list **?** |
| Scanlation group (unit) | Chapter `group_name[]` | |
| Language (unit) | Chapter `lang` | |

### MangaDex

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title`; `altTitles` | Each is keyed by language code |
| Creators | Author and artist entries | As for MangaBaka |
| Summaries | `description` | Keyed by language code |
| Genres | Tags in group `genre` | |
| Tags | Tags in groups `theme` and `content` | The `content` group has `Sexual Violence` and `Gore` |
| External IDs | `id`; `links` | Key `mangadex`. The keys inside `links` are **?** |
| Format | `originalLanguage`; tags in group `format` | See Format |
| Original language | `originalLanguage` | |
| Publication status | `status` | See Publication status |
| Demographic | `publicationDemographic` | Same value |
| Content rating | `contentRating` | Same value |
| Start date | `year` | Year only |
| Total volumes, chapters | `lastVolume`, `lastChapter` | Strings |
| Reading mode | Tag `Long Strip` in group `format` | Gives `longStrip` |

### nhentai

Each entry is a gallery: one standalone unit.

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title.english`; `title.japanese`; `title.pretty` | `pretty` is a short form: kind `abbreviated` **≈** |
| Creators | Tags of type `artist` | Role `storyAndArt` **≈** |
| Tags | Tags of type `tag` | No namespace at this provider |
| Characters | Tags of type `character` | |
| Parodies | Tags of type `parody` | The value `original` means no parody **?** |
| Circles | Tags of type `group` | |
| External IDs | `id` | Key `nhentai` |
| Publication type | Tags of type `category` | See Format |
| Content rating | — | `pornographic` **≈** |
| Censorship state | Tags `uncensored`, `mosaic censorship` | Give `uncensored` and `mosaic`. No tag gives no value |
| Language (unit) | Tags of type `language` | The tag `translated` is not a language: drop it |
| Scanlation group (unit) | `scanlator` | |
| Page count (unit) | `num_pages` | |

The upload date is not a release date. Do not use it.

### E-Hentai

Community wiki only. Each entry is a gallery: one standalone unit.

| Our field | Provider field | Notes |
|---|---|---|
| Titles | `title`; `title_jpn` | `title` is English or romanized; `title_jpn` is `ja` **≈** |
| Creators | Tags in namespace `artist` | Role `storyAndArt` **≈** |
| Tags | Tags in namespaces `female`, `male`, `mixed`, `other`, `location` | The provider namespace gives our tag namespace |
| Characters | Tags in namespace `character` | |
| Parodies | Tags in namespace `parody` | |
| Circles | Tags in namespace `group` | |
| External IDs | `gid` | Key `ehentai`. A lookup also needs the `token` |
| Publication type | `category` | See Format |
| Content rating | `category` | See Content rating |
| Censorship state | Tags | The tag names are **?** |
| Language (unit) | Tags in namespace `language` | |
| Page count (unit) | `filecount` | |

## Gaps

These items block a complete conversion. Each needs a check against the provider.

| Provider | Gap |
|---|---|
| MyAnimeList | The role values of `authors[]`, and the genre names, are not in the specification that the research read |
| Kitsu | Where the demographic is, and the value lists of genres and categories |
| MangaUpdates | The words for hiatus and cancelled in the `status` text |
| MangaBaka | The meaning of relation type `series`, and the tag names in "Audience Demographics" |
| Bangumi | The `infobox` keys for a series; the relation strings |
| Hikka | The role names |
| Comick | The whole detail shape (one sample); the relation values; the link keys `ap` and `mb` |
| MangaDex | The relation list and the keys inside `links` |
| E-Hentai | Everything: the API itself was not read |
| All | Event: no provider has it as a field |
