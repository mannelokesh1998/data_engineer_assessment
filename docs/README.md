# Data Engineering Assessment

Welcome! This exercise evaluates your core **data-engineering** skills across SQL and Python ETL competencies.

## Table of Contents
- [Overview](#overview)
- [Prerequisites & Setup](#prerequisites--setup)
- [Problem Summary](#problem-summary)
- [Database Design](#database-design)
- [Workflow](#workflow)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Submission Guidelines](#submission-guidelines)
- [Notes](#notes)

## Overview

This assessment focuses on two key competencies:

| Competency | Focus Areas |
|------------|-------------|
| **SQL** | Relational modelling, normalisation, DDL/DML scripting |
| **Python ETL** | Data ingestion, cleaning, transformation, & loading (ELT/ETL) |

## Prerequisites & Setup

### Requirements

- **Python ≥ 3.8**
- **MySQL 8**
- **Docker & Docker Compose**

### Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```text
pymysql>=1.0.3
pandas>=1.5.0
```

> **Note:** This assessment uses lightweight helper libraries only. No ORMs or migration frameworks are used - all SQL scripts are hand-written.

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd data_engineer_assessment
   ```

2. **Start MySQL databases:**
   ```bash
   docker-compose -f docker-compose.initial.yml up --build -d
   ```

3. **Database Connections:**
   - **Initial DB:** `localhost:3306` (staging/raw data)
   - **Final DB:** `localhost:3307` (normalized schema)
   - **Credentials:** Located in `docker-compose.initial.yml`

## Problem Summary

### Input Data
- **Source:** Raw JSON file containing property records (`data/fake_property_data.json`)
- **Challenge:** Each record mixes multiple data domains in a denormalized structure

### Data Domains
The input data contains the following mixed domains:
- Property details
- Leads metadata  
- Taxes information
- Valuation history
- HOA fees
- Rehab estimates

### Objectives
Design a normalized database schema and build an ETL pipeline to:

1. **Load** raw JSON into staging tables
2. **Transform** and clean data (deduplication, validation)
3. **Load** into final normalized tables with proper relationships and foreign key constraints

## Database Design

### Normalized Schema (3NF)

The final database consists of six main tables:

| Table | Description |
|-------|-------------|
| `property` | Core property attributes |
| `leads` | Status, source, and financial metrics |
| `taxes` | Property tax information |
| `valuation` | List price, zestimate, FMR, etc. |
| `hoa` | HOA fees and flags |
| `rehab` | Rehab and renovation details |

### Relationships

```
property (1) → leads (1)     # One-to-one
property (1) → taxes (1)     # One-to-one  
property (1) → valuation (M) # One-to-many
property (1) → hoa (M)       # One-to-many
property (1) → rehab (M)     # One-to-many
```

> All foreign keys are enforced with `ON DELETE CASCADE` for referential integrity.

## Workflow

### Step 1: Create Initial Database Schema

```bash
mysql -h localhost -P 3306 -u db_user -p6equj5_db_user home_db < sql/01_initial_tables_schema.sql
```

**Creates staging tables for raw data ingestion.**

### Step 2: Load Raw JSON into Initial DB

```bash
python scripts/read_raw_file_ingest_into_initial_db.py
```

**This script:**
- Reads `data/fake_property_data.json`
- References field configuration from `data/Field Config.xlsx`
- Inserts raw data into staging tables:
  - `property_raw`
  - `valuation_raw`
  - `hoa_raw`
  - `rehab_raw`
  - `taxes_raw`

### Step 3: Data Cleaning and Pre-Processing

```bash
mysql -h localhost -P 3306 -u db_user -p6equj5_db_user home_db < sql/02_data_cleaning_test_pre_processing.sql
```

**Transformations applied:**
- Remove duplicates
- Replace NULLs with appropriate defaults
- Normalize boolean flags
- Ensure data types match final schema requirements
- Run data quality tests

### Step 4: Create Final Database Schema

```bash
mysql -h localhost -P 3307 -u db_user -p6equj5_db_user home_db < sql/03_final_tables_schema.sql
```

**Creates normalized tables in the final database.**

### Step 5: Transform and Load into Final DB

```bash
python scripts/etl_transform_to_final.py
```

**This ETL script:**
- Reads cleaned data from initial DB (port 3306)
- Transforms data according to normalized schema
- Upserts records into final DB (port 3307)
- Uses `INSERT ... ON DUPLICATE KEY UPDATE` for idempotency
- Maintains referential integrity through foreign keys

### Step 6: Post-Transformation Testing

```bash
mysql -h localhost -P 3307 -u db_user -p6equj5_db_user home_db < sql/04_post_transformation_test.sql
```

**Validates the final transformed data and relationships.**

## Project Structure

```
.
├── data/
│   ├── fake_property_data.json                  # Input JSON data
│   └── Field Config.xlsx                        # Field configuration and data types
├── scripts/
│   ├── load_initial_db.py                       # Legacy script (if needed)
│   ├── read_raw_file_ingest_into_initial_db.py  # Stage raw JSON → initial DB
│   └── etl_transform_to_final.py                # Transform & load → final DB
├── sql/
│   ├── 01_initial_tables_schema.sql             # Initial/staging table definitions
│   ├── 02_data_cleaning_test_pre_processing.sql # Data cleanup & validation
│   ├── 03_final_tables_schema.sql               # Normalized schema definitions
│   └── 04_post_transformation_test.sql          # Final data validation tests
├── requirements.txt                             # Python dependencies
├── docker-compose.initial.yml                   # Database setup
└── README.md                                    # This file
```

## Testing

### Verify Staging Data
```sql
-- Connect to initial DB (port 3306)
SELECT COUNT(*) FROM property_raw;
SELECT COUNT(*) FROM valuation_raw;
SELECT COUNT(*) FROM hoa_raw;
SELECT COUNT(*) FROM rehab_raw;
SELECT COUNT(*) FROM taxes_raw;
```

### Verify Normalized Data
```sql
-- Connect to final DB (port 3307)
SELECT COUNT(*) FROM property;
SELECT COUNT(*) FROM leads;
SELECT COUNT(*) FROM taxes;
SELECT COUNT(*) FROM valuation;
SELECT COUNT(*) FROM hoa;
SELECT COUNT(*) FROM rehab;
```

### Test Idempotency
Run the ETL pipeline multiple times to ensure no duplicates are created:
```bash
python scripts/etl_transform_to_final.py
python scripts/etl_transform_to_final.py  # Should not create duplicates
```

### Run All Tests
Execute the complete test suite:
```bash
# Pre-processing tests
mysql -h localhost -P 3306 -u db_user -p6equj5_db_user home_db < sql/02_data_cleaning_test_pre_processing.sql

# Post-transformation tests
mysql -h localhost -P 3307 -u db_user -p6equj5_db_user home_db < sql/04_post_transformation_test.sql
```

## Submission Guidelines

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/etl-cleanup
   ```

2. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Final ETL implementation and documentation"
   ```

3. **Push and create PR:**
   ```bash
   git push origin feature/etl-cleanup
   ```

4. **Create a Pull Request** on GitHub for review

## Notes

### Assumptions
- Data types and field configurations are defined in `Field Config.xlsx`
- Default values for NULL fields follow business logic assumptions
- Boolean flags are normalized to consistent format (0/1)
- SQL scripts are executed in numbered sequence (01, 02, 03, 04)

### Limitations
- Some NULL and flag handling may require further clarification from stakeholders
- Error handling could be enhanced for production use
- Data validation rules are based on sample data patterns

### Next Steps
- Add comprehensive CI/CD tests to validate ETL correctness
- Implement data quality monitoring
- Add logging and error handling improvements
- Consider adding data lineage tracking

---

## Solutions Summary

✅ **Schema Design:** Normalized to 3NF with clear one-to-many relationships  
✅ **ETL Logic:** JSON → staging → cleanup → upsert into normalized schema  
✅ **Idempotency:** Pipeline can be run multiple times safely  
✅ **Data Quality:** Deduplication and validation built into process

For questions or issues, please refer to the documentation or create an issue in the repository.
