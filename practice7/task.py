"""
PhoneBook CLI using PostgreSQL + psycopg2
Based on: https://www.postgresqltutorial.com/postgresql-python/ (psycopg / psycopg2 recommended). See citation in chat.

Features implemented:
- create table `phonebook` (id, first_name, last_name, phone, email, created_at)
- insert in two ways:
  1) upload CSV file (COPY FROM STDIN)
  2) interactive console input (prompt for name + phone)
- update records (change first name or phone)
- query records with different filters (by first/last name, phone, LIKE search)
- delete by username (first name + optional last name) or by phone

Requirements:
- Python 3.8+
- psycopg2-binary (`pip install psycopg2-binary`)

Environment variables (or change defaults in script):
- PGHOST (default: localhost)
- PGPORT (default: 5432)
- PGUSER
- PGPASSWORD
- PGDATABASE

CSV format (header optional). Example rows (comma separated):
first_name,last_name,phone,email
John,Doe,+7-701-123-4567,john@example.com
Alice,Smith,+7-701-987-6543,alice@example.com

Usage examples:
python phonebook.py init
python phonebook.py import-csv data.csv
python phonebook.py add
python phonebook.py update-name --by-phone "+7-701-123-4567" --new-first "Johnny"
python phonebook.py update-phone --by-name "John" --new-phone "+7-777-000-0000"
python phonebook.py query --first "John"
python phonebook.py query --like "Al"
python phonebook.py delete-by-phone "+7-701-123-4567"
python phonebook.py delete-by-name --first "Alice" --last "Smith"

"""

import os
import argparse
import csv
import sys
from datetime import datetime

import psycopg2
from psycopg2 import sql

# DB connection helpers ------------------------------------------------------

def get_conn():
    params = dict(
        host='localhost',
        port='5432',
        user='postgres',
        password='0',  # ваш пароль
        dbname='postgres',
    )
    conn = psycopg2.connect(**params)
    return conn

# Schema / DDL ----------------------------------------------------------------

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                phone VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255),
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW())
            );
        ''')
    conn.commit()
    print('Table `phonebook` created or already exists.')

# Insertion methods ----------------------------------------------------------

def import_csv(conn, filepath, has_header=True):
    """Bulk import from CSV using COPY. CSV columns should be first_name,last_name,phone,email
    """
    with conn.cursor() as cur, open(filepath, 'r', encoding='utf-8') as f:
        # If the CSV has a header, skip it for COPY by reading into a temporary file or using copy_expert
        if has_header:
            # Use COPY with CSV HEADER to handle header automatically
            sql_copy = sql.SQL("COPY phonebook (first_name, last_name, phone, email) FROM STDIN WITH (FORMAT csv, HEADER true)")
            cur.copy_expert(sql_copy.as_string(conn), f)
        else:
            cur.copy_expert("COPY phonebook (first_name, last_name, phone, email) FROM STDIN WITH (FORMAT csv)", f)
    conn.commit()
    print('CSV imported.')


def insert_single(conn, first_name, last_name, phone, email=None):
    with conn.cursor() as cur:
        cur.execute(
            '''INSERT INTO phonebook (first_name, last_name, phone, email) VALUES (%s, %s, %s, %s)
               ON CONFLICT (phone) DO UPDATE SET first_name = EXCLUDED.first_name, last_name = EXCLUDED.last_name, email = EXCLUDED.email
            ''',
            (first_name, last_name, phone, email)
        )
    conn.commit()
    print(f'Inserted/updated {first_name} {last_name} ({phone}).')

# Console input insertion -----------------------------------------------------

def add_from_console(conn):
    print('Add new contact (leave last name or email empty if none).')
    first = input('First name: ').strip()
    if not first:
        print('First name is required.')
        return
    last = input('Last name: ').strip() or None
    phone = input('Phone: ').strip()
    if not phone:
        print('Phone is required.')
        return
    email = input('Email: ').strip() or None
    try:
        insert_single(conn, first, last, phone, email)
    except Exception as e:
        print('Error inserting:', e)
        conn.rollback()

# Updating records ------------------------------------------------------------

def update_first_name_by_phone(conn, phone, new_first_name):
    with conn.cursor() as cur:
        cur.execute('UPDATE phonebook SET first_name = %s WHERE phone = %s RETURNING id, first_name, last_name, phone', (new_first_name, phone))
        res = cur.fetchone()
    if res:
        conn.commit()
        print('Updated:', res)
    else:
        print('No record found with phone', phone)


def update_phone_by_name(conn, first_name, last_name, new_phone):
    with conn.cursor() as cur:
        if last_name:
            cur.execute('UPDATE phonebook SET phone = %s WHERE first_name = %s AND last_name = %s RETURNING id, first_name, last_name, phone', (new_phone, first_name, last_name))
        else:
            cur.execute('UPDATE phonebook SET phone = %s WHERE first_name = %s RETURNING id, first_name, last_name, phone', (new_phone, first_name))
        res = cur.fetchone()
    if res:
        conn.commit()
        print('Updated:', res)
    else:
        print('No record found for name', first_name, last_name)

# Querying --------------------------------------------------------------------

def query_all(conn, limit=100):
    with conn.cursor() as cur:
        cur.execute('SELECT id, first_name, last_name, phone, email, created_at FROM phonebook ORDER BY id LIMIT %s', (limit,))
        rows = cur.fetchall()
    return rows


def query_by_first(conn, first):
    with conn.cursor() as cur:
        cur.execute('SELECT id, first_name, last_name, phone, email FROM phonebook WHERE first_name = %s', (first,))
        return cur.fetchall()


def query_by_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute('SELECT id, first_name, last_name, phone, email FROM phonebook WHERE phone = %s', (phone,))
        return cur.fetchall()


def query_like_name(conn, like_term):
    pattern = f"%{like_term}%"
    with conn.cursor() as cur:
        cur.execute('SELECT id, first_name, last_name, phone, email FROM phonebook WHERE first_name ILIKE %s OR last_name ILIKE %s', (pattern, pattern))
        return cur.fetchall()

# Deleting --------------------------------------------------------------------

def delete_by_phone(conn, phone):
    with conn.cursor() as cur:
        cur.execute('DELETE FROM phonebook WHERE phone = %s RETURNING id, first_name, last_name, phone', (phone,))
        res = cur.fetchone()
    if res:
        conn.commit()
        print('Deleted:', res)
    else:
        print('No record found with phone', phone)


def delete_by_name(conn, first_name, last_name=None):
    with conn.cursor() as cur:
        if last_name:
            cur.execute('DELETE FROM phonebook WHERE first_name = %s AND last_name = %s RETURNING id, first_name, last_name, phone', (first_name, last_name))
        else:
            cur.execute('DELETE FROM phonebook WHERE first_name = %s RETURNING id, first_name, last_name, phone', (first_name,))
        res = cur.fetchall()
    if res:
        conn.commit()
        print(f'Deleted {len(res)} record(s).')
        for r in res:
            print(r)
    else:
        print('No records found with name', first_name, last_name)

# CLI -------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Simple PhoneBook backed by PostgreSQL')
    sub = parser.add_subparsers(dest='cmd')

    sub.add_parser('init', help='Create phonebook table')

    p_import = sub.add_parser('import-csv', help='Import CSV into phonebook')
    p_import.add_argument('file', help='CSV file path')
    p_import.add_argument('--no-header', action='store_true', help='CSV has no header')

    sub.add_parser('add', help='Add a contact from console')

    p_upd1 = sub.add_parser('update-name', help='Update first name by phone')
    p_upd1.add_argument('--phone', required=True)
    p_upd1.add_argument('--new-first', required=True)

    p_upd2 = sub.add_parser('update-phone', help='Update phone by name')
    p_upd2.add_argument('--by-name', required=True, help='First name (or "First Last")')
    p_upd2.add_argument('--new-phone', required=True)

    p_q = sub.add_parser('query', help='Query contacts')
    p_q.add_argument('--all', action='store_true')
    p_q.add_argument('--first', help='Exact first name')
    p_q.add_argument('--phone', help='Exact phone')
    p_q.add_argument('--like', help='Partial search on first or last name')
    p_q.add_argument('--limit', type=int, default=100)

    p_del1 = sub.add_parser('delete-by-phone', help='Delete contact by phone')
    p_del1.add_argument('phone')

    p_del2 = sub.add_parser('delete-by-name', help='Delete contact(s) by name')
    p_del2.add_argument('--first', required=True)
    p_del2.add_argument('--last', help='Optional last name')

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    conn = get_conn()
    try:
        if args.cmd == 'init':
            create_table(conn)

        elif args.cmd == 'import-csv':
            import_csv(conn, args.file, has_header=not args.no_header)

        elif args.cmd == 'add':
            add_from_console(conn)

        elif args.cmd == 'update-name':
            update_first_name_by_phone(conn, args.phone, args.new_first)

        elif args.cmd == 'update-phone':
            # allow "First Last" or just "First"
            parts = args.by_name.strip().split(None, 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else None
            update_phone_by_name(conn, first, last, args.new_phone)

        elif args.cmd == 'query':
            if args.all:
                rows = query_all(conn, limit=args.limit)
            elif args.first:
                rows = query_by_first(conn, args.first)
            elif args.phone:
                rows = query_by_phone(conn, args.phone)
            elif args.like:
                rows = query_like_name(conn, args.like)
            else:
                print('Specify a filter for query (e.g. --all, --first, --phone, or --like)')
                return
            for r in rows:
                print(r)

        elif args.cmd == 'delete-by-phone':
            delete_by_phone(conn, args.phone)

        elif args.cmd == 'delete-by-name':
            delete_by_name(conn, args.first, args.last)

    finally:
        conn.close()

if __name__ == '__main__':
    main()