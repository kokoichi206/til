CREATE TABLE schedule (
  id SERIAL PRIMARY KEY NOT NULL,
  name TEXT NOT NULL,
  reservation_time TSRANGE NOT NULL,
  EXCLUDE USING GIST (reservation_time WITH &&)
);

INSERT INTO schedule (name, reservation_time)
VALUES
('a', '[2024-01-01 10:00, 2024-01-01 12:00)'),
('b', '[2025-01-25 11:00, 2025-01-28 13:00)')
;

-- これは範囲に重複があるので制約でエラーになる！！
INSERT INTO schedule (name, reservation_time) VALUES
('a', '[2024-01-01 10:00, 2024-01-01 12:00)'),
('b', '[2025-01-01 11:00, 2025-01-01 13:00)')
;

SELECT * FROM schedule
WHERE reservation_time @> '2024-01-01 11:00'::TIMESTAMP
;

SELECT * FROM schedule
WHERE reservation_time && '[2024-01-01 11:50, 2024-01-01 13:00)'::TSRANGE
;
