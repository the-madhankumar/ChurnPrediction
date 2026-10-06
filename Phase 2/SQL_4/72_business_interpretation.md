**67.Question:** What is the churn rate for each contract type?

**SQL:**

```sql
SELECT contract_type, AVG(churn) AS churn_rate
FROM fact_customer_account
JOIN dim_contract
GROUP BY contract_type
ORDER BY churn_rate DESC;
```

**Result:** All three contract types have a churn rate of **26.54%**.

**Meaning:** The result shows the same churn rate for all contract types.

---

**68.Question:** What is the churn rate for each payment method?

**SQL:**

```sql
SELECT payment_method, AVG(churn) AS churn_rate
FROM fact_customer_account
JOIN dim_payment
GROUP BY payment_method
ORDER BY churn_rate DESC;
```

**Result:** All payment methods have a churn rate of **26.54%**.

**Meaning:** The churn rate is the same for all payment methods.

---

**69.Question:** What is the average monthly charge for customers who churned and those who did not?

**SQL:**

```sql
SELECT
    CASE
        WHEN churn = 0 THEN 'Yes'
        ELSE 'No'
    END AS Churn,
    AVG(monthly_charges) AS avg_monthly_charges
FROM fact_customer_account
GROUP BY churn;
```

**Result:** Churned customers have an average monthly charge of **61.27**, while non-churned customers have **74.44**.

**Meaning:** Customers who did not churn have higher average monthly charges.

---

**70.Question:** How many customers are at high risk based on their contract, tenure, and monthly charges?

**SQL:**

```sql
SELECT COUNT(f.customer_id) AS count
FROM fact_customer_account AS f
JOIN dim_contract AS d
    ON f.contract_key = d.contract_key
WHERE d.contract_type = 'Month-to-month'
  AND f.tenure < 12
  AND f.monthly_charges > (
      SELECT AVG(monthly_charges)
      FROM fact_customer_account
  );
```

**Result:** There are **935 customers** who meet these conditions.

**Meaning:** **935 customers** are in this high-risk segment.

---

**71.Question:** How many customers have total charges above 2000, and what is their average tenure?

**SQL:**

```sql
SELECT
    COUNT(customer_id) AS count,
    AVG(tenure) AS avg_tenure
FROM fact_customer_account
WHERE total_charges > 2000;
```

**Result:** **2,856 customers** have total charges above 2000, with an average tenure of **53.07 months**.

**Meaning:** These customers have been with the company for about **53 months on average**.
