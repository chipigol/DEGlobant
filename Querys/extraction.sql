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

with amount_hired as (
	select count(id) amount, department_id
	from hired_employees
	where EXTRACT(YEAR FROM TO_TIMESTAMP(datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')) = 2021
	group by department_id
), 

avg_hired as (
	select AVG(amount) average
	from amount_hired
)

select am.department_id id, d.department, am.amount hired
from amount_hired am 
inner join avg_hired av on am.amount > av.average
inner join departments d  on am.department_id = d.id
order by am.amount desc;