-- Runs on DB init
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS stories;
DROP TABLE IF EXISTS exports;

CREATE TABLE images (
  id        INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id VARCHAR(36) NOT NULL,
  "image"   BYTEA        NOT NULL
);

CREATE TABLE stories (
  id         INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id  VARCHAR(36) NOT NULL,
  "text"     TEXT        NOT NULL CHECK (length("text") > 0 AND length("text") < 100),
  "action"   TEXT        NOT NULL CHECK (length("action") > 0 AND length("action") < 50),
  "image_id" INTEGER     NOT NULL REFERENCES images(id)
);

CREATE TABLE exports (
  id          INTEGER     GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id   VARCHAR(36) NOT NULL,
  story_id    INTEGER     NOT NULL REFERENCES stories(id),
  dimensions  TEXT        NOT NULL,
  progress    TEXT        NOT NULL,
  ready       boolean     NOT NULL DEFAULT FALSE,
  image       BYTEA            NULL
);
