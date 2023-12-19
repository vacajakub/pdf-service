BEGIN;

DROP TYPE IF EXISTS document_state CASCADE;
CREATE TYPE document_state AS ENUM (
  'processing',
  'done'
);


DROP TABLE IF EXISTS documents CASCADE;
CREATE TABLE documents (
    id                  INT PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    status              document_state,
    n_pages             INT NOT NULL
);


DROP TABLE IF EXISTS pages CASCADE;
CREATE TABLE pages (
    document_id         INT NOT NULL,
    document_page       INT NOT NULL,
    image               bytea NOT NULL,

    FOREIGN KEY (document_id) REFERENCES documents (id)
);

CREATE UNIQUE INDEX document_id_page ON pages (document_id, document_page);

COMMIT;
