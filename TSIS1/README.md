# TSIS 1 — PhoneBook Extended Contact Management

## Files
- `phonebook.py` — console application
- `config.py` — database settings
- `connect.py` — PostgreSQL connection helper
- `schema.sql` — updated schema
- `procedures.sql` — new procedures and function
- `contacts.csv` — sample import file

## Requirements
Install:
```bash
pip install psycopg2-binary
```

## Setup
1. Create a PostgreSQL database, for example `phonebook`.
2. Edit `config.py` with your credentials.
3. Run `schema.sql`.
4. Run `procedures.sql`.
5. Start the app:
```bash
python phonebook.py
```

## Notes
- JSON export includes contacts with all phones.
- JSON import asks whether to skip or overwrite duplicates by name.
- CSV import expects columns: `name,email,birthday,group,phone,phone_type`.
- The app can also use an existing pagination function from your previous practice if it exists; otherwise it falls back to `LIMIT/OFFSET`.
