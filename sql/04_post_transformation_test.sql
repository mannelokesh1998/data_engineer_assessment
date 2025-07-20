-- 
SELECT property_title, count(property_title) AS duplicate_count FROM property
GROUP BY property_title
HAVING duplicate_count > 1;

SELECT property_title, count(property_title) AS occurance
FROM property
GROUP BY property_title
HAVING occurance > 1;
-- 
SELECT * FROM leads;
-- 
SELECT * FROM taxes;

SELECT * FROM valuation;

SELECT * FROM hoa;

SELECT * FROM rehab;
-- 

DROP TABLE property;

DROP TABLE leads;

DROP TABLE taxes;

DROP TABLE valuation;

DROP TABLE hoa;

DROP TABLE rehab;

USE home_db;
SHOW TABLES;

hoa      
leads
property 
rehab    
taxes    
valuation

hoa_raw      
property_raw 
rehab_raw    
taxes_raw    
valuation_raw
leads_raw
-- 
-- SHOW GRANTS FOR 'db_user'@'%';
-- 
-- GRANT ALL PRIVILEGES ON home_db.* TO 'db_user'@'%';
-- FLUSH PRIVILEGES;