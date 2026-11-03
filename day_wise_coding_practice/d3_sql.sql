-- Q3: SQL Employee Practice

-- 1. Display all employees
SELECT * FROM employees;


-- 2. Display employees whose salary is greater than 25000
SELECT * FROM employees
WHERE salary > 25000;

-- Salary between 20,000 and 35,000
SELECT * FROM employees
WHERE salary BETWEEN 20000 AND 35000;

-- Employees whose name starts with H
SELECT * FROM employees
WHERE name LIKE 'H%';

