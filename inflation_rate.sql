DROP TABLE IF EXISTS inflation;
CREATE TABLE inflation (
    month VARCHAR(12),
    inflation_rate NUMERIC(4, 2)
);

INSERT INTO inflation (month, inflation_rate)
VALUES
('January23', 0.84),
('February23', 0.46),
('March23', 0.37),
('April23', 0.38),
('May23', 0.31),
('June23', 0.37),
('July23', 0.63),
('August23', 0.28),
('September23', 0.87),
('October23', 0.83),
('November23', 1.11),
('December23', 0.73),
('January24', 0.86);

SELECT * FROM inflation;