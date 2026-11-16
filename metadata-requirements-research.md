# MangaInfo.xml: requirements research findings

Research date: 2026-11-16. Audience: the project owner, deciding the field list for MangaInfo.xml.

Legend used throughout:

- **[V]** verified directly this session: I read the schema/spec file or saw a live response.
- **[S]** secondary: read in a source that is not the provider's own schema (a web search summary, a third-party client, a news piece). Treat as a lead.
- **[U]** unverified: stated from prior knowledge or inferred, not confirmed against a source read this session.
- **[X]** could not be reached or confirmed.

All live requests were unauthenticated, read-only, with a generic client name (`research-client/1.0`).

---

## 1. Summary

### Main conclusions

1. **No provider has a single clean vocabulary, so MangaInfo.xml needs its own enums plus a mapping layer.** The nine providers disagree on format (7 to 9 values each, different names), status (3 to 6 values), relation types (8 to 22 values) and age/content rating (4 different systems). Section 3 lists every conflict.
2. **ComicInfo.xml is per-file, flat and comma-separated.** It has one `Manga` element and one `AgeRating` enum (Section 5). It cannot say: origin country, native or romanized title, publication status, demographic, serialization magazine, structured creators with roles, external IDs, or content warnings. Every one of those exists in at least five of the nine providers.
3. **Most manga metadata is series-level, not per-file.** Only a few things (volume number, page count, ISBN, release date, translator, scan info, page types) belong to a single volume/chapter file. The Mylar `series.json` evidence (Section 6) supports adding a separate series-level file. Mylar's own schema is too small and comics-specific to reuse as is.
4. **Adult (18+) content: the structured sources are two gallery sites (E-Hentai, nhentai) plus the general providers' rating flags.** The gallery sites carry fields the general providers lack: parody (source work), circle/group, artist, character, language and translation tags, scanlator, censorship state (as tags). **Neither exposes a structured "event" (Comiket) field** in what I read. The dedicated adult metadata site Hentag has announced it is closing (Section 4). Details in Section 4.
5. **Comick still exists but in a new form** (comick.dev, with a documented catalog API). Its response schema is untyped in the OpenAPI document, so field shapes come from a live sample only.
6. **Licence/terms matter for which sources a tool can draw on.** MAL's API agreement forbids commercial use without approval and bars server-side storing of user content. AniList is free below 150 USD/month revenue and bars "hoarding". MangaBaka's own data is CC BY-NC-SA 4.0. MangaUpdates requires credit and caching. Others state nothing I could find (Section 7, per provider).

### Decisions these point to (for the owner)

| Decision | Evidence |
|---|---|
| Use a structured creator list (`<Creator role="...">`), not eight per-role elements like ComicInfo | Roles are free text in AniList, MAL, Kitsu, Shikimori, Hikka and Bangumi; role sets differ per provider (Section 3.4) |
| Keep titles as a typed, language-tagged list | MangaBaka, MAL (Jikan), Kitsu, MU, AniList, Comick all model title variants differently; only MangaBaka/Comick tag each with a language code |
| Separate "genre", "demographic", "theme" and "tag" (with optional rank, spoiler flag, adult flag) | AniList, MangaBaka, Hikka, Shikimori, Jikan separate them; MU and Kitsu mix them; only AniList and MangaBaka carry per-tag rank/weight and spoiler flags |
| Carry cross-site IDs as `<Id site="..." value="..."/>` | MangaBaka, Kitsu, Comick and AniList (idMal) all provide mappings; no shared ID exists |
| Dates need a precision model | AniList and Shikimori use year/month/day with nulls; MAL uses `YYYY`, `YYYY-MM` or `YYYY-MM-DD` strings; MangaBaka adds `is_estimated`; Hikka uses epoch integers |
| Two files: `MangaInfo.xml` (per volume/chapter file) and a series-level file | Section 6 |
| Adult content: one content-rating enum plus a separate flag list for content warnings | Section 4 |

---

## 2. Cross-provider comparison matrix

Cell text is the field name in that provider's API. "none" means I found no such field in what I read. Source for each column is the per-provider reference in Section 7.

| Concept | MangaBaka | MAL (official v2; Jikan noted) | AniList | Kitsu | MangaUpdates | Shikimori | Bangumi | Hikka | Comick |
|---|---|---|---|---|---|---|---|---|---|
| Main title | `title`, `native_title`, `romanized_title` (deprecated for `titles[]`) | `title` | `title.romaji`/`english`/`native`/`userPreferred` | `canonicalTitle`, `titles{locale:string}` | `title` | `name`, `russian` | `name`, `name_cn` | `title_original`, `title_native`, `title_en`, `title_ua` | `title` (plus `md_titles[]`) |
| Alternative titles | `titles[]` {language, traits, title, note, is_primary} | `alternative_titles{synonyms,en,ja}`; Jikan `titles[]{type,title}` | `synonyms[]` | `abbreviatedTitles[]` | `associated[]{title}` | `english[]`, `japanese[]`, `synonyms[]` | `infobox` alias entries (free key/value) | `synonyms[]` | `md_titles[]{title,lang,is_default}` |
| Format / type | `type` (6) | `media_type` (8) | `format` (MANGA, NOVEL, ONE_SHOT) + `countryOfOrigin` | `subtype` (7) | `type` (18, includes language-specific) | `kind` (7) | `platform` free string + `type` 1 + category 1001 | `media_type` (5) | `media_type` (manga/anime/novel) + `country` |
| Publication status | `status` (6) | `status` (3) | `status` (5) | `status` (derived, 5) | `status` free text + `completed` bool | `status` (5) | none (infer from infobox) | `status` (5) | `status` int 1-4, `translation_status` |
| Demographic | genres/tags (shounen etc.) | genre entries (Jikan: `demographics[]`) | tag category "Demographic" (5 tags) | genre/category | `genres[]` where `demographic:true` | genre `kind: demographic` | none | genre `type: demographic` | `demographic` int 1-5 + string |
| Age / content rating | `content_rating` (4) | `nsfw` (white/gray/black) | `isAdult` bool | `ageRating` (G, PG, R, R18) + `ageRatingGuide` | genres Adult, Hentai, Smut, Mature | genres Ecchi/Erotica/Hentai; `isCensored` (GraphQL) | `nsfw` bool | `nsfw` bool + genre `type: explicit` | `content_rating` (4) + `violence_rating` (2) |
| Origin country/language | `original_language` (BCP 47) | none (inferred from media_type manhwa/manhua) | `countryOfOrigin` (ISO 3166-1 alpha-2) | `origin_countries`/`origin_languages` exist in server model [S]; not in manga response sample | none (in `type` for some) | none | none | none | `country` (lowercase code), `iso639_1`, `lang_name` |
| Genres | `genres[]` (46), deprecated, use tags | `genres[{id,name}]` | `genres[]` (19 strings) | `genres` relationship | `genres[{genre}]` (36) | `genres[]` (id, kind, name) | none | `genres[]` (type genre/theme/demographic/explicit) | `md_comic_md_genres[]` with `group` |
| Tags / themes | `tags_v2[]` (rank/weight, spoiler, adult) | none official; Jikan `themes[]` | `tags[]` (rank, spoiler, adult, category) | `categories` relationship (nsfw flag, parent) | `categories[]` (user votes) | genre kind theme | `tags[]{name,count}`, `meta_tags[]` | genre type theme | `mu_comic_categories[]` (votes), `/category/` |
| Creators / roles | `authors[]`, `artists[]` (names only) | `authors[{node,role}]` | `staff.edges[].role` (free text) | `staff` relationship, `role` free text | `authors[{name,author_id,type}]` (Author/Artist) | `/roles` `rolesEn[]` free text | `/persons` `relation` + `career[]` enum (7) | `authors[{person,roles[]}]` | `authors[]`, `artists[]` |
| Publisher | `publishers[]` per language | Jikan `serializations` only; no publisher in official | none | none (`serialization` is a string) | `publishers[]` (type = language, notes) | `publishers[]` (magazines), `licensors[]` | `infobox` key 出版社 | `magazines[]` | `mu_comics.mu_comic_publishers[]`, `publishers[]` |
| Serialization / magazine | none | `serialization[{node,role}]` | none | `serialization` string | `publications[{publication_name,publisher_name}]` | `publishers[]` | infobox (连载杂志 seen on other subjects [U]) | `magazines[]` | none |
| Volume/chapter counts | `final_volume`, `total_chapters` | `num_volumes`, `num_chapters` (0 = unknown) | `volumes`, `chapters` | `volumeCount`, `chapterCount` | `latest_chapter`; counts in `status` text | `volumes`, `chapters` | `volumes`, `eps`, `total_episodes` | `volumes`, `chapters` | `last_chapter`, `chapter_count`, `final_chapter`, `final_volume` |
| Per-volume / per-chapter records | `/v1/works` (beta): volume records with ISBN etc. | none | none | `/chapters` records (`volumeNumber`, `number`, `published`) | `/releases` (release records) | none | each volume is its own subject | none | chapters list, `md_covers[]` per volume |
| Dates | `published.start_date`/`end_date` + `*_is_estimated` | `start_date`, `end_date` (year, year-month or full date) | `startDate`, `endDate` {year,month,day} | `startDate`, `endDate` | `year` string | `aired_on`, `released_on` (IncompleteDate in GraphQL) | `date` | `start_date`, `end_date` (epoch int), `year` | `year`, `to_year` |
| Description | `description` | `synopsis`, `background` | `description` | `synopsis`, `description` | `description` | `description`, `description_html` | `summary` | `synopsis_en`, `synopsis_ua` | `desc`, `parsed` |
| Cover images | `cover` (raw + x150/x250/x350, blurhash) + `/images` (volume covers) | `main_picture{large,medium}`, `pictures[]` | `coverImage{extraLarge,large,medium,color}`, `bannerImage` | `posterImage` (5 sizes + dims), `coverImage` | `image.url{original,thumb}` | `image{original,preview,x96,x48}` | `images{large,common,medium,small,grid}` | `image` (one URL) | `md_covers[]{vol,w,h,gpurl}` |
| Scores / popularity | `rating` (0-100), `popularity` ranks | `mean`, `rank`, `popularity`, `num_list_users`, `num_scoring_users` | `averageScore`, `meanScore`, `weightedScore`, `popularity`, `favourites`, `trending`, `rankings[]` | `averageRating`, `ratingRank`, `popularityRank`, `userCount`, `favoritesCount` | `bayesian_rating`, `rating_votes`, `rank{}` | `score`, `rates_scores_stats` | `rating{rank,total,count,score}`, `collection{}` | `score`, `native_score`, `stats{}` | `rating`, `bayesian_rating`, `rating_count`, `follow_rank` |
| External IDs / links | `source{7 sites}`, `links_v2[]` | Jikan `external[]`; official none | `idMal`, `externalLinks[]` | `mappings` (`externalSite`,`externalId`) | none (URLs only) | `myanimelist_id`, `external_links` | `infobox` | `mal_id`, `external[]` | `comic.links{al,ap,kt,mal,mb,mu,...}` |
| Relations | `relationships_v2[]` (22 types) | `related_manga[]` (8 types) | `relations` (14 types) | `mediaRelationships` (12 types) | `related_series[]` (10 types) | `/related` (12 types) | `/subjects/{id}/subjects` free-string `relation` | has_franchise bool only | `relate_from[]`, `md_relates.name` |
| Characters | none | Jikan `/characters` | `characters` (role MAIN/SUPPORTING/BACKGROUND) | `characters` (role 4 values) | none | `/roles` characters | `/characters` | `/manga/{slug}/characters` (`main` bool) | none |
| Licensed / adaptation flags | `is_licensed`, `has_anime`, `anime{start,end}` | none | `isLicensed` | none | `licensed`, `completed`, `anime{start,end}` | `licensors[]`, `license_name_ru` | none | `translated_ua` | `has_anime`, `anime{start,end}`, `translation_completed` |

---

## 3. Candidate field inventory for MangaInfo.xml

"Scope" says where the field naturally lives: **S** = series level, **F** = per-file (volume/chapter/gallery), **B** = both (series default, file may override). This is a proposal derived from the matrix; it is not a design.

### 3.1 Identity and titles

| Candidate | Scope | Type | Supplied by | Notes / conflicts |
|---|---|---|---|---|
| Series title (display) | S | string | all | ComicInfo has `Series`. |
| Native title + language | S | string, BCP 47 | MangaBaka, AniList, Hikka, Bangumi, MAL(en/ja), Shikimori(japanese) | AniList: romaji/english/native; MangaBaka also has `romanized_title`. |
| Romanized title | S | string | MangaBaka, AniList | MangaBaka language codes include script-specific `ja-Latn`, `ko-Latn`, `zh-Latn`, plus `ja-ro`, `ko-ro`, `ru-ro`, `zh-ro` (two romanization styles). |
| Typed title list | S | `<Title lang type primary>` | MangaBaka (traits official/native/alternative; v1 types alternative/native/official/romanized/unofficial/unknown), Comick (`md_titles` with `is_default`), MAL/Jikan (`type`), Kitsu (locale keys `en_jp`, `en_us`) | Type vocabularies differ; none define "short"/"abbreviated" except Kitsu `abbreviatedTitles`. |
| Volume/chapter title | F | string | Kitsu chapters, MangaBaka works `sub_title`, ComicInfo `Title` | |
| Sort title | S/F | string | none of the nine | Kavita adds `SeriesSort` to ComicInfo (Section 5). |
| Localized title | S | string | Kavita `LocalizedSeries` | |

### 3.2 Format, status, origin

| Candidate | Scope | Supplied by | Value-set conflicts |
|---|---|---|---|
| Publication format (manga/manhwa/manhua/novel/one-shot/doujin/OEL) | S | all except AniList (uses `countryOfOrigin`) | See table 3.2a. |
| Origin country | S | AniList (`countryOfOrigin` ISO 3166 alpha-2), Comick (`country` lowercase code) | MangaBaka uses a language code instead (`original_language`). `zh-Hant-TW` style codes vs ISO country codes: both are needed or one derived. |
| Original language | S | MangaBaka (BCP 47), Comick (`iso639_1`) | |
| Publication status | S | all | See table 3.2b. |
| Adaptation source (original, light novel...) | S | AniList `source` (15), Hikka `SourceEnum` (15, anime-oriented) | Only AniList exposes it for manga entries in a verified response. Includes `DOUJINSHI` (relevant for adult/derivative works). |

**3.2a Format values by provider [V]**

| Provider | Values |
|---|---|
| MangaBaka `type` | manga, novel, manhwa, manhua, oel, other |
| MAL official `media_type` | unknown, manga, novel, one_shot, doujinshi, manhwa, manhua, oel |
| Jikan search `type` | manga, novel, lightnovel, oneshot, doujin, manhwa, manhua |
| AniList `format` (manga-relevant) | MANGA, NOVEL, ONE_SHOT (anime values TV, TV_SHORT, MOVIE, SPECIAL, OVA, ONA, MUSIC also in same enum); manhwa/manhua are format MANGA with `countryOfOrigin` KR/CN (verified: a Korean title returned format MANGA, country KR) |
| Kitsu `subtype` (manga) | manga, novel, manhua, oneshot, doujin, manhwa, oel (server source) |
| MangaUpdates `type` | Artbook, Doujinshi, Drama CD, Filipino, Indonesian, Manga, Manhwa, Manhua, Novel, OEL, Thai, Vietnamese, Malaysian, Nordic, French, Spanish, German, Russian |
| Shikimori `kind` | manga, manhwa, manhua, light_novel, novel, one_shot, doujin |
| Bangumi | `type` 1 (book) + `SubjectBookCategory` 0 other, 1001 comic, 1002 novel, 1003 illustration; `platform` is a free string (samples: 小说, 漫画, 画集, 公式书) |
| Hikka `media_type` | one_shot, doujin, manhua, manhwa, manga (novels are a separate resource) |
| Comick | `media_type` manga / anime / novel; manhwa/manhua inferred from `country` |

Conflicts: "doujin" is `doujinshi` (MAL, MU) vs `doujin` (Jikan, Kitsu, Shikimori, Hikka). "One-shot" is `one_shot`, `oneshot`, `ONE_SHOT`. MangaUpdates' `type` mixes format with language/country for non-Japanese comics. Light novels are a separate type only in Jikan and Shikimori; others fold into novel. A MangaInfo enum should be small (for example manga, manhwa, manhua, novel, oneshot, doujinshi, oel, other) and keep origin country separate.

**3.2b Status values by provider [V]**

| Provider | Values |
|---|---|
| MangaBaka | cancelled, completed, hiatus, releasing, unknown, upcoming |
| MAL official | finished, currently_publishing, not_yet_published |
| Jikan search filter | publishing, complete, hiatus, discontinued, upcoming |
| AniList | FINISHED, RELEASING, NOT_YET_RELEASED, CANCELLED, HIATUS |
| Kitsu | tba, unreleased, upcoming, current, finished (computed from dates in the server model, not stored) |
| MangaUpdates | no enum: `status` free text ("43 Volumes (Ongoing)") + `completed` boolean |
| Shikimori | anons, ongoing, released, paused, discontinued |
| Bangumi | none |
| Hikka | discontinued, announced, finished, ongoing, paused |
| Comick | int: 1 ongoing, 2 completed, 3 cancelled, 4 hiatus; plus separate `translation_status` / `translation_completed` |
| Mylar series.json | Continuing, Ended |

Conflicts: only MangaBaka, AniList, Shikimori, Hikka and Comick have both hiatus/paused and cancelled/discontinued. MAL has neither. Comick distinguishes translation completion from series completion (a concept MangaInfo may want for scanlated files).

### 3.3 Classification

| Candidate | Scope | Supplied by | Notes |
|---|---|---|---|
| Genre list | S | all with genres | Vocabularies overlap but differ in spelling (`Sci-Fi`, `sci-fi`, `Sci-fi`; `Shoujo Ai`, `Girls Love`, `Girls' Love`). Needs a mapping table. |
| Demographic (shounen, shoujo, seinen, josei, kids) | S | AniList (tag category), Shikimori/Hikka/Comick (explicit), MU (genre flagged `demographic`) | MU flags `demographic:true` on: Josei, Lolicon, Seinen, Shotacon, Shoujo, Shoujo Ai, Shounen, Shounen Ai, Yaoi, Yuri. So MU's "demographic" mixes audience with content categories. Comick ints: 1 shounen, 2 shoujo, 3 seinen, 4 josei, 5 none. |
| Theme list | S | Hikka, Shikimori, Jikan (themes), MangaDex (theme group) | |
| Free-form tags with optional rank / spoiler / adult / category | S | AniList (rank 0-100, `isMediaSpoiler`, `isGeneralSpoiler`, `isAdult`, `category`), MangaBaka (`weight` core/defining/recurrent/incidental/unweighted, `is_spoiler`, `is_explicit`, `content_rating`, hierarchical `name_path`), MU (votes), Comick (votes) | Three different relevance models: rank int, weight enum, vote counts. |
| Age/content rating | S/F | see Section 4 | |
| Content warnings | S | MangaDex has a tag group `content` with Sexual Violence, Gore [V]; AniList tags (Rape, etc.) | |

### 3.4 People, publishers, serialization

| Candidate | Scope | Supplied by | Notes |
|---|---|---|---|
| Creator with role | S/F | AniList, Kitsu, MAL, Shikimori, Hikka, Bangumi (roles); MU (Author/Artist); MangaBaka (author/artist lists without roles) | Role vocabularies are free text, except Bangumi `career` (producer, mangaka, artist, seiyu, writer, illustrator, actor) and MU's two types. AniList roles carry volume ranges inside the string, e.g. "Story & Art (vols 1-41)", and language for translators, e.g. "Translator (English: vols 5-8, 10-)" [V]. This suggests optional `scope` (volume range) and `language` attributes. |
| Creator identity (native name, external ID) | S | AniList `Staff.name{full,native,alternative}`, MU `author_id`, Hikka person slug, MangaDex author social links (pixiv, fanbox, fantia, skeb, booth, melonBook...) [V] | |
| Publisher (per language/edition) | S/F | MangaBaka (`publishers[]` per language, with `note` such as "25 Volumes - Ongoing"), MU (`publishers[]` with `type` = language and `notes`), Comick (MU-derived) | Only MangaBaka and MU model multiple language editions. |
| Imprint | S/F | none in the nine; ComicInfo and Mylar have it | |
| Serialization (magazine, run dates) | S | MAL (`serialization[]`), MU (`publications[]` with run dates in text "Hakusensha; since 1992"), Shikimori (`publishers[]` = magazines), Hikka (`magazines[]`), Kitsu (single string) | Not in ComicInfo at all. |
| Licensor | S | Shikimori `licensors[]`, MangaBaka `is_licensed` | |

### 3.5 Counts, dates, structure

| Candidate | Scope | Supplied by | Notes |
|---|---|---|---|
| Total volumes / chapters (known or unknown) | S | MAL (0 = unknown), AniList (null), MangaBaka (null) | Unknown encoded three ways. ComicInfo uses -1 default. |
| Final volume / final chapter | S | MangaBaka, Comick | |
| Start / end publication date with precision | S | AniList, Shikimori (null parts), MAL (string precision), MangaBaka (`*_is_estimated`) | Hikka epoch ints cannot express partial dates. |
| Volume number, chapter number | F | ComicInfo `Volume`, `Number` (string) | Number must stay a string (e.g. 12.5, 0-1 appear in MU/Comick samples). |
| Release date of the file's edition | F | MangaBaka works `release_date`, Bangumi `date` per volume | |
| ISBN/GTIN | F | MangaBaka works `identifiers[{id,name}]`, Bangumi infobox ISBN, ComicInfo 2.1 `GTIN` | |
| Page count | F | ComicInfo, MangaBaka works `pages`, Bangumi infobox 页数 | |
| Reading direction | S/F | ComicInfo `Manga=YesAndRightToLeft` | No provider exposes it; infer from format/origin. Webtoon "long strip" is a tag in AniList (`Long Strip`), MangaDex (format), MU. |
| Colour (full colour, B&W) | S/F | ComicInfo `BlackAndWhite`; AniList tag "Full Color"; MangaDex "Full Color"/"Official Colored"/"Fan Colored" | |

### 3.6 Scores, links, relations

| Candidate | Scope | Supplied by | Notes |
|---|---|---|---|
| Community rating | S | all | Scales: MAL 0-10, AniList 0-100, Kitsu 0-100 (string, `averageRating "71.36"`), MU 0-10 bayesian, Bangumi 0-10, Shikimori 0-10 (string), MangaBaka 0-100 with per-source `rating_normalized`, ComicInfo 0.0-5.0. Store value with explicit scale and source. |
| External IDs | S | MangaBaka `source{}`, Kitsu `mappings`, AniList `idMal`, Comick `links{}`, Shikimori `myanimelist_id`, Hikka `mal_id` | MAL is the hub: Shikimori and Hikka use MAL IDs directly. |
| Web links by type | S | MangaBaka `links_v2` (type retailer/publisher/webplatform/info/social/news/piracy/other + language), AniList `externalLinks` (type INFO/STREAMING/SOCIAL + language), Hikka (`general`/`watch`/`read`), Shikimori (36 kinds) | |
| Relations | S | see 3.6a | |
| Characters | S/F | AniList, Kitsu, Jikan, Bangumi, Shikimori, Hikka | Role vocab: AniList MAIN/SUPPORTING/BACKGROUND; Kitsu main/supporting/recurring/cameo (server model; sample returned `main`); Hikka boolean `main`. |

**3.6a Relation types [V]**

| Provider | Values |
|---|---|
| MangaBaka (22) | adaptation, alternative, cameo, character_focus, compilation, contains, crossover, expansion, main, other, parent, parody, prequel, reboot, remake, sequel, series, side_story, source, spin_off, summary, uncollected (+ `chronology`: narrative, release, unknown; `is_manual`; `note`) |
| MAL official (8) | sequel, prequel, alternative_setting, alternative_version, side_story, parent_story, summary, full_story |
| AniList (14) | ADAPTATION, PREQUEL, SEQUEL, PARENT, SIDE_STORY, CHARACTER, SUMMARY, ALTERNATIVE, SPIN_OFF, OTHER, SOURCE, COMPILATION, CONTAINS, SAME_UNIVERSE |
| Kitsu (12) | sequel, prequel, alternative_setting, alternative_version, side_story, parent_story, summary, full_story, spinoff, adaptation, character, other |
| MangaUpdates (10) | Prequel, Sequel, Spin-Off, Adapted From, Alternate Version, Part of Anthology, Main Story, Side Story, Full Anthology, Other |
| Shikimori (12) | adaptation, alternative_setting, alternative_version, character, full_story, other, parent_story, prequel, sequel, side_story, spin_off, summary |
| Bangumi | free string (a volume to its series is `系列`) |
| Comick | `md_relates.name` string ("Sequel" seen); value list not documented [X] |

### 3.7 Translation / release-group fields (relevant to scanlated and adult content)

| Candidate | Scope | Supplied by |
|---|---|---|
| Translator | F | ComicInfo 2.1 `Translator` ("can also be used for fan translations"); AniList staff role "Translator (lang)" |
| Scanlation group | F | Comick chapters `group_name[]`; MangaUpdates releases `groups[]`; nhentai `scanlator`; ComicInfo `ScanInformation` free text |
| Translation completeness | S | Comick `translation_status`/`translation_completed`; nhentai/E-H language tag `translated` |
| Available translation languages | S | Comick `langList`; MangaDex `availableTranslatedLanguages` |
| Licensed in English | S | MangaBaka `is_licensed`, AniList `isLicensed`, MU `licensed` |

---

## 4. Adult (18+) content findings

### 4.1 How the nine providers treat adult content

| Provider | Handling | Verification |
|---|---|---|
| MangaBaka | Included. `content_rating` enum safe, suggestive, erotica, pornographic on each series, each tag and each cover image. Genres include adult, ecchi, erotica, hentai, smut, lolicon, shotacon, doujinshi, mature. Tag tree has a root group "Sexual Content"; tags carry `is_explicit`. Search with `content_rating=pornographic` returned results unauthenticated (448 for query "hentai"). | [V] spec + live |
| MAL official | Flag `nsfw` (white = safe, gray = may be NSFW, black = NSFW); `nsfw` query parameter, with the doc stating "By default, some APIs don't return nsfw content". `media_type` includes `doujinshi`; ranking type `doujin`. | [V] spec text |
| Jikan (unofficial) | Splits genres into `genres`, `explicit_genres`, `themes`, `demographics`; search param `sfw`. | [V] Jikan OpenAPI (live API timed out) |
| AniList | `isAdult` boolean on Media; genre "Hentai"; 67 of 430 tags have `isAdult:true` (category "Sexual Content" 66, plus Omegaverse in another category); media query accepts `isAdult:true` and returns results unauthenticated. `MediaSource` includes DOUJINSHI. No rating enum, no doujin format. | [V] introspection + live |
| Kitsu | `ageRating` G, PG, R, R18 (`AGE_RATINGS` in server model); categories have `nsfw` boolean. The API docs say "NSFW/R18 content ... hidden for all unauthenticated requests". An unauthenticated filter on `ageRating` was rejected ("age_rating is not allowed"). | [V] docs + server source |
| MangaUpdates | Included, no flag. Genres Adult, Hentai, Smut, Mature, Ecchi, Doujinshi, Lolicon, Shotacon; type "Doujinshi". Unauthenticated genre=Hentai search returned 826 hits. `exclude_filtered_genres` search option exists. | [V] spec + live |
| Shikimori | Included. Genres Ecchi, Erotica, Hentai (and Yaoi/Yuri); kind `doujin`; GraphQL `Manga.isCensored`. The v1 genre list for manga returned 48 entries including Hentai and Erotica. Unauthenticated search by genre returned adult doujin entries. | [V] introspection + live |
| Bangumi | `nsfw` boolean on subject. The Komf README says its Bangumi provider "require[s] a token to show nsfw items". | [V] schema; [S] token requirement |
| Hikka | `nsfw` boolean (info response) and genre `type: explicit` with Erotica, Ecchi, Hentai. Unauthenticated search with genre "hentai" returned entries (11,724 total). | [V] spec + live |
| Comick | `content_rating` safe/suggestive/erotica/pornographic (same four-level scale as MangaBaka and MangaDex), `violence_rating` none/graphic, `matureContent` bool; genres include Adult, Ecchi, Erotica, Hentai, Loli, Incest, Doujinshi. | [V] spec + live |

Value-set conflict: the four-level `safe / suggestive / erotica / pornographic` scale is shared by MangaBaka, Comick and MangaDex (verified). It is the only cross-provider rating scale found that has a distinction between "erotica" and "pornographic". ComicInfo's `AgeRating` is audience-oriented (see Section 5) and has no explicit/non-explicit distinction beyond "Adults Only 18+", "R18+", "X18+".

### 4.2 Sources with structured adult metadata

| Source | What I verified | Notes |
|---|---|---|
| **nhentai API v2** | OpenAPI 3 at `https://nhentai.net/api/v2/openapi.json` [V]. Gallery fields: `id`, `media_id`, `title{english,japanese,pretty}`, `cover`, `thumbnail`, `scanlator`, `upload_date` (int), `tags[]`, `num_pages`, `num_favorites`, `pages`. Tag object: `id`, `type`, `name`, `slug`, `url`, `count`, `description`, `is_community`, `links[]{service,label,url,handle}`. Tag types (all seven returned data): `tag`, `artist`, `parody`, `character`, `group`, `language`, `category`. Language tags include `japanese`, `translated`, `chinese`, ...; category tags include `doujinshi`, `manga`. Censorship is expressed as tags: `uncensored` ("The work is presented without any visual censorship...") and `mosaic censorship` exist; `decensored` returned no tag [V live]. | API key via account settings (`Authorization: Key ...`) for authenticated endpoints; tag listing worked unauthenticated; asks for a descriptive User-Agent; no licence terms read [X]. |
| **E-Hentai API** | Documented on the community wiki [S: ehwiki.org, not the site's own spec]: POST `https://api.e-hentai.org/api.php`, method `gdata`, `gidlist` of [gid, token] pairs (max 25 per request), `namespace:1` to get namespaced tags. Response fields: `gid`, `token`, `archiver_key`, `title`, `title_jpn`, `category`, `thumb`, `uploader`, `posted` (UNIX time), `filecount`, `filesize`, `expunged`, `rating`, `torrentcount`, `torrents[]`, `tags[]`, `parent_gid`/`parent_key`, `current_gid`/`current_key`, `first_gid`/`first_key`. Categories: Doujinshi, Manga, Artist CG, Game CG, Western, Image Set, Non-H, Cosplay, Asian Porn, Misc, Private. Namespaces (wiki table): artist (a), character (c), cosplayer (cos), female (f), group (g, circle), language (l), location (loc), male (m), mixed (x), other (o), parody (p), reclass (r). Rate guidance: about 4-5 sequential requests then a wait of roughly 5 s. | The API looks up known galleries only (no search). Terms of using the data not read [X]. Wiki states "page gives no explicit type" for most fields, so types are inferred. |
| **MangaDex API** (not on the owner's list; general, includes adult) | `contentRating` safe/suggestive/erotica/pornographic; adult manhwa returned by `contentRating[]=pornographic` unauthenticated (20,135 total) [V]. Tag groups [V]: format (12, includes Doujinshi, Self-Published, Official/Fan Colored, Long Strip, Web Comic), genre (25), theme (38, includes Loli, Shota, Incest, Gyaru), content (2: Sexual Violence, Gore). Series fields: `title`, `altTitles`, `description`, `originalLanguage`, `lastVolume`, `lastChapter`, `publicationDemographic` (shounen, shoujo, josei, seinen), `status` (completed, ongoing, cancelled, hiatus), `year`, `contentRating`, `availableTranslatedLanguages`, `links`. Author objects carry social/shop links (twitter, pixiv, melonBook, fanBox, booth, nicoVideo, skeb, fantia, tumblr, youtube, weibo, naver, website). | Terms/licence not read [X]. Candidate extra provider for MangaInfo, also the only one verified with a "content warning" tag group. |
| **Hentag** | Site now shows "A Final Update & Thank You" and states the operator is winding it down [V: hentag.com]. The Komf README config lists a `hentag` provider (disabled by default) [S], but the Komf source tree no longer has a hentag provider directory [V], and I found no API documentation [X]. | Treat as unavailable. |

### 4.3 Fields the adult sources have that general providers lack

| Field | Where | Notes for MangaInfo |
|---|---|---|
| Parody / source work (the franchise a doujin derives from) | nhentai `parody`, E-H `parody` | General providers only have AniList `source: DOUJINSHI`, and relations (`parody` in MangaBaka relation types). A `<Parody>` list distinct from `<Relation>` is justified. |
| Circle / group | nhentai `group`, E-H `group` (alias circle) | Creator-group, not a publisher. |
| Artist | nhentai `artist`, E-H `artist` | Single role (no author/artist split). |
| Character | nhentai `character`, E-H `character` | |
| Language of this edition | nhentai/E-H `language` tags (including `translated`) | General providers model original language only (MangaBaka `original_language`); per-file language is ComicInfo `LanguageISO`. |
| Translation status | tag `translated` (nhentai), Comick `translation_status` | |
| Scanlator | nhentai `scanlator` field | |
| Censorship state | tags `uncensored`, `mosaic censorship` (nhentai); Shikimori `isCensored` (GraphQL) | Not a structured field anywhere; a MangaInfo `<Censorship>` enum (uncensored, mosaic, other, unknown) would be new. |
| Subject-gender tag namespaces | E-H `female:`, `male:`, `mixed:`; nhentai tags are un-namespaced | E-H encodes who a fetish applies to; nhentai does not. |
| Category | nhentai `category`, E-H `category` | Doujinshi, Manga, Artist CG, Game CG, Western, Image Set, Non-H, Cosplay... ; overlaps with the "format" concept. |
| Event / convention (e.g. Comiket) | **not found in any source I read** (nhentai and E-H expose no event field in the verified schemas) | Probably only available from commercial shop sites (Fakku, Melonbooks, Toranoana): [U], none checked. |
| Upload date, favourites, page count | nhentai, E-H | Gallery-site specifics, not manga metadata. |

### 4.4 Not checked

Fakku, Hitomi, Tsumino, HentaiNexus, Doujinshi.org and Comiket catalog data were **not** examined. LANraragi (a self-hosted archive server that can import ComicInfo-style metadata and has E-Hentai/nhentai-style plugins): its docs pages I fetched did not give tag-namespace details [X]. Kavita and Komga parse adult-oriented gallery metadata only via ComicInfo (Section 5).

---

## 5. ComicInfo.xml findings

Primary sources: XSDs at `https://github.com/anansi-project/comicinfo` (raw: `schema/v1.0/ComicInfo.xsd`, `schema/v2.0/ComicInfo.xsd`, `drafts/v2.1/ComicInfo.xsd`), `DOCUMENTATION.md`, `CHANGELOG.md`. All read [V].

### 5.1 Scope

ComicInfo.xml lives **inside each archive** (a book/volume/issue). All values describe that one file, even `Series`, `Count`, `Genre`. The documentation notes `Count` "could be different on each book in a series. Consuming applications should consider using only the value for the latest book." There is no series-level construct in the schema. Servers derive series metadata from the files (Komga reads series fields from the first/other books via `SeriesMetadataFromBookProvider`; Kavita aggregates, for example AgeRating = most mature across files, Year = minimum).

### 5.2 Element inventory (v2.1 draft is the superset)

All elements are optional, `minOccurs=0`, in a fixed `xs:sequence` order. Defaults are as in the XSD.

| Element | Type | Default | Since | Notes (from DOCUMENTATION.md unless stated) |
|---|---|---|---|---|
| Title | string | "" | 1.0 | Title of the book. |
| Series | string | "" | 1.0 | |
| Number | string | "" | 1.0 | Number in series; string so "12.5" works. |
| Count | int | -1 | 1.0 | Total books in series. |
| Volume | int | -1 | 1.0 | "specific to US Comics" per docs. Int only: cannot hold "Vol 3.5". |
| AlternateSeries | string | "" | 1.0 | Crossover arcs. |
| AlternateNumber | string | "" | 1.0 | |
| AlternateCount | int | -1 | 1.0 | |
| Summary | string | "" | 1.0 | |
| Notes | string | "" | 1.0 | Usually the tool that wrote the file. |
| Year, Month | int | -1 | 1.0 | |
| Day | int | -1 | 2.0 | |
| Writer, Penciller, Inker, Colorist, Letterer, CoverArtist, Editor | string | "" | 1.0 | One element per role; multiple people are comma separated (docs: "accepted"). |
| Translator | string | "" | 2.1 draft | "can also be used for fan translations". |
| Publisher, Imprint | string | "" | 1.0 | |
| Genre | string | "" | 1.0 | Comma-separated. |
| Tags | string | "" | 2.1 draft | Comma-separated. |
| Web | string | "" | 1.0 | Space-separated URLs. |
| PageCount | int | 0 | 1.0 | |
| LanguageISO | string | "" | 1.0 | Docs recommend BCP 47 (it distinguishes Traditional/Simplified Chinese). |
| Format | string | "" | 1.0 | Free text: "TBP", "HC", "Web", "Digital". |
| BlackAndWhite | YesNo | Unknown | 1.0 | |
| Manga | Manga enum | Unknown | 1.0 (YesNo), 2.0 (enum) | See 5.3. |
| Characters, Teams, Locations | string | "" | 2.0 | Comma-separated. |
| ScanInformation | string | "" | 2.0 | Free text, "who scanned". |
| StoryArc | string | "" | 2.0 | |
| StoryArcNumber | string | "" | 2.1 draft | |
| SeriesGroup | string | "" | 2.0 | |
| AgeRating | AgeRating enum | Unknown | 2.0 | See 5.3. |
| Pages | ArrayOfComicPageInfo | none | 1.0 | See 5.4. |
| CommunityRating | decimal 0 to 5 | none | 2.0 | `fractionDigits` is 2 in v2.0 and 1 in v2.1 draft. |
| MainCharacterOrTeam | string | "" | 2.0 | |
| Review | string | "" | 2.0 | |
| GTIN | string | "" | 2.1 draft | ISBN/ISSN/EAN/JAN. |

Changelog confirms: 2.0 changed `Manga` from `YesNo` to a new enum (breaking) and added Characters, Teams, Locations, ScanInformation, StoryArc, SeriesGroup, AgeRating, Day, MainCharacterOrTeam, Review; 2.1 draft adds Translator, Tags, StoryArcNumber, GTIN. (My own diff of the three XSDs agrees.)

### 5.3 Enums

| Enum | Values |
|---|---|
| YesNo (BlackAndWhite) | Unknown, No, Yes |
| Manga | Unknown, No, Yes, YesAndRightToLeft |
| AgeRating | Unknown, Adults Only 18+, Early Childhood, Everyone, Everyone 10+, G, Kids to Adults, M, MA15+, Mature 17+, PG, R18+, Rating Pending, Teen, X18+ |

### 5.4 Page info (`Pages/Page`, attributes)

| Attribute | Type | Default |
|---|---|---|
| Image | int (required) | |
| Type | list of ComicPageType | Story |
| DoublePage | boolean | false |
| ImageSize | long | 0 |
| Key | string | "" (docs: "???") |
| Bookmark | string | "" |
| ImageWidth, ImageHeight | int | -1 |

ComicPageType values: FrontCover, InnerCover, Roundup, Story, Advertisement, Editorial, Letters, Preview, BackCover, Other, Deleted. (The doc text calls the last one "Delete".)

### 5.5 Fit for manga: gaps

| Need | ComicInfo today | Gap |
|---|---|---|
| Reading direction | `Manga` = `YesAndRightToLeft`; the `Manga` name conflates "is manga" with direction. Komga maps `No` to left-to-right, `YesAndRightToLeft` to right-to-left, `Yes`/`Unknown` to no direction set [V, Komga source]. | Manhwa/manhua are not "manga"; no way to say vertical scroll (webtoon). No origin country. |
| Format (manga/manhwa/manhua/doujinshi/one-shot/novel) | `Format` is free text for binding (TBP/HC) | No enum for series type. |
| Native/romanized/English titles | one `Series`, one `Title` | No alternate or native title, no language tag. Kavita invented `LocalizedSeries` and `SeriesSort` [V: Kavita docs]. |
| Creators with roles | 7 fixed roles + Translator | No Story vs Art split (Writer/Penciller approximates), no "Original creator"/"Supervisor", no per-volume scope, no IDs. |
| Volume | int | Per-volume with fractional/omnibus/"Vol 3.5" cannot be represented; ComicInfo `Number` + `Volume` are US-comics oriented per docs. |
| Chapter vs volume file | `Number` only | No flag for whether the file is a volume, chapter or collection of chapters; chapter-range for a volume file not representable. |
| Status | none | Publication status exists in 7 of 9 providers. |
| Demographic | none (put in Genre, e.g. "Shonen" per docs example) | |
| Serialization/magazine | none | |
| Age/content rating | single `AgeRating`, audience-style | No explicit/non-explicit vs rating, no content warnings. |
| External IDs | `Web` (space-separated URLs) | No typed IDs. Komga/Kavita use `Web` for links [V]. |
| Original-language vs file-language | `LanguageISO` is file language only | No original language. |
| Multi-valued fields | comma-separated strings | Names containing commas (common in Western names, "Last, First") are ambiguous; the schema's `maxOccurs=1` forces it. |
| Adult-specific (parody, circle, event, censorship) | none (could be abused via Tags) | Section 4.3. |
| Scanlation | `ScanInformation` free text, `Translator` | No group, no translation-complete flag. |

### 5.6 Consumers and their extensions

- **Komga**: reads `ComicInfo.xml` inside books [V, `ComicInfoProvider.kt`]. Splits Writer/Penciller/Inker/Colorist/Letterer/CoverArtist/Editor/Translator into authors with role names `writer`, `penciller`, `inker`, `colorist`, `letterer`, `cover`, `editor`, `translator`; Locations/Teams/Characters into "notable entities"; AlternateSeries + StoryArc(+Number) into read lists; `Web` split on spaces into links; Tags lowercased; GTIN validated as ISBN; `Manga` to reading direction; `Genre`, `Publisher`, `AgeRating`, `LanguageISO` (BCP 47 validated), `Count`, `SeriesGroup` (collections) to series metadata. No extension elements.
- **Kavita**: v2.1 draft supported; non-standard `LocalizedSeries` and `SeriesSort`; `Count` non-zero marks the series ended; `Format` values such as Annual/One-Shot/TPB/Omnibus make a "Special"; `AgeRating` takes the most mature across files; `GTIN` to ISBN; manga/reading direction not mentioned on the page [V: Kavita wiki].

---

## 6. Mylar `series.json` findings

### 6.1 Authoritative spec and where it is

The brief's "mylar schema" is `series.json` from the mylar3 project, documented on its GitHub wiki:

- `https://github.com/mylar3/mylar3/wiki/series.json-schema-(version-1.0)` [V, raw markdown read]
- `...(version-1.0.1)` and `...(version-1.0.2)` [V]
- `https://github.com/mylar3/mylar3/wiki/series.json-examples` [V]
- Writer implementation `https://github.com/mylar3/mylar3/blob/master/mylar/series_metadata.py` [V]

The "schema" pages are JSON-Schema-styled but **not valid JSON Schema** (typos: unbalanced quotes, `"type": "int"`), and the `metadata` object in 1.0 was documented as an array. They are descriptions, not machine-usable schemas.

### 6.2 Fields (version 1.0.2, current; the writer sets `version` to `1.0.2`) [V]

Root: `version` (string), `metadata` (object).

| Field | Type | Meaning / allowed values |
|---|---|---|
| type | string | constant `comicSeries` |
| publisher | string | publisher name |
| imprint | string or null | imprint under publisher |
| name | string | series title |
| comicid | int | ComicVine series ID (examples also show strings like `"4050-18005"` inside `collects`) |
| year | int | year the series started |
| description_text | string | plain text, no line breaks |
| description_formatted | string or null | same with line breaks |
| volume | int or null | "volume of the series ... either numerical or the series year" |
| booktype | string | schema text: Print, OneShot, TPB or GN. **The writer emits `One-Shot`** when `Total==1` (code in `series_metadata.py`), a mismatch with the spec text [V] |
| age_rating | string or null | "as taken from within Mylar"; allowed values are not given in the spec. Komga accepts: All, 9+, 12+, 15+, 17+, Adult [V, Komga `AgeRating.kt`] |
| collects | array or null | for TPB/GN: items `{series, comicid, issueid, issues}` (all strings; 1.0 documented an object) |
| comic_image | string | ComicVine cover URL (renamed from `comicImage` in 1.0.2) |
| total_issues | int | issues so far |
| publication_run | string | "Month Year - Month Year", end is "Present" when continuing |
| status | string | `Continuing` or `Ended` |

Version history [V]: 1.0 (string types, `metadata` as an array); 1.0.1 (`metadata` object, `year`/`comicid`/`volume` to int, added `age_rating` and `version`); 1.0.2 (`comicImage` renamed `comic_image`).

### 6.3 Consumers

- **Komga** reads `series.json` (library option "import Mylar series metadata") [V, `MylarSeriesProvider.kt`]. It maps: title (name, plus `(year)` if volume is not null and not 1), status (Ended/Continuing to ENDED/ONGOING), summary (formatted if present, else text), publisher, age rating, `total_issues` to total book count. It ignores unknown properties; accepts aliases `cid` for `comicid` and `ComicImage` for `comic_image`; skips oneshot series; it requires `type`, `publisher`, `name`, `year`, `booktype`, `comic_image`, `total_issues`, `publication_run`, `status` as non-null in its DTO (a `series.json` missing any of these fails to parse). It sets `readingDirection`, `language`, `genres`, collections to none from this file.
- **Kavita**: no evidence it reads `series.json` [S: web search found none; Kavita's metadata page mentions only ComicInfo]. Not confirmed absent [X].
- **Mylar itself** writes the file and, on update, re-reads description fields from it (versions 1.0 and later) [V].

### 6.4 Series-level vs per-file, and what this says about a separate schema

| Level | ComicInfo.xml | Mylar series.json |
|---|---|---|
| Granularity | One file per book | One file per series folder |
| Series title, publisher, imprint, description, age rating, status, total count | present but repeated in every file | present once |
| Genres, tags, creators | present per file | **absent** |
| Cover | per-page types only | `comic_image` URL |
| External ID | none | ComicVine ID only |
| Collections/trades | none | `collects[]` |

Evidence for a separate series-level MangaInfo file:

1. Most of the 40+ concepts in Section 3 are series-level (titles, format, status, demographic, origin, genres, tags, serialization, counts, relations, external IDs, scores). Repeating them in every volume file is how ComicInfo gets `Count` inconsistent across files (docs warning).
2. Komga must read series fields out of arbitrary book files because no series-level source exists in ComicInfo; Mylar `series.json` plus Komga's "import Mylar series metadata" option is the only existing sidecar convention.
3. `series.json` omits everything manga needs (genres, creators, titles, demographic, origin) and is comics-specific (ComicVine IDs, `collects`, `booktype` values). Reusing it unchanged does not help; its field naming (snake_case JSON) and `version` field are the only useful precedents.
4. A series-level file can double as the import format for providers: nearly every provider is a series-level API (the per-volume APIs are only MangaBaka `works`, Kitsu `chapters`, MU `releases`, Bangumi volume subjects).

Open: a reader (Komga) that parses a second sidecar would need support; whether to keep one XML schema with two root elements (`MangaSeriesInfo`/`MangaInfo`) or XML + JSON is a decision for the owner.

---

## 7. Per-provider reference

For each provider: access, terms, then fields and enums. Everything marked [V] unless noted.

### 7.1 MangaBaka

- Base `https://api.mangabaka.org` (the old `api.mangabaka.dev` replies HTTP 500 "deprecated and no longer serves traffic") [V live]. Docs `https://mangabaka.org/developers`; OpenAPI 3.1 at `https://mangabaka.org/api.json` (not at `api.mangabaka.org/api.json`, which 404s) [V].
- Auth: public endpoints need none; `/my` needs a personal access token or OAuth [V].
- Rate limits (`/developers/concepts/rate-limits-and-caching`): search 30/min burst 5; everything else 180/min burst 5; per IP; 429 with `Retry-After: 10`; nightly **data dumps** of the whole catalog are not rate limited and the docs tell you to use them rather than crawl [V].
- Licence (`/developers/concepts/license-and-attribution`): MangaBaka-original data CC BY-NC-SA 4.0; free for personal/non-commercial use with credit to MangaBaka and the data providers; commercial use refers to a pricing page; third-party data (AniList, MAL, etc.) stays under each provider's terms [V]. Data refreshed weekly [S: web search summary of the API page].
- Endpoints relevant: `/v1/series/{id}`, `/v2/series/{id}` (beta, typed numbers), `/v1/series/{id}/full` (adds raw source fields), `/v1/series/search`, `/v1/series/{id}/images`, `/v1/series/{id}/relationships`, `/v1/series/{id}/links`, `/v1/series/{id}/works` and `/v1/works/{id}` (beta, volume records), `/v1/collections/{id}` (internal), `/v1/editions/{id}` (beta), `/v1/publishers/{id}`, `/v1/genres`, `/v1/tags`, `/v1/source/{anilist|kitsu|manga-updates|my-anime-list|anime-planet}/{id}` (lookup by other provider's ID).

**Series object** (`/v1/series/{id}`; v2 differences noted):

| Field | Type | Notes |
|---|---|---|
| id | integer | |
| state | enum active, merged, deleted | `merged_with` gives the new ID |
| merged_with | number or null | |
| canonical_url | uri | |
| title, native_title, romanized_title, secondary_titles | string / object | marked "Use the titles property instead" |
| titles[] | array | `{language, traits[official/native/alternative], title, note, is_primary}`; v2 omits `note` and returns only the best title per language |
| cover | object | `raw{url,size,height,width,blurhash,thumbhash,format}`, `x150`, `x250`, `x350` each `{x1,x2,x3}`; v2 adds blurhash/width/height at top |
| authors, artists | array of string or null | names only, no IDs or roles |
| description | string or null | |
| year | number or null | deprecated, use `published` |
| published | object | `start_date`, `end_date` (YYYY-MM-DD), `start_date_is_estimated`, `end_date_is_estimated` |
| status | enum | cancelled, completed, hiatus, releasing, unknown, upcoming |
| is_licensed | boolean | licensed in English |
| has_anime, anime | boolean, object | `anime{start,end}` strings like "Vol 1 (S1)" (v2 adds `exists`) |
| content_rating | enum | safe, suggestive, erotica, pornographic ("highest level of sexual content shown") |
| type | enum | manga, novel, manhwa, manhua, oel, other |
| original_language | enum, BCP 47 | about 100 codes, including `zh-Hans`, `zh-Hant`, `zh-Hant-TW`, `zh-Hant-HK`, `yue-Hant-HK`, `es-la`, `pt-br`; nullable |
| rating | number or null | 0-100 average across sources; v2 adds `rating_count` |
| popularity | object | `global` and `type` each `{current rank, history{1d,1w,1mo,3mo,6mo,1y}}` |
| final_volume | string (v1) / number (v2) | |
| total_chapters | string (v1) / number (v2) | |
| links (deprecated), links_v2[] | array | `{id, url, name (host), name_display, type, language}`, type enum: retailer, publisher, webplatform, info, social, news, piracy, other |
| publishers[] | array | `{id, name, canonical_url, language, note, type}`; listed once per release language; `type` (Original/English/Other) deprecated |
| genres_v2 | null | "Not populated"; filter `tags_v2` on `is_genre` |
| genres (deprecated) | 46 values | action, adult, adventure, avant_garde, award_winning, boys_love, comedy, doujinshi, drama, ecchi, erotica, fantasy, gender_bender, girls_love, gourmet, harem, hentai, historical, horror, josei, lolicon, mahou_shoujo, martial_arts, mature, mecha, music, mystery, psychological, romance, school_life, sci-fi, seinen, shotacon, shoujo, shoujo_ai, shounen, shounen_ai, slice_of_life, smut, sports, supernatural, suspense, thriller, tragedy, yaoi, yuri |
| tags_v2[] | array | `{id, merged_with, is_spoiler, is_genre, is_explicit, implied_by_tag_ids[], parent_id, name, level, name_path ("Activities > Physical Activities > Swordplay"), series_count, description, content_rating, weight}`; weight enum core, defining, recurrent, incidental, unweighted |
| tags (deprecated) | string[] | "values are NOT stable" |
| relationships_v2[] | array | `{id, to_series_id, relation_type, is_manual, note, chronology}`; enum in Section 3.6a; chronology narrative / release / unknown |
| source | object | keys anilist, anime_planet, anime_news_network, kitsu, manga_updates, my_anime_list, shikimori; each `{id, rating, rating_normalized}`; no Bangumi, Hikka, Comick entries |
| last_updated_at | datetime | |

Live tag taxonomy: 7,153 tags; 19 root groups (Activities, Audience Demographics, Character Archetype, Character Traits, Character Types, Derivative Work, Locations, Narrative Tropes, Objects, Occupations, Relationship, Settings, Sexual Content, Species & Creatures, Themes, Time Period, Tone, Work Info, World Building); tag content_rating counts: safe 6,987, pornographic 87, erotica 65, suggestive 14.

**Volume-level records** (beta `/v1/works`): `id` uuid, `series_id`, `source_ids`, `sub_title`, `count_type` (main, extra, other), `release_date`, `sequence_string`, `sequence_numeric`, `identifiers[{id,name}]`, `trim`, `description`, `note`, `pages`, `price[{value,iso_code}]`, `links[{type,link,language}]`, `inc_chapters`, `part_of_volume`, `revision`, `images[]`. **Collections** (internal): `title, language, publisher, edition, type, format, medium, status, reading, licensed, description, note, start_date, end_date, links, related_collection_id, count_main/extra/other`. **Cover images** (`/v1/series/{id}/images`): `type` enum audiobook, banner, chapter, other, season, volume, volume_back; `language`, `content_rating`, `hashes{md5,sha1,ahash,chash,crc32,dhash,phash,whash,sha256}`. These beta/internal shapes were read from the OpenAPI document only; not exercised live [partly V].

### 7.2 MyAnimeList (official API v2)

- `https://api.myanimelist.net/v2`. Spec read from the embedded OpenAPI in `https://myanimelist.net/apiconfig/references/api/v2` [V]. A live unauthenticated call returned 403 (needs a client ID/OAuth) [V].
- Terms (`https://myanimelist.net/static/apiagreement.html`, summarised by the fetch tool; verify before relying) [S]: API limited to apps that interoperate with MAL; commercial applications need written approval before earning revenue (s. 3(a)(xiv)); no server-side storing of user personal information or user-generated content; client-side storage only for as long as reasonably necessary; delete/modify within 24 hours of a removal request; no scraping outside the API; no numeric rate limit stated ("must not place any unreasonable burden"). Practical consequence: an offline sidecar generator that caches MAL synopsis/scores is in a grey area.
- Fields are opt-in via `fields=`; the spec's listed example for manga requests: `id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_volumes,num_chapters,authors{first_name,last_name},pictures,background,related_anime,related_manga,recommendations,serialization{name}`.

| Field | Type | Notes |
|---|---|---|
| id | integer | |
| title | string | |
| main_picture | `{large?, medium}` | |
| alternative_titles | object | spec: `"synonyms" or ISO 639-1` keys; so `synonyms[]`, `en`, `ja` |
| start_date, end_date | string | "YYYY", "YYYY-MM" or "YYYY-MM-DD" |
| synopsis | string | BBCode stripped |
| mean | number | omitted when too few scores |
| rank, popularity | integer | |
| num_list_users, num_scoring_users | integer | |
| nsfw | string | white, gray, black |
| genres | `[{id,name}]` | |
| created_at, updated_at | string | ISO 8601 |
| media_type | string | unknown, manga, novel, one_shot, doujinshi, manhwa, manhua, oel |
| status | string | finished, currently_publishing, not_yet_published |
| num_volumes, num_chapters | integer | 0 if unknown |
| authors | `[{node{id,first_name,last_name}, role}]` | `role` is an unconstrained string (values not enumerated in the spec) |
| pictures, background | array, string | detail only |
| related_anime, related_manga | arrays of `{node, relation_type, relation_type_formatted}` | relation_type: sequel, prequel, alternative_setting, alternative_version, side_story, parent_story, summary, full_story |
| recommendations | `[{node, num_recommendations}]` | |
| serialization | `[{node{id,name}, role}]` | |
| my_list_status | user list data | excluded without token |
| ranking | `{rank, previous_rank}` | on `/manga/ranking`; ranking_type: all, manga, novels, oneshots, doujin, manhwa, manhua, bypopularity, favorite |

No publisher, no characters, no staff roles beyond `authors`, no tags/themes in the official API [V by absence in spec].

**Jikan (unofficial, scrapes MAL; not official)** `https://api.jikan.moe/v4`. Live request timed out; schema read from `https://github.com/jikan-me/jikan-rest/blob/master/storage/api-docs/api-docs.json` (version 4.0.0) [V spec, X live]. Limits 60/min, 3/s; responses cached 24 h; read-only; "It's still possible to get rate limited from MyAnimeList.net". Extra over official: `url`, `images{jpg,webp}{image_url,small_image_url,large_image_url}`, `approved`, `titles[{type,title}]`, `title_english`, `title_japanese`, `title_synonyms`, `published{from,to,prop{from{day,month,year},to{...}}}` (date parts), `publishing`, `scored_by`, `members`, `favorites`, `authors[]`/`serializations[]`/`genres[]`/`explicit_genres[]`/`themes[]`/`demographics[]` as `{mal_id,type,name,url}`, `relations[]`, `external[]{name,url}`. Endpoints: `/manga/{id}/full`, `/characters`, `/pictures`, `/statistics`, `/moreinfo`, `/recommendations`, `/reviews`, `/relations`, `/external`, `/genres/manga`. Jikan search enums: type manga, novel, lightnovel, oneshot, doujin, manhwa, manhua; status publishing, complete, hiatus, discontinued, upcoming. Terms of Jikan data not read [X]; because it scrapes MAL, MAL's agreement s. 4(i) (no scraping outside the API) is relevant [S].

### 7.3 AniList

- `https://graphql.anilist.co`. Schema read by live introspection [V].
- Auth: none for public queries. Rate limit: docs say 90 requests/min, with a banner saying the API is currently limited to 30/min as a temporary degraded-state measure; `X-RateLimit-*`, `Retry-After` headers; 1-minute timeout on excess [V: AniList/docs repo `docs/guide/rate-limiting.md`].
- Terms (`docs/guide/terms-of-use.md`) [V]: free for non-commercial; commercial use under 150 USD/month revenue is free, above needs a licence; using the API as a backup or data storage service is prohibited; "Hoarding or mass collection" is prohibited; apps must follow naming guidelines; use inside competing, non-complementary services (anime/manga list or tracker services) is prohibited, covering all data including media data. (The `anilist.co/terms` and `docs.anilist.co` pages returned 403 or an empty app shell [X].)

`Media` type fields (introspected): `id, idMal, title{romaji,english,native,userPreferred}, type (MediaType ANIME|MANGA), format, status, description, startDate, endDate (FuzzyDate {year,month,day}), season, seasonYear, seasonInt, episodes, duration, chapters, volumes, countryOfOrigin (CountryCode scalar, ISO 3166-1 alpha-2), isLicensed, source, hashtag, trailer, updatedAt, coverImage{extraLarge,large,medium,color}, bannerImage, genres[String], synonyms[String], weightedScore, meanScore, popularity, isLocked, trending, favourites, tags[MediaTag], relations (MediaConnection), characters, staff, studios, isAdult, nextAiringEpisode, airingSchedule, trends, externalLinks[], streamingEpisodes, rankings[], recommendations, reviews, stats, siteUrl, modNotes`. `averageScore` is queryable (returned 84 for a sample) but did not appear in the introspected field list [V live; inconsistency noted].

Manga-relevant enums: `MediaFormat` MANGA, NOVEL, ONE_SHOT; `MediaStatus` FINISHED, RELEASING, NOT_YET_RELEASED, CANCELLED, HIATUS; `MediaSource` ORIGINAL, MANGA, LIGHT_NOVEL, VISUAL_NOVEL, VIDEO_GAME, OTHER, NOVEL, DOUJINSHI, ANIME, WEB_NOVEL, LIVE_ACTION, GAME, COMIC, MULTIMEDIA_PROJECT, PICTURE_BOOK; `MediaRelation` in Section 3.6a; `CharacterRole` MAIN, SUPPORTING, BACKGROUND; `ExternalLinkType` INFO, STREAMING, SOCIAL; `MediaRankType` RATED, POPULAR.

- Genres (19): Action, Adventure, Comedy, Drama, Ecchi, Fantasy, Hentai, Horror, Mahou Shoujo, Mecha, Music, Mystery, Psychological, Romance, Sci-Fi, Slice of Life, Sports, Supernatural, Thriller.
- Tags: 430; `MediaTag` `{id, name, description, category, rank, isGeneralSpoiler, isMediaSpoiler, isAdult, userId}`. `rank` is a 0-100 relevance (sample values 95, 93, 92...). Categories seen (counts): Cast-Traits 73, Sexual Content 66, Theme-Other 60, Theme-Game-Sport 31, Setting-Scene 24, Technical 21, Theme-Fantasy 19, Theme-Romance 17, Theme-Arts 15, Cast-Main Cast 12, Theme-Drama 11, ... Demographic 5 (Josei, Kids, Seinen, Shoujo, Shounen). "Technical" includes 4-koma, Full Color, Long Strip, Anthology, Gekiga, Non-fiction, ...
- Staff: `StaffEdge{node, id, role (String), favouriteOrder}`; role is free text with scope, e.g. "Story & Art (vols 1-41)", "Translator (English: vols 5-8, 10-)", "Supervisor (vols 41- )" [V live sample]. `Staff{id, name{first,middle,last,full,native,alternative[],userPreferred}, languageV2, image, description, primaryOccupations[], gender, dateOfBirth, dateOfDeath, age, yearsActive[], homeTown, bloodType, ...}`.
- Characters: `Character{id, name, image, description, gender, dateOfBirth, age, bloodType, ...}`.
- External links sample: Young Animal (STREAMING), Official Site (INFO, per language), Lezhin, Naver Series, Twitter (SOCIAL)...
- **Absent for manga**: publisher, serialization magazine, demographic field (tag only), age rating enum, per-volume data, origin language (country only).

### 7.4 Kitsu

- `https://kitsu.io/api/edge/` (JSON:API; `Accept: application/vnd.api+json`). Public read, no auth required [V live and `apiary.apib` from `hummingbird-me/api-docs`]. The docs say the unversioned `edge` path "may change at any time"; previous major versions are kept one year or until under 2% traffic [V]. No rate-limit or licence text in the docs I read [X].
- Docs state: "NSFW/R18 content (feed posts, media, categories etc.) are hidden for all unauthenticated requests and for accounts that have NSFW content disabled" [V].
- Manga attributes from a live sample [V]: `createdAt, updatedAt, slug, synopsis, description, coverImageTopOffset, titles{en_jp,en_us,...}, canonicalTitle, abbreviatedTitles[], averageRating ("71.36", percent string), ratingFrequencies{2..20: count} (ten half-point buckets keyed 2 to 20), userCount, favoritesCount, startDate, endDate, nextRelease, popularityRank, ratingRank, ageRating (null in sample), ageRatingGuide, subtype, status, tba, posterImage{tiny,small,medium,large,original,meta{dimensions}}, coverImage, chapterCount, volumeCount, serialization (string), mangaType`.
- Enums from server source `hummingbird-me/kitsu-server` [V]: manga `subtype` manga 0, novel 1, manhua 2, oneshot 3, doujin 4, manhwa 5, oel 6; `age_rating` G, PG, R, R18; media `status` tba, unreleased, upcoming, current, finished (computed from start/end dates); `MediaRelationship.role` sequel, prequel, alternative_setting, alternative_version, side_story, parent_story, summary, full_story, spinoff, adaptation, character, other; `MediaCharacter.role` main, supporting, recurring, cameo; `MangaCharacter.role` main, supporting. Media model also has `origin_countries` and `origin_languages` validated attributes [S: model source; not in the manga response sample].
- Relationships exposed on a manga: genres, categories, castings, installments, mappings, reviews, mediaRelationships (path is `media-relationships`; `/manga/1/mediaRelationships` 404s), characters, staff, productions, quotes. Genre object `{name, slug, description}`; Category `{title, description, totalMediaCount, slug, nsfw, childCount}` with parent (hierarchy); Staff `{role}` free text linking to `person`; Chapter `{synopsis, titles, canonicalTitle, volumeNumber, number, published, length, thumbnail}`; Mapping `{externalSite, externalId}` (samples: `myanimelist/manga`, `anilist/manga`). Server also has a `Volume` model (number, titles, chapters_count) but I did not confirm a public `/volumes` route [U].

### 7.5 MangaUpdates

- `https://api.mangaupdates.com/v1`, OpenAPI 3.0 at `https://api.mangaupdates.com/openapi.yaml` [V]. Public reads need no account.
- Terms (in the spec description) [V]: no warranties; credit MangaUpdates; "reasonable spacing between requests" and "employ caching"; must not deceive, assist illegal action, spam, damage the database. No numeric rate limit.
- Series object (`GET /series/{id}`, live sample for Berserk) [V]: `series_id, title, url, associated[{title}], description, image{url{original,thumb},height,width}, type, year (string), bayesian_rating, rating_votes, genres[{genre}], categories[{series_id,category,votes,votes_plus,votes_minus,added_by}], latest_chapter, forum_id, status (free text), licensed, completed, anime{start,end}, related_series[{relation_id,relation_type,related_series_id,related_series_name,related_series_url,triggered_by_relation_id}], authors[{name,author_id,url,type}] (type Author or Artist), publishers[{publisher_name,publisher_id,url,type (language, e.g. English/Original),notes}], publications[{publication_name,publisher_name,publisher_id}] (magazine; publisher_name text like "Hakusensha; since 1992"), recommendations[], category_recommendations[], rank{position{week,month,three_months,six_months,year},old_position,lists{reading,wish,complete,unfinished,custom}}, last_updated{timestamp,as_rfc3339,as_string}, admin{approved,added_by}`.
- Enums [V spec]: `type` list in 3.2a; `related_series.relation_type` in 3.6a; genre list (36; `demographic:true` on Josei, Lolicon, Seinen, Shotacon, Shoujo, Shoujo Ai, Shounen, Shounen Ai, Yaoi, Yuri); search `orderby` score, title, rank, rating, year, date_added, week_pos...; `filter(s)` scanlated, completed, oneshots, no_oneshots, some_releases, no_releases. Author record (`/authors/{id}`): `name, associated, image, actualname, birthday, birthplace, bloodtype, gender, status (Active, Temporarily Inactive, Retired, Deceased), genres, stats, social{officialsite,facebook,twitter}`. Publisher record `type` is a language: N/A, Japanese, English, Korean, Taiwanese, Chinese, Thai, Indonesian, Filipino, Vietnamese, Malaysian, Nordic, French, Spanish, Russian, Polish, Portuguese, German, Hindi, Arabic. Release record (`/releases`) `{id,title,volume,chapter,groups[{name,group_id,url}],release_date,download_notes,comment}`.
- Notable: `categories` is the user-voted tag system (hundreds per series for popular titles; 268 for Berserk) with plus/minus votes. Status text carries volume counts and creator-change notes, unparseable without heuristics.

### 7.6 Shikimori

- REST v1/v2 + GraphQL at `https://shikimori.io/api/...` (`shikimori.one` returns 301 to `shikimori.io`) [V live]. Doc page `https://shikimori.io/api/doc`.
- Rules (from the doc page JSON) [V]: 5 requests/s and 90/min; the app name must be in `User-Agent`; "Don't mimic a browser"; "Please do not parse the main site". No licence text found [X]. GraphQL query depth is limited to 5 (error "Query has depth of 6, which exceeds max depth of 5") [V].
- REST `/api/mangas/{id}` live fields: `id, name, russian, image{original,preview,x96,x48}, url, kind, score (string), status, volumes, chapters, aired_on, released_on, english[], japanese[], synonyms[], license_name_ru, description, description_html, description_source, franchise, favoured, anons, ongoing, thread_id, topic_id, myanimelist_id, rates_scores_stats[{name,value}], rates_statuses_stats[], licensors[], genres[{id,name,russian,kind,entry_type}], publishers[{id,name}], user_rate`. Related: `/mangas/{id}/roles` (each `{roles[], roles_russian[], character, person}`), `/related` (`{relation, relation_russian, anime, manga}`), `/external_links` (`{kind,url,source,entry_id,entry_type,...}`).
- GraphQL `Manga` fields (introspected): `airedOn, releasedOn (IncompleteDate {date,day,month,year}), chapters, volumes, characterRoles, chronology, externalLinks, franchise, genres, id, isCensored, japanese, english, kind, licenseNameRu, licensors, malId, name, personRoles (PersonRole {person, rolesEn[], rolesRu[]}), poster, publishers, related (Related {relationKind, relationText, anime, manga}), russian, score, scoresStats, status, statusesStats, synonyms, topic, url`. `Person{birthOn, deceasedOn, isMangaka, isProducer, isSeyu, japanese, malId, name, russian, synonyms, website, ...}`.
- Enums [V introspection]: `MangaKindEnum` manga, manhwa, manhua, light_novel, novel, one_shot, doujin; `MangaStatusEnum` anons, ongoing, released, paused, discontinued; `RelationKindEnum` in 3.6a; `GenreKindEnum` demographic, genre, theme; `ExternalLinkKindEnum` (36) official_site, wikipedia, anime_news_network, myanimelist, anime_db, world_art, kinopoisk, kage_project, twitter, smotret_anime, shiki, amediateka, crunchyroll, amazon, hidive, hulu, ivi, deep, kinopoisk_hd, wink, netflix, okko, youtube, remanga, senkuro, mangalib, mangaupdates, readmanga, mangadex, mangafox, mangachan, mangahub, novel_tl, ruranobe, ranobelib, novelupdates.
- Manga genre taxonomy (GraphQL `genres(entryType: Manga)`, 81): demographic Shounen, Shoujo, Seinen, Josei, Kids; genre (22) Sci-Fi, Drama, Suspense, Horror, Slice of Life, Supernatural, Gourmet, Comedy, Ecchi, Fantasy, Romance, Avant Garde, Adventure, Boys Love, Girls Love, Action, Mystery, Sports, Erotica, Hentai, Yaoi, Yuri; theme (54) including Isekai, Reincarnation, Harem, Gore, School, ... (the older v1 `/api/genres` returns a different 48-item MAL-classic manga list such as Josei, Demons, Police: the two taxonomies coexist).
- Notable: Russian-language fields (`russian`, `license_name_ru`, `licensors`) show Russian licensing; "ranobe" URLs for novels. Staff roles are free text strings in two languages.

### 7.7 Bangumi

- `https://api.bgm.tv`; OpenAPI at `https://bangumi.github.io/api/dist.json` (version 2026-07-24) [V]. Requires an informative `User-Agent` (default library UAs may be blocked; docs name the format `author/app (url)`) [V: repo `docs-raw/user agent.md`]. Access-token for authenticated calls generated at `next.bgm.tv/demo/access-token`. Rate-limit/licence text: none found [X].
- Subject (`GET /v0/subjects/{id}`): `id, type (SubjectType 1 book, 2 anime, 3 music, 4 game, 6 real), name, name_cn, summary, series (bool, "is the main entry of a book series"), nsfw, locked, date (YYYY-MM-DD, "air date"), platform (string, e.g. TV, Web...), images{large,common,medium,small,grid}, infobox (array of {key, value: string or [{k?,v}]}), volumes ("number of volumes, parsed by the old server from the wiki"), eps, total_episodes, rating{rank,total,count{1..10},score}, collection{wish,collect,doing,on_hold,dropped}, meta_tags[] (curated tags), tags[{name,count,total_count}]`.
- Book categories (`SubjectBookCategory`): 0 other, 1001 comic, 1002 novel, 1003 illustration. List endpoint `/v0/subjects` has `type`, `cat`, `series`, `sort` (date|rank), `year`, `month` params.
- **Per-volume model**: each physical volume is a separate subject; a volume's `/v0/subjects/{id}/subjects` returned a relation named `系列` ("series") pointing to the series subject [V live, one sample]. Volume sample infobox keys: 出版社 (publisher), 价格 (price), 发售日 (release date), 页数 (pages), ISBN, ISBN-10, 作者 (author) [V one sample]. The author key and role strings are free Chinese text.
- People: `RelatedPerson{id,name,type (PersonType 1 individual, 2 corporation, 3 association),career[] (producer, mangaka, artist, seiyu, writer, illustrator, actor),images,relation (role string),eps}`; characters: `RelatedCharacter{id,name,summary,type (1 character, 2 mechanic, 3 ship, 4 organization),images,relation,actors[]}`.
- Value caveat: `/v0/search/subjects` with `keyword` returned unrelated results in my test (the keyword appeared ignored) [V as observed; cause unknown]. `/v0/subjects/{id}/persons` returned empty for the sample volume (staff are on the series subject, not per volume) [V one sample].
- Adult: `nsfw` boolean; Komf notes a token is needed to see NSFW items [S].

### 7.8 Hikka

- `https://api.hikka.io`, FastAPI, OpenAPI at `/openapi.json` (version 0.4.4), Swagger UI at `/docs` [V]. Public reads work without auth; no licence/terms or rate-limit text found [X].
- `GET /manga/{slug}` (`MangaInfoResponse`): `data_type, review_stats{maybe,yes,no}, authors[{roles[{name_ua,name_en,weight,slug}], person{data_type,name_native,name_ua,name_en,image,slug,description_ua,synonyms[]}}], magazines[{name_en,slug}], external[{url,text,type (general|watch|read)}], start_date, end_date (integer epoch seconds), created, updated, genres[{name_ua,name_en,slug,type}], title_original, title_native, stats{completed,reading,on_hold,dropped,planned,score_1..score_10}, synopsis_en, synopsis_ua, media_type, native_scored_by, chapters, title_en, title_ua, synonyms[], comments_count, has_franchise, translated_ua, native_score, volumes, status, image, year, scored_by, score, mal_id, nsfw, slug`.
- Enums [V spec]: `MangaMediaEnum` one_shot, doujin, manhua, manhwa, manga; `ContentStatusEnum` discontinued, announced, finished, ongoing, paused; `ReadStatusEnum` completed, reading, on_hold, dropped, planned; `ReadContentTypeEnum` manga, novel. Genres (live `/genres`): theme (52), genre (18), demographic (Josei, Kids, Seinen, Shoujo, Shounen), explicit (Erotica, Ecchi, Hentai); each with `name_en`, `name_ua`, `slug`.
- Characters: `/manga/{slug}/characters` returns `{main: bool, character{name_ua,name_en,name_ja,image,slug,synonyms}}`. No `/manga/{slug}/staff` (404).
- Notable: Ukrainian localisation fields (`title_ua`, `synopsis_ua`, `translated_ua` = fan translation exists); both "score" (community) and "native_score" (Ukrainian user score). Paths use slug with a hash suffix (e.g. `berserk-fb9fbd`), not the MAL ID. One image URL only.

### 7.9 Comick

**Status (current as of 2026-11-16).**

- `comick.io` and `comick.fun` serve a page "Comick has a new home — comick.dev" that redirects after 5 seconds [V live].
- `comick.dev` is the live site; it is behind a Cloudflare challenge for plain HTTP clients (a browser-based fetch got through) [V].
- Old API hosts: `api.comick.io` returned HTTP 522 and `api.comick.fun` failed to connect [V live]. The new catalog API is `https://api.comick.dev` with docs at `https://api.comick.dev/docs/` and OpenAPI 3.0.3 (v1.1) at `https://api.comick.dev/docs/json` [V].
- Web search results (news and social posts, not read in full) report that the original Comick shut down on 16 September 2025 after pressure from publishers, and that "comick.dev" is a later legal tracking/wiki site described as unaffiliated in one article [S]. I did not verify the relationship between the old and new operators [X]. Treat any ID continuity with the old `comick.io` dataset as unconfirmed.

**API.** Terms/licence for data: none read [X]. Developer docs at `https://comick.dev/docs` describe an OAuth library API (follows, status, progress, ratings) and "Catalog API ... Basic catalog requests do not require an account or an OAuth token" [V]. Limits: 200 requests/min/IP at the origin; search page and limit caps (page ≤ 50 with limit ≤ 50, or page ≤ 5 with limit ≤ 300); latest chapters empty above page 100; `x-ratelimit-*` and `Retry-After` headers; "these limits do not provide an exhaustive catalog-export contract"; Cloudflare may challenge [V].

Endpoints [V]: `/v1.0/search/`, `/v1.0/comic/{slug}/` (manga, anime or novel), `/v1.0/comic/{hid}/chapters`, `/comic/{slug}/` and `/comic/{hid}/chapters` (legacy), `/chapter/`, `/chapter/{hid}/`, `/chapter/{hid}/get_images`, `/genre/`, `/category/`, `/category/popular`, `/people/{slug}/`, `/top`, `/anime/...`, `/integrations/v1/...` (OAuth).

Detail response schema is declared only as `{"type":"object","additionalProperties":true}`, so the shape below comes from one live sample (`00-solo-leveling`) [V live, shape only]:

- Top level: `firstChapters[]{vol,title,chap,hid,lang,created_at,up_count,group_name[],md_chapters_groups}`, `comic{...}`, `artists[{name,slug}]`, `authors[{name,slug}]`, `langList[]`, `recommendable`, `demographic` (string, e.g. "Shounen"), `englishLink`, `matureContent`.
- `comic`: `id, hid, title, country, status (int), links{al, ap, kt, mal, mb, mu, engtl, othertl, wiki, raw, fandom, anilist_url, mal_url, urls{engtl[],othertl[],wiki[],raw[]}, resolved_external_links{...}, mal_external_links, anilist_external_links}, last_chapter, chapter_count, demographic (int), user_follow_count, follow_rank, desc, parsed (HTML), slug, mismatch, year, to_year, media_type, rating, bayesian_rating, rating_count, content_rating, violence_rating, comment_count, review_count, translation_completed, translation_status, chapter_numbers_reset_on_new_volume_manual, final_chapter, final_volume, anime{start,end}, has_anime, statistics[], recommendations[], relate_from[{relate_to{id,hid,slug,title,year,country,media_type,content_rating,violence_rating,md_titles[],md_covers[]},md_relates{name}}], is_english_title, md_titles[{id,title,lang,user_id,is_default}], md_comic_md_genres[{md_genres{name,type,slug,group}}], md_covers[{vol,w,h,b2key,gpurl,is_primary}], mu_comics{mu_comic_publishers[{mu_publishers{id,title,slug},type}],licensed_in_english,mu_comic_categories[...]}, mu_comic_categories[{mu_categories{id,title,slug,comic_count},positive_vote,negative_vote,score}], reviews[], iso639_1, lang_name, lang_native, publishers[{id,title,slug}]`.
- Meaning of the `links` short keys (`al`, `ap`, `kt`, `mal`, `mb`, `mu`) is not documented; `al`=AniList, `mal`=MyAnimeList, `kt`=Kitsu, `mu`=MangaUpdates fit the sample values, `ap` looks like Anime-Planet and `mb` is unknown [U].
- Documented query enums [V]: `status` 1 ongoing, 2 completed, 3 cancelled, 4 hiatus; `demographic` 1 shounen, 2 shoujo, 3 seinen, 4 josei, 5 unset; `content_rating` safe, suggestive, erotica, pornographic; `violence_rating` none, graphic; `country` lowercase codes such as jp, kr, cn; `type` user, author, group, comic; `media_type` manga, anime (novel on details); `sort` view, created_at, uploaded, rating, average_rating, follow, user_follow_count; language codes include en, fr, pt-br, es-419 (not country codes).
- `/genre/` returns `{id, name, slug, comic_count, group}` (group e.g. "Format"); includes 4-Koma, Adult, Doujinshi, Ecchi, Erotica, Full Color, Hentai, Incest, Loli, Long Strip, ... `/category/` returned 9,474 tags (MangaUpdates-derived, with votes).
- Notable: unique among the nine for chapter-level translation data (languages, groups, upload times) and per-volume covers; relation type list is undocumented; tag/category data is borrowed from MangaUpdates.

---

## 8. Open questions and things I could not verify

**Could not reach or confirm**

| Item | State |
|---|---|
| MAL official API live responses | Needs a client ID; spec read only. Author `role` value list not in the spec. No numeric rate limit anywhere. |
| MAL API agreement | Read via the fetch tool's summary, not verbatim [S]. |
| Jikan live | Request timed out; schema from the repo's OpenAPI. |
| AniList terms page | `anilist.co/terms` returned an empty app shell; `docs.anilist.co` 403. Used the `AniList/docs` GitHub repo markdown instead. |
| Kitsu rate limits, terms, whether `/volumes` is a public route | Not found. |
| Bangumi rate limits, licence; infobox key vocabulary for manga | Not found; keys seen from one volume sample only. |
| Hikka and Shikimori licence terms | Not found. |
| MangaUpdates numeric rate limit | None stated. |
| MangaBaka `works`/`collections`/`editions` real data | Schemas read from the OpenAPI; no live calls. These endpoints are marked beta/internal. |
| Comick: relationship between old comick.io and current comick.dev; meaning of `links.mb`; relation-type vocabulary; licence terms | Not confirmable. Shutdown story is from web-search summaries. |
| Hentag API | Site is closing; no docs found. |
| Fakku, Hitomi, Tsumino, HentaiNexus, Doujinshi.org, Melonbooks, Toranoana, Comiket catalog | Not examined. "Event" field existence for adult content is therefore unresolved. |
| E-Hentai API | Read from the community wiki only, not the API itself (needs valid gallery tokens). Terms of use not read. |
| nhentai terms of API use | Not read. |
| LANraragi namespaces/plugins | Docs pages fetched did not contain details. |
| Kavita reading `series.json` | Not confirmed either way. |
| Komga: other series-level sidecars | Only Mylar `series.json` confirmed in source. |

**Decisions the data does not settle**

1. One XML schema with series and file roots, or XML for files plus JSON for series?
2. Whether `MangaInfo.xml` should embed provider IDs and fetched scores (licence-sensitive: MAL, AniList, MangaBaka non-commercial terms).
3. Genre/tag vocabulary: own controlled list with per-provider mapping, or provider-tagged free strings?
4. Adult rating: adopt the four-level safe/suggestive/erotica/pornographic scale (shared by MangaBaka, Comick, MangaDex) alongside or instead of ComicInfo's `AgeRating`?
5. How to carry roles that include volume ranges (AniList style) without free text parsing.
6. Whether to treat Bangumi-style per-volume subjects and MangaBaka `works` as the model for per-file records.

