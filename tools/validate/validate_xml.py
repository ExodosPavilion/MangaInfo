"""Validate the MangaInfo examples and a set of test cases against the XSD.

Usage: python tools/validate/validate_xml.py
Needs: lxml (pip install -r tools/validate/requirements.txt)
Exit code 0 when every case behaves as expected, 1 otherwise.
"""

import sys
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[2]
NS = "https://exodospavilion.github.io/MangaInfo/1"
EXAMPLES = ["manga-volume", "manhwa-chapter", "doujinshi-gallery"]

schema = etree.XMLSchema(etree.parse(str(ROOT / "schema" / "1" / "MangaInfo.xsd")))
failures = 0


def check(label, doc, want_valid):
    """Validate one document and compare the result with what is expected."""
    global failures
    is_valid = schema.validate(doc)
    as_expected = is_valid == want_valid
    if not as_expected:
        failures += 1
    print("PASS" if as_expected else "FAIL", label, "->", "valid" if is_valid else "invalid")
    if not as_expected and not is_valid:
        print("     ", schema.error_log.last_error)


def wrap(body, version="1.0.0"):
    """Build a MangaInfo document around the given child elements."""
    text = f'<MangaInfo xmlns="{NS}" version="{version}">{body}</MangaInfo>'
    return etree.fromstring(text.encode("utf-8"))


SERIES = '<Series><Titles><Title primary="true">T</Title></Titles></Series>'
CHAPTER = '<Unit type="chapter"/>'

for name in EXAMPLES:
    path = ROOT / "examples" / name / "MangaInfo.xml"
    check(f"example {name}", etree.parse(str(path)), True)

# Each case: label, document, expected validity.
CASES = [
    ("minimal file", wrap(CHAPTER + SERIES), True),
    (
        "child order is free inside Unit",
        wrap('<Unit type="volume"><PageCount>10</PageCount><Volume>1</Volume></Unit>' + SERIES),
        True,
    ),
    (
        "extension contents are free",
        wrap(
            CHAPTER
            + SERIES
            + '<Extensions><Extension tool="t"><Anything a="1"><Deep/></Anything>text'
            + "</Extension></Extensions>"
        ),
        True,
    ),
    ("misspelled field", wrap('<Unit type="chapter"><Titel>x</Titel></Unit>' + SERIES), False),
    ("missing unit type", wrap("<Unit/>" + SERIES), False),
    ("unknown unit type", wrap('<Unit type="book"/>' + SERIES), False),
    ("no series and no description", wrap(CHAPTER), False),
    (
        "two primary titles",
        wrap(
            CHAPTER
            + '<Series><Titles><Title primary="true">A</Title>'
            + '<Title primary="true">B</Title></Titles></Series>'
        ),
        False,
    ),
    (
        "primary=false is not allowed",
        wrap(CHAPTER + '<Series><Titles><Title primary="false">A</Title></Titles></Series>'),
        False,
    ),
    (
        "bad enum value",
        wrap('<Unit type="chapter"><ReadingMode>webtoon</ReadingMode></Unit>' + SERIES),
        False,
    ),
    (
        "month 13",
        wrap('<Unit type="chapter"><ReleaseDate year="2020" month="13"/></Unit>' + SERIES),
        False,
    ),
    (
        "uppercase provider key",
        wrap(
            CHAPTER
            + '<Series><Titles><Title primary="true">T</Title></Titles>'
            + '<ExternalIds><ExternalId provider="AniList">1</ExternalId></ExternalIds></Series>'
        ),
        False,
    ),
    ("version 2.0.0", wrap(CHAPTER + SERIES, version="2.0.0"), False),
    (
        "duplicate page index",
        wrap(
            '<Unit type="chapter"><Pages><Page index="0"/><Page index="0"/></Pages></Unit>'
            + SERIES
        ),
        False,
    ),
    (
        "two summaries in one language",
        wrap(
            '<Unit type="gallery"/><Description><Titles><Title primary="true">T</Title></Titles>'
            + '<Summaries><Summary language="en">a</Summary><Summary language="en">b</Summary>'
            + "</Summaries></Description>"
        ),
        False,
    ),
    ("unknown top-level element", wrap(CHAPTER + SERIES + "<Score>9</Score>"), False),
]

for label, doc, want_valid in CASES:
    check(label, doc, want_valid)

print("xml failures:", failures)
sys.exit(1 if failures else 0)
