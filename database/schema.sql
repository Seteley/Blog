-- PostgreSQL — ejecutar una sola vez (o dejar que entrypoint.sh lo aplique)

CREATE TABLE IF NOT EXISTS articles (
    id         SERIAL        PRIMARY KEY,
    title      VARCHAR(200)  NOT NULL,
    content    TEXT          NOT NULL,
    created_at TIMESTAMPTZ   NOT NULL DEFAULT NOW()
);
