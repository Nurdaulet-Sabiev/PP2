-- schema.sql
-- Fresh schema for TSIS 1 PhoneBook extended model.
-- Safe to run multiple times.

CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) UNIQUE NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);
CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts(created_at);

CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);

CREATE INDEX IF NOT EXISTS idx_phones_contact_id ON phones(contact_id);
CREATE INDEX IF NOT EXISTS idx_phones_phone ON phones(phone);

CREATE OR REPLACE FUNCTION ensure_group(p_group_name VARCHAR)
RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    IF p_group_name IS NULL OR btrim(p_group_name) = '' THEN
        p_group_name := 'Other';
    END IF;

    INSERT INTO groups(name)
    VALUES (INITCAP(btrim(p_group_name)))
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = INITCAP(btrim(p_group_name));

    RETURN v_group_id;
END;
$$;

-- Optional helper for full name listing in the app.
CREATE OR REPLACE VIEW contacts_with_phones AS
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
GROUP BY c.id, c.name, c.email, c.birthday, g.name, c.created_at;
