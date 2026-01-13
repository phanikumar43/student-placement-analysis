--sql
SELECT COUNT(*) FROM students;

-- Placement count
SELECT placed, COUNT(*)
FROM students
GROUP BY placed;

-- Average CGPA of placed students
SELECT AVG(cgpa)
FROM students
WHERE placed = 1;

-- Internship impact on placement
SELECT internship_experience, AVG(placed)
FROM students
GROUP BY internship_experience;
