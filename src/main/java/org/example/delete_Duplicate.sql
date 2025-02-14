CREATE TEMPORARY TABLE temp_student AS
SELECT DISTINCT * FROM student;
DELETE FROM student;
INSERT INTO student SELECT * FROM temp_student;
DROP TEMPORARY TABLE temp_student;

