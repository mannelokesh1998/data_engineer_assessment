CREATE TABLE property_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    address TEXT,
    reviewed_status VARCHAR(50),
    most_recent_status VARCHAR(50),
    source VARCHAR(100),
    market VARCHAR(100),
    occupancy VARCHAR(50),
    flood VARCHAR(100),
    street_address TEXT,
    city VARCHAR(100),
    state VARCHAR(10),
    zip VARCHAR(20),
    property_type VARCHAR(100),
    highway VARCHAR(50),
    train VARCHAR(50),
    tax_rate FLOAT,
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
    net_yield FLOAT,
    irr FLOAT,
    rent_restricted VARCHAR(10),
    neighborhood_rating INT,
    latitude DOUBLE,
    longitude DOUBLE,
    subdivision VARCHAR(100),
    taxes INT,
    selling_reason TEXT,
    seller_retained_broker VARCHAR(100),
    final_reviewer VARCHAR(100),
    school_average FLOAT
);

CREATE TABLE rehab_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab INT,
    rehab_calculation INT,
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
    FOREIGN KEY (property_id) REFERENCES property_raw(id)
);

CREATE TABLE taxes_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    taxes DECIMAL(10,2),
    FOREIGN KEY (property_id) REFERENCES property_raw(id)
);

CREATE TABLE valuation_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    list_price INT,
    previous_rent INT,
    arv INT,
    zestimate INT,
    expected_rent INT,
    rent_zestimate INT,
    low_fmr INT,
    high_fmr INT,
    redfin_value INT,
    FOREIGN KEY (property_id) REFERENCES property_raw(id)
);

CREATE TABLE hoa_raw (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa INT,
    hoa_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property_raw(id)
);

