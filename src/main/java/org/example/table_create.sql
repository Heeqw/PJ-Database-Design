CREATE TABLE room_utf8 (
                      kdno VARCHAR(50),
                      kcno VARCHAR(50),
                      ccno VARCHAR(50),
                      kdname VARCHAR(255),
                      exptime DATETIME,
                      papername VARCHAR(100) DEFAULT 'unknown',
                      PRIMARY KEY (kdno, kcno, ccno)
);