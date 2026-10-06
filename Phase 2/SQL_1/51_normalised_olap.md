1. **Normalised OLTP schema**

   * Main data is split into 5 tables:

     * Customers
     * Contracts
     * Services
     * Billing
     * Customer Status
   * It provide benefits such as reducing duplicate data, maintaining consistency, and making updates easier.

> **I would recommend a normalised OLTP schema**

| Normalised OLTP               | Denormalised Analytics             |
| ----------------------------- | ---------------------------------- |
| Less duplication              | More duplication                   |
| Better data integrity         | Faster/easier analytical queries   |
| Easier updates                | Easier reporting                   |
| More table joins              | Fewer table joins                  |
| Suitable for operational data | Suitable for analysis/dashboarding |