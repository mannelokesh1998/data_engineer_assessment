import pymysql

# --- DB connections ---
initial_conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="db_user",
    password="6equj5_db_user",
    database="home_db"
)
final_conn = pymysql.connect(
    host="localhost",
    port=3307,
    user="db_user",
    password="6equj5_db_user",
    database="home_db"
)

initial_cursor = initial_conn.cursor(pymysql.cursors.DictCursor)
final_cursor = final_conn.cursor()

# --- Ensure unique index on property ---
try:
    final_cursor.execute("SHOW INDEX FROM property WHERE Key_name = 'unique_property'")
    index_exists = final_cursor.fetchone()
    if not index_exists:
        final_cursor.execute("""
            ALTER TABLE property 
            ADD UNIQUE KEY unique_property (property_title, address)
        """)
        final_conn.commit()
except Exception as e:
    print(f"🔧 Index check failed: {e}")

# --- Read property_raw records ---
initial_cursor.execute("SELECT * FROM property_raw")
property_records = initial_cursor.fetchall()

for record in property_records:
    try:
        # --- Upsert into property ---
        property_keys = [
            "property_title", "address", "market", "flood", "street_address", "city", "state", "zip",
            "property_type", "highway", "train", "tax_rate", "sqft_basement", "htw", "pool", "commercial",
            "water", "sewage", "year_built", "sqft_mu", "sqft_total", "parking", "bed", "bath",
            "basement_yes_no", "layout", "rent_restricted", "neighborhood_rating",
            "latitude", "longitude", "subdivision", "school_average"
        ]
        property_values = tuple(record.get(k) for k in property_keys)
        final_cursor.execute(f"""
            INSERT INTO property ({', '.join(property_keys)})
            VALUES ({', '.join(['%s'] * len(property_keys))})
            ON DUPLICATE KEY UPDATE
            {', '.join([f"{k} = VALUES({k})" for k in property_keys if k not in ['property_title', 'address']])}
        """, property_values)

        # Get property_id in final DB
        final_cursor.execute(
            "SELECT id FROM property WHERE property_title = %s AND address = %s",
            (record["property_title"], record["address"])
        )
        property_id = final_cursor.fetchone()[0]

        # --- Upsert leads ---
        final_cursor.execute("""
            INSERT INTO leads (
                property_id, reviewed_status, most_recent_status, source, occupancy,
                net_yield, irr, selling_reason, seller_retained_broker, final_reviewer
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                reviewed_status = VALUES(reviewed_status),
                most_recent_status = VALUES(most_recent_status),
                source = VALUES(source),
                occupancy = VALUES(occupancy),
                net_yield = VALUES(net_yield),
                irr = VALUES(irr),
                selling_reason = VALUES(selling_reason),
                seller_retained_broker = VALUES(seller_retained_broker),
                final_reviewer = VALUES(final_reviewer)
        """, (
            property_id, record.get("reviewed_status"), record.get("most_recent_status"),
            record.get("source"), record.get("occupancy"), record.get("net_yield"),
            record.get("irr"), record.get("selling_reason"), record.get("seller_retained_broker"),
            record.get("final_reviewer")
        ))

        # --- Upsert taxes ---
        if record.get("taxes") is not None:
            final_cursor.execute("""
                INSERT INTO taxes (property_id, taxes)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE taxes = VALUES(taxes)
            """, (property_id, record["taxes"]))

        # --- Get and upsert valuation_raw ---
        initial_cursor.execute("SELECT * FROM valuation_raw WHERE property_id = %s", (record["id"],))
        for val in initial_cursor.fetchall():
            final_cursor.execute("""
                INSERT INTO valuation (
                    property_id, list_price, previous_rent, arv, zestimate, expected_rent,
                    rent_zestimate, low_fmr, high_fmr, redfin_value
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    list_price = VALUES(list_price),
                    previous_rent = VALUES(previous_rent),
                    arv = VALUES(arv),
                    zestimate = VALUES(zestimate),
                    expected_rent = VALUES(expected_rent),
                    rent_zestimate = VALUES(rent_zestimate),
                    low_fmr = VALUES(low_fmr),
                    high_fmr = VALUES(high_fmr),
                    redfin_value = VALUES(redfin_value)
            """, (
                property_id, val.get("list_price"), val.get("previous_rent"), val.get("arv"),
                val.get("zestimate"), val.get("expected_rent"), val.get("rent_zestimate"),
                val.get("low_fmr"), val.get("high_fmr"), val.get("redfin_value")
            ))

        # --- Get and upsert hoa_raw ---
        initial_cursor.execute("SELECT * FROM hoa_raw WHERE property_id = %s", (record["id"],))
        for hoa in initial_cursor.fetchall():
            final_cursor.execute("""
                INSERT INTO hoa (property_id, hoa, hoa_flag)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    hoa = VALUES(hoa),
                    hoa_flag = VALUES(hoa_flag)
            """, (
                property_id, hoa.get("hoa"), hoa.get("hoa_flag")
            ))

        # --- Get and upsert rehab_raw ---
        initial_cursor.execute("SELECT * FROM rehab_raw WHERE property_id = %s", (record["id"],))
        for rehab in initial_cursor.fetchall():
            final_cursor.execute("""
                INSERT INTO rehab (
                    property_id, underwriting_rehab, rehab_calculation, paint,
                    flooring_flag, foundation_flag, roof_flag, hvac_flag,
                    kitchen_flag, bathroom_flag, appliances_flag,
                    windows_flag, landscaping_flag, trashout_flag
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    underwriting_rehab = VALUES(underwriting_rehab),
                    rehab_calculation = VALUES(rehab_calculation),
                    paint = VALUES(paint),
                    flooring_flag = VALUES(flooring_flag),
                    foundation_flag = VALUES(foundation_flag),
                    roof_flag = VALUES(roof_flag),
                    hvac_flag = VALUES(hvac_flag),
                    kitchen_flag = VALUES(kitchen_flag),
                    bathroom_flag = VALUES(bathroom_flag),
                    appliances_flag = VALUES(appliances_flag),
                    windows_flag = VALUES(windows_flag),
                    landscaping_flag = VALUES(landscaping_flag),
                    trashout_flag = VALUES(trashout_flag)
            """, (
                property_id, rehab.get("underwriting_rehab"), rehab.get("rehab_calculation"), rehab.get("paint"),
                rehab.get("flooring_flag"), rehab.get("foundation_flag"), rehab.get("roof_flag"), rehab.get("hvac_flag"),
                rehab.get("kitchen_flag"), rehab.get("bathroom_flag"), rehab.get("appliances_flag"),
                rehab.get("windows_flag"), rehab.get("landscaping_flag"), rehab.get("trashout_flag")
            ))

    except Exception as e:
        print(f"❌ Error processing property {record.get('address')}: {e}")
        continue

# --- Finalize ---
final_conn.commit()
initial_cursor.close()
final_cursor.close()
initial_conn.close()
final_conn.close()

print("✅ ETL process completed: All normalized data upserted into final_db.")
