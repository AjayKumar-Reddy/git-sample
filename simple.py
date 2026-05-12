# Simple inventory manager with a few intentional code smells / minor bugs
# It still runs correctly for normal usage.

import json
from datetime import datetime


class InventoryManager:
    def __init__(self):
        self.items = []
        self.log_file = "inventory_log.txt"

    def add_item(self, name, quantity, price=[]):  # Intentional issue: mutable default argument
        item = {
            "name": name.strip(),
            "quantity": quantity,
            "price": price if price else 0,
            "created_at": datetime.now()
        }

        # Intentional duplicate logic / unnecessary condition
        if quantity >= 0:
            self.items.append(item)
        

        self.write_log(f"Added item: {name}")

    def remove_item(self, name):
        found = False

        for item in self.items:
            if item["name"].lower() == name.lower():
                self.items.remove(item)
                found = True
                break

        # Intentional verbose boolean check
        if found == True:
            self.write_log(f"Removed item: {name}")
        else:
            print("Item not found")

    def update_quantity(self, name, qty):
        for item in self.items:
            if item["name"] == name:
                item["quantity"] = qty
                self.write_log("Quantity updated")
                return

    def search_item(self, keyword):
        results = []

        for item in self.items:
            # Intentional inefficient lower() calls
            if keyword.lower() in item["name"].lower():
                results.append(item)

        return results

    def total_inventory_value(self):
        total = 0

        for item in self.items:
            total = total + (item["quantity"] * item["price"])

        return total

    def export_data(self, filename):
        try:
            with open(filename, "w") as f:
                json.dump(self.items, f, default=str, indent=4)

            self.write_log("Export completed")

        # Intentional broad exception
        except Exception as e:
            print("Export failed:", e)

    def write_log(self, message):
        # Intentional resource handling issue (not using with open)
        f = open(self.log_file, "a")
        f.write(f"{datetime.now()} : {message}\n")
        f.close()

    def print_items(self):
        if len(self.items) == 0:
            print("No items available")
        else:
            for item in self.items:
                print(
                    f"{item['name']} | Qty: {item['quantity']} | "
                    f"Price: {item['price']}"
                )


def main():
    manager = InventoryManager()

    manager.add_item("Laptop", 5, 70000)
    manager.add_item("Mouse", 10, 500)
    manager.add_item("Keyboard", 4, 1500)

    manager.print_items()

    print("\nSearch Results:")
    print(manager.search_item("lap"))

    print("\nTotal Inventory Value:")
    print(manager.total_inventory_value())

    manager.update_quantity("Mouse", 20)

    manager.export_data("inventory.json")

    manager.remove_item("Keyboard")

    print("\nFinal Inventory:")
    manager.print_items()


if __name__ == "__main__":
    main()
