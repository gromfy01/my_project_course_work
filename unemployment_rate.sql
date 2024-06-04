DROP TABLE IF EXISTS unemployment;
CREATE TABLE unemployment (
    month VARCHAR(12),
    unemployment_rate NUMERIC(4, 2)
);

INSERT INTO unemployment (month, unemployment_rate)
VALUES
('January23', 3.6),
('February23', 3.5),
('March23', 3.5),
('April23', 3.3),
('May23', 3.2),
('June23', 3.1),
('July23', 3.0),
('August23', 3.0),
('September23', 3.0),
('October23', 2.9),
('November23', 2.9),
('December23', 3.0),
('January24', 2.9);

SELECT * FROM unemployment;