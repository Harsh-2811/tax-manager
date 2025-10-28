import csv
import os
from datetime import datetime
from tax_rules import TaxRules


class TaxMaster:
    def __init__(self, sales_file="sales_database.csv"):
        self.sales_file = sales_file
        self.tax_rules = TaxRules()
        self.initialize_sales_database()

    def initialize_sales_database(self):
        if not os.path.exists(self.sales_file):
            with open(self.sales_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        "Transaction_Date",
                        "Customer_Name",
                        "Country_Code",
                        "Item_Name",
                        "Item_Rate",
                        "Item_Quantity",
                        "Item_Amount",
                        "Tax_Amount",
                        "Total_Amount",
                        "Total_Sales_Value",
                    ]
                )

                initial_data = [
                    ["2025-10-27", "test1", "INDIA", "Laptop", 45000, 1],
                    ["2025-10-27", "test2", "INDIA", "Mouse", 500, 2],
                    ["2025-10-27", "test3", "INDIA", "Mobile Phone", 25000, 1],
                    ["2025-10-27", "test4", "INDIA", "Charger", 800, 1],
                    ["2025-10-27", "test5", "USA", "Tablet", 30000, 1],
                    ["2025-10-27", "test6", "USA", "Headphones", 1500, 1],
                    ["2025-10-27", "test7", "INDIA", "Keyboard", 3500, 1],
                    ["2025-10-27", "test8", "INDIA", "Pen Drive", 600, 3],
                    ["2025-10-27", "test9", "UK", "Monitor", 15000, 1],
                    ["2025-10-27", "test10", "UK", "Cable", 200, 5],
                ]

                for record in initial_data:
                    self.write_sales_record(writer, record)

    def write_sales_record(self, writer, record):
        date, customer, country, item, rate, qty = record
        item_amount = rate * qty
        tax_rate = self.tax_rules.calculate_tax(item, rate, country)
        tax_amount = round(item_amount * tax_rate / 100, 2)
        total_amount = item_amount + tax_amount

        item_amount_str = f"{item_amount}"
        total_amount_str = f"{total_amount}"

        total_sales_value = f"{item_amount_str}, {total_amount_str}"

        writer.writerow(
            [
                date,
                customer,
                country,
                item,
                rate,
                qty,
                item_amount,
                tax_amount,
                total_amount,
                total_sales_value,
            ]
        )

    def add_transaction(
        self, customer_name, country_code, item_name, item_rate, item_quantity
    ):
        date = datetime.now().strftime("%Y-%m-%d")
        item_amount = item_rate * item_quantity
        tax_rate = self.tax_rules.calculate_tax(item_name, item_rate, country_code)
        tax_amount = round(item_amount * tax_rate / 100, 2)
        total_amount = item_amount + tax_amount

        item_amount_str = f"{item_amount}"
        total_amount_str = f"{total_amount}"

        total_sales_value = f"{item_amount_str}, {total_amount_str}"

        with open(self.sales_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    date,
                    customer_name,
                    country_code,
                    item_name,
                    item_rate,
                    item_quantity,
                    item_amount,
                    tax_amount,
                    total_amount,
                    total_sales_value,
                ]
            )

        print("Transaction added successfully!")


def main():
    tm = TaxMaster()

    while True:
        print()
        print("1. Add New Transaction")
        print("2. Update/Add Tax Rule")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            print("\n--> Add New Transaction")
            customer = input("Customer Name: ")
            country = input("Country Code: ")
            item = input("Item Name: ") or "DEFAULT"
            rate = float(input("Item Rate: "))
            qty = int(input("Item Quantity: "))
            tm.add_transaction(customer, country, item, rate, qty)

        elif choice == "2":
            print("\n--> Update/Add Tax Rule")
            item = input("Item Name (or DEFAULT): ") or "DEFAULT"
            country = input("Country Code: ")
            threshold = float(input("Rate Threshold: "))
            tax = float(input("Tax Rate (%): "))
            tm.tax_rules.update_tax_rule(item, country, threshold, tax)

        elif choice == "3":
            print("\nThank you for using Tax Master!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
