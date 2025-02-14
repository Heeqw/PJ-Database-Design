CREATE TABLE room (
                           kdno VARCHAR(50),
                           kcno VARCHAR(50),
                           ccno VARCHAR(50),
                           kdname VARCHAR(255),
                           exptime DATETIME,
                           papername VARCHAR(100) DEFAULT 'unknown',
                           PRIMARY KEY (kdno, kcno, ccno)
);
CREATE TABLE student (
                         registno VARCHAR(100) PRIMARY KEY,
                         name VARCHAR(255),
                         kdno VARCHAR(50),
                         kcno VARCHAR(50),
                         ccno VARCHAR(50),
                         seat INT,
                         FOREIGN KEY (kdno,kcno,ccno) REFERENCES room(kdno,kcno,ccno)
);