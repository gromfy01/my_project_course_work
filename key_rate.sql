DROP TABLE IF EXISTS key_rate;
CREATE TABLE key_rate (
    month VARCHAR(12),
    key_rate NUMERIC(4, 2)
);

INSERT INTO key_rate (month, key_rate)
VALUES
('January23', 7.5),
('February23', 7.5),
('March23', 7.5),
('April23', 7.5),
('May23', 7.5),
('June23', 7.5),
('July23', 7.5),
('August23', 8.5),
('September23', 12),
('October23', 13),
('November23', 15),
('December23', 15),
('January24', 16);

SELECT * FROM key_rate;