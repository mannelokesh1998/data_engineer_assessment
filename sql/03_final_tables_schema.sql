CREATE DATABASE IF NOT EXISTS final_db;
USE final_db;

-- Property Table
CREATE TABLE property (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    address VARCHAR(255),
    market VARCHAR(100),
    flood VARCHAR(100),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    property_type VARCHAR(100),
    highway VARCHAR(50),
    train VARCHAR(50),
    tax_rate DECIMAL(5,2),
    sqft_basement INT,
    htw VARCHAR(10),
    pool VARCHAR(10),
    commercial VARCHAR(10),
    water VARCHAR(50),
    sewage VARCHAR(50),
    year_built INT,
    sqft_mu INT,
    sqft_total INT,
    parking VARCHAR(50),
    bed INT,
    bath INT,
    basement_yes_no VARCHAR(10),
    layout VARCHAR(50),
    rent_restricted VARCHAR(10),
    neighborhood_rating INT,
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    subdivision VARCHAR(100),
    school_average DECIMAL(5,2),
    UNIQUE KEY unique_property (property_title, address)
);

-- Leads Table
CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    reviewed_status VARCHAR(50),
    most_recent_status VARCHAR(50),
    source VARCHAR(50),
    occupancy VARCHAR(50),
    net_yield DECIMAL(5,2),
    irr DECIMAL(5,2),
    selling_reason VARCHAR(255),
    seller_retained_broker VARCHAR(255),
    final_reviewer VARCHAR(100),
    UNIQUE KEY unique_leads (property_id),
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

-- Taxes Table
CREATE TABLE taxes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    taxes DECIMAL(10,2),
    UNIQUE KEY unique_taxes (property_id),
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

-- Valuation Table
CREATE TABLE valuation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    list_price DECIMAL(12,2),
    previous_rent DECIMAL(10,2),
    arv DECIMAL(12,2),
    zestimate DECIMAL(12,2),
    expected_rent DECIMAL(10,2),
    rent_zestimate DECIMAL(10,2),
    low_fmr DECIMAL(10,2),
    high_fmr DECIMAL(10,2),
    redfin_value DECIMAL(12,2),
    UNIQUE KEY unique_valuation (property_id, list_price, arv),
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

-- HOA Table
CREATE TABLE hoa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa DECIMAL(10,2),
    hoa_flag VARCHAR(10),
    UNIQUE KEY unique_hoa (property_id, hoa, hoa_flag),
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);

-- Rehab Table
CREATE TABLE rehab (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab DECIMAL(12,2),
    rehab_calculation DECIMAL(12,2),
    paint VARCHAR(10),
    flooring_flag VARCHAR(10),
    foundation_flag VARCHAR(10),
    roof_flag VARCHAR(10),
    hvac_flag VARCHAR(10),
    kitchen_flag VARCHAR(10),
    bathroom_flag VARCHAR(10),
    appliances_flag VARCHAR(10),
    windows_flag VARCHAR(10),
    landscaping_flag VARCHAR(10),
    trashout_flag VARCHAR(10),
    UNIQUE KEY unique_rehab (property_id, underwriting_rehab, rehab_calculation),
    FOREIGN KEY (property_id) REFERENCES property(id) ON DELETE CASCADE
);


-- SELECT * FROM property;
-- WHERE address IS NOT NULL;
-- 
-- DELETE FROM property;
-- DROP TABLE leads;
-- DROP TABLE property;
-- DROP TABLE taxes;
-- DROP TABLE valuation;
-- DROP TABLE hoa;
-- DROP TABLE rehab;
-- 
