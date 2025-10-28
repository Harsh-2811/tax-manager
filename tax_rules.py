import csv
import os


class TaxRules:
    def __init__(self, csv_file="tax_structure.csv"):
        self.csv_file = csv_file
        self.tax_rules = []
        self.load_tax_structure()

    def load_tax_structure(self):
        """Load tax structure from CSV file"""
        if not os.path.exists(self.csv_file):
            self.create_default_tax_structure()

        self.tax_rules = []
        with open(self.csv_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.tax_rules.append(
                    {
                        "item_name": row["item_name"],
                        "country_code": row["country_code"],
                        "rate_threshold": float(row["rate_threshold"]),
                        "tax_rate": float(row["tax_rate"]),
                    }
                )

    def create_default_tax_structure(self):
        """Create default tax structure CSV"""
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["item_name", "country_code", "rate_threshold", "tax_rate"])
            writer.writerow(["DEFAULT", "INDIA", "2000", "10"])

    def calculate_tax(self, item_name, item_rate, country_code):
        country_code = country_code.upper()
        item_name = item_name.upper()

        for rule in self.tax_rules:
            if (
                rule["item_name"].upper() == item_name
                and rule["country_code"].upper() == country_code
            ):
                if item_rate > rule["rate_threshold"]:
                    return rule["tax_rate"]
                else:
                    return 0.0

        for rule in self.tax_rules:
            if (
                rule["item_name"].upper() == "DEFAULT"
                and rule["country_code"].upper() == country_code
            ):
                if item_rate > rule["rate_threshold"]:
                    return rule["tax_rate"]
                else:
                    return 0.0

        return 0.0

    def save_tax_structure(self):
        """Save all tax rules back to CSV"""
        with open(self.csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["item_name", "country_code", "rate_threshold", "tax_rate"])
            for rule in self.tax_rules:
                writer.writerow(
                    [
                        rule["item_name"],
                        rule["country_code"],
                        rule["rate_threshold"],
                        rule["tax_rate"],
                    ]
                )

    def update_tax_rule(self, item_name, country_code, rate_threshold, tax_rate):
        """Update existing tax rule or add new one"""
        found = False
        for rule in self.tax_rules:
            if (
                rule["item_name"].upper() == item_name.upper()
                and rule["country_code"].upper() == country_code.upper()
            ):
                rule["rate_threshold"] = float(rate_threshold)
                rule["tax_rate"] = float(tax_rate)
                found = True
                print(f"Tax rule updated: {item_name} in {country_code}")
                break

        if not found:
            self.tax_rules.append(
                {
                    "item_name": item_name,
                    "country_code": country_code,
                    "rate_threshold": float(rate_threshold),
                    "tax_rate": float(tax_rate),
                }
            )
            print(f"New tax rule added: {item_name} in {country_code}")

        self.save_tax_structure()
