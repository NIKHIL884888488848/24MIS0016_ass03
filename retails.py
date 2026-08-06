import csv
import os

# Define the product dataset matching all requested structure fields
# Structure: Product ID, Product Name, Category, Opening Stock, Units Sold, Units Returned, Supplier Lead Time, Unit Cost, Selling Price
products = [
    {"id": "P001", "name": "Laptop", "category": "Electronics", "opening_stock": 100, "units_sold": 85, "units_returned": 5, "lead_time": 5, "unit_cost": 500, "selling_price": 800},
    {"id": "P002", "name": "Smartphone", "category": "Electronics", "opening_stock": 150, "units_sold": 140, "units_returned": 10, "lead_time": 3, "unit_cost": 300, "selling_price": 500},
    {"id": "P003", "name": "Desk Chair", "category": "Furniture", "opening_stock": 50, "units_sold": 20, "units_returned": 1, "lead_time": 10, "unit_cost": 50, "selling_price": 120},
    {"id": "P004", "name": "Coffee Maker", "category": "Appliances", "opening_stock": 80, "units_sold": 75, "units_returned": 3, "lead_time": 7, "unit_cost": 40, "selling_price": 90},
    {"id": "P005", "name": "Headphones", "category": "Electronics", "opening_stock": 200, "units_sold": 190, "units_returned": 15, "lead_time": 4, "unit_cost": 25, "selling_price": 60},
    {"id": "P006", "name": "Office Desk", "category": "Furniture", "opening_stock": 30, "units_sold": 28, "units_returned": 2, "lead_time": 14, "unit_cost": 150, "selling_price": 350},
    {"id": "P007", "name": "Blender", "category": "Appliances", "opening_stock": 60, "units_sold": 15, "units_returned": 0, "lead_time": 6, "unit_cost": 30, "selling_price": 70}
]

CSV_FILENAME = "inventory_report.csv"

def run_inventory_system():
    print("=== Smart Retail Inventory and Demand Forecasting System ===\n")

    # 1. Calculate current stock
    # Formula: Current Stock = Opening Stock - Units Sold + Units Returned
    for p in products:
        p["current_stock"] = p["opening_stock"] - p["units_sold"] + p["units_returned"]

    # 2. Calculate profit for each product
    # Formula: Net Profit = (Units Sold - Units Returned) * (Selling Price - Unit Cost)
    for p in products:
        net_sold = p["units_sold"] - p["units_returned"]
        p["profit"] = net_sold * (p["selling_price"] - p["unit_cost"])

    # 3. Identify products requiring immediate reorder
    # Logic: Reorder flag triggered if current stock falls below safety threshold (e.g., 15 units)
    reorder_threshold = 15
    reorder_list = [p["name"] for p in products if p["current_stock"] <= reorder_threshold]
    print(f"1 & 3. Reorder Alerts (Stock <= {reorder_threshold}): {reorder_list}\n")

    # 4. Compute inventory turnover ratio
    # Formula: Turnover Ratio = Units Sold / Average Stock; Average Stock = (Opening + Current) / 2
    print("4. Inventory Turnover Ratios:")
    for p in products:
        avg_stock = (p["opening_stock"] + p["current_stock"]) / 2
        p["turnover_ratio"] = round(p["units_sold"] / avg_stock, 2) if avg_stock > 0 else 0.0
        print(f"   - {p['name']}: {p['turnover_ratio']}")
    print()

    # 5. Find the highest profit product
    highest_profit_prod = max(products, key=lambda x: x["profit"])
    print(f"5. Highest Profit Product: {highest_profit_prod['name']} (${highest_profit_prod['profit']})\n")

    # 6. Calculate category-wise profit
    category_profit = {}
    for p in products:
        category_profit[p["category"]] = category_profit.get(p["category"], 0) + p["profit"]
    print("6. Category-wise Profits:")
    for cat, prof in category_profit.items():
        print(f"   - {cat}: ${prof}")
    print()

    # 7. Predict next month demand using moving average logic
    # Logic: Evaluates standard movement metrics over available cycle data points
    print("7. Next Month Demand Predictions (Moving Average Logic):")
    for p in products:
        p["predicted_demand"] = round((p["opening_stock"] + p["units_sold"]) / 2)
        print(f"   - {p['name']}: {p['predicted_demand']} units")
    print()

    # 8. Sort products by profitability (descending order)
    products_sorted = sorted(products, key=lambda x: x["profit"], reverse=True)

    # 9. Export inventory report to CSV
    # Fields written dynamically matching system state structure
    fieldnames = ["id", "name", "category", "opening_stock", "units_sold", "units_returned", 
                  "lead_time", "unit_cost", "selling_price", "current_stock", "profit", 
                  "turnover_ratio", "predicted_demand"]
    
    with open(CSV_FILENAME, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for p in products_sorted:
            # Create a clean row mapping containing all targeted computational metrics
            writer.writerow({k: p[k] for k in fieldnames})
    print(f"9. Successfully exported data report to: {os.path.abspath(CSV_FILENAME)}\n")

    # 10. Read the CSV and display the top five profitable products
    print("10. Verified Top 5 Profitable Products read directly from CSV:")
    if os.path.exists(CSV_FILENAME):
        with open(CSV_FILENAME, mode="r") as file:
            reader = csv.DictReader(file)
            csv_products = list(reader)
            
            # Sort the freshly parsed strings safely converting profit strings into numerical elements
            csv_products.sort(key=lambda x: float(x["profit"]), reverse=True)
            
            for idx, row in enumerate(csv_products[:5], start=1):
                print(f"    {idx}. {row['name']} (Category: {row['category']}) -> Net Profit: ${row['profit']}")
    else:
        print("    Error: Generated CSV report file target was not found.")

if __name__ == "__main__":
    run_inventory_system()
