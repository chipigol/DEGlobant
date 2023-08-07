--Number of employees hired for each job and department in 2021 divided by quarter. 
--The table must be ordered alphabetically by department and job.

SELECT
    d.department AS department,
    j.job AS job,
    SUM(CASE WHEN EXTRACT(YEAR FROM DATE(datetime)) = 2021 AND EXTRACT(QUARTER FROM DATE(datetime)) = 1 THEN 1 ELSE 0 END) AS Q1_2021,
    SUM(CASE WHEN EXTRACT(YEAR FROM DATE(datetime)) = 2021 AND EXTRACT(QUARTER FROM DATE(datetime)) = 2 THEN 1 ELSE 0 END) AS Q2_2021,
    SUM(CASE WHEN EXTRACT(YEAR FROM DATE(datetime)) = 2021 AND EXTRACT(QUARTER FROM DATE(datetime)) = 3 THEN 1 ELSE 0 END) AS Q3_2021,
    SUM(CASE WHEN EXTRACT(YEAR FROM DATE(datetime)) = 2021 AND EXTRACT(QUARTER FROM DATE(datetime)) = 4 THEN 1 ELSE 0 END) AS Q4_2021
FROM
    hired_employees he
INNER JOIN departments d ON he.department_id = d.id
INNER JOIN jobs j ON he.job_id = j.id
GROUP BY
    d.department, j.job
ORDER BY
    d.department, j.job;

--List of ids, name and number of employees hired of each department that hired more
--employees than the mean of employees hired in 2021 for all the departments, ordered
--by the number of employees hired (descending).

WITH hired_employees_2021 AS (
    SELECT *
    FROM hired_employees
    WHERE EXTRACT(YEAR FROM TO_TIMESTAMP(datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
),
employees_per_department AS (
    SELECT
        department_id,
        COUNT(id) AS num_employees_hired_2021
    FROM hired_employees_2021
    GROUP BY department_id
),
mean_employees_hired AS (
    SELECT
        AVG(num_employees_hired_2021) AS mean_employees
    FROM employees_per_department
)
SELECT
    d.id AS department_id,
    d.department AS department_name,
    COUNT(he.id) AS num_employees_hired
FROM
    hired_employees_2021 he
INNER JOIN departments d ON he.department_id = d.id
INNER JOIN mean_employees_hired m ON 1=1
WHERE
    employees_per_department.num_employees_hired_2021 > m.mean_employees
GROUP BY
    d.id, d.department
ORDER BY
    num_employees_hired DESC;
