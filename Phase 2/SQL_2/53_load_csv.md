### Task 52 – Create and Load the Raw Staging Table

1. Connected to **MySQL Workbench** and selected the `customer_intelligence_labs` database.
2. Created the `stg_customer_raw` table with the **same 21 columns** as the raw CSV.
3. Defined `TotalCharges` as `VARCHAR` to preserve the raw values, including blanks/non-numeric entries.
4. Used the **Table Data Import Wizard** to load `telco_customer.csv` into the staging table.
5. Mapped the CSV columns to the corresponding table columns and skipped the CSV header.
6. Verified the imported records using `SELECT COUNT(*)` and `SELECT * ... LIMIT 10`.
7. Checked the table structure using `DESCRIBE stg_customer_raw`.
8. Confirmed that the raw data was loaded successfully without applying any transformations.

**Outcome:** Successfully created and populated `stg_customer_raw` while preserving the original CSV data for subsequent cleaning and transformation.
