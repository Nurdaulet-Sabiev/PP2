# phonebook.py
import csv
import json
from datetime import datetime, date
from pathlib import Path

import psycopg2
from psycopg2 import sql

from connect import get_connection
from config import PAGE_SIZE

ROOT = Path(__file__).resolve().parent
SCHEMA_FILE = ROOT / "schema.sql"
PROCEDURES_FILE = ROOT / "procedures.sql"

PHONE_TYPES = ("home", "work", "mobile")
DEFAULT_GROUPS = ("Family", "Work", "Friend", "Other")

def read_sql_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def run_sql_file(path: Path) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(read_sql_file(path))
    print(f"Executed {path.name}")

def run_sql_script(path: Path) -> None:
    script = read_sql_file(path)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(script)
    print(f"Executed {path.name}")
def parse_date(value: str | None):
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()

def normalize_group(value: str | None) -> str:
    if not value or not value.strip():
        return "Other"
    return value.strip().capitalize()

def normalize_phone_type(value: str | None) -> str:
    if not value or not value.strip():
        return "mobile"
    v = value.strip().lower()
    if v not in PHONE_TYPES:
        raise ValueError("Phone type must be home, work, or mobile")
    return v

def get_group_id(cur, group_name: str | None):
    cur.execute("SELECT ensure_group(%s);", (normalize_group(group_name),))
    return cur.fetchone()[0]

def contact_exists(cur, name: str) -> bool:
    cur.execute("SELECT 1 FROM contacts WHERE name = %s;", (name,))
    return cur.fetchone() is not None

def get_contact_id(cur, name: str):
    cur.execute("SELECT id FROM contacts WHERE name = %s;", (name,))
    row = cur.fetchone()
    return row[0] if row else None

def add_contact_interactive():
    name = input("Name: ").strip()
    if not name:
        print("Name is required.")
        return

    email = input("Email: ").strip() or None
    birthday = parse_date(input("Birthday (YYYY-MM-DD): ").strip() or None)
    group_name = normalize_group(input("Group (Family/Work/Friend/Other): "))
    phones = []
    while True:
        phone = input("Phone number (leave empty to stop): ").strip()
        if not phone:
            break
        try:
            ptype = normalize_phone_type(input("Phone type (home/work/mobile): "))
        except ValueError as e:
            print(e)
            continue
        phones.append((phone, ptype))

    if not phones:
        print("At least one phone number is required.")
        return

    with get_connection() as conn:
        with conn.cursor() as cur:
            if contact_exists(cur, name):
                print("Contact already exists. Use update/import overwrite logic instead.")
                return

            cur.execute("SELECT ensure_group(%s);", (group_name,))
            group_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (name, email, birthday, group_id),
            )
            contact_id = cur.fetchone()[0]

            for phone, ptype in phones:
                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type;
                    """,
                    (contact_id, phone, ptype),
                )
    print("Contact added.")

def fetch_contacts_page(limit=PAGE_SIZE, offset=0, group_name=None, email_query=None, sort_by="name"):
    sort_map = {
        "name": "c.name",
        "birthday": "c.birthday NULLS LAST",
        "date": "c.created_at",
    }
    order_by = sort_map.get(sort_by, "c.name")
    params = []
    where = []

    if group_name:
        where.append("g.name = %s")
        params.append(normalize_group(group_name))
    if email_query:
        where.append("COALESCE(c.email, '') ILIKE %s")
        params.append(f"%{email_query}%")

    where_sql = "WHERE " + " AND ".join(where) if where else ""
    query = f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            c.created_at,
            COALESCE(
                string_agg(p.phone || ' (' || p.type || ')', ', ' ORDER BY p.id),
                ''
            ) AS phones
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where_sql}
        GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_by}
        LIMIT %s OFFSET %s
    """
    params.extend([limit, offset])

    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
                rows = cur.fetchall()
                cols = [d.name for d in cur.description]
                result = [dict(zip(cols, row)) for row in rows]
                if result:
                    return result
            except Exception:
                conn.rollback()
            cur.execute(query, params)
            cols = [d.name for d in cur.description]
            rows = cur.fetchall()
            return [dict(zip(cols, row)) for row in rows]

def count_contacts(group_name=None, email_query=None):
    params = []
    where = []
    if group_name:
        where.append("g.name = %s")
        params.append(normalize_group(group_name))
    if email_query:
        where.append("COALESCE(c.email, '') ILIKE %s")
        params.append(f"%{email_query}%")
    where_sql = "WHERE " + " AND ".join(where) if where else ""
    query = f"""
        SELECT COUNT(DISTINCT c.id)
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        LEFT JOIN phones p ON p.contact_id = c.id
        {where_sql}
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()[0]

def print_rows(rows):
    if not rows:
        print("No contacts found.")
        return
    for row in rows:
        print("-" * 60)
        print(f"ID: {row.get('id') or row.get('contact_id')}")
        print(f"Name: {row['name']}")
        print(f"Email: {row.get('email') or ''}")
        print(f"Birthday: {row.get('birthday') or ''}")
        print(f"Group: {row.get('group_name') or ''}")
        print(f"Created: {row.get('created_at') or ''}")
        print(f"Phones: {row.get('phones') or ''}")

def browse_contacts():
    group_name = input("Filter by group (blank for all): ").strip() or None
    email_query = input("Search by email (blank for all): ").strip() or None
    sort_by = input("Sort by name / birthday / date: ").strip().lower() or "name"
    page = 0

    while True:
        total = count_contacts(group_name, email_query)
        pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        if page >= pages:
            page = pages - 1

        rows = fetch_contacts_page(
            limit=PAGE_SIZE,
            offset=page * PAGE_SIZE,
            group_name=group_name,
            email_query=email_query,
            sort_by=sort_by,
        )

        print(f"\nPage {page + 1} / {pages} | Total: {total}")
        print_rows(rows)
        cmd = input("\n[next / prev / quit]: ").strip().lower()
        if cmd == "next":
            if page + 1 < pages:
                page += 1
            else:
                print("Already at last page.")
        elif cmd == "prev":
            if page > 0:
                page -= 1
            else:
                print("Already at first page.")
        elif cmd == "quit":
            break

def search_contacts_db():
    query = input("Search query: ").strip()
    if not query:
        return
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s);", (query,))
            rows = cur.fetchall()
            cols = [d.name for d in cur.description]
            results = [dict(zip(cols, row)) for row in rows]
    print_rows(results)

def add_phone_via_procedure():
    name = input("Contact name: ").strip()
    phone = input("Phone number: ").strip()
    ptype = normalize_phone_type(input("Phone type (home/work/mobile): "))
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s, %s, %s);", (name, phone, ptype))
    print("Phone added.")

def move_contact_group_via_procedure():
    name = input("Contact name: ").strip()
    group_name = input("New group: ").strip()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s, %s);", (name, group_name))
    print("Contact moved.")

def upsert_contact_from_dict(contact: dict, overwrite: bool):
    name = contact.get("name", "").strip()
    if not name:
        return

    email = contact.get("email") or None
    birthday = parse_date(contact.get("birthday")) if contact.get("birthday") else None
    group_name = normalize_group(contact.get("group") or contact.get("group_name") or "Other")
    phones = contact.get("phones") or []
    if isinstance(phones, dict):
        phones = [phones]

    with get_connection() as conn:
        with conn.cursor() as cur:
            existing_id = get_contact_id(cur, name)
            cur.execute("SELECT ensure_group(%s);", (group_name,))
            group_id = cur.fetchone()[0]

            if existing_id is None:
                cur.execute(
                    """
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (name, email, birthday, group_id),
                )
                contact_id = cur.fetchone()[0]
            else:
                contact_id = existing_id
                if overwrite:
                    cur.execute(
                        """
                        UPDATE contacts
                        SET email = %s, birthday = %s, group_id = %s
                        WHERE id = %s
                        """,
                        (email, birthday, group_id, contact_id),
                    )

            for phone in phones:
                phone_value = phone.get("phone", "").strip()
                if not phone_value:
                    continue
                ptype = normalize_phone_type(phone.get("type") or "mobile")
                cur.execute(
                    """
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (contact_id, phone) DO UPDATE SET type = EXCLUDED.type
                    """,
                    (contact_id, phone_value, ptype),
                )

def export_to_json():
    file_name = input("JSON file name (default contacts.json): ").strip() or "contacts.json"
    out_path = ROOT / file_name

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    c.id,
                    c.name,
                    c.email,
                    c.birthday,
                    g.name AS group_name,
                    c.created_at
                FROM contacts c
                LEFT JOIN groups g ON g.id = c.group_id
                ORDER BY c.name
                """
            )
            contacts = cur.fetchall()
            cols = [d.name for d in cur.description]
            contact_rows = [dict(zip(cols, row)) for row in contacts]

            cur.execute(
                """
                SELECT p.contact_id, p.phone, p.type
                FROM phones p
                ORDER BY p.contact_id, p.id
                """
            )
            phone_rows = cur.fetchall()
            phone_map = {}
            for contact_id, phone, ptype in phone_rows:
                phone_map.setdefault(contact_id, []).append({"phone": phone, "type": ptype})

    payload = []
    for c in contact_rows:
        payload.append({
            "name": c["name"],
            "email": c["email"],
            "birthday": c["birthday"].isoformat() if c["birthday"] else None,
            "group": c["group_name"],
            "created_at": c["created_at"].isoformat() if c["created_at"] else None,
            "phones": phone_map.get(c["id"], []),
        })

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Exported to {out_path}")

def import_from_json():
    file_name = input("JSON file name: ").strip()
    if not file_name:
        return
    in_path = ROOT / file_name
    if not in_path.exists():
        print("File not found.")
        return

    data = json.loads(in_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        print("JSON must contain a list of contacts.")
        return

    for item in data:
        name = item.get("name", "").strip()
        if not name:
            continue

        with get_connection() as conn:
            with conn.cursor() as cur:
                exists = contact_exists(cur, name)

        if exists:
            choice = input(f'Duplicate "{name}". [s]kip or [o]verwrite? ').strip().lower()
            if choice == "s":
                continue
            overwrite = choice == "o"
        else:
            overwrite = False

        upsert_contact_from_dict(item, overwrite=overwrite)
    print("Import finished.")

def import_from_csv():
    file_name = input("CSV file name: ").strip()
    if not file_name:
        return
    in_path = ROOT / file_name
    if not in_path.exists():
        print("File not found.")
        return

    with in_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    grouped = {}
    for row in rows:
        name = (row.get("name") or "").strip()
        if not name:
            continue
        grouped.setdefault(name, {
            "name": name,
            "email": row.get("email"),
            "birthday": row.get("birthday"),
            "group": row.get("group"),
            "phones": [],
        })
        phone = (row.get("phone") or "").strip()
        if phone:
            grouped[name]["phones"].append({
                "phone": phone,
                "type": row.get("phone_type") or "mobile",
            })

    for contact in grouped.values():
        upsert_contact_from_dict(contact, overwrite=True)

    print("CSV import finished.")

def menu():
    print("\nPhoneBook")
    print("1. Add contact")
    print("2. Browse contacts")
    print("3. Search contacts")
    print("4. Add phone to contact")
    print("5. Move contact to group")
    print("6. Export to JSON")
    print("7. Import from JSON")
    print("8. Import from CSV")
    print("9. Install schema")
    print("10. Install procedures")
    print("0. Quit")

def main():
    while True:
        menu()
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                add_contact_interactive()
            elif choice == "2":
                browse_contacts()
            elif choice == "3":
                search_contacts_db()
            elif choice == "4":
                add_phone_via_procedure()
            elif choice == "5":
                move_contact_group_via_procedure()
            elif choice == "6":
                export_to_json()
            elif choice == "7":
                import_from_json()
            elif choice == "8":
                import_from_csv()
            elif choice == "9":
                run_sql_script(SCHEMA_FILE)
            elif choice == "10":
                run_sql_script(PROCEDURES_FILE)
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
