DROP TABLE IF EXISTS memo;

CREATE TABLE memo
(
    uid    TEXT NOT NULL,
    memo   TEXT NOT NULL,
    secret INTEGER NOT NULL
);

INSERT INTO memo (uid, memo, secret) VALUES 
(
  'redacted',
  'LINECTF{redacted}',
  TRUE
),
(
  'redacted',
  'Oh, How did you find my memo?',
  FALSE
);