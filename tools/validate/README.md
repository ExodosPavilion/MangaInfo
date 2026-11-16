# Validation

These scripts check the example files against the two schemas. They also check a set of small test cases: files that must pass and files that must fail.

Run them after each change to a schema or an example.

## Setup (one time)

```sh
cd tools/validate
pip install -r requirements.txt
npm install
```

## Run

```sh
cd tools/validate
npm run validate
```

Or run one side only, from any folder:

```sh
python tools/validate/validate_xml.py    # MangaInfo.xml against schema/1/MangaInfo.xsd
node tools/validate/validate_json.mjs    # MangaSeries.json against schema/1/MangaSeries.schema.json
```

Each script prints one line for each case and exits with code 1 if a case does not behave as expected.

## Add a case

- A new example folder: add its name to `EXAMPLES` in the script for its file type.
- A new rule in a schema: add one case that must pass and one that must fail to `CASES`.
