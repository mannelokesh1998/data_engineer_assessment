USE home_db;
SHOW TABLES;

-- Check for duplicates in property_raw and de-dup
DELETE pr
FROM property_raw pr
JOIN (
    SELECT property_title, address, MIN(id) AS min_id
    FROM property_raw
    GROUP BY property_title, address
) AS keep
ON pr.property_title = keep.property_title AND pr.address = keep.address
WHERE pr.id != keep.min_id;


-- Check for duplicates in leads_raw and de-dup
DELETE l
FROM leads_raw l
JOIN (
    SELECT property_id, MIN(id) AS min_id
    FROM leads_raw
    GROUP BY property_id
) AS keep
ON l.property_id = keep.property_id AND l.id != keep.min_id;



-- Check for duplicates in taxes_raw and de-dup
DELETE t
FROM taxes_raw t
JOIN (
    SELECT property_id, MIN(id) AS min_id
    FROM taxes_raw
    GROUP BY property_id
) AS keep
ON t.property_id = keep.property_id AND t.id != keep.min_id;


-- Check for duplicates in valuation_raw and de-dup
DELETE v
FROM valuation_raw v
JOIN (
    SELECT property_id, list_price, arv, MIN(id) AS min_id
    FROM valuation_raw
    GROUP BY property_id, list_price, arv
) AS keep
ON v.property_id = keep.property_id AND v.list_price = keep.list_price AND v.arv = keep.arv
WHERE v.id != keep.min_id;


-- Check for duplicates in hoa_raw and de-dup
DELETE h
FROM hoa_raw h
JOIN (
    SELECT property_id, hoa, hoa_flag, MIN(id) AS min_id
    FROM hoa_raw
    GROUP BY property_id, hoa, hoa_flag
) AS keep
ON h.property_id = keep.property_id AND h.hoa = keep.hoa AND h.hoa_flag = keep.hoa_flag
WHERE h.id != keep.min_id;



-- Check for duplicates in rehab_raw and de-dup
DELETE r
FROM rehab_raw r
JOIN (
    SELECT property_id, underwriting_rehab, rehab_calculation, MIN(id) AS min_id
    FROM rehab_raw
    GROUP BY property_id, underwriting_rehab, rehab_calculation
) AS keep
ON r.property_id = keep.property_id 
   AND r.underwriting_rehab = keep.underwriting_rehab 
   AND r.rehab_calculation = keep.rehab_calculation
WHERE r.id != keep.min_id;


