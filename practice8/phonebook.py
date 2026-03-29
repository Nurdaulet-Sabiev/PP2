import argparse
import psycopg2
import sys

# ---------------- DB CONNECTION ----------------
def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="0",
        port="5432"
    )

# ---------------- INIT DATABASE ----------------
def init_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),
            phone VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255),
            created_at TIMESTAMP DEFAULT NOW()
        );
        """)

        # Function search by pattern
        cur.execute("""
        CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
        RETURNS TABLE (
            id INT,
            first_name VARCHAR,
            last_name VARCHAR,
            phone VARCHAR,
            email VARCHAR
        )
        LANGUAGE sql
        AS $$
            SELECT id, first_name, last_name, phone, email
            FROM phonebook
            WHERE first_name ILIKE '%' || pattern || '%'
               OR last_name ILIKE '%' || pattern || '%'
               OR phone ILIKE '%' || pattern || '%'
            ORDER BY id;
        $$;
        """)

        # Procedure upsert user
        cur.execute("""
        CREATE OR REPLACE PROCEDURE upsert_user(
            p_first_name TEXT,
            p_last_name TEXT,
            p_phone TEXT,
            p_email TEXT
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM phonebook
                WHERE first_name = p_first_name
                  AND COALESCE(last_name,'') = COALESCE(p_last_name,'')
            ) THEN
                UPDATE phonebook
                SET phone = p_phone,
                    email = p_email
                WHERE first_name = p_first_name
                  AND COALESCE(last_name,'') = COALESCE(p_last_name,'');
            ELSE
                INSERT INTO phonebook(first_name, last_name, phone, email)
                VALUES (p_first_name, p_last_name, p_phone, p_email);
            END IF;
        END;
        $$;
        """)

        # Procedure insert many users
        cur.execute("""
        CREATE OR REPLACE PROCEDURE insert_many_users(
            first_names TEXT[],
            last_names TEXT[],
            phones TEXT[],
            emails TEXT[]
        )
        LANGUAGE plpgsql
        AS $$
        DECLARE
            i INT;
        BEGIN
            FOR i IN 1..array_length(first_names, 1)
            LOOP
                IF phones[i] ~ '^[0-9+]+$' THEN
                    CALL upsert_user(first_names[i], last_names[i], phones[i], emails[i]);
                ELSE
                    RAISE NOTICE 'Incorrect phone: %', phones[i];
                END IF;
            END LOOP;
        END;
        $$;
        """)

        # Pagination function
        cur.execute("""
        CREATE OR REPLACE FUNCTION get_phonebook_page(lim INT, offs INT)
        RETURNS TABLE (
            id INT,
            first_name VARCHAR,
            last_name VARCHAR,
            phone VARCHAR,
            email VARCHAR
        )
        LANGUAGE sql
        AS $$
            SELECT id, first_name, last_name, phone, email
            FROM phonebook
            ORDER BY id
            LIMIT lim OFFSET offs;
        $$;
        """)

        # Delete procedure
        cur.execute("""
        CREATE OR REPLACE PROCEDURE delete_user(
            p_first_name TEXT,
            p_phone TEXT
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            IF p_phone IS NOT NULL THEN
                DELETE FROM phonebook WHERE phone = p_phone;
            ELSE
                DELETE FROM phonebook WHERE first_name = p_first_name;
            END IF;
        END;
        $$;
        """)

    conn.commit()
    print("Database initialized")


# ---------------- SEARCH ----------------
def search_pattern(conn, pattern):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
        for row in cur.fetchall():
            print(row)


# ---------------- UPSERT ----------------
def upsert_user(conn, first, last, phone, email):
    with conn.cursor() as cur:
        cur.execute("CALL upsert_user(%s, %s, %s, %s)",
                    (first, last, phone, email))
    conn.commit()
    print("User inserted/updated")


# ---------------- BULK INSERT ----------------
def bulk_insert(conn):
    n = int(input("How many users: "))
    first_names, last_names, phones, emails = [], [], [], []

    for i in range(n):
        print("User", i+1)
        first_names.append(input("First name: "))
        last_names.append(input("Last name: "))
        phones.append(input("Phone: "))
        emails.append(input("Email: "))

    with conn.cursor() as cur:
        cur.execute("CALL insert_many_users(%s, %s, %s, %s)",
                    (first_names, last_names, phones, emails))
    conn.commit()
    print("Bulk insert done")


# ---------------- PAGINATION ----------------
def pagination(conn, limit, offset):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM get_phonebook_page(%s, %s)", (limit, offset))
        for row in cur.fetchall():
            print(row)


# ---------------- DELETE ----------------
def delete_user(conn, first_name=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("CALL delete_user(%s, %s)", (first_name, phone))
    conn.commit()
    print("User deleted")


# ---------------- CLI ----------------
def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("init")

    s = sub.add_parser("search")
    s.add_argument("--pattern")

    u = sub.add_parser("upsert")
    u.add_argument("--first")
    u.add_argument("--last")
    u.add_argument("--phone")
    u.add_argument("--email")

    sub.add_parser("bulk")

    p = sub.add_parser("page")
    p.add_argument("--limit", type=int)
    p.add_argument("--offset", type=int)

    d = sub.add_parser("delete")
    d.add_argument("--first")
    d.add_argument("--phone")

    args = parser.parse_args()

    conn = get_conn()

    if args.cmd == "init":
        init_db(conn)
    elif args.cmd == "search":
        search_pattern(conn, args.pattern)
    elif args.cmd == "upsert":
        upsert_user(conn, args.first, args.last, args.phone, args.email)
    elif args.cmd == "bulk":
        bulk_insert(conn)
    elif args.cmd == "page":
        pagination(conn, args.limit, args.offset)
    elif args.cmd == "delete":
        delete_user(conn, args.first, args.phone)
    else:
        print("Commands: init, search, upsert, bulk, page, delete")

    conn.close()


if __name__ == "__main__":
    main()