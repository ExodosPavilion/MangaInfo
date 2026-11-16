# MangaInfo

A metadata format for manga, manhwa and manhua. It describes a series and the archives that belong to it, for readers and library tools.

## Language

### Files

**MangaInfo file**:
The metadata file that describes one archive. Its name is `MangaInfo.xml`.
_Avoid_: ComicInfo, sidecar, book metadata

**Series file**:
The metadata file that describes one series. Its name is `MangaSeries.json`.
_Avoid_: series.json (the Mylar file), series metadata, series sidecar

**Series folder**:
The folder that holds one series file and the archives of that series.
_Avoid_: Library folder, directory

**Archive**:
One file that holds the pages of a unit, with its MangaInfo file inside.
_Avoid_: Book, issue, comic file

### Structure

**Series**:
A work that is published in parts under one title.
_Avoid_: Title, comic, entry, subject

**Unit**:
What one archive contains: a volume, a chapter, a chapter range, a one-shot or a gallery.
_Avoid_: Book, issue, release

**Unit type**:
The value that states which kind of unit an archive contains.

**Chapter range**:
A unit of several consecutive chapters that is not an official volume.
_Avoid_: Batch, pack

**Volume**:
A unit that the publisher released as one collected book.
_Avoid_: Tankobon, book

**Chapter**:
One serialized installment of a series.
_Avoid_: Episode, issue

**One-shot**:
A complete work in one unit that has no series.

**Gallery**:
A standalone unit that has no series, typical for doujinshi.
_Avoid_: Album, set

**Series identity**:
The small set of series facts that a MangaInfo file repeats, so that an archive is usable without its series file.

**Description**:
The set of descriptive facts about a work, such as titles, creators, genres and tags. A series file holds a full description; a MangaInfo file holds one only for a unit that has no series.

**Standalone unit**:
A unit that has no series file: a one-shot or a gallery.

### Titles and people

**Title**:
One name of a series or unit, with its language and its kind: official, alternative or abbreviated.
_Avoid_: Name, synonym, alias

**Primary title**:
The one title that tools show by default.
_Avoid_: Main title, canonical title, display title

**Creator**:
A person or group credited for a work, with a role.
_Avoid_: Author, staff, person

**Role**:
What a creator did on a work, such as story, art or translator.
_Avoid_: Job, position, credit type

### Publication

**Edition**:
One published version of a series in one language by one publisher.
_Avoid_: Release, localization, version

**Publisher**:
The company that publishes an edition.
_Avoid_: Licensor, label

**Imprint**:
A brand name that a publisher uses for a line of its books.
_Avoid_: Label, line

**Magazine**:
A periodical in which the chapters of a series first appeared.
_Avoid_: Publication, serialization, anthology

**Scanlation group**:
The fan group that translated and prepared an unofficial edition of a unit.
_Avoid_: Scanlator, group, release group

### Reading

**Reading mode**:
How the pages of a unit are meant to be read: right to left, left to right, vertical or long strip.
_Avoid_: Reading direction, viewer mode

**Long strip**:
A reading mode where the pages form one continuous vertical scroll.
_Avoid_: Webtoon, continuous, infinite scroll

**Page type**:
The purpose of one page in a unit, such as cover, story or advertisement.

### Classification

**Format**:
The kind of work a series is, such as manga, manhwa, manhua or doujinshi.
_Avoid_: Type, media type, kind, subtype

**Publication type**:
How a work reached readers: commercial, doujinshi or webcomic. It is independent of format.
_Avoid_: Release type, distribution

**Origin country**:
The country where a series was first published.
_Avoid_: Country, nationality

**Original language**:
The language in which a series was first published.
_Avoid_: Source language, native language

**Publication status**:
The state of the original publication of a series, such as ongoing or completed.
_Avoid_: Status, state

**Demographic**:
The audience that the original publication was aimed at, such as shounen or josei.
_Avoid_: Audience, target

**Content rating**:
The level of sexual content in a series or unit.
_Avoid_: Age rating, NSFW flag, maturity

**Genre**:
A broad category of story, written as free text.

**Tag**:
A specific descriptive label, written as free text.
_Avoid_: Category, theme, keyword

**Tag namespace**:
A group name in front of a tag that states who or what the tag applies to, such as female or male.
_Avoid_: Prefix, tag category

**Spoiler tag**:
A tag that reveals part of the story.

**Summary**:
The text that describes the story of a series or unit, in one language.
_Avoid_: Description, synopsis, blurb

**Character**:
A named person in the story of a work.

**Relation**:
A typed link from one series to another series, such as sequel or spin-off.
_Avoid_: Related series, relationship

### Adult content

**Parody**:
The existing work that a derivative work is based on.
_Avoid_: Source work, franchise

**Circle**:
The group of creators that produced a doujinshi.
_Avoid_: Group, doujin group

**Event**:
The convention where a doujinshi was first released, such as Comiket.
_Avoid_: Convention, release event

**Censorship state**:
How explicit imagery is obscured in a unit.
_Avoid_: Censored flag

**Decensored**:
A censorship state where fans removed the censorship from an official release.
_Avoid_: Uncensored (which means the official release had no censorship)

### Sources

**Provider**:
An external site or service that supplies metadata about series.
_Avoid_: Source, metadata site, database

**External ID**:
The identifier of a series or unit at a provider.
_Avoid_: Mapping, link ID

**Link**:
A web address about a work, with an optional kind and language. It does not identify the work at a provider.
_Avoid_: URL, external link, web

**Cover**:
An image that represents a series or one of its volumes, given as a web address.
_Avoid_: Poster, thumbnail, main picture

**Licensed language**:
A language in which a series has an official licensed edition.
_Avoid_: Licensed flag, is licensed

**Extension data**:
Data that a tool keeps in a file for its own use. It is not part of the format.
_Avoid_: Custom fields, plugin data, metadata extras

**Provider mapping**:
The conversion of one provider's fields and values to the fields and values of the format.
_Avoid_: Crosswalk, translation table

**Override**:
A value in a MangaInfo file that replaces a series value for that unit only.

**Volatile data**:
Provider data that changes often, such as scores, ranks and follower counts. It is not part of the format.
_Avoid_: Stats, ratings
