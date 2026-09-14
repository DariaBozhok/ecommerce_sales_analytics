# DAX Measures and Calculated Columns

All calculations used in the model, grouped by purpose.

---

## Base aggregations

```dax
Total Sales = SUM(Orders[OrderAmount])

Total Quantity = SUM(Order_Details[Quantity])

Total Tax = SUM(Order_Details[Tax])

Total Shipping Cost = SUM(Order_Details[ShippingCost])

Sales by Product Category = SUM(Order_Details[Line Total])

Orders Count = COUNTROWS(Orders)

Customers Count = DISTINCTCOUNT(Customers[CustomerID])
```

`Customers Count` uses `DISTINCTCOUNT` rather than `COUNTROWS`, so a customer
with several orders is counted once.

## Averages and ratios

```dax
Average Order Amount = AVERAGE(Orders[OrderAmount])

Average Quantity = AVERAGE(Order_Details[Quantity])

Sales per Customer =
DIVIDE(
    [Total Sales],
    [Customers Count]
)

Cancelled Sales Share =
DIVIDE(
    [Cancelled Sales],
    [Total Sales]
)
```

`DIVIDE` is used instead of the `/` operator so that an empty denominator
returns blank rather than an error.

## Filtered measures

```dax
Completed Sales =
CALCULATE(
    SUM(Orders[OrderAmount]),
    Orders[Delivery Status] = "Completed"
)

Cancelled Sales =
CALCULATE(
    SUM(Orders[OrderAmount]),
    Orders[Delivery Status] = "Cancelled"
)

High Sales Orders =
CALCULATE(
    SUM(Orders[OrderAmount]),
    Orders[OrderAmount] > 500
)

Big Orders Count =
CALCULATE(
    COUNTROWS(Orders),
    Orders[OrderAmount] > 1000
)
```

## Removing filter context

```dax
Sales All Cities =
CALCULATE(
    SUM(Orders[OrderAmount]),
    ALL(Customers[City])
)
```

`ALL` clears the city filter, so the measure always returns the total across
every city. Placed next to a city-level measure, it gives each city's share of
the whole.

## Conditional logic

```dax
Discount Amount =
SWITCH(
    TRUE(),
    [Total Sales] > 1000, [Total Sales] * 0.10,
    [Total Sales] >= 500, [Total Sales] * 0.05,
    0
)

Sales After Discount = [Total Sales] - [Discount Amount]

Average Check Category =
SWITCH(
    TRUE(),
    [Average Order Amount] > 500, "High",
    [Average Order Amount] > 100, "Medium",
    "Low"
)
```

`SWITCH(TRUE(), ...)` is used instead of nested `IF` statements: conditions are
evaluated top to bottom and the expression stays readable as tiers are added.

## Calculated columns

```dax
Full Name = Customers[FirstName] & " " & Customers[LastName]

Line Total = Order_Details[Quantity] * Order_Details[BasePrice]

Line Total With Tax = Order_Details[Line Total] + Order_Details[Tax]

Delivery Days =
DATEDIFF(
    Orders[OrderDate],
    Orders[ShippingDate],
    DAY
)

Order Year = YEAR(Orders[OrderDate])

Order Month = MONTH(Orders[OrderDate])

Is Big Order = IF(Orders[OrderAmount] > 1000, "Yes", "No")

Sales Category =
SWITCH(
    TRUE(),
    Orders[OrderAmount] > 500, "High",
    Orders[OrderAmount] > 100 && Orders[OrderAmount] <= 500, "Medium",
    "Low"
)

Delivery Status =
SWITCH(
    TRUE(),
    Orders[Delivery Days] <= 3, "Fast",
    Orders[Delivery Days] <= 7, "Normal",
    "Slow"
)

Price Category =
SWITCH(
    TRUE(),
    VALUE(Products[ProductPrice]) > 500, "Expensive",
    VALUE(Products[ProductPrice]) >= 100, "Medium",
    "Cheap"
)
```

These are columns rather than measures because they classify individual rows and
are used as axes and slicers, not as values.

`Line Total` is the base for most revenue calculations, so it is materialised as
a column rather than recomputed inside every measure. `Delivery Days` uses
`DATEDIFF` on the order and shipping dates and feeds the delivery speed tiers
above.

## Dynamic metric switching

```dax
Dynamic Sales =
-- paste your expression here
```

`Sales Metric` is a table that is deliberately left unrelated to the rest of the
model. The slicer built on it does not filter any data; the measure reads the
selection and returns the corresponding calculation. One card visual then serves
several metrics instead of duplicating it for each.
