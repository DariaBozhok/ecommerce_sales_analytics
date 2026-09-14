"""
Cleaning of the Customers and Order_Details tables before loading into Power BI.

Approach to missing values:
    - descriptive fields are filled with "Unknown" to preserve sample size;
    - rows without a product key or a base price are dropped, because neither
      can be imputed without distorting revenue metrics;
    - optional charges (discount, shipping, tax) are filled with 0, since a
      missing value here means the charge was not applied.
"""

import pandas as pd

CUSTOMERS_IN = "Customers.csv"
ORDERS_IN = "Order_Details.csv"
CUSTOMERS_OUT = "Customers_Cleaned.csv"
ORDERS_OUT = "Order_Details_Cleaned.csv"

TEXT_COLUMNS = ["FirstName", "LastName", "City"]


def report_missing(df, name):
    print(f"Missing values in {name}:")
    print(df.isnull().sum(), "\n")


def clean_customers(customers):
    customers["FirstName"] = customers["FirstName"].fillna("Unknown")
    customers["LastName"] = customers["LastName"].fillna("Unknown")
    customers["City"] = customers["City"].fillna("Unknown City")

    customers["Phone"] = customers["Phone"].astype(str)

    # Trim and normalise casing so the same city does not appear twice in the report
    for col in TEXT_COLUMNS:
        customers[col] = customers[col].str.strip().str.title()

    customers = customers.drop_duplicates(subset=["CustomerID"])
    customers["CustomerID"] = customers["CustomerID"].astype(int)

    return customers


def clean_orders(orders):
    # A product key and a base price cannot be recovered, so these rows are removed
    orders = orders.dropna(subset=["ProductID", "BasePrice"])

    for col in ["Discount", "ShippingCost", "Tax"]:
        orders[col] = orders[col].fillna(0)

    orders["OrderStatus"] = orders["OrderStatus"].fillna("Unknown")
    orders["OrderStatus"] = orders["OrderStatus"].str.strip().str.title()

    orders = orders.drop_duplicates(subset=["OrderDetailID"])

    int_columns = ["OrderDetailID", "OrderID", "ProductID", "Quantity"]
    float_columns = ["BasePrice", "Discount", "ShippingCost", "Tax"]

    for col in int_columns:
        orders[col] = orders[col].astype(int)
    for col in float_columns:
        orders[col] = orders[col].astype(float)

    return orders


def main():
    customers = pd.read_csv(CUSTOMERS_IN)
    orders = pd.read_csv(ORDERS_IN)

    report_missing(customers, "Customers")
    report_missing(orders, "Order_Details")

    customers = clean_customers(customers)
    orders = clean_orders(orders)

    print("Customers after cleaning:")
    print(customers.head(), "\n")
    print("Order_Details after cleaning:")
    print(orders.head(), "\n")

    customers.to_csv(CUSTOMERS_OUT, index=False)
    orders.to_csv(ORDERS_OUT, index=False)

    print(f"Done. Rows kept: {len(customers)} customers, {len(orders)} order lines.")


if __name__ == "__main__":
    main()
