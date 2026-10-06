### Task 45 – Categorised the 21 Dataset Columns

Reviewed and categorised all 21 columns of the Telco Churn dataset based on their purpose and business meaning. The columns were grouped into stable customer identity, service subscription, billing/charges, and churn outcome categories.

### Task 46 – Defined the Entities

Identified and defined the main entities required to structure the dataset into a relational database. Created five logical entities: Customers, Contracts, Services, Billing, and Customer Status, and assigned the relevant attributes to each entity.

### Task 47 – Created the Entity-Relationship Diagram

Designed the ER diagram to visually represent the entities, their attributes, and the relationships between them. Used `customer_id` as the common link between the customer-related tables and established the appropriate one-to-one relationships.

### Task 48 – Defined Primary and Foreign Keys

Defined `customer_id` as the natural primary key for the customer entity and used it as the primary/foreign key in the related tables. This structure helps maintain unique customer records and ensures referential integrity across the database.

### Task 49 – Classified Dimensions and Measures

Reviewed the dataset attributes and classified them into dimension-like and measure-like fields. Categorical fields such as Contract, Payment Method, and Internet Service were identified as dimensions, while Tenure, Monthly Charges, and Total Charges were identified as measurable numeric fields.

### Task 50 – Created the Database Tables

Converted the logical database design into SQL `CREATE TABLE` statements. Created the Customers, Contracts, Services, Billing, and Customer Status tables with appropriate data types, primary keys, and foreign key constraints.

### Task 51 – Evaluated the Database Schema

Compared the suitability of a normalised OLTP schema with a denormalised analytics schema for the Telco Churn dataset. Evaluated the benefits of reduced data duplication and data integrity in OLTP against the simpler querying and reporting advantages of a denormalised analytical structure.
