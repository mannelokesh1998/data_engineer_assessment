import json
import pymysql

# --- Load data from JSON ---
with open("./data/fake_property_data.json") as f:
    raw_data = json.load(f)

# --- Establish DB connection ---
conn = pymysql.connect(
    host='localhost',
    user='db_user',
    password='6equj5_db_user',
    database='home_db'
)
cursor = conn.cursor()

for record in raw_data:
    # --- Insert into property table ---
    cursor.execute("""
        INSERT INTO property_raw (
            property_title, address, reviewed_status, most_recent_status, source, market, occupancy, flood,
            street_address, city, state, zip, property_type, highway, train, tax_rate, sqft_basement, htw,
            pool, commercial, water, sewage, year_built, sqft_mu, sqft_total, parking, bed, bath,
            basement_yes_no, layout, net_yield, irr, rent_restricted, neighborhood_rating, latitude, longitude,
            subdivision, taxes, selling_reason, seller_retained_broker, final_reviewer, school_average
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        record.get("Property_Title"), record.get("Address"), record.get("Reviewed_Status"), record.get("Most_Recent_Status"),
        record.get("Source"), record.get("Market"), record.get("Occupancy"), record.get("Flood"),
        record.get("Street_Address"), record.get("City"), record.get("State"), record.get("Zip"), record.get("Property_Type"),
        record.get("Highway"), record.get("Train"), record.get("Tax_Rate"), record.get("SQFT_Basement"), record.get("HTW"),
        record.get("Pool"), record.get("Commercial"), record.get("Water"), record.get("Sewage"), record.get("Year_Built"),
        record.get("SQFT_MU"), record.get("SQFT_Total"), record.get("Parking"), record.get("Bed"), record.get("Bath"),
        record.get("BasementYesNo"), record.get("Layout"), record.get("Net_Yield"), record.get("IRR"),
        record.get("Rent_Restricted"), record.get("Neighborhood_Rating"), record.get("Latitude"), record.get("Longitude"),
        record.get("Subdivision"), record.get("Taxes"), record.get("Selling_Reason"), record.get("Seller_Retained_Broker"),
        record.get("Final_Reviewer"), record.get("School_Average")
    ))
    property_id = cursor.lastrowid

    # --- Insert into leads_raw ---
    cursor.execute("""
        INSERT INTO leads_raw (
            property_id, reviewed_status, most_recent_status, source, occupancy,
            net_yield, irr, selling_reason, seller_retained_broker, final_reviewer
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        property_id, record.get("Reviewed_Status"), record.get("Most_Recent_Status"),
        record.get("Source"), record.get("Occupancy"), record.get("Net_Yield"),
        record.get("IRR"), record.get("Selling_Reason"), record.get("Seller_Retained_Broker"),
        record.get("Final_Reviewer")
    ))


    # --- Insert into valuation ---
    for v in record.get("Valuation", []):
        cursor.execute("""
            INSERT INTO valuation_raw (
                property_id, list_price, previous_rent, arv, zestimate, expected_rent,
                rent_zestimate, low_fmr, high_fmr, redfin_value
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            property_id, v.get("List_Price"), v.get("Previous_Rent"), v.get("ARV"), v.get("Zestimate"),
            v.get("Expected_Rent"), v.get("Rent_Zestimate"), v.get("Low_FMR"), v.get("High_FMR"), v.get("Redfin_Value")
        ))

    # --- Insert into HOA ---
    for h in record.get("HOA", []):
        cursor.execute("""
            INSERT INTO hoa_raw (property_id, hoa, hoa_flag)
            VALUES (%s, %s, %s)
        """, (
            property_id, h.get("HOA"), h.get("HOA_Flag")
        ))

    # --- Insert into rehab ---
    for r in record.get("Rehab", []):
        cursor.execute("""
            INSERT INTO rehab_raw (
                property_id, underwriting_rehab, rehab_calculation, paint, flooring_flag,
                foundation_flag, roof_flag, hvac_flag, kitchen_flag, bathroom_flag, appliances_flag,
                windows_flag, landscaping_flag, trashout_flag
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            property_id, r.get("Underwriting_Rehab"), r.get("Rehab_Calculation"), r.get("Paint"), r.get("Flooring_Flag"),
            r.get("Foundation_Flag"), r.get("Roof_Flag"), r.get("HVAC_Flag"), r.get("Kitchen_Flag"),
            r.get("Bathroom_Flag"), r.get("Appliances_Flag"), r.get("Windows_Flag"),
            r.get("Landscaping_Flag"), r.get("Trashout_Flag")
        ))

    # --- Insert into taxes_raw ---
    if "Taxes" in record and record["Taxes"] is not None:
        cursor.execute("""
            INSERT INTO taxes_raw (property_id, taxes)
            VALUES (%s, %s)
        """, (
            property_id, record["Taxes"]
        ))

# --- Finalize ---
conn.commit()
cursor.close()
conn.close()
print("✅ All data inserted successfully.")
